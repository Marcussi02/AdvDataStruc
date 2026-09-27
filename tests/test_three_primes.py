import random

import pytest

from three_primes import millerRabinRandomisedPrimality, outputFile, primeOfThree


def sieve(limit):
    flags = [True] * (limit + 1)
    flags[0] = flags[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if flags[i]:
            flags[i * i::i] = [False] * len(flags[i * i::i])
    return flags


def test_miller_rabin_matches_sieve():
    flags = sieve(20000)
    rng = random.Random(1)
    for n in range(20001):
        assert millerRabinRandomisedPrimality(n, rng=rng) == flags[n], n


@pytest.mark.parametrize("n", [561, 1105, 1729, 2465, 2821, 6601, 8911, 41041])
def test_carmichael_numbers_are_composite(n):
    assert millerRabinRandomisedPrimality(n) is False


def test_large_known_values():
    assert millerRabinRandomisedPrimality(2**61 - 1)
    assert millerRabinRandomisedPrimality(1_000_000_007)
    assert not millerRabinRandomisedPrimality((2**31 - 1) * (2**61 - 1))


def test_three_primes_for_every_odd_number():
    flags = sieve(3000)
    for n in range(7, 3001, 2):
        p, q, r = primeOfThree(n)
        assert p + q + r == n and p <= q <= r
        assert flags[p] and flags[q] and flags[r]


def test_known_answers_and_invalid_inputs():
    assert primeOfThree(31) == [3, 5, 23]
    assert primeOfThree(7) == [2, 2, 3]
    assert primeOfThree(10) == [] and primeOfThree(5) == []


def test_output_file(tmp_path):
    path = tmp_path / "out.txt"
    assert outputFile("31", path) == [3, 5, 23]
    assert path.read_text() == "3 5 23"
