"""
Define some operations required for the entropy and trace calculation.
"""
import numpy as np
import numba as nb
import tensorflow as tf

# mininum threshold for the eigenvalues
EIG_EPS = 1E-11


def reference_entropy():
    """ Computes the asymptotic behaviour for the
    scaling of the entropy.

    Returns
    -------
        The asymptotic value
    """
    return -3 / np.pi**2 * np.log2(3 / np.pi**2) - (1 - 3 / np.pi**2) * np.log2( 1 - 3 / np.pi**2 )


@tf.function
def make_density_matrix(state, norm):
    """ Computes the density matrix (rho) for a given state
    of prime numbers.

    Parameters
    ----------
        `state`: the binary matrix containing the encoded primes
        `norm`: the number of generated primes (PrimePi)

    Returns
    -------
        The unnormalized density matrix of the prime state
    """
    return tf.linalg.matmul(tf.transpose(state), state) / norm


@tf.function
def get_eigenvalues(rho, eps=EIG_EPS):
    """ Computes the eigenvalues of the density matrix
    and applies a threshold filtering condition.

    Parameters
    ----------
        `rho`: the normalized density matrix
        `eps`: minimum threshold to accept the eigenvalue

    Returns
    -------
        The filtered eigenvalue array

    """
    # compute eigenvalues
    w = tf.linalg.eigvalsh(rho)

    # apply eigenvalues filtering
    wf = tf.gather(w, tf.where(w > eps))

    return wf


@tf.function
def compute_entropy(w):
    """ Computes the entropy for the eigenvalues of the
    density matrix.

    Parameters
    ----------
        `w`: the eigenvalues of the density matrix

    Returns
    -------
        The entropy of the state.
    """
    return -tf.reduce_sum(w*tf.math.log(w)) / np.log(2)


@tf.function
def compute_purity(w):
    """ Computes the purity for the eigenvalues of the
    density matrix.

    Parameters
    ----------
        `w`: the eigenvalues of the density matrix

    Returns
    -------
        The purity of the state
    """
    return tf.reduce_sum(tf.square(w))


@tf.function
def compute_unitarity(w):
    """ Compute the unitarity for the eigenvalues of the
    density matrix.

    Parameters
    ----------
        `w`: the eigenvalues of the density matrix

    Returns
    -------
        The unitarity of the state
    """
    return tf.reduce_sum(w)


@tf.function
def check_purity(rho):
    """ Computes the purity from the density matrix.

    Parameters
    ----------
        `rho`: the normalized density matrix

    Returns
    -------
        The purity of the density matrix state
    """
    p = tf.reduce_sum(
            tf.linalg.diag_part(
                tf.linalg.matmul(rho, tf.transpose(rho))
            )
        )
    return p


@tf.function
def check_unitarity(rho):
    """ Computes the unitarity of the density matrix.

    Parameters
    ----------
        `rho`: the normalized density matrix

    Returns
    -------
        The unitarity of the density matrix
    """
    return tf.reduce_sum(
            tf.linalg.diag_part(rho)
            )


@nb.njit(parallel=True)
def build_state(n):
    """ Computes prime numbers using the sieve of Atkin up to 2**n.
    The prime numbers are not stored in memory, instead the state
    matrix is computed from the sieve mask.

    This algoritm works only for even n.

    Parameters
    ----------
        `n`: the number of qbits for the system

    Returns
    -------
        The binary matrix containing the encoded primes.
        The total number of generated prime numbers.

    """
    limit = 2**n
    sieve = np.zeros(limit, dtype=np.ubyte)
    x = 1
    while(x * x < limit ) :
        y = 1
        while(y * y < limit ) :
            # Main part of
            # Sieve of Atkin
            z = (4 * x * x) + (y * y)
            z12 = z % 12
            if (z <= limit and (z12 == 1 or
                                z12 == 5)):
                sieve[z] = not sieve[z]

            z = (3 * x * x) + (y * y)
            z12 = z % 12
            if (z <= limit and z12 == 7):
                sieve[z] = not sieve[z]

            z = (3 * x * x) - (y * y)
            z12 = z % 12
            if (x > y and z <= limit and z12 == 11):
                sieve[z] = not sieve[z]
            y += 1
        x += 1
    # Mark all multiples of
    # squares as non-prime
    r = 5
    while(r * r < limit) :
        if (sieve[r]) :
            for i in range(r * r, limit, r * r):
                sieve[i] = 0
        r += 1
    # Print primes
    norm = np.int64(2**(n/2))
    pp = np.zeros(shape=(norm, norm//2), dtype=np.int32)
    pp[0,0] = 1 # 2
    pp[0,1] = 1 # 3
    size = 2
    for i in range(5, limit, 2):
        if sieve[i] == 1:
            b = np.int64(i % norm)
            a = np.int64((i - b) / norm)
            b = np.int64((b-1)/2)
            pp[a, b] = 1
            size += 1
    return pp, size