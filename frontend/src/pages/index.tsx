import {
  useCallback,
  useEffect,
  useState,
  useTransition,
  type Dispatch,
  type SetStateAction,
} from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { toast } from "sonner";

import { rpFetch } from "@/lib/api";
import {
  base64urlToBuffer,
  binaryStringToBuffer,
  serializeAssertion,
  serializeAttestation,
} from "@/lib/webauthn";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

type AuthenticatorCredential = {
  id: string;
  rpId: string;
  userHandle: string;
  decodedUserHandle?: string;
  lastUsed?: number | null;
};

type BridgeCredential = {
  id: string;
  rp_id: string;
  user_handle: string;
  decoded_user_handle?: string;
  last_used?: number;
};

type BridgeListResponse = {
  credentials: BridgeCredential[];
};

declare global {
  interface Window {
    __pqListCredentials?: () => Promise<BridgeListResponse>;
  }
}

const registerSchema = z.object({
  username: z.string().min(3).max(64),
  displayName: z.string().min(1).max(64),
});

const authenticateSchema = z.object({
  username: z.string().min(3).max(64),
});

type RegisterFormValues = z.infer<typeof registerSchema>;
type AuthenticateFormValues = z.infer<typeof authenticateSchema>;

type RegisterOptionsPayload = {
  challenge: string;
  rp: { id: string; name: string };
  user: { id: string; name: string; displayName: string };
  pubKeyCredParams: { type: "public-key"; alg: number }[];
  timeout: number;
  attestation: AttestationConveyancePreference;
  authenticatorSelection: AuthenticatorSelectionCriteria;
  excludeCredentials?: { id: string; type: "public-key"; transports?: AuthenticatorTransport[] }[];
  extensions?: AuthenticationExtensionsClientInputs;
};

type AuthenticateOptionsPayload = {
  challenge: string;
  rpId: string;
  allowCredentials: { id: string; type: "public-key"; transports?: AuthenticatorTransport[] }[];
  timeout: number;
  userVerification: "required" | "preferred" | "discouraged";
};

const algorithmOptions = [
  { label: "ML-DSA-44", value: -48 },
  { label: "ML-DSA-65", value: -49 },
  { label: "ML-DSA-87", value: -50 },
];
const CTA_BUTTON_CLASS =
  "w-full border border-[#FB6A23] bg-[#FFF7F0] text-[#FB6A23] font-semibold shadow-[0_10px_30px_rgba(251,106,35,0.15)] transition-colors hover:bg-[#FFEFE3]";

function summarizeCredentialId(id: string) {
  if (id.length <= 16) {
    return id;
  }
  return `${id.slice(0, 8)}…${id.slice(-4)}`;
}

function pushLog(
  setter: Dispatch<SetStateAction<string[]>>,
  message: string,
) {
  const entry = `${new Date().toLocaleTimeString()} · ${message}`;
  setter((prev) => [entry, ...prev].slice(0, 10));
}

export default function HomePage() {
  const [registerLog, setRegisterLog] = useState<string[]>([]);
  const [authLog, setAuthLog] = useState<string[]>([]);
  const [credentials, setCredentials] = useState<AuthenticatorCredential[]>([]);
  const [credentialsLoading, setCredentialsLoading] = useState(true);
  const [credentialError, setCredentialError] = useState<string | null>(null);
  const [currentRpId, setCurrentRpId] = useState("");
  const [credentialBadgeMode, setCredentialBadgeMode] = useState<"register" | "authenticate" | "manual">("manual");
  const [activeTab, setActiveTab] = useState("register");
  const [algorithm, setAlgorithm] = useState<number>(algorithmOptions[1].value);
  const [isRegistering, startRegister] = useTransition();
  const [isAuthenticating, startAuth] = useTransition();

  const registerForm = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
    defaultValues: { username: "alice", displayName: "Alice" },
  });

  const authenticateForm = useForm<AuthenticateFormValues>({
    resolver: zodResolver(authenticateSchema),
    defaultValues: { username: "alice" },
  });

  const refreshCredentials = useCallback(async (mode: "register" | "authenticate" | "manual" = "manual") => {
    setCredentialsLoading(true);
    setCredentialError(null);
    try {
      if (typeof window === "undefined" || typeof window.__pqListCredentials !== "function") {
        throw new Error("Authenticator bridge not connected");
      }
      const data = await window.__pqListCredentials();
      const normalized: AuthenticatorCredential[] = data.credentials
        .map((credential) => ({
          id: credential.id,
          rpId: credential.rp_id,
          userHandle: credential.user_handle,
          decodedUserHandle: credential.decoded_user_handle,
          lastUsed: credential.last_used ?? null,
        }))
        .sort((a, b) => (b.lastUsed ?? 0) - (a.lastUsed ?? 0));
      const host = window.location.hostname;
      setCurrentRpId(host);
      const filtered = normalized.filter((credential) => credential.rpId === host);
      setCredentials(filtered);
      setCredentialBadgeMode(mode);
    } catch (error) {
      console.error(error);
      setCredentialError((error as Error).message ?? "Failed to load credentials");
    } finally {
      setCredentialsLoading(false);
    }
  }, []);

  useEffect(() => {
    void refreshCredentials();
  }, [refreshCredentials]);

  const handleRegister = registerForm.handleSubmit((values) => {
    startRegister(async () => {
      try {
        const options = await rpFetch<RegisterOptionsPayload>(
          "/register/options",
          {
            username: values.username,
            display_name: values.displayName,
          },
        );
        pushLog(setRegisterLog, "Received creation options");

        const normalizedParams = options.pubKeyCredParams || [];
        const orderedParams = [
          { type: "public-key" as const, alg: algorithm },
          ...normalizedParams.filter((param) => param.alg !== algorithm),
        ];

        const publicKey: PublicKeyCredentialCreationOptions = {
          rp: options.rp,
          user: {
            ...options.user,
            id: binaryStringToBuffer(options.user.id),
          },
          challenge: base64urlToBuffer(options.challenge),
          pubKeyCredParams: orderedParams,
          timeout: options.timeout,
          attestation: options.attestation,
          authenticatorSelection: options.authenticatorSelection,
          extensions: options.extensions,
          excludeCredentials: options.excludeCredentials?.map((cred) => ({
            ...cred,
            id: base64urlToBuffer(cred.id),
          })),
        };

        if (!("credentials" in navigator)) {
          throw new Error("navigator.credentials is not available in this browser");
        }

        const credential = (await navigator.credentials.create({
          publicKey,
        })) as PublicKeyCredential;
        const serialized = serializeAttestation(credential);

        const attestationResponse = serialized.response as Record<string, unknown>;
        if (!attestationResponse.attestationObject || !attestationResponse.clientDataJSON) {
          throw new Error(
            "Attestation payload incomplete. Ensure the Python authenticator bridge is running.",
          );
        }

        await rpFetch("/register/verify", {
          username: values.username,
          credential: serialized,
        });
        pushLog(setRegisterLog, `Credential ${serialized.id} stored`);
        toast.success("Registration completed");
        await refreshCredentials("register");
      } catch (error) {
        console.error(error);
        const message = (error as Error).message ?? "Registration failed";
        const friendlyMessage = message.includes("Credential creation excluded")
          ? "Credential already registered for this RP."
          : message;
        toast.error(friendlyMessage);
        pushLog(setRegisterLog, `Registration failed: ${friendlyMessage}`);
      }
    });
  });

  const handleAuthenticate = authenticateForm.handleSubmit((values) => {
    startAuth(async () => {
      try {
        const options = await rpFetch<AuthenticateOptionsPayload>(
          "/authenticate/options",
          { username: values.username },
        );
        pushLog(setAuthLog, "Received assertion options");

        const publicKey: PublicKeyCredentialRequestOptions = {
          challenge: base64urlToBuffer(options.challenge),
          allowCredentials: options.allowCredentials.map((cred) => ({
            ...cred,
            id: base64urlToBuffer(cred.id),
          })),
          rpId: options.rpId,
          timeout: options.timeout,
          userVerification: options.userVerification,
        };

        if (!("credentials" in navigator)) {
          throw new Error("navigator.credentials is not available in this browser");
        }

        const credential = (await navigator.credentials.get({
          publicKey,
        })) as PublicKeyCredential;
        const serialized = serializeAssertion(credential);
        await rpFetch("/authenticate/verify", {
          username: values.username,
          credential: serialized,
        });
        pushLog(setAuthLog, `Assertion verified for ${serialized.id}`);
        toast.success("Authentication successful");
        await refreshCredentials("authenticate");
      } catch (error) {
        console.error(error);
        const message = (error as Error).message ?? "Authentication failed";
        toast.error(message);
        pushLog(setAuthLog, `Authentication failed: ${message}`);
      }
    });
  });

  return (
    <main className="relative min-h-screen overflow-hidden bg-[#FCFCFB] text-slate-900">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(251,106,35,0.12),_transparent_62%)]" />
      <div className="pointer-events-none absolute inset-0 opacity-60" aria-hidden>
        <div className="h-full w-full bg-[linear-gradient(90deg,rgba(0,0,0,0.02)_1px,transparent_1px),linear-gradient(rgba(0,0,0,0.02)_1px,transparent_1px)] bg-[size:90px_90px]" />
      </div>
      <div className="relative z-10 mx-auto flex max-w-5xl flex-col items-center gap-8 px-6 py-16 text-center">
        <header className="space-y-4 text-slate-900">
          <Badge className="bg-[#FB6A23]/10 text-[#FB6A23]">
            Post-Quantum Ready
          </Badge>
          <h1 className="text-4xl font-semibold tracking-tight text-slate-900 md:text-5xl">
            Post-Quantum WebAuthn Demo
          </h1>
          <p className="mx-auto max-w-2xl text-lg text-slate-600">
            Explore ML-DSA registration and authentication flows using the Python authenticator bridge,
            complete with live ceremony logs and credential visibility.
          </p>
        </header>

        <div className="grid w-full gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(280px,1fr)]">
          <Tabs
            value={activeTab}
            onValueChange={setActiveTab}
            className="w-full text-left"
            defaultValue="register"
          >
            <TabsList className="grid w-full grid-cols-2 gap-3 bg-transparent">
              <TabsTrigger
                value="register"
                className="rounded-full border border-[#FB6A23] bg-white/90 px-6 py-3 text-sm font-semibold text-slate-600 shadow-sm transition data-[state=active]:bg-[#FB6A23] data-[state=active]:text-white data-[state=active]:shadow-[0_15px_30px_rgba(251,106,35,0.25)] hover:bg-[#FFF2E9]"
              >
                Register
              </TabsTrigger>
              <TabsTrigger
                value="authenticate"
                className="rounded-full border border-[#FB6A23] bg-white/90 px-6 py-3 text-sm font-semibold text-slate-600 shadow-sm transition data-[state=active]:bg-[#FB6A23] data-[state=active]:text-white data-[state=active]:shadow-[0_15px_30px_rgba(251,106,35,0.25)] hover:bg-[#FFF2E9]"
              >
                Authenticate
              </TabsTrigger>
            </TabsList>

            <TabsContent value="register" className="mt-6">
              <Card className="border-[#FB6A23]/10 bg-white text-slate-900 shadow-[0_30px_80px_rgba(15,23,42,0.12)]">
                <CardHeader>
                  <CardTitle>Register Credential</CardTitle>
                  <CardDescription className="text-slate-600">
                    Request creation options from the RP, reorder ML-DSA algorithms, and invoke
                    `navigator.credentials.create`.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Form {...registerForm}>
                    <form className="space-y-5" onSubmit={handleRegister}>
                      <FormField
                        control={registerForm.control}
                        name="username"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="text-slate-700">Username</FormLabel>
                            <FormControl>
                              <Input
                                placeholder="alice"
                                className="border-slate-200 bg-white text-slate-900 placeholder:text-slate-400"
                                {...field}
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <FormField
                        control={registerForm.control}
                        name="displayName"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="text-slate-700">Display name</FormLabel>
                            <FormControl>
                              <Input
                                placeholder="Alice"
                                className="border-slate-200 bg-white text-slate-900 placeholder:text-slate-400"
                                {...field}
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      <div className="space-y-2">
                        <FormLabel className="text-slate-700">ML-DSA algorithm</FormLabel>
                        <Select
                          value={String(algorithm)}
                          onValueChange={(value) => setAlgorithm(Number(value))}
                        >
                          <SelectTrigger className="border-slate-200 bg-white text-slate-900">
                            <SelectValue placeholder="Select algorithm" />
                          </SelectTrigger>
                          <SelectContent className="border border-slate-200 bg-white text-slate-900">
                            {algorithmOptions.map((option) => (
                              <SelectItem key={option.value} value={String(option.value)}>
                                {option.label}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>

                      <Button
                        type="submit"
                        disabled={isRegistering}
                        className={CTA_BUTTON_CLASS}
                      >
                        {isRegistering ? "Processing…" : "Create credential"}
                      </Button>
                    </form>
                  </Form>
                  <LogPanel entries={registerLog} emptyCopy="Awaiting registration events" />
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="authenticate" className="mt-6">
              <Card className="border-[#FB6A23]/10 bg-white text-slate-900 shadow-[0_30px_80px_rgba(15,23,42,0.12)]">
                <CardHeader>
                  <CardTitle>Authenticate</CardTitle>
                  <CardDescription className="text-slate-600">
                    Request assertion options and trigger `navigator.credentials.get`.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Form {...authenticateForm}>
                    <form className="space-y-5" onSubmit={handleAuthenticate}>
                      <FormField
                        control={authenticateForm.control}
                        name="username"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="text-slate-700">Username</FormLabel>
                            <FormControl>
                              <Input
                                placeholder="alice"
                                className="border-slate-200 bg-white text-slate-900 placeholder:text-slate-400"
                                {...field}
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <Button
                        type="submit"
                        disabled={isAuthenticating}
                        className={CTA_BUTTON_CLASS}
                      >
                        {isAuthenticating ? "Processing…" : "Request assertion"}
                      </Button>
                    </form>
                  </Form>
                  <LogPanel entries={authLog} emptyCopy="Awaiting authentication events" />
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>

          <CredentialCard
            credentials={credentials}
            loading={credentialsLoading}
            error={credentialError}
            onRefresh={refreshCredentials}
            className="sticky top-6"
            rpId={currentRpId}
            badgeMode={credentialBadgeMode}
          />
        </div>
      </div>
    </main>
  );
}

type LogPanelProps = {
  entries: string[];
  emptyCopy: string;
};

function LogPanel({ entries, emptyCopy }: LogPanelProps) {
  if (!entries.length) {
    return <p className="mt-4 text-sm text-slate-500">{emptyCopy}</p>;
  }
  return (
    <div className="mt-4 max-h-48 space-y-2 overflow-y-auto rounded-xl border border-slate-200 bg-white p-4 text-sm text-slate-700">
      {entries.map((entry, index) => (
        <p key={`${entry}-${index}`}>{entry}</p>
      ))}
    </div>
  );
}

type CredentialCardProps = {
  credentials: AuthenticatorCredential[];
  loading: boolean;
  error: string | null;
  onRefresh: () => void;
  className?: string;
  rpId?: string;
  badgeMode: "register" | "authenticate" | "manual";
};

function CredentialCard({
  credentials,
  loading,
  error,
  onRefresh,
  className,
  rpId,
  badgeMode,
}: CredentialCardProps) {
  return (
    <div
      className={cn(
        "rounded-2xl border border-[#FB6A23]/20 bg-gradient-to-br from-white via-[#FFF8F4] to-white p-5 text-left text-slate-900 shadow-[0_30px_70px_rgba(15,23,42,0.05)]",
        className,
      )}
    >
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-sm font-semibold text-[#FB6A23]">Authenticator Credentials</p>
          <p className="text-2xl font-semibold text-slate-900">{credentials.length} stored</p>
          <p className="text-xs text-slate-500">
            Listed directly from the Python authenticator index for{" "}
            <span className="font-semibold">{rpId || "this origin"}</span>, ordered by most recent activity.
          </p>
        </div>
        <Button
          type="button"
          disabled={loading}
          onClick={onRefresh}
          className="border border-[#FB6A23] bg-white px-4 py-2 text-sm font-semibold text-[#FB6A23] shadow-[0_10px_25px_rgba(251,106,35,0.12)] transition-colors hover:bg-[#FFF2E9]"
        >
          {loading ? "Refreshing…" : "Refresh"}
        </Button>
      </div>

      <div className="mt-4 max-h-[28rem] overflow-y-auto pr-1">
        {error ? (
          <p className="text-sm text-red-500">{error}</p>
        ) : loading ? (
          <div className="space-y-2">
            {[0, 1].map((item) => (
              <div
                key={item}
                className="h-14 animate-pulse rounded-2xl border border-slate-200 bg-slate-100"
              />
            ))}
          </div>
        ) : credentials.length === 0 ? (
          <p className="text-sm text-slate-500">No credentials recorded yet.</p>
        ) : (
          <Accordion
            type="multiple"
            className="space-y-3"
          >
            {credentials.map((credential, index) => (
              <AccordionItem
                key={credential.id}
                value={credential.id}
                className="overflow-hidden rounded-2xl border border-slate-200 bg-white/90 px-4 shadow-[0_15px_35px_rgba(15,23,42,0.04)]"
              >
                <AccordionTrigger className="py-3 text-left text-sm font-semibold text-slate-900">
                  <div className="flex w-full flex-col gap-1 text-left">
                    <span className="font-mono text-sm">
                      {summarizeCredentialId(credential.id)}
                    </span>
                    <span className="text-xs text-slate-500">{credential.rpId}</span>
                  </div>
                  <Badge className="bg-[#FB6A23]/10 text-[#FB6A23]">
                    {badgeMode === "authenticate" && index === 0 ? "Last used" : "Ready"}
                  </Badge>
                </AccordionTrigger>
                <AccordionContent>
                  <div className="space-y-2 text-xs text-slate-600">
                    <div>
                      <p className="font-semibold text-slate-800">Full ID</p>
                      <p className="font-mono break-all text-slate-600">{credential.id}</p>
                    </div>
                    <div>
                      <p className="font-semibold text-slate-800">User handle</p>
                      <p className="font-mono break-all text-slate-600">
                        {(credential.decodedUserHandle ?? credential.userHandle) || "Unknown"}
                      </p>
                    </div>
                    <div>
                      <p className="font-semibold text-slate-800">RP ID</p>
                      <p>{credential.rpId}</p>
                    </div>
                  </div>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        )}
      </div>
    </div>
  );
}
