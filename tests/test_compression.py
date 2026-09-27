import random

import pytest

from codec import BitReader, BitWriter, dec_elias, elias, huffman, lz77, expand
from myunzip import decode, decompress
from myzip import compress, encode


def test_elias_round_trip_and_known_codes():
    assert elias(0) == "1"
    assert elias(1) == "010"
    w = BitWriter()
    values = list(range(300)) + [10**6, 2**31]
    for v in values:
        w.write(elias(v))
    r = BitReader(w.to_bytes())
    assert [dec_elias(r) for _ in values] == values


def test_huffman_is_prefix_free_and_optimal_order():
    codes = huffman("aaaaabbbc")
    words = list(codes.values())
    assert not any(a != b and b.startswith(a) for a in words for b in words)
    assert len(codes["a"]) <= len(codes["b"]) <= len(codes["c"])
    assert huffman("zzz") == {"z": "0"}


@pytest.mark.parametrize(("window", "lookahead"), [(1, 1), (6, 4), (32, 16)])
def test_lz77_reconstructs(window, lookahead):
    rng = random.Random(window * 100 + lookahead)
    for _ in range(300):
        text = "".join(rng.choice("abc") for _ in range(rng.randint(0, 80)))
        triples = lz77(text, window, lookahead)
        assert expand(triples, len(text)) == text
        assert all(o <= window and ln <= lookahead for o, ln, _ in triples)


def test_round_trip_random_texts():
    rng = random.Random(3)
    for _ in range(200):
        text = "".join(rng.choice("ab \n\x00\xff") for _ in range(rng.randint(0, 200)))
        name, restored = decompress(compress(text, "f.txt", rng.randint(1, 40), rng.randint(1, 20)))
        assert (name, restored) == ("f.txt", text)


def test_repetitive_text_gets_smaller():
    text = "the quick brown fox " * 200
    assert len(compress(text, "fox.txt", 64, 32)) < len(text) / 5


def test_files_round_trip(tmp_path):
    src = tmp_path / "x.asc"
    src.write_bytes(b"aacaacabcaba")
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    restored = decode(encode(str(src), 6, 4), str(out_dir))
    assert (out_dir / "x.asc").read_bytes() == b"aacaacabcaba"
    assert restored.endswith("x.asc")
