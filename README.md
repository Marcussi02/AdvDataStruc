# Advanced Data Structures & Algorithms

[![CI](https://github.com/Marcussi02/AdvDataStruc/actions/workflows/ci.yml/badge.svg)](https://github.com/Marcussi02/AdvDataStruc/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

Implementations from the advanced algorithms unit of my **Computer Science degree at Monash University Malaysia**: string matching, suffix trees, compression, graphs and randomised number theory, written from first principles in pure Python with no third-party dependencies.

Every algorithm is checked against a brute-force reference on randomised inputs.

## Contents

| Topic | File | What it implements | Status |
|---|---|---|---|
| **String matching** | [`string-matching/modified_boyer_moore.py`](string-matching/modified_boyer_moore.py) | Boyer-Moore with extended **bad-character**, **good-suffix** and **matched-prefix** rules; preprocessing built on the **Z-algorithm** | 🟢 Complete, tested |
| **Suffix trees** | [`suffix-trees/generalised_suffix_tree.py`](suffix-trees/generalised_suffix_tree.py) | **Ukkonen's** linear-time **generalised suffix tree** (global end, active point, skip/count, suffix links), with substring search, occurrence listing and **longest common substring** | 🟢 Complete, tested |
| **Compression** | [`compression/myzip.py`](compression/myzip.py) | **LZ77** factorisation (via the Z-algorithm), **Huffman** coding and **Elias omega** integer codes, packed into a custom bit-level file format | 🟢 Complete, tested |
| | [`compression/myunzip.py`](compression/myunzip.py) | Decoder: header parsing, Elias and Huffman decoding, LZ77 reconstruction | 🟢 Complete, round-trip tested |
| | [`compression/codec.py`](compression/codec.py) | Shared bit I/O and codecs | 🟢 |
| **Graphs** | [`graphs/kruskal_mst.py`](graphs/kruskal_mst.py) | **Kruskal's MST** on a **union-find** with union by height and path compression | 🟢 Complete, tested |
| **Number theory** | [`number-theory/three_primes.py`](number-theory/three_primes.py) | **Miller-Rabin** randomised primality test, used to write an odd number as a sum of three primes (weak Goldbach) | 🟢 Complete, tested |

The first versions were written during the unit; some were unfinished drafts. I completed them later, fixed the bugs I found, and added the test suite.

## Complexity

| Algorithm | Time | Notes |
|---|---|---|
| Z-algorithm | O(n) | |
| Boyer-Moore preprocessing | O(m + m·σ) | σ = pattern alphabet |
| Boyer-Moore search | O(n/m) typical, O(nm) worst | |
| Ukkonen suffix tree | O(n) construction | n = total length of all strings |
| Longest common substring | O(n) | one bitmask per node |
| Kruskal | O(E log E) | near-constant union-find |
| Miller-Rabin | O(k log³ n) | error ≤ 4⁻ᵏ |

## Why this unit matters

These are the algorithms underneath tools used every day:

- **Boyer-Moore and the Z-algorithm:** fast text search, as in `grep`, editors and DNA matching.
- **Suffix trees:** linear-time substring queries, genome indexing and plagiarism detection.
- **LZ77 + Huffman:** the core idea behind DEFLATE (zip, gzip, PNG).
- **Elias codes:** compact, self-delimiting integers in compressed formats and indexes.
- **Union-find + Kruskal:** network design and clustering.
- **Miller-Rabin:** how RSA key generation finds large primes quickly.

## Running

Python 3.10+, standard library only.

```bash
# Boyer-Moore: prints 1-based match positions
python string-matching/modified_boyer_moore.py text.txt pattern.txt

# Longest common substring of any number of strings
python suffix-trees/generalised_suffix_tree.py banana ananas     # anana

# Compress and decompress (window 6, lookahead 4)
cd compression
python myzip.py samples/x.asc 6 4      # writes samples/x.asc.bin
python myunzip.py samples/x.asc.bin    # restores x.asc
cd ..

# Minimum spanning tree: file is "V E" then E lines of "u v w"
python graphs/kruskal_mst.py graph.txt

# Odd number as a sum of three primes
python number-theory/three_primes.py 31                          # 3 5 23
```

## Tests

```bash
pip install -r requirements-dev.txt
pytest -q
ruff check --select E,F --line-length 100 .
```

## License

[MIT](LICENSE)
