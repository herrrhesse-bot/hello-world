"""Train a small 1D CNN to map noisy sine curves back to clean sine curves."""

from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import torch
    from torch import Tensor, nn
    from torch.utils.data import DataLoader, TensorDataset, random_split
except ImportError:  # pragma: no cover - exercised in runtime environments without torch
    torch = None
    Tensor = Any
    nn = None
    DataLoader = None
    TensorDataset = None
    random_split = None


def torch_is_available() -> bool:
    return torch is not None


def require_torch() -> None:
    if not torch_is_available():
        raise RuntimeError(
            "PyTorch is not installed in the active environment. "
            "Install torch and rerun this example."
        )


@dataclass(frozen=True)
class TrainingConfig:
    samples: int = 256
    sequence_length: int = 128
    noise_std: float = 0.20
    batch_size: int = 32
    epochs: int = 60
    learning_rate: float = 0.01
    seed: int = 7


def generate_noisy_sine_dataset(
    samples: int = 256,
    sequence_length: int = 128,
    noise_std: float = 0.20,
    seed: int = 7,
) -> tuple[Tensor, Tensor, Tensor]:
    require_torch()
    generator = torch.Generator().manual_seed(seed)
    phase_rng = random.Random(seed)

    x_axis = torch.linspace(0.0, 2.0 * math.pi, sequence_length, dtype=torch.float32)
    clean_curves = []
    noisy_curves = []

    for _ in range(samples):
        amplitude = phase_rng.uniform(0.7, 1.3)
        frequency = phase_rng.uniform(0.8, 1.4)
        phase = phase_rng.uniform(0.0, math.pi)
        offset = phase_rng.uniform(-0.15, 0.15)

        clean = amplitude * torch.sin(frequency * x_axis + phase) + offset
        noise = torch.randn(sequence_length, generator=generator) * noise_std
        noisy = clean + noise

        clean_curves.append(clean)
        noisy_curves.append(noisy)

    features = torch.stack(noisy_curves).unsqueeze(1)
    targets = torch.stack(clean_curves).unsqueeze(1)
    return x_axis, features, targets


if torch_is_available():

    class SineCNN(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.network = nn.Sequential(
                nn.Conv1d(1, 16, kernel_size=9, padding=4),
                nn.ReLU(),
                nn.Conv1d(16, 16, kernel_size=9, padding=4),
                nn.ReLU(),
                nn.Conv1d(16, 1, kernel_size=9, padding=4),
            )

        def forward(self, inputs: Tensor) -> Tensor:
            return self.network(inputs)

else:

    class SineCNN:
        def __init__(self) -> None:
            require_torch()


def make_data_loaders(
    features: Tensor,
    targets: Tensor,
    batch_size: int,
    seed: int,
) -> tuple[Any, Any]:
    require_torch()
    dataset = TensorDataset(features, targets)
    train_size = int(len(dataset) * 0.8)
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = random_split(
        dataset,
        [train_size, test_size],
        generator=torch.Generator().manual_seed(seed),
    )
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    return train_loader, test_loader


def train_model(config: TrainingConfig) -> dict[str, Any]:
    require_torch()
    torch.manual_seed(config.seed)

    x_axis, features, targets = generate_noisy_sine_dataset(
        samples=config.samples,
        sequence_length=config.sequence_length,
        noise_std=config.noise_std,
        seed=config.seed,
    )
    train_loader, test_loader = make_data_loaders(
        features=features,
        targets=targets,
        batch_size=config.batch_size,
        seed=config.seed,
    )

    model = SineCNN()
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    loss_fn = nn.MSELoss()

    for epoch in range(1, config.epochs + 1):
        model.train()
        total_loss = 0.0
        seen = 0

        for batch_inputs, batch_targets in train_loader:
            optimizer.zero_grad()
            predictions = model(batch_inputs)
            loss = loss_fn(predictions, batch_targets)
            loss.backward()
            optimizer.step()

            batch_size = batch_inputs.size(0)
            total_loss += loss.item() * batch_size
            seen += batch_size

        if epoch == 1 or epoch % 10 == 0 or epoch == config.epochs:
            print(f"epoch {epoch:>3d}/{config.epochs}: train_mse={total_loss / seen:.6f}")

    metrics = evaluate_model(model, test_loader)
    return {
        "config": config,
        "model": model,
        "x_axis": x_axis,
        "features": features,
        "targets": targets,
        "metrics": metrics,
    }


def evaluate_model(model: Any, data_loader: Any) -> dict[str, float]:
    require_torch()
    model.eval()
    total_mse = 0.0
    total_mae = 0.0
    seen = 0

    with torch.no_grad():
        for batch_inputs, batch_targets in data_loader:
            predictions = model(batch_inputs)
            diff = predictions - batch_targets
            batch_size = batch_inputs.size(0)
            total_mse += torch.mean(diff.square()).item() * batch_size
            total_mae += torch.mean(diff.abs()).item() * batch_size
            seen += batch_size

    return {
        "test_mse": total_mse / seen,
        "test_mae": total_mae / seen,
    }


def save_plot_if_possible(
    x_axis: Tensor,
    features: Tensor,
    targets: Tensor,
    predictions: Tensor,
    output_path: Path,
) -> bool:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available; skipping plot generation.")
        return False

    output_path.parent.mkdir(parents=True, exist_ok=True)
    x_points = x_axis.detach().cpu().tolist()
    noisy = features[0, 0].detach().cpu().tolist()
    clean = targets[0, 0].detach().cpu().tolist()
    pred = predictions[0, 0].detach().cpu().tolist()

    figure, axis = plt.subplots(figsize=(9, 4.5))
    axis.plot(x_points, noisy, label="noisy input", alpha=0.6)
    axis.plot(x_points, clean, label="clean target", linewidth=2)
    axis.plot(x_points, pred, label="cnn prediction", linewidth=2)
    axis.set_title("Noisy sine denoising with a 1D CNN")
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.legend()
    figure.tight_layout()
    figure.savefig(output_path, dpi=150)
    plt.close(figure)
    print(f"saved plot to {output_path}")
    return True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=TrainingConfig.samples)
    parser.add_argument("--sequence-length", type=int, default=TrainingConfig.sequence_length)
    parser.add_argument("--noise-std", type=float, default=TrainingConfig.noise_std)
    parser.add_argument("--batch-size", type=int, default=TrainingConfig.batch_size)
    parser.add_argument("--epochs", type=int, default=TrainingConfig.epochs)
    parser.add_argument("--learning-rate", type=float, default=TrainingConfig.learning_rate)
    parser.add_argument("--seed", type=int, default=TrainingConfig.seed)
    parser.add_argument(
        "--plot-path",
        type=Path,
        default=Path("projects/ml/noisy_sine_cnn/artifacts/noisy_sine_fit.png"),
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = TrainingConfig(
        samples=args.samples,
        sequence_length=args.sequence_length,
        noise_std=args.noise_std,
        batch_size=args.batch_size,
        epochs=args.epochs,
        learning_rate=args.learning_rate,
        seed=args.seed,
    )
    result = train_model(config)
    model = result["model"]
    model.eval()

    with torch.no_grad():
        predictions = model(result["features"])

    metrics = result["metrics"]
    print("evaluation summary:")
    print(f"  test_mse={metrics['test_mse']:.6f}")
    print(f"  test_mae={metrics['test_mae']:.6f}")

    save_plot_if_possible(
        x_axis=result["x_axis"],
        features=result["features"],
        targets=result["targets"],
        predictions=predictions,
        output_path=args.plot_path,
    )


if __name__ == "__main__":
    main()
