# -*- coding: utf-8 -*-
"""Field Continuity Detection Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.field_continuity_detection_planning_items_v1 import (
    ABNORMAL_CASE_POLICY,
    CONTINUITY_STATUSES,
    DECISION_MODEL,
    DO_NOT_MISCLASSIFY,
    FIELD_SESSION_STATES,
    INPUT_OUTPUT_CONTRACT,
    MOCK_CASES,
    NEXT_IMPLEMENTATION_PLAN,
    PLANNING_PRINCIPLES,
    PROHIBITED_SCOPE,
    SCOPE_DEFINITION,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    SIGNAL_REGISTRY,
    STATE_TRANSITIONS,
)
from capabilities.midplatform.field_continuity_detection_planning_lineage_v1 import (
    FIELD_CONTINUITY_PLANNING_STAGE_ADDITIONS,
    FIELD_CONTINUITY_PLANNING_STAGE_TERM_OVERRIDES,
    FIELD_CONTINUITY_PLANNING_WHITELIST_FILES,
)
from capabilities.midplatform.field_scene_small_range_construction_core_definition_v1 import (
    DEFAULT_OUTPUT as DEFAULT_FIELD_SCENE_ROOT,
    FINAL_DECISION_GO as FIELD_SCENE_FINAL_GO,
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

PHASE_ID = "Phase-Midplatform-Field-Continuity-Detection-Planning-v1-001"
SCOPE = "field_continuity_detection_planning_only"
SOURCE_CHAIN = "field_continuity_detection_planning_v1"
FINAL_DECISION_GO = "MIDPLATFORM_FIELD_CONTINUITY_DETECTION_PLANNING_READY_FOR_CONTROLLED_SKELETON_IMPLEMENTATION"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_FIELD_CONTINUITY_DETECTION_PLANNING_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_FIELD_CONTINUITY_DETECTION_PLANNING_BLOCKED_BY_PLANNING_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Field-Continuity-Detection-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_continuity_detection_planning_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_CONTINUITY_DETECTION_PLANNING_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/field_continuity_detection_planning_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_continuity_detection_planning_v1.py",
    "capabilities/midplatform/field_continuity_detection_planning_items_v1.py",
    "capabilities/midplatform/field_continuity_detection_planning_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_continuity_detection_planning_v1.py",
    "tools/evaluation/midplatform/verify_field_continuity_detection_planning_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_field_scene_small_range_construction_go",
    "field_continuity_detection_planning_complete",
    "signal_registry_complete",
    "decision_model_complete",
    "field_session_state_machine_complete",
    "abnormal_case_policy_complete",
    "mock_cases_complete",
    "continuity_before_tracking",
    "non_execution_boundary_ok",
    "no_tracking_execution",
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


def _meta(out: Path, scene_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "field_continuity_detection_planning_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "field_scene_root": str(scene_root),
    }


def run_field_continuity_detection_planning_v1(
    *,
    field_scene_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    scene_upstream = Path(field_scene_root or DEFAULT_FIELD_SCENE_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, scene_upstream)
    issues: List[str] = []

    scene_s = _read_json(scene_upstream / "summary.json")
    scene_v = _read_json(scene_upstream / "verifier_report.json")
    prior_scene_go = (
        scene_s.get("final_decision") == FIELD_SCENE_FINAL_GO
        and scene_v.get("verifier") == "GO"
        and int(scene_v.get("passed_checks", 0)) >= 360
        and scene_s.get("field_scene_small_range_construction_pass") is True
    )
    if not prior_scene_go:
        issues.append("field_scene_construction_not_go")

    absence = {k: scene_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = prior_scene_go and scene_s.get("non_execution_boundary_ok") is True and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    signal_registry_complete = len(SIGNAL_REGISTRY) >= 8
    decision_model_complete = DECISION_MODEL.get("candidate_only") is True and len(DECISION_MODEL.get("fields") or []) >= 10
    field_session_state_machine_complete = len(FIELD_SESSION_STATES) >= 7 and len(STATE_TRANSITIONS) >= 10
    abnormal_case_policy_complete = len(ABNORMAL_CASE_POLICY.get("cases") or ()) >= 10
    mock_cases_complete = len(MOCK_CASES) >= 10
    field_continuity_detection_planning_complete = (
        signal_registry_complete and decision_model_complete
        and field_session_state_machine_complete and abnormal_case_policy_complete and mock_cases_complete
    )

    scope_def = {**SCOPE_DEFINITION, **meta}
    signal_reg = {"registry_id": "field_continuity_signal_registry_v1", "signal_registry_complete": signal_registry_complete, "count": len(SIGNAL_REGISTRY), "signals": list(SIGNAL_REGISTRY), **meta}
    status_reg = {"registry_id": "field_continuity_status_registry_v1", "statuses": list(CONTINUITY_STATUSES), **meta}
    decision_model = {**DECISION_MODEL, "decision_model_complete": decision_model_complete, **meta}
    state_machine = {"machine_id": "field_session_state_machine_v1", "field_session_state_machine_complete": field_session_state_machine_complete, "states": list(FIELD_SESSION_STATES), "transitions": list(STATE_TRANSITIONS), **meta}
    abnormal = {**ABNORMAL_CASE_POLICY, "abnormal_case_policy_complete": abnormal_case_policy_complete, **meta}
    mock_registry = {"registry_id": "field_continuity_mock_case_registry_v1", "count": len(MOCK_CASES), "cases": [{"case_id": c["case_id"], "expected_status": c["expected_status"]} for c in MOCK_CASES], **meta}
    mock_expected = {"results_id": "field_continuity_mock_case_expected_results_v1", "mock_cases_complete": mock_cases_complete, "cases": list(MOCK_CASES), **meta}
    io_contract = {**INPUT_OUTPUT_CONTRACT, **meta}
    next_plan = {**NEXT_IMPLEMENTATION_PLAN, **meta}
    prohibited = {**PROHIBITED_SCOPE, **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    planning_pass = (
        prior_scene_go and field_continuity_detection_planning_complete
        and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Field-Scene-Small-Range-Construction-Core-Definition-v1-001",
        base_capability=FIELD_CONTINUITY_PLANNING_WHITELIST_FILES[0],
        base_runner=FIELD_CONTINUITY_PLANNING_WHITELIST_FILES[1],
        base_verifier=FIELD_CONTINUITY_PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Field-Continuity-Detection-Planning-v1-001",
        stage_term_overrides=FIELD_CONTINUITY_PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=FIELD_CONTINUITY_PLANNING_STAGE_ADDITIONS,
        template_files=FIELD_CONTINUITY_PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Field-Scene-Small-Range-Construction-Core-Definition-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    scene_fs = _read_json(scene_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=scene_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    planning_pass = planning_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if planning_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if planning_pass else (FINAL_DECISION_UPSTREAM if not prior_scene_go else FINAL_DECISION_RECAL)

    go_values = {
        "prior_field_scene_small_range_construction_go": prior_scene_go,
        "field_continuity_detection_planning_complete": field_continuity_detection_planning_complete,
        "signal_registry_complete": signal_registry_complete,
        "decision_model_complete": decision_model_complete,
        "field_session_state_machine_complete": field_session_state_machine_complete,
        "abnormal_case_policy_complete": abnormal_case_policy_complete,
        "mock_cases_complete": mock_cases_complete,
        "continuity_before_tracking": True,
        "no_tracking_execution": True,
        "no_trajectory_simulation": True,
        "no_semantic_attachment": True,
        "no_world_model_fact_creation": True,
        "no_persistent_memory_write": True,
        "no_model_download": True,
        "no_weight_download": True,
        "no_real_inference_execution": True,
        "no_runtime_execution": True,
        "no_integration_test": True,
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": planning_pass,
        "field_continuity_detection_planning_pass": planning_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "mock_case_count": len(MOCK_CASES),
        "signal_count": len(SIGNAL_REGISTRY),
        "status_count": len(CONTINUITY_STATUSES),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        "midplatform_still_has_remaining_work": True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(scene_s.get("chain_trace_nodes") or []) + ["field_continuity_detection_planning"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Field Continuity Detection Planning v1",
        f"Signals: `{len(SIGNAL_REGISTRY)}` | Statuses: `{len(CONTINUITY_STATUSES)}` | Mock cases: `{len(MOCK_CASES)}`",
        "Pipeline: FieldScene(t-1) + FieldScene(t) → FieldContinuityDecisionCandidate",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "principles": PLANNING_PRINCIPLES, "final_decision": final_decision, **meta}
    return {
        "field_continuity_detection_planning_report": report,
        "field_continuity_detection_planning_report_md": md,
        "field_continuity_scope_definition": scope_def,
        "field_continuity_signal_registry": signal_reg,
        "field_continuity_status_registry": status_reg,
        "field_continuity_decision_model": decision_model,
        "field_session_state_machine": state_machine,
        "field_continuity_abnormal_case_policy": abnormal,
        "field_continuity_mock_case_registry": mock_registry,
        "field_continuity_mock_case_expected_results": mock_expected,
        "field_continuity_input_output_contract": io_contract,
        "field_continuity_next_implementation_plan": next_plan,
        "prohibited_scope": prohibited,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
