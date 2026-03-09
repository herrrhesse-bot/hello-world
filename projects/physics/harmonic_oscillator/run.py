"""Simulate a 1D harmonic oscillator with a symplectic Euler integrator."""

from __future__ import annotations

import math

from shared.text import format_table


def simulate(
    steps: int = 200,
    dt: float = 0.05,
    position: float = 1.0,
    velocity: float = 0.0,
    mass: float = 1.0,
    spring_constant: float = 1.0,
) -> list[tuple[float, float, float, float]]:
    omega = math.sqrt(spring_constant / mass)
    state: list[tuple[float, float, float, float]] = []
    x = position
    v = velocity

    for step in range(steps + 1):
        time = step * dt
        energy = 0.5 * mass * v * v + 0.5 * spring_constant * x * x
        state.append((time, x, v, energy))

        acceleration = -(omega * omega) * x
        v += dt * acceleration
        x += dt * v

    return state


def run_model() -> None:
    trajectory = simulate()
    rows = [
        [f"{time:.2f}", f"{x:.4f}", f"{v:.4f}", f"{energy:.6f}"]
        for time, x, v, energy in trajectory[::40]
    ]
    energies = [energy for _, _, _, energy in trajectory]

    print("Harmonic oscillator trajectory sample")
    print(format_table(["t", "x", "v", "energy"], rows))
    print()
    print(
        "Energy range:",
        f"{min(energies):.6f} .. {max(energies):.6f}",
        f"(drift span {max(energies) - min(energies):.6f})",
    )


if __name__ == "__main__":
    run_model()
