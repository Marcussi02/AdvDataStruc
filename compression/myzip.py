"""Compress a file with LZ77 + Huffman + Elias codes.

    python myzip.py <file> <window_size> <lookahead_size>    # writes <file>.bin
"""

import os
import sys

from codec import BitWriter, elias, huffman, lz77


def compress(text: str, name: str, window: int, lookahead: int) -> bytes:
    if window < 1 or lookahead < 1:
        raise ValueError("window and lookahead must be at least 1")
    out = BitWriter()
    out.write(elias(len(name)))
    for ch in name:
        out.write_uint(ord(ch), 8)
    out.write(elias(len(text)))
    codes = huffman(text)
    out.write(elias(len(codes)))
    for ch, code in codes.items():
        out.write_uint(ord(ch), 8)
        out.write(elias(len(code)))
        out.write(code)
    for offset, length, char in lz77(text, window, lookahead):
        out.write(elias(offset))
        out.write(elias(length))
        out.write(codes[char])
    return out.to_bytes()


def encode(filename: str, window: int, lookahead: int) -> str:
    with open(filename, "rb") as f:
        text = f.read().decode("latin-1")  # 1 byte == 1 character, any file
    name = os.path.basename(filename)
    if any(ord(ch) > 255 for ch in name):
        raise ValueError("file name must be 8-bit characters")
    target = filename + ".bin"
    with open(target, "wb") as f:
        f.write(compress(text, name, window, lookahead))
    return target


if __name__ == "__main__":
    print(encode(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])))
