"""Structured errors for Causal Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass


ERROR_NAMESPACE = "causal_governance.controlled_implementation.v1"


@dataclass(frozen=True)
class CausalGovernanceErrorV1:
    code: str
    message: str
    phase: str = "Phase-Luna-Causal-Governance-Controlled-Implementation-v1-001"
    namespace: str = ERROR_NAMESPACE


ERROR_CODES_V1 = {
    "INVALID_OWNER",
    "INVALID_INPUT_REFS",
    "MISSING_EVIDENCE",
    "BOUNDARY_VIOLATION",
    "INVALID_STATE_TRANSITION",
    "INVALID_HANDOFF",
}
