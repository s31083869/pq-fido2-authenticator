"""Platform user verification helpers."""

from __future__ import annotations

import asyncio
import logging
import threading
import time
from typing import Protocol

LOGGER = logging.getLogger(__name__)


class UserVerificationError(RuntimeError):
    pass


class UserVerifier(Protocol):
    def verify_user(self, prompt: str | None = None) -> bool:
        ...


class TouchIDVerifier:
    def __init__(self, reason: str = "Authenticate with Touch ID", timeout: int = 30) -> None:
        self.reason = reason
        self.timeout = timeout

    def verify_user(self, prompt: str | None = None) -> bool:
        message = prompt or self.reason
        try:
            from LocalAuthentication import (
                LAPolicyDeviceOwnerAuthenticationWithBiometrics,
                LAContext,
            )
            from Foundation import NSDate, NSRunLoop
        except Exception as exc:  # pragma: no cover - only hit on non-macOS
            raise UserVerificationError(
                "Touch ID is unavailable on this platform."
            ) from exc

        context = LAContext.alloc().init()
        success, error = context.canEvaluatePolicy_error_(
            LAPolicyDeviceOwnerAuthenticationWithBiometrics, None
        )
        if not success:
            raise UserVerificationError(f"Touch ID unavailable: {error}")

        result_holder = {"done": False, "success": False, "error": None}

        def handler(result: bool, err) -> None:
            result_holder["done"] = True
            result_holder["success"] = bool(result)
            result_holder["error"] = err

        context.evaluatePolicy_localizedReason_reply_(
            LAPolicyDeviceOwnerAuthenticationWithBiometrics, message, handler
        )

        run_loop = NSRunLoop.currentRunLoop()
        deadline = time.time() + self.timeout
        while not result_holder["done"] and time.time() < deadline:
            run_loop.runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.1))

        if not result_holder["done"]:
            raise UserVerificationError("Touch ID timed out. Please try again.")
        if not result_holder["success"]:
            raise UserVerificationError("Touch ID verification failed")
        return True


class WindowsHelloVerifier:
    def __init__(
        self,
        reason: str = "Authenticate with Windows Hello",
        timeout: int = 30,
    ) -> None:
        self.reason = reason
        self.timeout = timeout

    def verify_user(self, prompt: str | None = None) -> bool:
        message = prompt or self.reason
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            asyncio.run(self._verify_user_async(message))
            return True

        error_holder: dict[str, BaseException] = {}

        def runner() -> None:
            try:
                asyncio.run(self._verify_user_async(message))
            except BaseException as exc:  # pragma: no cover - defensive event-loop bridge
                error_holder["error"] = exc

        thread = threading.Thread(target=runner, daemon=True)
        thread.start()
        thread.join()
        if "error" in error_holder:
            raise error_holder["error"]
        return True

    async def _verify_user_async(self, message: str) -> None:
        try:
            (
                UserConsentVerifier,
                UserConsentVerificationResult,
                UserConsentVerifierAvailability,
            ) = _load_windows_hello_api()
        except Exception as exc:  # pragma: no cover - platform/package dependent
            raise UserVerificationError(
                "Windows Hello verifier requires the Python WinRT projection. "
                "Install the optional Windows dependency, for example: "
                "uv add \"winsdk>=1.0.0b10; sys_platform == 'win32'\""
            ) from exc

        availability = await UserConsentVerifier.check_availability_async()
        if not _enum_is(availability, UserConsentVerifierAvailability, "available"):
            raise UserVerificationError(
                f"Windows Hello is unavailable: {_enum_label(availability)}"
            )

        try:
            result = await asyncio.wait_for(
                UserConsentVerifier.request_verification_async(message),
                timeout=self.timeout,
            )
        except asyncio.TimeoutError as exc:
            raise UserVerificationError("Windows Hello timed out. Please try again.") from exc
        if not _enum_is(result, UserConsentVerificationResult, "verified"):
            raise UserVerificationError(
                f"Windows Hello verification failed: {_enum_label(result)}"
            )


def _load_windows_hello_api():
    try:
        from winsdk.windows.security.credentials.ui import (
            UserConsentVerifier,
            UserConsentVerificationResult,
            UserConsentVerifierAvailability,
        )
    except ImportError:
        from winrt.windows.security.credentials.ui import (
            UserConsentVerifier,
            UserConsentVerificationResult,
            UserConsentVerifierAvailability,
        )

    return (
        UserConsentVerifier,
        UserConsentVerificationResult,
        UserConsentVerifierAvailability,
    )


def _enum_label(value: object) -> str:
    name = getattr(value, "name", None)
    if isinstance(name, str):
        return name
    return str(value)


def _enum_is(value: object, enum_type: object, expected_name: str) -> bool:
    expected = getattr(enum_type, expected_name.upper(), None)
    if expected is not None:
        return value == expected
    return _enum_label(value).lower().endswith(expected_name.lower())


class NoopVerifier:
    """User verifier that unconditionally succeeds (useful on non-macOS)."""

    def verify_user(self, prompt: str | None = None) -> bool:
        LOGGER.info("Skipping user verification: NoopVerifier in use")
        return True


class DummyVerifier:
    """Simple verifier that always prompts via CLI."""

    def verify_user(self, prompt: str | None = None) -> bool:
        msg = prompt or "Confirm authenticator action"
        answer = input(f"{msg} (y/N): ")
        if answer.strip().lower() == "y":
            return True
        raise UserVerificationError("User declined")
