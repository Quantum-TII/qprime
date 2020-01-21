# QPrime

Compute entropy and trace of prime number sequences based on qbit states.
The library is designed to run on GPU and CPU using multi-threading.

## Installation

In order to install open a terminal, clone this repository using `git`:
```bash
git clone https://github.com/Quantum-TII/qprime.git
```

Then proceed with the python installation:
```bash
pip install .
```

## Examples

We have placed examples in the `examples` folder:
```bash
usage: primes.py [-h] n
primes.py: error: the following arguments are required: n
```
computes the prime numbers for quantum bits.

```bash
usage: reference_trace.py [-h] s n
reference_trace.py: error: the following arguments are required: s, n
```
compute the reference trace for state (s, n).

```bash
usage: traces.py [-h] s n
traces.py: error: the following arguments are required: s, n
```
computes the trace for a state (s, n)
