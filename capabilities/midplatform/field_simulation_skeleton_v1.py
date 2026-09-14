# -*- coding: utf-8 -*-
"""Field Simulation Skeleton v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.field_simulation_core_v1 import run_all_simulation_skeleton_cases
from capabilities.midplatform.field_simulation_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
)
from capabilities.midplatform.field_simulation_skeleton_items_v1 import (
    DO_NOT_MISCLASSIFY,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    SKELETON_CASES,
)
from capabilities.midplatform.field_simulation_skeleton_lineage_v1 import (
    SKELETON_STAGE_ADDITIONS,
    SKELETON_STAGE_TERM_OVERRIDES,
    SKELETON_WHITELIST_FILES,
)
from capabilities.midplatform.field_simulation_static_validators_v1 import (
    validate_no_action_no_fact_boundary,
    validate_non_execution_boundary,
)
from capabilities.midplatform.field_simulation_types_v1 import FINAL_DECISION_GO, NON_EXECUTION_FLAGS
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.real_model_field_construction_success_path_hardening_v1 import (
    DEFAULT_OUTPUT as DEFAULT_HARDENING_ROOT,
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
from capabilities.midplatform.yolo_depth_controlled_real_model_dryrun_v1 import (
    DEFAULT_OUTPUT as DEFAULT_DRYRUN_ROOT,
)

PHASE_ID = "Phase-Midplatform-Field-Simulation-Skeleton-v1-001"
SCOPE = "field_simulation_skeleton_only"
SOURCE_CHAIN = "field_simulation_skeleton_v1"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_FIELD_SIMULATION_SKELETON_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_FIELD_SIMULATION_SKELETON_BLOCKED_BY_IMPLEMENTATION_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Field-Simulation-Skeleton-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_simulation_skeleton_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_SIMULATION_SKELETON_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/field_simulation_skeleton_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_simulation_types_v1.py",
    "capabilities/midplatform/field_simulation_input_view_builder_v1.py",
    "capabilities/midplatform/simulation_eligibility_evaluator_v1.py",
    "capabilities/midplatform/field_simulation_plan_builder_v1.py",
    "capabilities/midplatform/field_simulation_candidate_generator_v1.py",
    "capabilities/midplatform/field_simulation_readiness_assembler_v1.py",
    "capabilities/midplatform/field_simulation_static_validators_v1.py",
    "capabilities/midplatform/field_simulation_core_v1.py",
    "capabilities/midplatform/field_simulation_skeleton_v1.py",
    "capabilities/midplatform/field_simulation_skeleton_items_v1.py",
    "capabilities/midplatform/field_simulation_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_simulation_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_field_simulation_skeleton_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_field_simulation_planning_go",
    "field_simulation_skeleton_complete",
    "simulation_input_view_builder_complete",
    "eligibility_evaluator_complete",
    "simulation_plan_builder_complete",
    "simulation_candidate_generator_complete",
    "readiness_assembler_complete",
    "all_skeleton_cases_passed",
    "current_state_simulation_generated",
    "short_horizon_projection_block_or_generate_supported",
    "occlusion_missing_info_simulation_generated",
    "task_relevance_projection_generated_without_action",
    "safety_risk_projection_generated_without_action",
    "field_quality_projection_generated",
    "failure_baselines_blocked_correctly",
    "traceability_preserved",
    "no_action_output",
    "no_fact_output",
    "no_action_no_fact_boundary_ok",
    "readiness_for_task_reasoning_planning_ok",
    "no_task_reasoning",
    "no_world_model_fact_creation",
    "common_validation_reuse_ok",
    "no_model_download",
    "no_weight_download",
    "no_runtime_execution",
    "candidate_only_outputs",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, planning_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "field_simulation_skeleton_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "planning_root": str(planning_root),
        "route": "field_simulation_planning_to_skeleton",
    }


def _index_upstream(
    dryrun_results: List[Dict[str, Any]],
    hardened_results: List[Dict[str, Any]],
    reusable_cases: List[Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    by_source: Dict[str, Dict[str, Any]] = {}
    hardened_by_scene = {h.get("enhanced_field_scene_ref", ""): h for h in hardened_results}
    reusable_by_source = {c["source_case_id"]: c for c in reusable_cases}
    for dr in dryrun_results:
        frame_ref = dr.get("frame_input_ref", "")
        if frame_ref.startswith("rfi_"):
            source_id = frame_ref[4:]
            scene_ref = (dr.get("enhanced_field_scene_candidate") or {}).get("field_scene_id")
            by_source[source_id] = {
                "dryrun": dr,
                "hardened": hardened_by_scene.get(scene_ref),
                "reusable": reusable_by_source.get(source_id),
            }
    return by_source


def run_field_simulation_skeleton_v1(
    *,
    planning_root: str,
    hardening_root: Optional[str] = None,
    dryrun_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    plan_upstream = Path(planning_root or DEFAULT_PLANNING_ROOT).expanduser().resolve()
    hard_upstream = Path(hardening_root or DEFAULT_HARDENING_ROOT).expanduser().resolve()
    dry_upstream = Path(dryrun_root or DEFAULT_DRYRUN_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, plan_upstream)
    issues: List[str] = []

    plan_s = _read_json(plan_upstream / "summary.json")
    plan_v = _read_json(plan_upstream / "verifier_report.json")
    prior_planning_go = (
        plan_s.get("final_decision") == PLANNING_FINAL_GO
        and plan_v.get("verifier") == "GO"
        and int(plan_v.get("passed_checks", 0)) >= 380
        and plan_s.get("field_simulation_planning_pass") is True
    )
    readiness_plan = _read_json(plan_upstream / "readiness_for_field_simulation_skeleton_review_v1.json")
    prior_planning_go = prior_planning_go and (
        readiness_plan.get("readiness_for_field_simulation_skeleton_ok") is True
    )
    if not prior_planning_go:
        issues.append("field_simulation_planning_not_go")

    dryrun_reg = _read_json(dry_upstream / "real_field_assembly_dryrun_result_candidate_registry_v1.json")
    hardened_reg = _read_json(hard_upstream / "hardened_field_construction_result_candidate_registry_v1.json")
    reusable_reg = _read_json(hard_upstream / "reusable_field_construction_case_registry_v1.json")
    indexed = _index_upstream(
        list(dryrun_reg.get("results") or []),
        list(hardened_reg.get("results") or []),
        list(reusable_reg.get("cases") or []),
    )

    absence = {k: plan_s.get(k) is True for k in ABSENCE_KEYS}
    non_exec_ok, _ = validate_non_execution_boundary(NON_EXECUTION_FLAGS)
    non_execution_boundary_ok = (
        prior_planning_go and plan_s.get("non_execution_boundary_ok") is True
        and non_exec_ok and all(absence.values())
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    case_results, all_passed = run_all_simulation_skeleton_cases(
        cases=SKELETON_CASES, indexed_upstream=indexed,
    )

    input_views = [r["input_view"] for r in case_results if r.get("input_view")]
    eligibilities = [r["eligibility"] for r in case_results if r.get("eligibility")]
    plans = [r["plan"] for r in case_results if r.get("plan")]
    all_candidates = [c for r in case_results for c in (r.get("simulation_candidates") or [])]
    readiness_list = [r["readiness"] for r in case_results if r.get("readiness")]

    no_action_ok, _ = validate_no_action_no_fact_boundary(all_candidates)
    traceability_ok = all(len((r.get("skeleton_result") or {}).get("traceability_refs") or []) >= 3 for r in case_results if r.get("skeleton_result"))
    readiness_trp_ok = any(r.get("readiness_for_task_reasoning_planning") for r in readiness_list)

    generated_modes = {c.get("mode") for c in all_candidates if c.get("simulation_status") in ("generated", "generated_degraded")}
    blocked_failure_ok = all(
        not any(c.get("simulation_status") in ("generated", "generated_degraded") for c in (r.get("simulation_candidates") or []))
        for r in case_results
        if r.get("case_id") in ("invalid_bbox_failure_simulation_blocked", "no_detection_blocked_no_entity")
    )

    field_simulation_skeleton_complete = (
        all_passed and len(SKELETON_CASES) >= 10 and no_action_ok
        and traceability_ok and len(issues) == 0
    )

    traceability_review = {
        "review_id": "field_simulation_traceability_review_v1",
        "traceability_preserved": traceability_ok,
        "cases_with_traceability": sum(
            1 for r in case_results if len((r.get("skeleton_result") or {}).get("traceability_refs") or []) >= 4
        ),
        **meta,
    }
    no_action_review = {
        "review_id": "no_action_no_fact_boundary_review_v1",
        "no_action_no_fact_boundary_ok": no_action_ok,
        "candidate_count": len(all_candidates),
        **meta,
    }
    readiness_trp_review = {
        "review_id": "readiness_for_task_reasoning_planning_review_v1",
        "readiness_for_task_reasoning_planning_ok": readiness_trp_ok and field_simulation_skeleton_complete,
        **meta,
    }
    non_exec_review = {
        "review_id": "non_execution_boundary_review_v1",
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "flags": dict(NON_EXECUTION_FLAGS),
        **meta,
    }
    case_registry = {
        "registry_id": "field_simulation_skeleton_case_results_v1",
        "count": len(case_results),
        "all_skeleton_cases_passed": all_passed,
        "results": [
            {
                "case_id": r["case_id"],
                "source_case_id": r.get("source_case_id"),
                "case_passed": r.get("case_passed"),
                "eligibility_status": (r.get("eligibility") or {}).get("eligibility_status"),
                "generated_modes": [
                    c.get("mode") for c in (r.get("simulation_candidates") or [])
                    if c.get("simulation_status") in ("generated", "generated_degraded")
                ],
            }
            for r in case_results
        ],
        **meta,
    }
    prohibited = {**PROHIBITED_SCOPE, **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    skeleton_pass = field_simulation_skeleton_complete and non_execution_boundary_ok

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Field-Simulation-Planning-v1-001",
        base_capability=SKELETON_WHITELIST_FILES[0],
        base_runner=SKELETON_WHITELIST_FILES[1],
        base_verifier=SKELETON_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase=PHASE_ID,
        stage_term_overrides=SKELETON_STAGE_TERM_OVERRIDES,
        stage_additions=SKELETON_STAGE_ADDITIONS,
        template_files=SKELETON_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Field-Simulation-Planning-v1-001",
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
    skeleton_pass = skeleton_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if skeleton_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if skeleton_pass else (
        FINAL_DECISION_UPSTREAM if not prior_planning_go else FINAL_DECISION_RECAL
    )

    go_values = {
        "prior_field_simulation_planning_go": prior_planning_go,
        "field_simulation_skeleton_complete": field_simulation_skeleton_complete,
        "simulation_input_view_builder_complete": len(input_views) >= 8,
        "eligibility_evaluator_complete": len(eligibilities) >= 8,
        "simulation_plan_builder_complete": len(plans) >= 8,
        "simulation_candidate_generator_complete": len(all_candidates) >= 10,
        "readiness_assembler_complete": len(readiness_list) >= 8,
        "all_skeleton_cases_passed": all_passed,
        "current_state_simulation_generated": "current_state_simulation" in generated_modes,
        "short_horizon_projection_block_or_generate_supported": (
            "short_horizon_motion_projection" in generated_modes
            or any(c.get("mode") == "short_horizon_motion_projection" and c.get("simulation_status") == "blocked_insufficient_input" for c in all_candidates)
        ),
        "occlusion_missing_info_simulation_generated": "occlusion_and_missing_info_simulation" in generated_modes,
        "task_relevance_projection_generated_without_action": "task_relevance_field_projection" in generated_modes,
        "safety_risk_projection_generated_without_action": "safety_risk_projection" in generated_modes,
        "field_quality_projection_generated": "field_quality_projection" in generated_modes,
        "failure_baselines_blocked_correctly": blocked_failure_ok,
        "traceability_preserved": traceability_ok,
        "no_action_output": no_action_ok,
        "no_fact_output": no_action_ok,
        "no_action_no_fact_boundary_ok": no_action_ok,
        "readiness_for_task_reasoning_planning_ok": readiness_trp_ok,
        "no_task_reasoning": True,
        "no_world_model_fact_creation": True,
        "common_validation_reuse_ok": True,
        "no_model_download": True,
        "no_weight_download": True,
        "no_runtime_execution": True,
        "no_persistent_memory_write": True,
        "no_integration_test": True,
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": skeleton_pass,
        "field_simulation_skeleton_pass": skeleton_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "skeleton_case_count": len(case_results),
        "simulation_candidate_count": len(all_candidates),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        "midplatform_still_has_remaining_work": True,
        **absence,
    }

    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS if k in go_values},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(plan_s.get("chain_trace_nodes") or []) + ["field_simulation_skeleton"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Field Simulation Skeleton v1",
        f"Skeleton cases: `{len(case_results)}` | Candidates: `{len(all_candidates)}` | All passed: `{all_passed}`",
        "Candidate-level simulation results — no task reasoning, no action, no world model fact",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "final_decision": final_decision, **meta}
    return {
        "field_simulation_skeleton_report": report,
        "field_simulation_skeleton_report_md": md,
        "field_simulation_input_view_registry": {
            "registry_id": "field_simulation_input_view_registry_v1",
            "views": input_views, "count": len(input_views), **meta,
        },
        "simulation_eligibility_candidate_registry": {
            "registry_id": "simulation_eligibility_candidate_registry_v1",
            "candidates": eligibilities, "count": len(eligibilities), **meta,
        },
        "field_simulation_plan_candidate_registry": {
            "registry_id": "field_simulation_plan_candidate_registry_v1",
            "plans": plans, "count": len(plans), **meta,
        },
        "field_simulation_candidate_registry": {
            "registry_id": "field_simulation_candidate_registry_v1",
            "candidates": all_candidates, "count": len(all_candidates), **meta,
        },
        "field_simulation_readiness_candidate_registry": {
            "registry_id": "field_simulation_readiness_candidate_registry_v1",
            "readiness_candidates": readiness_list, "count": len(readiness_list), **meta,
        },
        "field_simulation_skeleton_case_results": case_registry,
        "field_simulation_traceability_review": traceability_review,
        "no_action_no_fact_boundary_review": no_action_review,
        "readiness_for_task_reasoning_planning_review": readiness_trp_review,
        "non_execution_boundary_review": non_exec_review,
        "prohibited_scope": prohibited,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
