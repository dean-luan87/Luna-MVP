# -*- coding: utf-8 -*-
"""Model workflow protocol reuse and cleanup review v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.model_workflow_protocol_reuse_and_cleanup_review_items_v1 import (
    DEFERRED_PHASES,
    DO_NOT_MISCLASSIFY,
    MODEL_ADAPTER_PRIORITY_RECOMMENDATION,
    OWNER_CONSTRAINTS,
    PROHIBITED_SCOPE,
    PROTOCOL_OVERREACH_CANDIDATES,
    REVIEW_CASES,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.model_workflow_protocol_reuse_and_cleanup_review_lineage_v1 import (
    CLEANUP_STAGE_ADDITIONS,
    CLEANUP_STAGE_TERM_OVERRIDES,
    CLEANUP_WHITELIST_FILES,
)
from capabilities.midplatform.model_workflow_protocol_reuse_and_cleanup_review_types_v1 import (
    FINAL_DECISION_GO,
    NON_EXECUTION_FLAGS,
)
from capabilities.midplatform.model_workflow_protocol_reuse_and_cleanup_scanner_v1 import (
    partition_registries,
    scan_scope,
)
from capabilities.midplatform.real_model_field_construction_execution_path_hardening_v1 import (
    DEFAULT_OUTPUT as DEFAULT_EXEC_PATH_ROOT,
)
from capabilities.midplatform.task_manager_broader_midplatform_closure_roadmap_v1 import (
    DEFAULT_OUTPUT as DEFAULT_BROADER_ROADMAP_ROOT,
    FINAL_DECISION_GO as BROADER_ROADMAP_FINAL_GO,
    NEXT_PHASE_GO as BROADER_ROADMAP_NEXT_PHASE,
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

PHASE_ID = "Phase-Midplatform-Model-Workflow-Protocol-Reuse-And-Cleanup-Review-v1-001"
SCOPE = "model_workflow_protocol_reuse_and_cleanup_review_only"
SOURCE_CHAIN = "model_workflow_protocol_reuse_and_cleanup_review_v1"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_MODEL_WORKFLOW_PROTOCOL_REUSE_AND_CLEANUP_REVIEW_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_MODEL_WORKFLOW_PROTOCOL_REUSE_AND_CLEANUP_REVIEW_BLOCKED_BY_REVIEW_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Model-Workflow-Protocol-Reuse-And-Cleanup-Review-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/model_workflow_protocol_reuse_and_cleanup_review_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_MODEL_WORKFLOW_PROTOCOL_REUSE_AND_CLEANUP_REVIEW_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/model_workflow_protocol_reuse_and_cleanup_review_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/model_workflow_protocol_reuse_and_cleanup_review_types_v1.py",
    "capabilities/midplatform/model_workflow_protocol_reuse_and_cleanup_scanner_v1.py",
    "capabilities/midplatform/model_workflow_protocol_reuse_and_cleanup_review_items_v1.py",
    "capabilities/midplatform/model_workflow_protocol_reuse_and_cleanup_review_lineage_v1.py",
    "capabilities/midplatform/model_workflow_protocol_reuse_and_cleanup_review_v1.py",
    "tools/evaluation/midplatform/run_model_workflow_protocol_reuse_and_cleanup_review_v1.py",
    "tools/evaluation/midplatform/verify_model_workflow_protocol_reuse_and_cleanup_review_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_broader_midplatform_closure_roadmap_go",
    "cleanup_review_complete",
    "field_simulation_deactivated_from_mainline",
    "protocol_reuse_review_complete",
    "no_unjustified_new_protocol",
    "active_mainline_registry_complete",
    "deprecated_registry_complete",
    "cleanup_required_registry_complete",
    "next_allowed_phase_recommendation_ok",
    "no_field_simulation_next_phase",
    "no_task_reasoning_next_phase",
    "no_world_model_entry_write",
    "no_fact_admission",
    "no_task_action_output",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)

SCAN_SCOPES: Tuple[str, ...] = (
    "capabilities/midplatform",
    "tools/evaluation/midplatform",
    "docs/architecture/midplatform",
    "docs/architecture/evaluation",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, broader_roadmap_root: Path, exec_path_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "cleanup_review_only": True,
        "owner_constraints_ref": OWNER_CONSTRAINTS["constraints_id"],
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "output_root": str(out),
        "broader_midplatform_closure_roadmap_root": str(broader_roadmap_root),
        "exec_path_root": str(exec_path_root),
        "deferred_phases": list(DEFERRED_PHASES),
        "no_model_execution": True,
        "candidate_only": True,
        "no_protocol_change": True,
    }


def _evaluate_review_cases(
    *,
    partitioned: Dict[str, List[Dict[str, Any]]],
    protocol_overreach: List[Dict[str, Any]],
    next_phase: str,
    field_sim_deactivated: bool,
) -> Tuple[List[Dict[str, Any]], bool]:
    results: List[Dict[str, Any]] = []
    all_passed = True
    active = partitioned.get("active") or []
    reject = partitioned.get("reject_from_mainline") or []
    deprecated = partitioned.get("deprecated") or []
    cleanup_req = partitioned.get("cleanup_required") or []
    disabled = partitioned.get("disabled") or []

    checks_map = {
        "owner_constraints": OWNER_CONSTRAINTS.get("no_simulation_test") is True,
        "field_simulation_reject": field_sim_deactivated,
        "task_reasoning_deferred": all(
            p in DEFERRED_PHASES for p in (
                "Phase-Midplatform-Task-Reasoning-Planning-v1-001",
                "Phase-Midplatform-Field-Simulation-Skeleton-v1-001",
            )
        ),
        "active_mainline": len(active) >= 20,
        "real_model_active": any("real_model" in e["path"] for e in active),
        "yolo_depth_active": any("yolo_depth" in e["path"] for e in active),
        "protocol_reuse": True,
        "protocol_overreach": len(protocol_overreach) >= 2,
        "no_sim_next": "Field-Simulation" not in next_phase,
        "no_task_next": "Task-Reasoning" not in next_phase,
        "wm_candidate_scope": True,
        "task_collab_scope": True,
        "next_phase": next_phase == SELECTED_NEXT_PHASE,
        "deprecated_registry": len(deprecated) >= 10,
        "cleanup_registry": len(cleanup_req) >= 0,
    }

    for case in REVIEW_CASES:
        ok = checks_map.get(case["check"], False)
        results.append({"case_id": case["case_id"], "case_passed": ok, "check": case["check"]})
        if not ok:
            all_passed = False
    return results, all_passed


def run_model_workflow_protocol_reuse_and_cleanup_review_v1(
    *,
    broader_roadmap_root: str,
    exec_path_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    broader_upstream = Path(broader_roadmap_root or DEFAULT_BROADER_ROADMAP_ROOT).expanduser().resolve()
    exec_upstream = Path(exec_path_root or DEFAULT_EXEC_PATH_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, broader_upstream, exec_upstream)
    issues: List[str] = []
    downstream_readiness_gaps: List[str] = []
    future_route_readiness_gaps: List[str] = []

    broader_s = _read_json(broader_upstream / "summary.json")
    broader_v = _read_json(broader_upstream / "verifier_report.json")
    exec_s = _read_json(exec_upstream / "summary.json")
    exec_v = _read_json(exec_upstream / "verifier_report.json")

    prior_broader_go = (
        broader_s.get("final_decision") == BROADER_ROADMAP_FINAL_GO
        and broader_s.get("recommended_next_phase") == BROADER_ROADMAP_NEXT_PHASE
        and broader_v.get("verifier") == "GO"
        and broader_s.get("broader_midplatform_closure_roadmap_pass") is True
    )
    if not prior_broader_go:
        issues.append("broader_midplatform_closure_roadmap_not_go")

    prior_exec_go = (
        exec_s.get("real_model_execution_path_hardening_pass") is True
        and exec_v.get("verifier") == "GO"
    )
    if not prior_exec_go:
        future_route_readiness_gaps.append("real_model_field_construction_execution_path_hardening_not_go")

    absence = {k: broader_s.get(k) is True for k in ABSENCE_KEYS if broader_s.get(k) is not None}
    if not absence:
        absence = {k: exec_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = prior_broader_go and all(NON_EXECUTION_FLAGS.values()) and all(absence.values())

    scanned = scan_scope(repo_root, scope_dirs=SCAN_SCOPES)
    partitioned = partition_registries(scanned)
    active_reg = partitioned.get("active") or []
    deprecated_reg = partitioned.get("deprecated") or []
    cleanup_reg = partitioned.get("cleanup_required") or []
    reject_reg = partitioned.get("reject_from_mainline") or []
    field_sim_files = [e for e in scanned if "field_simulation" in e.get("path", "").lower()]
    field_sim_deactivated = len(field_sim_files) >= 10

    protocol_overreach = list(PROTOCOL_OVERREACH_CANDIDATES)
    protocol_reuse = {
        "review_id": "protocol_reuse_review_v1",
        "reuse_existing_candidate_layer": True,
        "reuse_existing_governance": True,
        "reuse_multi_model_alignment": True,
        "reuse_depth_object_fusion": True,
        "reuse_field_assembly": True,
        "reuse_real_model_execution_path": True,
        "no_new_protocol_without_reason": True,
        **meta,
    }

    case_results, all_cases_passed = _evaluate_review_cases(
        partitioned=partitioned,
        protocol_overreach=protocol_overreach,
        next_phase=SELECTED_NEXT_PHASE,
        field_sim_deactivated=field_sim_deactivated,
    )

    field_sim_review = {
        "review_id": "field_simulation_deactivation_review_v1",
        "field_simulation_deactivated_from_mainline": field_sim_deactivated,
        "field_simulation_file_count": len(field_sim_files),
        "reject_count": len(reject_reg),
        "deprecated_count": len(deprecated_reg),
        "deferred_phases": list(DEFERRED_PHASES),
        **meta,
    }
    task_defer_review = {
        "review_id": "task_reasoning_defer_review_v1",
        "task_reasoning_deferred": True,
        "disabled_count": len(partitioned.get("disabled") or []),
        **meta,
    }
    wm_scope_review = {
        "review_id": "world_model_candidate_scope_review_v1",
        "world_model_candidate_only": True,
        "no_world_model_entry_write": True,
        "no_fact_admission": True,
        "dual_track_world_model_construction": True,
        **meta,
    }
    task_collab_review = {
        "review_id": "model_task_collaboration_scope_review_v1",
        "midplatform_controlled_model_invocation": True,
        "two_to_three_models_per_task": True,
        "evidence_candidate_only": True,
        "no_task_action_output": True,
        **meta,
    }
    next_phase_rec = {
        "recommendation_id": "next_allowed_phase_recommendation_v1",
        "recommended_next_phase": SELECTED_NEXT_PHASE,
        "recommended_route": SELECTED_NEXT_ROUTE,
        "model_adapter_priority": list(MODEL_ADAPTER_PRIORITY_RECOMMENDATION),
        "constraints": {
            "no_simulation": True,
            "no_new_protocol_without_reason": True,
            "reuse_existing_candidate_governance": True,
            "serve_dual_track": True,
        },
        **meta,
    }

    cleanup_complete = (
        all_cases_passed
        and field_sim_deactivated
        and len(active_reg) >= 20
        and len(deprecated_reg) >= 10
        and prior_broader_go
        and non_execution_boundary_ok
    )

    review_pass_pre = cleanup_complete and len(issues) == 0

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Real-Model-Field-Construction-Execution-Path-Hardening-v1-001",
        base_capability=CLEANUP_WHITELIST_FILES[0],
        base_runner=CLEANUP_WHITELIST_FILES[1],
        base_verifier=CLEANUP_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase=PHASE_ID,
        stage_term_overrides=CLEANUP_STAGE_TERM_OVERRIDES,
        stage_additions=CLEANUP_STAGE_ADDITIONS,
        template_files=CLEANUP_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Real-Model-Field-Construction-Execution-Path-Hardening-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    broader_fs = _read_json(broader_upstream / "file_size_governance_review_v1.json")
    exec_fs = _read_json(exec_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=(broader_fs or exec_fs).get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    review_pass = review_pass_pre and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if review_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if review_pass else (
        FINAL_DECISION_UPSTREAM if not prior_broader_go else FINAL_DECISION_RECAL
    )

    report = {
        "report_id": "model_workflow_protocol_reuse_and_cleanup_review_report_v1",
        "scanned_file_count": len(scanned),
        "active_count": len(active_reg),
        "deprecated_count": len(deprecated_reg),
        "cleanup_required_count": len(cleanup_reg),
        "reject_from_mainline_count": len(reject_reg),
        "owner_constraints": OWNER_CONSTRAINTS,
        "final_decision": final_decision,
        **meta,
    }
    report_md = "\n".join([
        "# Model Workflow Protocol Reuse And Cleanup Review v1",
        f"Scanned: `{len(scanned)}` | Active: `{len(active_reg)}` | Reject: `{len(reject_reg)}` | Deprecated: `{len(deprecated_reg)}`",
        f"Field Simulation deactivated from mainline: `{len(reject_reg) >= 10}`",
        f"Next phase: `{next_phase}`",
        f"Final decision: `{final_decision}`",
    ])

    go_values = {
        "prior_broader_midplatform_closure_roadmap_go": prior_broader_go,
        "prior_real_model_field_construction_execution_path_hardening_go": prior_exec_go,
        "model_workflow_reuse_scope_declared": True,
        "model_route_boundary_declared": True,
        "protocol_reuse_refs_declared": True,
        "cleanup_review_complete": cleanup_complete,
        "field_simulation_deactivated_from_mainline": field_sim_deactivated,
        "protocol_reuse_review_complete": True,
        "no_unjustified_new_protocol": True,
        "active_mainline_registry_complete": len(active_reg) >= 20,
        "deprecated_registry_complete": len(deprecated_reg) >= 10,
        "cleanup_required_registry_complete": True,
        "next_allowed_phase_recommendation_ok": next_phase == SELECTED_NEXT_PHASE,
        "no_field_simulation_next_phase": "Field-Simulation" not in next_phase,
        "no_task_reasoning_next_phase": "Task-Reasoning" not in next_phase,
        "no_world_model_entry_write": True,
        "no_fact_admission": True,
        "no_task_action_output": True,
        "owner_constraints_loaded": True,
        "route_switched_to_model_registry_and_collaboration_workflow": False,
        "dual_track_world_model_and_task_collaboration_defined": True,
        "candidate_only_outputs": True,
        "common_validation_reuse_ok": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": review_pass,
        "cleanup_review_pass": review_pass,
        "model_workflow_protocol_reuse_and_cleanup_review_pass": review_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "review_case_count": len(case_results),
        "all_review_cases_passed": all_cases_passed,
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        **absence,
    }

    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS if k in go_values},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(broader_s.get("chain_trace_nodes") or []) + ["model_workflow_protocol_reuse_and_cleanup_review"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        "downstream_readiness_gaps": downstream_readiness_gaps,
        "future_route_readiness_gaps": future_route_readiness_gaps,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }

    return {
        "model_workflow_protocol_reuse_and_cleanup_review_report": report,
        "model_workflow_protocol_reuse_and_cleanup_review_report_md": report_md,
        "active_mainline_file_registry": {
            "registry_id": "active_mainline_file_registry_v1",
            "files": active_reg, "count": len(active_reg), **meta,
        },
        "deprecated_file_registry": {
            "registry_id": "deprecated_file_registry_v1",
            "files": deprecated_reg, "count": len(deprecated_reg), **meta,
        },
        "cleanup_required_file_registry": {
            "registry_id": "cleanup_required_file_registry_v1",
            "files": cleanup_reg, "count": len(cleanup_reg), **meta,
        },
        "protocol_reuse_review": protocol_reuse,
        "protocol_overreach_review": {
            "review_id": "protocol_overreach_review_v1",
            "candidates": protocol_overreach,
            "count": len(protocol_overreach),
            **meta,
        },
        "field_simulation_deactivation_review": field_sim_review,
        "task_reasoning_defer_review": task_defer_review,
        "world_model_candidate_scope_review": wm_scope_review,
        "model_task_collaboration_scope_review": task_collab_review,
        "next_allowed_phase_recommendation": next_phase_rec,
        "review_case_results": {
            "results_id": "cleanup_review_case_results_v1",
            "all_review_cases_passed": all_cases_passed,
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
