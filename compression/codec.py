"""Shared pieces of the myzip/myunzip format: bit I/O, Elias codes, Huffman, LZ77.

File format (all integers Elias-coded, all characters 8-bit):

    header:  len(filename) | filename | file size | number of distinct characters
             then for each character: char | len(codeword) | codeword (Huffman table)
    data:    LZ77 triples <offset, length, next character (as its Huffman codeword)>

No third-party dependencies: bits are packed with the standard library.
"""

import heapq
from collections import Counter

# ---------- bit I/O ----------


class BitWriter:
    def __init__(self) -> None:
        self.bits: list[int] = []

    def write(self, bits) -> None:
        self.bits.extend(int(b) for b in bits)

    def write_uint(self, value: int, width: int) -> None:
        self.write(format(value, f"0{width}b"))

    def to_bytes(self) -> bytes:
        padded = self.bits + [0] * (-len(self.bits) % 8)  # zero-pad the last byte
        return bytes(
            int("".join(map(str, padded[i : i + 8])), 2) for i in range(0, len(padded), 8)
        )


class BitReader:
    def __init__(self, data: bytes) -> None:
        self.bits = "".join(format(byte, "08b") for byte in data)
        self.pos = 0

    def read(self, n: int) -> str:
        if self.pos + n > len(self.bits):
            raise ValueError("unexpected end of compressed data")
        chunk = self.bits[self.pos : self.pos + n]
        self.pos += n
        return chunk

    def read_uint(self, width: int) -> int:
        return int(self.read(width), 2)


# ---------- Elias omega-style integer code (n >= 0, stored as n + 1) ----------


def elias(n: int) -> str:
    """Self-delimiting code: binary of n+1, preceded by a chain of length
    components, each with its leading 1 flipped to 0 to mark it as a length."""
    if n < 0:
        raise ValueError("elias codes non-negative integers")
    body = format(n + 1, "b")
    parts = [body]
    length = len(body)
    while length > 1:
        component = format(length - 1, "b")
        parts.append("0" + component[1:])
        length = len(component)
    return "".join(reversed(parts))


def dec_elias(reader: BitReader) -> int:
    width = 1
    while True:
        component = reader.read(width)
        if component[0] == "1":
            return int(component, 2) - 1
        width = int("1" + component[1:], 2) + 1


# ---------- Huffman ----------


def huffman(text: str) -> dict[str, str]:
    """Prefix-free codeword per character; ties broken by insertion order so
    encoding is deterministic."""
    freq = Counter(text)
    if not freq:
        return {}
    if len(freq) == 1:
        return {next(iter(freq)): "0"}
    heap = [(count, order, [ch]) for order, (ch, count) in enumerate(sorted(freq.items()))]
    heapq.heapify(heap)
    codes = {ch: "" for ch in freq}
    order = len(heap)
    while len(heap) > 1:
        c1, _, group1 = heapq.heappop(heap)
        c2, _, group2 = heapq.heappop(heap)
        for ch in group1:
            codes[ch] = "0" + codes[ch]
        for ch in group2:
            codes[ch] = "1" + codes[ch]
        heapq.heappush(heap, (c1 + c2, order, group1 + group2))
        order += 1
    return codes


# ---------- LZ77 via the Z-algorithm ----------


def z_array(s: str) -> list[int]:
    n = len(s)
    z = [0] * n
    if n:
        z[0] = n
    left = right = 0
    for i in range(1, n):
        if i < right:
            z[i] = min(z[i - left], right - i)
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > right:
            left, right = i, i + z[i]
    return z


SEPARATOR = "\x00￿"  # never matches: not in 8-bit input


def lz77(text: str, window: int, lookahead: int) -> list[tuple[int, int, str]]:
    """Greedy LZ77 factorisation into (offset, length, next char) triples.

    For each position, the Z-algorithm on  lookahead + separator + window + lookahead
    gives, at every window start, how far a match with the lookahead extends.
    Matches may run past the window into the lookahead (overlapping copies).
    """
    triples = []
    i, n = 0, len(text)
    while i < n:
        max_len = min(lookahead, n - i - 1)  # keep one character for the literal
        best_len, best_offset = 0, 0
        start = max(0, i - window)
        if max_len > 0 and start < i:
            ahead = text[i : i + max_len]
            z = z_array(ahead + SEPARATOR + text[start : i + max_len])
            base = len(ahead) + len(SEPARATOR)
            for j in range(start, i):
                length = min(z[base + (j - start)], max_len)
                if length > best_len or (length == best_len and length and i - j < best_offset):
                    best_len, best_offset = length, i - j
        triples.append((best_offset, best_len, text[i + best_len]))
        i += best_len + 1
    return triples


def expand(triples, size: int) -> str:
    out: list[str] = []
    for offset, length, char in triples:
        for _ in range(length):
            out.append(out[-offset])  # char by char, so overlapping copies work
        if len(out) < size:
            out.append(char)
    return "".join(out)
