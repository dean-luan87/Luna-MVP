"""Canonical local JSON serialization for A3 Runtime Skeleton DryRun v1."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Mapping


def to_jsonable_v1(value: Any) -> Any:
    """Convert immutable DryRun values without resolving any reference."""
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return to_jsonable_v1(asdict(value))
    if isinstance(value, Mapping):
        return {str(key): to_jsonable_v1(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [to_jsonable_v1(item) for item in value]
    if isinstance(value, list):
        return [to_jsonable_v1(item) for item in value]
    return value


def serialize_json_v1(value: Any) -> str:
    """Return deterministic canonical JSON text for an already-built value."""
    return json.dumps(to_jsonable_v1(value), indent=2, sort_keys=True) + "\n"


def write_json_v1(path: Path, value: Any) -> None:
    path.write_text(serialize_json_v1(value), encoding="utf-8")


def read_json_v1(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))
