# Noisy Sine CNN

This toy project trains a small 1D convolutional neural network in PyTorch to map noisy sine curves back to their clean sine targets.

It keeps the setup deliberately small:

- synthetic sine-wave dataset generated on the fly
- a compact `Conv1d` model
- short training loop with printed loss updates
- simple evaluation summary with test MSE and MAE
- optional plot saving when `matplotlib` is installed

## Run

From the repo root, use the existing micromamba environment:

```bash
XDG_CACHE_HOME=/tmp/.cache /home/sure/Downloads/bin/micromamba run -n toybox-dev \
  python -m projects.ml.noisy_sine_cnn.run
```

You can reduce runtime further with fewer epochs:

```bash
XDG_CACHE_HOME=/tmp/.cache /home/sure/Downloads/bin/micromamba run -n toybox-dev \
  python -m projects.ml.noisy_sine_cnn.run --epochs 20 --samples 128
```

If `matplotlib` is available, the script saves a plot to:

```text
projects/ml/noisy_sine_cnn/artifacts/noisy_sine_fit.png
```

If `matplotlib` is not installed, the script still trains and prints results.

## Notes

- The model is doing denoising rather than forecasting: input is a noisy sine trace, target is the clean trace.
- The code expects `torch` to be installed in `toybox-dev`.
