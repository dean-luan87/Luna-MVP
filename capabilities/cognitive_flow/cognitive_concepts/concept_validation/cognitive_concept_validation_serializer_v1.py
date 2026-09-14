"""Canonical serialization for Concept Validation Closure evidence."""

from __future__ import annotations

import json
from typing import Any, Mapping


def serialize_canonical_json_v1(value: Mapping[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
