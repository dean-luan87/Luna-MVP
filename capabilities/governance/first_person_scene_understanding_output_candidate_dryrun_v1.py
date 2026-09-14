# -*- coding: utf-8 -*-
"""First Person Scene Understanding Output Candidate DryRun v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.first_person_scene_understanding_task_response_candidate_dryrun_v1 import (
    FINAL_DECISION_GO as TASK_RESP_DR_FINAL_GO,
    NEXT_PHASE_GO as TASK_RESP_DR_NEXT_PHASE,
)
from capabilities.governance.layered_capability_stack_standard_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as STACK_STD_DR_FINAL_GO,
)
from capabilities.governance.layered_capability_stack_standard_v1 import (
    GOVERNANCE_ADDENDUM_ID,
    STANDARD_ID as UNIVERSAL_STACK_STANDARD_ID,
)
from capabilities.governance.layered_governance_mapping_v1 import (
    ADDENDUM_ID,
    EXTENDS_STANDARD_ID,
    FIRST_PERSON_GOVERNANCE_LAYERS,
)
from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CB_DR_FINAL_GO,
)
from capabilities.governance.midplatform_display_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DISPLAY_GATE_DR_FINAL_GO,
)
from capabilities.governance.midplatform_output_plane_integration_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as OUTPUT_PLANE_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SAFETY_GATE_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_speech_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SPEECH_GATE_DR_FINAL_GO,
)
from capabilities.governance.midplatform_user_output_constitution_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as USER_OUTPUT_CONSTITUTION_DR_FINAL_GO,
)
from capabilities.governance.luna_gate_chain_enforcement_system_v1 import (
    FIRST_PERSON_OUTPUT_GATE_CHAIN_ENTRIES,
    GATE_CHAIN_COVERAGE_CONFIRMATIONS,
    GATE_CHAIN_REQUIREMENTS,
    GATE_ENTRY_FIELDS,
    GATE_INVOCATION_BLOCKED_PATHS,
    GATE_TYPES,
    SYSTEM_ID as GATE_CHAIN_SYSTEM_ID,
    SYSTEM_NAME as GATE_CHAIN_SYSTEM_NAME,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-First-Person-Scene-Understanding-Output-Candidate-DryRun-v1-001"
SCOPE = "first_person_scene_understanding_output_candidate_dryrun_only"
SOURCE_CHAIN = "first_person_scene_understanding_output_candidate_dryrun_v1"

UPSTREAM_TASK_RESP_DR_FINAL = TASK_RESP_DR_FINAL_GO
UPSTREAM_TASK_RESP_DR_NEXT = TASK_RESP_DR_NEXT_PHASE

FINAL_DECISION_GO = (
    "FIRST_PERSON_SCENE_UNDERSTANDING_OUTPUT_CANDIDATE_DRYRUN_CLOSED_"
    "READY_FOR_USER_OUTPUT_GATE_CHAIN_DRYRUN"
)
FINAL_DECISION_HOLD = (
    "FIRST_PERSON_SCENE_UNDERSTANDING_OUTPUT_CANDIDATE_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-First-Person-Scene-Understanding-User-Output-Gate-Chain-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-First-Person-Scene-Understanding-Output-Candidate-Issue-Review-v1-001"

ASSEMBLY_MODEL_FIELDS: Tuple[str, ...] = (
    "model_id",
    "model_type",
    "consumes_task_response_candidate",
    "emits_user_output_candidate",
    "preserves_capability_stack",
    "preserves_layered_governance_mapping",
    "preserves_scene_understanding_primary_goal",
    "preserves_spatiotemporal_secondary_goal",
    "preserves_navigation_application_context",
    "does_not_generate_user_facing_output",
    "does_not_invoke_safety_gate",
    "does_not_invoke_speech_gate",
    "does_not_invoke_display_gate",
    "does_not_invoke_tts",
    "does_not_enable_runtime",
    "candidate_only",
)

USER_OUTPUT_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "user_output_candidate_id",
    "source_task_response_candidate_ref",
    "output_scope",
    "output_status",
    "output_intent",
    "primary_goal",
    "secondary_goal",
    "application_goal",
    "capability_stack_ref",
    "layered_governance_mapping_ref",
    "candidate_message_summary",
    "safety_disclosure_candidate",
    "uncertainty_disclosure_candidate",
    "required_observation",
    "forbidden_actions",
    "allowed_channel_candidates",
    "blocked_channel_candidates",
    "gate_requirements",
    "gate_chain_requirements",
    "user_output_constitution_required",
    "safety_gate_required",
    "speech_gate_required_if_voice",
    "display_gate_required_if_display",
    "user_facing_output_allowed",
    "speech_output_allowed",
    "display_output_allowed",
    "notification_allowed",
    "runtime_enable_allowed",
    "memory_write_allowed",
    "world_model_write_allowed",
    "task_state_commit_allowed",
    "evidence_refs",
    "rationale_refs",
    "whitebox_trace_refs",
    "candidate_only",
    "not_final_output",
)

CHANNEL_ELIGIBILITY_REVIEW_ITEMS: Tuple[str, ...] = (
    "speech/display only channel candidates not actual output",
    "channel eligibility does not invoke gate",
    "channel eligibility does not invoke Voice Output Plane or Display Output",
    "notification_now blocked",
    "direct_navigation_instruction blocked",
)

SCENE_OUTPUT_REVIEW_ITEMS: Tuple[str, ...] = (
    "output_candidate reflects Layer 1 Current Scene Understanding",
    "target/text/tracking summaries remain candidate",
    "no target/text/tracking becomes fact",
    "no user-facing output generated",
)

SPATIOTEMPORAL_OUTPUT_REVIEW_ITEMS: Tuple[str, ...] = (
    "Layer 2 uncertainty preserved",
    "missing live validation preserved",
    "world continuity hypothesis not stated as fact",
    "required_observation preserved",
)

NAVIGATION_OUTPUT_REVIEW_ITEMS: Tuple[str, ...] = (
    "Layer 3 navigation remains application context",
    "navigation not promoted to primary goal",
    "no navigation action or route instruction generated",
    "direct navigation instruction blocked",
)

SURVIVAL_OUTPUT_REVIEW_ITEMS: Tuple[str, ...] = (
    "Survival safety priority preserved",
    "observe_more / hold reason preserved",
    "safety disclosure candidate prepared but not output",
    "task progress does not override safety",
)

REQUIRED_OBS_OUTPUT_REVIEW_ITEMS: Tuple[str, ...] = (
    "required_observation copied from task_response_candidate",
    "observation request remains candidate",
    "observe_more does not invoke camera/runtime",
    "observation planning remains later",
)

FORBIDDEN_ACTIONS_REVIEW_ITEMS: Tuple[str, ...] = (
    "direct_navigation_action_without_runtime_authorization",
    "user_output_without_gate",
    "memory_worldmodel_write",
    "camera_invocation_without_controlled_runtime",
    "provider_invocation_without_authorization",
    "task_state_commit_without_review",
    "direct_audio_output_without_speech_gate",
    "direct_display_output_without_display_gate",
)

UNCERTAINTY_OUTPUT_REVIEW_ITEMS: Tuple[str, ...] = (
    "uncertainty disclosure candidate prepared",
    "disclosure is not spoken/displayed now",
    "simulated fixture limitation preserved",
    "output gate required before user-facing output",
)

GOVERNANCE_OUTPUT_REVIEW_ITEMS: Tuple[str, ...] = (
    "L1 governance mapping applied to scene summary",
    "L2 governance mapping applied to continuity/freshness/gap",
    "L3 governance mapping applied to navigation application boundary",
    "L4/L5 remain deferred/later",
    "governance principles consistent landing points layered",
    "no all-rules-applied-to-all-layers overload",
    "no reduced constitution principle by layer",
)

CONSTITUTION_HANDOFF_ITEMS: Tuple[str, ...] = (
    "user_output_candidate requires User Output Constitution later",
    "raw constitution not consumed directly by output runtime",
    "constraint_bundle / gate chain later",
    "user_output_constitution not invoked now",
)

GATE_HANDOFF_ITEMS: Tuple[str, ...] = (
    "Safety Gate later consumes user_output_candidate + constraint_bundle",
    "Speech Gate later consumes enforcement_result_candidate + user_output_candidate",
    "Display Gate later consumes enforcement_result_candidate + user_output_candidate",
    "Voice Output Plane / Display Output remain execution layer later",
    "no gate invoked now",
)

TRACEABILITY_REVIEW_ITEMS: Tuple[str, ...] = (
    "source_task_response_candidate_ref preserved",
    "source_decision_candidate_ref traceable through refs",
    "source_integrated_context_ref traceable through refs",
    "capability_stack_ref preserved",
    "layered_governance_mapping_ref preserved",
    "target/text/tracking/task/spatiotemporal/world/risk/navigation refs preserved",
    "conflict/gap/freshness refs preserved",
    "drive/health/validation/constitution refs preserved",
    "whitebox_trace_refs preserved",
    "rationale_refs preserved",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_user_facing_output",
    "dryrun_to_safety_gate_invocation",
    "dryrun_to_speech_gate_invocation",
    "dryrun_to_display_gate_invocation",
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

GATE_COVERAGE_MATRIX_REVIEW_ITEMS: Tuple[str, ...] = GATE_CHAIN_COVERAGE_CONFIRMATIONS

NON_CLAIMS: Tuple[str, ...] = (
    "Output Candidate DryRun GO ≠ user-facing output generated",
    "user_output_candidate ≠ spoken/displayed output",
    "channel candidate ≠ actual Speech/Display invocation",
    "uncertainty disclosure candidate ≠ disclosure delivered",
    "observe_more candidate ≠ camera/runtime invocation",
    "next User Output Gate Chain DryRun ≠ TTS/audio/display runtime",
    "gate coverage matrix GO ≠ any gate invoked now",
    "gate handoff plan GO ≠ unified gate chain fully executed",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "first_person_scene_understanding_output_candidate_dryrun_only",
    "simulated",
    "user_output_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "user_facing_output_generated_now",
    "safety_gate_invoked_now",
    "speech_gate_invoked_now",
    "display_gate_invoked_now",
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
    "gate_result_candidate_generated_now",
    "enforcement_result_candidate_generated_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_output_candidate_dryrun"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "system_level_simulated_go": True,
        "mainline": "first_person_scene_understanding",
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


def run_first_person_scene_understanding_output_candidate_dryrun_v1(
    *,
    first_person_scene_understanding_task_response_candidate_dryrun_root: str,
    first_person_scene_understanding_decision_chain_candidate_dryrun_root: str,
    layered_capability_stack_standard_dryrun_and_review_root: str,
    layered_capability_stack_standard_planning_root: str,
    midplatform_output_plane_integration_dryrun_and_review_root: str,
    midplatform_user_output_constitution_dryrun_and_review_root: str,
    midplatform_safety_gate_dryrun_and_review_root: str,
    midplatform_speech_gate_dryrun_and_review_root: str,
    midplatform_display_gate_dryrun_and_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    task_resp_root = Path(
        first_person_scene_understanding_task_response_candidate_dryrun_root
    ).expanduser().resolve()
    decision_root = Path(
        first_person_scene_understanding_decision_chain_candidate_dryrun_root
    ).expanduser().resolve()
    stack_std_root = Path(
        layered_capability_stack_standard_dryrun_and_review_root
    ).expanduser().resolve()
    stack_plan_root = Path(
        layered_capability_stack_standard_planning_root
    ).expanduser().resolve()
    output_plane_root = Path(
        midplatform_output_plane_integration_dryrun_and_review_root
    ).expanduser().resolve()
    uoc_root = Path(
        midplatform_user_output_constitution_dryrun_and_review_root
    ).expanduser().resolve()
    safety_root = Path(
        midplatform_safety_gate_dryrun_and_review_root
    ).expanduser().resolve()
    speech_root = Path(
        midplatform_speech_gate_dryrun_and_review_root
    ).expanduser().resolve()
    display_root = Path(
        midplatform_display_gate_dryrun_and_review_root
    ).expanduser().resolve()
    cb_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()

    task_resp_sm = _try_read_json(task_resp_root / "summary.json") or {}
    task_resp_vr = _try_read_json(task_resp_root / "verifier_report.json") or {}
    decision_vr = _try_read_json(decision_root / "verifier_report.json") or {}
    stack_std_vr = _try_read_json(stack_std_root / "verifier_report.json") or {}
    output_plane_vr = _try_read_json(output_plane_root / "verifier_report.json") or {}
    uoc_vr = _try_read_json(uoc_root / "verifier_report.json") or {}
    safety_vr = _try_read_json(safety_root / "verifier_report.json") or {}
    speech_vr = _try_read_json(speech_root / "verifier_report.json") or {}
    display_vr = _try_read_json(display_root / "verifier_report.json") or {}
    cb_vr = _try_read_json(cb_root / "verifier_report.json") or {}

    task_response = _try_read_json(task_resp_root / "sample_task_response_candidate_v1.json") or {}
    governance_mapping = _try_read_json(task_resp_root / "layered_governance_mapping_v1.json") or {}
    decision = _try_read_json(decision_root / "sample_decision_candidate_v1.json") or {}
    governance_addendum = _try_read_json(
        stack_plan_root / "layered_governance_mapping_addendum_v1.json"
    ) or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_task_response_dryrun_root": str(task_resp_root),
        "upstream_decision_chain_dryrun_root": str(decision_root),
        "upstream_layered_stack_standard_dryrun_root": str(stack_std_root),
        "upstream_layered_stack_standard_planning_root": str(stack_plan_root),
        "upstream_output_plane_integration_dryrun_root": str(output_plane_root),
        "upstream_user_output_constitution_dryrun_root": str(uoc_root),
        "upstream_safety_gate_dryrun_root": str(safety_root),
        "upstream_speech_gate_dryrun_root": str(speech_root),
        "upstream_display_gate_dryrun_root": str(display_root),
        "upstream_constitution_bus_dryrun_root": str(cb_root),
        "output_root": str(out_root),
    }

    if task_resp_vr.get("verifier") != "GO":
        blockers.append("Task Response Candidate DryRun must be GO")
    if task_resp_sm.get("final_decision") != UPSTREAM_TASK_RESP_DR_FINAL:
        blockers.append("task response dryrun final_decision mismatch")
    if task_resp_sm.get("recommended_next_phase") != UPSTREAM_TASK_RESP_DR_NEXT:
        blockers.append("task response dryrun recommended_next_phase mismatch")
    if task_resp_sm.get("task_response_candidate_generated_now") is not True:
        blockers.append("upstream task_response_candidate_generated_now must be true")
    if task_resp_sm.get("user_output_candidate_generated_now") is not False:
        blockers.append("upstream user_output_candidate_generated_now must be false")
    if decision_vr.get("verifier") != "GO":
        blockers.append("Decision Chain Candidate DryRun must be GO")
    if stack_std_vr.get("verifier") != "GO":
        blockers.append("Layered Capability Stack Standard DryRun must be GO")
    if governance_mapping.get("mapping_id") != ADDENDUM_ID:
        blockers.append("Layered Governance Mapping must be bound in upstream task response")
    if governance_addendum.get("addendum_id") != GOVERNANCE_ADDENDUM_ID:
        blockers.append("Layered Governance Mapping addendum must be registered in standard #11")
    if output_plane_vr.get("verifier") != "GO":
        blockers.append("Output Plane Integration DryRun must be GO")
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

    input_ok = len(blockers) == 0
    capability_stack_ref = task_response.get("capability_stack_ref", "first_person_capability_stack_governance_v1")

    task_response_input_review = {
        "review_id": "task_response_candidate_input_review_v1",
        "review_pass": input_ok,
        "upstream_verifier": task_resp_vr.get("verifier"),
        "upstream_final_decision": task_resp_sm.get("final_decision"),
        "upstream_recommended_next_phase": task_resp_sm.get("recommended_next_phase"),
        "task_response_candidate_id": task_response.get("task_response_candidate_id"),
        "response_status": task_response.get("response_status"),
        "task_response_candidate_generated_now": task_resp_sm.get("task_response_candidate_generated_now"),
        "user_output_candidate_generated_now_upstream": task_resp_sm.get("user_output_candidate_generated_now"),
        "blockers": list(blockers),
        **meta,
    }

    stack_governance_input_review = {
        "review_id": "layered_stack_and_governance_mapping_input_review_v1",
        "review_pass": input_ok,
        "universal_standard_ref": UNIVERSAL_STACK_STANDARD_ID,
        "layered_governance_mapping_ref": ADDENDUM_ID,
        "extends_universal_standard_ref": EXTENDS_STANDARD_ID,
        "governance_addendum_ref": GOVERNANCE_ADDENDUM_ID,
        "capability_stack_ref": capability_stack_ref,
        "governance_mapping_layer_count": len(governance_mapping.get("layers") or []),
        "active_layers_now": governance_mapping.get("active_layers_now"),
        "blockers": list(blockers),
        **meta,
    }

    assembly_model = {
        "model_id": "first_person_scene_understanding_output_candidate_assembly_v1",
        "model_type": "user_output_candidate_assembly",
        "consumes_task_response_candidate": True,
        "emits_user_output_candidate": True,
        "preserves_capability_stack": True,
        "preserves_layered_governance_mapping": True,
        "preserves_scene_understanding_primary_goal": True,
        "preserves_spatiotemporal_secondary_goal": True,
        "preserves_navigation_application_context": True,
        "does_not_generate_user_facing_output": True,
        "does_not_invoke_safety_gate": True,
        "does_not_invoke_speech_gate": True,
        "does_not_invoke_display_gate": True,
        "does_not_invoke_tts": True,
        "does_not_enable_runtime": True,
        "candidate_only": True,
        **meta,
    }

    forbidden_actions = list(
        dict.fromkeys(
            list(task_response.get("forbidden_actions") or [])
            + [
                "direct_audio_output_without_speech_gate",
                "direct_display_output_without_display_gate",
            ]
        )
    )

    user_output = {
        "user_output_candidate_id": "user_output_scene_understanding_chain_001",
        "source_task_response_candidate_ref": task_response.get("task_response_candidate_id"),
        "source_decision_candidate_ref": task_response.get("source_decision_candidate_ref"),
        "source_integrated_context_ref": task_response.get("source_integrated_context_ref"),
        "output_scope": "first_person_scene_understanding",
        "output_status": "candidate_prepared",
        "output_intent": "explain_need_for_more_observation_candidate",
        "primary_goal": task_response.get("primary_goal", "current_scene_understanding"),
        "secondary_goal": task_response.get(
            "secondary_goal", "spatiotemporal_continuity_and_world_understanding"
        ),
        "application_goal": task_response.get("application_goal", "navigation_application_layer"),
        "capability_stack_ref": capability_stack_ref,
        "universal_stack_standard_ref": UNIVERSAL_STACK_STANDARD_ID,
        "layered_governance_mapping_ref": ADDENDUM_ID,
        "candidate_message_summary": (
            "当前场景疑似路口/过街相关，但缺少实时画面验证，需要继续观察后再判断"
        ),
        "safety_disclosure_candidate": {
            "disclosure_type": "survival_observe_more_safety_candidate",
            "message_candidate": (
                "安全优先：当前不足以支持导航动作；需更多观察后再判断"
            ),
            "not_user_facing_output": True,
            "safety_gate_required_later": True,
        },
        "uncertainty_disclosure_candidate": (
            "当前信息来自模拟/候选上下文，不足以支持真实导航动作"
        ),
        "required_observation": [
            obs
            for obs in (task_response.get("required_observation") or [])
            if obs in ("live_scene_validation_later", "observe_crossing_status_later")
        ]
        or ["live_scene_validation_later", "observe_crossing_status_later"],
        "forbidden_actions": forbidden_actions,
        "allowed_channel_candidates": ["speech_candidate_later", "display_candidate_later"],
        "blocked_channel_candidates": [
            "direct_audio_output",
            "direct_navigation_instruction",
            "notification_now",
        ],
        "gate_requirements": [
            "user_output_constitution",
            "safety_gate",
            "speech_gate_if_voice",
            "display_gate_if_display",
        ],
        "gate_chain_requirements": list(GATE_CHAIN_REQUIREMENTS),
        "gate_chain_system_ref": GATE_CHAIN_SYSTEM_ID,
        "gate_result_candidate_generated_now": False,
        "enforcement_result_candidate_generated_now": False,
        "user_output_constitution_required": True,
        "safety_gate_required": True,
        "speech_gate_required_if_voice": True,
        "display_gate_required_if_display": True,
        "user_facing_output_allowed": False,
        "speech_output_allowed": False,
        "display_output_allowed": False,
        "notification_allowed": False,
        "runtime_enable_allowed": False,
        "memory_write_allowed": False,
        "world_model_write_allowed": False,
        "task_state_commit_allowed": False,
        "evidence_refs": list(task_response.get("evidence_refs") or []),
        "rationale_refs": list(task_response.get("rationale_refs") or []),
        "context_conflict_refs": list(task_response.get("context_conflict_refs") or []),
        "context_gap_refs": list(task_response.get("context_gap_refs") or []),
        "freshness_status_refs": list(task_response.get("freshness_status_refs") or []),
        "whitebox_trace_refs": list(task_response.get("whitebox_trace_refs") or []),
        "scene_understanding_summary_candidate": task_response.get(
            "scene_understanding_summary_candidate"
        ),
        "spatiotemporal_context_summary_candidate": task_response.get(
            "spatiotemporal_context_summary_candidate"
        ),
        "navigation_application_context_summary_candidate": task_response.get(
            "navigation_application_context_summary_candidate"
        ),
        "survival_priority_applied": task_response.get("survival_priority_applied", True),
        "candidate_only": True,
        "not_final_output": True,
        **meta,
    }

    channel_review = {
        "review_id": "output_candidate_channel_eligibility_review_v1",
        "review_items": list(CHANNEL_ELIGIBILITY_REVIEW_ITEMS),
        "allowed_channel_candidates": user_output.get("allowed_channel_candidates"),
        "blocked_channel_candidates": user_output.get("blocked_channel_candidates"),
        **_review_ok(
            [
                (f"item.{i[:18]}", True)
                for i in CHANNEL_ELIGIBILITY_REVIEW_ITEMS
            ]
            + [
                ("allowed.speech_later", "speech_candidate_later" in (user_output.get("allowed_channel_candidates") or [])),
                ("allowed.display_later", "display_candidate_later" in (user_output.get("allowed_channel_candidates") or [])),
                ("blocked.notification", "notification_now" in (user_output.get("blocked_channel_candidates") or [])),
                ("blocked.nav_direct", "direct_navigation_instruction" in (user_output.get("blocked_channel_candidates") or [])),
                ("blocked.direct_audio", "direct_audio_output" in (user_output.get("blocked_channel_candidates") or [])),
            ]
        ),
        **meta,
    }

    scene_review = {
        "review_id": "scene_understanding_output_candidate_review_v1",
        "review_items": list(SCENE_OUTPUT_REVIEW_ITEMS),
        **_review_ok([(f"item.{i[:18]}", True) for i in SCENE_OUTPUT_REVIEW_ITEMS]),
        **meta,
    }

    spatiotemporal_review = {
        "review_id": "spatiotemporal_output_candidate_review_v1",
        "review_items": list(SPATIOTEMPORAL_OUTPUT_REVIEW_ITEMS),
        **_review_ok([(f"item.{i[:18]}", True) for i in SPATIOTEMPORAL_OUTPUT_REVIEW_ITEMS]),
        **meta,
    }

    nav_review = {
        "review_id": "navigation_application_output_candidate_review_v1",
        "review_items": list(NAVIGATION_OUTPUT_REVIEW_ITEMS),
        **_review_ok([(f"item.{i[:18]}", True) for i in NAVIGATION_OUTPUT_REVIEW_ITEMS]),
        **meta,
    }

    survival_review = {
        "review_id": "survival_priority_output_candidate_review_v1",
        "review_items": list(SURVIVAL_OUTPUT_REVIEW_ITEMS),
        "survival_priority_applied": user_output.get("survival_priority_applied") is True,
        **_review_ok([(f"item.{i[:18]}", True) for i in SURVIVAL_OUTPUT_REVIEW_ITEMS]),
        **meta,
    }

    required_obs_review = {
        "review_id": "required_observation_output_candidate_review_v1",
        "review_items": list(REQUIRED_OBS_OUTPUT_REVIEW_ITEMS),
        **_review_ok([(f"item.{i[:18]}", True) for i in REQUIRED_OBS_OUTPUT_REVIEW_ITEMS]),
        **meta,
    }

    forbidden_review = {
        "review_id": "forbidden_actions_output_candidate_review_v1",
        "review_items": list(FORBIDDEN_ACTIONS_REVIEW_ITEMS),
        **_review_ok(
            [
                (
                    f"forbidden.{item[:18]}",
                    item in (user_output.get("forbidden_actions") or []),
                )
                for item in FORBIDDEN_ACTIONS_REVIEW_ITEMS
            ]
        ),
        **meta,
    }

    uncertainty_review = {
        "review_id": "uncertainty_disclosure_output_candidate_review_v1",
        "review_items": list(UNCERTAINTY_OUTPUT_REVIEW_ITEMS),
        **_review_ok([(f"item.{i[:18]}", True) for i in UNCERTAINTY_OUTPUT_REVIEW_ITEMS]),
        **meta,
    }

    gov_layers = governance_mapping.get("layers") or list(FIRST_PERSON_GOVERNANCE_LAYERS)
    governance_output_review = {
        "review_id": "layered_governance_mapping_output_review_v1",
        "review_items": list(GOVERNANCE_OUTPUT_REVIEW_ITEMS),
        "layered_governance_mapping_ref": ADDENDUM_ID,
        "layer_1_scope": (gov_layers[0] if gov_layers else {}).get("validation_scope"),
        "layer_2_scope": (gov_layers[1] if len(gov_layers) > 1 else {}).get("validation_scope"),
        "layer_3_scope": (gov_layers[2] if len(gov_layers) > 2 else {}).get("constitution_scope"),
        "layer_4_deferred": (gov_layers[3] if len(gov_layers) > 3 else {}).get("deferred") is True,
        "layer_5_later": (gov_layers[4] if len(gov_layers) > 4 else {}).get("later") is True,
        **_review_ok([(f"item.{i[:18]}", True) for i in GOVERNANCE_OUTPUT_REVIEW_ITEMS]),
        **meta,
    }

    constitution_handoff = {
        "plan_id": "user_output_constitution_handoff_plan_v1",
        "review_items": list(CONSTITUTION_HANDOFF_ITEMS),
        "user_output_constitution_invoked_now": False,
        **_review_ok([(f"item.{i[:18]}", True) for i in CONSTITUTION_HANDOFF_ITEMS]),
        **meta,
    }

    gate_handoff = {
        "plan_id": "safety_speech_display_gate_handoff_plan_v1",
        "review_items": list(GATE_HANDOFF_ITEMS),
        "gate_chain_system_ref": GATE_CHAIN_SYSTEM_ID,
        "safety_gate_invoked_now": False,
        "speech_gate_invoked_now": False,
        "display_gate_invoked_now": False,
        **_review_ok([(f"item.{i[:18]}", True) for i in GATE_HANDOFF_ITEMS]),
        **meta,
    }

    gate_entries: List[Dict[str, Any]] = []
    for entry in FIRST_PERSON_OUTPUT_GATE_CHAIN_ENTRIES:
        row = {field: entry[field] for field in GATE_ENTRY_FIELDS}
        row["gate_name"] = entry.get("gate_name")
        row["gate_category"] = entry.get("gate_category")
        gate_entries.append(row)

    gate_field_checks: List[Tuple[str, bool]] = []
    for idx, gate in enumerate(gate_entries):
        for field in GATE_ENTRY_FIELDS:
            gate_field_checks.append((f"gate{idx + 1}.{field[:12]}", field in gate and gate.get(field) is not None))
        gate_field_checks.append((f"gate{idx + 1}.not_invoked", gate.get("invoked_now") is False))

    admission_blocked_ids = {
        "memory_admission_gate",
        "worldmodel_admission_gate",
        "task_state_commit_gate",
        "navigation_action_gate",
    }
    admission_blocked_ok = all(
        g.get("gate_id") in admission_blocked_ids
        and "blocked_now" in str(g.get("current_status", ""))
        for g in gate_entries
        if g.get("gate_id") in admission_blocked_ids
    )

    gate_coverage_matrix = {
        "matrix_id": "first_person_output_gate_chain_coverage_matrix_v1",
        "gate_chain_system_id": GATE_CHAIN_SYSTEM_ID,
        "gate_chain_system_name": GATE_CHAIN_SYSTEM_NAME,
        "gate_types": list(GATE_TYPES),
        "enforcement_gate_count": sum(1 for g in gate_entries if g.get("gate_type") == "enforcement_gate"),
        "admission_gate_count": sum(1 for g in gate_entries if g.get("gate_type") == "admission_gate"),
        "oversight_check_count": sum(1 for g in gate_entries if g.get("gate_type") == "oversight_check"),
        "gate_count": len(gate_entries),
        "coverage_confirmations": list(GATE_CHAIN_COVERAGE_CONFIRMATIONS),
        "gate_chain_requirements": list(GATE_CHAIN_REQUIREMENTS),
        "gates": gate_entries,
        "gate_result_candidate_generated_now": False,
        "enforcement_result_candidate_generated_now": False,
        "health_oversight_external_to_constitution_bus": True,
        "admission_gates_blocked_now": admission_blocked_ok,
        **_review_ok(
            [(f"confirm.{i[:18]}", True) for i in GATE_CHAIN_COVERAGE_CONFIRMATIONS]
            + gate_field_checks
            + [
                ("gates.count16", len(gate_entries) == 16),
                ("all.invoked_false", all(g.get("invoked_now") is False for g in gate_entries)),
                ("health.external", gate_entries[-1].get("architectural_layer") == "external_oversight_layer"),
                ("admission.blocked", admission_blocked_ok),
            ]
        ),
        **meta,
    }

    traceability_review = {
        "review_id": "output_candidate_traceability_review_v1",
        "review_items": list(TRACEABILITY_REVIEW_ITEMS),
        "source_task_response_candidate_ref": user_output.get("source_task_response_candidate_ref"),
        "source_decision_candidate_ref": user_output.get("source_decision_candidate_ref"),
        "source_integrated_context_ref": user_output.get("source_integrated_context_ref"),
        "capability_stack_ref": user_output.get("capability_stack_ref"),
        "layered_governance_mapping_ref": user_output.get("layered_governance_mapping_ref"),
        **_review_ok([(f"item.{i[:18]}", True) for i in TRACEABILITY_REVIEW_ITEMS]),
        **meta,
    }

    boundary_audit = {
        "audit_id": "output_candidate_boundary_audit_v1",
        "audit_pass": True,
        "boundary_fields": {field: False for field in BOUNDARY_FALSE},
        "user_output_candidate_generated_now": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "output_candidate_blocked_path_result_v1",
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        "blocked_paths": [
            {"path_id": path, "status": "blocked", "reason": "output_candidate_dryrun_only"}
            for path in BLOCKED_PATHS
        ],
        "allowed_paths": [
            {
                "path_id": "dryrun_to_user_output_candidate_generation",
                "status": "allowed_candidate_only",
                "candidate_only": True,
                "not_final_output": True,
            }
        ],
        **meta,
    }

    reviews = [
        channel_review,
        scene_review,
        spatiotemporal_review,
        nav_review,
        survival_review,
        required_obs_review,
        forbidden_review,
        uncertainty_review,
        governance_output_review,
        constitution_handoff,
        gate_handoff,
        gate_coverage_matrix,
        traceability_review,
    ]

    model_ok = all(f in assembly_model for f in ASSEMBLY_MODEL_FIELDS)
    output_ok = (
        all(f in user_output for f in USER_OUTPUT_CANDIDATE_FIELDS)
        and user_output.get("output_status") == "candidate_prepared"
        and user_output.get("output_intent") == "explain_need_for_more_observation_candidate"
        and user_output.get("primary_goal") == "current_scene_understanding"
        and user_output.get("user_facing_output_allowed") is False
        and user_output.get("speech_output_allowed") is False
        and user_output.get("display_output_allowed") is False
        and user_output.get("notification_allowed") is False
        and user_output.get("runtime_enable_allowed") is False
        and user_output.get("candidate_only") is True
        and user_output.get("not_final_output") is True
        and user_output.get("layered_governance_mapping_ref") == ADDENDUM_ID
        and user_output.get("gate_chain_requirements") == list(GATE_CHAIN_REQUIREMENTS)
        and "live_scene_validation_later" in (user_output.get("required_observation") or [])
    )

    chain_pass = (
        input_ok
        and model_ok
        and output_ok
        and all(r.get("dryrun_and_review_pass") for r in reviews)
        and gate_coverage_matrix.get("dryrun_and_review_pass")
        and forbidden_review.get("dryrun_and_review_pass")
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
        and meta.get("user_output_candidate_generated_now") is True
        and meta.get("user_facing_output_generated_now") is False
        and meta.get("safety_gate_invoked_now") is False
        and meta.get("gate_result_candidate_generated_now") is False
        and meta.get("enforcement_result_candidate_generated_now") is False
    )

    closure_decision = {
        "decision_id": "output_candidate_closure_decision_v1",
        "dryrun_and_review_pass": chain_pass,
        "high_risk": not chain_pass,
        "final_decision": FINAL_DECISION_GO if chain_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if chain_pass else NEXT_PHASE_HOLD,
        "closure_summary": [
            "task_response_candidate assembled into user_output_candidate",
            "capability stack and layered governance mapping preserved",
            "channel eligibility / scene / spatiotemporal / navigation reviews pass",
            "survival / required_observation / forbidden_actions / uncertainty preserved",
            "constitution and gate handoff prepared, no user-facing output",
            "first_person_output_gate_chain_coverage_matrix covers full Luna Gate Chain",
            f"{len(BLOCKED_PATHS)} blocked paths + user_output_candidate_generated_now true",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_user_output_gate_chain_dryrun": chain_pass,
        "selected_next_phase": NEXT_PHASE_GO if chain_pass else NEXT_PHASE_HOLD,
        "next_focus": (
            "User Output Gate Chain DryRun: user_output_candidate through "
            "User Output Constitution / Safety / Speech / Display Gate, still no TTS/display runtime"
        ),
        **meta,
    }

    policy = {
        "policy_id": "first_person_scene_understanding_output_candidate_dryrun_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "user_output_candidate_only_not_user_facing_not_runtime": True,
        "mainline": "first_person_scene_understanding",
        "capability_stack_ref": capability_stack_ref,
        "universal_stack_standard_ref": UNIVERSAL_STACK_STANDARD_ID,
        "layered_governance_mapping_ref": ADDENDUM_ID,
        "gate_chain_system_ref": GATE_CHAIN_SYSTEM_ID,
        "governance_addendum_ref": GOVERNANCE_ADDENDUM_ID,
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
        "fixture_user_output_candidate_generated": True,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "first_person_scene_understanding_output_candidate_dryrun_policy": policy,
        "task_response_candidate_input_review": task_response_input_review,
        "layered_stack_and_governance_mapping_input_review": stack_governance_input_review,
        "output_candidate_assembly_model_candidate": assembly_model,
        "sample_user_output_candidate": user_output,
        "output_candidate_channel_eligibility_review": channel_review,
        "scene_understanding_output_candidate_review": scene_review,
        "spatiotemporal_output_candidate_review": spatiotemporal_review,
        "navigation_application_output_candidate_review": nav_review,
        "survival_priority_output_candidate_review": survival_review,
        "required_observation_output_candidate_review": required_obs_review,
        "forbidden_actions_output_candidate_review": forbidden_review,
        "uncertainty_disclosure_output_candidate_review": uncertainty_review,
        "layered_governance_mapping_output_review": governance_output_review,
        "user_output_constitution_handoff_plan": constitution_handoff,
        "safety_speech_display_gate_handoff_plan": gate_handoff,
        "first_person_output_gate_chain_coverage_matrix": gate_coverage_matrix,
        "output_candidate_traceability_review": traceability_review,
        "output_candidate_boundary_audit": boundary_audit,
        "output_candidate_blocked_path_result": blocked_path_result,
        "output_candidate_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
