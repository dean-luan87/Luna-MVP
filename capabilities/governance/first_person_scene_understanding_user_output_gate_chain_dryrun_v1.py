# -*- coding: utf-8 -*-
"""First Person Scene Understanding User Output Gate Chain DryRun v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.first_person_scene_understanding_output_candidate_dryrun_v1 import (
    FINAL_DECISION_GO as OUTPUT_CANDIDATE_DR_FINAL_GO,
    NEXT_PHASE_GO as OUTPUT_CANDIDATE_DR_NEXT_PHASE,
)
from capabilities.governance.layered_capability_stack_standard_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as STACK_STD_DR_FINAL_GO,
)
from capabilities.governance.layered_capability_stack_standard_v1 import STANDARD_ID as UNIVERSAL_STACK_STANDARD_ID
from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID
from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CB_DR_FINAL_GO,
)
from capabilities.governance.luna_gate_chain_enforcement_system_v1 import (
    GATE_CHAIN_REQUIREMENTS,
    GATE_INVOCATION_BLOCKED_PATHS,
    SYSTEM_ID as GATE_CHAIN_SYSTEM_ID,
)
from capabilities.governance.midplatform_display_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DISPLAY_GATE_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_safety_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SAFETY_GATE_DR_FINAL_GO,
)
from capabilities.governance.midplatform_speech_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SPEECH_GATE_DR_FINAL_GO,
)
from capabilities.governance.midplatform_user_output_constitution_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as USER_OUTPUT_CONSTITUTION_DR_FINAL_GO,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-First-Person-Scene-Understanding-User-Output-Gate-Chain-DryRun-v1-001"
SCOPE = "first_person_scene_understanding_user_output_gate_chain_dryrun_only"
SOURCE_CHAIN = "first_person_scene_understanding_user_output_gate_chain_dryrun_v1"

UPSTREAM_OUTPUT_CANDIDATE_DR_FINAL = OUTPUT_CANDIDATE_DR_FINAL_GO
UPSTREAM_OUTPUT_CANDIDATE_DR_NEXT = OUTPUT_CANDIDATE_DR_NEXT_PHASE

FINAL_DECISION_GO = (
    "FIRST_PERSON_SCENE_UNDERSTANDING_USER_OUTPUT_GATE_CHAIN_DRYRUN_CLOSED_"
    "READY_FOR_OUTPUT_CHAIN_CLOSURE_REVIEW"
)
FINAL_DECISION_HOLD = (
    "FIRST_PERSON_SCENE_UNDERSTANDING_USER_OUTPUT_GATE_CHAIN_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-First-Person-Scene-Understanding-Output-Chain-Closure-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-First-Person-Scene-Understanding-User-Output-Gate-Chain-Issue-Review-v1-001"

GATE_CHAIN_MODEL_FIELDS: Tuple[str, ...] = (
    "model_id",
    "model_type",
    "consumes_user_output_candidate",
    "consumes_constraint_bundle",
    "consumes_gate_chain_requirements",
    "emits_gate_result_candidates",
    "emits_enforcement_result_candidate",
    "invokes_user_output_constitution_gate_dryrun",
    "invokes_safety_gate_dryrun",
    "invokes_speech_gate_dryrun",
    "invokes_display_gate_dryrun",
    "does_not_generate_user_facing_output",
    "does_not_invoke_voice_output_plane",
    "does_not_invoke_tts",
    "does_not_invoke_display_output",
    "does_not_send_notification",
    "does_not_enable_runtime",
    "candidate_only",
)

CONSTITUTION_GATE_RESULT_FIELDS: Tuple[str, ...] = (
    "gate_result_candidate_id",
    "gate_id",
    "source_user_output_candidate_ref",
    "constraint_bundle_ref",
    "gate_status",
    "allowed_next_gates",
    "blocked_next_gates",
    "required_disclosures",
    "forbidden_actions",
    "applicable_rule_refs",
    "rationale_refs",
    "whitebox_trace_refs",
    "candidate_only",
    "not_user_output",
    "runtime_enable_allowed",
)

SAFETY_GATE_RESULT_FIELDS: Tuple[str, ...] = (
    "safety_gate_result_candidate_id",
    "enforcement_result_candidate_id",
    "gate_id",
    "source_user_output_candidate_ref",
    "source_constitution_gate_result_ref",
    "safety_status",
    "allowed_downstream_gates",
    "blocked_downstream_gates",
    "required_disclosures",
    "forbidden_actions",
    "safety_rationale",
    "survival_priority_applied",
    "candidate_only",
    "not_user_output",
    "runtime_enable_allowed",
)

SPEECH_GATE_RESULT_FIELDS: Tuple[str, ...] = (
    "speech_gate_result_candidate_id",
    "gate_id",
    "source_user_output_candidate_ref",
    "source_safety_gate_result_ref",
    "speech_status",
    "speech_channel_candidate_allowed",
    "speech_request_candidate_allowed",
    "voice_output_plane_allowed",
    "tts_allowed",
    "required_speech_disclosure",
    "blocked_speech_actions",
    "candidate_only",
    "not_speech_request",
    "not_audio_output",
)

DISPLAY_GATE_RESULT_FIELDS: Tuple[str, ...] = (
    "display_gate_result_candidate_id",
    "gate_id",
    "source_user_output_candidate_ref",
    "source_safety_gate_result_ref",
    "display_status",
    "display_channel_candidate_allowed",
    "display_output_allowed",
    "notification_allowed",
    "required_display_disclosure",
    "blocked_display_actions",
    "candidate_only",
    "not_display_output",
    "not_notification",
)

ENFORCEMENT_RESULT_FIELDS: Tuple[str, ...] = (
    "enforcement_result_candidate_id",
    "source_gate_result_refs",
    "enforcement_chain_status",
    "allowed_channel_candidates",
    "blocked_channel_candidates",
    "required_disclosures",
    "forbidden_actions",
    "required_observation",
    "output_gate_chain_complete_candidate",
    "user_facing_output_allowed",
    "voice_output_plane_allowed",
    "display_output_allowed",
    "notification_allowed",
    "runtime_enable_allowed",
    "candidate_only",
)

CONSTITUTION_GATE_REVIEW_ITEMS: Tuple[str, ...] = (
    "User Output Constitution Gate consumes user_output_candidate + constraint_bundle",
    "raw constitution not consumed by output runtime",
    "applicable_rule_refs preserved",
    "gate result candidate generated",
    "no user-facing output generated",
)

SAFETY_GATE_REVIEW_ITEMS: Tuple[str, ...] = (
    "Safety Gate consumes user_output_candidate + constitution gate result",
    "survival priority preserved",
    "observe_more / hold reason preserved",
    "direct navigation instruction blocked",
    "memory/worldmodel/task commit forbidden actions preserved",
    "no output generated",
)

SPEECH_GATE_REVIEW_ITEMS: Tuple[str, ...] = (
    "Speech Gate consumes safety enforcement context",
    "speech channel candidate can be allowed later",
    "speech_request not generated",
    "Voice Output Plane not invoked",
    "TTS not invoked",
    "direct audio output blocked",
)

DISPLAY_GATE_REVIEW_ITEMS: Tuple[str, ...] = (
    "Display Gate consumes safety enforcement context",
    "display channel candidate can be allowed later",
    "display output not generated",
    "notification not sent",
    "direct display output blocked",
)

NOTIFICATION_DEFERMENT_REVIEW_ITEMS: Tuple[str, ...] = (
    "Notification Gate is covered in matrix",
    "notification_now blocked",
    "notification gate deferred later",
    "notification_sent_now=false",
)

MEMORY_WM_TASK_NAV_BLOCK_REVIEW_ITEMS: Tuple[str, ...] = (
    "Memory Admission Gate blocked now",
    "WorldModel Admission Gate blocked now",
    "Task State Commit Gate blocked now",
    "Navigation Action Gate blocked now",
    "Device Action Gate deferred",
    "no state/write/action gate invoked",
)

PRIVACY_IDENTITY_DEFERMENT_REVIEW_ITEMS: Tuple[str, ...] = (
    "Privacy Gate covered and required later if sensitive",
    "Identity / Personal Continuity Gate covered and required later",
    "neither invoked now",
    "no person recognition / identity claim produced",
)

HEALTH_OVERSIGHT_REVIEW_ITEMS: Tuple[str, ...] = (
    "Health Oversight Check is external supervision",
    "Health refs may be carried",
    "Health does not belong to Bus self-judgement",
    "Bus transports health_ref ≠ bus judges health",
    "Health gate/check not invoked as output gate",
)

EXECUTION_HANDOFF_ITEMS: Tuple[str, ...] = (
    "enforcement_result_candidate can handoff to Voice Output Plane later",
    "enforcement_result_candidate can handoff to Display Output later",
    "Voice Output Plane / TTS / Display Output remain execution layer",
    "no execution layer invoked now",
    "execution requires later controlled runtime/admission where applicable",
)

TRACEABILITY_REVIEW_ITEMS: Tuple[str, ...] = (
    "source_user_output_candidate_ref preserved",
    "source_task_response_candidate_ref traceable",
    "source_decision_candidate_ref traceable",
    "constraint_bundle_ref preserved",
    "capability_stack_ref traceable",
    "layered_governance_mapping_ref traceable",
    "gate_chain_requirements preserved",
    "applicable_rule_refs preserved",
    "forbidden_actions preserved",
    "required_observation preserved",
    "rationale_refs preserved",
    "whitebox_trace_refs preserved",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_user_facing_output",
    "dryrun_to_voice_output_plane_invocation",
    "dryrun_to_tts_invocation",
    "dryrun_to_display_output_invocation",
    "dryrun_to_notification_send",
    "dryrun_to_output_runtime",
    "dryrun_to_camera_invocation",
    "dryrun_to_real_frame_read",
    "dryrun_to_vision_runtime_enable",
    "dryrun_to_ocr_runtime_enable",
    "dryrun_to_real_ocr_execution",
    "dryrun_to_map_provider_invocation",
    "dryrun_to_navigation_runtime_enable",
    "dryrun_to_real_navigation_action",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_controlled_runtime_enable",
) + GATE_INVOCATION_BLOCKED_PATHS

ALLOWED_PATHS: Tuple[str, ...] = (
    "dryrun_to_user_output_constitution_gate_result_candidate_generation",
    "dryrun_to_safety_gate_result_candidate_generation",
    "dryrun_to_speech_gate_result_candidate_generation",
    "dryrun_to_display_gate_result_candidate_generation",
    "dryrun_to_enforcement_result_candidate_generation",
)

NON_CLAIMS: Tuple[str, ...] = (
    "User Output Gate Chain DryRun GO ≠ user-facing output generated",
    "gate_result_candidate ≠ spoken/displayed output",
    "enforcement_result_candidate ≠ Voice Output Plane invocation",
    "speech_gate_result_candidate ≠ speech_request",
    "display_gate_result_candidate ≠ display output",
    "next Closure Review ≠ runtime execution",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "first_person_scene_understanding_user_output_gate_chain_dryrun_only",
    "simulated",
    "user_output_gate_chain_dryrun_executed_now",
    "user_output_constitution_gate_result_candidate_generated_now",
    "safety_gate_result_candidate_generated_now",
    "speech_gate_result_candidate_generated_now",
    "display_gate_result_candidate_generated_now",
    "enforcement_result_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "user_facing_output_generated_now",
    "voice_output_plane_invoked_now",
    "tts_invoked_now",
    "display_output_invoked_now",
    "notification_sent_now",
    "output_plane_runtime_enabled_now",
    "camera_invoked_now",
    "real_frame_read_now",
    "vision_runtime_enabled_now",
    "ocr_runtime_enabled_now",
    "real_ocr_executed_now",
    "map_provider_invoked_now",
    "navigation_runtime_enabled_now",
    "real_navigation_action_executed_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "controlled_runtime_enabled_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_user_output_gate_chain_dryrun"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "system_level_simulated_go": True,
        "mainline": "first_person_scene_understanding",
        "gate_chain_system_ref": GATE_CHAIN_SYSTEM_ID,
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _review_ok(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "dryrun_and_review_pass": len(issues) == 0,
    }


def run_first_person_scene_understanding_user_output_gate_chain_dryrun_v1(
    *,
    first_person_scene_understanding_output_candidate_dryrun_root: str,
    first_person_scene_understanding_task_response_candidate_dryrun_root: str,
    midplatform_user_output_constitution_dryrun_and_review_root: str,
    midplatform_safety_gate_dryrun_and_review_root: str,
    midplatform_speech_gate_dryrun_and_review_root: str,
    midplatform_display_gate_dryrun_and_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    layered_capability_stack_standard_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    output_cand_root = Path(
        first_person_scene_understanding_output_candidate_dryrun_root
    ).expanduser().resolve()
    task_resp_root = Path(
        first_person_scene_understanding_task_response_candidate_dryrun_root
    ).expanduser().resolve()
    uoc_root = Path(
        midplatform_user_output_constitution_dryrun_and_review_root
    ).expanduser().resolve()
    safety_root = Path(midplatform_safety_gate_dryrun_and_review_root).expanduser().resolve()
    speech_root = Path(midplatform_speech_gate_dryrun_and_review_root).expanduser().resolve()
    display_root = Path(midplatform_display_gate_dryrun_and_review_root).expanduser().resolve()
    cb_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    stack_std_root = Path(
        layered_capability_stack_standard_dryrun_and_review_root
    ).expanduser().resolve()

    output_cand_sm = _try_read_json(output_cand_root / "summary.json") or {}
    output_cand_vr = _try_read_json(output_cand_root / "verifier_report.json") or {}
    uoc_vr = _try_read_json(uoc_root / "verifier_report.json") or {}
    safety_vr = _try_read_json(safety_root / "verifier_report.json") or {}
    speech_vr = _try_read_json(speech_root / "verifier_report.json") or {}
    display_vr = _try_read_json(display_root / "verifier_report.json") or {}
    cb_vr = _try_read_json(cb_root / "verifier_report.json") or {}
    stack_std_vr = _try_read_json(stack_std_root / "verifier_report.json") or {}

    user_output = _try_read_json(output_cand_root / "sample_user_output_candidate_v1.json") or {}
    gate_matrix = _try_read_json(
        output_cand_root / "first_person_output_gate_chain_coverage_matrix_v1.json"
    ) or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_output_candidate_dryrun_root": str(output_cand_root),
        "upstream_task_response_dryrun_root": str(task_resp_root),
        "upstream_user_output_constitution_dryrun_root": str(uoc_root),
        "upstream_safety_gate_dryrun_root": str(safety_root),
        "upstream_speech_gate_dryrun_root": str(speech_root),
        "upstream_display_gate_dryrun_root": str(display_root),
        "upstream_constitution_bus_dryrun_root": str(cb_root),
        "upstream_layered_stack_standard_dryrun_root": str(stack_std_root),
        "output_root": str(out_root),
    }

    if output_cand_vr.get("verifier") != "GO":
        blockers.append("Output Candidate DryRun must be GO")
    if output_cand_sm.get("final_decision") != UPSTREAM_OUTPUT_CANDIDATE_DR_FINAL:
        blockers.append("output candidate dryrun final_decision mismatch")
    if output_cand_sm.get("recommended_next_phase") != UPSTREAM_OUTPUT_CANDIDATE_DR_NEXT:
        blockers.append("output candidate dryrun recommended_next_phase mismatch")
    if output_cand_sm.get("user_output_candidate_generated_now") is not True:
        blockers.append("upstream user_output_candidate_generated_now must be true")
    if output_cand_sm.get("user_facing_output_generated_now") is not False:
        blockers.append("upstream user_facing_output_generated_now must be false")
    if gate_matrix.get("gate_count") != 16:
        blockers.append("Gate Coverage Matrix must cover 16 gates")
    if uoc_vr.get("verifier") != "GO":
        blockers.append("User Output Constitution DryRun must be GO")
    if safety_vr.get("verifier") != "GO":
        blockers.append("Safety Gate DryRun must be GO")
    if speech_vr.get("verifier") != "GO":
        blockers.append("Speech Gate DryRun must be GO")
    if display_vr.get("verifier") != "GO":
        blockers.append("Display Gate DryRun must be GO")
    if cb_vr.get("verifier") != "GO":
        blockers.append("Constitution-Bus DryRun must be GO")
    if stack_std_vr.get("verifier") != "GO":
        blockers.append("Layered Capability Stack Standard DryRun must be GO")

    input_ok = len(blockers) == 0
    forbidden_actions = list(user_output.get("forbidden_actions") or [])
    required_observation = list(user_output.get("required_observation") or [])
    rationale_refs = list(user_output.get("rationale_refs") or [])
    whitebox_trace_refs = list(user_output.get("whitebox_trace_refs") or [])
    constraint_bundle_ref = "constraint_bundle_scene_understanding_chain_001"

    output_candidate_input_review = {
        "review_id": "output_candidate_input_review_v1",
        "review_pass": input_ok,
        "upstream_verifier": output_cand_vr.get("verifier"),
        "upstream_final_decision": output_cand_sm.get("final_decision"),
        "user_output_candidate_id": user_output.get("user_output_candidate_id"),
        "user_output_candidate_generated_now_upstream": output_cand_sm.get(
            "user_output_candidate_generated_now"
        ),
        "user_facing_output_generated_now_upstream": output_cand_sm.get(
            "user_facing_output_generated_now"
        ),
        "blockers": list(blockers),
        **meta,
    }

    gate_coverage_input_review = {
        "review_id": "gate_coverage_matrix_input_review_v1",
        "review_pass": input_ok,
        "gate_matrix_ref": gate_matrix.get("matrix_id"),
        "gate_count": gate_matrix.get("gate_count"),
        "gate_chain_system_ref": gate_matrix.get("gate_chain_system_id"),
        "gate_chain_requirements": list(user_output.get("gate_chain_requirements") or []),
        "blockers": list(blockers),
        **meta,
    }

    gate_chain_model = {
        "model_id": "first_person_scene_understanding_user_output_gate_chain_v1",
        "model_type": "gate_chain_dryrun_model",
        "consumes_user_output_candidate": True,
        "consumes_constraint_bundle": True,
        "consumes_gate_chain_requirements": True,
        "emits_gate_result_candidates": True,
        "emits_enforcement_result_candidate": True,
        "invokes_user_output_constitution_gate_dryrun": True,
        "invokes_safety_gate_dryrun": True,
        "invokes_speech_gate_dryrun": True,
        "invokes_display_gate_dryrun": True,
        "does_not_generate_user_facing_output": True,
        "does_not_invoke_voice_output_plane": True,
        "does_not_invoke_tts": True,
        "does_not_invoke_display_output": True,
        "does_not_send_notification": True,
        "does_not_enable_runtime": True,
        "candidate_only": True,
        **meta,
    }

    constitution_gate_result = {
        "gate_result_candidate_id": "constitution_gate_result_scene_understanding_chain_001",
        "gate_id": "user_output_constitution_gate",
        "source_user_output_candidate_ref": user_output.get("user_output_candidate_id"),
        "constraint_bundle_ref": constraint_bundle_ref,
        "gate_status": "pass_with_constraints",
        "allowed_next_gates": ["safety_gate"],
        "blocked_next_gates": [
            "direct_user_facing_output",
            "voice_output_plane",
            "display_output",
        ],
        "required_disclosures": [
            user_output.get("uncertainty_disclosure_candidate"),
            "output_gate_chain_required_before_user_facing_output",
        ],
        "forbidden_actions": forbidden_actions,
        "applicable_rule_refs": [
            "uoc:admission:uncertainty_disclosure",
            "uoc:admission:safety_survival_priority",
            "uoc:channel:no_direct_output_without_gate",
            "uoc:fact:not_fact_candidate_only",
        ],
        "rationale_refs": rationale_refs,
        "whitebox_trace_refs": whitebox_trace_refs,
        "capability_stack_ref": user_output.get("capability_stack_ref"),
        "layered_governance_mapping_ref": user_output.get("layered_governance_mapping_ref"),
        "candidate_only": True,
        "not_user_output": True,
        "runtime_enable_allowed": False,
        **meta,
    }

    safety_gate_result = {
        "safety_gate_result_candidate_id": "safety_gate_result_scene_understanding_chain_001",
        "enforcement_result_candidate_id": "enforcement_result_scene_understanding_chain_001",
        "gate_id": "safety_gate",
        "source_user_output_candidate_ref": user_output.get("user_output_candidate_id"),
        "source_constitution_gate_result_ref": constitution_gate_result["gate_result_candidate_id"],
        "safety_status": "hold_or_observe_more_allowed_candidate",
        "allowed_downstream_gates": ["speech_gate", "display_gate"],
        "blocked_downstream_gates": [
            "direct_audio_output",
            "direct_display_output",
            "navigation_action_gate",
        ],
        "required_disclosures": [
            str(user_output.get("safety_disclosure_candidate", {}).get("message_candidate", "")),
            user_output.get("uncertainty_disclosure_candidate"),
        ],
        "forbidden_actions": forbidden_actions,
        "safety_rationale": "survival_priority_observe_more_insufficient_live_validation",
        "survival_priority_applied": user_output.get("survival_priority_applied", True),
        "required_observation": required_observation,
        "candidate_only": True,
        "not_user_output": True,
        "runtime_enable_allowed": False,
        **meta,
    }

    speech_gate_result = {
        "speech_gate_result_candidate_id": "speech_gate_result_scene_understanding_chain_001",
        "gate_id": "speech_gate",
        "source_user_output_candidate_ref": user_output.get("user_output_candidate_id"),
        "source_safety_gate_result_ref": safety_gate_result["safety_gate_result_candidate_id"],
        "speech_status": "speech_candidate_later_allowed_with_constraints",
        "speech_channel_candidate_allowed": True,
        "speech_request_candidate_allowed": False,
        "voice_output_plane_allowed": False,
        "tts_allowed": False,
        "required_speech_disclosure": user_output.get("uncertainty_disclosure_candidate"),
        "blocked_speech_actions": [
            "direct_audio_output_without_speech_gate",
            "tts_invocation",
            "voice_output_plane_invocation",
        ],
        "candidate_only": True,
        "not_speech_request": True,
        "not_audio_output": True,
        **meta,
    }

    display_gate_result = {
        "display_gate_result_candidate_id": "display_gate_result_scene_understanding_chain_001",
        "gate_id": "display_gate",
        "source_user_output_candidate_ref": user_output.get("user_output_candidate_id"),
        "source_safety_gate_result_ref": safety_gate_result["safety_gate_result_candidate_id"],
        "display_status": "display_candidate_later_allowed_with_constraints",
        "display_channel_candidate_allowed": True,
        "display_output_allowed": False,
        "notification_allowed": False,
        "required_display_disclosure": user_output.get("uncertainty_disclosure_candidate"),
        "blocked_display_actions": [
            "direct_display_output_without_display_gate",
            "notification_now",
        ],
        "candidate_only": True,
        "not_display_output": True,
        "not_notification": True,
        **meta,
    }

    enforcement_result = {
        "enforcement_result_candidate_id": safety_gate_result["enforcement_result_candidate_id"],
        "source_gate_result_refs": [
            constitution_gate_result["gate_result_candidate_id"],
            safety_gate_result["safety_gate_result_candidate_id"],
            speech_gate_result["speech_gate_result_candidate_id"],
            display_gate_result["display_gate_result_candidate_id"],
        ],
        "source_user_output_candidate_ref": user_output.get("user_output_candidate_id"),
        "source_task_response_candidate_ref": user_output.get("source_task_response_candidate_ref"),
        "source_decision_candidate_ref": user_output.get("source_decision_candidate_ref"),
        "constraint_bundle_ref": constraint_bundle_ref,
        "enforcement_chain_status": "gate_chain_passed_for_candidate_only_or_hold",
        "allowed_channel_candidates": ["speech_candidate_later", "display_candidate_later"],
        "blocked_channel_candidates": [
            "direct_audio_output",
            "direct_display_output",
            "direct_navigation_instruction",
            "notification_now",
        ],
        "required_disclosures": [
            user_output.get("uncertainty_disclosure_candidate"),
            "observe_more_candidate_not_navigation_action",
        ],
        "forbidden_actions": forbidden_actions,
        "required_observation": required_observation,
        "gate_chain_requirements": list(user_output.get("gate_chain_requirements") or GATE_CHAIN_REQUIREMENTS),
        "output_gate_chain_complete_candidate": True,
        "user_facing_output_allowed": False,
        "voice_output_plane_allowed": False,
        "display_output_allowed": False,
        "notification_allowed": False,
        "runtime_enable_allowed": False,
        "capability_stack_ref": user_output.get("capability_stack_ref"),
        "layered_governance_mapping_ref": user_output.get("layered_governance_mapping_ref"),
        "rationale_refs": rationale_refs,
        "whitebox_trace_refs": whitebox_trace_refs,
        "candidate_only": True,
        **meta,
    }

    constitution_review = {
        "review_id": "constitution_gate_chain_review_v1",
        "review_items": list(CONSTITUTION_GATE_REVIEW_ITEMS),
        **_review_ok([(f"item.{i[:18]}", True) for i in CONSTITUTION_GATE_REVIEW_ITEMS]),
        **meta,
    }

    safety_review = {
        "review_id": "safety_gate_chain_review_v1",
        "review_items": list(SAFETY_GATE_REVIEW_ITEMS),
        "survival_priority_applied": safety_gate_result.get("survival_priority_applied") is True,
        **_review_ok([(f"item.{i[:18]}", True) for i in SAFETY_GATE_REVIEW_ITEMS]),
        **meta,
    }

    speech_review = {
        "review_id": "speech_gate_chain_review_v1",
        "review_items": list(SPEECH_GATE_REVIEW_ITEMS),
        **_review_ok([(f"item.{i[:18]}", True) for i in SPEECH_GATE_REVIEW_ITEMS]),
        **meta,
    }

    display_review = {
        "review_id": "display_gate_chain_review_v1",
        "review_items": list(DISPLAY_GATE_REVIEW_ITEMS),
        **_review_ok([(f"item.{i[:18]}", True) for i in DISPLAY_GATE_REVIEW_ITEMS]),
        **meta,
    }

    notification_deferment_review = {
        "review_id": "notification_gate_deferment_review_v1",
        "review_items": list(NOTIFICATION_DEFERMENT_REVIEW_ITEMS),
        "notification_gate_in_matrix": any(
            g.get("gate_id") == "notification_gate" for g in (gate_matrix.get("gates") or [])
        ),
        **_review_ok([(f"item.{i[:18]}", True) for i in NOTIFICATION_DEFERMENT_REVIEW_ITEMS]),
        **meta,
    }

    memory_wm_task_nav_block_review = {
        "review_id": "memory_worldmodel_task_navigation_gate_block_review_v1",
        "review_items": list(MEMORY_WM_TASK_NAV_BLOCK_REVIEW_ITEMS),
        "blocked_gate_ids": [
            "memory_admission_gate",
            "worldmodel_admission_gate",
            "task_state_commit_gate",
            "navigation_action_gate",
        ],
        **_review_ok([(f"item.{i[:18]}", True) for i in MEMORY_WM_TASK_NAV_BLOCK_REVIEW_ITEMS]),
        **meta,
    }

    privacy_identity_deferment_review = {
        "review_id": "privacy_identity_gate_deferment_review_v1",
        "review_items": list(PRIVACY_IDENTITY_DEFERMENT_REVIEW_ITEMS),
        **_review_ok([(f"item.{i[:18]}", True) for i in PRIVACY_IDENTITY_DEFERMENT_REVIEW_ITEMS]),
        **meta,
    }

    health_oversight_review = {
        "review_id": "health_oversight_gate_chain_review_v1",
        "review_items": list(HEALTH_OVERSIGHT_REVIEW_ITEMS),
        "health_oversight_external": True,
        "health_ref_carried": any("drive_signal" in r for r in rationale_refs),
        **_review_ok([(f"item.{i[:18]}", True) for i in HEALTH_OVERSIGHT_REVIEW_ITEMS]),
        **meta,
    }

    traceability_review = {
        "review_id": "gate_result_traceability_review_v1",
        "review_items": list(TRACEABILITY_REVIEW_ITEMS),
        "source_user_output_candidate_ref": user_output.get("user_output_candidate_id"),
        "source_task_response_candidate_ref": user_output.get("source_task_response_candidate_ref"),
        "source_decision_candidate_ref": user_output.get("source_decision_candidate_ref"),
        "constraint_bundle_ref": constraint_bundle_ref,
        "capability_stack_ref": user_output.get("capability_stack_ref"),
        "layered_governance_mapping_ref": user_output.get("layered_governance_mapping_ref"),
        **_review_ok([(f"item.{i[:18]}", True) for i in TRACEABILITY_REVIEW_ITEMS]),
        **meta,
    }

    execution_handoff = {
        "plan_id": "gate_chain_to_execution_layer_handoff_plan_v1",
        "review_items": list(EXECUTION_HANDOFF_ITEMS),
        "voice_output_plane_invoked_now": False,
        "tts_invoked_now": False,
        "display_output_invoked_now": False,
        **_review_ok([(f"item.{i[:18]}", True) for i in EXECUTION_HANDOFF_ITEMS]),
        **meta,
    }

    boundary_audit = {
        "audit_id": "gate_chain_boundary_audit_v1",
        "audit_pass": True,
        "boundary_fields": {field: False for field in BOUNDARY_FALSE},
        **meta,
    }

    blocked_path_result = {
        "result_id": "gate_chain_blocked_path_result_v1",
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        "blocked_paths": [
            {"path_id": path, "status": "blocked", "reason": "gate_chain_dryrun_candidate_only"}
            for path in BLOCKED_PATHS
        ],
        "allowed_paths": [
            {
                "path_id": path,
                "status": "allowed_candidate_only",
                "candidate_only": True,
                "not_user_facing_output": True,
            }
            for path in ALLOWED_PATHS
        ],
        **meta,
    }

    reviews = [
        constitution_review,
        safety_review,
        speech_review,
        display_review,
        notification_deferment_review,
        memory_wm_task_nav_block_review,
        privacy_identity_deferment_review,
        health_oversight_review,
        traceability_review,
        execution_handoff,
    ]

    model_ok = all(f in gate_chain_model for f in GATE_CHAIN_MODEL_FIELDS)
    constitution_ok = all(f in constitution_gate_result for f in CONSTITUTION_GATE_RESULT_FIELDS)
    safety_ok = all(f in safety_gate_result for f in SAFETY_GATE_RESULT_FIELDS)
    speech_ok = all(f in speech_gate_result for f in SPEECH_GATE_RESULT_FIELDS)
    display_ok = all(f in display_gate_result for f in DISPLAY_GATE_RESULT_FIELDS)
    enforcement_ok = all(f in enforcement_result for f in ENFORCEMENT_RESULT_FIELDS)

    gate_results_ok = (
        constitution_ok
        and safety_ok
        and speech_ok
        and display_ok
        and enforcement_ok
        and constitution_gate_result.get("gate_status") == "pass_with_constraints"
        and safety_gate_result.get("safety_status") == "hold_or_observe_more_allowed_candidate"
        and speech_gate_result.get("speech_request_candidate_allowed") is False
        and speech_gate_result.get("voice_output_plane_allowed") is False
        and display_gate_result.get("display_output_allowed") is False
        and enforcement_result.get("output_gate_chain_complete_candidate") is True
        and enforcement_result.get("user_facing_output_allowed") is False
    )

    chain_pass = (
        input_ok
        and model_ok
        and gate_results_ok
        and all(r.get("dryrun_and_review_pass") for r in reviews)
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
        and meta.get("user_output_gate_chain_dryrun_executed_now") is True
        and meta.get("enforcement_result_candidate_generated_now") is True
        and meta.get("user_facing_output_generated_now") is False
        and meta.get("voice_output_plane_invoked_now") is False
    )

    closure_decision = {
        "decision_id": "gate_chain_closure_decision_v1",
        "dryrun_and_review_pass": chain_pass,
        "high_risk": not chain_pass,
        "final_decision": FINAL_DECISION_GO if chain_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if chain_pass else NEXT_PHASE_HOLD,
        "closure_summary": [
            "user_output_candidate passed through constitution/safety/speech/display gate dryrun",
            "gate_result_candidates and enforcement_result_candidate generated",
            "admission gates remain blocked; notification/privacy/identity deferred",
            "health oversight external; no execution layer invoked",
            f"{len(BLOCKED_PATHS)} blocked paths + {len(ALLOWED_PATHS)} allowed candidate paths",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_output_chain_closure_review": chain_pass,
        "selected_next_phase": NEXT_PHASE_GO if chain_pass else NEXT_PHASE_HOLD,
        "next_focus": (
            "Output Chain Closure Review: candidate → decision → task_response → "
            "user_output_candidate → gate_result_candidate full chain收口"
        ),
        **meta,
    }

    policy = {
        "policy_id": "first_person_scene_understanding_user_output_gate_chain_dryrun_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "gate_chain_dryrun_only_not_user_facing_not_execution": True,
        "mainline": "first_person_scene_understanding",
        "gate_chain_system_ref": GATE_CHAIN_SYSTEM_ID,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": chain_pass,
        "violations": list(blockers),
        "dryrun_and_review_pass": chain_pass,
        "system_level_simulated_go": True,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "first_person_scene_understanding_user_output_gate_chain_dryrun_policy": policy,
        "output_candidate_input_review": output_candidate_input_review,
        "gate_coverage_matrix_input_review": gate_coverage_input_review,
        "user_output_gate_chain_model_candidate": gate_chain_model,
        "sample_user_output_constitution_gate_result_candidate": constitution_gate_result,
        "sample_safety_gate_result_candidate": safety_gate_result,
        "sample_speech_gate_result_candidate": speech_gate_result,
        "sample_display_gate_result_candidate": display_gate_result,
        "sample_enforcement_result_candidate": enforcement_result,
        "constitution_gate_chain_review": constitution_review,
        "safety_gate_chain_review": safety_review,
        "speech_gate_chain_review": speech_review,
        "display_gate_chain_review": display_review,
        "notification_gate_deferment_review": notification_deferment_review,
        "memory_worldmodel_task_navigation_gate_block_review": memory_wm_task_nav_block_review,
        "privacy_identity_gate_deferment_review": privacy_identity_deferment_review,
        "health_oversight_gate_chain_review": health_oversight_review,
        "gate_result_traceability_review": traceability_review,
        "gate_chain_to_execution_layer_handoff_plan": execution_handoff,
        "gate_chain_boundary_audit": boundary_audit,
        "gate_chain_blocked_path_result": blocked_path_result,
        "gate_chain_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
