"""Local vocabulary and guards for the Loop semantic cutover seam."""

from __future__ import annotations

from typing import Dict, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_registry_v1 import (
    ROLE_A,
    ROLE_BRAIN,
    ROLE_LOOP,
)


PHASE = "Phase-Luna-Loop-Semantic-To-Mechanical-Cutover-Controlled-Implementation-v1-001"

RESUME_DISPOSITIONS: Tuple[str, ...] = ("KEEP", "REPLAN", "SUPERSEDE", "COMPLETE", "WAITING")
LOCAL_DISPOSITIONS: Tuple[str, ...] = ("SUFFICIENT", "INSUFFICIENT", "RECONSIDER", "DEFER")
CLOSURE_DISPOSITIONS: Tuple[str, ...] = (
    "COMPLETED",
    "STOPPED",
    "SUPERSEDED",
    "ABANDONED_BY_VALUE",
    "FAILED",
)
CLOSURE_SOURCE_OWNERS: Tuple[str, ...] = (ROLE_A, ROLE_BRAIN)

# This is an integration mapping.  SUPERSEDE_RECORDED_REF is represented by
# the already-existing canonical mechanical command SUPERSEDE_REQUIREMENT.
RESUME_TO_COMMANDS: Dict[str, Tuple[str, ...]] = {
    "KEEP": ("RESUME_KEEP",),
    "REPLAN": ("RECORD_STATE_VERSION", "RECORD_NEED_REF"),
    "SUPERSEDE": ("SUPERSEDE_REQUIREMENT",),
    "COMPLETE": ("CLOSE", "FREEZE_FINAL_STATE"),
    "WAITING": ("WAIT",),
}
LOCAL_TO_COMMANDS: Dict[str, Tuple[str, ...]] = {
    # RECORD_PENDING_CANDIDATE is the existing mechanical RECORD_REFS
    # representation; the semantic disposition remains supplied by A.
    "SUFFICIENT": ("RECORD_PENDING_CANDIDATE",),
    "INSUFFICIENT": ("RECORD_PENDING_CANDIDATE",),
    "RECONSIDER": ("RECORD_PENDING_CANDIDATE",),
    "DEFER": ("RECORD_PENDING_CANDIDATE",),
}
CLOSURE_TO_COMMANDS: Dict[str, Tuple[str, ...]] = {
    disposition: ("RECORD_OUTCOME_REF", "CLOSE", "FREEZE_FINAL_STATE", "ARCHIVE_HISTORY_BOUNDARY")
    for disposition in CLOSURE_DISPOSITIONS
}

REQUIRED_A_AUTHORITIES = {
    "RESUME": "REQUEST_RESUME",
    "LOCAL_DISPOSITION": "DECIDE_LOCAL_CONTINUATION",
    "CLOSURE": "REQUEST_CLOSURE",
}

NEGATIVE_GUARDS: Dict[str, bool] = {
    "candidate_only": True,
    "synthetic_only": True,
    "loop_resume_semantic_judgment": False,
    "loop_local_disposition_inference": False,
    "loop_closure_reason_inference": False,
    "loop_continuity_semantic_interpretation": False,
    "loop_need_selection": False,
    "loop_sufficiency_judgment": False,
    "loop_reconsideration_judgment": False,
    "loop_next_step_judgment": False,
    "loop_concern_authority": False,
    "legacy_loop_semantic_authority": False,
    "compatibility_source_only": True,
    "provider_invocation": False,
    "model_inference": False,
    "camera": False,
    "ocr": False,
    "action_execution": False,
    "learning": False,
    "memory_mutation": False,
    "experience_mutation": False,
    "scheduler": False,
    "loop_manager": False,
    "loop_planner": False,
}

__all__ = [
    "PHASE",
    "ROLE_A",
    "ROLE_BRAIN",
    "ROLE_LOOP",
    "RESUME_DISPOSITIONS",
    "LOCAL_DISPOSITIONS",
    "CLOSURE_DISPOSITIONS",
    "CLOSURE_SOURCE_OWNERS",
    "RESUME_TO_COMMANDS",
    "LOCAL_TO_COMMANDS",
    "CLOSURE_TO_COMMANDS",
    "REQUIRED_A_AUTHORITIES",
    "NEGATIVE_GUARDS",
]
