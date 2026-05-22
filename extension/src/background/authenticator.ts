import { encodeCbor } from "@/lib/cbor";
import { base64UrlToBytes, bytesToBase64Url } from "@/lib/base64url";
import { concatBytes, decodeStringBinary, equalBytes } from "@/lib/binary";
import { sha256 } from "@/lib/hash";
import {
  type AuthenticationResponsePayload,
  type CreationRequestPayload,
  type PersistedCredential,
  type RegistrationResponsePayload,
  type RequestRequestPayload,
  type Settings,
  type SupportedAlg
} from "@/types/messages";
import type { PQSigner } from "./pq-signer";
import { LiboqsWasmSigner } from "./liboqs-wasm-signer";
import { verifyNativeUserVerification } from "./native-uv";
import { listCredentials, upsertCredential } from "./store";

const SUPPORTED_ALGORITHMS = new Set<number>([-48, -49, -50]);
const AAGUID = new Uint8Array(16);

export class WebAuthnError extends Error {
  constructor(public readonly name: string, message: string) {
    super(message);
  }
}

function ensure(condition: unknown, name: string, message: string): asserts condition {
  if (!condition) {
    throw new WebAuthnError(name, message);
  }
}

function toSupportedAlg(alg: number): SupportedAlg {
  if (alg === -48 || alg === -49 || alg === -50) {
    return alg;
  }
  throw new WebAuthnError("NotSupportedError", `Unsupported algorithm: ${alg}`);
}

function selectAlgorithm(
  params: Array<{ type: "public-key"; alg: number }> | undefined,
  defaultAlgorithm: SupportedAlg
): SupportedAlg {
  if (!params || params.length === 0) {
    return defaultAlgorithm;
  }

  for (const param of params) {
    if (param.type === "public-key" && SUPPORTED_ALGORITHMS.has(param.alg)) {
      return toSupportedAlg(param.alg);
    }
  }

  throw new WebAuthnError("NotSupportedError", "No supported algorithm in pubKeyCredParams");
}

function uint32ToBytes(value: number): Uint8Array {
  return new Uint8Array([
    (value >> 24) & 0xff,
    (value >> 16) & 0xff,
    (value >> 8) & 0xff,
    value & 0xff
  ]);
}

function credentialPublicKeyCose(algorithm: SupportedAlg, publicKey: Uint8Array): Uint8Array {
  const map = new Map<number, number | string | Uint8Array>();
  // ML-DSA COSE representation uses AKP key type.
  // 1: kty=7 (AKP), 3: alg, -1: pub
  map.set(1, 7);
  map.set(3, algorithm);
  map.set(-1, publicKey);
  return encodeCbor(map);
}

function randomBytes(size: number): Uint8Array {
  const bytes = new Uint8Array(size);
  crypto.getRandomValues(bytes);
  return bytes;
}

async function rpIdHash(rpId: string): Promise<Uint8Array> {
  return sha256(new TextEncoder().encode(rpId));
}

async function buildClientDataJSON(
  type: "webauthn.create" | "webauthn.get",
  challenge: Uint8Array,
  origin: string
): Promise<Uint8Array> {
  const payload = {
    type,
    challenge: bytesToBase64Url(challenge),
    origin,
    crossOrigin: false
  };
  return new TextEncoder().encode(JSON.stringify(payload));
}

function originHost(origin: string): string {
  try {
    return new URL(origin).hostname;
  } catch {
    throw new WebAuthnError("SecurityError", "Invalid origin");
  }
}

function ensureRpIdMatchesOrigin(rpId: string, origin: string): void {
  const host = originHost(origin);
  if (rpId !== host) {
    throw new WebAuthnError("SecurityError", `rpId mismatch: ${rpId} vs ${host}`);
  }
}

function createAuthData(
  rpHash: Uint8Array,
  flags: number,
  signCount: number,
  attested?: {
    credentialId: Uint8Array;
    credentialPublicKey: Uint8Array;
  }
): Uint8Array {
  const head = concatBytes(rpHash, new Uint8Array([flags]), uint32ToBytes(signCount));
  if (!attested) {
    return head;
  }

  const idLen = new Uint8Array([(attested.credentialId.length >> 8) & 0xff, attested.credentialId.length & 0xff]);
  return concatBytes(head, AAGUID, idLen, attested.credentialId, attested.credentialPublicKey);
}

async function performUserVerification(
  settings: Settings,
  context: {
    operation: "create" | "get";
    rpId: string;
    origin: string;
  }
): Promise<void> {
  if (!settings.enabled) {
    throw new WebAuthnError("NotAllowedError", "Extension is disabled");
  }

  if (settings.uvMode === "soft-auto") {
    // UV intentionally deferred in soft-auto mode.
    return;
  }

  if (settings.uvMode === "native-touch-id" || settings.uvMode === "native-windows-hello") {
    try {
      await verifyNativeUserVerification({
        mode: settings.uvMode,
        operation: context.operation,
        rpId: context.rpId,
        origin: context.origin
      });
      return;
    } catch (error) {
      if (error instanceof Error) {
        throw new WebAuthnError(error.name || "NotAllowedError", error.message);
      }
      throw new WebAuthnError("NotAllowedError", "Touch ID verification failed");
    }
  }

  // Exhaustive guard for future uvMode variants.
  {
    const neverMode: never = settings.uvMode;
    void neverMode;
    throw new WebAuthnError("NotAllowedError", "Unsupported UV mode");
  }
}

function normalizeId(value: string): Uint8Array {
  return decodeStringBinary(value);
}

function pickCredentialForAssertion(
  credentials: PersistedCredential[],
  rpId: string,
  allowCredentials?: Array<{ type: "public-key"; id: string }>
): PersistedCredential {
  const rpCredentials = credentials.filter((credential) => credential.rpId === rpId);

  if (allowCredentials && allowCredentials.length > 0) {
    for (const descriptor of allowCredentials) {
      const descriptorBytes = normalizeId(descriptor.id);
      const matched = rpCredentials.find((record) => {
        const recordId = base64UrlToBytes(record.credentialId);
        return equalBytes(recordId, descriptorBytes);
      });
      if (matched) {
        return matched;
      }
    }
    throw new WebAuthnError("NotAllowedError", "No credential matched allowCredentials");
  }

  const first = rpCredentials[0];
  if (!first) {
    throw new WebAuthnError("NotAllowedError", "No credential available for rpId");
  }

  return first;
}

export class PQAuthenticator {
  private signer: PQSigner;

  constructor(signer: PQSigner = new LiboqsWasmSigner()) {
    this.signer = signer;
  }

  async makeCredential(
    payload: CreationRequestPayload,
    settings: Settings
  ): Promise<RegistrationResponsePayload> {
    ensure(payload?.publicKey, "TypeError", "Missing publicKey options");

    const { publicKey } = payload;
    ensure(publicKey.rp?.id, "TypeError", "Missing publicKey.rp.id");
    ensure(publicKey.user?.id, "TypeError", "Missing publicKey.user.id");
    ensure(publicKey.challenge, "TypeError", "Missing publicKey.challenge");
    ensure(publicKey.pubKeyCredParams?.length, "TypeError", "Missing publicKey.pubKeyCredParams");

    const rpId = publicKey.rp.id;
    ensureRpIdMatchesOrigin(rpId, payload.origin);
    const challengeBytes = decodeStringBinary(publicKey.challenge);
    const userHandleBytes = decodeStringBinary(publicKey.user.id);
    const selectedAlgorithm = selectAlgorithm(publicKey.pubKeyCredParams, settings.defaultAlgorithm);

    const credentials = await listCredentials();
    for (const descriptor of publicKey.excludeCredentials ?? []) {
      const descriptorId = normalizeId(descriptor.id);
      const dup = credentials.find((record) => {
        if (record.rpId !== rpId) {
          return false;
        }
        return equalBytes(base64UrlToBytes(record.credentialId), descriptorId);
      });
      if (dup) {
        throw new WebAuthnError("InvalidStateError", "Credential already exists");
      }
    }

    await performUserVerification(settings, {
      operation: "create",
      rpId,
      origin: payload.origin
    });

    const { publicKey: generatedPublicKey, privateKey } = await this.signer.generateKeyPair(selectedAlgorithm);
    const credentialIdBytes = randomBytes(32);
    const credentialId = bytesToBase64Url(credentialIdBytes);

    const cosePublicKey = credentialPublicKeyCose(selectedAlgorithm, generatedPublicKey);
    const rpHash = await rpIdHash(rpId);
    const authData = createAuthData(rpHash, 0x45, 0, {
      credentialId: credentialIdBytes,
      credentialPublicKey: cosePublicKey
    });

    const clientDataJSON = await buildClientDataJSON("webauthn.create", challengeBytes, payload.origin);
    const attestationObject = encodeCbor({
      fmt: "none",
      authData,
      attStmt: {}
    });

    const record: PersistedCredential = {
      credentialId,
      rpId,
      userHandle: bytesToBase64Url(userHandleBytes),
      publicKey: bytesToBase64Url(generatedPublicKey),
      privateKey: bytesToBase64Url(privateKey),
      algorithm: selectedAlgorithm,
      signCount: 0,
      createdAt: new Date().toISOString()
    };

    await upsertCredential(record);

    const includeCredProps = payload.publicKey.extensions?.credProps === true;
    const clientExtensionResults = includeCredProps ? { credProps: { rk: false } } : {};

    return {
      id: credentialId,
      rawId: credentialId,
      type: "public-key",
      authenticatorAttachment: "platform",
      clientExtensionResults,
      response: {
        clientDataJSON: bytesToBase64Url(clientDataJSON),
        attestationObject: bytesToBase64Url(attestationObject),
        authenticatorData: bytesToBase64Url(authData),
        publicKeyAlgorithm: selectedAlgorithm,
        publicKey: bytesToBase64Url(generatedPublicKey),
        transports: ["internal"]
      }
    };
  }

  async getAssertion(
    payload: RequestRequestPayload,
    settings: Settings
  ): Promise<AuthenticationResponsePayload> {
    ensure(payload?.publicKey, "TypeError", "Missing publicKey options");
    ensure(payload.publicKey.challenge, "TypeError", "Missing publicKey.challenge");

    const rpId = payload.publicKey.rpId ?? originHost(payload.origin);
    ensureRpIdMatchesOrigin(rpId, payload.origin);
    const challengeBytes = decodeStringBinary(payload.publicKey.challenge);
    const credentials = await listCredentials();
    const selected = pickCredentialForAssertion(credentials, rpId, payload.publicKey.allowCredentials);

    await performUserVerification(settings, {
      operation: "get",
      rpId,
      origin: payload.origin
    });

    const rpHash = await rpIdHash(rpId);
    const clientDataJSON = await buildClientDataJSON("webauthn.get", challengeBytes, payload.origin);
    const clientDataHash = await sha256(clientDataJSON);

    const nextSignCount = selected.signCount + 1;
    const authData = createAuthData(rpHash, 0x05, nextSignCount);
    const signingInput = concatBytes(authData, clientDataHash);

    const signature = await this.signer.sign(
      selected.algorithm,
      base64UrlToBytes(selected.privateKey),
      signingInput
    );

    selected.signCount = nextSignCount;
    await upsertCredential(selected);

    return {
      id: selected.credentialId,
      rawId: selected.credentialId,
      type: "public-key",
      authenticatorAttachment: "platform",
      clientExtensionResults: {},
      response: {
        clientDataJSON: bytesToBase64Url(clientDataJSON),
        authenticatorData: bytesToBase64Url(authData),
        signature: bytesToBase64Url(signature),
        userHandle: selected.userHandle
      }
    };
  }
}
