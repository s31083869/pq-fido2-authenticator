export const textEncoder = new TextEncoder();

export function bufferToBase64url(buffer: ArrayBuffer): string {
  const bytes = new Uint8Array(buffer);
  let binary = "";
  bytes.forEach((b) => {
    binary += String.fromCharCode(b);
  });
  return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

export function base64urlToBuffer(value: string): ArrayBuffer {
  const padding = "=".repeat((4 - (value.length % 4)) % 4);
  const base64 = (value + padding).replace(/-/g, "+").replace(/_/g, "/");
  const raw = atob(base64);
  const buffer = new ArrayBuffer(raw.length);
  const view = new Uint8Array(buffer);
  for (let i = 0; i < raw.length; i += 1) {
    view[i] = raw.charCodeAt(i);
  }
  return buffer;
}

export function stringToBuffer(value: string): ArrayBuffer {
  return textEncoder.encode(value).buffer;
}

const HEX_RE = /^[0-9a-fA-F]+$/;
const BASE64_RE = /^[A-Za-z0-9+/]+={0,2}$/;
const BASE64URL_RE = /^[A-Za-z0-9_-]+$/;

export function binaryStringToBuffer(value: string): ArrayBuffer {
  const trimmed = value.trim();
  if (!trimmed) {
    return new ArrayBuffer(0);
  }

  if (HEX_RE.test(trimmed) && trimmed.length % 2 === 0) {
    const bytes = new Uint8Array(trimmed.length / 2);
    for (let i = 0; i < bytes.length; i += 1) {
      const index = i * 2;
      bytes[i] = Number.parseInt(trimmed.slice(index, index + 2), 16);
    }
    return bytes.buffer;
  }

  if (BASE64URL_RE.test(trimmed)) {
    try {
      return base64urlToBuffer(trimmed);
    } catch {
      // Fall through to other decoders.
    }
  }

  if (BASE64_RE.test(trimmed)) {
    try {
      return base64urlToBuffer(trimmed.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""));
    } catch {
      // Fall through to UTF-8 encoding.
    }
  }

  return stringToBuffer(trimmed);
}

export type WebAuthnCredentialJSON = {
  id: string;
  rawId: string;
  type: string;
  response: Record<string, unknown>;
};

export function serializeAttestation(credential: PublicKeyCredential): WebAuthnCredentialJSON {
  const response =
    credential.response as AuthenticatorAttestationResponse &
      Partial<{
        publicKey: ArrayBuffer | string;
        publicKeyAlgorithm: number;
        authenticatorData: ArrayBuffer | string;
        credentialId: string;
        transports: string[];
        getPublicKey: () => ArrayBuffer | null;
        getPublicKeyAlgorithm: () => number | null;
        getAuthenticatorData: () => ArrayBuffer;
        getTransports: () => string[];
      }>;

  const publicKey = response.publicKey ?? response.getPublicKey?.() ?? undefined;
  const publicKeyAlgorithm =
    response.publicKeyAlgorithm ?? response.getPublicKeyAlgorithm?.() ?? undefined;
  const authenticatorData =
    response.authenticatorData ?? response.getAuthenticatorData?.() ?? undefined;
  const transports = response.transports ?? response.getTransports?.() ?? undefined;

  const enriched: Record<string, unknown> = {
    clientDataJSON: bufferToBase64url(response.clientDataJSON),
    attestationObject: bufferToBase64url(response.attestationObject),
  };

  if (authenticatorData) {
    enriched.authenticatorData =
      typeof authenticatorData === "string"
        ? authenticatorData
        : bufferToBase64url(authenticatorData);
  }
  if (publicKey) {
    enriched.publicKey =
      typeof publicKey === "string"
        ? publicKey
        : bufferToBase64url(publicKey);
  }
  if (typeof publicKeyAlgorithm === "number") {
    enriched.publicKeyAlgorithm = publicKeyAlgorithm;
  }
  if (response.credentialId) {
    enriched.credentialId = response.credentialId;
  }
  if (transports?.length) {
    enriched.transports = transports;
  }

  return {
    id: credential.id,
    rawId: bufferToBase64url(credential.rawId),
    type: credential.type,
    response: enriched,
  };
}

export function serializeAssertion(credential: PublicKeyCredential): WebAuthnCredentialJSON {
  const response =
    credential.response as AuthenticatorAssertionResponse &
      Partial<{ signature: ArrayBuffer | string; authenticatorData: ArrayBuffer | string; clientDataJSON: ArrayBuffer | string }>;

  const encodeField = (value: ArrayBuffer | string | undefined) => {
    if (!value) return undefined;
    if (typeof value === "string") return value;
    return bufferToBase64url(value);
  };

  return {
    id: credential.id,
    rawId: bufferToBase64url(credential.rawId),
    type: credential.type,
    response: {
      clientDataJSON: encodeField(response.clientDataJSON)!,
      authenticatorData: encodeField(response.authenticatorData)!,
      signature: encodeField(response.signature)!,
      userHandle:
        typeof response.userHandle === "string"
          ? response.userHandle
          : response.userHandle
            ? bufferToBase64url(response.userHandle)
            : undefined,
    },
  };
}
