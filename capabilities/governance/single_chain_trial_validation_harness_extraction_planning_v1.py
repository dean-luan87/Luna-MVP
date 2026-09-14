# -*- coding: utf-8 -*-
"""Single-Chain Trial Validation Harness Extraction Planning v1."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.single_chain_trial_validation_harness_v1 import (
    build_extraction_planning_artifacts,
    validate_limited_runtime_post_dryrun_review,
)

PHASE_ID = "Phase-Single-Chain-Trial-Validation-Harness-Extraction-Planning-v1-001"
PLANNING_SCOPE = "single_chain_trial_validation_harness_extraction_planning_only"
SOURCE_CHAIN = "single_chain_trial_validation_harness_extraction_planning_v1"

UPSTREAM_PHASE = "Phase-Vision-OCR-Navigation-Task-Limited-Runtime-Trial-Post-DryRun-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "VISION_OCR_NAVIGATION_TASK_LIMITED_RUNTIME_TRIAL_POST_DRYRUN_REVIEW_READY_FOR_SINGLE_CHAIN_VISION_SAMPLE_FRAME_TRIAL_PLANNING"
)
UPSTREAM_NEXT_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Limited-Runtime-Trial-Planning-v1-001"


def _boundary_meta() -> Dict[str, Any]:
    return {
        "single_chain_trial_validation_harness_extraction_planning_only": True,
        "harness_generated_now": False,
        "harness_enforced_now": False,
        "chain_trial_started_now": False,
        "runtime_enabled_now": False,
        "live_camera_enabled_now": False,
        "ocr_provider_invoked_now": False,
        "navigation_action_triggered_now": False,
        "task_state_committed_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "tts_invoked_now": False,
        "llm_invoked_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _is_workspace_fallback(path: Path) -> bool:
    return "Luna-Workspace-Min" in str(path)


def run_single_chain_trial_validation_harness_extraction_planning_v1(
    *,
    vision_ocr_navigation_task_limited_runtime_trial_post_dryrun_review_root: str,
    vision_ocr_navigation_task_limited_runtime_trial_dryrun_root: Optional[str] = None,
    vision_ocr_navigation_task_controlled_trial_plan_and_dryrun_root: Optional[str] = None,
) -> Dict[str, Any]:
    review_root = Path(
        vision_ocr_navigation_task_limited_runtime_trial_post_dryrun_review_root
    ).expanduser().resolve()
    dryrun_root = (
        Path(vision_ocr_navigation_task_limited_runtime_trial_dryrun_root).expanduser().resolve()
        if vision_ocr_navigation_task_limited_runtime_trial_dryrun_root
        else review_root.parent / "vision_ocr_navigation_task_limited_runtime_trial_dryrun"
    )
    plan_dryrun_root = (
        Path(vision_ocr_navigation_task_controlled_trial_plan_and_dryrun_root).expanduser().resolve()
        if vision_ocr_navigation_task_controlled_trial_plan_and_dryrun_root
        else review_root.parent / "vision_ocr_navigation_task_controlled_trial_plan_and_dryrun"
    )

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(review_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "reference_roots": {
            "post_dryrun_review": str(review_root),
            "limited_runtime_dryrun": str(dryrun_root),
            "controlled_trial_plan_and_dryrun": str(plan_dryrun_root),
        },
    }

    blockers, _ctx = validate_limited_runtime_post_dryrun_review(
        review_root,
        upstream_phase=UPSTREAM_PHASE,
        upstream_required_final=UPSTREAM_REQUIRED_FINAL,
        upstream_next_phase=UPSTREAM_NEXT_PHASE,
    )
    boundary_ok = len(blockers) == 0

    artifacts = build_extraction_planning_artifacts(
        meta=meta,
        upstream_roots=meta["reference_roots"],
        boundary_ok=boundary_ok,
    )

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": artifacts["readiness"]["final_decision"],
        "recommended_next_phase": artifacts["readiness"]["recommended_next_phase"],
        **meta,
    }

    return {
        "single_chain_trial_validation_harness_extraction_policy": artifacts["extraction_policy"],
        "reusable_single_chain_trial_validation_contract": artifacts["contract"],
        "chain_config_schema_planning": artifacts["chain_config_schema"],
        "reusable_gate_library_planning": artifacts["gate_library"],
        "reusable_stop_condition_library_planning": artifacts["stop_library"],
        "reusable_flow_contract_planning": artifacts["flow_contract"],
        "reusable_candidate_output_contract_planning": artifacts["output_contract_plan"],
        "future_chain_adoption_matrix": artifacts["adoption_matrix"],
        "anti_recursion_rules_for_single_chain_trials": artifacts["anti_recursion"],
        "single_chain_harness_extraction_readiness_decision": artifacts["readiness"],
        "summary": summary,
    }
