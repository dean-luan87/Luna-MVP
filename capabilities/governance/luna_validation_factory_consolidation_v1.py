# -*- coding: utf-8 -*-
"""Luna Validation Factory Consolidation v1."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from capabilities.governance.luna_validation_factory_v1 import (
    build_factory_consolidation_artifacts,
    validate_consolidation_upstream,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Luna-Validation-Factory-Consolidation-v1-001"
CONSOLIDATION_SCOPE = "luna_validation_factory_consolidation_only"
SOURCE_CHAIN = "luna_validation_factory_consolidation_v1"

FINAL_DECISION = (
    "LUNA_VALIDATION_FACTORY_CONSOLIDATION_READY_FOR_VISION_SAMPLE_FRAME_AUTHORIZATION_VIA_HARNESS"
)
NEXT_PHASE = "Phase-Vision-Sample-Frame-Single-Chain-Controlled-Trial-Authorization-Via-Harness-v1-001"


def _boundary_meta() -> Dict[str, Any]:
    return {
        "luna_validation_factory_consolidation_only": True,
        "validation_factory_contract_generated_now": True,
        "validation_factory_runtime_enforced_now": False,
        "trial_execution_authorized_now": False,
        "request_sent_now": False,
        "grant_issued_now": False,
        "controlled_trial_started_now": False,
        "execution_window_opened_now": False,
        "runtime_enabled_now": False,
        "live_camera_enabled_now": False,
        "ocr_provider_invoked_now": False,
        "navigation_action_triggered_now": False,
        "task_state_committed_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "user_facing_output_generated_now": False,
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


def run_luna_validation_factory_consolidation_v1(
    *,
    main_project_structure_migration_final_closure_root: str,
    b0_harness_adoption_and_reusable_contract_closure_root: str,
    single_chain_trial_validation_harness_validation_closure_root: str,
    vision_sample_frame_single_chain_plan_and_dryrun_root: str,
    vision_sample_frame_single_chain_controlled_trial_dryrun_and_review_root: str,
    vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_root: str,
    vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_root: str,
    vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_root: str,
    consolidation_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    eval_base = Path(main_project_structure_migration_final_closure_root).expanduser().resolve().parent

    reference_roots = {
        "migration_final_closure": str(
            Path(main_project_structure_migration_final_closure_root).expanduser().resolve()
        ),
        "b0_harness_adoption_closure": str(
            Path(b0_harness_adoption_and_reusable_contract_closure_root).expanduser().resolve()
        ),
        "single_chain_harness_closure": str(
            Path(single_chain_trial_validation_harness_validation_closure_root).expanduser().resolve()
        ),
        "vision_plan_and_dryrun": str(
            Path(vision_sample_frame_single_chain_plan_and_dryrun_root).expanduser().resolve()
        ),
        "vision_controlled_trial_dryrun": str(
            Path(vision_sample_frame_single_chain_controlled_trial_dryrun_and_review_root).expanduser().resolve()
        ),
        "vision_auth_planning": str(
            Path(
                vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_root
            ).expanduser().resolve()
        ),
        "vision_auth_dryrun": str(
            Path(
                vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_root
            ).expanduser().resolve()
        ),
        "vision_request_planning": str(
            Path(
                vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_root
            ).expanduser().resolve()
        ),
    }

    out_root = (
        Path(consolidation_output_root).expanduser().resolve()
        if consolidation_output_root
        else eval_base / "luna_validation_factory_consolidation"
    )

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(eval_base) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "phase": PHASE_ID,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "consolidation_output_root": str(out_root),
        "eval_base": str(eval_base),
    }

    blockers, _ctx = validate_consolidation_upstream(reference_roots)
    boundary_ok = len(blockers) == 0

    artifacts = build_factory_consolidation_artifacts(
        meta=meta,
        reference_roots=reference_roots,
        boundary_ok=boundary_ok,
    )

    summary = {
        "phase": PHASE_ID,
        "consolidation_scope": CONSOLIDATION_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": artifacts["decision"]["final_decision"],
        "recommended_next_phase": artifacts["decision"]["recommended_next_phase"],
        "module_registry_count": len(artifacts["registry"]["modules"]),
        **meta,
    }

    return {
        "luna_validation_factory_consolidation_policy": artifacts["policy"],
        "validation_factory_module_registry": artifacts["registry"],
        "batch_preflight_harness_registry_review": artifacts["batch_review"],
        "single_chain_trial_validation_harness_registry_review": artifacts["single_chain_review"],
        "controlled_trial_authorization_harness_contract": artifacts["auth_harness_contract"],
        "candidate_output_contract": artifacts["candidate_contract"],
        "no_runtime_boundary_audit_contract": artifacts["no_runtime_contract"],
        "controlled_trial_post_execution_review_harness_contract": artifacts["post_review_contract"],
        "validation_factory_usage_guide": artifacts["usage_guide"],
        "validation_factory_anti_recursion_rules": artifacts["anti_recursion"],
        "validation_factory_future_adoption_matrix": artifacts["adoption_matrix"],
        "vision_sample_frame_integrated_consumer_review": artifacts["vision_integrated_review"],
        "validation_factory_non_claims_register": artifacts["non_claims"],
        "validation_factory_consolidation_decision": artifacts["decision"],
        "summary": summary,
    }
