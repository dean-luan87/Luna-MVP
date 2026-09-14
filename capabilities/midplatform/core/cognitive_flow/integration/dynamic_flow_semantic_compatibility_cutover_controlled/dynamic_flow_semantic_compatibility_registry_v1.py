"""Static vocabulary and guard registry for the compatibility seam."""

from __future__ import annotations

PHASE = "Phase-Luna-Dynamic-Flow-Semantic-Compatibility-Cutover-Controlled-Implementation-v1-001"
SOURCE_OWNER = "COGNITIVE_FLOW_GOVERNANCE"
A_OWNER = "A_REASONING_ROLE"

SUPPORTED_FAMILIES = (
    "NEED",
    "SUFFICIENCY",
    "RECONSIDERATION",
    "NEXT_STEP",
    "CALLER_CUTOVER",
    "REAL_CAPABILITY_RESERVATION",
    "LEGACY_COMPATIBILITY",
    "NEGATIVE_GUARD",
)

RETIREMENT_READINESS = {
    "_select_next_need": "R3",
    "_reconsideration": "R3",
    "legacy_sufficiency_computation": "R2",
    "legacy_next_step_computation": "R2",
}


def negative_guards() -> dict[str, bool]:
    return {
        "candidate_only": True,
        "synthetic_only": True,
        "dynamic_flow_semantic_authority": False,
        "dynamic_flow_direct_semantic_consumption": False,
        "a_need_authority": True,
        "a_sufficiency_authority": True,
        "a_reconsideration_authority": True,
        "a_next_step_authority": True,
        "dynamic_flow_computation_retained": True,
        "dynamic_flow_helper_deleted": False,
        "dynamic_flow_engine_rewritten": False,
        "legacy_semantic_fields_removed": False,
        "loop_semantic_authority": False,
        "provider_invocation": False,
        "model_inference": False,
        "camera": False,
        "ocr": False,
        "action_execution": False,
        "second_real_provider_invocation": False,
        "learning": False,
        "memory_mutation": False,
        "experience_mutation": False,
        "scheduler": False,
        "brain_runtime": False,
    }


__all__ = ["A_OWNER", "PHASE", "RETIREMENT_READINESS", "SOURCE_OWNER", "SUPPORTED_FAMILIES", "negative_guards"]
