# -*- coding: utf-8 -*-
"""Controlled Trial Authorization Harness Extraction Planning v1."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from capabilities.governance.controlled_trial_authorization_harness_v1 import (
    build_extraction_planning_artifacts,
    validate_vision_authorization_reference_roots,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Controlled-Trial-Authorization-Harness-Extraction-Planning-v1-001"
PLANNING_SCOPE = "controlled_trial_authorization_harness_extraction_planning_only"
SOURCE_CHAIN = "controlled_trial_authorization_harness_extraction_planning_v1"

FINAL_DECISION = "CONTROLLED_TRIAL_AUTHORIZATION_HARNESS_EXTRACTION_PLANNING_READY_FOR_VALIDATION_CLOSURE"
NEXT_PHASE = "Phase-Controlled-Trial-Authorization-Harness-Validation-Closure-v1-001"


def _boundary_meta() -> Dict[str, Any]:
    return {
        "controlled_trial_authorization_harness_extraction_planning_only": True,
        "authorization_harness_generated_now": False,
        "authorization_harness_enforced_globally_now": False,
        "request_artifact_generated_now": False,
        "request_sent_now": False,
        "grant_issued_now": False,
        "execution_window_opened_now": False,
        "controlled_trial_started_now": False,
        "trial_execution_authorized_now": False,
        "authorization_request_artifact_generated_now": False,
        "authorization_request_sent_now": False,
        "execution_authorization_granted_now": False,
        "runtime_enabled_now": False,
        "live_camera_enabled_now": False,
        "vision_model_invoked_now": False,
        "ocr_provider_invoked_now": False,
        "navigation_action_triggered_now": False,
        "task_state_committed_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "user_facing_output_generated_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _is_workspace_fallback(path: Path) -> bool:
    return "Luna-Workspace-Min" in str(path)


def run_controlled_trial_authorization_harness_extraction_planning_v1(
    *,
    vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_root: str,
    vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_root: str,
    vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_root: str,
    planning_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    auth_plan_root = Path(
        vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_root
    ).expanduser().resolve()
    auth_dryrun_root = Path(
        vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_root
    ).expanduser().resolve()
    request_plan_root = Path(
        vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_root
    ).expanduser().resolve()

    plan_out = (
        Path(planning_output_root).expanduser().resolve()
        if planning_output_root
        else auth_plan_root.parent / "controlled_trial_authorization_harness_extraction_planning"
    )

    reference_roots = {
        "authorization_planning": str(auth_plan_root),
        "authorization_dryrun_and_review": str(auth_dryrun_root),
        "request_planning": str(request_plan_root),
    }

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(auth_plan_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "phase": PHASE_ID,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "reference_roots": reference_roots,
        "extraction_planning_output_root": str(plan_out),
    }

    blockers, _ctx = validate_vision_authorization_reference_roots(
        authorization_planning_root=auth_plan_root,
        authorization_dryrun_and_review_root=auth_dryrun_root,
        request_planning_root=request_plan_root,
    )
    boundary_ok = len(blockers) == 0

    artifacts = build_extraction_planning_artifacts(
        meta=meta,
        reference_roots=reference_roots,
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
        "controlled_trial_authorization_harness_extraction_policy": artifacts["extraction_policy"],
        "reusable_authorization_lifecycle_contract": artifacts["lifecycle_contract"],
        "authorization_config_schema_planning": artifacts["config_schema"],
        "authorization_scope_contract_planning": artifacts["scope_contract"],
        "allowlist_blocklist_contract_planning": artifacts["allowlist_blocklist_contract"],
        "pre_execution_gate_contract_planning": artifacts["gate_contract"],
        "execution_window_contract_planning": artifacts["window_contract"],
        "abort_condition_contract_planning": artifacts["abort_contract"],
        "output_contract_binding_planning": artifacts["output_contract"],
        "request_lifecycle_contract_planning": artifacts["request_lifecycle_contract"],
        "grant_lifecycle_contract_planning": artifacts["grant_lifecycle_contract"],
        "post_execution_review_contract_planning": artifacts["post_review_contract"],
        "future_trial_authorization_adoption_matrix": artifacts["adoption_matrix"],
        "anti_recursion_rules_for_authorization_trials": artifacts["anti_recursion"],
        "controlled_trial_authorization_harness_readiness_decision": artifacts["readiness"],
        "summary": summary,
    }
