"""Boyer-Moore string matching with bad-character, good-suffix and matched-prefix rules.

All preprocessing is built on the Z-algorithm (Gusfield's formulation):

- extended bad character: for each position k and character x, the rightmost
  occurrence of x in pat[:k], so a mismatch shifts the pattern just far enough
  to line that occurrence up with the mismatched text character
- good suffix: from the Z-values of the reversed pattern, the rightmost other
  copy of the matched suffix pat[k+1:] that is preceded by a different character
- matched prefix: the longest suffix of pat[k:] that is also a prefix of pat,
  used when the good suffix does not reappear, and after a full match

The shift at a mismatch is the larger of the bad-character and good-suffix
shifts, so the scan never skips an occurrence. Worst case O(nm) without Galil's
optimisation; sublinear on typical text.

    python modified_boyer_moore.py text.txt pattern.txt   # prints 1-based positions
"""

import sys


def zalgro(s: str) -> list[int]:
    """z[i] = length of the longest substring starting at i that matches a prefix of s."""
    n = len(s)
    if n == 0:
        return []
    z = [0] * n
    z[0] = n
    left = right = 0  # current Z-box is s[left:right]
    for i in range(1, n):
        if i < right:  # inside a Z-box: reuse the value from the matching prefix position
            z[i] = min(z[i - left], right - i)
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:  # extend explicitly past the box
            z[i] += 1
        if i + z[i] > right:
            left, right = i, i + z[i]
    return z


def BC(pat: str) -> list[dict[str, int]]:
    """bc[k][x] = rightmost index j < k with pat[j] == x (missing key means none).

    Built left to right: each position inherits the table of the previous one,
    updated with the character just passed. Stored as small dicts rather than a
    full alphabet-by-length matrix, so any character set works.
    """
    table: list[dict[str, int]] = []
    last: dict[str, int] = {}
    for k, ch in enumerate(pat):
        table.append(last)
        last = {**last, ch: k}
    return table


def GS(pat: str) -> list[int]:
    """gs[j] = end index p of the rightmost copy of the suffix pat[j:] that is not a
    suffix of pat and is preceded by a different character; -1 if none. gs has m+1 entries."""
    m = len(pat)
    # Z-values of the reversed pattern give, for each end position p, the length of
    # the longest substring ending at p that is also a suffix of pat.
    z_rev = zalgro(pat[::-1])
    z_suffix = [z_rev[m - 1 - p] for p in range(m)]
    gs = [-1] * (m + 1)
    for p in range(m - 1):  # p = m-1 would be the suffix itself
        length = z_suffix[p]
        if length:
            gs[m - length] = p  # later (larger) p overwrites: rightmost copy wins
    return gs


def MP(pat: str) -> list[int]:
    """mp[k] = length of the longest suffix of pat[k:] that is also a prefix of pat."""
    m = len(pat)
    z = zalgro(pat)
    mp = [0] * (m + 1)
    for k in range(m - 1, -1, -1):
        mp[k] = z[k] if z[k] + k == m else mp[k + 1]
    return mp


def boyerMoore(txt: str, pat: str) -> list[int]:
    """0-based start positions of every occurrence of pat in txt."""
    n, m = len(txt), len(pat)
    if m == 0 or m > n:
        return []
    bc, gs, mp = BC(pat), GS(pat), MP(pat)
    full_match_shift = m - mp[1] if m > 1 else 1
    result = []
    s = 0  # alignment of pat[0] in txt
    while s <= n - m:
        k = m - 1
        while k >= 0 and pat[k] == txt[s + k]:  # compare right to left
            k -= 1
        if k < 0:
            result.append(s)
            s += full_match_shift
            continue
        bc_shift = k - bc[k].get(txt[s + k], -1)
        if k == m - 1:
            gs_shift = 1  # nothing matched yet, so there is no good suffix
        elif gs[k + 1] >= 0:
            gs_shift = m - 1 - gs[k + 1]
        else:
            gs_shift = m - mp[k + 1]
        s += max(bc_shift, gs_shift, 1)
    return result


def read_file(filename: str) -> str:
    with open(filename, encoding="utf-8") as f:
        return f.read().rstrip("\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python modified_boyer_moore.py <text file> <pattern file>")
    text, pattern = read_file(sys.argv[1]), read_file(sys.argv[2])
    for position in boyerMoore(text, pattern):
        print(position + 1)
