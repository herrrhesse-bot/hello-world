# Toybox

Lightweight sandbox for small computational, scientific, and programming experiments.

This repository is organized as a toybox rather than a single app. Each experiment lives in its own small directory, shared helpers stay minimal, and benchmarks have a clear place when they stop being one-off snippets.

## Layout

```text
.
|-- benchmarks/                  # Cross-project benchmark scripts and notes
|-- projects/                    # Self-contained toy experiments
|   |-- algorithms/
|   |   `-- sorting_lab/
|   `-- physics/
|       `-- harmonic_oscillator/
|-- shared/                      # Tiny reusable Python helpers
|-- Makefile
`-- pyproject.toml
```

## Included Examples

### Algorithm / benchmark example

`projects/algorithms/sorting_lab/` compares a few sorting strategies on random integer arrays:

- Python's built-in `sorted`
- insertion sort
- merge sort

Run it from the repo root:

```bash
python3 -m projects.algorithms.sorting_lab.run
```

Or:

```bash
make sorting
```

### Physics / model example

`projects/physics/harmonic_oscillator/` simulates a 1D harmonic oscillator with a simple symplectic Euler integrator and reports position, velocity, and energy behavior.

Run it from the repo root:

```bash
python3 -m projects.physics.harmonic_oscillator.run
```

Or:

```bash
make oscillator
```

## Conventions For New Toy Projects

Add a new experiment under `projects/<topic>/<project_name>/`.

Recommended contents:

```text
projects/<topic>/<project_name>/
|-- README.md
|-- __init__.py
`-- run.py
```

Keep projects small and self-contained:

- Put project-specific code next to the project.
- Put genuinely reusable helpers in `shared/`.
- Put benchmark-only scripts in `benchmarks/` when they compare multiple projects or explore performance outside one project.
- Prefer standard library Python first. Add dependencies only when they clearly pay for themselves.

If a project later needs multiple languages, keep one project root and add language-specific subdirectories like `python/`, `rust/`, or `cpp/`.

## Setup

Python 3.11+ is recommended.

Optional editable install:

```bash
python3 -m pip install -e .
```

The examples also run directly from the repo root without installation.

## Quick Start

```bash
make help
make sorting
make oscillator
```

## Benchmarks And Shared Utilities

- `benchmarks/README.md` explains what belongs in `benchmarks/`.
- `shared/` contains tiny helpers for timing and table formatting used by the examples.

The goal is a practical toybox: simple scripts, clear structure, and enough consistency that adding the next experiment is frictionless.
