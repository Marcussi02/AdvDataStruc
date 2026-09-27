"""Write an odd number as a sum of three primes (weak Goldbach).

Primality is tested with the randomised Miller-Rabin test.

Usage::

    python three_primes.py 31      # writes "3 5 23" to output_threeprimes.txt
"""

import random
import sys

_SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def millerRabinRandomisedPrimality(n, k=20, rng=random):
    """Return True if n is (very probably) prime, False if n is composite.

    Each of the k rounds picks a random witness a in [2, n-2]. A composite n
    survives one round with probability at most 1/4.
    """
    if n < 2:
        return False
    for p in _SMALL_PRIMES:
        if n % p == 0:
            return n == p

    # n - 1 = 2^s * t with t odd
    s, t = 0, n - 1
    while t % 2 == 0:
        s += 1
        t //= 2

    for _ in range(k):
        a = rng.randrange(2, n - 1)
        x = pow(a, t, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            # never reached -1: a is a witness that n is composite
            return False
    return True


def primeOfThree(n, is_prime=millerRabinRandomisedPrimality):
    """Return [p, q, r] with p <= q <= r, all prime and p + q + r == n.

    Returns [] if n is not an odd number greater than 5. The search picks
    the smallest possible p, then the smallest q, so the answer is
    deterministic.
    """
    if n <= 5 or n % 2 == 0:
        return []
    p = 2
    while 3 * p <= n:
        if is_prime(p):
            q = p
            while p + 2 * q <= n:
                r = n - p - q
                if is_prime(q) and is_prime(r):
                    return [p, q, r]
                q += 1
        p += 1
    return []


def outputFile(N, path="output_threeprimes.txt"):
    lst = primeOfThree(int(N))
    with open(path, "w") as f:
        f.write(" ".join(str(x) for x in lst))
    return lst


def main(argv):
    if len(argv) != 2:
        print("usage: python three_primes.py <odd number > 5>", file=sys.stderr)
        return 1
    result = outputFile(argv[1])
    if not result:
        print("no decomposition: input must be an odd number greater than 5",
              file=sys.stderr)
        return 1
    print(*result)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
