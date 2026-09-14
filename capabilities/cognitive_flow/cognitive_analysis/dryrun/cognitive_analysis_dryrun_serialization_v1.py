"""Deterministic local JSON/Markdown output helpers for A3 DryRun v1."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .cognitive_analysis_dryrun_types_v1 import to_jsonable_v1


def write_json_v1(path: Path, value: Any) -> None:
    path.write_text(json.dumps(to_jsonable_v1(value), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json_v1(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))
