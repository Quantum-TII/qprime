#!/usr/bin/env python
"""
Computes entropy for a given number of even qbits n.
"""
import argparse
import numpy as np
from sympy.ntheory import mobius as mu
from sympy.ntheory import totient as phi
from qprime.api import entropy


def Lambda(kk, n):
    m = n//2
    w = np.zeros(kk.shape[0])
    for k in range(1, len(kk)+1):
        w[k-1] = 2**(1-m)*np.abs(mu(k))*(1+2**m/(phi(k)**2*n*np.log(2)))
    return w


def main(n):
    e, p, u, w = entropy(n)
    k = np.arange(1, 2**(n//2-1))
    w2 = Lambda(k, n)
    w2 = w2[w2 > 0]
    print('Eigenvalues entropy:', w)
    print('Eigenvalues formula:', w2)
    np.save('eig_entropy_n%d.npy' % n, w)
    np.save('eig_formula_n%d.npy' % n, w2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Prime numbers entropy')
    parser.add_argument('n', type=int, help='an integer for the number of qbits')
    args = parser.parse_args()
    main(args.n)
