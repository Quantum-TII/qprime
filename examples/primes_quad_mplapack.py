#!/usr/bin/env python
"""
Computes entropy for a given number of even qbits n.
This program computes numbers using quadruple precision.
"""
import argparse
import tensorflow as tf
from qprime.api import timer
from qprime.engine import build_state
import eigen


def main(n):
    pp, size = build_state(n)

    # build the density as integer matrix
    rho = tf.linalg.matmul(tf.transpose(pp), pp)

    # send rho and size to the quadruple eigen implementation
    print('Starting eigen.so:')
    e = eigen.entropy(rho, size)

    print('\n> Final entropy', e)
    filename = 'entropy_n%d.dat' % n
    print('Writing result to %s' % filename)
    with open(filename, 'w') as f:
        f.write('%d %s\n' % (n, e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Prime numbers entropy')
    parser.add_argument('n', type=int, help='an integer for the number of qbits')
    args = parser.parse_args()
    main(args.n)
