#!/usr/bin/env python
"""
Computes entropy for a given number of even qbits n.
"""
import argparse
from qprime.api import entropy_mpf


def main(n, bits):
    e = entropy_mpf(n, bits=bits)
    print('\n> Final entropy', e)
    with open('entropy_n%d.dat' % n, 'w') as f:
        f.write('%d %s\n' % (n, e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Prime numbers entropy')
    parser.add_argument('n', type=int, help='an integer for the number of qbits')
    parser.add_argument('--bits', type=int, default=113, help='number of bits for the operation, default 113 (quadruple precision)')
    args = parser.parse_args()
    main(args.n, args.bits)
