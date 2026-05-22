export async function sha256(data: Uint8Array): Promise<Uint8Array> {
  const input = new Uint8Array(data.byteLength);
  input.set(data);
  const hash = await crypto.subtle.digest("SHA-256", input);
  return new Uint8Array(hash);
}
