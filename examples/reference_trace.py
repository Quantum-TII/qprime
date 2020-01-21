#!/usr/bin/env python
"""
Computes entropy for a given number of even qbits n.
"""
import argparse
from qprime.api import compute_reference_trace


def main(s, n):
    r = compute_reference_trace(s, n)
    print('\n> Reference trace for s=%d, n=%d primes is %.10e <\n' % (s, n, r))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Prime numbers entropy')
    parser.add_argument('s', type=int, help='an integer for the number of qbits')
    parser.add_argument('n', type=int, help='an integer for the number of qbits')
    args = parser.parse_args()
    main(args.s, args.n)
