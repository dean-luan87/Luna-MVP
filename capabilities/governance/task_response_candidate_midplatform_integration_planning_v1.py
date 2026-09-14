# -*- coding: utf-8 -*-
"""Task Response Candidate Midplatform Integration Planning v1 — planning-only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.luna_validation_factory_consolidation_v1 import (
    FINAL_DECISION as FACTORY_FINAL,
    PHASE_ID as FACTORY_PHASE,
)
from capabilities.governance.midplatform_backbone_definition_alignment_v1 import (
    FINAL_DECISION_GO as ALIGNMENT_FINAL_GO,
    PHASE_ID as ALIGNMENT_PHASE,
)
from capabilities.governance.midplatform_minimal_backbone_dryrun_v1 import BLOCK_CHECKS as BACKBONE_BLOCK_CHECKS
from capabilities.governance.midplatform_minimal_backbone_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
    PHASE_ID as POST_REVIEW_PHASE,
)
from capabilities.governance.midplatform_post_backbone_roadmap_decision_v1 import (
    DEFERRED_ROUTE,
    FINAL_DECISION_GO as ROADMAP_FINAL_GO,
    NEXT_PHASE_GO as ROADMAP_NEXT_PHASE,
    PHASE_ID as ROADMAP_PHASE,
    SELECTED_ROUTE,
)
from capabilities.governance.midplatform_structure_cleanup_planning_v1 import (
    FINAL_DECISION_GO as CLEANUP_FINAL_GO,
    PHASE_ID as CLEANUP_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Task-Response-Candidate-Midplatform-Integration-Planning-v1-001"
SCOPE = "task_response_candidate_integration_planning_only"
SOURCE_CHAIN = "task_response_candidate_midplatform_integration_planning_v1"

UPSTREAM_ROADMAP_FINAL = ROADMAP_FINAL_GO
UPSTREAM_ROADMAP_NEXT = ROADMAP_NEXT_PHASE

FINAL_DECISION_GO = "TASK_RESPONSE_CANDIDATE_MIDPLATFORM_INTEGRATION_PLANNING_READY_FOR_DRYRUN"
FINAL_DECISION_HOLD = "TASK_RESPONSE_CANDIDATE_MIDPLATFORM_INTEGRATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Task-Response-Candidate-Midplatform-Integration-DryRun-v1-001"

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "task_response_candidate_midplatform_integration_planning"
)

CLOSED_INPUT_CANDIDATES: Tuple[str, ...] = (
    "visual_observation_candidate",
    "ocr_result_candidate",
    "navigation_guidance_candidate",
)

ALLOWED_MIDPLATFORM_INPUTS: Tuple[str, ...] = CLOSED_INPUT_CANDIDATES + (
    "task_routing_candidate",
    "guidance_queue_item",
    "output_arbitration_candidate",
    "fallback_candidate",
    "clarification_requirement_candidate",
)

FORBIDDEN_INPUTS: Tuple[str, ...] = (
    "live_camera",
    "real_ocr_provider",
    "navigation_action",
    "task_commit",
    "tts_output",
    "llm_output",
    "memory_write",
    "world_model_write",
    "library_direct_experience",
    "hive_direct_experience",
)

TASK_RESPONSE_DEFAULT_FIELDS: Dict[str, Any] = {
    "output_type": "task_response_candidate",
    "candidate_only": True,
    "fact_status": "not_fact",
    "task_commit_allowed": False,
    "user_facing_output_allowed": False,
    "tts_allowed": False,
    "runtime_action_allowed": False,
    "write_allowed": False,
    "source_chain_required": True,
    "provenance_required": True,
    "related_task_state_candidate_required": True,
    "related_input_candidates_required": True,
    "output_arbitration_required": True,
    "constitution_gate_required": True,
}

CONSTITUTION_BLOCKS: Tuple[str, ...] = (
    "task_response_candidate_to_fact",
    "task_response_candidate_to_task_commit",
    "task_response_candidate_to_tts",
    "task_response_candidate_to_user_facing_output",
    "task_response_candidate_to_navigation_action",
    "task_response_candidate_to_memory_write",
    "task_response_candidate_to_world_model_write",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "task_response_to_task_commit",
    "task_response_to_tts",
    "task_response_to_user_output",
    "task_response_to_fact_write",
    "task_response_to_memory_write",
    "task_response_to_world_model_write",
    "task_response_to_navigation_action",
    "task_response_to_llm_invocation",
    "task_response_to_model_runtime",
)

FLOW_PLANS: Tuple[Dict[str, Any], ...] = (
    {
        "flow_id": "Flow_1_vision_based_task_response",
        "label": "Vision-based task response candidate",
        "steps": [
            "visual_observation_candidate",
            "task_routing_candidate",
            "task_response_candidate",
        ],
    },
    {
        "flow_id": "Flow_2_ocr_based_task_response",
        "label": "OCR-based task response candidate",
        "steps": [
            "ocr_result_candidate",
            "task_routing_candidate",
            "task_response_candidate",
        ],
    },
    {
        "flow_id": "Flow_3_navigation_guidance_based_task_response",
        "label": "Navigation-guidance-based task response candidate",
        "steps": [
            "navigation_guidance_candidate",
            "constitution_safety_gate",
            "task_routing_candidate",
            "task_response_candidate",
        ],
    },
    {
        "flow_id": "Flow_4_mixed_candidate_task_response",
        "label": "Mixed candidate task response candidate",
        "steps": [
            "visual_observation_candidate",
            "ocr_result_candidate",
            "navigation_guidance_candidate",
            "evidence_governance",
            "task_routing_candidate",
            "task_response_candidate",
        ],
    },
)

NON_CLAIMS: Tuple[str, ...] = (
    "Planning GO ≠ task_response_candidate generated",
    "task_response_candidate defined ≠ user response generated",
    "task_response_candidate defined ≠ task commit allowed",
    "output arbitration planned ≠ TTS allowed",
    "task layer integration planned ≠ task manager runtime enabled",
    "task response flow planned ≠ Memory / WorldModel write allowed",
    "Route A selected ≠ Route B cancelled",
)

BOUNDARY_FALSE_FIELDS: Tuple[str, ...] = (
    "task_response_candidate_generated_now",
    "task_response_chain_started_now",
    "task_state_committed_now",
    "task_manager_committed_now",
    "task_runtime_action_executed_now",
    "tts_invoked_now",
    "speech_response_candidate_generated_now",
    "user_facing_output_generated_now",
    "llm_invoked_now",
    "model_runtime_invoked_now",
    "navigation_action_triggered_now",
    "world_model_written_now",
    "memory_written_now",
    "library_write_executed_now",
    "hive_sync_executed_now",
    "runtime_enabled_now",
    "real_runtime_enabled_now",
)


def _boundary_meta() -> Dict[str, Any]:
    return {
        "task_response_candidate_integration_planning_only": True,
        "task_response_candidate_generated_now": False,
        "task_response_chain_started_now": False,
        "task_state_committed_now": False,
        "task_manager_committed_now": False,
        "task_runtime_action_executed_now": False,
        "tts_invoked_now": False,
        "speech_response_candidate_generated_now": False,
        "user_facing_output_generated_now": False,
        "llm_invoked_now": False,
        "model_runtime_invoked_now": False,
        "navigation_action_triggered_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "library_write_executed_now": False,
        "hive_sync_executed_now": False,
        "runtime_enabled_now": False,
        "real_runtime_enabled_now": False,
        "task_response_candidate_started_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        **{k: v for k, v in TASK_RESPONSE_DEFAULT_FIELDS.items() if k not in ("output_arbitration_required", "constitution_gate_required")},
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _check_go(root: Path) -> bool:
    if not root.is_dir():
        return False
    vr = _try_read_json(root / "verifier_report.json") or {}
    sm = _try_read_json(root / "summary.json") or {}
    return (vr.get("verifier") == "GO" and vr.get("passed") is True) or sm.get("boundary_ok") is True


def run_task_response_candidate_midplatform_integration_planning_v1(
    *,
    midplatform_post_backbone_roadmap_decision_root: str,
    midplatform_minimal_backbone_post_dryrun_review_root: str,
    midplatform_minimal_backbone_dryrun_root: str,
    midplatform_structure_cleanup_planning_root: str,
    midplatform_backbone_definition_alignment_root: str,
    luna_validation_factory_consolidation_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    roots = {
        "roadmap": Path(midplatform_post_backbone_roadmap_decision_root).expanduser().resolve(),
        "post_review": Path(midplatform_minimal_backbone_post_dryrun_review_root).expanduser().resolve(),
        "dryrun": Path(midplatform_minimal_backbone_dryrun_root).expanduser().resolve(),
        "cleanup": Path(midplatform_structure_cleanup_planning_root).expanduser().resolve(),
        "alignment": Path(midplatform_backbone_definition_alignment_root).expanduser().resolve(),
        "factory": Path(luna_validation_factory_consolidation_root).expanduser().resolve(),
    }
    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_boundary_meta(), "output_root": str(out_root), "upstream_roots": {k: str(v) for k, v in roots.items()}}

    roadmap_sm = _try_read_json(roots["roadmap"] / "summary.json") or {}
    roadmap_vr = _try_read_json(roots["roadmap"] / "verifier_report.json") or {}
    route_a = _try_read_json(roots["roadmap"] / "route_a_task_response_candidate_assessment_v1.json") or {}
    post_sm = _try_read_json(roots["post_review"] / "summary.json") or {}
    post_vr = _try_read_json(roots["post_review"] / "verifier_report.json") or {}
    dryrun_sm = _try_read_json(roots["dryrun"] / "summary.json") or {}
    dryrun_vr = _try_read_json(roots["dryrun"] / "verifier_report.json") or {}
    cleanup_sm = _try_read_json(roots["cleanup"] / "summary.json") or {}
    align_sm = _try_read_json(roots["alignment"] / "summary.json") or {}
    factory_sm = _try_read_json(roots["factory"] / "summary.json") or {}

    roadmap_go = roadmap_vr.get("verifier") == "GO" and roadmap_vr.get("passed") is True
    if not roadmap_go:
        blockers.append("roadmap decision verifier must be GO")
    if roadmap_sm.get("final_decision") != UPSTREAM_ROADMAP_FINAL:
        blockers.append("roadmap final_decision mismatch")
    if roadmap_sm.get("recommended_next_phase") != UPSTREAM_ROADMAP_NEXT:
        blockers.append("roadmap recommended_next_phase mismatch")
    if roadmap_sm.get("selected_route") != SELECTED_ROUTE:
        blockers.append("selected_route must be Route A")
    if roadmap_sm.get("deferred_route") != DEFERRED_ROUTE:
        blockers.append("deferred_route must be Route B")
    if roadmap_sm.get("task_response_candidate_started_now") is True:
        blockers.append("task_response_candidate_started_now must be false")

    invariants = route_a.get("required_invariants") or {}
    if invariants.get("candidate_only") is not True:
        blockers.append("route_a candidate_only must be true")
    if invariants.get("fact_status") != "not_fact":
        blockers.append("route_a fact_status must be not_fact")
    for key in ("task_commit_allowed", "user_facing_output_allowed", "tts_allowed"):
        if invariants.get(key) is not False:
            blockers.append(f"route_a invariant {key} must be false")

    if not (post_vr.get("verifier") == "GO" and post_sm.get("boundary_ok") is True):
        blockers.append("post-dryrun review must be GO")
    if post_sm.get("three_candidate_flows_trusted") is not True:
        blockers.append("three_candidate_flows_trusted required")
    if post_sm.get("ten_blocks_all_blocked") is not True:
        blockers.append("ten_blocks_all_blocked required")

    if not (dryrun_vr.get("verifier") == "GO" and dryrun_sm.get("flows_all_pass") is True):
        blockers.append("minimal backbone dryrun must be GO with flows pass")

    for label, root, phase, final in (
        ("cleanup", roots["cleanup"], CLEANUP_PHASE, CLEANUP_FINAL_GO),
        ("alignment", roots["alignment"], ALIGNMENT_PHASE, ALIGNMENT_FINAL_GO),
        ("factory", roots["factory"], FACTORY_PHASE, FACTORY_FINAL),
    ):
        if not _check_go(root):
            blockers.append(f"{label} upstream must be GO")
        sm = _try_read_json(root / "summary.json") or {}
        if phase and sm.get("phase") != phase:
            blockers.append(f"{label} phase mismatch")
        if final and sm.get("final_decision") != final:
            blockers.append(f"{label} final_decision mismatch")

    input_review = {
        "review_id": "post_backbone_roadmap_input_review_v1",
        "roadmap_root": str(roots["roadmap"]),
        "post_review_root": str(roots["post_review"]),
        "dryrun_root": str(roots["dryrun"]),
        "roadmap_verifier_go": roadmap_go,
        "selected_route": roadmap_sm.get("selected_route"),
        "deferred_route": roadmap_sm.get("deferred_route"),
        "route_a_invariants": invariants,
        "post_review_go": post_vr.get("verifier") == "GO",
        "flows_trusted": post_sm.get("three_candidate_flows_trusted"),
        "ten_blocks_blocked": post_sm.get("ten_blocks_all_blocked"),
        "backbone_block_checks_observed": list(BACKBONE_BLOCK_CHECKS),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    scope_doc = {
        "scope_id": "task_response_candidate_scope_v1",
        "definition": (
            "task_response_candidate is a Task Layer candidate object expressing how the system "
            "might respond to current task state — not a final answer, TTS, commit, or memory write."
        ),
        "is_not": [
            "final_answer",
            "tts_output",
            "task_commit",
            "user_facing_output",
            "memory_write",
            "world_model_write",
        ],
        "primary_layers": ["task", "input_output", "constitution_overlay", "output_arbitration", "runtime_boundary"],
        **meta,
    }

    input_contract = {
        "contract_id": "task_response_candidate_input_contract_v1",
        "allowed_inputs": list(ALLOWED_MIDPLATFORM_INPUTS),
        "forbidden_inputs": list(FORBIDDEN_INPUTS),
        "closed_chain_prerequisites": list(CLOSED_INPUT_CANDIDATES),
        "requires_task_routing": True,
        **meta,
    }

    output_contract = {
        "contract_id": "task_response_candidate_output_contract_v1",
        "default_fields": dict(TASK_RESPONSE_DEFAULT_FIELDS),
        "must_not_emit": ["speech_response", "committed_task_state", "navigation_action", "ocr_fact", "visual_fact"],
        **meta,
    }

    task_layer_plan = {
        "plan_id": "task_layer_integration_plan_v1",
        "layer": "task",
        "role": "synthesize task_response_candidate from routed input candidates",
        "modules_planned_not_implemented": [
            "task_response_candidate_synthesis_contract",
            "task_state_candidate_link_registry",
        ],
        "task_commit_blocked": True,
        "task_manager_runtime_blocked": True,
        **meta,
    }

    io_layer_plan = {
        "plan_id": "input_output_layer_integration_plan_v1",
        "layer": "input_output",
        "role": "intake closed candidates and hand off to task layer without user output",
        "intake_from": list(CLOSED_INPUT_CANDIDATES),
        "output_arbitration_before_any_user_channel": True,
        **meta,
    }

    constitution_plan = {
        "plan_id": "constitution_overlay_for_task_response_v1",
        "overlay": "global_horizontal",
        "gates_required": True,
        "must_block": list(CONSTITUTION_BLOCKS),
        "all_blocks_enforced_in_planning": True,
        **meta,
    }

    arbitration_plan = {
        "plan_id": "output_arbitration_for_task_response_v1",
        "task_response_candidate_must_enter_arbitration": True,
        "output_allowed_default": False,
        "speech_response_candidate_generated_now": False,
        "allowed_arbitration_outcomes": [
            "hold",
            "fallback_candidate",
            "clarification_required",
        ],
        "direct_tts_forbidden": True,
        **meta,
    }

    runtime_plan = {
        "plan_id": "runtime_boundary_for_task_response_v1",
        "dryrun_allowed": True,
        "controlled_trial_allowed": False,
        "limited_runtime_allowed": False,
        "real_runtime_allowed": False,
        "task_commit_blocked": True,
        "user_output_blocked": True,
        "model_runtime_blocked": True,
        "memory_write_blocked": True,
        "world_model_write_blocked": True,
        **meta,
    }

    flow_plan = {
        "plan_id": "task_response_candidate_flow_plan_v1",
        "flows": list(FLOW_PLANS),
        "dryrun_will_cover": [f["flow_id"] for f in FLOW_PLANS],
        **meta,
    }

    blocked_matrix = {
        "matrix_id": "task_response_candidate_blocked_path_matrix_v1",
        "paths": [{"path_id": pid, "blocked": True, "observed_now": False} for pid in BLOCKED_PATHS],
        "paths_total": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "task_response_candidate_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "objective": "validate midplatform can emit task_response_candidate from three closed candidates with all boundaries off",
        "flows_to_simulate": [f["flow_id"] for f in FLOW_PLANS],
        "separate_post_dryrun_review_recommended": True,
        "do_not_merge_with_minimal_backbone_post_review": True,
        **meta,
    }

    planning_ok = input_review.get("review_pass") is True

    readiness = {
        "readiness_id": "task_response_integration_readiness_decision_v1",
        "ready_for_integration_dryrun": planning_ok,
        "final_decision": FINAL_DECISION_GO if planning_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_ok else PHASE_ID,
        "route_b_still_deferred": True,
        **meta,
    }

    policy = {
        "policy_id": "task_response_candidate_integration_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_only": True,
        **meta,
    }

    non_claims = {
        "register_id": "task_response_integration_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": planning_ok,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "high_risk_count": 0 if planning_ok else 1,
        **meta,
    }

    return {
        "task_response_candidate_integration_planning_policy": policy,
        "post_backbone_roadmap_input_review": input_review,
        "task_response_candidate_scope": scope_doc,
        "task_response_candidate_input_contract": input_contract,
        "task_response_candidate_output_contract": output_contract,
        "task_layer_integration_plan": task_layer_plan,
        "input_output_layer_integration_plan": io_layer_plan,
        "constitution_overlay_for_task_response": constitution_plan,
        "output_arbitration_for_task_response": arbitration_plan,
        "runtime_boundary_for_task_response": runtime_plan,
        "task_response_candidate_flow_plan": flow_plan,
        "task_response_candidate_blocked_path_matrix": blocked_matrix,
        "task_response_candidate_dryrun_plan": dryrun_plan,
        "task_response_integration_non_claims_register": non_claims,
        "task_response_integration_readiness_decision": readiness,
        "summary": summary,
    }
