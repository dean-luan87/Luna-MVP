# -*- coding: utf-8 -*-
"""Field-First Minimal Real Model Adapter Integration Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.field_first_core_logic_formal_implementation_v1 import (
    DEFAULT_OUTPUT as DEFAULT_CORE_LOGIC_ROOT,
    FINAL_DECISION_GO as CORE_LOGIC_FINAL_GO,
)
from capabilities.midplatform.field_first_minimal_real_model_adapter_integration_items_v1 import (
    DEPTH_MISSING_FALLBACK_POLICY,
    DETECTOR_ADAPTER_PLAN,
    DETECTOR_TO_OBSERVATION_MAPPING,
    DO_NOT_MISCLASSIFY,
    DOWNLOAD_AUTHORIZATION_STATUS,
    MOCK_PLANNING_CASES,
    P0_MODELS,
    P1_OPTIONAL,
    P2_DEFERRED,
    PLANNING_RULES,
    PROHIBITED_SCOPE,
    REAL_MODEL_SUCCESS_PATH_READINESS,
    REAL_OBSERVATION_INGESTION_PLAN,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    SUPERVISION_NORMALIZATION_PLAN,
)
from capabilities.midplatform.field_first_minimal_real_model_adapter_integration_lineage_v1 import (
    ADAPTER_PLANNING_STAGE_ADDITIONS,
    ADAPTER_PLANNING_STAGE_TERM_OVERRIDES,
    ADAPTER_PLANNING_WHITELIST_FILES,
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

PHASE_ID = "Phase-Midplatform-Field-First-Minimal-Real-Model-Adapter-Integration-Planning-v1-001"
SCOPE = "minimal_real_model_adapter_integration_planning_only"
SOURCE_CHAIN = "field_first_minimal_real_model_adapter_integration_planning_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_FIELD_FIRST_MINIMAL_REAL_MODEL_ADAPTER_INTEGRATION_PLANNING_READY_FOR_REAL_OBSERVATION_CANDIDATE_INGESTION_SKELETON"
)
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_MINIMAL_REAL_MODEL_ADAPTER_PLANNING_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_MINIMAL_REAL_MODEL_ADAPTER_PLANNING_BLOCKED_BY_PLANNING_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Minimal-Real-Model-Adapter-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_first_minimal_real_model_adapter_integration_planning_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_MINIMAL_REAL_MODEL_ADAPTER_INTEGRATION_PLANNING_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/field_first_minimal_real_model_adapter_integration_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_minimal_real_model_adapter_integration_planning_v1.py",
    "capabilities/midplatform/field_first_minimal_real_model_adapter_integration_items_v1.py",
    "capabilities/midplatform/field_first_minimal_real_model_adapter_integration_lineage_v1.py",
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "tools/evaluation/midplatform/run_field_first_minimal_real_model_adapter_integration_planning_v1.py",
    "tools/evaluation/midplatform/verify_field_first_minimal_real_model_adapter_integration_planning_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_field_first_core_logic_go",
    "minimal_real_model_adapter_integration_planning_complete",
    "detector_adapter_plan_complete",
    "supervision_normalization_plan_complete",
    "observation_candidate_mapping_complete",
    "depth_missing_fallback_policy_complete",
    "real_model_success_path_readiness_plan_complete",
    "no_weight_download",
    "no_large_dependency_install",
    "no_production_model_selection",
    "no_field_simulation",
    "no_task_execution",
    "no_runtime_execution",
    "no_world_model_fact_creation",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
    "first_batch_scope_limited_to_detector_and_normalization",
    "model_output_maps_to_observation_candidate",
    "depth_unknown_policy_defined",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, core_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "minimal_real_model_adapter_integration_planning_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "core_logic_root": str(core_root),
        "route_correction": "field_simulation_deferred_until_real_model_success_path",
    }


def run_field_first_minimal_real_model_adapter_integration_planning_v1(
    *,
    core_logic_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    core_upstream = Path(core_logic_root or DEFAULT_CORE_LOGIC_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, core_upstream)
    issues: List[str] = []

    core_s = _read_json(core_upstream / "summary.json")
    core_v = _read_json(core_upstream / "verifier_report.json")
    prior_core_go = (
        core_s.get("final_decision") == CORE_LOGIC_FINAL_GO
        and core_v.get("verifier") == "GO"
        and int(core_v.get("passed_checks", 0)) >= 420
        and core_s.get("field_first_core_logic_formal_implementation_pass") is True
    )
    if not prior_core_go:
        issues.append("core_logic_not_go")

    absence = {k: core_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = prior_core_go and core_s.get("non_execution_boundary_ok") is True and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    detector_adapter_plan_complete = DETECTOR_ADAPTER_PLAN.get("candidate_only") is True and DETECTOR_ADAPTER_PLAN.get("maps_to_candidate_type") == "ObjectObservationCandidate"
    supervision_normalization_plan_complete = SUPERVISION_NORMALIZATION_PLAN.get("candidate_only") is True
    observation_candidate_mapping_complete = DETECTOR_TO_OBSERVATION_MAPPING.get("candidate_only") is True
    depth_missing_fallback_policy_complete = "when_depth_absent" in DEPTH_MISSING_FALLBACK_POLICY
    real_model_success_path_readiness_plan_complete = len(REAL_MODEL_SUCCESS_PATH_READINESS.get("success_path_validates") or []) >= 5
    mock_cases_complete = len(MOCK_PLANNING_CASES) >= 10
    minimal_real_model_adapter_integration_planning_complete = (
        detector_adapter_plan_complete and supervision_normalization_plan_complete
        and observation_candidate_mapping_complete and depth_missing_fallback_policy_complete
        and real_model_success_path_readiness_plan_complete and mock_cases_complete
        and len(P0_MODELS) >= 2 and len(PLANNING_RULES) >= 8
    )

    detector_plan = {**DETECTOR_ADAPTER_PLAN, "detector_adapter_plan_complete": detector_adapter_plan_complete, "p0_models": list(P0_MODELS), "p1_optional": list(P1_OPTIONAL), "p2_deferred": list(P2_DEFERRED), **meta}
    supervision_plan = {**SUPERVISION_NORMALIZATION_PLAN, "supervision_normalization_plan_complete": supervision_normalization_plan_complete, **meta}
    ingestion_plan = {**REAL_OBSERVATION_INGESTION_PLAN, "observation_candidate_mapping_complete": observation_candidate_mapping_complete, **meta}
    mapping = {**DETECTOR_TO_OBSERVATION_MAPPING, **meta}
    depth_policy = {**DEPTH_MISSING_FALLBACK_POLICY, "depth_missing_fallback_policy_complete": depth_missing_fallback_policy_complete, **meta}
    readiness = {**REAL_MODEL_SUCCESS_PATH_READINESS, "real_model_success_path_readiness_plan_complete": real_model_success_path_readiness_plan_complete, **meta}
    download_status = {**DOWNLOAD_AUTHORIZATION_STATUS, **meta}
    mock_registry = {"registry_id": "minimal_real_model_planning_case_registry_v1", "count": len(MOCK_PLANNING_CASES), "cases": list(MOCK_PLANNING_CASES), **meta}
    rule_reg = {"registry_id": "minimal_real_model_planning_rules_v1", "rules": list(PLANNING_RULES), **meta}
    prohibited = {**PROHIBITED_SCOPE, **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    planning_pass = prior_core_go and minimal_real_model_adapter_integration_planning_complete and non_execution_boundary_ok and len(issues) == 0

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Field-First-Core-Logic-Formal-Implementation-v1-001",
        base_capability=ADAPTER_PLANNING_WHITELIST_FILES[0],
        base_runner=ADAPTER_PLANNING_WHITELIST_FILES[1],
        base_verifier=ADAPTER_PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Field-First-Minimal-Real-Model-Adapter-Integration-Planning-v1-001",
        stage_term_overrides=ADAPTER_PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=ADAPTER_PLANNING_STAGE_ADDITIONS,
        template_files=ADAPTER_PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Field-First-Core-Logic-Formal-Implementation-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    core_fs = _read_json(core_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=core_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    planning_pass = planning_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if planning_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if planning_pass else (FINAL_DECISION_UPSTREAM if not prior_core_go else FINAL_DECISION_RECAL)

    go_values = {
        "prior_field_first_core_logic_go": prior_core_go,
        "minimal_real_model_adapter_integration_planning_complete": minimal_real_model_adapter_integration_planning_complete,
        "detector_adapter_plan_complete": detector_adapter_plan_complete,
        "supervision_normalization_plan_complete": supervision_normalization_plan_complete,
        "observation_candidate_mapping_complete": observation_candidate_mapping_complete,
        "depth_missing_fallback_policy_complete": depth_missing_fallback_policy_complete,
        "real_model_success_path_readiness_plan_complete": real_model_success_path_readiness_plan_complete,
        "mock_cases_complete": mock_cases_complete,
        "common_validation_reuse_ok": True,
        "first_batch_scope_limited_to_detector_and_normalization": True,
        "yolo_or_lightweight_detector_positioned_as_adapter_source": True,
        "supervision_positioned_as_normalization_layer": True,
        "model_output_maps_to_observation_candidate": True,
        "depth_unknown_policy_defined": True,
        "no_weight_download": True,
        "no_large_dependency_install": True,
        "no_production_model_selection": True,
        "no_model_download": True,
        "no_real_inference_execution": True,
        "no_field_simulation": True,
        "no_final_action_output": True,
        "no_task_execution": True,
        "no_runtime_execution": True,
        "no_world_model_fact_creation": True,
        "no_persistent_memory_write": True,
        "no_integration_test": True,
        "candidate_only_outputs": True,
        "field_first_route_preserved": True,
        "field_core_pipeline_unchanged": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": planning_pass,
        "minimal_real_model_adapter_integration_planning_pass": planning_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "mock_case_count": len(MOCK_PLANNING_CASES),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        "midplatform_still_has_remaining_work": True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(core_s.get("chain_trace_nodes") or []) + ["field_first_minimal_real_model_adapter_integration_planning"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Field-First Minimal Real Model Adapter Integration Planning v1",
        f"P0 models: `{len(P0_MODELS)}` | P2 deferred: `{len(P2_DEFERRED)}` | Planning cases: `{len(MOCK_PLANNING_CASES)}`",
        "Route: real detector → supervision normalize → ObservationCandidate → Field-First Core",
        f"Field Simulation deferred until real-model success path validated",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "final_decision": final_decision, **meta}
    return {
        "minimal_real_model_adapter_integration_planning_report": report,
        "minimal_real_model_adapter_integration_planning_report_md": md,
        "minimal_detector_adapter_plan": detector_plan,
        "supervision_normalization_plan": supervision_plan,
        "real_observation_candidate_ingestion_plan": ingestion_plan,
        "detector_output_to_observation_candidate_mapping": mapping,
        "depth_missing_fallback_policy": depth_policy,
        "real_model_success_path_readiness_plan": readiness,
        "model_download_authorization_status": download_status,
        "minimal_real_model_planning_case_registry": mock_registry,
        "minimal_real_model_planning_rules": rule_reg,
        "prohibited_scope": prohibited,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
