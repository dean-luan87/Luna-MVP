"""Case and binding contracts for the bounded real cognitive observation loop.

These are evaluation-layer references.  They do not replace the canonical
Provider Runtime or Cognitive State Formation contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class RealOCRObservationBindingV1:
    binding_ref: str
    source_ref: str
    information_refs: Tuple[str, ...]
    source_region_ref: str


@dataclass(frozen=True)
class RealCognitiveObservationCaseV1:
    case_id: str
    title: str
    goal_ref: str
    concern_ref: str
    information_need_ref: str
    required_information_refs: Tuple[str, ...]
    first_binding: RealOCRObservationBindingV1
    second_binding: RealOCRObservationBindingV1 | None = None
    role_refs: Tuple[str, ...] = ("role:observer",)
    task_ref: str = "task:observe-text-candidates"
    relation_refs: Tuple[str, ...] = ("relation:source-to-text-candidate",)
    field_refs: Tuple[str, ...] = ("field:real-ocr-observation-loop:v1",)


__all__ = [
    "RealOCRObservationBindingV1",
    "RealCognitiveObservationCaseV1",
]
