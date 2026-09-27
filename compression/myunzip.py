"""Restore a file compressed by myzip.

    python myunzip.py <file.bin> [output_dir]    # writes the original file name
"""

import os
import sys

from codec import BitReader, dec_elias, expand


def decompress(data: bytes) -> tuple[str, str]:
    reader = BitReader(data)
    name = "".join(chr(reader.read_uint(8)) for _ in range(dec_elias(reader)))
    size = dec_elias(reader)
    decode_table = {}
    for _ in range(dec_elias(reader)):
        ch = chr(reader.read_uint(8))
        decode_table[reader.read(dec_elias(reader))] = ch
    triples, produced = [], 0
    while produced < size:
        offset = dec_elias(reader)
        length = dec_elias(reader)
        code = ""
        while code not in decode_table:  # Huffman codes are prefix-free
            code += reader.read(1)
            if len(code) > 256:
                raise ValueError("corrupt Huffman data")
        triples.append((offset, length, decode_table[code]))
        produced += length + 1
    return name, expand(triples, size)


def decode(filename: str, output_dir: str = ".") -> str:
    with open(filename, "rb") as f:
        name, text = decompress(f.read())
    target = os.path.join(output_dir, os.path.basename(name))  # never escape output_dir
    with open(target, "wb") as f:
        f.write(text.encode("latin-1"))
    return target


if __name__ == "__main__":
    print(decode(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "."))
