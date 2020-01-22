"""
Define pipeline for the entropy and trace calculation.
"""
import time
import numba as nb
import numpy as np
import tensorflow as tf
from qprime.engine import build_state, make_density_matrix, \
                          check_purity, check_unitarity, \
                          compute_entropy, compute_purity, \
                          compute_unitarity, get_eigenvalues, \
                          atkin, build_trace

class timer:
    """ A trivial timer class. """
    def __init__(self):
        pass

    def start(self):
        self.t0 = time.time()
        self.t1 = time.process_time()

    def print(self, message):
        d0 = time.time() - self.t0
        d1 = time.process_time() - self.t1
        print("%fs (wall) | %fs (cpu) - %s" % (d0, d1, message))


def entropy(n):
    """ Computes the prime number entropy.

    Parameters
    ----------
        `n`: number of qbits
        `verbose`: flag which enables printing.

    Return
    ------
        The entropy, unitarity and purity.
    """
    # build the state
    t = timer()
    t_b = timer()
    t_b.start()
    t.start()
    pp, size = build_state(n)
    t.print('prime number generation [1/4]')

    # build the density
    t.start()
    rho = make_density_matrix(pp, size)
    t.print('density construction [2/4]')

    #print(check_purity(rho), check_unitarity(rho))

    t.start()
    w = get_eigenvalues(rho, 0)
    t.print('eigenvalues [3/4]')

    t.start()
    entropy = compute_entropy(w)
    unitarity = compute_unitarity(w)
    purity = compute_purity(w)
    t.print('entropy [4/4]')

    t_b.print('total execution time')

    return entropy.numpy(), unitarity.numpy(), purity.numpy(), w.numpy()


@nb.njit
def compute_reference_trace(s, n):
    """ Computes the reference for the trace.

    Parameters
    ----------
        `s`: the s power.
        `n`: the number of elements for the series
    Returns
    -------
        The reference value
    """
    limit = 2**n
    sieve = atkin(n)

    def ratio(p):
        return (1.0+1.0/np.float64(p-1)**(2*s-1))

    ref = ratio(3)
    for i in range(5, limit, 2):
        if sieve[i] == 1:
            ref *= ratio(i)
    return ref


def trace(n, s):
    """ Compute trace.

    Parameters
    ----------
        `n`: the number of qubits

    Results
    -------
        The trace.
    """
    t = timer()
    t.start()
    m = n/2
    c = build_trace(n)
    cs = np.eye(c.shape[0], dtype=np.float64)
    for _ in range(s):
        cs = tf.linalg.matmul(cs, c)
    tr = 2**(-m*s)*tf.linalg.trace(cs)
    t.print('total execution time')
    return tr.numpy()
