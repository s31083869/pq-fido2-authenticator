const RP_BASE_URL =
  process.env.NEXT_PUBLIC_RP_SERVER_URL || "http://localhost:5005";

async function parseResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `RP request failed: ${response.status}`);
  }

  const payload = await response.json();
  if (payload.success === false) {
    throw new Error(payload.message || "RP reported failure");
  }
  return payload.data as T;
}

export async function rpFetch<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${RP_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return parseResponse<T>(response);
}
