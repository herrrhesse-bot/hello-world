# Harmonic Oscillator

Simple 1D harmonic oscillator toy model using a symplectic Euler time stepper.

State variables:

- position `x`
- velocity `v`

Model:

- mass `m = 1`
- spring constant `k = 1`
- force `F = -kx`

## Run

From the repo root:

```bash
python3 -m projects.physics.harmonic_oscillator.run
```

or:

```bash
make oscillator
```

## What It Shows

- a basic time integrator for a standard physics toy model
- approximate energy conservation with a symplectic method
- a compact pattern for future numerical experiments
