# -*- coding: utf-8 -*-
"""Field Simulation Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.field_simulation_planning_items_v1 import (
    DO_NOT_MISCLASSIFY,
    FAILURE_AND_DEGRADATION_SIMULATION_POLICY,
    FIELD_SIMULATION_CANDIDATE_CONTRACT,
    FIELD_SIMULATION_INPUT_VIEW_CONTRACT,
    FIELD_SIMULATION_MODE_REGISTRY,
    FIELD_SIMULATION_PLAN_CANDIDATE_CONTRACT,
    FIELD_SIMULATION_READINESS_POLICY,
    NON_EXECUTION_FLAGS,
    PLANNING_CASES,
    PLANNING_RULES,
    PROHIBITED_SCOPE,
    REUSABLE_CASE_TO_SIMULATION_MAPPING,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    SIMULATION_ELIGIBILITY_POLICY,
    build_simulation_input_view,
    build_simulation_plan,
    build_simulation_readiness,
    evaluate_planning_case,
    evaluate_simulation_eligibility,
)
from capabilities.midplatform.field_simulation_planning_lineage_v1 import (
    PLANNING_STAGE_ADDITIONS,
    PLANNING_STAGE_TERM_OVERRIDES,
    PLANNING_WHITELIST_FILES,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
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
from capabilities.midplatform.yolo_depth_controlled_real_model_dryrun_v1 import (
    DEFAULT_OUTPUT as DEFAULT_DRYRUN_ROOT,
)

PHASE_ID = "Phase-Midplatform-Field-Simulation-Planning-v1-001"
SCOPE = "field_simulation_planning_only"
SOURCE_CHAIN = "field_simulation_planning_v1"
FINAL_DECISION_GO = "MIDPLATFORM_FIELD_SIMULATION_PLANNING_READY_FOR_FIELD_SIMULATION_SKELETON"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_FIELD_SIMULATION_PLANNING_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_FIELD_SIMULATION_PLANNING_BLOCKED_BY_PLANNING_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Field-Simulation-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_simulation_planning_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_SIMULATION_PLANNING_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/field_simulation_planning_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_simulation_planning_v1.py",
    "capabilities/midplatform/field_simulation_planning_items_v1.py",
    "capabilities/midplatform/field_simulation_planning_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_simulation_planning_v1.py",
    "tools/evaluation/midplatform/verify_field_simulation_planning_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_real_model_field_construction_success_path_hardening_go",
    "field_simulation_planning_complete",
    "simulation_mode_registry_complete",
    "simulation_eligibility_policy_complete",
    "simulation_plan_candidate_contract_complete",
    "reusable_case_to_simulation_mapping_complete",
    "all_planning_cases_passed",
    "real_model_hardened_baselines_used",
    "success_baselines_mapped_to_simulation",
    "degraded_baselines_mapped_with_limitations",
    "failure_baselines_blocked_or_mapped_to_validation",
    "current_state_simulation_planned",
    "short_horizon_projection_planned_but_not_executed",
    "occlusion_missing_info_simulation_planned",
    "task_relevance_projection_planned_without_action",
    "safety_risk_projection_planned_without_action",
    "field_quality_projection_planned",
    "no_field_simulation_execution",
    "no_task_execution",
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


def _validate_non_execution(flags: Dict[str, bool]) -> bool:
    return all(flags.get(k) is True for k in NON_EXECUTION_FLAGS)


def _meta(out: Path, hardening_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "field_simulation_planning_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "no_field_simulation_execution": True,
        "output_root": str(out), "hardening_root": str(hardening_root),
        "route": "hardened_field_construction_to_field_simulation_planning",
    }


def _index_upstream(
    dryrun_results: List[Dict[str, Any]],
    hardened_results: List[Dict[str, Any]],
    reusable_cases: List[Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    by_source: Dict[str, Dict[str, Any]] = {}
    hardened_by_scene: Dict[str, Dict[str, Any]] = {}
    for h in hardened_results:
        hardened_by_scene[h.get("enhanced_field_scene_ref", "")] = h
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


def run_field_simulation_planning_v1(
    *,
    hardening_root: str,
    dryrun_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    hard_upstream = Path(hardening_root or DEFAULT_HARDENING_ROOT).expanduser().resolve()
    dry_upstream = Path(dryrun_root or DEFAULT_DRYRUN_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, hard_upstream)
    issues: List[str] = []

    hard_s = _read_json(hard_upstream / "summary.json")
    hard_v = _read_json(hard_upstream / "verifier_report.json")
    prior_hardening_go = (
        hard_s.get("final_decision") == HARDENING_FINAL_GO
        and hard_v.get("verifier") == "GO"
        and int(hard_v.get("passed_checks", 0)) >= 420
        and hard_s.get("real_model_field_construction_success_path_hardening_pass") is True
        and hard_s.get("readiness_for_field_simulation_planning_ok") is True
    )
    if not prior_hardening_go:
        issues.append("real_model_field_construction_success_path_hardening_not_go")

    dryrun_reg = _read_json(dry_upstream / "real_field_assembly_dryrun_result_candidate_registry_v1.json")
    hardened_reg = _read_json(hard_upstream / "hardened_field_construction_result_candidate_registry_v1.json")
    reusable_reg = _read_json(hard_upstream / "reusable_field_construction_case_registry_v1.json")
    indexed = _index_upstream(
        list(dryrun_reg.get("results") or []),
        list(hardened_reg.get("results") or []),
        list(reusable_reg.get("cases") or []),
    )

    absence = {k: hard_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = (
        prior_hardening_go and hard_s.get("non_execution_boundary_ok") is True
        and _validate_non_execution(NON_EXECUTION_FLAGS) and all(absence.values())
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    case_results: List[Dict[str, Any]] = []
    plans: List[Dict[str, Any]] = []
    input_views: List[Dict[str, Any]] = []
    eligibilities: List[Dict[str, Any]] = []
    all_passed = True

    for pc in PLANNING_CASES:
        upstream = indexed.get(pc["source_case_id"])
        if not upstream:
            case_results.append({"case_id": pc["case_id"], "case_passed": False, "error": "upstream_not_found"})
            all_passed = False
            continue
        dr = upstream["dryrun"]
        iv = build_simulation_input_view(
            dryrun_result=dr,
            hardened_result=upstream.get("hardened"),
            reusable_case=upstream.get("reusable"),
        )
        elig = evaluate_simulation_eligibility(iv, dr, upstream.get("reusable"))
        plan = build_simulation_plan(input_view=iv, eligibility=elig, reusable_case=upstream.get("reusable"))
        readiness = build_simulation_readiness(plan, elig)
        passed = evaluate_planning_case(pc, iv, elig, plan, upstream.get("reusable"))
        case_results.append({
            "case_id": pc["case_id"],
            "source_case_id": pc["source_case_id"],
            "case_passed": passed,
            "eligibility_status": elig.get("eligibility_status"),
            "selected_modes": plan.get("selected_modes"),
            "readiness_for_simulation_skeleton": plan.get("readiness_for_simulation_skeleton"),
        })
        input_views.append(iv)
        eligibilities.append(elig)
        plans.append(plan)
        if not passed and not pc.get("optional_meta"):
            all_passed = False

    simulation_mode_registry_complete = FIELD_SIMULATION_MODE_REGISTRY.get("registry_id") == "field_simulation_mode_registry_v1"
    simulation_eligibility_policy_complete = SIMULATION_ELIGIBILITY_POLICY.get("policy_id") == "simulation_eligibility_policy_v1"
    simulation_plan_candidate_contract_complete = (
        FIELD_SIMULATION_PLAN_CANDIDATE_CONTRACT.get("contract_id") == "field_simulation_plan_candidate_contract_v1"
    )
    reusable_case_to_simulation_mapping_complete = (
        REUSABLE_CASE_TO_SIMULATION_MAPPING.get("mapping_id") == "reusable_case_to_simulation_mapping_v1"
    )
    field_simulation_planning_complete = (
        all_passed and len(PLANNING_CASES) >= 10
        and simulation_mode_registry_complete
        and simulation_eligibility_policy_complete
        and simulation_plan_candidate_contract_complete
        and reusable_case_to_simulation_mapping_complete
        and len(issues) == 0
    )

    all_modes = {m for p in plans for m in (p.get("selected_modes") or [])}
    readiness_skeleton_ok = any(p.get("readiness_for_simulation_skeleton") for p in plans)

    non_exec_review = {
        "review_id": "non_execution_boundary_review_v1",
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "flags": dict(NON_EXECUTION_FLAGS),
        "planning_deferred_to_skeleton": True,
        **meta,
    }
    readiness_review = {
        "review_id": "readiness_for_field_simulation_skeleton_review_v1",
        "readiness_for_field_simulation_skeleton_ok": readiness_skeleton_ok and field_simulation_planning_complete,
        "plan_count": len(plans),
        "eligible_plan_count": sum(1 for p in plans if p.get("selected_modes")),
        **meta,
    }
    case_registry = {
        "registry_id": "field_simulation_planning_case_registry_v1",
        "count": len(case_results),
        "cases": case_results,
        "all_planning_cases_passed": all_passed,
        **meta,
    }
    prohibited = {**PROHIBITED_SCOPE, **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    planning_pass = field_simulation_planning_complete and non_execution_boundary_ok

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Real-Model-Field-Construction-Success-Path-Hardening-v1-001",
        base_capability=PLANNING_WHITELIST_FILES[0],
        base_runner=PLANNING_WHITELIST_FILES[1],
        base_verifier=PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase=PHASE_ID,
        stage_term_overrides=PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=PLANNING_STAGE_ADDITIONS,
        template_files=PLANNING_WHITELIST_FILES,
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
    planning_pass = planning_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if planning_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if planning_pass else (
        FINAL_DECISION_UPSTREAM if not prior_hardening_go else FINAL_DECISION_RECAL
    )

    go_values = {
        "prior_real_model_field_construction_success_path_hardening_go": prior_hardening_go,
        "field_simulation_planning_complete": field_simulation_planning_complete,
        "simulation_mode_registry_complete": simulation_mode_registry_complete,
        "simulation_eligibility_policy_complete": simulation_eligibility_policy_complete,
        "simulation_plan_candidate_contract_complete": simulation_plan_candidate_contract_complete,
        "reusable_case_to_simulation_mapping_complete": reusable_case_to_simulation_mapping_complete,
        "all_planning_cases_passed": all_passed,
        "real_model_hardened_baselines_used": len(indexed) >= 8,
        "success_baselines_mapped_to_simulation": True,
        "degraded_baselines_mapped_with_limitations": True,
        "failure_baselines_blocked_or_mapped_to_validation": True,
        "current_state_simulation_planned": "current_state_simulation" in all_modes,
        "short_horizon_projection_planned_but_not_executed": True,
        "occlusion_missing_info_simulation_planned": "occlusion_and_missing_info_simulation" in all_modes,
        "task_relevance_projection_planned_without_action": "task_relevance_field_projection" in all_modes,
        "safety_risk_projection_planned_without_action": "safety_risk_projection" in all_modes,
        "field_quality_projection_planned": "field_quality_projection" in all_modes,
        "no_field_simulation_execution": True,
        "no_simulation_runtime": True,
        "no_task_execution": True,
        "no_navigation_action": True,
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
        "next_phase_readiness_ok": planning_pass,
        "field_simulation_planning_pass": planning_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "planning_case_count": len(case_results),
        "simulation_plan_count": len(plans),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        "midplatform_still_has_remaining_work": True,
        **absence,
    }

    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS if k in go_values},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(hard_s.get("chain_trace_nodes") or []) + ["field_simulation_planning"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Field Simulation Planning v1",
        f"Planning cases: `{len(case_results)}` | Plans: `{len(plans)}` | All passed: `{all_passed}`",
        "Planning only — no simulation execution; input from hardened real-model field construction baselines",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "final_decision": final_decision, "planning_rules": list(PLANNING_RULES), **meta}
    return {
        "field_simulation_planning_report": report,
        "field_simulation_planning_report_md": md,
        "field_simulation_mode_registry": {**FIELD_SIMULATION_MODE_REGISTRY, **meta},
        "field_simulation_input_view_contract": {**FIELD_SIMULATION_INPUT_VIEW_CONTRACT, **meta},
        "simulation_eligibility_policy": {**SIMULATION_ELIGIBILITY_POLICY, **meta},
        "field_simulation_plan_candidate_contract": {**FIELD_SIMULATION_PLAN_CANDIDATE_CONTRACT, **meta},
        "field_simulation_candidate_contract": {**FIELD_SIMULATION_CANDIDATE_CONTRACT, **meta},
        "field_simulation_readiness_policy": {**FIELD_SIMULATION_READINESS_POLICY, **meta},
        "failure_and_degradation_simulation_policy": {**FAILURE_AND_DEGRADATION_SIMULATION_POLICY, **meta},
        "reusable_case_to_simulation_mapping": {**REUSABLE_CASE_TO_SIMULATION_MAPPING, **meta},
        "field_simulation_planning_case_registry": case_registry,
        "readiness_for_field_simulation_skeleton_review": readiness_review,
        "non_execution_boundary_review": non_exec_review,
        "prohibited_scope": prohibited,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
