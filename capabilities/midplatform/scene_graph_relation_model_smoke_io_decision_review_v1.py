# -*- coding: utf-8 -*-
"""Scene Graph / Relation Model Smoke IO Decision Review v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.scene_graph_relation_model_smoke_io_decision_review_items_v1 import (
    DECISION_CASES,
    DEPENDENCY_REVIEW,
    DO_NOT_MISCLASSIFY,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_DEFERRED,
    FINAL_DECISION_READY,
    INPUT_SOURCE_REVIEWS,
    NEW_PROTOCOL_REASON_REPORT,
    NON_EXECUTION_FLAGS,
    PREREQUISITE_CHAIN,
    PROHIBITED_SCOPE,
    PROTOCOL_REUSE_DECISION,
    SCENE_GRAPH_CANDIDATE_REGISTRY,
    SELECTED_NEXT_PHASE_BLOCKED,
    SELECTED_NEXT_PHASE_DEFERRED,
    SELECTED_NEXT_PHASE_READY,
    SELECTED_NEXT_ROUTE_BLOCKED,
    SELECTED_NEXT_ROUTE_DEFERRED,
    SELECTED_NEXT_ROUTE_READY,
    SMOKE_IO_ELIGIBILITY_GATES,
    UPSTREAM_TASK_PLANNING_ARTIFACTS,
    VALID_FINAL_DECISIONS,
)
from capabilities.midplatform.scene_graph_relation_model_smoke_io_decision_review_lineage_v1 import (
    PLANNING_STAGE_ADDITIONS,
    PLANNING_STAGE_TERM_OVERRIDES,
    PLANNING_WHITELIST_FILES,
)
from capabilities.midplatform.scene_graph_relation_model_smoke_io_decision_review_evaluator_v1 import (
    evaluate_decision_cases,
    evaluate_eligibility_gates,
    evaluate_input_sources,
    evaluate_prerequisite_chain,
    read_json as _read_json,
)
from capabilities.midplatform.segmentation_mask_task_collaboration_planning_items_v1 import (
    FINAL_DECISION_GO as UPSTREAM_FINAL_GO,
)
from capabilities.midplatform.segmentation_mask_task_collaboration_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_TASK_PLANNING_ROOT,
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

PHASE_ID = "Phase-Midplatform-Scene-Graph-Relation-Model-Smoke-IO-Decision-Review-v1-001"
SCOPE = "scene_graph_relation_model_smoke_io_decision_review_only"
SOURCE_CHAIN = "scene_graph_relation_model_smoke_io_decision_review_v1"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/scene_graph_relation_model_smoke_io_decision_review_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_SCENE_GRAPH_RELATION_MODEL_SMOKE_IO_DECISION_REVIEW_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/scene_graph_relation_model_smoke_io_decision_review_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/scene_graph_relation_model_smoke_io_decision_review_items_v1.py",
    "capabilities/midplatform/scene_graph_relation_model_smoke_io_decision_review_evaluator_v1.py",
    "capabilities/midplatform/scene_graph_relation_model_smoke_io_decision_review_lineage_v1.py",
    "capabilities/midplatform/scene_graph_relation_model_smoke_io_decision_review_v1.py",
    "tools/evaluation/midplatform/run_scene_graph_relation_model_smoke_io_decision_review_v1.py",
    "tools/evaluation/midplatform/verify_scene_graph_relation_model_smoke_io_decision_review_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_segmentation_mask_task_collaboration_planning_go",
    "scene_graph_relation_is_p4_deferred_review",
    "decision_review_only",
    "p0_p3_prerequisite_chain_review_complete",
    "input_source_review_complete",
    "dependency_review_complete",
    "deferred_status_review_complete",
    "smoke_io_eligibility_review_complete",
    "next_phase_decision_complete",
    "smoke_io_gate_decision_made",
    "all_decision_cases_passed",
    "no_scene_graph_runtime",
    "no_scene_graph_model_execution",
    "no_smoke_io_yet",
    "no_adapter_skeleton_yet",
    "no_task_collaboration_planning_yet",
    "no_relation_candidate_generated",
    "no_world_relation_candidate_generated",
    "no_world_model_assembly",
    "no_world_model_candidate_generated",
    "no_world_model_entry_created",
    "no_fact_admission",
    "no_task_reasoning_execution",
    "no_action_output",
    "no_field_simulation",
    "no_new_protocol_without_reason",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)


def _meta(out: Path, upstream_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "decision_review_only": True,
        "scene_graph_relation_is_p4_deferred_review": True,
        "no_scene_graph_runtime": True,
        "no_smoke_io_yet": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "output_root": str(out),
        "upstream_task_planning_root": str(upstream_root),
    }


def run_scene_graph_relation_model_smoke_io_decision_review_v1(
    *,
    task_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(task_planning_root or DEFAULT_TASK_PLANNING_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    up_s = _read_json(upstream / "summary.json")
    up_v = _read_json(upstream / "verifier_report.json")
    prior_upstream_go = (
        up_s.get("final_decision") == UPSTREAM_FINAL_GO
        and up_v.get("verifier") == "GO"
        and int(up_v.get("passed_checks", 0)) >= 360
        and up_s.get("segmentation_mask_task_collaboration_planning_pass") is True
        and up_s.get("no_world_model_assembly_boundary_ok") is True
    )
    if not prior_upstream_go:
        issues.append("segmentation_mask_task_collaboration_planning_not_go")

    upstream_artifacts_read = all((upstream / f).is_file() for f in UPSTREAM_TASK_PLANNING_ARTIFACTS)
    if not upstream_artifacts_read:
        issues.append("upstream_task_planning_artifacts_missing")

    prerequisite_rows, all_prereqs_go, prereq_go_count = evaluate_prerequisite_chain()
    input_source_rows, overall_sufficiency = evaluate_input_sources(prerequisite_rows)
    eligibility_gates, eligibility_ok = evaluate_eligibility_gates(
        input_source_rows, all_prereqs_go=all_prereqs_go,
    )

    owner_blocked = NEW_PROTOCOL_REASON_REPORT.get("owner_approval_required") is True
    if owner_blocked:
        selected_option = "blocked_pending_owner_decision"
        smoke_io_allowed = False
        scene_graph_still_deferred = True
    elif eligibility_ok and prior_upstream_go:
        selected_option = "ready_for_smoke_io"
        smoke_io_allowed = True
        scene_graph_still_deferred = False
    else:
        selected_option = "remain_deferred"
        smoke_io_allowed = False
        scene_graph_still_deferred = True

    gate_decision = {
        "decision_id": "scene_graph_relation_smoke_io_gate_decision_v1",
        "adapter_id": "scene_graph_relation",
        "priority": "P4",
        "prior_deferred_status": True,
        "selected_option": selected_option,
        "smoke_io_allowed": smoke_io_allowed,
        "scene_graph_still_deferred": scene_graph_still_deferred,
        "prerequisite_go_count": prereq_go_count,
        "prerequisite_total": len(PREREQUISITE_CHAIN),
        "all_p0_p3_task_collaboration_go": all_prereqs_go,
        "overall_input_sufficiency": overall_sufficiency,
        "eligibility_gates_passed": eligibility_ok,
        "decision_basis": (
            "all_p0_p3_task_collaboration_planning_and_input_eligibility_required"
            if not smoke_io_allowed
            else "p0_p3_prerequisite_chain_and_input_eligibility_complete"
        ),
        "smoke_io_checks_when_allowed": (
            "model_runnable_io_only_no_relation_assembly_no_world_model_assembly"
            if smoke_io_allowed
            else None
        ),
        "world_model_assembly_precondition_review_required": (
            selected_option == "remain_deferred"
        ),
        "no_scene_graph_runtime": True,
        "no_smoke_io_inspection_execution_in_this_phase": True,
        **meta,
    }

    absence = {k: up_s.get(k) is True for k in ABSENCE_KEYS}
    owner_compliance_ok = prior_upstream_go and all(NON_EXECUTION_FLAGS.values()) and all(absence.values())
    case_results, all_cases_passed = evaluate_decision_cases(
        input_source_rows=input_source_rows,
        overall_sufficiency=overall_sufficiency,
        gate_decision=gate_decision,
        owner_compliance_ok=owner_compliance_ok,
    )
    non_execution_boundary_ok = owner_compliance_ok

    review_complete = (
        all_cases_passed
        and len(DECISION_CASES) >= 10
        and len(input_source_rows) == len(INPUT_SOURCE_REVIEWS)
        and PROTOCOL_REUSE_DECISION.get("new_protocol_added") is False
        and prior_upstream_go
        and upstream_artifacts_read
        and gate_decision.get("decision_id") is not None
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Segmentation-Mask-Task-Collaboration-Planning-v1-001",
        base_capability=PLANNING_WHITELIST_FILES[0],
        base_runner=PLANNING_WHITELIST_FILES[1],
        base_verifier=PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase=PHASE_ID,
        stage_term_overrides=PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=PLANNING_STAGE_ADDITIONS,
        template_files=PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Segmentation-Mask-Task-Collaboration-Planning-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    up_fs = _read_json(upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first",
        full_repo_scan=False,
        previous_interruption_type=up_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True

    review_pass = (
        review_complete
        and template_lineage.get("template_lineage_ok")
        and fs_ok
        and non_execution_boundary_ok
        and len(issues) == 0
    )

    if not review_pass:
        final_decision = FINAL_DECISION_DEFERRED
        next_phase = SELECTED_NEXT_PHASE_DEFERRED
        selected_route = SELECTED_NEXT_ROUTE_DEFERRED
    elif selected_option == "blocked_pending_owner_decision":
        final_decision = FINAL_DECISION_BLOCKED
        next_phase = SELECTED_NEXT_PHASE_BLOCKED
        selected_route = SELECTED_NEXT_ROUTE_BLOCKED
    elif selected_option == "ready_for_smoke_io":
        final_decision = FINAL_DECISION_READY
        next_phase = SELECTED_NEXT_PHASE_READY
        selected_route = SELECTED_NEXT_ROUTE_READY
    else:
        final_decision = FINAL_DECISION_DEFERRED
        next_phase = SELECTED_NEXT_PHASE_DEFERRED
        selected_route = SELECTED_NEXT_ROUTE_DEFERRED

    report_md = "\n".join([
        "# Scene Graph / Relation Model Smoke IO Decision Review v1",
        "",
        f"Prerequisite GO: `{prereq_go_count}/{len(PREREQUISITE_CHAIN)}` | Cases: `{len(case_results)}`",
        "",
        "Decision review only. No Scene Graph runtime. No Smoke IO execution. No world model assembly.",
        "",
        f"Input sufficiency: `{overall_sufficiency}` | smoke_io_allowed: `{smoke_io_allowed}`",
        f"scene_graph_still_deferred: `{scene_graph_still_deferred}` | selected_option: `{selected_option}`",
        "",
        f"**Final decision:** `{final_decision}`",
        f"**Next:** `{next_phase}`",
    ])

    owner_review = {
        "review_id": "owner_constraint_compliance_review_v1",
        "owner_constraints_inherited": prior_upstream_go,
        "no_scene_graph_runtime": True,
        "no_smoke_io_inspection_execution": True,
        "no_world_model_assembly": True,
        "no_field_simulation": True,
        "no_task_reasoning_execution": True,
        "no_action_output": True,
        "no_fact_admission": True,
        "no_relation_candidate_generated": True,
        "no_new_protocol_without_reason": True,
        "owner_constraint_compliance_ok": owner_compliance_ok,
        **meta,
    }

    go_values = {
        "prior_segmentation_mask_task_collaboration_planning_go": prior_upstream_go,
        "scene_graph_relation_is_p4_deferred_review": True,
        "decision_review_only": True,
        "p0_p3_prerequisite_chain_review_complete": len(prerequisite_rows) == len(PREREQUISITE_CHAIN),
        "input_source_review_complete": len(input_source_rows) == len(INPUT_SOURCE_REVIEWS),
        "dependency_review_complete": DEPENDENCY_REVIEW.get("review_id") is not None,
        "deferred_status_review_complete": True,
        "smoke_io_eligibility_review_complete": len(eligibility_gates) == len(SMOKE_IO_ELIGIBILITY_GATES),
        "next_phase_decision_complete": bool(final_decision),
        "smoke_io_gate_decision_made": gate_decision.get("decision_id") is not None,
        "smoke_io_allowed": smoke_io_allowed,
        "scene_graph_still_deferred": scene_graph_still_deferred,
        "selected_option": selected_option,
        "overall_input_sufficiency": overall_sufficiency,
        "all_decision_cases_passed": all_cases_passed,
        "prerequisite_go_count": prereq_go_count,
        "prerequisite_total": len(PREREQUISITE_CHAIN),
        "all_p0_p3_task_collaboration_go": all_prereqs_go,
        "eligibility_gates_passed": eligibility_ok,
        "no_scene_graph_runtime": True,
        "no_scene_graph_model_execution": True,
        "no_smoke_io_yet": True,
        "no_adapter_skeleton_yet": True,
        "no_task_collaboration_planning_yet": True,
        "no_relation_candidate_generated": True,
        "no_world_relation_candidate_generated": True,
        "no_world_model_assembly": True,
        "no_world_model_candidate_generated": True,
        "no_world_entity_candidate_generated": True,
        "no_world_geometry_candidate_generated": True,
        "no_world_model_entry_created": True,
        "no_fact_admission": True,
        "no_task_reasoning_execution": True,
        "no_action_output": True,
        "no_field_simulation": True,
        "no_smoke_io_inspection_execution": True,
        "no_new_protocol_without_reason": True,
        "candidate_only_outputs": True,
        "common_validation_reuse_ok": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": review_pass,
        "decision_review_complete": review_pass,
        "decision_case_count": len(case_results),
        "scene_graph_relation_model_smoke_io_decision_review_pass": review_pass,
        "selected_next_route": selected_route,
        "valid_final_decisions": list(VALID_FINAL_DECISIONS),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        **absence,
    }

    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS if k in go_values},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(up_s.get("chain_trace_nodes") or []) + ["scene_graph_relation_smoke_io_decision_review"]),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "blocker_count": len(issues),
        "issues": issues,
        **go_values,
        **core_fields,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }

    return {
        "scene_graph_relation_model_smoke_io_decision_review_report": {
            "report_id": "scene_graph_relation_model_smoke_io_decision_review_report_v1",
            "decision_case_count": len(case_results),
            "input_source_count": len(input_source_rows),
            "upstream_artifacts_read": upstream_artifacts_read,
            "smoke_io_allowed": smoke_io_allowed,
            "scene_graph_still_deferred": scene_graph_still_deferred,
            "selected_option": selected_option,
            "overall_input_sufficiency": overall_sufficiency,
            "final_decision": final_decision,
            **meta,
        },
        "scene_graph_relation_model_smoke_io_decision_review_report_md": report_md,
        "scene_graph_relation_input_source_review": {
            "review_id": "scene_graph_relation_input_source_review_v1",
            "rows": input_source_rows,
            "overall_classification": overall_sufficiency,
            **meta,
        },
        "scene_graph_relation_candidate_dependency_review": {**DEPENDENCY_REVIEW, **meta},
        "scene_graph_relation_deferred_status_review": {
            "review_id": "scene_graph_relation_deferred_status_review_v1",
            "prior_deferred_status": True,
            "scene_graph_still_deferred": scene_graph_still_deferred,
            "deferred_reason": (
                "p0_p3_prerequisite_or_input_eligibility_incomplete"
                if scene_graph_still_deferred
                else "deferred_lifted_ready_for_smoke_io_inspection"
            ),
            "prerequisite_go_count": prereq_go_count,
            **meta,
        },
        "scene_graph_relation_smoke_io_eligibility_review": {
            "review_id": "scene_graph_relation_smoke_io_eligibility_review_v1",
            "gates": eligibility_gates,
            "eligibility_ok": eligibility_ok,
            "smoke_io_allowed": smoke_io_allowed,
            **meta,
        },
        "scene_graph_relation_next_phase_decision": {
            "decision_id": "scene_graph_relation_next_phase_decision_v1",
            "selected_option": selected_option,
            "final_decision": final_decision,
            "recommended_next_phase": next_phase,
            "selected_next_route": selected_route,
            **meta,
        },
        "scene_graph_relation_protocol_reuse_decision": {**PROTOCOL_REUSE_DECISION, **meta},
        "new_protocol_reason_required_report": {**NEW_PROTOCOL_REASON_REPORT, **meta},
        "no_relation_candidate_generation_review": {
            "review_id": "no_relation_candidate_generation_review_v1",
            "no_relation_candidate_generated": True,
            "no_world_relation_candidate_generated": True,
            "no_scene_relation_candidate_generated": True,
            "reference_only_scene_relation_schema": True,
            **meta,
        },
        "no_world_model_assembly_boundary_review": {
            "review_id": "no_world_model_assembly_boundary_review_v1",
            "no_world_model_assembly": True,
            "no_world_model_candidate_generated": True,
            "no_world_model_entry_created": True,
            "no_world_entity_candidate_generated": True,
            "no_world_geometry_candidate_generated": True,
            "inherited_from_upstream": up_s.get("no_world_model_assembly_boundary_ok"),
            **meta,
        },
        "owner_constraint_compliance_review": owner_review,
        "non_execution_boundary_review": {
            "review_id": "non_execution_boundary_review_v1",
            "non_execution_boundary_ok": non_execution_boundary_ok,
            "flags": dict(NON_EXECUTION_FLAGS),
            **meta,
        },
        "prohibited_scope": {**PROHIBITED_SCOPE, **meta},
        "do_not_misclassify_rules": {
            "rules_id": "do_not_misclassify_rules_v1",
            "rules": list(DO_NOT_MISCLASSIFY),
            **meta,
        },
        "decision_case_registry": {
            "registry_id": "scene_graph_relation_smoke_io_decision_case_registry_v1",
            "all_decision_cases_passed": all_cases_passed,
            "results": case_results,
            **meta,
        },
        "scene_graph_relation_candidate_registry_review": {
            "review_id": "scene_graph_relation_candidate_registry_review_v1",
            "candidates": list(SCENE_GRAPH_CANDIDATE_REGISTRY),
            "count": len(SCENE_GRAPH_CANDIDATE_REGISTRY),
            "reference_only_not_runtime": True,
            **meta,
        },
        "scene_graph_relation_prerequisite_chain_review": {
            "review_id": "scene_graph_relation_prerequisite_chain_review_v1",
            "rows": prerequisite_rows,
            "all_p0_p3_task_collaboration_go": all_prereqs_go,
            "prerequisite_go_count": prereq_go_count,
            **meta,
        },
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
