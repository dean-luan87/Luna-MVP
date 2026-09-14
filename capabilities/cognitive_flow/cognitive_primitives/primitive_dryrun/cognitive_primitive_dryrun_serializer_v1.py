"""Canonical JSON serializer for Primitive DryRun evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .cognitive_primitive_dryrun_types_v1 import PRIMITIVE_DRYRUN_RESULT_V1


def canonical_json_v1(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_result_v1(output_dir: Path, value: Any) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / PRIMITIVE_DRYRUN_RESULT_V1).write_text(canonical_json_v1(value), encoding="utf-8")

