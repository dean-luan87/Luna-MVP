"""Structured error namespace for Decision Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass


ERROR_NAMESPACE = "decision_governance.controlled_implementation.v1"


@dataclass(frozen=True)
class DecisionGovernanceErrorV1:
    code: str
    message: str
    phase: str = "Phase-Luna-Decision-Governance-Controlled-Implementation-v1-001"
    namespace: str = ERROR_NAMESPACE


ERROR_CODES_V1 = {
    "INVALID_OWNER",
    "INVALID_INPUT_REFS",
    "INVALID_OPTION",
    "PERMISSION_BYPASS_ATTEMPT",
    "SAFETY_BYPASS_ATTEMPT",
    "FABRICATED_CONFIRMATION",
    "INVALID_HANDOFF",
    "RUNTIME_BOUNDARY_VIOLATION",
}
