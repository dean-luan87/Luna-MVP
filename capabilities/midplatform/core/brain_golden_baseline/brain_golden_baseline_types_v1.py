"""Small, business-logic-free types for Golden Baseline metadata."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Tuple


BASELINE_ID = "luna-brain-real-evidence-cognitive-loop-golden-baseline"
BASELINE_VERSION = "B5-PLANNED-V1"
COMPATIBILITY_STATUSES = (
    "BACKWARD_COMPATIBLE",
    "REQUIRES_TARGETED_REGRESSION",
    "REQUIRES_FULL_REGRESSION",
    "BREAKING_CHANGE",
    "BLOCKED_CHANGE",
)


@dataclass(frozen=True)
class BaselineIssue:
    code: str
    detail: str
    severity: str = "ERROR"


@dataclass(frozen=True)
class ChangeImpact:
    change_domain: str
    required_regressions: Tuple[str, ...]
    review_level: str
    execution_requested: bool = False


@dataclass(frozen=True)
class CompatibilityDecision:
    classification: str
    reason: str
    regression_required: Tuple[str, ...]


@dataclass(frozen=True)
class BaselineSnapshot:
    manifest: Mapping[str, Any]
    inventory: Mapping[str, Any]
    owner_matrix: Mapping[str, Any]
    regression_index: Mapping[str, Any]
    change_impact: Mapping[str, Any]
    compatibility: Mapping[str, Any]
    guards: Mapping[str, Any]
    trace: Mapping[str, Any]
    candidate_truth: Mapping[str, Any]
    feedback: Mapping[str, Any]
    real_synthetic: Mapping[str, Any]
    deferred: Mapping[str, Any]
