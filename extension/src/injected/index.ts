import { base64UrlToBytes } from "@/lib/base64url";
import { isBinaryLike, toBase64Url } from "@/lib/binary";

const REQUEST_SOURCE = "PQ_WEBAUTHN_INJECTED";
const RESPONSE_SOURCE = "PQ_WEBAUTHN_CONTENT";
const HOOK_FLAG = "__pqWebAuthnHookInstalled";

type BridgeAction = "create" | "get";

function randomId(): string {
  return crypto.randomUUID();
}

function arrayBuffer(value: Uint8Array): ArrayBuffer {
  const copy = new Uint8Array(value.byteLength);
  copy.set(value);
  return copy.buffer;
}

function serializeDescriptor(descriptor: PublicKeyCredentialDescriptor) {
  return {
    type: descriptor.type,
    id: isBinaryLike(descriptor.id) ? toBase64Url(descriptor.id) : String(descriptor.id),
    transports: descriptor.transports
  };
}

function serializeCreateOptions(publicKey: PublicKeyCredentialCreationOptions) {
  return {
    rp: {
      id: publicKey.rp.id,
      name: publicKey.rp.name
    },
    user: {
      id: toBase64Url(publicKey.user.id),
      name: publicKey.user.name,
      displayName: publicKey.user.displayName
    },
    challenge: toBase64Url(publicKey.challenge),
    pubKeyCredParams: (publicKey.pubKeyCredParams ?? []).map((param) => ({
      type: param.type,
      alg: param.alg
    })),
    timeout: publicKey.timeout,
    excludeCredentials: (publicKey.excludeCredentials ?? []).map((descriptor) =>
      serializeDescriptor(descriptor)
    ),
    authenticatorSelection: publicKey.authenticatorSelection,
    attestation: publicKey.attestation,
    extensions: publicKey.extensions as Record<string, unknown> | undefined
  };
}

function serializeGetOptions(publicKey: PublicKeyCredentialRequestOptions) {
  return {
    challenge: toBase64Url(publicKey.challenge),
    timeout: publicKey.timeout,
    rpId: publicKey.rpId,
    allowCredentials: (publicKey.allowCredentials ?? []).map((descriptor) =>
      serializeDescriptor(descriptor)
    ),
    userVerification: publicKey.userVerification,
    extensions: publicKey.extensions as Record<string, unknown> | undefined
  };
}

function createAttestationResponse(payload: any): AuthenticatorAttestationResponse {
  const response: any = {
    clientDataJSON: arrayBuffer(base64UrlToBytes(payload.clientDataJSON)),
    attestationObject: arrayBuffer(base64UrlToBytes(payload.attestationObject)),
    getPublicKey: () =>
      payload.publicKey ? arrayBuffer(base64UrlToBytes(payload.publicKey)) : null,
    getPublicKeyAlgorithm: () => payload.publicKeyAlgorithm ?? null,
    getAuthenticatorData: () => arrayBuffer(base64UrlToBytes(payload.authenticatorData)),
    getTransports: () => payload.transports ?? []
  };

  return response as AuthenticatorAttestationResponse;
}

function createAssertionResponse(payload: any): AuthenticatorAssertionResponse {
  const response: any = {
    clientDataJSON: arrayBuffer(base64UrlToBytes(payload.clientDataJSON)),
    authenticatorData: arrayBuffer(base64UrlToBytes(payload.authenticatorData)),
    signature: arrayBuffer(base64UrlToBytes(payload.signature)),
    userHandle: payload.userHandle ? arrayBuffer(base64UrlToBytes(payload.userHandle)) : null
  };

  return response as AuthenticatorAssertionResponse;
}

function buildCredential(payload: any): PublicKeyCredential {
  const response = payload.response.attestationObject
    ? createAttestationResponse(payload.response)
    : createAssertionResponse(payload.response);

  const credential: Partial<PublicKeyCredential> = {
    id: payload.id,
    rawId: arrayBuffer(base64UrlToBytes(payload.rawId)),
    type: "public-key",
    authenticatorAttachment: payload.authenticatorAttachment ?? "platform",
    response,
    getClientExtensionResults: () => payload.clientExtensionResults ?? {},
    toJSON: () => payload
  };

  return credential as PublicKeyCredential;
}

function requestBridge(action: BridgeAction, payload: unknown): Promise<any> {
  const requestId = randomId();

  return new Promise((resolve, reject) => {
    const onMessage = (event: MessageEvent) => {
      if (event.source !== window) {
        return;
      }
      const data = event.data;
      if (!data || data.source !== RESPONSE_SOURCE || data.kind !== "RESPONSE") {
        return;
      }
      if (data.requestId !== requestId) {
        return;
      }

      window.removeEventListener("message", onMessage);
      if (data.ok) {
        resolve(data.result);
        return;
      }

      const err = new Error(data.error?.message ?? "Unknown extension error") as Error & {
        name: string;
      };
      err.name = data.error?.name ?? "Error";
      reject(err);
    };

    window.addEventListener("message", onMessage);
    window.postMessage(
      {
        source: REQUEST_SOURCE,
        kind: "REQUEST",
        requestId,
        action,
        payload
      },
      window.location.origin
    );
  });
}

function installHook(): void {
  const credentials = navigator.credentials as CredentialsContainer & {
    [HOOK_FLAG]?: boolean;
  };
  if (!credentials || credentials[HOOK_FLAG]) {
    return;
  }

  const originalCreate = credentials.create.bind(credentials);
  const originalGet = credentials.get.bind(credentials);

  credentials.create = async (options?: CredentialCreationOptions): Promise<Credential | null> => {
    if (!options?.publicKey) {
      return originalCreate(options);
    }

    const result = await requestBridge("create", {
      origin: window.location.origin,
      publicKey: serializeCreateOptions(options.publicKey)
    });
    return buildCredential(result);
  };

  credentials.get = async (options?: CredentialRequestOptions): Promise<Credential | null> => {
    if (!options?.publicKey) {
      return originalGet(options);
    }

    const result = await requestBridge("get", {
      origin: window.location.origin,
      publicKey: serializeGetOptions(options.publicKey)
    });
    return buildCredential(result);
  };

  credentials[HOOK_FLAG] = true;
}

installHook();
