#!/usr/bin/env python
"""
Computes entropy for a given number of even qbits n.
"""
import argparse
from qprime.api import entropy


def main(n):
    e, p, u, w = entropy(n)
    print('\n> Final entropy for %d qubit primes is %.10e <\n' % (n, e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Prime numbers entropy')
    parser.add_argument('n', type=int, help='an integer for the number of qbits')
    args = parser.parse_args()
    main(args.n)
