"""Small timing helpers."""

from __future__ import annotations

from time import perf_counter
from typing import Any, Callable


def timed_call(func: Callable[..., Any], *args: Any, **kwargs: Any) -> tuple[float, Any]:
    start = perf_counter()
    result = func(*args, **kwargs)
    elapsed = perf_counter() - start
    return elapsed, result
