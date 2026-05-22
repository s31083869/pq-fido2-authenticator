import { base64ToBytes, base64UrlToBytes, bytesToBase64Url } from "@/lib/base64url";

export type BinaryLike = string | ArrayBuffer | ArrayBufferView;

const HEX_RE = /^[0-9a-fA-F]+$/;
const BASE64_RE = /^[A-Za-z0-9+/]+={0,2}$/;
const BASE64URL_RE = /^[A-Za-z0-9_-]+$/;

export function isBinaryLike(value: unknown): value is BinaryLike {
  return (
    typeof value === "string" ||
    value instanceof ArrayBuffer ||
    ArrayBuffer.isView(value)
  );
}

export function toBytes(value: BinaryLike): Uint8Array {
  if (typeof value === "string") {
    return decodeStringBinary(value);
  }
  if (value instanceof ArrayBuffer) {
    return new Uint8Array(value);
  }
  return new Uint8Array(value.buffer, value.byteOffset, value.byteLength);
}

export function toBase64Url(value: BinaryLike): string {
  return bytesToBase64Url(toBytes(value));
}

export function decodeStringBinary(value: string): Uint8Array {
  const trimmed = value.trim();
  if (!trimmed) {
    return new Uint8Array();
  }

  if (HEX_RE.test(trimmed) && trimmed.length % 2 === 0) {
    const bytes = new Uint8Array(trimmed.length / 2);
    for (let i = 0; i < trimmed.length; i += 2) {
      bytes[i / 2] = Number.parseInt(trimmed.slice(i, i + 2), 16);
    }
    return bytes;
  }

  if (BASE64URL_RE.test(trimmed) && !trimmed.includes("+") && !trimmed.includes("/")) {
    try {
      return base64UrlToBytes(trimmed);
    } catch {
      // continue
    }
  }

  if (BASE64_RE.test(trimmed)) {
    try {
      return base64ToBytes(trimmed);
    } catch {
      // continue
    }
  }

  return new TextEncoder().encode(trimmed);
}

export function concatBytes(...parts: Uint8Array[]): Uint8Array {
  const total = parts.reduce((sum, part) => sum + part.length, 0);
  const out = new Uint8Array(total);
  let offset = 0;
  for (const part of parts) {
    out.set(part, offset);
    offset += part.length;
  }
  return out;
}

export function equalBytes(a: Uint8Array, b: Uint8Array): boolean {
  if (a.length !== b.length) {
    return false;
  }
  for (let i = 0; i < a.length; i += 1) {
    if (a[i] !== b[i]) {
      return false;
    }
  }
  return true;
}
