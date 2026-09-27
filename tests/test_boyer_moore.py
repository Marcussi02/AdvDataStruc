import random

import pytest

from modified_boyer_moore import GS, MP, boyerMoore, zalgro


def brute_z(s):
    return [len(s)] + [
        next((k for k in range(len(s) - i) if s[k] != s[i + k]), len(s) - i)
        for i in range(1, len(s))
    ] if s else []


def brute_find(txt, pat):
    return [i for i in range(len(txt) - len(pat) + 1) if txt[i : i + len(pat)] == pat]


def test_z_algorithm_textbook_example():
    assert zalgro("aabxaabxcaabxaabxay")[:9] == [19, 1, 0, 0, 4, 1, 0, 0, 0]


@pytest.mark.parametrize("seed", range(5))
def test_z_matches_brute_force(seed):
    rng = random.Random(seed)
    for _ in range(300):
        s = "".join(rng.choice("ab") for _ in range(rng.randint(0, 30)))
        assert zalgro(s) == brute_z(s)


def test_matched_prefix_and_good_suffix_tables():
    assert MP("abcab") == [5, 2, 2, 2, 0, 0]
    gs = GS("abcab")
    assert gs[3] == 1  # suffix "ab" reappears ending at index 1


@pytest.mark.parametrize("alphabet", ["ab", "abc", "acgt", "abcdefgh"])
def test_boyer_moore_matches_brute_force(alphabet):
    rng = random.Random(alphabet)
    for _ in range(2000):
        txt = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 60)))
        pat = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 6)))
        assert boyerMoore(txt, pat) == brute_find(txt, pat), (txt, pat)


def test_overlapping_and_edge_cases():
    assert boyerMoore("aaaaa", "aa") == [0, 1, 2, 3]
    assert boyerMoore("abc", "abcd") == []
    assert boyerMoore("abc", "") == []
    assert boyerMoore("hello world", "o w") == [4]
