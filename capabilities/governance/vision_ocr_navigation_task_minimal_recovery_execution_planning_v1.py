# -*- coding: utf-8 -*-
"""Vision / OCR / Navigation / Task Minimal Recovery Execution Planning v1.

Controlled minimal execution scheme design after post-dryrun review GO. Planning-only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Vision-OCR-Navigation-Task-Minimal-Recovery-Execution-Planning-v1-001"
PLANNING_SCOPE = "minimal_recovery_execution_planning_only"
SOURCE_CHAIN = "vision_ocr_navigation_task_minimal_recovery_execution_planning_v1"

UPSTREAM_PHASE = "Phase-Vision-OCR-Navigation-Task-Midplatform-Recovery-Post-DryRun-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "VISION_OCR_NAVIGATION_TASK_MIDPLATFORM_RECOVERY_POST_DRYRUN_REVIEW_READY_FOR_MINIMAL_RECOVERY_EXECUTION_PLANNING"
)
UPSTREAM_NEXT_PHASE = "Phase-Vision-OCR-Navigation-Task-Minimal-Recovery-Execution-Planning-v1-001"

FINAL_DECISION = "VISION_OCR_NAVIGATION_TASK_MINIMAL_RECOVERY_EXECUTION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Vision-OCR-Navigation-Task-Minimal-Recovery-Execution-DryRun-v1-001"

NON_CLAIMS: Tuple[str, ...] = (
    "Planning GO ≠ runtime enabled",
    "Minimal execution plan ≠ real execution",
    "Vision candidate ≠ visual fact",
    "OCR request candidate ≠ OCR provider invoked",
    "Navigation guidance candidate ≠ navigation action",
    "Task state candidate ≠ task committed",
    "Speech response candidate ≠ TTS invoked",
    "Cross-chain flow pass ≠ WorldModel / Memory write allowed",
    "Midplatform ambiguity registered ≠ midplatform refactored",
)

EXECUTION_GATES: Tuple[str, ...] = (
    "safety_gate",
    "source_chain_gate",
    "task_scope_gate",
    "runtime_disabled_gate",
    "no_worldmodel_write_gate",
    "no_memory_write_gate",
    "no_tts_gate",
    "no_navigation_action_gate",
    "no_ocr_provider_gate",
    "no_camera_gate",
    "fallback_gate",
)

CROSS_CHAIN_STEPS: Tuple[Dict[str, str], ...] = (
    {"step": 1, "node": "vision", "output": "visual_observation_candidate", "mode": "candidate_only"},
    {"step": 2, "node": "task_midplatform", "output": "task_observation_requirement", "mode": "candidate_only"},
    {
        "step": 3,
        "node": "ocr",
        "output": "ocr_request_candidate",
        "mode": "conditional_if_task_requires_text",
    },
    {
        "step": 4,
        "node": "navigation",
        "output": "navigation_guidance_candidate",
        "mode": "conditional_if_task_requires_movement",
    },
    {"step": 5, "node": "task_midplatform", "output": "task_response_candidate", "mode": "candidate_only"},
)

RUNTIME_BOUNDARY_FIELDS: Tuple[str, ...] = (
    "runtime_enabled_now",
    "camera_runtime_enabled_now",
    "vision_model_invoked_now",
    "ocr_provider_invoked_now",
    "navigation_action_triggered_now",
    "task_state_committed_now",
    "task_manager_committed_now",
    "world_model_written_now",
    "memory_written_now",
    "scene_delta_generated_now",
    "tts_invoked_now",
    "llm_invoked_now",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "minimal_recovery_execution_planning_only": True,
        "feature_implementation_started_now": False,
        "runtime_enabled_now": False,
        "camera_runtime_enabled_now": False,
        "vision_model_invoked_now": False,
        "ocr_provider_invoked_now": False,
        "navigation_runtime_enabled_now": False,
        "navigation_action_triggered_now": False,
        "task_midplatform_runtime_enabled_now": False,
        "task_state_committed_now": False,
        "task_manager_committed_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "scene_delta_generated_now": False,
        "tts_invoked_now": False,
        "llm_invoked_now": False,
        "midplatform_refactor_executed_now": False,
        "protected_asset_modified_now": False,
        "eval_out_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _is_workspace_fallback(path: Path) -> bool:
    return "Luna-Workspace-Min" in str(path)


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_vision_ocr_navigation_task_minimal_recovery_execution_planning_v1(
    *,
    vision_ocr_navigation_task_midplatform_recovery_post_dryrun_review_root: str,
) -> Dict[str, Any]:
    blockers: List[str] = []
    review_root = Path(
        vision_ocr_navigation_task_midplatform_recovery_post_dryrun_review_root
    ).expanduser().resolve()

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(review_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_post_dryrun_review_root": str(review_root),
    }

    review_sm = _try_read_json(review_root / "summary.json") or {}
    review_vr = _try_read_json(review_root / "verifier_report.json") or {}
    p0_rev = _try_read_json(review_root / "p0_chain_readiness_review_v1.json") or {}
    minimal_upstream = _try_read_json(
        review_root / "minimal_recovery_execution_planning_readiness_v1.json"
    ) or {}

    review_verifier_trusted = review_vr.get("verifier") == "GO" and review_vr.get("passed") is True
    review_summary_trusted = (
        review_sm.get("boundary_ok") is True
        and review_sm.get("phase") == UPSTREAM_PHASE
        and review_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL
        and review_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE
        and review_sm.get("review_only") is True
        and (review_sm.get("high_risk_count") or 0) == 0
    )
    if not review_verifier_trusted and not review_summary_trusted:
        blockers.append("post-dryrun review verifier must be GO")
    if p0_rev.get("all_chains_ready") is not True:
        blockers.append("all P0 chains must be ready")
    if minimal_upstream.get("ready_for_minimal_recovery_execution_planning") is not True:
        blockers.append("minimal_recovery_execution_planning readiness must be true")

    for field in RUNTIME_BOUNDARY_FIELDS:
        if review_sm.get(field) is True:
            blockers.append(f"{field} must be false")

    if review_sm.get("midplatform_refactor_executed_now") is True:
        blockers.append("midplatform_refactor_executed_now must be false")

    boundary_ok = not blockers

    policy = {
        "policy_id": "minimal_recovery_execution_planning_policy_v1",
        "scope": PLANNING_SCOPE,
        "mode": "controlled_minimal_execution_scheme_design_only",
        "p0_chains": ["vision", "ocr", "navigation", "task_midplatform"],
        **meta,
    }

    input_review = {
        "review_id": "recovery_post_dryrun_review_input_review_v1",
        "upstream_root": str(review_root),
        "upstream_verifier": review_vr.get("verifier"),
        "upstream_verifier_trusted": review_verifier_trusted,
        "upstream_summary_trusted": review_summary_trusted,
        "upstream_final_decision": review_sm.get("final_decision"),
        "all_p0_chains_ready": p0_rev.get("all_chains_ready"),
        "runtime_boundary_intact": review_sm.get("runtime_boundary_intact"),
        "midplatform_dual_directory_severity": "medium",
        "review_pass": boundary_ok,
        "blockers": blockers,
        **meta,
    }

    scope_matrix = {
        "matrix_id": "minimal_execution_scope_matrix_v1",
        "chains": [
            {
                "chain_id": "vision",
                "allowed": [
                    "controlled_frame_reference",
                    "focus_candidate",
                    "tracking_reference",
                ],
                "forbidden": [
                    "camera_runtime",
                    "new_image_read",
                    "vision_model_inference",
                    "visual_fact_write",
                ],
                "output_type": "visual_observation_candidate",
            },
            {
                "chain_id": "ocr",
                "allowed": ["OCRRequest", "ROI", "Evidence_Pack_planning"],
                "forbidden": [
                    "ocr_provider_invoke",
                    "paddle",
                    "rapidocr",
                    "ocr_evidence_generation",
                    "fact_layer_write",
                ],
                "role": "task_driven_auxiliary_ability",
                "output_type": "ocr_request_candidate",
            },
            {
                "chain_id": "navigation",
                "allowed": [
                    "guidance_candidate",
                    "readonly_map_hint",
                    "route_state_candidate",
                ],
                "forbidden": [
                    "navigation_action",
                    "map_write",
                    "gps_as_strong_fact_anchor",
                ],
                "output_type": "navigation_guidance_candidate",
            },
            {
                "chain_id": "task_midplatform",
                "allowed": [
                    "task_state_candidate",
                    "lifecycle_candidate",
                    "observation_requirement",
                    "guidance_candidate",
                    "speech_response_candidate",
                ],
                "forbidden": [
                    "task_state_commit",
                    "task_manager_runtime",
                    "tts",
                    "llm",
                    "memory_write",
                    "worldmodel_write",
                ],
                "output_type": "task_response_candidate",
            },
        ],
        **meta,
    }

    vision_plan = {
        "plan_id": "vision_minimal_execution_plan_v1",
        "allowed_inputs": ["controlled_frame_reference", "focus_candidate", "tracking_reference"],
        "outputs": ["visual_observation_candidate"],
        "execution_steps": [
            "resolve controlled frame reference (metadata-only)",
            "derive focus_candidate from task observation requirement",
            "attach tracking_reference if policy allows",
            "emit visual_observation_candidate (not_fact)",
        ],
        "camera_runtime_enabled_now": False,
        "vision_model_invoked_now": False,
        "candidate_only": True,
        **meta,
    }

    ocr_plan = {
        "plan_id": "ocr_minimal_execution_plan_v1",
        "inherits": "OCR-Mainline-Final-Closure-v1-001",
        "allowed_chain": ["OCRRequest", "ROI", "Evidence_Pack"],
        "outputs": ["ocr_request_candidate"],
        "execution_steps": [
            "if task requires text: build OCRRequest candidate",
            "define ROI reference without provider call",
            "plan Evidence Pack envelope without generation",
            "block provider invocation at gate",
        ],
        "ocr_provider_invoked_now": False,
        "fact_layer_write_now": False,
        "task_driven_auxiliary": True,
        **meta,
    }

    navigation_plan = {
        "plan_id": "navigation_minimal_execution_plan_v1",
        "allowed_outputs": [
            "guidance_candidate",
            "readonly_map_hint",
            "route_state_candidate",
        ],
        "execution_steps": [
            "consume visual_observation_candidate for safety context",
            "read readonly map hint (non-authoritative)",
            "emit guidance_candidate only",
            "block navigation_action at gate",
        ],
        "map_authority": "readonly_hint_only",
        "navigation_action_triggered_now": False,
        "candidate_only": True,
        **meta,
    }

    task_plan = {
        "plan_id": "task_midplatform_minimal_execution_plan_v1",
        "allowed_outputs": [
            "task_state_candidate",
            "lifecycle_candidate",
            "observation_requirement",
            "guidance_candidate",
            "speech_response_candidate",
        ],
        "execution_steps": [
            "derive task_observation_requirement from task scope",
            "route to OCR/Navigation candidates conditionally",
            "assemble task_response_candidate",
            "never commit task_state",
        ],
        "midplatform_note": "capabilities/midplatform + mid_platform coexist; medium risk registered only",
        "task_state_committed_now": False,
        "task_manager_committed_now": False,
        "midplatform_refactor_executed_now": False,
        **meta,
    }

    cross_chain = {
        "plan_id": "cross_chain_execution_flow_plan_v1",
        "flow_label": "candidate_only_minimal_loop",
        "steps": list(CROSS_CHAIN_STEPS),
        "invariants": [
            "candidate_only",
            "no_fact_layer_write",
            "no_external_action",
        ],
        "diagram": (
            "visual_observation_candidate → task_observation_requirement → "
            "ocr_request_candidate (if text) → navigation_guidance_candidate (if movement) → "
            "task_response_candidate"
        ),
        **meta,
    }

    gate_matrix = {
        "matrix_id": "execution_boundary_gate_matrix_v1",
        "gates": [
            {"gate_id": g, "status": "required", "default": "closed"} for g in EXECUTION_GATES
        ],
        "all_gates_closed_in_planning": True,
        **meta,
    }

    failure_fallback = {
        "plan_id": "failure_and_fallback_plan_v1",
        "rules": [
            {
                "condition": "missing_vision_input",
                "action": "hold",
                "fallback": "request_controlled_sample_later",
            },
            {
                "condition": "ocr_provider_required",
                "action": "blocked",
                "fallback": "defer_until_ocr_runtime_phase",
            },
            {
                "condition": "navigation_action_required",
                "action": "candidate_only",
                "fallback": "no_action_execute",
            },
            {
                "condition": "task_commit_required",
                "action": "blocked",
                "fallback": "defer_until_task_runtime_phase",
            },
            {
                "condition": "midplatform_ambiguity",
                "action": "defer",
                "fallback": "Phase-Midplatform-Structure-Cleanup-Planning-v1-001",
            },
            {
                "condition": "user_facing_speech_required",
                "action": "defer",
                "fallback": "Phase-Voice-Interaction-Runtime-Integration-Planning-v1-001",
            },
        ],
        **meta,
    }

    dryrun_plan = {
        "plan_id": "minimal_execution_dryrun_plan_v1",
        "next_phase": NEXT_PHASE,
        "dryrun_goals": [
            "simulate cross-chain candidate flow",
            "verify execution gates consumable",
            "no runtime enabled",
            "no fact layer write",
            "no user-facing output",
        ],
        "inputs_required": [
            "minimal_execution_scope_matrix_v1.json",
            "cross_chain_execution_flow_plan_v1.json",
            "execution_boundary_gate_matrix_v1.json",
        ],
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    readiness = {
        "decision_id": "minimal_recovery_execution_planning_readiness_decision_v1",
        "final_decision": FINAL_DECISION if boundary_ok else "VISION_OCR_NAVIGATION_TASK_MINIMAL_RECOVERY_EXECUTION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "boundary_ok": boundary_ok,
        "upstream_blockers": blockers,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "cross_chain_candidate_only": True,
        "execution_gates_count": len(EXECUTION_GATES),
        **meta,
    }

    return {
        "minimal_recovery_execution_planning_policy": policy,
        "recovery_post_dryrun_review_input_review": input_review,
        "minimal_execution_scope_matrix": scope_matrix,
        "vision_minimal_execution_plan": vision_plan,
        "ocr_minimal_execution_plan": ocr_plan,
        "navigation_minimal_execution_plan": navigation_plan,
        "task_midplatform_minimal_execution_plan": task_plan,
        "cross_chain_execution_flow_plan": cross_chain,
        "execution_boundary_gate_matrix": gate_matrix,
        "failure_and_fallback_plan": failure_fallback,
        "minimal_execution_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "minimal_recovery_execution_planning_readiness_decision": readiness,
        "summary": summary,
    }
