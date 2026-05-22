export type SupportedAlg = -48 | -49 | -50;

export type BinaryLikeString = string;

export interface CredentialDescriptorPayload {
  type: "public-key";
  id: BinaryLikeString;
  transports?: AuthenticatorTransport[];
}

export interface CreationRequestPayload {
  origin: string;
  publicKey: {
    rp: {
      id: string;
      name?: string;
    };
    user: {
      id: BinaryLikeString;
      name: string;
      displayName: string;
    };
    challenge: BinaryLikeString;
    pubKeyCredParams: Array<{ type: "public-key"; alg: number }>;
    timeout?: number;
    excludeCredentials?: CredentialDescriptorPayload[];
    authenticatorSelection?: Record<string, unknown>;
    attestation?: string;
    extensions?: Record<string, unknown>;
  };
}

export interface RequestRequestPayload {
  origin: string;
  publicKey: {
    challenge: BinaryLikeString;
    timeout?: number;
    rpId?: string;
    allowCredentials?: CredentialDescriptorPayload[];
    userVerification?: string;
    extensions?: Record<string, unknown>;
  };
}

export interface RegistrationResponsePayload {
  id: string;
  rawId: string;
  type: "public-key";
  authenticatorAttachment: "platform";
  clientExtensionResults: Record<string, unknown>;
  response: {
    clientDataJSON: string;
    attestationObject: string;
    authenticatorData: string;
    publicKeyAlgorithm: SupportedAlg;
    publicKey: string;
    transports: string[];
  };
}

export interface AuthenticationResponsePayload {
  id: string;
  rawId: string;
  type: "public-key";
  authenticatorAttachment: "platform";
  clientExtensionResults: Record<string, unknown>;
  response: {
    clientDataJSON: string;
    authenticatorData: string;
    signature: string;
    userHandle: string | null;
  };
}

interface BridgeRequestBase {
  channel: "PQ_WEBAUTHN_BRIDGE";
  requestId: string;
}

export interface BridgeCreateRequestMessage extends BridgeRequestBase {
  action: "create";
  payload: CreationRequestPayload;
}

export interface BridgeGetRequestMessage extends BridgeRequestBase {
  action: "get";
  payload: RequestRequestPayload;
}

export type BridgeRequestMessage = BridgeCreateRequestMessage | BridgeGetRequestMessage;

export interface BridgeSuccessMessage {
  ok: true;
  result: RegistrationResponsePayload | AuthenticationResponsePayload;
}

export interface BridgeErrorMessage {
  ok: false;
  error: {
    name: string;
    message: string;
  };
}

export type BridgeResponseMessage = BridgeSuccessMessage | BridgeErrorMessage;

export interface PersistedCredential {
  credentialId: string;
  rpId: string;
  userHandle: string;
  publicKey: string;
  privateKey: string;
  algorithm: SupportedAlg;
  signCount: number;
  createdAt: string;
}

export interface Settings {
  enabled: boolean;
  defaultAlgorithm: SupportedAlg;
  uvMode: "soft-auto" | "native-touch-id" | "native-windows-hello";
}
