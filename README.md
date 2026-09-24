# Advanced Data Structures & Algorithms

Implementations from the advanced algorithms unit of my **Computer Science degree at Monash University Malaysia**: string matching, suffix trees, compression, graphs and randomised number theory, written from first principles in Python.

> If you know, you know. 🧠

These are my coursework implementations, kept as they were written, with light tidying. Some are complete; others are honest drafts that capture where my thinking got to.

## Contents

| Topic | File | What it implements | Status |
|---|---|---|---|
| **String matching** | [`string-matching/modified_boyer_moore.py`](string-matching/modified_boyer_moore.py) | Boyer-Moore with **bad-character**, **good-suffix** and **matched-prefix** shift rules, with the preprocessing built on the **Z-algorithm** | 🟡 Z-algorithm works; full matcher in progress |
| **Suffix trees** | [`suffix-trees/generalised_suffix_tree.py`](suffix-trees/generalised_suffix_tree.py) | Ukkonen-style **generalised suffix tree** (nodes, edges, global end pointer) | 🔴 Design sketch |
| **Compression** | [`compression/myzip.py`](compression/myzip.py) | **LZ77** factorisation, **Huffman** coding and **Elias** universal integer codes, packed into a custom bit-level file format | 🟢 Encoder works |
| | [`compression/myunzip.py`](compression/myunzip.py) | Decoder: header parsing, Elias and Huffman decoding, LZ77 reconstruction | 🟡 In progress |
| **Graphs** | [`graphs/kruskal_mst.py`](graphs/kruskal_mst.py) | **Kruskal's MST** on a **disjoint-set / union-find** with union by height | 🟢 Union-find works · 🟡 Kruskal loop in progress |
| **Number theory** | [`number-theory/three_primes.py`](number-theory/three_primes.py) | **Miller-Rabin** randomised primality test, used to write an odd number as a sum of three primes (weak Goldbach) | 🟢 Works |

## Why this unit matters

These are the algorithms underneath tools used every day:

- **Boyer-Moore and the Z-algorithm:** fast text search, as in `grep`, editors and DNA matching.
- **Suffix trees:** linear-time substring queries, genome indexing and plagiarism detection.
- **LZ77 + Huffman:** the core idea behind DEFLATE (zip, gzip, PNG).
- **Elias codes:** compact, self-delimiting integers in compressed formats and indexes.
- **Union-find + Kruskal:** network design and clustering.
- **Miller-Rabin:** how RSA key generation finds large primes quickly.

## Running

Python 3.10+. The compression scripts need `bitarray`:

```bash
pip install bitarray

python -c "import sys; sys.path.insert(0,'number-theory'); import three_primes as t; print(t.primeOfThree(31))"
# [3, 5, 23]

cd compression && python myzip.py samples/x.asc 6 4
# writes samples/x.asc.bin
```
