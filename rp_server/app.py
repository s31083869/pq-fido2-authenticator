"""Flask application exposing RP endpoints."""

from __future__ import annotations

import json
import logging
import secrets

from flask import Flask, jsonify, request
from flask_cors import CORS

from .challenges import ChallengeCache
from .config import RPSettings
from .database import Database
from .schemas import (
    AuthenticateOptionsRequest,
    AuthenticateOptionsResponse,
    AuthenticateVerifyRequest,
    RegisterOptionsRequest,
    RegisterOptionsResponse,
    RegisterVerifyRequest,
    RPResponse,
)
from .services import (
    ensure_user,
    get_user,
    new_user_handle,
    list_credentials,
    store_credential,
    verify_authentication_payload,
    verify_registration_payload,
)

LOGGER = logging.getLogger(__name__)

STAGE_LABELS = {
    "register": "Register",
    "authn": "Authenticate",
}

EVENT_LABELS = {
    ("register", "options.start"): "Creating Register Options",
    ("register", "user.resolve"): "Resolved registration user handle",
    ("register", "options.success"): "Issued Register Options",
    ("register", "verify.start"): "Verifying Registration",
    ("register", "verify.expired"): "Registration Challenge Expired",
    ("register", "verify.success"): "Registration Completed",
    ("authn", "options.start"): "Creating Authentication Options",
    ("authn", "options.unknown_user"): "Authentication Unknown User",
    ("authn", "options.no_credentials"): "Authentication User Has No Credentials",
    ("authn", "options.success"): "Issued Authentication Options",
    ("authn", "verify.start"): "Verifying Authentication",
    ("authn", "verify.expired"): "Authentication Challenge Expired",
    ("authn", "verify.unknown_user"): "Authentication Unknown User",
    ("authn", "verify.success"): "Authentication Completed",
}


def _truncate(value: str, limit: int = 64) -> str:
    if len(value) <= limit:
        return value
    half = limit // 2
    return f"{value[:half]}…{value[-half:]}"


def _build_payload(req: str, **fields: object) -> dict[str, object]:
    payload: dict[str, object] = {"request_id": req}
    for key, value in fields.items():
        if value is None:
            continue
        if isinstance(value, str):
            payload[key] = _truncate(value)
        else:
            payload[key] = value
    return payload


def _log(stage: str, event: str, req: str, level: int = logging.INFO, **fields: object) -> None:
    stage_label = STAGE_LABELS.get(stage, stage.title())
    event_label = EVENT_LABELS.get((stage, event), event)
    payload = json.dumps(_build_payload(req, **fields), indent=2, sort_keys=True)
    message = f"[RP Server: {stage_label}]: {event_label}\n{payload}"
    LOGGER.log(level, message)


def create_app(settings: RPSettings | None = None) -> Flask:
    settings = settings or RPSettings()
    db = Database(settings)
    db.create_all()
    challenge_cache = ChallengeCache()

    app = Flask(__name__)
    CORS(app)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logging.getLogger("werkzeug").setLevel(logging.WARNING)

    @app.post("/register/options")
    def register_options():
        payload = RegisterOptionsRequest.model_validate(request.get_json() or {})
        req_id = secrets.token_hex(4)
        _log("register", "options.start", req_id, user=payload.username, display=payload.display_name)
        with db.session() as session:
            user = get_user(session, payload.username)
            if user:
                user_handle = user.user_handle
                credentials = list_credentials(session, user)
            else:
                user_handle = new_user_handle(session)
                credentials = []
            _log("register", "user.resolve", req_id, user_id=user.id if user else None, user_handle=user_handle)
        challenge = challenge_cache.issue(
            "register",
            payload.username,
            metadata={
                "display_name": payload.display_name,
                "user_handle": user_handle,
            },
        )
        response = RegisterOptionsResponse(
            challenge=challenge,
            rp={"id": settings.rp_id, "name": settings.rp_name},
            user={
                "id": user_handle,
                "name": payload.username,
                "displayName": payload.display_name,
            },
            pubKeyCredParams=[
                {"type": "public-key", "alg": alg} for alg in settings.hosted_algorithms
            ],
            timeout=90_000,
            authenticatorSelection={
                "requireResidentKey": False,
                "residentKey": "discouraged",
                "userVerification": "preferred",
            },
            extensions={"credProps": True},
            excludeCredentials=[
                {"id": cred.id, "type": "public-key", "transports": ["internal"]}
                for cred in credentials
            ],
        )
        _log(
            "register",
            "options.success",
            req_id,
            user=payload.username,
            user_handle=user_handle,
            credential_count=len(credentials),
        )
        return jsonify(RPResponse(success=True, data=response.model_dump()).model_dump())

    @app.post("/register/verify")
    def register_verify():
        payload = RegisterVerifyRequest.model_validate(request.get_json() or {})
        req_id = secrets.token_hex(4)
        _log("register", "verify.start", req_id, user=payload.username)
        challenge_record = challenge_cache.pop_record("register", payload.username)
        if not challenge_record:
            _log("register", "verify.expired", req_id, user=payload.username, level=logging.WARNING)
            return jsonify(RPResponse(success=False, message="Challenge expired").model_dump()), 400
        credential_id, algorithm, public_key = verify_registration_payload(
            payload.credential,
            challenge_record.challenge,
            settings,
        )
        with db.session() as session:
            user = get_user(session, payload.username)
            if not user:
                user = ensure_user(
                    session,
                    payload.username,
                    challenge_record.metadata.get("display_name", payload.username),
                    user_handle=challenge_record.metadata.get("user_handle"),
                )
            elif user.display_name != challenge_record.metadata.get("display_name", user.display_name):
                user.display_name = challenge_record.metadata.get("display_name", user.display_name)
            store_credential(session, user, credential_id, public_key, algorithm)
            _log(
                "register",
                "verify.success",
                req_id,
                user=payload.username,
                user_handle=user.user_handle,
                credential_id=credential_id,
                algorithm=algorithm,
        )
        return jsonify(RPResponse(success=True).model_dump())

    @app.post("/authenticate/options")
    def authenticate_options():
        payload = AuthenticateOptionsRequest.model_validate(request.get_json() or {})
        req_id = secrets.token_hex(4)
        _log("authn", "options.start", req_id, user=payload.username)
        with db.session() as session:
            user = get_user(session, payload.username)
            if not user:
                _log(
                    "authn",
                    "options.unknown_user",
                    req_id,
                    user=payload.username,
                    level=logging.WARNING,
                )
                return (
                    jsonify(
                        RPResponse(success=False, message="Unknown user").model_dump()
                    ),
                    400,
                )
            credentials = list_credentials(session, user)
            if not credentials:
                _log(
                    "authn",
                    "options.no_credentials",
                    req_id,
                    user=payload.username,
                    level=logging.WARNING,
                )
                return (
                    jsonify(
                        RPResponse(success=False, message="No credential registered").model_dump()
                    ),
                    400,
                )
        challenge = challenge_cache.issue("authenticate", payload.username)
        response = AuthenticateOptionsResponse(
            challenge=challenge,
            rpId=settings.rp_id,
            allowCredentials=[
                {"id": cred.id, "type": "public-key", "transports": ["internal"]}
                for cred in credentials
            ],
            timeout=90_000,
        )
        _log(
            "authn",
            "options.success",
            req_id,
            user=payload.username,
            credential_count=len(credentials),
        )
        return jsonify(RPResponse(success=True, data=response.model_dump()).model_dump())

    @app.post("/authenticate/verify")
    def authenticate_verify():
        payload = AuthenticateVerifyRequest.model_validate(request.get_json() or {})
        req_id = secrets.token_hex(4)
        _log("authn", "verify.start", req_id, user=payload.username)
        challenge = challenge_cache.pop("authenticate", payload.username)
        if not challenge:
            _log("authn", "verify.expired", req_id, user=payload.username, level=logging.WARNING)
            return jsonify(RPResponse(success=False, message="Challenge expired").model_dump()), 400
        with db.session() as session:
            user = get_user(session, payload.username)
            if not user:
                _log(
                    "authn",
                    "verify.unknown_user",
                    req_id,
                    user=payload.username,
                    level=logging.WARNING,
                )
                return (
                    jsonify(
                        RPResponse(success=False, message="Unknown user").model_dump()
                    ),
                    400,
                )
            credential = verify_authentication_payload(
                session,
                payload.credential,
                challenge,
                settings,
                user,
            )
            session.add(credential)
            _log(
                "authn",
                "verify.success",
                req_id,
                user=payload.username,
                credential_id=credential.id,
                sign_count=credential.sign_count,
            )
        return jsonify(RPResponse(success=True).model_dump())

    @app.errorhandler(400)
    def handle_bad_request(error):
        message = getattr(error, "description", "Bad Request")
        return (
            jsonify(
                RPResponse(success=False, message=message).model_dump()
            ),
            400,
        )

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
