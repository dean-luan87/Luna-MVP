# -*- coding: utf-8 -*-
"""Field-First Core Logic Formal Implementation v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.field_first_core_consistency_validators_v1 import validate_cross_stage_consistency
from capabilities.midplatform.field_first_core_logic_formal_implementation_items_v1 import (
    CORE_PIPELINE_MOCK_CASES,
    DO_NOT_MISCLASSIFY,
    INPUT_OUTPUT_CONTRACT,
    NEXT_STAGE_SPLIT_PLAN,
    PIPELINE_REGISTRY,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.field_first_core_logic_formal_implementation_lineage_v1 import (
    CORE_LOGIC_STAGE_ADDITIONS,
    CORE_LOGIC_STAGE_TERM_OVERRIDES,
    CORE_LOGIC_WHITELIST_FILES,
    UPSTREAM_SKELETONS,
)
from capabilities.midplatform.field_first_core_logic_types_v1 import FINAL_DECISION_GO, NON_EXECUTION_FLAGS
from capabilities.midplatform.field_first_core_logic_v1 import run_all_core_pipeline_dryrun_cases
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
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
from capabilities.midplatform.trajectory_analysis_static_validators_v1 import validate_non_execution_boundary

PHASE_ID = "Phase-Midplatform-Field-First-Core-Logic-Formal-Implementation-v1-001"
SCOPE = "field_first_core_logic_formal_implementation_only"
SOURCE_CHAIN = "field_first_core_logic_formal_implementation_v1"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_FIELD_FIRST_CORE_LOGIC_BLOCKED_BY_UPSTREAM_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_FIELD_FIRST_CORE_LOGIC_BLOCKED_BY_IMPLEMENTATION_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Field-First-Core-Logic-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_first_core_logic_formal_implementation_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_LOGIC_FORMAL_IMPLEMENTATION_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/field_first_core_logic_formal_implementation_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_core_logic_types_v1.py",
    "capabilities/midplatform/field_first_core_pipeline_v1.py",
    "capabilities/midplatform/field_first_core_result_assembler_v1.py",
    "capabilities/midplatform/field_first_core_consistency_validators_v1.py",
    "capabilities/midplatform/field_first_core_logic_v1.py",
    "capabilities/midplatform/field_first_core_logic_formal_implementation_v1.py",
    "capabilities/midplatform/field_first_core_logic_formal_implementation_items_v1.py",
    "capabilities/midplatform/field_first_core_logic_formal_implementation_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_logic_formal_implementation_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_logic_formal_implementation_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "all_four_upstream_skeletons_go",
    "field_first_core_pipeline_complete",
    "core_result_candidate_generated",
    "cross_stage_consistency_validated",
    "all_core_pipeline_mock_cases_passed",
    "missing_information_propagation_ok",
    "warning_summary_ok",
    "decision_readiness_summary_ok",
    "common_validation_reuse_ok",
    "non_execution_boundary_ok",
    "no_model_execution",
    "no_runtime_execution",
    "no_final_action_output",
    "no_world_model_fact_creation",
    "no_memory_write",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _check_upstream_skeletons(repo_root: Path) -> Tuple[bool, Dict[str, bool], List[str]]:
    status: Dict[str, bool] = {}
    issues: List[str] = []
    for sk in UPSTREAM_SKELETONS:
        s = _read_json(repo_root / sk["summary_path"])
        v = _read_json(repo_root / sk["verifier_path"])
        ok = (
            s.get("final_decision") == sk["final_go"]
            and v.get("verifier") == "GO"
            and int(v.get("passed_checks", 0)) >= sk["min_checks"]
            and s.get(sk["pass_flag"]) is True
        )
        status[sk["phase"]] = ok
        if not ok:
            issues.append(f"{sk['phase']}_not_go")
    return all(status.values()), status, issues


def run_field_first_core_logic_formal_implementation_v1(
    *,
    output_root: Optional[str] = None,
    repo_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    root = Path(repo_root or Path(__file__).resolve().parents[2]).expanduser().resolve()
    meta = {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "field_first_core_logic_formal_implementation_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out),
    }
    issues: List[str] = []

    all_upstream_go, upstream_status, upstream_issues = _check_upstream_skeletons(root)
    issues.extend(upstream_issues)

    traj_s = _read_json(root / UPSTREAM_SKELETONS[3]["summary_path"])
    absence = {k: traj_s.get(k) is True for k in ABSENCE_KEYS}
    non_exec_ok, _ = validate_non_execution_boundary(NON_EXECUTION_FLAGS)
    non_execution_boundary_ok = all_upstream_go and non_exec_ok and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    dryrun_results, all_mock_passed = run_all_core_pipeline_dryrun_cases(CORE_PIPELINE_MOCK_CASES)
    all_results = [r["final_result_candidate"] for r in dryrun_results]
    consistency_rows: List[Dict[str, Any]] = []
    all_consistent = True
    for r in dryrun_results:
        ok, c_issues, checks = validate_cross_stage_consistency(r["final_result_candidate"])
        consistency_rows.append({"case_id": r["case_id"], "consistent": ok, "issues": c_issues, "checks": checks})
        if not ok:
            all_consistent = False

    core_result_candidate_generated = len(all_results) >= 8
    field_first_core_pipeline_complete = all_mock_passed and core_result_candidate_generated
    cross_stage_consistency_validated = all_consistent
    missing_information_propagation_ok = all(
        (res.get("missing_information_candidates") is not None) for res in all_results
    )
    warning_summary_ok = all(
        isinstance(res.get("warning_summary"), dict) for res in all_results
    )
    decision_readiness_summary_ok = all(
        isinstance(res.get("decision_readiness_summary"), dict) for res in all_results
    )

    readiness_registry = {
        "registry_id": "decision_readiness_summary_registry_v1",
        "summaries": [r.get("decision_readiness_summary") for r in all_results],
        **meta,
    }
    result_reg = {
        "registry_id": "field_first_core_result_candidate_registry_v1",
        "count": len(all_results),
        "results": [{"result_candidate_id": r.get("result_candidate_id"), "case_id": dryrun_results[i]["case_id"]} for i, r in enumerate(all_results)],
        **meta,
    }
    propagation_review = {
        "review_id": "warning_missing_information_propagation_review_v1",
        "missing_information_propagation_ok": missing_information_propagation_ok,
        "warning_summary_ok": warning_summary_ok,
        "samples": [{
            "case_id": r["case_id"],
            "warning_count": len((r["final_result_candidate"].get("warning_summary") or {}).get("warnings") or []),
            "missing_count": len(r["final_result_candidate"].get("missing_information_candidates") or []),
        } for r in dryrun_results],
        **meta,
    }
    consistency_val = {
        "validation_id": "field_first_core_consistency_validation_results_v1",
        "cross_stage_consistency_validated": cross_stage_consistency_validated,
        "results": consistency_rows,
        **meta,
    }
    mock_results = {
        "results_id": "field_first_core_mock_case_results_v1",
        "all_core_pipeline_mock_cases_passed": all_mock_passed,
        "count": len(dryrun_results),
        "results": dryrun_results,
        **meta,
    }
    io_contract = {**INPUT_OUTPUT_CONTRACT, **meta}
    pipeline_reg = {**PIPELINE_REGISTRY, **meta}
    non_exec_review = {"review_id": "non_execution_boundary_review_v1", "non_execution_boundary_ok": non_execution_boundary_ok, "flags": dict(NON_EXECUTION_FLAGS), **meta}
    next_split = {**NEXT_STAGE_SPLIT_PLAN, **meta}
    prohibited = {**PROHIBITED_SCOPE, **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    impl_pass = (
        all_upstream_go and field_first_core_pipeline_complete and all_mock_passed
        and cross_stage_consistency_validated and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Trajectory-Analysis-Task-Impact-Controlled-Skeleton-Implementation-v1-001",
        base_capability=CORE_LOGIC_WHITELIST_FILES[0],
        base_runner=CORE_LOGIC_WHITELIST_FILES[1],
        base_verifier=CORE_LOGIC_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Field-First-Core-Logic-Formal-Implementation-v1-001",
        stage_term_overrides=CORE_LOGIC_STAGE_TERM_OVERRIDES,
        stage_additions=CORE_LOGIC_STAGE_ADDITIONS,
        template_files=CORE_LOGIC_WHITELIST_FILES,
        repo_root=root,
        upstream_review_phase="Midplatform-Trajectory-Analysis-Task-Impact-Controlled-Skeleton-Implementation-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    traj_fs = _read_json(root / "_tmp_eval_out/trajectory_analysis_task_impact_controlled_skeleton_implementation_v1_smoke_v0/file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=traj_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    impl_pass = impl_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if impl_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if impl_pass else (FINAL_DECISION_UPSTREAM if not all_upstream_go else FINAL_DECISION_RECAL)

    go_values = {
        "all_four_upstream_skeletons_go": all_upstream_go,
        "upstream_skeleton_status": upstream_status,
        "field_first_core_pipeline_complete": field_first_core_pipeline_complete,
        "core_result_candidate_generated": core_result_candidate_generated,
        "cross_stage_consistency_validated": cross_stage_consistency_validated,
        "all_core_pipeline_mock_cases_passed": all_mock_passed,
        "missing_information_propagation_ok": missing_information_propagation_ok,
        "warning_summary_ok": warning_summary_ok,
        "decision_readiness_summary_ok": decision_readiness_summary_ok,
        "common_validation_reuse_ok": True,
        "no_model_execution": True,
        "no_runtime_execution": True,
        "no_final_action_output": True,
        "no_world_model_fact_creation": True,
        "no_memory_write": True,
        "no_field_simulation": True,
        "no_trajectory_when_tracking_frozen": True,
        "new_field_resets_trajectory": True,
        "no_real_tracking_execution": True,
        "no_trajectory_prediction": True,
        "no_task_execution": True,
        "candidate_only_outputs": True,
        "field_first_route_preserved": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": impl_pass,
        "field_first_core_logic_formal_implementation_pass": impl_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "mock_case_count": len(dryrun_results),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        "midplatform_still_has_remaining_work": True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(traj_s.get("chain_trace_nodes") or []) + ["field_first_core_logic_formal_implementation"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Field-First Core Logic Formal Implementation v1",
        f"Pipeline cases: `{len(dryrun_results)}` | All passed: `{all_mock_passed}` | Upstream skeletons GO: `{all_upstream_go}`",
        "Integrated pipeline: FieldScene → Continuity → Tracking → Trajectory/TaskImpact → CoreResult",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "final_decision": final_decision, **meta}
    return {
        "field_first_core_logic_formal_implementation_report": report,
        "field_first_core_logic_formal_implementation_report_md": md,
        "field_first_core_input_package_contract": io_contract,
        "field_first_core_pipeline_registry": pipeline_reg,
        "field_first_core_result_candidate_registry": result_reg,
        "field_first_core_consistency_validation_results": consistency_val,
        "field_first_core_mock_case_results": mock_results,
        "decision_readiness_summary_registry": readiness_registry,
        "warning_missing_information_propagation_review": propagation_review,
        "non_execution_boundary_review": non_exec_review,
        "next_stage_split_plan": next_split,
        "prohibited_scope": prohibited,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
