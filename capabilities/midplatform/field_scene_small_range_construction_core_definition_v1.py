# -*- coding: utf-8 -*-
"""Field Scene Small Range Construction Core Definition v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.field_first_core_model_io_compatibility_precheck_v1 import (
    DEFAULT_OUTPUT as DEFAULT_IO_PRECHECK_ROOT,
    FINAL_DECISION_GO as IO_PRECHECK_FINAL_GO,
)
from capabilities.midplatform.field_scene_small_range_builder_v1 import construct_small_range_field_scene
from capabilities.midplatform.field_scene_small_range_construction_items_v1 import (
    DEPTH_UNCERTAINTY_POLICY,
    DO_NOT_MISCLASSIFY,
    FIELD_ZONE_ASSIGNMENT_POLICY,
    INPUT_CANDIDATE_CONTRACT,
    MOCK_CASES,
    NEXT_STAGE_SPLIT_PLAN,
    OUTPUT_CANDIDATE_CONTRACT,
    PROCESSING_FLOW,
    PROHIBITED_SCOPE,
    SCOPE_DEFINITION,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.field_scene_small_range_construction_lineage_v1 import (
    FIELD_SCENE_SMALL_RANGE_STAGE_ADDITIONS,
    FIELD_SCENE_SMALL_RANGE_STAGE_TERM_OVERRIDES,
    FIELD_SCENE_SMALL_RANGE_WHITELIST_FILES,
)
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

PHASE_ID = "Phase-Midplatform-Field-Scene-Small-Range-Construction-Core-Definition-v1-001"
SCOPE = "field_scene_small_range_construction_only"
SOURCE_CHAIN = "field_scene_small_range_construction_core_definition_v1"
FINAL_DECISION_GO = "MIDPLATFORM_FIELD_SCENE_SMALL_RANGE_CONSTRUCTION_CORE_DEFINITION_READY_FOR_FIELD_CONTINUITY_DETECTION_PLANNING"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_FIELD_SCENE_SMALL_RANGE_CONSTRUCTION_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_FIELD_SCENE_SMALL_RANGE_CONSTRUCTION_BLOCKED_BY_CONSTRUCTION_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Field-Scene-Small-Range-Construction-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_scene_small_range_construction_core_definition_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_SCENE_SMALL_RANGE_CONSTRUCTION_CORE_DEFINITION_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/field_scene_small_range_construction_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_scene_small_range_types_v1.py",
    "capabilities/midplatform/field_scene_small_range_builder_v1.py",
    "capabilities/midplatform/field_scene_small_range_static_validators_v1.py",
    "capabilities/midplatform/field_scene_small_range_core_v1.py",
    "capabilities/midplatform/field_scene_small_range_construction_core_definition_v1.py",
    "capabilities/midplatform/field_scene_small_range_construction_items_v1.py",
    "capabilities/midplatform/field_scene_small_range_construction_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_scene_small_range_construction_core_definition_v1.py",
    "tools/evaluation/midplatform/verify_field_scene_small_range_construction_core_definition_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_model_io_compatibility_precheck_go",
    "small_range_field_scene_construction_complete",
    "field_scene_candidate_generated",
    "field_entity_candidates_generated",
    "depth_uncertainty_policy_complete",
    "field_zone_assignment_policy_complete",
    "mock_cases_all_passed",
    "non_execution_boundary_ok",
    "no_model_download",
    "no_real_inference_execution",
    "no_runtime_execution",
    "file_size_governance_review_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, io_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "field_scene_small_range_construction_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "io_precheck_root": str(io_root),
    }


def _run_mock_cases() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], bool]:
    results: List[Dict[str, Any]] = []
    all_entities: List[Dict[str, Any]] = []
    all_pass = True
    for case in MOCK_CASES:
        out = construct_small_range_field_scene(
            observations=[dict(o) for o in case["observations"]],
            user_state=dict(case["user_state"]),
            camera_state=dict(case["camera_state"]),
            field_session_ref=f"session_{case['case_id']}",
        )
        passed = out["construction_pass"]
        entities = out["entities"]
        warnings = out["warnings"]
        if case.get("expect_pass") and not passed:
            all_pass = False
        if case.get("min_entities") and len(entities) < case["min_entities"]:
            all_pass = False
        if case.get("expected_zones"):
            zones = {e["field_zone"] for e in entities}
            if not any(z in zones for z in case["expected_zones"]):
                all_pass = False
        if case.get("expect_missing"):
            mi = out["field_scene"].get("missing_information") or []
            if case["expect_missing"] not in mi:
                all_pass = False
        if case.get("require_depth_error_expected"):
            if not all(e.get("depth_error_expected") for e in entities if e.get("depth_source") == "estimated"):
                all_pass = False
        if case.get("expected_warnings_contain"):
            if not any(case["expected_warnings_contain"] in w for w in warnings):
                all_pass = False
        all_entities.extend(entities)
        results.append({
            "case_id": case["case_id"],
            "description": case["description"],
            "construction_pass": passed,
            "entity_count": len(entities),
            "field_scene_id": out["field_scene"]["field_scene_id"],
            "warnings": warnings,
            "entity_labels": [e["label"] for e in entities],
            "field_zones": [e["field_zone"] for e in entities],
        })
    return results, all_entities, all_pass


def run_field_scene_small_range_construction_core_definition_v1(
    *,
    io_precheck_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    io_upstream = Path(io_precheck_root or DEFAULT_IO_PRECHECK_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, io_upstream)
    issues: List[str] = []

    io_s = _read_json(io_upstream / "summary.json")
    io_v = _read_json(io_upstream / "verifier_report.json")
    prior_io_go = (
        io_s.get("final_decision") == IO_PRECHECK_FINAL_GO
        and io_v.get("verifier") == "GO"
        and int(io_v.get("passed_checks", 0)) >= 420
        and io_s.get("field_first_core_model_io_compatibility_precheck_pass") is True
    )
    if not prior_io_go:
        issues.append("io_precheck_not_go")

    absence = {k: io_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = prior_io_go and io_s.get("non_execution_boundary_ok") is True and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    mock_results, all_entities, mock_all_passed = _run_mock_cases()
    entity_registry = [{"entity_candidate_id": e["entity_candidate_id"], "label": e["label"], "field_zone": e["field_zone"], "depth_source": e["depth_source"], "fact_status": e["fact_status"]} for e in all_entities]
    unique_labels = sorted({e["label"] for e in all_entities})

    field_scene_candidate_generated = any(r["construction_pass"] for r in mock_results)
    field_entity_candidates_generated = len(all_entities) >= 5 and len(unique_labels) >= 5
    small_range_field_scene_construction_complete = len(mock_results) >= 8 and mock_all_passed and field_scene_candidate_generated
    depth_uncertainty_policy_complete = DEPTH_UNCERTAINTY_POLICY.get("depth_estimated_not_fact") is True
    field_zone_assignment_policy_complete = all(
        FIELD_ZONE_ASSIGNMENT_POLICY.get(k) is True
        for k in ("inner_zone_supported", "working_zone_supported", "forecast_zone_reserved", "unknown_zone_supported")
    )

    scope_def = {**SCOPE_DEFINITION, **meta}
    input_contract = {**INPUT_CANDIDATE_CONTRACT, **meta}
    output_contract = {**OUTPUT_CANDIDATE_CONTRACT, **meta}
    flow = {"flow_id": "field_scene_processing_flow_v1", "steps": list(PROCESSING_FLOW), **meta}
    mock_registry = {"registry_id": "field_scene_mock_case_registry_v1", "count": len(MOCK_CASES), "cases": [{"case_id": c["case_id"], "description": c["description"]} for c in MOCK_CASES], **meta}
    mock_case_results = {"results_id": "field_scene_mock_case_results_v1", "mock_cases_all_passed": mock_all_passed, "results": mock_results, **meta}
    entity_reg = {"registry_id": "field_entity_candidate_registry_v1", "count": len(entity_registry), "unique_label_count": len(unique_labels), "entities": entity_registry, **meta}
    depth_policy = {**DEPTH_UNCERTAINTY_POLICY, "depth_uncertainty_policy_complete": depth_uncertainty_policy_complete, **meta}
    zone_policy = {**FIELD_ZONE_ASSIGNMENT_POLICY, "field_zone_assignment_policy_complete": field_zone_assignment_policy_complete, **meta}
    prohibited = {**PROHIBITED_SCOPE, **meta}
    next_split = {**NEXT_STAGE_SPLIT_PLAN, **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    construction_pass = (
        prior_io_go and small_range_field_scene_construction_complete
        and field_scene_candidate_generated and field_entity_candidates_generated
        and depth_uncertainty_policy_complete and field_zone_assignment_policy_complete
        and mock_all_passed and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Field-First-Core-Model-IO-Compatibility-Precheck-v1-001",
        base_capability=FIELD_SCENE_SMALL_RANGE_WHITELIST_FILES[0],
        base_runner=FIELD_SCENE_SMALL_RANGE_WHITELIST_FILES[1],
        base_verifier=FIELD_SCENE_SMALL_RANGE_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Field-Scene-Small-Range-Construction-Core-Definition-v1-001",
        stage_term_overrides=FIELD_SCENE_SMALL_RANGE_STAGE_TERM_OVERRIDES,
        stage_additions=FIELD_SCENE_SMALL_RANGE_STAGE_ADDITIONS,
        template_files=FIELD_SCENE_SMALL_RANGE_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Field-First-Core-Model-IO-Compatibility-Precheck-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    io_fs = _read_json(io_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=io_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    construction_pass = construction_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if construction_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if construction_pass else (FINAL_DECISION_UPSTREAM if not prior_io_go else FINAL_DECISION_RECAL)

    go_values = {
        "prior_model_io_compatibility_precheck_go": prior_io_go,
        "small_range_field_scene_construction_complete": small_range_field_scene_construction_complete,
        "field_scene_candidate_generated": field_scene_candidate_generated,
        "field_entity_candidates_generated": field_entity_candidates_generated,
        "depth_uncertainty_policy_complete": depth_uncertainty_policy_complete,
        "field_zone_assignment_policy_complete": field_zone_assignment_policy_complete,
        "mock_cases_all_passed": mock_all_passed,
        "no_model_download": True,
        "no_weight_download": True,
        "no_real_inference_execution": True,
        "no_runtime_execution": True,
        "no_integration_test": True,
        "candidate_only_outputs": True,
        "no_semantic_attachment": True,
        "no_tracking_execution": True,
        "no_trajectory_simulation": True,
        "no_world_model_fact_creation": True,
        "no_persistent_memory_write": True,
        "depth_estimated_not_fact": True,
        "inner_zone_supported": True,
        "working_zone_supported": True,
        "forecast_zone_reserved": True,
        "unknown_zone_supported": True,
        "pseudo_3d_position_supported": True,
        "missing_depth_handled": True,
        "low_confidence_object_not_silently_dropped": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": construction_pass,
        "field_scene_small_range_construction_pass": construction_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "mock_case_count": len(mock_results),
        "entity_candidate_count": len(all_entities),
        "unique_entity_label_count": len(unique_labels),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        "midplatform_still_has_remaining_work": True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(io_s.get("chain_trace_nodes") or []) + ["field_scene_small_range_construction"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Field Scene Small Range Construction v1",
        f"Mock cases: `{len(mock_results)}` | Entities: `{len(all_entities)}` | Labels: `{len(unique_labels)}`",
        "Pipeline: ObservationCandidate → Small Range Field Scene → FieldSceneCandidate",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "final_decision": final_decision, **meta}
    return {
        "field_scene_small_range_construction_report": report,
        "field_scene_small_range_construction_report_md": md,
        "field_scene_scope_definition": scope_def,
        "field_scene_input_candidate_contract": input_contract,
        "field_scene_output_candidate_contract": output_contract,
        "field_scene_processing_flow": flow,
        "field_scene_mock_case_registry": mock_registry,
        "field_scene_mock_case_results": mock_case_results,
        "field_entity_candidate_registry": entity_reg,
        "depth_uncertainty_policy": depth_policy,
        "field_zone_assignment_policy": zone_policy,
        "prohibited_scope": prohibited,
        "next_stage_split_plan": next_split,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
