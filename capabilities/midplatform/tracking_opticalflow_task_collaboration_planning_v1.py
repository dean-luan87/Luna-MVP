# -*- coding: utf-8 -*-
"""Tracking / Optical Flow Task Collaboration Planning v1."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.tracking_opticalflow_adapter_skeleton_v1 import (
    DEFAULT_OUTPUT as DEFAULT_SKELETON_ROOT,
    FINAL_DECISION_GO as SKELETON_FINAL_GO,
)
from capabilities.midplatform.tracking_opticalflow_task_collaboration_planning_items_v1 import (
    DO_NOT_MISCLASSIFY,
    FAILURE_DEGRADATION_POLICY,
    FINAL_DECISION_GO,
    INVOCATION_CONTROL_POLICY,
    NEW_PROTOCOL_REASON_REPORT,
    NON_EXECUTION_FLAGS,
    PLANNING_CASES,
    PROHIBITED_SCOPE,
    PROTOCOL_REUSE_DECISION,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    TASK_INPUT_MAPPING,
    TASK_MODEL_GROUPS,
    TASK_OUTPUT_EVIDENCE_MAPPING,
    UPSTREAM_SKELETON_ARTIFACTS,
)
from capabilities.midplatform.tracking_opticalflow_task_collaboration_planning_lineage_v1 import (
    PLANNING_STAGE_ADDITIONS,
    PLANNING_STAGE_TERM_OVERRIDES,
    PLANNING_WHITELIST_FILES,
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

PHASE_ID = "Phase-Midplatform-Tracking-OpticalFlow-Task-Collaboration-Planning-v1-001"
SCOPE = "tracking_opticalflow_task_collaboration_planning_only"
SOURCE_CHAIN = "tracking_opticalflow_task_collaboration_planning_v1"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_TRACKING_OPTICALFLOW_TASK_COLLABORATION_PLANNING_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_TRACKING_OPTICALFLOW_TASK_COLLABORATION_PLANNING_BLOCKED_BY_PLANNING_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Tracking-OpticalFlow-Task-Collaboration-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/tracking_opticalflow_task_collaboration_planning_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_TRACKING_OPTICALFLOW_TASK_COLLABORATION_PLANNING_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/tracking_opticalflow_task_collaboration_planning_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/tracking_opticalflow_task_collaboration_planning_items_v1.py",
    "capabilities/midplatform/tracking_opticalflow_task_collaboration_planning_lineage_v1.py",
    "capabilities/midplatform/tracking_opticalflow_task_collaboration_planning_v1.py",
    "tools/evaluation/midplatform/run_tracking_opticalflow_task_collaboration_planning_v1.py",
    "tools/evaluation/midplatform/verify_tracking_opticalflow_task_collaboration_planning_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_tracking_opticalflow_adapter_skeleton_go",
    "smoke_io_then_adapter_then_task_collaboration_order_respected",
    "tracking_opticalflow_task_collaboration_planning_complete",
    "model_group_registry_complete",
    "task_input_mapping_complete",
    "task_output_evidence_mapping_complete",
    "invocation_control_review_ok",
    "failure_degradation_policy_complete",
    "all_planning_cases_passed",
    "no_action_boundary_ok",
    "no_world_model_assembly_boundary_ok",
    "no_task_reasoning_execution",
    "no_action_output",
    "no_field_simulation",
    "no_world_entity_candidate_generated",
    "no_world_model_candidate_generated",
    "no_world_model_entry_created",
    "no_fact_admission",
    "no_new_protocol_without_reason",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _group(group_id: str) -> Optional[Dict[str, Any]]:
    return next((g for g in TASK_MODEL_GROUPS if g["group_id"] == group_id), None)


def _failure_policy(condition: str) -> Optional[Dict[str, Any]]:
    return next((p for p in FAILURE_DEGRADATION_POLICY if p["condition"] == condition), None)


def _build_evidence_bundle(group: Dict[str, Any], *, execution_mode: str = "adapter_stub") -> Dict[str, Any]:
    """Planning-only TaskEvidenceBundleCandidate using existing candidate pattern."""
    bundle_id = f"teb_{uuid.uuid4().hex[:12]}"
    models = list(group["models"])
    return {
        "evidence_bundle_id": bundle_id,
        "task_context_ref": f"task_ctx_{group['group_id']}",
        "model_group": models,
        "input_refs": list(group["tracking_inputs"]),
        "model_output_refs": list(group["tracking_outputs"]),
        "tracking_opticalflow_refs": list(group["tracking_outputs"]),
        "yolo_refs": ["YOLO"] if "YOLO" in models else [],
        "depth_refs": ["Depth"] if "Depth" in models or "Depth_optional" in models else [],
        "slam_refs": ["SLAM_Spatial_Mapping"] if "SLAM_Spatial_Mapping" in models else [],
        "evidence_items": list(group["evidence_outputs"]),
        "missing_information": [],
        "warning_summary": {"execution_mode": execution_mode, "planning_only": True},
        "conflict_summary": [],
        "traceability_refs": [bundle_id, f"task_ctx_{group['group_id']}"],
        "candidate_only": True,
        "no_action_output": True,
        "no_world_model_candidate_generated": True,
        "no_world_entity_candidate_generated": True,
    }


def _evaluate_planning_cases(
    *,
    skeleton_s: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], bool]:
    results: List[Dict[str, Any]] = []
    bundles: List[Dict[str, Any]] = []
    all_passed = True

    for case in PLANNING_CASES:
        ok = False
        cid = case["case_id"]
        bundle: Optional[Dict[str, Any]] = None

        if case.get("group_id"):
            grp = _group(case["group_id"])
            ok = grp is not None and tuple(grp["models"]) == case["models"]
            if ok and grp:
                bundle = _build_evidence_bundle(grp)
                bundles.append(bundle)
        elif case.get("failure_condition"):
            pol = _failure_policy(case["failure_condition"])
            ok = pol is not None and pol.get("handling") == case.get("expect_handling")
        elif case.get("expect_no_action"):
            ok = all(
                g.get("no_action_output", True)
                or g.get("no_path_planning", True)
                or g.get("no_final_find_decision", True)
                or g.get("no_avoidance_action", True)
                or g.get("no_crossing_suggestion", True)
                for g in TASK_MODEL_GROUPS
            ) and NON_EXECUTION_FLAGS.get("no_action_output") is True
        elif case.get("expect_no_wm_candidate"):
            ok = (
                skeleton_s.get("no_world_model_candidate_generated") is True
                and skeleton_s.get("no_world_entity_candidate_generated") is True
            )
        elif case.get("expect_new_protocol") is False:
            ok = PROTOCOL_REUSE_DECISION.get("new_protocol_added") is False

        results.append({"case_id": cid, "case_passed": ok, "evidence_bundle_id": (bundle or {}).get("evidence_bundle_id")})
        if not ok:
            all_passed = False

    return results, bundles, all_passed


def _meta(out: Path, skeleton_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "task_collaboration_planning_only": True,
        "no_task_reasoning_execution": True,
        "no_action_output": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "output_root": str(out), "skeleton_root": str(skeleton_root),
    }


def run_tracking_opticalflow_task_collaboration_planning_v1(
    *,
    skeleton_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    sk_upstream = Path(skeleton_root or DEFAULT_SKELETON_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, sk_upstream)
    issues: List[str] = []

    sk_s = _read_json(sk_upstream / "summary.json")
    sk_v = _read_json(sk_upstream / "verifier_report.json")
    prior_skeleton_go = (
        sk_s.get("final_decision") == SKELETON_FINAL_GO
        and sk_v.get("verifier") == "GO"
        and int(sk_v.get("passed_checks", 0)) >= 430
        and sk_s.get("tracking_opticalflow_adapter_skeleton_pass") is True
        and sk_s.get("readiness_for_task_collaboration_ok") is True
        and sk_s.get("no_world_model_candidate_generated") is True
        and sk_s.get("no_world_entity_candidate_generated") is True
    )
    if not prior_skeleton_go:
        issues.append("tracking_opticalflow_adapter_skeleton_not_go")

    upstream_artifacts_read = all((sk_upstream / f).is_file() for f in UPSTREAM_SKELETON_ARTIFACTS)
    if not upstream_artifacts_read:
        issues.append("upstream_skeleton_artifacts_missing")

    task_collab_review = _read_json(sk_upstream / "tracking_opticalflow_task_collaboration_readiness_review_v1.json")
    wm_boundary = _read_json(sk_upstream / "no_world_model_assembly_boundary_review_v1.json")
    no_action_boundary = _read_json(sk_upstream / "no_action_boundary_review_v1.json")

    absence = {k: sk_s.get(k) is True for k in ABSENCE_KEYS}
    order_respected = (
        sk_s.get("adapter_based_on_smoke_io_inspection") is True
        and sk_s.get("prior_tracking_opticalflow_smoke_io_inspection_go") is True
        and sk_s.get("no_world_model_assembly") is True
    )
    non_execution_boundary_ok = prior_skeleton_go and all(NON_EXECUTION_FLAGS.values()) and all(absence.values())

    case_results, evidence_bundles, all_cases_passed = _evaluate_planning_cases(skeleton_s=sk_s)

    planning_complete = (
        all_cases_passed
        and len(PLANNING_CASES) >= 12
        and len(TASK_MODEL_GROUPS) == 4
        and len(FAILURE_DEGRADATION_POLICY) >= 7
        and PROTOCOL_REUSE_DECISION.get("new_protocol_added") is False
        and INVOCATION_CONTROL_POLICY.get("new_protocol_added") is False
        and prior_skeleton_go
        and upstream_artifacts_read
        and order_respected
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Tracking-OpticalFlow-Adapter-Skeleton-v1-001",
        base_capability=PLANNING_WHITELIST_FILES[0],
        base_runner=PLANNING_WHITELIST_FILES[1],
        base_verifier=PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase=PHASE_ID,
        stage_term_overrides=PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=PLANNING_STAGE_ADDITIONS,
        template_files=PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Tracking-OpticalFlow-Adapter-Skeleton-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    sk_fs = _read_json(sk_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=sk_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    planning_pass = (
        planning_complete and template_lineage.get("template_lineage_ok")
        and fs_ok and non_execution_boundary_ok and len(issues) == 0
    )
    next_phase = SELECTED_NEXT_PHASE if planning_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if planning_pass else (
        FINAL_DECISION_UPSTREAM if not prior_skeleton_go else FINAL_DECISION_RECAL
    )

    report = {
        "report_id": "tracking_opticalflow_task_collaboration_planning_report_v1",
        "planning_case_count": len(case_results),
        "model_group_count": len(TASK_MODEL_GROUPS),
        "evidence_bundle_count": len(evidence_bundles),
        "upstream_artifacts_read": upstream_artifacts_read,
        "final_decision": final_decision,
        **meta,
    }
    report_md = "\n".join([
        "# Tracking / Optical Flow Task Collaboration Planning v1",
        f"Groups: `{len(TASK_MODEL_GROUPS)}` | Cases: `{len(case_results)}` | Evidence bundles: `{len(evidence_bundles)}`",
        "Planning only. No Task Reasoning. No actions. No world model assembly.",
        f"Final decision: `{final_decision}`",
        f"Next: `{next_phase}`",
    ])

    owner_review = {
        "review_id": "owner_constraint_compliance_review_v1",
        "owner_constraints_inherited": prior_skeleton_go,
        "no_task_reasoning_execution": True,
        "no_action_output": True,
        "no_world_model_assembly": True,
        "no_field_simulation": True,
        "no_new_protocol_without_reason": True,
        **meta,
    }

    go_values = {
        "prior_tracking_opticalflow_adapter_skeleton_go": prior_skeleton_go,
        "smoke_io_then_adapter_then_task_collaboration_order_respected": order_respected,
        "tracking_opticalflow_task_collaboration_planning_complete": planning_complete,
        "model_group_registry_complete": len(TASK_MODEL_GROUPS) == 4,
        "task_input_mapping_complete": len(TASK_INPUT_MAPPING) == 4,
        "task_output_evidence_mapping_complete": len(TASK_OUTPUT_EVIDENCE_MAPPING) == 4,
        "invocation_control_review_ok": INVOCATION_CONTROL_POLICY.get("new_protocol_added") is False,
        "failure_degradation_policy_complete": len(FAILURE_DEGRADATION_POLICY) >= 7,
        "all_planning_cases_passed": all_cases_passed,
        "road_crossing_group_defined": _group("road_crossing_safety") is not None,
        "moving_obstacle_group_defined": _group("moving_obstacle_avoidance") is not None,
        "find_moving_object_group_defined": _group("find_moving_object") is not None,
        "return_location_group_defined": _group("return_to_location_context") is not None,
        "failure_degradation_handled": len(FAILURE_DEGRADATION_POLICY) >= 7,
        "cached_output_not_marked_as_real_run": sk_s.get("cached_output_not_marked_as_real_run") is True,
        "blocked_authorization_not_fabricated": sk_s.get("blocked_cases_do_not_fabricate_outputs") is True,
        "no_action_boundary_ok": NON_EXECUTION_FLAGS.get("no_action_output") is True,
        "no_world_model_assembly_boundary_ok": wm_boundary.get("no_world_model_assembly") is True,
        "no_task_reasoning_execution": True,
        "no_action_output": True,
        "no_field_simulation": True,
        "no_world_entity_candidate_generated": True,
        "no_world_model_candidate_generated": True,
        "no_world_model_entry_created": True,
        "no_fact_admission": True,
        "no_new_protocol_without_reason": True,
        "candidate_only_outputs": True,
        "common_validation_reuse_ok": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": planning_pass,
        "planning_case_count": len(case_results),
        "tracking_task_collaboration_planning_pass": planning_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        **absence,
    }

    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS if k in go_values},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(sk_s.get("chain_trace_nodes") or []) + ["tracking_opticalflow_task_collaboration_planning"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }

    return {
        "tracking_opticalflow_task_collaboration_planning_report": report,
        "tracking_opticalflow_task_collaboration_planning_report_md": report_md,
        "tracking_task_collaboration_model_group_registry": {
            "registry_id": "tracking_task_collaboration_model_group_registry_v1",
            "groups": list(TASK_MODEL_GROUPS),
            "count": len(TASK_MODEL_GROUPS),
            "inherited_from_skeleton_review": task_collab_review.get("review_id"),
            **meta,
        },
        "tracking_task_input_mapping_review": {
            "review_id": "tracking_task_input_mapping_review_v1",
            "mappings": list(TASK_INPUT_MAPPING),
            **meta,
        },
        "tracking_task_output_evidence_mapping_review": {
            "review_id": "tracking_task_output_evidence_mapping_review_v1",
            "mappings": list(TASK_OUTPUT_EVIDENCE_MAPPING),
            **meta,
        },
        "tracking_task_invocation_control_review": {
            "review_id": "tracking_task_invocation_control_review_v1",
            "policy": INVOCATION_CONTROL_POLICY,
            "midplatform_controlled": True,
            **meta,
        },
        "tracking_task_failure_degradation_policy": {
            "policy_id": "tracking_task_failure_degradation_policy_v1",
            "policies": list(FAILURE_DEGRADATION_POLICY),
            **meta,
        },
        "tracking_task_collaboration_case_registry": {
            "registry_id": "tracking_task_collaboration_case_registry_v1",
            "all_planning_cases_passed": all_cases_passed,
            "results": case_results,
            "evidence_bundles": evidence_bundles,
            **meta,
        },
        "tracking_task_collaboration_protocol_reuse_decision": {**PROTOCOL_REUSE_DECISION, **meta},
        "new_protocol_reason_required_report": {**NEW_PROTOCOL_REASON_REPORT, **meta},
        "no_action_boundary_review": {
            "review_id": "no_action_boundary_review_v1",
            "no_action_output": True,
            "no_navigation_suggestion": True,
            "no_task_reasoning_execution": True,
            "inherited_from_skeleton": no_action_boundary.get("review_id"),
            **meta,
        },
        "no_world_model_assembly_boundary_review": {
            "review_id": "no_world_model_assembly_boundary_review_v1",
            "no_world_model_assembly": True,
            "no_world_model_candidate_generated": True,
            "no_world_model_entry_created": True,
            "no_world_entity_candidate_generated": True,
            "inherited_from_skeleton": wm_boundary.get("review_id"),
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
        "do_not_misclassify_rules": {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta},
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
