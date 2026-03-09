# Projects

Each subdirectory in `projects/` is a self-contained experiment.

Use topic groupings when they help:

- `projects/algorithms/...`
- `projects/physics/...`
- `projects/numerics/...`
- `projects/ml/...`

Current ML example:

- `projects/ml/noisy_sine_cnn/` for a compact PyTorch `Conv1d` denoising experiment on synthetic sine-wave data

For a new project, start with:

```text
projects/<topic>/<project_name>/
|-- README.md
|-- __init__.py
`-- run.py
```

Prefer direct runnable entry points over framework-heavy structure.
