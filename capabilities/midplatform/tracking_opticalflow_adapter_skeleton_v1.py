# -*- coding: utf-8 -*-
"""Tracking / Optical Flow Adapter Skeleton v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.tracking_opticalflow_adapter_core_v1 import (
    load_smoke_io_inspection_artifacts,
    run_all_skeleton_cases,
)
from capabilities.midplatform.tracking_opticalflow_adapter_skeleton_items_v1 import (
    DO_NOT_MISCLASSIFY,
    LATER_WORLD_MODEL_READINESS,
    NEW_PROTOCOL_REASON_REPORT,
    PROHIBITED_SCOPE,
    PROTOCOL_REUSE_DECISION,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    SKELETON_CASES,
    SMOKE_IO_ARTIFACT_FILES,
    TASK_COLLABORATION_MAPPING,
)
from capabilities.midplatform.tracking_opticalflow_adapter_skeleton_lineage_v1 import (
    SKELETON_STAGE_ADDITIONS,
    SKELETON_STAGE_TERM_OVERRIDES,
    SKELETON_WHITELIST_FILES,
)
from capabilities.midplatform.tracking_opticalflow_adapter_static_validators_v1 import (
    validate_no_protocol_overreach,
    validate_non_execution_boundary,
)
from capabilities.midplatform.tracking_opticalflow_adapter_types_v1 import (
    FINAL_DECISION_GO,
    NON_EXECUTION_FLAGS,
)
from capabilities.midplatform.tracking_opticalflow_model_smoke_io_inspection_v1 import (
    DEFAULT_OUTPUT as DEFAULT_SMOKE_IO_ROOT,
    FINAL_DECISION_GO as SMOKE_IO_FINAL_GO,
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

PHASE_ID = "Phase-Midplatform-Tracking-OpticalFlow-Adapter-Skeleton-v1-001"
SCOPE = "tracking_opticalflow_adapter_skeleton_only"
SOURCE_CHAIN = "tracking_opticalflow_adapter_skeleton_v1"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_TRACKING_OPTICALFLOW_ADAPTER_SKELETON_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_TRACKING_OPTICALFLOW_ADAPTER_SKELETON_BLOCKED_BY_IMPLEMENTATION_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Tracking-OpticalFlow-Adapter-Skeleton-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/tracking_opticalflow_adapter_skeleton_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_TRACKING_OPTICALFLOW_ADAPTER_SKELETON_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/tracking_opticalflow_adapter_skeleton_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/tracking_opticalflow_adapter_types_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_input_builder_v1.py",
    "capabilities/midplatform/tracking_opticalflow_raw_output_loader_v1.py",
    "capabilities/midplatform/tracking_opticalflow_output_normalizer_v1.py",
    "capabilities/midplatform/object_persistence_candidate_builder_v1.py",
    "capabilities/midplatform/motion_candidate_builder_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_result_assembler_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_static_validators_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_core_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_skeleton_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_skeleton_items_v1.py",
    "capabilities/midplatform/tracking_opticalflow_adapter_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_tracking_opticalflow_adapter_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_tracking_opticalflow_adapter_skeleton_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_tracking_opticalflow_smoke_io_inspection_go",
    "smoke_io_inspection_artifacts_read",
    "adapter_based_on_real_inspection_results",
    "tracking_opticalflow_adapter_skeleton_complete",
    "adapter_input_builder_complete",
    "raw_output_loader_complete",
    "output_normalizer_complete",
    "object_persistence_builder_complete",
    "motion_candidate_builder_complete",
    "adapter_result_assembler_complete",
    "all_skeleton_cases_passed",
    "protocol_reuse_decision_ok",
    "readiness_for_task_collaboration_ok",
    "readiness_for_later_world_model_candidate_assembly_ok",
    "existing_io_reuse_ok",
    "no_new_protocol_without_reason",
    "cached_output_not_marked_as_real_run",
    "adapter_stub_not_marked_as_real_run",
    "blocked_cases_do_not_fabricate_outputs",
    "short_track_not_persistent",
    "identity_switch_degrades_persistence",
    "lost_track_degraded",
    "no_real_tracking_execution",
    "no_real_opticalflow_execution",
    "no_model_download",
    "no_field_simulation",
    "no_task_reasoning",
    "no_action_output",
    "no_world_entity_candidate_generated",
    "no_world_model_candidate_generated",
    "no_world_model_entry_created",
    "no_fact_admission",
    "owner_constraints_inherited",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _sanitize(d: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in d.items() if not str(k).startswith("_")}


def _meta(out: Path, smoke_io_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "adapter_skeleton_only": True,
        "adapter_based_on_smoke_io_inspection": True,
        "no_real_tracking_execution": True,
        "no_real_opticalflow_execution": True,
        "no_world_model_assembly": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "output_root": str(out), "smoke_io_root": str(smoke_io_root),
    }


def run_tracking_opticalflow_adapter_skeleton_v1(
    *,
    smoke_io_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    smoke_upstream = Path(smoke_io_root or DEFAULT_SMOKE_IO_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, smoke_upstream)
    issues: List[str] = []

    smoke_s = _read_json(smoke_upstream / "summary.json")
    smoke_v = _read_json(smoke_upstream / "verifier_report.json")
    prior_smoke_io_go = (
        smoke_s.get("final_decision") == SMOKE_IO_FINAL_GO
        and smoke_v.get("verifier") == "GO"
        and int(smoke_v.get("passed_checks", 0)) >= 360
        and smoke_s.get("tracking_opticalflow_smoke_io_inspection_pass") is True
        and smoke_s.get("no_world_model_assembly") is True
        and smoke_s.get("no_field_simulation") is True
    )
    if not prior_smoke_io_go:
        issues.append("tracking_opticalflow_smoke_io_inspection_not_go")

    artifacts_read = all((smoke_upstream / f).is_file() for f in SMOKE_IO_ARTIFACT_FILES)
    if not artifacts_read:
        issues.append("smoke_io_inspection_artifacts_missing")

    inspection_artifacts = load_smoke_io_inspection_artifacts(smoke_upstream)
    absence = {k: smoke_s.get(k) is True for k in ABSENCE_KEYS}
    proto_ok, _ = validate_no_protocol_overreach(0)
    non_exec_ok, _ = validate_non_execution_boundary(NON_EXECUTION_FLAGS)
    non_execution_boundary_ok = prior_smoke_io_go and proto_ok and non_exec_ok and all(absence.values())

    case_results, all_cases_passed = run_all_skeleton_cases(
        SKELETON_CASES, inspection_artifacts=inspection_artifacts,
    )

    inputs = [_sanitize(r["adapter_input"]) for r in case_results]
    raw_outputs = [_sanitize(r["raw_output"]) for r in case_results if r.get("raw_output")]
    tracks = [t for r in case_results for t in r.get("tracks") or []]
    persistences = [p for r in case_results for p in r.get("persistences") or []]
    motions = [m for r in case_results for m in r.get("motions") or []]
    qualities = [q for r in case_results for q in r.get("qualities") or []]
    results = [r["adapter_result"] for r in case_results if r.get("adapter_result")]

    task_ready = any(r.get("readiness_for_midplatform_task_collaboration") for r in results)
    later_wm_ready = any(r.get("readiness_for_later_world_model_candidate_assembly") for r in results)
    no_wm_candidate = all(not r.get("world_model_candidate_generated") for r in results)
    no_wm_entry = all(not r.get("world_model_entry_created") for r in results)
    no_wm_entity = all(not r.get("world_entity_candidate_generated") for r in results)
    no_action = all(not r.get("task_action_output") for r in results)

    blocked_weight = next((r for r in case_results if r["case_id"] == "blocked_missing_weight_no_output_fabrication"), {})
    blocked_dep = next((r for r in case_results if r["case_id"] == "blocked_missing_dependency_no_output_fabrication"), {})
    blocked_ok = blocked_weight.get("case_passed") is True and blocked_dep.get("case_passed") is True

    short_track_row = next((r for r in case_results if r["case_id"] == "short_track_not_persistent"), {})
    identity_row = next((r for r in case_results if r["case_id"] == "identity_switch_degrades_persistence"), {})
    lost_row = next((r for r in case_results if r["case_id"] == "lost_track_lifecycle_degraded"), {})
    short_track_ok = short_track_row.get("case_passed") is True
    identity_ok = identity_row.get("case_passed") is True
    lost_ok = lost_row.get("case_passed") is True

    skeleton_complete = (
        all_cases_passed and len(case_results) >= 12
        and len(raw_outputs) >= 10 and task_ready and later_wm_ready
        and no_wm_candidate and no_wm_entry and no_wm_entity and no_action
        and blocked_ok and short_track_ok and identity_ok and lost_ok
        and artifacts_read and prior_smoke_io_go
        and PROTOCOL_REUSE_DECISION.get("new_protocol_added") is False
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Tracking-OpticalFlow-Model-Smoke-IO-Inspection-v1-001",
        base_capability=SKELETON_WHITELIST_FILES[0],
        base_runner=SKELETON_WHITELIST_FILES[1],
        base_verifier=SKELETON_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase=PHASE_ID,
        stage_term_overrides=SKELETON_STAGE_TERM_OVERRIDES,
        stage_additions=SKELETON_STAGE_ADDITIONS,
        template_files=SKELETON_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Tracking-OpticalFlow-Model-Smoke-IO-Inspection-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    smoke_fs = _read_json(smoke_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=smoke_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    skeleton_pass = (
        skeleton_complete and template_lineage.get("template_lineage_ok")
        and fs_ok and non_execution_boundary_ok and len(issues) == 0
    )
    next_phase = SELECTED_NEXT_PHASE if skeleton_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if skeleton_pass else (
        FINAL_DECISION_UPSTREAM if not prior_smoke_io_go else FINAL_DECISION_RECAL
    )

    report = {
        "report_id": "tracking_opticalflow_adapter_skeleton_report_v1",
        "revision": "based_on_smoke_io_inspection_v1",
        "skeleton_case_count": len(case_results),
        "raw_output_count": len(raw_outputs),
        "track_count": len(tracks),
        "persistence_count": len(persistences),
        "motion_count": len(motions),
        "smoke_io_artifacts_read": artifacts_read,
        "final_decision": final_decision,
        **meta,
    }
    report_md = "\n".join([
        "# Tracking / Optical Flow Adapter Skeleton v1",
        f"Cases: `{len(case_results)}` | Tracks: `{len(tracks)}` | Based on smoke IO inspection",
        "No real tracker/flow. No world model assembly. Candidate-only.",
        f"Final decision: `{final_decision}`",
        f"Next: `{next_phase}`",
    ])

    owner_review = {
        "review_id": "owner_constraint_compliance_review_v1",
        "owner_constraints_inherited": prior_smoke_io_go,
        "adapter_based_on_smoke_io_inspection": True,
        "no_field_simulation": True,
        "no_world_model_assembly": True,
        "no_task_reasoning": True,
        "no_new_protocol_without_reason": True,
        **meta,
    }

    go_values = {
        "prior_tracking_opticalflow_smoke_io_inspection_go": prior_smoke_io_go,
        "smoke_io_inspection_artifacts_read": artifacts_read,
        "adapter_based_on_real_inspection_results": artifacts_read and prior_smoke_io_go,
        "tracking_opticalflow_adapter_skeleton_complete": skeleton_complete,
        "adapter_input_builder_complete": len(inputs) >= 12,
        "raw_output_loader_complete": len(raw_outputs) >= 10,
        "output_normalizer_complete": len(tracks) >= 1,
        "object_persistence_builder_complete": len(persistences) >= 1,
        "motion_candidate_builder_complete": len(motions) >= 1,
        "adapter_result_assembler_complete": len(results) >= 12,
        "all_skeleton_cases_passed": all_cases_passed,
        "protocol_reuse_decision_ok": PROTOCOL_REUSE_DECISION.get("new_protocol_added") is False,
        "readiness_for_task_collaboration_ok": task_ready,
        "readiness_for_later_world_model_candidate_assembly_ok": later_wm_ready,
        "existing_io_reuse_ok": PROTOCOL_REUSE_DECISION.get("reuse_real_frame_input_package") is True,
        "no_new_protocol_without_reason": True,
        "cached_output_not_marked_as_real_run": smoke_s.get("cached_output_not_marked_as_real_run") is True,
        "adapter_stub_not_marked_as_real_run": smoke_s.get("adapter_stub_not_marked_as_real_run") is True,
        "blocked_cases_do_not_fabricate_outputs": blocked_ok,
        "short_track_not_persistent": short_track_ok,
        "identity_switch_degrades_persistence": identity_ok,
        "lost_track_degraded": lost_ok,
        "no_real_tracking_execution": True,
        "no_real_opticalflow_execution": True,
        "no_model_download": True,
        "no_field_simulation": True,
        "no_task_reasoning": True,
        "no_action_output": no_action,
        "no_world_entity_candidate_generated": no_wm_entity,
        "no_world_model_candidate_generated": no_wm_candidate,
        "no_world_model_entry_created": no_wm_entry,
        "no_fact_admission": True,
        "owner_constraints_inherited": prior_smoke_io_go,
        "candidate_only_outputs": True,
        "common_validation_reuse_ok": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": skeleton_pass,
        "skeleton_case_count": len(case_results),
        "tracking_opticalflow_adapter_skeleton_pass": skeleton_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        **absence,
    }

    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS if k in go_values},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(smoke_s.get("chain_trace_nodes") or []) + ["tracking_opticalflow_adapter_skeleton"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }

    return {
        "tracking_opticalflow_adapter_skeleton_report": report,
        "tracking_opticalflow_adapter_skeleton_report_md": report_md,
        "tracking_opticalflow_adapter_input_registry": {
            "registry_id": "tracking_opticalflow_adapter_input_registry_v1",
            "inputs": inputs, "count": len(inputs), **meta,
        },
        "tracking_opticalflow_raw_output_candidate_registry": {
            "registry_id": "tracking_opticalflow_raw_output_candidate_registry_v1",
            "candidates": raw_outputs, "count": len(raw_outputs), **meta,
        },
        "object_track_candidate_registry": {
            "registry_id": "object_track_candidate_registry_v1",
            "candidates": tracks, "count": len(tracks), **meta,
        },
        "object_persistence_candidate_registry": {
            "registry_id": "object_persistence_candidate_registry_v1",
            "candidates": persistences, "count": len(persistences), **meta,
        },
        "motion_candidate_registry": {
            "registry_id": "motion_candidate_registry_v1",
            "candidates": motions, "count": len(motions), **meta,
        },
        "tracking_quality_candidate_registry": {
            "registry_id": "tracking_quality_candidate_registry_v1",
            "candidates": qualities, "count": len(qualities), **meta,
        },
        "tracking_opticalflow_adapter_result_candidate_registry": {
            "registry_id": "tracking_opticalflow_adapter_result_candidate_registry_v1",
            "results": results, "count": len(results), **meta,
        },
        "tracking_opticalflow_task_collaboration_readiness_review": {
            "review_id": "tracking_opticalflow_task_collaboration_readiness_review_v1",
            "mappings": list(TASK_COLLABORATION_MAPPING),
            "no_task_action_output": True,
            "no_task_reasoning": True,
            **meta,
        },
        "tracking_opticalflow_later_world_model_readiness_review": {
            "review_id": "tracking_opticalflow_later_world_model_readiness_review_v1",
            "mappings": list(LATER_WORLD_MODEL_READINESS),
            "readiness_only_no_assembly": True,
            "no_world_model_candidate_generated": True,
            **meta,
        },
        "protocol_reuse_decision": {**PROTOCOL_REUSE_DECISION, **meta},
        "new_protocol_reason_required_report": {**NEW_PROTOCOL_REASON_REPORT, **meta},
        "no_action_boundary_review": {
            "review_id": "no_action_boundary_review_v1",
            "no_task_action_output": no_action,
            "no_navigation_suggestion": True,
            "no_task_reasoning": True,
            **meta,
        },
        "no_world_model_assembly_boundary_review": {
            "review_id": "no_world_model_assembly_boundary_review_v1",
            "no_world_model_assembly": True,
            "no_world_model_candidate_generated": no_wm_candidate,
            "no_world_model_entry_created": no_wm_entry,
            "no_world_entity_candidate_generated": no_wm_entity,
            **meta,
        },
        "owner_constraint_compliance_review": owner_review,
        "skeleton_case_results": {
            "results_id": "skeleton_case_results_v1",
            "all_skeleton_cases_passed": all_cases_passed,
            "results": [{"case_id": r["case_id"], "case_passed": r.get("case_passed"), "source_smoke_case_id": r.get("source_smoke_case_id")} for r in case_results],
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
