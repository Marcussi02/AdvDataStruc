import random

import pytest

from generalised_suffix_tree import GeneralisedSuffixTree, build_suffix_tree


def brute_occurrences(strings, pat):
    return sorted(
        (i, j)
        for i, s in enumerate(strings)
        for j in range(len(s) - len(pat) + 1)
        if s[j : j + len(pat)] == pat
    )


def brute_lcs_length(strings):
    first = strings[0]
    best = 0
    for a in range(len(first)):
        for b in range(a + best + 1, len(first) + 1):
            if all(first[a:b] in s for s in strings[1:]):
                best = b - a
            else:
                break
    return best


def test_single_string_suffixes_are_all_found():
    tree = build_suffix_tree("mississippi")
    for i in range(len("mississippi")):
        assert tree.contains("mississippi"[i:])
    assert tree.occurrences("issi") == [(0, 1), (0, 4)]
    assert not tree.contains("issp")


def test_every_suffix_is_one_leaf():
    text = "abcabxabcd"
    tree = build_suffix_tree(text)
    leaves, stack = [], [tree.root]
    while stack:
        node = stack.pop()
        if node.is_leaf:
            leaves.append(node.suffix_start)
        stack.extend(node.children.values())
    assert sorted(leaves) == list(range(len(text) + 1))  # every suffix, plus the terminator


@pytest.mark.parametrize("alphabet", ["ab", "abc", "acgt"])
def test_occurrences_match_brute_force(alphabet):
    rng = random.Random(alphabet)
    for _ in range(300):
        strings = [
            "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 25)))
            for _ in range(rng.randint(1, 4))
        ]
        tree = GeneralisedSuffixTree(strings)
        for _ in range(10):
            pat = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 5)))
            assert tree.occurrences(pat) == brute_occurrences(strings, pat), (strings, pat)


def test_longest_common_substring():
    assert GeneralisedSuffixTree(["banana", "ananas"]).longest_common_substring() == "anana"
    assert GeneralisedSuffixTree(["abc", "xyz"]).longest_common_substring() == ""
    rng = random.Random(7)
    for _ in range(300):
        strings = ["".join(rng.choice("ab") for _ in range(rng.randint(1, 15))) for _ in range(3)]
        lcs = GeneralisedSuffixTree(strings).longest_common_substring()
        assert len(lcs) == brute_lcs_length(strings)
        assert all(lcs in s for s in strings)


def test_long_input_does_not_hit_recursion_limit():
    tree = build_suffix_tree("a" * 20000 + "b")
    assert tree.occurrences("ab") == [(0, 19999)]
