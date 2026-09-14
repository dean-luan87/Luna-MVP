"""Error namespace types for Runtime Executor controlled implementation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeExecutorErrorV1:
    code: str
    message: str
    category: str
    recoverable: bool


def make_error(
    code: str, message: str, category: str, recoverable: bool
) -> RuntimeExecutorErrorV1:
    return RuntimeExecutorErrorV1(
        code=code,
        message=message,
        category=category,
        recoverable=recoverable,
    )
