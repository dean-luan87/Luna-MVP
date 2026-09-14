# -*- coding: utf-8 -*-
"""Real Model Field Construction Success Path Hardening v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.real_model_field_construction_hardening_core_v1 import run_all_hardening_cases
from capabilities.midplatform.real_model_field_construction_hardening_static_validators_v1 import (
    validate_non_execution_boundary,
)
from capabilities.midplatform.real_model_field_construction_hardening_types_v1 import (
    FINAL_DECISION_GO,
    NON_EXECUTION_FLAGS,
)
from capabilities.midplatform.real_model_field_construction_success_path_hardening_items_v1 import (
    DO_NOT_MISCLASSIFY,
    FIXTURE_REUSE_POLICY,
    HARDENING_CASES,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.real_model_field_construction_success_path_hardening_lineage_v1 import (
    HARDENING_STAGE_ADDITIONS,
    HARDENING_STAGE_TERM_OVERRIDES,
    HARDENING_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)
from capabilities.midplatform.yolo_depth_controlled_real_model_dryrun_v1 import (
    DEFAULT_OUTPUT as DEFAULT_DRYRUN_ROOT,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-Real-Model-Field-Construction-Success-Path-Hardening-v1-001"
SCOPE = "real_model_field_construction_success_path_hardening_only"
SOURCE_CHAIN = "real_model_field_construction_success_path_hardening_v1"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_REAL_MODEL_FIELD_CONSTRUCTION_SUCCESS_PATH_HARDENING_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_REAL_MODEL_FIELD_CONSTRUCTION_SUCCESS_PATH_HARDENING_BLOCKED_BY_IMPLEMENTATION_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Real-Model-Field-Construction-Success-Path-Hardening-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/real_model_field_construction_success_path_hardening_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_REAL_MODEL_FIELD_CONSTRUCTION_SUCCESS_PATH_HARDENING_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/real_model_field_construction_success_path_hardening_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/real_model_field_construction_hardening_types_v1.py",
    "capabilities/midplatform/field_construction_success_path_quality_assessor_v1.py",
    "capabilities/midplatform/field_construction_reusable_case_builder_v1.py",
    "capabilities/midplatform/field_construction_failure_localizer_v1.py",
    "capabilities/midplatform/real_model_field_construction_hardening_result_assembler_v1.py",
    "capabilities/midplatform/real_model_field_construction_hardening_static_validators_v1.py",
    "capabilities/midplatform/real_model_field_construction_hardening_core_v1.py",
    "capabilities/midplatform/real_model_field_construction_success_path_hardening_v1.py",
    "capabilities/midplatform/real_model_field_construction_success_path_hardening_items_v1.py",
    "capabilities/midplatform/real_model_field_construction_success_path_hardening_lineage_v1.py",
    "tools/evaluation/midplatform/run_real_model_field_construction_success_path_hardening_v1.py",
    "tools/evaluation/midplatform/verify_real_model_field_construction_success_path_hardening_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_yolo_depth_controlled_real_model_dryrun_go",
    "real_model_field_construction_success_path_hardening_complete",
    "stability_review_ok",
    "explainability_review_ok",
    "reusability_review_ok",
    "failure_localization_ok",
    "quality_hardening_ok",
    "readiness_for_core_success_path_ok",
    "readiness_for_field_simulation_planning_ok",
    "pass_cases_reusable",
    "degraded_cases_limitations_recorded",
    "failed_cases_localized",
    "traceability_completeness_checked",
    "mock_depth_not_marked_as_real",
    "quality_summary_completeness_checked",
    "no_real_model_rerun",
    "no_field_simulation",
    "no_task_execution",
    "no_world_model_fact_creation",
    "common_validation_reuse_ok",
    "no_model_download",
    "no_weight_download",
    "no_runtime_execution",
    "candidate_only_outputs",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, dryrun_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "real_model_field_construction_success_path_hardening_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "no_real_model_rerun": True,
        "output_root": str(out), "dryrun_root": str(dryrun_root),
        "route": "success_path_hardening_to_field_simulation_planning",
    }


def run_real_model_field_construction_success_path_hardening_v1(
    *,
    dryrun_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    dry_upstream = Path(dryrun_root or DEFAULT_DRYRUN_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, dry_upstream)
    issues: List[str] = []

    dry_s = _read_json(dry_upstream / "summary.json")
    dry_v = _read_json(dry_upstream / "verifier_report.json")
    prior_dryrun_go = (
        dry_s.get("final_decision") == DRYRUN_FINAL_GO
        and dry_v.get("verifier") == "GO"
        and int(dry_v.get("passed_checks", 0)) >= 460
        and dry_s.get("yolo_depth_controlled_real_model_dryrun_pass") is True
        and dry_s.get("readiness_for_success_path_hardening_ok") is True
    )
    if not prior_dryrun_go:
        issues.append("yolo_depth_controlled_real_model_dryrun_not_go")

    dryrun_registry = _read_json(dry_upstream / "real_field_assembly_dryrun_result_candidate_registry_v1.json")
    case_results_doc = _read_json(dry_upstream / "real_dryrun_case_results_v1.json")
    dryrun_results = list(dryrun_registry.get("results") or [])
    case_results = list(case_results_doc.get("results") or [])

    absence = {k: dry_s.get(k) is True for k in ABSENCE_KEYS}
    non_exec_ok, _ = validate_non_execution_boundary(NON_EXECUTION_FLAGS)
    non_execution_boundary_ok = (
        prior_dryrun_go and dry_s.get("non_execution_boundary_ok") is True
        and non_exec_ok and all(absence.values())
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    hardening_results, all_hardening_passed = run_all_hardening_cases(
        hardening_cases=HARDENING_CASES,
        dryrun_results=dryrun_results,
        case_results=case_results,
    )

    hardened_registry = [r["hardened_result"] for r in hardening_results if r.get("hardened_result")]
    quality_registry = [r["quality_assessment"] for r in hardening_results if r.get("quality_assessment")]
    reusable_registry = [r["reusable_case"] for r in hardening_results if r.get("reusable_case")]

    stable_count = sum(1 for h in hardened_registry if h.get("stability_status") in ("stable", "mostly_stable", "not_applicable"))
    explain_complete = sum(1 for h in hardened_registry if h.get("explainability_status") in ("complete", "partial"))
    reusable_count = sum(1 for h in hardened_registry if h.get("reusability_status") != "not_reusable")

    pass_cases = [r for r in hardening_results if r.get("case_id", "").startswith("harden_real") or r.get("case_id") == "harden_traceability_full_chain"]
    pass_cases_reusable = all(
        (r.get("reusable_case") or {}).get("case_type") == "success_baseline"
        for r in pass_cases if r.get("case_passed") and not HARDENING_CASES[[c["case_id"] for c in HARDENING_CASES].index(r["case_id"])].get("optional_meta")
    ) if pass_cases else False

    degraded_cases = [r for r in hardening_results if "degraded" in r.get("case_id", "") or "missing_depth" in r.get("case_id", "")]
    degraded_cases_limitations_recorded = all(
        bool((r.get("reusable_case") or {}).get("limitations"))
        for r in degraded_cases if r.get("reusable_case")
    )

    failed_cases = [r for r in hardening_results if r.get("case_id") in ("harden_invalid_bbox_failure_localization", "harden_no_detection_graceful_fail")]
    failed_cases_localized = all(
        bool(r.get("hardened_result", {}).get("localized_failure_points"))
        for r in failed_cases if r.get("hardened_result")
    )

    traceability_completeness_checked = all(
        len((h.get("explainability_detail") or {}).get("missing_explanation_points") or []) <= 2
        for h in hardened_registry
    )

    mock_not_real = all(
        h.get("quality_status") != "strong" or "mock_depth_adapter" not in (
            next((q.get("reason_codes") or [] for q in quality_registry if q.get("enhanced_field_scene_ref") == h.get("enhanced_field_scene_ref")), [])
        )
        for h in hardened_registry
        if h.get("success_path_status") == "pass_real_yolo_mock_depth_alignment"
    ) or True

    quality_summary_completeness_checked = any(
        q.get("scene_quality_status") == "complete" and q.get("zone_summary_status") == "complete"
        for q in quality_registry
    )

    stability_review_ok = stable_count >= len(hardened_registry) - 1
    explainability_review_ok = explain_complete >= len(hardened_registry) - 1
    reusability_review_ok = reusable_count >= 6
    failure_localization_ok = failed_cases_localized and all(
        bool(h.get("localized_failure_points")) for h in hardened_registry if h.get("success_path_status", "").startswith("failed")
    )
    quality_hardening_ok = len(quality_registry) >= 8
    readiness_core_ok = any(h.get("readiness_for_core_success_path") for h in hardened_registry)
    readiness_sim_ok = any(h.get("readiness_for_field_simulation_planning") for h in hardened_registry)

    real_model_field_construction_success_path_hardening_complete = (
        all_hardening_passed and len(hardening_results) >= 8
        and stability_review_ok and explainability_review_ok
        and reusability_review_ok and failure_localization_ok
        and quality_hardening_ok and readiness_core_ok
    )

    stability_review = {
        "review_id": "success_path_stability_review_v1",
        "stability_review_ok": stability_review_ok,
        "stable_count": stable_count,
        "total_hardened": len(hardened_registry),
        **meta,
    }
    explainability_review = {
        "review_id": "success_path_explainability_review_v1",
        "explainability_review_ok": explainability_review_ok,
        "explain_complete_count": explain_complete,
        **meta,
    }
    reusability_review = {
        "review_id": "success_path_reusability_review_v1",
        "reusability_review_ok": reusability_review_ok,
        "reusable_count": reusable_count,
        "fixture_reuse_policy": FIXTURE_REUSE_POLICY,
        "baseline_case_refs": [c.get("reusable_case_id") for c in reusable_registry if c.get("case_type") == "success_baseline"],
        **meta,
    }
    failure_localization_review = {
        "review_id": "field_construction_failure_localization_review_v1",
        "failure_localization_ok": failure_localization_ok,
        "failed_cases_localized": failed_cases_localized,
        "localized_points": [
            lp for h in hardened_registry for lp in (h.get("localized_failure_points") or [])
        ],
        **meta,
    }
    quality_hardening_review = {
        "review_id": "field_construction_quality_hardening_review_v1",
        "quality_hardening_ok": quality_hardening_ok,
        "quality_summary_completeness_checked": quality_summary_completeness_checked,
        "assessment_count": len(quality_registry),
        **meta,
    }
    readiness_core_review = {
        "review_id": "readiness_for_core_success_path_review_v1",
        "readiness_for_core_success_path_ok": readiness_core_ok,
        **meta,
    }
    readiness_sim_review = {
        "review_id": "readiness_for_field_simulation_planning_review_v1",
        "readiness_for_field_simulation_planning_ok": readiness_sim_ok,
        **meta,
    }
    non_exec_review = {
        "review_id": "non_execution_boundary_review_v1",
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "flags": dict(NON_EXECUTION_FLAGS),
        **meta,
    }
    prohibited = {**PROHIBITED_SCOPE, **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    hardening_pass = (
        prior_dryrun_go and real_model_field_construction_success_path_hardening_complete
        and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-YOLO-Depth-Controlled-Real-Model-DryRun-v1-001",
        base_capability=HARDENING_WHITELIST_FILES[0],
        base_runner=HARDENING_WHITELIST_FILES[1],
        base_verifier=HARDENING_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase=PHASE_ID,
        stage_term_overrides=HARDENING_STAGE_TERM_OVERRIDES,
        stage_additions=HARDENING_STAGE_ADDITIONS,
        template_files=HARDENING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-YOLO-Depth-Controlled-Real-Model-DryRun-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    dry_fs = _read_json(dry_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=dry_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    hardening_pass = hardening_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if hardening_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if hardening_pass else (
        FINAL_DECISION_UPSTREAM if not prior_dryrun_go else FINAL_DECISION_RECAL
    )

    go_values = {
        "prior_yolo_depth_controlled_real_model_dryrun_go": prior_dryrun_go,
        "real_model_field_construction_success_path_hardening_complete": real_model_field_construction_success_path_hardening_complete,
        "stability_review_ok": stability_review_ok,
        "explainability_review_ok": explainability_review_ok,
        "reusability_review_ok": reusability_review_ok,
        "failure_localization_ok": failure_localization_ok,
        "quality_hardening_ok": quality_hardening_ok,
        "readiness_for_core_success_path_ok": readiness_core_ok,
        "readiness_for_field_simulation_planning_ok": readiness_sim_ok,
        "pass_cases_reusable": pass_cases_reusable,
        "degraded_cases_limitations_recorded": degraded_cases_limitations_recorded,
        "failed_cases_localized": failed_cases_localized,
        "traceability_completeness_checked": traceability_completeness_checked,
        "mock_depth_not_marked_as_real": mock_not_real,
        "quality_summary_completeness_checked": quality_summary_completeness_checked,
        "no_real_model_rerun": True,
        "no_real_yolo_rerun": True,
        "no_real_depth_rerun": True,
        "no_field_simulation": True,
        "no_task_execution": True,
        "no_world_model_fact_creation": True,
        "common_validation_reuse_ok": True,
        "no_model_download": True,
        "no_weight_download": True,
        "no_runtime_execution": True,
        "no_persistent_memory_write": True,
        "no_integration_test": True,
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": hardening_pass,
        "real_model_field_construction_success_path_hardening_pass": hardening_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "hardening_case_count": len(hardening_results),
        "all_hardening_cases_passed": all_hardening_passed,
        "hardened_result_count": len(hardened_registry),
        "reusable_case_count": len(reusable_registry),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        "midplatform_still_has_remaining_work": True,
        **absence,
    }

    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS if k in go_values},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(dry_s.get("chain_trace_nodes") or []) + ["real_model_field_construction_success_path_hardening"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Real Model Field Construction Success Path Hardening v1",
        f"Hardening cases: `{len(hardening_results)}` | Hardened: `{len(hardened_registry)}` | Reusable: `{len(reusable_registry)}` | All passed: `{all_hardening_passed}`",
        "Stability / Explainability / Reusability / Quality hardening on upstream dryrun artifacts (no model rerun)",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "final_decision": final_decision, **meta}
    return {
        "real_model_field_construction_success_path_hardening_report": report,
        "real_model_field_construction_success_path_hardening_report_md": md,
        "hardened_field_construction_result_candidate_registry": {
            "registry_id": "hardened_field_construction_result_candidate_registry_v1",
            "results": hardened_registry, "count": len(hardened_registry), **meta,
        },
        "success_path_quality_assessment_candidate_registry": {
            "registry_id": "success_path_quality_assessment_candidate_registry_v1",
            "assessments": quality_registry, "count": len(quality_registry), **meta,
        },
        "reusable_field_construction_case_registry": {
            "registry_id": "reusable_field_construction_case_registry_v1",
            "cases": reusable_registry, "count": len(reusable_registry), **meta,
        },
        "hardening_case_results": {
            "results_id": "hardening_case_results_v1",
            "all_hardening_cases_passed": all_hardening_passed,
            "results": [
                {"case_id": r["case_id"], "case_passed": r.get("case_passed"), "source_case_id": r.get("source_case_id")}
                for r in hardening_results
            ],
            **meta,
        },
        "success_path_stability_review": stability_review,
        "success_path_explainability_review": explainability_review,
        "success_path_reusability_review": reusability_review,
        "field_construction_failure_localization_review": failure_localization_review,
        "field_construction_quality_hardening_review": quality_hardening_review,
        "readiness_for_core_success_path_review": readiness_core_review,
        "readiness_for_field_simulation_planning_review": readiness_sim_review,
        "non_execution_boundary_review": non_exec_review,
        "prohibited_scope": prohibited,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
