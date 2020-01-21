"""
Define pipeline for the entropy and trace calculation.
"""
import time
from qprime.engine import build_state, make_density_matrix, \
                          check_purity, check_unitarity, \
                          compute_entropy, compute_purity, \
                          compute_unitarity, get_eigenvalues

class timer:
    def __init__(self):
        pass

    def start(self):
        self.t0 = time.time()
        self.t1 = time.process_time()

    def print(self, message):
        d0 = time.time() - self.t0
        d1 = time.process_time() - self.t1
        print("%fs (wall) | %fs (cpu) - %s" % (d0, d1, message))


def entropy(n, verbose=True):
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
    t_b = t
    t.start()
    pp, size = build_state(n)
    t.print('prime number generation [1/4]')

    # build the density
    t.start()
    rho = make_density_matrix(pp, size)
    t.print('density construction [2/4]')

    #print(check_purity(rho), check_unitarity(rho))

    t.start()
    w = get_eigenvalues(rho)
    t.print('eigenvalues [3/4]')

    t.start()
    entropy = compute_entropy(w)
    unitarity = compute_unitarity(w)
    purity = compute_purity(w)
    t.print('entropy [4/4]')

    if verbose:
        t_b.print('total execution time')

    return entropy.numpy(), unitarity.numpy(), purity.numpy()