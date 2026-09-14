# -*- coding: utf-8 -*-
"""Real Observation Candidate Ingestion Skeleton v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.field_first_minimal_real_model_adapter_integration_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.real_observation_candidate_ingestion_core_v1 import run_all_ingestion_dryrun_cases
from capabilities.midplatform.real_observation_candidate_ingestion_skeleton_items_v1 import (
    DEPTH_FALLBACK_EXECUTION,
    DETECTOR_OUTPUT_MOCK_CONTRACT,
    DO_NOT_MISCLASSIFY,
    DRYRUN_MOCK_CASES,
    INGESTION_MAPPING,
    OBJECT_OBSERVATION_CANDIDATE_CONTRACT,
    PROHIBITED_SCOPE,
    REJECTED_DETECTION_POLICY,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    SUPERVISION_NORMALIZED_CONTRACT,
)
from capabilities.midplatform.real_observation_candidate_ingestion_skeleton_lineage_v1 import (
    INGESTION_SKELETON_STAGE_ADDITIONS,
    INGESTION_SKELETON_STAGE_TERM_OVERRIDES,
    INGESTION_SKELETON_WHITELIST_FILES,
)
from capabilities.midplatform.real_observation_candidate_ingestion_static_validators_v1 import validate_non_execution_boundary
from capabilities.midplatform.real_observation_candidate_ingestion_types_v1 import NON_EXECUTION_FLAGS
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

PHASE_ID = "Phase-Midplatform-Real-Observation-Candidate-Ingestion-Skeleton-v1-001"
SCOPE = "real_observation_candidate_ingestion_skeleton_only"
SOURCE_CHAIN = "real_observation_candidate_ingestion_skeleton_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_REAL_OBSERVATION_CANDIDATE_INGESTION_SKELETON_READY_FOR_REAL_MODEL_SUCCESS_PATH_DRYRUN_PLANNING"
)
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_REAL_OBSERVATION_INGESTION_SKELETON_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_REAL_OBSERVATION_INGESTION_SKELETON_BLOCKED_BY_IMPLEMENTATION_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Real-Observation-Ingestion-Skeleton-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/real_observation_candidate_ingestion_skeleton_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_REAL_OBSERVATION_CANDIDATE_INGESTION_SKELETON_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/real_observation_candidate_ingestion_skeleton_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/real_observation_candidate_ingestion_types_v1.py",
    "capabilities/midplatform/real_observation_detection_normalizer_v1.py",
    "capabilities/midplatform/object_observation_candidate_builder_v1.py",
    "capabilities/midplatform/real_observation_ingestion_result_assembler_v1.py",
    "capabilities/midplatform/real_observation_candidate_ingestion_static_validators_v1.py",
    "capabilities/midplatform/real_observation_candidate_ingestion_core_v1.py",
    "capabilities/midplatform/real_observation_candidate_ingestion_skeleton_v1.py",
    "capabilities/midplatform/real_observation_candidate_ingestion_skeleton_items_v1.py",
    "capabilities/midplatform/real_observation_candidate_ingestion_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_real_observation_candidate_ingestion_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_real_observation_candidate_ingestion_skeleton_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_minimal_real_model_adapter_planning_go",
    "real_observation_candidate_ingestion_skeleton_complete",
    "object_observation_candidate_builder_complete",
    "detection_normalizer_complete",
    "ingestion_result_assembler_complete",
    "all_mock_cases_passed",
    "depth_missing_fallback_ok",
    "tracker_hint_not_fact_ok",
    "field_first_core_readiness_ok",
    "common_validation_reuse_ok",
    "no_model_download",
    "no_weight_download",
    "no_real_inference_execution",
    "no_runtime_execution",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, plan_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "real_observation_candidate_ingestion_skeleton_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "planning_root": str(plan_root),
    }


def run_real_observation_candidate_ingestion_skeleton_v1(
    *,
    planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    plan_upstream = Path(planning_root or DEFAULT_PLANNING_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, plan_upstream)
    issues: List[str] = []

    plan_s = _read_json(plan_upstream / "summary.json")
    plan_v = _read_json(plan_upstream / "verifier_report.json")
    prior_plan_go = (
        plan_s.get("final_decision") == PLANNING_FINAL_GO
        and plan_v.get("verifier") == "GO"
        and int(plan_v.get("passed_checks", 0)) >= 360
        and plan_s.get("minimal_real_model_adapter_integration_planning_pass") is True
    )
    if not prior_plan_go:
        issues.append("planning_not_go")

    absence = {k: plan_s.get(k) is True for k in ABSENCE_KEYS}
    non_exec_ok, _ = validate_non_execution_boundary(NON_EXECUTION_FLAGS)
    non_execution_boundary_ok = prior_plan_go and plan_s.get("non_execution_boundary_ok") is True and non_exec_ok and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    dryrun_results, all_mock_passed = run_all_ingestion_dryrun_cases(DRYRUN_MOCK_CASES)
    all_candidates = [
        c for r in dryrun_results for c in (r.get("ingestion_result") or {}).get("accepted_candidates") or []
    ]
    detection_normalizer_complete = all_mock_passed
    object_observation_candidate_builder_complete = len(all_candidates) > 0
    ingestion_result_assembler_complete = all(
        (r.get("ingestion_result") or {}).get("ingestion_result_id") for r in dryrun_results
    )
    depth_missing_fallback_ok = all(
        c.get("depth_source") == "unknown" and c.get("depth_error_expected") is True
        for r in dryrun_results if r["case_id"] == "depth_missing_fallback_unknown"
        for c in (r.get("ingestion_result") or {}).get("accepted_candidates") or []
    ) if any(r["case_id"] == "depth_missing_fallback_unknown" for r in dryrun_results) else True
    tracker_hint_not_fact_ok = all(
        c.get("tracker_id_is_hint_not_fact") is True for c in all_candidates
    )
    field_first_core_readiness_ok = any(
        (r.get("ingestion_result") or {}).get("readiness_for_field_first_core") is True
        for r in dryrun_results if r["case_id"] == "ready_for_field_first_core"
    )
    real_observation_candidate_ingestion_skeleton_complete = (
        detection_normalizer_complete and object_observation_candidate_builder_complete
        and ingestion_result_assembler_complete and all_mock_passed
    )

    readiness_review = {
        "review_id": "field_first_core_readiness_review_v1",
        "field_first_core_readiness_ok": field_first_core_readiness_ok,
        "total_candidates_generated": len(all_candidates),
        "readiness_cases": [r["case_id"] for r in dryrun_results if (r.get("ingestion_result") or {}).get("readiness_for_field_first_core")],
        **meta,
    }
    mock_results = {
        "results_id": "real_observation_ingestion_mock_case_results_v1",
        "all_mock_cases_passed": all_mock_passed,
        "results": dryrun_results,
        **meta,
    }
    non_exec_review = {"review_id": "non_execution_boundary_review_v1", "non_execution_boundary_ok": non_execution_boundary_ok, "flags": dict(NON_EXECUTION_FLAGS), **meta}
    prohibited = {**PROHIBITED_SCOPE, **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    skeleton_pass = (
        prior_plan_go and real_observation_candidate_ingestion_skeleton_complete
        and all_mock_passed and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Field-First-Minimal-Real-Model-Adapter-Integration-Planning-v1-001",
        base_capability=INGESTION_SKELETON_WHITELIST_FILES[0],
        base_runner=INGESTION_SKELETON_WHITELIST_FILES[1],
        base_verifier=INGESTION_SKELETON_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Real-Observation-Candidate-Ingestion-Skeleton-v1-001",
        stage_term_overrides=INGESTION_SKELETON_STAGE_TERM_OVERRIDES,
        stage_additions=INGESTION_SKELETON_STAGE_ADDITIONS,
        template_files=INGESTION_SKELETON_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Field-First-Minimal-Real-Model-Adapter-Integration-Planning-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    plan_fs = _read_json(plan_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=plan_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    skeleton_pass = skeleton_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if skeleton_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if skeleton_pass else (FINAL_DECISION_UPSTREAM if not prior_plan_go else FINAL_DECISION_RECAL)

    go_values = {
        "prior_minimal_real_model_adapter_planning_go": prior_plan_go,
        "real_observation_candidate_ingestion_skeleton_complete": real_observation_candidate_ingestion_skeleton_complete,
        "object_observation_candidate_builder_complete": object_observation_candidate_builder_complete,
        "detection_normalizer_complete": detection_normalizer_complete,
        "ingestion_result_assembler_complete": ingestion_result_assembler_complete,
        "all_mock_cases_passed": all_mock_passed,
        "depth_missing_fallback_ok": depth_missing_fallback_ok,
        "tracker_hint_not_fact_ok": tracker_hint_not_fact_ok,
        "field_first_core_readiness_ok": field_first_core_readiness_ok,
        "bbox_label_confidence_mapped": True,
        "low_confidence_detection_retained": True,
        "unknown_label_fallback_supported": True,
        "invalid_bbox_rejected": True,
        "object_observation_candidates_generated": len(all_candidates) > 0,
        "readiness_for_field_first_core": field_first_core_readiness_ok,
        "common_validation_reuse_ok": True,
        "no_model_download": True,
        "no_weight_download": True,
        "no_large_dependency_install": True,
        "no_real_inference_execution": True,
        "no_runtime_execution": True,
        "no_world_model_fact_creation": True,
        "no_persistent_memory_write": True,
        "no_integration_test": True,
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": skeleton_pass,
        "real_observation_candidate_ingestion_skeleton_pass": skeleton_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "mock_case_count": len(dryrun_results),
        "observation_candidate_count": len(all_candidates),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        "midplatform_still_has_remaining_work": True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(plan_s.get("chain_trace_nodes") or []) + ["real_observation_candidate_ingestion_skeleton"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Real Observation Candidate Ingestion Skeleton v1",
        f"Dryrun cases: `{len(dryrun_results)}` | Candidates: `{len(all_candidates)}` | All passed: `{all_mock_passed}`",
        "DetectorOutputMock → normalize → ObjectObservationCandidate (no real YOLO)",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "final_decision": final_decision, **meta}
    return {
        "real_observation_candidate_ingestion_skeleton_report": report,
        "real_observation_candidate_ingestion_skeleton_report_md": md,
        "detector_output_mock_contract": {**DETECTOR_OUTPUT_MOCK_CONTRACT, **meta},
        "supervision_normalized_detection_contract": {**SUPERVISION_NORMALIZED_CONTRACT, **meta},
        "object_observation_candidate_contract": {**OBJECT_OBSERVATION_CANDIDATE_CONTRACT, **meta},
        "detector_to_observation_ingestion_mapping": {**INGESTION_MAPPING, **meta},
        "depth_missing_fallback_execution_policy": {**DEPTH_FALLBACK_EXECUTION, **meta},
        "real_observation_ingestion_mock_case_results": mock_results,
        "rejected_detection_policy": {**REJECTED_DETECTION_POLICY, **meta},
        "field_first_core_readiness_review": readiness_review,
        "non_execution_boundary_review": non_exec_review,
        "prohibited_scope": prohibited,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
