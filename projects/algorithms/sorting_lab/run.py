"""Compare a few sorting strategies on random integer data."""

from __future__ import annotations

import random
from statistics import median

from shared.text import format_table
from shared.timing import timed_call


def insertion_sort(values: list[int]) -> list[int]:
    items = values[:]
    for index in range(1, len(items)):
        current = items[index]
        position = index - 1
        while position >= 0 and items[position] > current:
            items[position + 1] = items[position]
            position -= 1
        items[position + 1] = current
    return items


def merge_sort(values: list[int]) -> list[int]:
    if len(values) <= 1:
        return values[:]

    midpoint = len(values) // 2
    left = merge_sort(values[:midpoint])
    right = merge_sort(values[midpoint:])

    merged: list[int] = []
    left_index = 0
    right_index = 0
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged


def run_benchmark() -> None:
    rng = random.Random(7)
    sizes = [32, 128, 512, 2048]
    algorithms = [
        ("sorted", sorted),
        ("insertion_sort", insertion_sort),
        ("merge_sort", merge_sort),
    ]
    rows: list[list[str]] = []

    for size in sizes:
        sample = [rng.randint(-10_000, 10_000) for _ in range(size)]
        baseline = sorted(sample)
        for name, func in algorithms:
            runs = []
            for _ in range(5):
                elapsed, output = timed_call(func, sample)
                if output != baseline:
                    raise ValueError(f"{name} produced an incorrect result for n={size}")
                runs.append(elapsed * 1_000_000)

            rows.append(
                [
                    str(size),
                    name,
                    f"{median(runs):.1f}",
                    f"{min(runs):.1f}",
                    f"{max(runs):.1f}",
                ]
            )

    print("Sorting benchmark (microseconds)")
    print(format_table(["n", "algorithm", "median", "min", "max"], rows))


if __name__ == "__main__":
    run_benchmark()
