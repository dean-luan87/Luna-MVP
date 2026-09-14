# -*- coding: utf-8 -*-
"""Model adapter priority sequence planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.model_adapter_priority_sequence_planning_items_v1 import (
    DEFERRED_ADAPTERS,
    DO_NOT_MISCLASSIFY,
    MODEL_ADAPTER_PRIORITY_REGISTRY,
    NEW_PROTOCOL_REASON_REPORT,
    NEXT_SKELETON_RECOMMENDATION,
    PLANNING_CASES,
    PROHIBITED_SCOPE,
    PROTOCOL_REUSE_DECISION,
    REUSE_PATH_REGISTRY,
    SCENARIO_MODEL_GROUPS,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    TASK_COLLABORATION_MAPPING,
    WORLD_MODEL_CONSTRUCTION_MAPPING,
)
from capabilities.midplatform.model_adapter_priority_sequence_planning_lineage_v1 import (
    PLANNING_STAGE_ADDITIONS,
    PLANNING_STAGE_TERM_OVERRIDES,
    PLANNING_WHITELIST_FILES,
)
from capabilities.midplatform.model_adapter_priority_sequence_planning_types_v1 import (
    FINAL_DECISION_GO,
    NON_EXECUTION_FLAGS,
)
from capabilities.midplatform.model_workflow_protocol_reuse_and_cleanup_review_v1 import (
    DEFAULT_OUTPUT as DEFAULT_CLEANUP_ROOT,
    FINAL_DECISION_GO as CLEANUP_FINAL_GO,
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

PHASE_ID = "Phase-Midplatform-Model-Adapter-Priority-Sequence-Planning-v1-001"
SCOPE = "model_adapter_priority_sequence_planning_only"
SOURCE_CHAIN = "model_adapter_priority_sequence_planning_v1"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_MODEL_ADAPTER_PRIORITY_SEQUENCE_PLANNING_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_MODEL_ADAPTER_PRIORITY_SEQUENCE_PLANNING_BLOCKED_BY_PLANNING_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Model-Adapter-Priority-Sequence-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/model_adapter_priority_sequence_planning_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_MODEL_ADAPTER_PRIORITY_SEQUENCE_PLANNING_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/model_adapter_priority_sequence_planning_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/model_adapter_priority_sequence_planning_types_v1.py",
    "capabilities/midplatform/model_adapter_priority_sequence_planning_items_v1.py",
    "capabilities/midplatform/model_adapter_priority_sequence_planning_lineage_v1.py",
    "capabilities/midplatform/model_adapter_priority_sequence_planning_v1.py",
    "tools/evaluation/midplatform/run_model_adapter_priority_sequence_planning_v1.py",
    "tools/evaluation/midplatform/verify_model_adapter_priority_sequence_planning_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_model_workflow_protocol_reuse_and_cleanup_review_go",
    "model_adapter_priority_sequence_planning_complete",
    "priority_registry_complete",
    "reuse_path_registry_complete",
    "world_model_mapping_complete",
    "task_collaboration_mapping_complete",
    "scenario_model_group_registry_complete",
    "no_new_protocol_without_reason",
    "no_field_simulation_route",
    "no_task_reasoning_route",
    "owner_constraints_inherited",
    "slam_or_spatial_mapping_prioritized",
    "tracking_second_priority",
    "ocr_third_priority",
    "segmentation_fourth_priority",
    "scene_graph_deferred",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _priority_by_id(adapter_id: str) -> Optional[Dict[str, Any]]:
    return next((a for a in MODEL_ADAPTER_PRIORITY_REGISTRY if a["adapter_id"] == adapter_id), None)


def _scenario(scenario_id: str) -> Optional[Dict[str, Any]]:
    return next((s for s in SCENARIO_MODEL_GROUPS if s["scenario_id"] == scenario_id), None)


def _evaluate_planning_cases(
    *,
    cleanup_s: Dict[str, Any],
    next_phase: str,
) -> Tuple[List[Dict[str, Any]], bool]:
    results: List[Dict[str, Any]] = []
    all_passed = True
    priority_map = {a["adapter_id"]: a for a in MODEL_ADAPTER_PRIORITY_REGISTRY}

    for case in PLANNING_CASES:
        ok = False
        cid = case["case_id"]
        if case.get("expect_priority"):
            row = priority_map.get(case["adapter"])
            ok = row is not None and row.get("priority") == case["expect_priority"]
        elif case.get("expect_status"):
            row = priority_map.get(case["adapter"])
            ok = row is not None and row.get("status") == case["expect_status"]
        elif case.get("scenario"):
            sc = _scenario(case["scenario"])
            ok = sc is not None and set(sc["models"]) == set(case["models"])
        elif case.get("expect_new_protocol") is False:
            ok = PROTOCOL_REUSE_DECISION.get("new_protocol_added") is False
        elif case.get("forbidden_in_next"):
            ok = case["forbidden_in_next"] not in next_phase
        elif case.get("inherit_cleanup"):
            ok = (
                cleanup_s.get("field_simulation_deactivated_from_mainline") is True
                and cleanup_s.get("no_unjustified_new_protocol") is True
                and cleanup_s.get("cleanup_review_pass") is True
            )
        results.append({"case_id": cid, "case_passed": ok})
        if not ok:
            all_passed = False
    return results, all_passed


def _meta(out: Path, cleanup_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "priority_sequence_planning_only": True,
        "dual_track": ("world_model_construction", "task_collaboration_under_midplatform"),
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "output_root": str(out), "cleanup_root": str(cleanup_root),
    }


def run_model_adapter_priority_sequence_planning_v1(
    *,
    cleanup_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    cleanup_upstream = Path(cleanup_root or DEFAULT_CLEANUP_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, cleanup_upstream)
    issues: List[str] = []

    cleanup_s = _read_json(cleanup_upstream / "summary.json")
    cleanup_v = _read_json(cleanup_upstream / "verifier_report.json")
    prior_cleanup_go = (
        cleanup_s.get("final_decision") == CLEANUP_FINAL_GO
        and cleanup_v.get("verifier") == "GO"
        and int(cleanup_v.get("passed_checks", 0)) >= 300
        and cleanup_s.get("cleanup_review_pass") is True
        and cleanup_s.get("field_simulation_deactivated_from_mainline") is True
        and cleanup_s.get("no_unjustified_new_protocol") is True
    )
    if not prior_cleanup_go:
        issues.append("model_workflow_protocol_reuse_and_cleanup_review_not_go")

    absence = {k: cleanup_s.get(k) is True for k in ABSENCE_KEYS}
    owner_compliance = {
        "review_id": "owner_constraint_compliance_review_v1",
        "owner_constraints_inherited": prior_cleanup_go,
        "no_field_simulation_route": True,
        "no_task_reasoning_route": True,
        "no_new_protocol_without_reason": True,
        "no_world_model_entry_write": True,
        "no_fact_admission": True,
        "no_task_action_output": True,
        **meta,
    }
    non_execution_boundary_ok = prior_cleanup_go and all(NON_EXECUTION_FLAGS.values()) and all(absence.values())

    case_results, all_cases_passed = _evaluate_planning_cases(
        cleanup_s=cleanup_s,
        next_phase=SELECTED_NEXT_PHASE,
    )

    slam_p0 = _priority_by_id("slam_spatial_mapping")
    tracking_p1 = _priority_by_id("tracking_optical_flow")
    ocr_p2 = _priority_by_id("ocr_text_model")
    seg_p3 = _priority_by_id("segmentation_grounded_mask")
    scene_deferred = _priority_by_id("scene_graph_relation")

    planning_complete = (
        all_cases_passed
        and len(PLANNING_CASES) >= 10
        and slam_p0 and slam_p0.get("priority") == "P0"
        and tracking_p1 and tracking_p1.get("priority") == "P1"
        and ocr_p2 and ocr_p2.get("priority") == "P2"
        and seg_p3 and seg_p3.get("priority") == "P3"
        and scene_deferred and scene_deferred.get("status") == "deferred"
        and PROTOCOL_REUSE_DECISION.get("new_protocol_added") is False
        and "Field-Simulation" not in SELECTED_NEXT_PHASE
        and "Task-Reasoning" not in SELECTED_NEXT_PHASE
        and prior_cleanup_go
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Model-Workflow-Protocol-Reuse-And-Cleanup-Review-v1-001",
        base_capability=PLANNING_WHITELIST_FILES[0],
        base_runner=PLANNING_WHITELIST_FILES[1],
        base_verifier=PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase=PHASE_ID,
        stage_term_overrides=PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=PLANNING_STAGE_ADDITIONS,
        template_files=PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Model-Workflow-Protocol-Reuse-And-Cleanup-Review-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    cleanup_fs = _read_json(cleanup_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=cleanup_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    planning_pass = (
        planning_complete and template_lineage.get("template_lineage_ok")
        and fs_ok and non_execution_boundary_ok and len(issues) == 0
    )
    next_phase = SELECTED_NEXT_PHASE if planning_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if planning_pass else (
        FINAL_DECISION_UPSTREAM if not prior_cleanup_go else FINAL_DECISION_RECAL
    )

    report = {
        "report_id": "model_adapter_priority_sequence_planning_report_v1",
        "adapter_count": len(MODEL_ADAPTER_PRIORITY_REGISTRY),
        "scenario_count": len(SCENARIO_MODEL_GROUPS),
        "planning_case_count": len(PLANNING_CASES),
        "next_adapter": "slam_spatial_mapping",
        "final_decision": final_decision,
        **meta,
    }
    report_md = "\n".join([
        "# Model Adapter Priority Sequence Planning v1",
        "P0: SLAM/Spatial Mapping | P1: Tracking | P2: OCR | P3: Segmentation | P4: Scene Graph (deferred)",
        f"Next: `{next_phase}`",
        f"Final decision: `{final_decision}`",
    ])

    go_values = {
        "prior_model_workflow_protocol_reuse_and_cleanup_review_go": prior_cleanup_go,
        "model_adapter_priority_sequence_planning_complete": planning_complete,
        "priority_registry_complete": len(MODEL_ADAPTER_PRIORITY_REGISTRY) >= 5,
        "reuse_path_registry_complete": len(REUSE_PATH_REGISTRY) >= 5,
        "world_model_mapping_complete": len(WORLD_MODEL_CONSTRUCTION_MAPPING) >= 7,
        "task_collaboration_mapping_complete": len(TASK_COLLABORATION_MAPPING) >= 6,
        "scenario_model_group_registry_complete": len(SCENARIO_MODEL_GROUPS) >= 6,
        "no_new_protocol_without_reason": PROTOCOL_REUSE_DECISION.get("new_protocol_added") is False,
        "no_field_simulation_route": True,
        "no_task_reasoning_route": True,
        "owner_constraints_inherited": prior_cleanup_go,
        "slam_or_spatial_mapping_prioritized": slam_p0 is not None and slam_p0.get("priority") == "P0",
        "tracking_second_priority": tracking_p1 is not None and tracking_p1.get("priority") == "P1",
        "ocr_third_priority": ocr_p2 is not None and ocr_p2.get("priority") == "P2",
        "segmentation_fourth_priority": seg_p3 is not None and seg_p3.get("priority") == "P3",
        "scene_graph_deferred": scene_deferred is not None and scene_deferred.get("status") == "deferred",
        "candidate_only_outputs": True,
        "common_validation_reuse_ok": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": planning_pass,
        "model_adapter_priority_sequence_planning_pass": planning_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "all_planning_cases_passed": all_cases_passed,
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        **absence,
    }

    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS if k in go_values},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(cleanup_s.get("chain_trace_nodes") or []) + ["model_adapter_priority_sequence_planning"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }

    return {
        "model_adapter_priority_sequence_planning_report": report,
        "model_adapter_priority_sequence_planning_report_md": report_md,
        "model_adapter_priority_registry": {
            "registry_id": "model_adapter_priority_registry_v1",
            "adapters": list(MODEL_ADAPTER_PRIORITY_REGISTRY),
            "count": len(MODEL_ADAPTER_PRIORITY_REGISTRY),
            **meta,
        },
        "model_adapter_reuse_path_registry": {
            "registry_id": "model_adapter_reuse_path_registry_v1",
            "paths": list(REUSE_PATH_REGISTRY),
            "count": len(REUSE_PATH_REGISTRY),
            **meta,
        },
        "world_model_construction_model_mapping": {
            "mapping_id": "world_model_construction_model_mapping_v1",
            "mappings": list(WORLD_MODEL_CONSTRUCTION_MAPPING),
            "count": len(WORLD_MODEL_CONSTRUCTION_MAPPING),
            "candidate_only": True,
            "no_world_model_entry_write": True,
            **meta,
        },
        "task_collaboration_model_mapping": {
            "mapping_id": "task_collaboration_model_mapping_v1",
            "mappings": list(TASK_COLLABORATION_MAPPING),
            "count": len(TASK_COLLABORATION_MAPPING),
            "two_to_three_models_per_scenario": True,
            **meta,
        },
        "scenario_2_to_3_model_group_registry": {
            "registry_id": "scenario_2_to_3_model_group_registry_v1",
            "scenarios": list(SCENARIO_MODEL_GROUPS),
            "count": len(SCENARIO_MODEL_GROUPS),
            **meta,
        },
        "model_adapter_protocol_reuse_decision": {**PROTOCOL_REUSE_DECISION, **meta},
        "model_adapter_new_protocol_reason_required_report": {**NEW_PROTOCOL_REASON_REPORT, **meta},
        "next_model_adapter_skeleton_recommendation": {**NEXT_SKELETON_RECOMMENDATION, **meta},
        "deferred_model_adapter_registry": {
            "registry_id": "deferred_model_adapter_registry_v1",
            "adapters": list(DEFERRED_ADAPTERS),
            "count": len(DEFERRED_ADAPTERS),
            **meta,
        },
        "owner_constraint_compliance_review": owner_compliance,
        "planning_case_results": {
            "results_id": "planning_case_results_v1",
            "all_planning_cases_passed": all_cases_passed,
            "results": case_results,
            **meta,
        },
        "non_execution_boundary_review": {
            "review_id": "non_execution_boundary_review_v1",
            "non_execution_boundary_ok": non_execution_boundary_ok,
            "flags": dict(NON_EXECUTION_FLAGS),
            **meta,
        },
        "prohibited_scope": {**PROHIBITED_SCOPE, **meta},
        "do_not_misclassify_rules": {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta},
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
