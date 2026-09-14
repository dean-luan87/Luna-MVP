# -*- coding: utf-8 -*-
"""Real Model Field Construction Execution Path Hardening v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.real_field_construction_baseline_builder_v1 import (
    build_real_field_construction_baselines,
)
from capabilities.midplatform.real_field_construction_quality_report_builder_v1 import (
    build_real_field_construction_quality_report,
)
from capabilities.midplatform.real_image_set_loader_v1 import load_real_frame_input_set
from capabilities.midplatform.real_model_execution_authorization_resolver_v1 import (
    resolve_real_model_execution_authorization,
)
from capabilities.midplatform.real_model_execution_path_hardening_core_v1 import run_all_execution_cases
from capabilities.midplatform.real_model_execution_path_hardening_static_validators_v1 import (
    validate_authorization_boundary,
    validate_no_simulation_boundary,
    validate_real_field_construction_baseline,
    validate_real_field_construction_quality_report,
)
from capabilities.midplatform.real_model_execution_path_hardening_types_v1 import (
    FINAL_DECISION_GO,
    NON_EXECUTION_FLAGS,
)
from capabilities.midplatform.real_model_field_construction_execution_path_hardening_items_v1 import (
    DEFAULT_EXECUTION_AUTHORIZATION,
    DO_NOT_MISCLASSIFY,
    EXECUTION_HARDENING_CASES,
    PROHIBITED_SCOPE,
    ROUTE_CORRECTION,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.real_model_field_construction_execution_path_hardening_lineage_v1 import (
    EXECUTION_PATH_STAGE_ADDITIONS,
    EXECUTION_PATH_STAGE_TERM_OVERRIDES,
    EXECUTION_PATH_WHITELIST_FILES,
)
from capabilities.midplatform.real_model_field_construction_success_path_hardening_v1 import (
    DEFAULT_OUTPUT as DEFAULT_HARDENING_ROOT,
    FINAL_DECISION_GO as HARDENING_FINAL_GO,
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
from capabilities.midplatform.yolo_depth_controlled_real_model_dryrun_items_v1 import (
    CONTROLLED_DRYRUN_CASES,
)
from capabilities.midplatform.yolo_depth_controlled_real_model_dryrun_v1 import (
    DEFAULT_OUTPUT as DEFAULT_DRYRUN_ROOT,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-Real-Model-Field-Construction-Execution-Path-Hardening-v1-001"
SCOPE = "real_model_field_construction_execution_path_hardening_only"
SOURCE_CHAIN = "real_model_field_construction_execution_path_hardening_v1"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_REAL_MODEL_FIELD_CONSTRUCTION_EXECUTION_PATH_HARDENING_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_REAL_MODEL_FIELD_CONSTRUCTION_EXECUTION_PATH_HARDENING_BLOCKED_BY_IMPLEMENTATION_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Real-Model-Field-Construction-Execution-Path-Hardening-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/real_model_field_construction_execution_path_hardening_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_REAL_MODEL_FIELD_CONSTRUCTION_EXECUTION_PATH_HARDENING_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/real_model_field_construction_execution_path_hardening_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/real_model_execution_path_hardening_types_v1.py",
    "capabilities/midplatform/real_model_execution_authorization_resolver_v1.py",
    "capabilities/midplatform/real_image_set_loader_v1.py",
    "capabilities/midplatform/yolo_execution_path_bridge_v1.py",
    "capabilities/midplatform/depth_execution_path_bridge_v1.py",
    "capabilities/midplatform/real_model_field_construction_pipeline_v1.py",
    "capabilities/midplatform/real_field_construction_quality_report_builder_v1.py",
    "capabilities/midplatform/real_field_construction_baseline_builder_v1.py",
    "capabilities/midplatform/real_model_execution_path_hardening_static_validators_v1.py",
    "capabilities/midplatform/real_model_execution_path_hardening_core_v1.py",
    "capabilities/midplatform/real_model_field_construction_execution_path_hardening_v1.py",
    "capabilities/midplatform/real_model_field_construction_execution_path_hardening_items_v1.py",
    "capabilities/midplatform/real_model_field_construction_execution_path_hardening_lineage_v1.py",
    "tools/evaluation/midplatform/run_real_model_field_construction_execution_path_hardening_v1.py",
    "tools/evaluation/midplatform/verify_real_model_field_construction_execution_path_hardening_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_yolo_depth_controlled_real_model_dryrun_go",
    "prior_real_model_field_construction_success_path_hardening_go",
    "real_model_execution_path_hardening_complete",
    "authorization_boundary_ok",
    "real_frame_input_set_loaded",
    "yolo_execution_path_ok",
    "depth_execution_path_classified",
    "enhanced_field_scene_candidate_generated",
    "real_field_construction_quality_report_generated",
    "real_field_construction_baseline_registry_generated",
    "mock_depth_not_marked_as_real",
    "stub_depth_not_marked_as_full_real_model",
    "failure_localization_ok",
    "traceability_review_ok",
    "no_simulation_boundary_ok",
    "route_switched_from_simulation_to_real_content",
    "field_simulation_deferred",
    "no_field_simulation",
    "no_task_execution",
    "no_world_model_fact_creation",
    "no_model_download",
    "no_weight_download",
    "no_runtime_execution",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, dryrun_root: Path, hardening_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "real_model_field_construction_execution_path_hardening_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "field_simulation_deferred": True,
        "route_switched_from_simulation_to_real_content": True,
        "output_root": str(out), "dryrun_root": str(dryrun_root), "hardening_root": str(hardening_root),
        "route_correction": ROUTE_CORRECTION,
    }


def _collect_execution_results(case_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    exec_results: List[Dict[str, Any]] = []
    for row in case_results:
        if row.get("batch_results"):
            for br in row["batch_results"]:
                if br.get("execution_result"):
                    exec_results.append(br["execution_result"])
        elif row.get("execution_result"):
            exec_results.append(row["execution_result"])
    return exec_results


def run_real_model_field_construction_execution_path_hardening_v1(
    *,
    dryrun_root: str,
    hardening_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    dry_upstream = Path(dryrun_root or DEFAULT_DRYRUN_ROOT).expanduser().resolve()
    hard_upstream = Path(hardening_root or DEFAULT_HARDENING_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, dry_upstream, hard_upstream)
    issues: List[str] = []

    dry_s = _read_json(dry_upstream / "summary.json")
    dry_v = _read_json(dry_upstream / "verifier_report.json")
    prior_dryrun_go = (
        dry_s.get("final_decision") == DRYRUN_FINAL_GO
        and dry_v.get("verifier") == "GO"
        and int(dry_v.get("passed_checks", 0)) >= 460
        and dry_s.get("yolo_depth_controlled_real_model_dryrun_pass") is True
    )
    if not prior_dryrun_go:
        issues.append("yolo_depth_controlled_real_model_dryrun_not_go")

    hard_s = _read_json(hard_upstream / "summary.json")
    hard_v = _read_json(hard_upstream / "verifier_report.json")
    prior_hardening_go = (
        hard_s.get("final_decision") == HARDENING_FINAL_GO
        and hard_v.get("verifier") == "GO"
        and int(hard_v.get("passed_checks", 0)) >= 420
        and hard_s.get("real_model_field_construction_success_path_hardening_pass") is True
    )
    if not prior_hardening_go:
        issues.append("real_model_field_construction_success_path_hardening_not_go")

    absence = {k: dry_s.get(k) is True for k in ABSENCE_KEYS}
    auth_candidate, auth_resolved, _ = resolve_real_model_execution_authorization(
        matrix=DEFAULT_EXECUTION_AUTHORIZATION,
    )
    auth_ok, _ = validate_authorization_boundary(auth_candidate)
    sim_ok, _ = validate_no_simulation_boundary(NON_EXECUTION_FLAGS)
    non_execution_boundary_ok = (
        prior_dryrun_go and dry_s.get("non_execution_boundary_ok") is True
        and auth_ok and sim_ok and all(absence.values())
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    case_defs = {c["case_id"]: c for c in CONTROLLED_DRYRUN_CASES}
    frame_specs = [
        {
            "case_id": c["case_id"],
            "frame_ref": c.get("frame_ref"),
            "expected_scene_notes": c.get("description"),
        }
        for c in CONTROLLED_DRYRUN_CASES
    ]
    work_dir = str(out / "fixtures")
    input_pkg, frames, frame_fps = load_real_frame_input_set(
        image_set_ref="real_field_construction_fixture_set_v1",
        frame_specs=frame_specs,
        work_dir=work_dir,
    )
    frames_by_case = {f.get("test_case_id", f["frame_input_id"].replace("rfi_", "")): f for f in frames}

    case_results, auth_resolved_list, all_cases_passed = run_all_execution_cases(
        cases=EXECUTION_HARDENING_CASES,
        frames_by_case=frames_by_case,
        case_defs=case_defs,
        base_matrix=DEFAULT_EXECUTION_AUTHORIZATION,
    )

    exec_results = _collect_execution_results(case_results)
    yolo_registry = [
        {"frame_input_ref": r.get("frame_input_ref"), "yolo_output_ref": r.get("yolo_output_ref"),
         "yolo_execution_mode": r.get("yolo_execution_mode"), "candidate_only": True}
        for r in exec_results
    ]
    depth_registry = [
        {"frame_input_ref": r.get("frame_input_ref"), "depth_output_ref": r.get("depth_output_ref"),
         "depth_execution_mode": r.get("depth_execution_mode"), "candidate_only": True}
        for r in exec_results
    ]

    quality_report = build_real_field_construction_quality_report(execution_results=exec_results)
    baselines = build_real_field_construction_baselines(execution_results=exec_results)
    validate_real_field_construction_quality_report(quality_report)
    for bl in baselines:
        validate_real_field_construction_baseline(bl)

    enhanced_count = quality_report.get("enhanced_scene_count", 0)
    mock_not_real = not quality_report.get("mock_depth_marked_as_real")
    stub_not_full = not quality_report.get("stub_depth_marked_as_full_real")
    depth_classified = all(
        r.get("depth_execution_mode") in (
            "real_adapter", "stub_depth", "mock_adapter_with_real_frame_alignment",
            "missing", "blocked_depth_authorization", "authorized_model",
        )
        for r in exec_results
    )
    yolo_ok = any(r.get("yolo_execution_mode") in ("real_runner", "cached_output") for r in exec_results)
    failure_localization_ok = all(
        bool(r.get("failure_points") is not None)
        for r in exec_results
    ) and any(
        "invalid_bbox" in " ".join(r.get("failure_points") or []) for r in exec_results
    )
    traceability_ok = all(len(r.get("traceability_refs") or []) >= 4 for r in exec_results if r.get("enhanced_field_scene_ref"))

    real_model_execution_path_hardening_complete = (
        all_cases_passed and len(case_results) >= 10 and len(exec_results) >= 5
        and enhanced_count >= 1 and mock_not_real and stub_not_full
        and depth_classified and yolo_ok and failure_localization_ok
    )

    exec_pass_pre = (
        prior_dryrun_go and prior_hardening_go and real_model_execution_path_hardening_complete
        and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Real-Model-Field-Construction-Success-Path-Hardening-v1-001",
        base_capability=EXECUTION_PATH_WHITELIST_FILES[0],
        base_runner=EXECUTION_PATH_WHITELIST_FILES[1],
        base_verifier=EXECUTION_PATH_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase=PHASE_ID,
        stage_term_overrides=EXECUTION_PATH_STAGE_TERM_OVERRIDES,
        stage_additions=EXECUTION_PATH_STAGE_ADDITIONS,
        template_files=EXECUTION_PATH_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Real-Model-Field-Construction-Success-Path-Hardening-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    hard_fs = _read_json(hard_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=hard_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    exec_pass = exec_pass_pre and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if exec_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if exec_pass else (
        FINAL_DECISION_UPSTREAM if not (prior_dryrun_go and prior_hardening_go) else FINAL_DECISION_RECAL
    )

    hardening_report = {
        "report_id": "real_model_field_construction_execution_path_hardening_report_v1",
        "execution_case_count": len(case_results),
        "execution_result_count": len(exec_results),
        "enhanced_scene_count": enhanced_count,
        "baseline_count": len(baselines),
        "field_simulation_deferred": True,
        "route_switched_from_simulation_to_real_content": True,
        "final_decision": final_decision,
        **meta,
    }
    report_md = "\n".join([
        "# Real Model Field Construction Execution Path Hardening v1",
        f"Cases: `{len(case_results)}` | Execution results: `{len(exec_results)}` | Enhanced scenes: `{enhanced_count}`",
        f"Field simulation deferred: `True`",
        f"Final decision: `{final_decision}`",
        f"Next: `{next_phase}`",
    ])

    failure_review = {
        "review_id": "real_field_failure_localization_review_v1",
        "failure_localization_ok": failure_localization_ok,
        "localized_points": quality_report.get("failure_localization_summary") or [],
        **meta,
    }
    trace_review = {
        "review_id": "real_field_traceability_review_v1",
        "traceability_review_ok": traceability_ok,
        "traceability_refs_per_result": [
            {"execution_path_result_id": r.get("execution_path_result_id"), "refs": r.get("traceability_refs")}
            for r in exec_results
        ],
        **meta,
    }
    no_sim_review = {
        "review_id": "no_simulation_boundary_review_v1",
        "no_simulation_boundary_ok": sim_ok,
        "flags": dict(NON_EXECUTION_FLAGS),
        **ROUTE_CORRECTION,
        **meta,
    }
    readiness_review = {
        "review_id": "readiness_for_real_field_quality_evaluation_review_v1",
        "readiness_for_real_field_quality_evaluation": quality_report.get("readiness_for_real_field_quality_evaluation"),
        **meta,
    }
    non_exec_review = {
        "review_id": "non_execution_boundary_review_v1",
        "non_execution_boundary_ok": non_execution_boundary_ok,
        **meta,
    }

    go_values = {
        "prior_yolo_depth_controlled_real_model_dryrun_go": prior_dryrun_go,
        "prior_real_model_field_construction_success_path_hardening_go": prior_hardening_go,
        "real_model_execution_path_hardening_complete": real_model_execution_path_hardening_complete,
        "authorization_boundary_ok": auth_ok,
        "real_frame_input_set_loaded": len(frames) >= 5,
        "yolo_execution_path_ok": yolo_ok,
        "depth_execution_path_classified": depth_classified,
        "enhanced_field_scene_candidate_generated": enhanced_count >= 1,
        "real_field_construction_quality_report_generated": bool(quality_report.get("quality_report_id")),
        "real_field_construction_baseline_registry_generated": len(baselines) >= 1,
        "mock_depth_not_marked_as_real": mock_not_real,
        "stub_depth_not_marked_as_full_real_model": stub_not_full,
        "failure_localization_ok": failure_localization_ok,
        "traceability_review_ok": traceability_ok,
        "no_simulation_boundary_ok": sim_ok,
        "route_switched_from_simulation_to_real_content": True,
        "field_simulation_deferred": True,
        "no_field_simulation": True,
        "no_task_execution": True,
        "no_task_reasoning": True,
        "no_navigation_action": True,
        "no_world_model_fact_creation": True,
        "no_model_download": True,
        "no_weight_download": True,
        "no_runtime_execution": True,
        "no_persistent_memory_write": True,
        "no_integration_test": True,
        "candidate_only_outputs": True,
        "common_validation_reuse_ok": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": exec_pass,
        "real_model_execution_path_hardening_pass": exec_pass,
        "real_model_field_construction_execution_path_hardening_pass": exec_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "execution_case_count": len(case_results),
        "all_execution_cases_passed": all_cases_passed,
        "execution_result_count": len(exec_results),
        "quality_report_count": 1,
        "baseline_count": len(baselines),
        "real_frame_count": len(frames),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        "midplatform_still_has_remaining_work": True,
        **absence,
    }

    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS if k in go_values},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(hard_s.get("chain_trace_nodes") or []) + ["real_model_field_construction_execution_path_hardening"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }

    return {
        "real_model_field_construction_execution_path_hardening_report": hardening_report,
        "real_model_field_construction_execution_path_hardening_report_md": report_md,
        "real_model_execution_authorization_resolved": {
            "resolved_id": "real_model_execution_authorization_resolved_v1",
            "authorization_candidate": auth_candidate,
            "default_resolved": auth_resolved,
            "case_resolved": [a for a in auth_resolved_list if a],
            **meta,
        },
        "real_frame_input_set_registry": {
            "registry_id": "real_frame_input_set_registry_v1",
            "input_package": input_pkg,
            "frames": frames,
            "frame_load_failure_points": frame_fps,
            "count": len(frames),
            **meta,
        },
        "yolo_execution_path_result_registry": {
            "registry_id": "yolo_execution_path_result_registry_v1",
            "results": yolo_registry,
            "count": len(yolo_registry),
            **meta,
        },
        "depth_execution_path_result_registry": {
            "registry_id": "depth_execution_path_result_registry_v1",
            "results": depth_registry,
            "count": len(depth_registry),
            **meta,
        },
        "real_model_execution_path_result_registry": {
            "registry_id": "real_model_execution_path_result_registry_v1",
            "results": exec_results,
            "count": len(exec_results),
            **meta,
        },
        "real_field_construction_quality_report": quality_report,
        "real_field_construction_baseline_registry": {
            "registry_id": "real_field_construction_baseline_registry_v1",
            "baselines": baselines,
            "count": len(baselines),
            **meta,
        },
        "real_model_execution_case_results": {
            "results_id": "real_model_execution_case_results_v1",
            "all_execution_cases_passed": all_cases_passed,
            "results": [
                {"case_id": r["case_id"], "case_passed": r.get("case_passed"), "source_case_id": r.get("source_case_id")}
                for r in case_results
            ],
            **meta,
        },
        "real_field_failure_localization_review": failure_review,
        "real_field_traceability_review": trace_review,
        "no_simulation_boundary_review": no_sim_review,
        "readiness_for_real_field_quality_evaluation_review": readiness_review,
        "non_execution_boundary_review": non_exec_review,
        "prohibited_scope": {**PROHIBITED_SCOPE, **meta},
        "do_not_misclassify_rules": {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta},
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
