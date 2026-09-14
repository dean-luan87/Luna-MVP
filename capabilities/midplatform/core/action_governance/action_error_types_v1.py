"""Structured error namespace for Action Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass


ERROR_NAMESPACE = "action_governance.controlled_implementation.v1"


@dataclass(frozen=True)
class ActionGovernanceErrorV1:
    code: str
    message: str
    phase: str = "Phase-Luna-Action-Governance-Controlled-Implementation-v1-001"
    namespace: str = ERROR_NAMESPACE


ERROR_CODES_V1 = {
    "INVALID_OWNER",
    "INVALID_INPUT_REFS",
    "INVALID_ACTION_CANDIDATE",
    "PERMISSION_RECHECK_FAILED",
    "SAFETY_RECHECK_FAILED",
    "CONFIRMATION_INVALID",
    "PRECONDITION_NOT_SATISFIED",
    "DEPENDENCY_NOT_SATISFIED",
    "RUNTIME_BOUNDARY_VIOLATION",
    "TASK_CREATION_FORBIDDEN",
    "EXECUTOR_HANDOFF_INVALID",
}
