"""Canonical serializer for A3 Translation Layer Controlled DryRun v1."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any


TRANSLATION_DRYRUN_RESULT_FILENAME_V1 = "cognitive_translation_dryrun_result_v1.json"
TRANSLATION_DRYRUN_VERIFICATION_FILENAME_V1 = "cognitive_translation_dryrun_verification_v1.json"


def canonical_json_v1(value: Any) -> str:
    """Serialize data deterministically; no external access or skeleton invocation occurs here."""
    if hasattr(value, "__dataclass_fields__"):
        value = asdict(value)
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def write_translation_dryrun_result_v1(output_dir: Path, value: Any) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / TRANSLATION_DRYRUN_RESULT_FILENAME_V1
    path.write_text(canonical_json_v1(value), encoding="utf-8")
    return path


def write_translation_dryrun_verification_v1(output_dir: Path, value: Any) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / TRANSLATION_DRYRUN_VERIFICATION_FILENAME_V1
    path.write_text(canonical_json_v1(value), encoding="utf-8")
    return path
