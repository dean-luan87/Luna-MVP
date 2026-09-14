"""Static registry for the A-owned semantic migration seam."""

from __future__ import annotations

from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_registry_v1 import (
    A_AUTHORITIES,
    LOOP_COMMAND_CAPABILITY,
    MECHANICAL_COMMANDS,
    ROLE_A,
)


PHASE = "Phase-Luna-A-Owned-Semantic-Decision-To-Loop-Mechanical-Bridge-Controlled-Implementation-v1-001"
COMPATIBILITY_SOURCE_OWNER = "Cognitive Flow Governance"
DECISION_OWNER = ROLE_A

REQUIRED_AUTHORITIES = {
    "NEED": "SELECT_CURRENT_NEED",
    "SUFFICIENCY": "JUDGE_LOCAL_SUFFICIENCY",
    "RECONSIDERATION": "JUDGE_RECONSIDERATION",
    "NEXT_STEP": "DECIDE_LOCAL_CONTINUATION",
}

SUFFICIENCY_STATUSES = (
    "SUFFICIENT",
    "INSUFFICIENT",
    "REQUIRES_RECONSIDERATION",
)

NEXT_STEP_DISPOSITIONS = (
    "CONTINUE",
    "REQUEST_MORE_EVIDENCE",
    "REPLAN",
    "STOP_SUFFICIENT",
    "DEFER",
    "WAIT",
    "PAUSE",
)

FAILURE_CLASSES = (
    "AUTHORITY_NOT_GRANTED",
    "CAPABILITY_BOUNDARY_VIOLATION",
    "SCOPE_MISMATCH",
    "STALE_STATE_VERSION",
    "GRANT_REVOKED",
    "GRANT_EXPIRED",
    "RESPONSIBILITY_BINDING_INVALID",
    "INVALID_DECISION_VALUE",
)

__all__ = [
    "A_AUTHORITIES",
    "COMPATIBILITY_SOURCE_OWNER",
    "DECISION_OWNER",
    "FAILURE_CLASSES",
    "LOOP_COMMAND_CAPABILITY",
    "MECHANICAL_COMMANDS",
    "NEXT_STEP_DISPOSITIONS",
    "PHASE",
    "REQUIRED_AUTHORITIES",
    "SUFFICIENCY_STATUSES",
]
