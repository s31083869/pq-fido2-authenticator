type CborValue = unknown;

function encodeTypeAndLength(majorType: number, length: number): number[] {
  if (length < 24) {
    return [(majorType << 5) | length];
  }
  if (length < 0x100) {
    return [(majorType << 5) | 24, length];
  }
  if (length < 0x10000) {
    return [(majorType << 5) | 25, (length >> 8) & 0xff, length & 0xff];
  }
  if (length < 0x100000000) {
    return [
      (majorType << 5) | 26,
      (length >> 24) & 0xff,
      (length >> 16) & 0xff,
      (length >> 8) & 0xff,
      length & 0xff
    ];
  }
  throw new Error("Length too large for minimal CBOR encoder");
}

function encodeInt(value: number): Uint8Array {
  if (!Number.isInteger(value)) {
    throw new Error("Only integer numbers are supported in this CBOR encoder");
  }

  if (value >= 0) {
    return Uint8Array.from(encodeTypeAndLength(0, value));
  }

  return Uint8Array.from(encodeTypeAndLength(1, -1 - value));
}

function encodeBytes(bytes: Uint8Array): Uint8Array {
  const prefix = Uint8Array.from(encodeTypeAndLength(2, bytes.length));
  const out = new Uint8Array(prefix.length + bytes.length);
  out.set(prefix, 0);
  out.set(bytes, prefix.length);
  return out;
}

function encodeText(text: string): Uint8Array {
  const body = new TextEncoder().encode(text);
  const prefix = Uint8Array.from(encodeTypeAndLength(3, body.length));
  const out = new Uint8Array(prefix.length + body.length);
  out.set(prefix, 0);
  out.set(body, prefix.length);
  return out;
}

function encodeArray(values: CborValue[]): Uint8Array {
  const items = values.map((value) => encodeCbor(value));
  const total = items.reduce((sum, item) => sum + item.length, 0);
  const prefix = Uint8Array.from(encodeTypeAndLength(4, values.length));
  const out = new Uint8Array(prefix.length + total);
  out.set(prefix, 0);
  let offset = prefix.length;
  for (const item of items) {
    out.set(item, offset);
    offset += item.length;
  }
  return out;
}

function encodeMapEntries(entries: Array<[number | string, CborValue]>): Uint8Array {
  const encoded = entries.map(([key, value]) => [encodeCbor(key), encodeCbor(value)] as const);
  const total = encoded.reduce((sum, [k, v]) => sum + k.length + v.length, 0);
  const prefix = Uint8Array.from(encodeTypeAndLength(5, entries.length));
  const out = new Uint8Array(prefix.length + total);
  out.set(prefix, 0);
  let offset = prefix.length;
  for (const [keyBytes, valueBytes] of encoded) {
    out.set(keyBytes, offset);
    offset += keyBytes.length;
    out.set(valueBytes, offset);
    offset += valueBytes.length;
  }
  return out;
}

export function encodeCbor(value: CborValue): Uint8Array {
  if (value === null) {
    return Uint8Array.from([0xf6]);
  }

  if (typeof value === "boolean") {
    return Uint8Array.from([value ? 0xf5 : 0xf4]);
  }

  if (typeof value === "number") {
    return encodeInt(value);
  }

  if (typeof value === "string") {
    return encodeText(value);
  }

  if (value instanceof Uint8Array) {
    return encodeBytes(value);
  }

  if (Array.isArray(value)) {
    return encodeArray(value);
  }

  if (value instanceof Map) {
    return encodeMapEntries(Array.from(value.entries()));
  }

  if (typeof value === "object" && value !== null) {
    return encodeMapEntries(Object.entries(value as Record<string, CborValue>));
  }

  throw new Error("Unsupported CBOR value");
}
