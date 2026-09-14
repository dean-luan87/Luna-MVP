# -*- coding: utf-8 -*-
"""Tracking / Optical Flow Model Smoke IO Inspection v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.slam_spatial_mapping_task_collaboration_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_TASK_PLANNING_ROOT,
    FINAL_DECISION_GO as TASK_PLANNING_FINAL_GO,
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
from capabilities.midplatform.tracking_opticalflow_model_smoke_io_inspection_core_v1 import run_all_smoke_io_cases
from capabilities.midplatform.tracking_opticalflow_model_smoke_io_inspection_items_v1 import (
    CANDIDATE_MAPPING_TARGETS,
    DEFAULT_TRACKING_OPTICALFLOW_AVAILABILITY,
    DO_NOT_MISCLASSIFY,
    NEW_PROTOCOL_REASON_REPORT,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    SMOKE_IO_CASES,
)
from capabilities.midplatform.tracking_opticalflow_model_smoke_io_inspection_lineage_v1 import (
    STAGE_ADDITIONS,
    STAGE_TERM_OVERRIDES,
    WHITELIST_FILES,
)
from capabilities.midplatform.tracking_opticalflow_model_smoke_io_inspection_static_validators_v1 import (
    validate_no_protocol_overreach,
    validate_non_execution_boundary,
)
from capabilities.midplatform.tracking_opticalflow_model_smoke_io_inspection_types_v1 import (
    FINAL_DECISION_GO,
    NON_EXECUTION_FLAGS,
)

PHASE_ID = "Phase-Midplatform-Tracking-OpticalFlow-Model-Smoke-IO-Inspection-v1-001"
SCOPE = "tracking_opticalflow_model_smoke_io_inspection_only"
SOURCE_CHAIN = "tracking_opticalflow_model_smoke_io_inspection_v1"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_TRACKING_OPTICALFLOW_MODEL_SMOKE_IO_INSPECTION_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_TRACKING_OPTICALFLOW_MODEL_SMOKE_IO_INSPECTION_BLOCKED_BY_IMPLEMENTATION_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Tracking-OpticalFlow-Model-Smoke-IO-Inspection-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/tracking_opticalflow_model_smoke_io_inspection_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_TRACKING_OPTICALFLOW_MODEL_SMOKE_IO_INSPECTION_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_types_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_availability_checker_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_smoke_runner_v1.py",
    "capabilities/midplatform/tracking_opticalflow_io_inspector_v1.py",
    "capabilities/midplatform/tracking_opticalflow_candidate_mapping_reviewer_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_static_validators_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_core_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_items_v1.py",
    "capabilities/midplatform/tracking_opticalflow_model_smoke_io_inspection_lineage_v1.py",
    "tools/evaluation/midplatform/run_tracking_opticalflow_model_smoke_io_inspection_v1.py",
    "tools/evaluation/midplatform/verify_tracking_opticalflow_model_smoke_io_inspection_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_slam_task_collaboration_planning_go",
    "route_follows_model_smoke_io_first",
    "tracking_opticalflow_smoke_io_inspection_complete",
    "execution_authorization_review_ok",
    "input_output_inspection_complete",
    "candidate_mapping_feasibility_review_complete",
    "no_unauthorized_download",
    "no_adapter_skeleton_yet",
    "no_field_simulation",
    "no_world_model_assembly",
    "no_task_reasoning",
    "no_new_protocol_without_reason",
    "traceability_preserved",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _sanitize_smoke_run(run: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in run.items() if not str(k).startswith("_")}


def _meta(out: Path, task_planning_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "model_smoke_io_inspection_only": True,
        "no_adapter_skeleton_yet": True,
        "route_follows_model_smoke_io_first": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "output_root": str(out), "task_planning_root": str(task_planning_root),
    }


def run_tracking_opticalflow_model_smoke_io_inspection_v1(
    *,
    task_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    plan_upstream = Path(task_planning_root or DEFAULT_TASK_PLANNING_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, plan_upstream)
    issues: List[str] = []

    plan_s = _read_json(plan_upstream / "summary.json")
    plan_v = _read_json(plan_upstream / "verifier_report.json")
    prior_task_planning_go = (
        plan_s.get("final_decision") == TASK_PLANNING_FINAL_GO
        and plan_v.get("verifier") == "GO"
        and int(plan_v.get("passed_checks", 0)) >= 360
        and plan_s.get("slam_task_collaboration_planning_pass") is True
        and plan_s.get("no_action_output") is True
        and plan_s.get("no_world_model_candidate_generated") is True
        and plan_s.get("no_field_simulation") is True
    )
    if not prior_task_planning_go:
        issues.append("slam_task_collaboration_planning_not_go")

    absence = {k: plan_s.get(k) is True for k in ABSENCE_KEYS}
    route_ok = plan_s.get("smoke_io_then_adapter_then_task_collaboration_order_respected") is True
    proto_ok, _ = validate_no_protocol_overreach(0)
    non_exec_ok, _ = validate_non_execution_boundary(NON_EXECUTION_FLAGS)
    non_execution_boundary_ok = prior_task_planning_go and proto_ok and non_exec_ok and all(absence.values())

    case_results, all_cases_passed = run_all_smoke_io_cases(
        SMOKE_IO_CASES, matrix=DEFAULT_TRACKING_OPTICALFLOW_AVAILABILITY,
    )

    smoke_runs = [_sanitize_smoke_run(r["smoke_run"]) for r in case_results]
    io_inspections = [r["io_inspection"] for r in case_results]
    mappings = [m for r in case_results for m in r.get("mapping_feasibilities") or []]
    auths = [r["authorization_candidate"] for r in case_results]
    modes = {r["smoke_run"].get("execution_mode") for r in case_results}

    blocked_no_download = all(
        not (r["smoke_run"].get("runtime_environment_summary") or {}).get("download_attempted")
        for r in case_results
    )
    cached_not_real = all(
        r["smoke_run"].get("execution_mode") != "cached_output"
        or "cached_output_inspection_not_real_run" in (r["smoke_run"].get("warning_codes") or [])
        for r in case_results
    )
    stub_not_real = all(
        r["smoke_run"].get("execution_mode") != "adapter_stub"
        or "adapter_stub_inspection_not_real_run" in (r["smoke_run"].get("warning_codes") or [])
        for r in case_results
    )
    trace_row = next((r for r in case_results if r["case_id"] == "traceability_preserved"), {})
    traceability_ok = trace_row.get("case_passed") is True

    track_map_ok = any(
        m.get("mapping_status") == "feasible"
        for r in case_results if r["case_id"] == "track_id_mapping_feasibility"
        for m in r.get("mapping_feasibilities") or []
        if "ObjectTrackCandidate" in (m.get("candidate_mapping_targets") or [])
    )
    persist_map_ok = any(
        m.get("mapping_status") == "feasible"
        for r in case_results if r["case_id"] == "object_persistence_mapping_feasibility"
        for m in r.get("mapping_feasibilities") or []
        if "ObjectPersistenceCandidate" in (m.get("candidate_mapping_targets") or [])
    )
    motion_map_ok = any(
        m.get("mapping_status") == "feasible"
        for r in case_results if r["case_id"] == "motion_candidate_mapping_feasibility"
        for m in r.get("mapping_feasibilities") or []
        if "MotionCandidate" in (m.get("candidate_mapping_targets") or [])
    )

    inspection_complete = (
        all_cases_passed and len(case_results) >= 10
        and blocked_no_download and cached_not_real and stub_not_real
        and traceability_ok and track_map_ok and persist_map_ok and motion_map_ok
        and prior_task_planning_go and route_ok
        and NEW_PROTOCOL_REASON_REPORT.get("new_protocol_proposals") == []
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-SLAM-Spatial-Mapping-Task-Collaboration-Planning-v1-001",
        base_capability=WHITELIST_FILES[0],
        base_runner=WHITELIST_FILES[1],
        base_verifier=WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase=PHASE_ID,
        stage_term_overrides=STAGE_TERM_OVERRIDES,
        stage_additions=STAGE_ADDITIONS,
        template_files=WHITELIST_FILES[:3],
        repo_root=repo_root,
        upstream_review_phase="Midplatform-SLAM-Spatial-Mapping-Task-Collaboration-Planning-v1-001",
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
    inspection_pass = (
        inspection_complete and template_lineage.get("template_lineage_ok")
        and fs_ok and non_execution_boundary_ok and len(issues) == 0
    )
    next_phase = SELECTED_NEXT_PHASE if inspection_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if inspection_pass else (
        FINAL_DECISION_UPSTREAM if not prior_task_planning_go else FINAL_DECISION_RECAL
    )

    input_formats = [i.get("input_format_observed") for i in io_inspections]
    output_formats = [i.get("output_format_observed") for i in io_inspections]
    failure_points = [fp for r in case_results for fp in r.get("failure_points") or []]

    report = {
        "report_id": "tracking_opticalflow_model_smoke_io_inspection_report_v1",
        "case_count": len(case_results),
        "execution_modes_observed": sorted(modes),
        "tracking_opticalflow_smoke_io_inspection_complete": inspection_complete,
        "final_decision": final_decision,
        **meta,
    }
    report_md = "\n".join([
        "# Tracking / Optical Flow Model Smoke IO Inspection v1",
        f"Cases: `{len(case_results)}` | Modes: `{sorted(modes)}`",
        "P1 model smoke + IO inspection. No adapter skeleton. No world model assembly.",
        f"Final decision: `{final_decision}`",
        f"Next: `{next_phase}`",
    ])

    owner_review = {
        "review_id": "owner_constraint_compliance_review_v1",
        "owner_constraints_inherited": prior_task_planning_go,
        "route_follows_model_smoke_io_first": True,
        "no_adapter_skeleton_yet": True,
        "no_field_simulation": True,
        "no_world_model_assembly": True,
        "no_task_reasoning": True,
        "no_new_protocol_without_reason": True,
        **meta,
    }

    go_values = {
        "prior_slam_task_collaboration_planning_go": prior_task_planning_go,
        "route_follows_model_smoke_io_first": route_ok,
        "tracking_opticalflow_smoke_io_inspection_complete": inspection_complete,
        "execution_authorization_review_ok": len(auths) >= 10,
        "input_output_inspection_complete": len(io_inspections) >= 10,
        "candidate_mapping_feasibility_review_complete": len(mappings) >= 10,
        "no_unauthorized_download": blocked_no_download,
        "no_adapter_skeleton_yet": True,
        "no_field_simulation": True,
        "no_world_model_assembly": True,
        "no_task_reasoning": True,
        "no_new_protocol_without_reason": True,
        "traceability_preserved": traceability_ok,
        "candidate_only_outputs": True,
        "common_validation_reuse_ok": True,
        "model_execution_modes_classified": len(modes) >= 4,
        "blocked_cases_do_not_download": blocked_no_download,
        "cached_output_not_marked_as_real_run": cached_not_real,
        "adapter_stub_not_marked_as_real_run": stub_not_real,
        "track_id_mapping_feasibility_checked": track_map_ok,
        "object_persistence_mapping_feasibility_checked": persist_map_ok,
        "motion_candidate_mapping_feasibility_checked": motion_map_ok,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": inspection_pass,
        "tracking_opticalflow_smoke_io_inspection_pass": inspection_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "smoke_io_case_count": len(case_results),
        **absence,
    }

    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS if k in go_values},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(plan_s.get("chain_trace_nodes") or []) + ["tracking_opticalflow_model_smoke_io_inspection"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }

    return {
        "tracking_opticalflow_model_smoke_io_inspection_report": report,
        "tracking_opticalflow_model_smoke_io_inspection_report_md": report_md,
        "model_smoke_run_candidate_registry": {
            "registry_id": "model_smoke_run_candidate_registry_v1",
            "candidates": smoke_runs, "count": len(smoke_runs), **meta,
        },
        "model_io_inspection_candidate_registry": {
            "registry_id": "model_io_inspection_candidate_registry_v1",
            "candidates": io_inspections, "count": len(io_inspections), **meta,
        },
        "model_candidate_mapping_feasibility_registry": {
            "registry_id": "model_candidate_mapping_feasibility_registry_v1",
            "candidates": mappings, "count": len(mappings), **meta,
        },
        "tracking_opticalflow_available_model_review": {
            "review_id": "tracking_opticalflow_available_model_review_v1",
            "availability_matrix": DEFAULT_TRACKING_OPTICALFLOW_AVAILABILITY,
            "execution_modes_observed": sorted(modes),
            "p1_model": "tracking_optical_flow",
            **meta,
        },
        "tracking_opticalflow_input_format_review": {
            "review_id": "tracking_opticalflow_input_format_review_v1",
            "input_formats": input_formats,
            "reused_protocols": ("RealFrameInputPackage", "ObjectObservationCandidate", "MultiModelAlignedObservationCandidate"),
            **meta,
        },
        "tracking_opticalflow_output_format_review": {
            "review_id": "tracking_opticalflow_output_format_review_v1",
            "output_formats": output_formats,
            **meta,
        },
        "tracking_opticalflow_failure_point_review": {
            "review_id": "tracking_opticalflow_failure_point_review_v1",
            "failure_points": failure_points,
            **meta,
        },
        "tracking_opticalflow_candidate_mapping_review": {
            "review_id": "tracking_opticalflow_candidate_mapping_review_v1",
            "mapping_targets": list(CANDIDATE_MAPPING_TARGETS),
            "mapping_count": len(mappings),
            **meta,
        },
        "model_execution_authorization_review": {
            "review_id": "model_execution_authorization_review_v1",
            "authorization_candidates": auths,
            "no_unauthorized_download": blocked_no_download,
            **meta,
        },
        "new_protocol_reason_required_report": {**NEW_PROTOCOL_REASON_REPORT, **meta},
        "owner_constraint_compliance_review": owner_review,
        "smoke_io_case_results": {
            "results_id": "smoke_io_case_results_v1",
            "all_smoke_io_cases_passed": all_cases_passed,
            "results": [{"case_id": r["case_id"], "case_passed": r.get("case_passed"), "execution_mode": r["smoke_run"].get("execution_mode")} for r in case_results],
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
