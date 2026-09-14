"""Evaluation-only contracts for same-evidence cognitive conditioning."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class ConditioningSideSpecV1:
    side_id: str
    role_ref: str
    task_ref: str
    goal_ref: str
    concern_ref: str
    information_need_ref: str
    required_information_refs: Tuple[str, ...]
    available_information_refs: Tuple[str, ...]
    observed_information_refs: Tuple[str, ...]


@dataclass(frozen=True)
class ConditioningContrastSpecV1:
    contrast_id: str
    category: str
    title: str
    source_path: Path
    left: ConditioningSideSpecV1
    right: ConditioningSideSpecV1
    field_refs: Tuple[str, ...]
    relation_refs: Tuple[str, ...]


__all__ = ["ConditioningSideSpecV1", "ConditioningContrastSpecV1"]
