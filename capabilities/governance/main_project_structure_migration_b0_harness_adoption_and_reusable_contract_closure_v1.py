# -*- coding: utf-8 -*-
"""Main Project Structure Migration B0 Harness Adoption and Reusable Contract Closure v1.

Closure-only: compress the chain and freeze the reusable Batch Preflight Harness contract as the
long-term migration validation engine.

This phase merges:
- B0 harness adoption dry-run review (credibility audit)
- Reusable harness contract freeze
- Future batch usage guide + batch_config template

STRICT: no formal harness generation/enforcement/runtime integration, no preflight execution,
no migration/arming/file-op, no verifier/template modification, no old phase deletion/deprecation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-and-Reusable-Contract-Closure-v1-001"
CLOSURE_SCOPE = "main_project_structure_migration_b0_harness_adoption_and_reusable_contract_closure_only"
SOURCE_CHAIN = "main_project_structure_migration_b0_harness_adoption_and_reusable_contract_closure_v1"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_HARNESS_ADOPTION_AND_REUSABLE_CONTRACT_CLOSED_READY_FOR_B0_PREFLIGHT_VIA_HARNESS"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-B0-Preflight-Via-Harness-v1-001"

UPSTREAM_SPECS: Tuple[Tuple[str, str, str], ...] = (
    (
        "batch_preflight_harness_extraction_post_review_root",
        "Phase-Main-Project-Structure-Migration-Batch-Preflight-Harness-Extraction-Post-DryRun-Review-v1-001",
        "MAIN_PROJECT_STRUCTURE_MIGRATION_BATCH_PREFLIGHT_HARNESS_EXTRACTION_POST_DRYRUN_REVIEW_READY_FOR_B0_HARNESS_ADOPTION_PLANNING",
    ),
    (
        "b0_harness_adoption_dryrun_root",
        "Phase-Main-Project-Structure-Migration-B0-Harness-Adoption-DryRun-v1-001",
        "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_HARNESS_ADOPTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW",
    ),
)

UPSTREAM_REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
)

REUSABLE_FIXED_CHECKS: Tuple[str, ...] = (
    "scope_check",
    "domain_isolation_check",
    "protected_guard_check",
    "eval_out_readonly_check",
    "file_operation_boundary_check",
    "manifest_requirement_check",
    "rollback_requirement_check",
    "verifier_rerun_requirement_check",
    "post_migration_test_requirement_check",
    "abort_condition_check",
    "workspace_fallback_check",
    "non_claims_check",
    "migration_refactor_opportunity_scan_check",
    "readiness_decision",
)

REQUIRED_CONFIG_FIELDS: Tuple[str, ...] = (
    "batch_id",
    "batch_domain",
    "candidate_paths",
    "allowed_operations",
    "blocked_operations",
    "protected_path_policy",
    "eval_out_policy",
    "before_manifest_requirement",
    "after_manifest_requirement",
    "rollback_route",
    "verifier_rerun_list",
    "post_migration_test_list",
    "abort_conditions",
    "workspace_fallback_policy",
    "non_claims",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "closure_only": True,
        "review_only": True,
        "selected_batch_id": "B0",
        "b0_only": True,
        "b1_b7_parameterized_consumers_only": True,
        "harness_generated_now": False,
        "harness_registered_now": False,
        "harness_enforced_now": False,
        "harness_runtime_integrated_now": False,
        "preflight_executed_now": False,
        "batch_config_applied_to_real_batch_now": False,
        "batch_armed_now": False,
        "batch_execution_started_now": False,
        "execution_window_opened_now": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_file_merge_executed": False,
        "actual_file_copy_executed": False,
        "actual_file_overwrite_executed": False,
        "actual_archive_executed": False,
        "verifier_rerun_executed_now": False,
        "rollback_rehearsal_executed_now": False,
        "post_migration_tests_executed_now": False,
        "eval_out_modified_now": False,
        "protected_asset_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "runtime_refactor_executed_now": False,
        "old_phase_deleted_now": False,
        "old_phase_deprecated_now": False,
        "verifier_modified_now": False,
        "phase_template_modified_now": False,
        "file_operation_executed_now": False,
        "real_migration_execution_allowed": False,
        "real_rehearsal_execution_allowed": False,
        "rollback_rehearsal_execution_allowed": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_path_mode": "repo_eval_out",
        "standard_eval_out_write_pending_on_local_repro": False,
        "runtime_invoked": False,
        "execution_committed": False,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "batch_arming_allowed": False,
        "success_claim_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_boundary_meta(), "closed_now": True, "executed_now": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_root(root_str: Optional[str], required_phase: str) -> Dict[str, Any]:
    root = Path(root_str).expanduser().resolve() if root_str else None
    missing: List[str] = []
    artifacts: Dict[str, Any] = {}
    if root:
        for name in UPSTREAM_REQUIRED_ARTIFACTS:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                artifacts[name] = payload
    loaded = bool(root) and not missing and (artifacts.get("summary.json") or {}).get("phase") == required_phase
    return {"root": root, "loaded": loaded, "missing": missing, "artifacts": artifacts}


def _is_workspace_fallback(root: Optional[Path]) -> bool:
    return bool(root) and "Luna-Workspace-Min" in str(root)


def run_main_project_structure_migration_b0_harness_adoption_and_reusable_contract_closure_v1(
    *,
    batch_preflight_harness_extraction_post_review_root: str,
    b0_harness_adoption_dryrun_root: str,
) -> Dict[str, Any]:
    blockers: List[str] = []

    upstream_loaded: Dict[str, bool] = {}
    upstream_summaries: Dict[str, Any] = {}
    upstream_verifiers: Dict[str, Any] = {}

    roots = {
        "batch_preflight_harness_extraction_post_review_root": batch_preflight_harness_extraction_post_review_root,
        "b0_harness_adoption_dryrun_root": b0_harness_adoption_dryrun_root,
    }

    source_path_mode = "workspace_fallback" if any(_is_workspace_fallback(Path(v).expanduser().resolve()) for v in roots.values() if v) else "repo_eval_out"
    standard_pending = source_path_mode == "workspace_fallback"
    meta = {**_boundary_meta(), "source_path_mode": source_path_mode, "standard_eval_out_write_pending_on_local_repro": standard_pending}

    for key, phase_required, final_required in UPSTREAM_SPECS:
        up = _load_root(roots[key], phase_required)
        upstream_loaded[key] = up["loaded"]
        if not up["loaded"]:
            blockers.append(f"upstream not loaded: {key} missing={up['missing']}")
            continue
        sm = up["artifacts"].get("summary.json") or {}
        vr = up["artifacts"].get("verifier_report.json") or {}
        upstream_summaries[key] = {"phase": sm.get("phase"), "final_decision": sm.get("final_decision"), "recommended_next_phase": sm.get("recommended_next_phase"), "boundary_ok": sm.get("boundary_ok")}
        upstream_verifiers[key] = {"verifier": vr.get("verifier"), "passed": vr.get("passed"), "check_count": vr.get("check_count")}
        if vr.get("verifier") != "GO" or vr.get("passed") is not True:
            blockers.append(f"upstream verifier must be GO: {key}")
        if sm.get("final_decision") != final_required:
            blockers.append(f"upstream final_decision mismatch: {key}")
        if sm.get("boundary_ok") is not True:
            blockers.append(f"upstream boundary_ok must be true: {key}")

    # Freeze reusable contract
    reusable_contract = {
        "harness_id": "main_project_structure_migration_batch_preflight_harness_v1",
        "contract_frozen_now": True,
        "fixed_checks": list(REUSABLE_FIXED_CHECKS),
        "batch_config_required_fields": list(REQUIRED_CONFIG_FIELDS),
        "forbidden_actions_during_migration": [
            "runtime_refactor",
            "formal_harness_generation",
            "formal_harness_enforcement",
            "runtime_integration",
            "old_phase_deletion",
            "verifier_modification",
            "template_modification",
        ],
        "b1_b7_policy": "parameterized_consumers_only; no repeated harness extraction/adoption chains",
        **meta,
    }

    # Usage guide + template (as artifacts; do not implement runtime engine here)
    usage_guide = {
        "guide_id": "batch_preflight_harness_usage_guide_v1",
        "how_to_use": [
            "Write batch_config JSON following required fields.",
            "Run BatchPreflightHarness.run(batch_config) in preflight-only mode (no file-op).",
            "If preflight passes, proceed to controlled execution planning for that batch.",
        ],
        "do_not_do": [
            "Do not generate a new harness extraction/adoption chain for each batch.",
            "Do not refactor runtime during migration phases.",
        ],
        "outputs_min": [
            "batch_config",
            "preflight_result",
            "migration_refactor_opportunity_scan",
            "final_batch_readiness_decision",
        ],
        **meta,
    }

    batch_config_template = {
        "template_id": "batch_config_template_v1",
        "template": {
            "batch_id": "<BATCH_ID>",
            "batch_domain": "<DOMAIN>",
            "candidate_paths": ["<PATH_1>", "<PATH_2>"],
            "allowed_operations": ["move", "rename"],
            "blocked_operations": ["delete", "overwrite", "merge", "copy"],
            "protected_path_policy": {"blocked": ["protected/**", "**/protected/**"]},
            "eval_out_policy": {"write_allowed": False, "mode": "readonly"},
            "before_manifest_requirement": {"required": True},
            "after_manifest_requirement": {"required": True},
            "rollback_route": {"route_id": "<ROUTE_ID>", "rehearsal_required": True},
            "verifier_rerun_list": ["<VERIFY_MODULE>"],
            "post_migration_test_list": ["<TEST_ID>"],
            "abort_conditions": ["<ABORT_CONDITION>"],
            "workspace_fallback_policy": {"enabled": True},
            "non_claims": ["<NON_CLAIM_TEXT>"],
        },
        "notes": ["This is a template only; not applied to any real batch now."],
        **meta,
    }

    # Hard rules (stop-loss)
    anti_recursion_rules = {
        "rule_id": "no_repeated_harness_chains_v1",
        "forbidden_future_patterns": [
            "B1–B7 Harness Extraction chain regeneration",
            "B1–B7 Adoption chain regeneration",
            "batch-specific authorization dry-run/review long chains duplicating preflight checks",
        ],
        "allowed_per_batch_outputs": [
            "batch_config",
            "preflight_result",
            "execution_result",
            "post_migration_review",
        ],
        "principles": [
            "能参数化的，不复制。",
            "能抽成 helper 的，不重复写 runner / verifier。",
            "能变成 harness 的，不再生成长链 phase。",
            "迁移只负责结构稳定，不顺手改业务逻辑。",
        ],
        **meta,
    }

    # Review B0 adoption dryrun credibility at closure time (lightweight)
    b0_review_pass = upstream_loaded.get("b0_harness_adoption_dryrun_root") is True and not any(
        "b0_harness_adoption_dryrun_root" in b for b in blockers
    )

    non_claims = [
        "Closure GO ≠ formal harness generated",
        "Closure GO ≠ harness enforced",
        "Closure GO ≠ runtime integrated",
        "Closure GO ≠ B0 preflight executed",
        "Closure GO ≠ B0 migration executed",
        "Reusable contract frozen ≠ runtime refactor allowed",
        "Usage guide generated ≠ batch_config applied to real batch",
        "Anti-recursion rules ≠ old phase deletion",
        "workspace_fallback GO ≠ standard _eval_out already written",
    ]

    boundary_ok = not blockers

    policy = _row(
        phase_id=PHASE_ID,
        closure_scope=CLOSURE_SCOPE,
        source_path_mode=source_path_mode,
        standard_eval_out_write_pending_on_local_repro=standard_pending,
    )

    input_review = {
        "upstream_loaded": upstream_loaded,
        "upstream_summaries": upstream_summaries,
        "upstream_verifiers": upstream_verifiers,
        "b0_adoption_dryrun_review_pass": b0_review_pass,
        "all_pass": boundary_ok,
        "blockers": blockers,
        **meta,
    }

    non_claims_register = {
        "rows": [_row(non_claim_id=f"NC_B0_HARNESS_CLOSURE_{i+1:02d}", text=t, non_claim_pass=True) for i, t in enumerate(non_claims)],
        "row_count": len(non_claims),
        "all_pass": True,
        **meta,
    }

    readiness = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_HARNESS_ADOPTION_AND_REUSABLE_CONTRACT_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_b0_preflight_via_harness": boundary_ok,
        "ready_for_b1_b7_parameterized_consumers": boundary_ok,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "closure_only": True,
        "review_only": True,
        "selected_batch_id": "B0",
        "b0_only": True,
        "b1_b7_parameterized_consumers_only": True,
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": standard_pending,
        "upstream_loaded": upstream_loaded,
        "b0_adoption_dryrun_review_pass": b0_review_pass,
        "reusable_contract_frozen_now": True,
        "usage_guide_generated_now": True,
        "batch_config_template_generated_now": True,
        "anti_recursion_rules_frozen_now": True,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_B0_HARNESS_ADOPTION_AND_REUSABLE_CONTRACT_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **meta,
    }

    return {
        "summary": summary,
        "b0_harness_adoption_and_reusable_contract_closure_policy": policy,
        "b0_harness_adoption_and_reusable_contract_closure_input_review": input_review,
        "reusable_batch_preflight_harness_contract_closure": reusable_contract,
        "future_batch_usage_guide": usage_guide,
        "batch_config_template": batch_config_template,
        "anti_recursion_rules_freeze": anti_recursion_rules,
        "b0_harness_adoption_closure_non_claims_register": non_claims_register,
        "b0_harness_adoption_and_reusable_contract_closure_readiness_decision": readiness,
    }

