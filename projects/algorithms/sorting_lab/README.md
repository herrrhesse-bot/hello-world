# Sorting Lab

Small benchmark-oriented experiment comparing a few sorting implementations on random integer arrays.

Included algorithms:

- built-in `sorted`
- insertion sort
- merge sort

## Run

From the repo root:

```bash
python3 -m projects.algorithms.sorting_lab.run
```

or:

```bash
make sorting
```

## What It Shows

- asymptotic differences become visible quickly
- simple custom Python sorts are useful for learning, but not competitive with the built-in implementation
- benchmark plumbing stays small and easy to modify
