import { describe, expect, test } from "bun:test";

import {
  binaryStringToBuffer,
  base64urlToBuffer,
  bufferToBase64url,
  stringToBuffer,
} from "./webauthn";

const decoder = new TextDecoder();

describe("webauthn helpers", () => {
  test("buffer round trip", () => {
    const data = new TextEncoder().encode("pq-fido2");
    const encoded = bufferToBase64url(data.buffer);
    const decoded = base64urlToBuffer(encoded);
    expect(decoder.decode(new Uint8Array(decoded))).toBe("pq-fido2");
  });

  test("stringToBuffer encodes UTF-8", () => {
    const bytes = stringToBuffer("Touch ID");
    expect(decoder.decode(new Uint8Array(bytes))).toBe("Touch ID");
  });

  test("binaryStringToBuffer decodes base64url data", () => {
    const bytes = binaryStringToBuffer("cHEtZmlkbzI");
    expect(decoder.decode(new Uint8Array(bytes))).toBe("pq-fido2");
  });

  test("binaryStringToBuffer preserves plain UTF-8 strings", () => {
    const bytes = binaryStringToBuffer("Touch ID");
    expect(decoder.decode(new Uint8Array(bytes))).toBe("Touch ID");
  });
});
