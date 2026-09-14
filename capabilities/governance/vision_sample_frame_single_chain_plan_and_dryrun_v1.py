# -*- coding: utf-8 -*-
"""Vision Sample Frame Single-Chain Plan+DryRun v1 via SingleChainTrialValidationHarness."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.single_chain_trial_validation_harness_v1 import (
    build_vision_sample_frame_chain_config,
    run_single_chain_trial_plan_and_dryrun,
    validate_limited_runtime_post_dryrun_review,
)

PHASE_ID = "Phase-Vision-Sample-Frame-Single-Chain-Limited-Runtime-Trial-PlanAndDryRun-v1-001"
SCOPE = "vision_sample_frame_single_chain_plan_and_dryrun_only"
SOURCE_CHAIN = "vision_sample_frame_single_chain_plan_and_dryrun_v1"

UPSTREAM_PHASE = "Phase-Vision-OCR-Navigation-Task-Limited-Runtime-Trial-Post-DryRun-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "VISION_OCR_NAVIGATION_TASK_LIMITED_RUNTIME_TRIAL_POST_DRYRUN_REVIEW_READY_FOR_SINGLE_CHAIN_VISION_SAMPLE_FRAME_TRIAL_PLANNING"
)
UPSTREAM_NEXT_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Limited-Runtime-Trial-Planning-v1-001"


def _boundary_meta() -> Dict[str, Any]:
    return {
        "vision_sample_frame_single_chain_plan_and_dryrun_only": True,
        "simulated": True,
        "single_chain_trial_started_now": False,
        "limited_runtime_trial_started_now": False,
        "runtime_enabled_now": False,
        "live_runtime_enabled_now": False,
        "live_camera_enabled_now": False,
        "camera_runtime_enabled_now": False,
        "frame_capture_executed_now": False,
        "new_image_read_executed_now": False,
        "arbitrary_image_read_executed_now": False,
        "vision_model_invoked_now": False,
        "visual_fact_generated_now": False,
        "ocr_provider_invoked_now": False,
        "navigation_action_triggered_now": False,
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
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _is_workspace_fallback(path: Path) -> bool:
    return "Luna-Workspace-Min" in str(path)


def run_vision_sample_frame_single_chain_plan_and_dryrun_v1(
    *,
    vision_ocr_navigation_task_limited_runtime_trial_post_dryrun_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    review_root = Path(
        vision_ocr_navigation_task_limited_runtime_trial_post_dryrun_review_root
    ).expanduser().resolve()

    out_root = (
        Path(output_root).expanduser().resolve()
        if output_root
        else review_root.parent / "vision_sample_frame_single_chain_plan_and_dryrun"
    )

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(review_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "phase": PHASE_ID,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_post_dryrun_review_root": str(review_root),
        "output_root": str(out_root),
    }

    blockers, ctx = validate_limited_runtime_post_dryrun_review(
        review_root,
        upstream_phase=UPSTREAM_PHASE,
        upstream_required_final=UPSTREAM_REQUIRED_FINAL,
        upstream_next_phase=UPSTREAM_NEXT_PHASE,
    )

    chain_config = build_vision_sample_frame_chain_config(source_chain=SOURCE_CHAIN)
    harness_result = run_single_chain_trial_plan_and_dryrun(
        chain_config=chain_config,
        boundary_meta=meta,
        upstream_blockers=blockers,
        policy_id="vision_sample_frame_plan_and_dryrun_policy_v1",
        scope_label=SCOPE,
    )

    input_review = {
        "review_id": "input_review_v1",
        "upstream_root": str(review_root),
        "upstream_verifier": ctx["review_vr"].get("verifier"),
        "upstream_final_decision": ctx["review_sm"].get("final_decision"),
        "positive_flows_passed": ctx["positive"].get("positive_flows_passed"),
        "blocked_flows_enforced": ctx["blocked"].get("blocked_flows_enforced"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "plan_and_dryrun_scope": SCOPE,
        **harness_result["summary"],
        **meta,
    }

    return {
        "vision_sample_frame_plan_and_dryrun_policy": harness_result["policy"],
        "input_review": input_review,
        "vision_sample_frame_scope_and_source_policy": harness_result["scope_and_source"],
        "visual_observation_candidate_schema": harness_result["candidate_schema"],
        "vision_sample_frame_fixture_input_matrix": harness_result["fixture_matrix"],
        "vision_sample_frame_positive_flow_result": harness_result["positive_flow_result"],
        "vision_sample_frame_blocked_flow_result": harness_result["blocked_flow_result"],
        "vision_sample_frame_gate_result": harness_result["gate_result"],
        "vision_sample_frame_stop_condition_result": harness_result["stop_result"],
        "no_runtime_boundary_audit": harness_result["runtime_audit"],
        "vision_sample_frame_next_step_readiness_decision": harness_result["readiness"],
        "non_claims_register": harness_result["non_claims"],
        "summary": summary,
    }
