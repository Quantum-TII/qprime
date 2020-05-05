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
usage: primes.py [-h] nqubits
```
computes the prime numbers for quantum bits.

If quadruple precision is needed you can run the example:
```bash
usage: primes_quad_mplapack.py [-h] nqubits
```
after compiling the respective c++ code with `make`.

```bash
usage: reference_trace.py [-h] pows nqubits
```
compute the reference trace for state (pows, nqubits).

```bash
usage: traces.py [-h] pows nqubits
```
computes the trace for a state (pows, nqubits).
