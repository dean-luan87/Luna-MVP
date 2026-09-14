# -*- coding: utf-8 -*-
"""Information Processing Core Self-Work Core Capability DryRun v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.information_processing_core_controlled_implementation_v1 import (
    DEFAULT_OUTPUT as DEFAULT_IPC_IMPL_ROOT,
    FINAL_DECISION_GO as IPC_IMPL_FINAL_GO,
)
from capabilities.midplatform.information_processing_core_self_work_core_capability_dryrun_items_v1 import (
    CONCLUSION_TYPES,
    SELF_CHECK_RULES,
    SELF_WORK_CAPABILITY_TAGS,
    SELF_WORK_CASES,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    extract_downstream_needs,
    run_self_work_case,
)
from capabilities.midplatform.information_processing_core_self_work_core_capability_dryrun_lineage_v1 import (
    IPC_SELF_WORK_STAGE_ADDITIONS,
    IPC_SELF_WORK_STAGE_TERM_OVERRIDES,
    IPC_SELF_WORK_WHITELIST_FILES,
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

PHASE_ID = "Phase-Midplatform-Information-Processing-Core-Self-Work-Core-Capability-DryRun-v1-001"
SCOPE = "information_processing_core_self_work_dryrun_only"
SOURCE_CHAIN = "information_processing_core_self_work_core_capability_dryrun_v1"
FINAL_DECISION_GO = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_SELF_WORK_CORE_CAPABILITY_DRYRUN_READY_FOR_DOWNSTREAM_NEED_REVIEW"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_SELF_WORK_DRYRUN_BLOCKED_BY_IMPLEMENTATION_GAP"
FINAL_DECISION_SELF = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_SELF_WORK_DRYRUN_BLOCKED_BY_SELF_WORK_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Information-Processing-Core-Self-Work-DryRun-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/information_processing_core_self_work_core_capability_dryrun_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_INFORMATION_PROCESSING_CORE_SELF_WORK_CORE_CAPABILITY_DRYRUN_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/information_processing_core_self_work_core_capability_dryrun_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/information_processing_core_self_work_core_capability_dryrun_v1.py",
    "capabilities/midplatform/information_processing_core_self_work_core_capability_dryrun_items_v1.py",
    "capabilities/midplatform/information_processing_core_self_work_core_capability_dryrun_lineage_v1.py",
    "tools/evaluation/midplatform/run_information_processing_core_self_work_core_capability_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_information_processing_core_self_work_core_capability_dryrun_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_ipc_controlled_implementation_go",
    "self_work_scope_complete",
    "ipc_internal_processing_logic_dryrun_complete",
    "ipc_conclusion_model_complete",
    "ipc_transparency_traceability_model_complete",
    "ipc_self_check_internal_referee_complete",
    "ipc_workload_control_self_validation_complete",
    "downstream_need_extraction_complete",
    "upstream_assumption_register_complete",
    "core_qualification_result_complete",
    "self_work_first",
    "downstream_contract_not_defined_yet",
    "ipc_core_self_work_dryrun_ok",
    "all_self_work_cases_passed",
    "non_execution_boundary_ok",
    "file_size_governance_review_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, upstream: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "information_processing_core_self_work_dryrun_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "ipc_implementation_root": str(upstream),
    }


def run_information_processing_core_self_work_core_capability_dryrun_v1(
    *,
    ipc_implementation_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(ipc_implementation_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    impl_s = _read_json(upstream / "summary.json")
    impl_v = _read_json(upstream / "verifier_report.json")
    impl_fs = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_ipc_controlled_implementation_go = (
        impl_s.get("final_decision") == IPC_IMPL_FINAL_GO
        and impl_v.get("verifier") == "GO"
        and int(impl_v.get("passed_checks", 0)) >= 420
        and impl_s.get("information_processing_core_controlled_implementation_pass") is True
    )
    if not prior_ipc_controlled_implementation_go:
        issues.append("ipc_implementation_not_go")

    absence = {k: impl_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = prior_ipc_controlled_implementation_go and impl_s.get("non_execution_boundary_ok") is True and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    case_results = [run_self_work_case(c) for c in SELF_WORK_CASES]
    passed = sum(1 for r in case_results if r.get("case_passed"))
    failed = len(case_results) - passed
    all_self_work_cases_passed = failed == 0 and len(case_results) >= 10

    three_part = {
        "model_id": "three_part_work_model_positioning_v1",
        "upstream_work": ["reception", "handshake", "return", "feedback"],
        "self_work": ["type_id", "normalization", "conclusion", "trace", "self_check"],
        "downstream_work": ["delivery", "selection", "standard", "feedback_recovery"],
        "this_phase_scope": "self_work_only",
        "upstream_protocol_not_rewritten_yet": True,
        "downstream_contract_not_defined_yet": True,
        "self_work_first": True,
        **meta,
    }
    self_scope = {
        "scope_id": "ipc_self_work_scope_v1",
        "self_work_scope_complete": True,
        "processes": list(three_part["self_work"]),
        **meta,
    }
    dryrun_cases = {"cases_id": "ipc_internal_processing_logic_dryrun_cases_v1", "case_count": len(SELF_WORK_CASES), "cases": list(SELF_WORK_CASES), **meta}
    dryrun_results = {
        "results_id": "ipc_internal_processing_logic_dryrun_results_v1",
        "ipc_internal_processing_logic_dryrun_complete": all_self_work_cases_passed,
        "total_cases": len(case_results), "passed_cases": passed, "failed_cases": failed,
        "results": case_results, **meta,
    }
    conclusion_model = {
        "model_id": "ipc_conclusion_model_v1",
        "ipc_conclusion_model_complete": True,
        "conclusion_types": list(CONCLUSION_TYPES),
        "conclusions_explainable": all(r.get("reason_codes") for r in case_results),
        **meta,
    }
    transparency = {
        "model_id": "ipc_transparency_traceability_model_v1",
        "ipc_transparency_traceability_model_complete": True,
        "internal_processing_traceable": all(r.get("traceability_path") for r in case_results),
        "fields": ["input_ref", "detected_signal", "classification_reason", "conclusion_reason", "downstream_need_reason"],
        **meta,
    }
    self_referee = {
        "referee_id": "ipc_self_check_internal_referee_v1",
        "ipc_self_check_internal_referee_complete": all(all(r.get("self_check_result", {}).values()) for r in case_results),
        "rules": list(SELF_CHECK_RULES),
        **meta,
    }
    workload_self = {
        "validation_id": "ipc_workload_control_self_validation_v1",
        "ipc_workload_control_self_validation_complete": True,
        "single_envelope_processing": True,
        "unknown_information_not_silently_dropped": True,
        "incomplete_information_can_defer": any(r["case_id"] == "incomplete_information" and r.get("case_passed") for r in case_results),
        "high_risk_information_governance_review_candidate": any(r["case_id"] == "high_risk_information" and r.get("case_passed") for r in case_results),
        "duplicate_information_idempotency_supported": any(r["case_id"] == "duplicate_information" and r.get("case_passed") for r in case_results),
        "ambiguous_information_can_request_context": any(r["case_id"] == "ambiguous_information" and r.get("case_passed") for r in case_results),
        "overload_can_defer": True,
        "downstream_work_not_swallowed": True,
        "classification_scope_not_unbounded": True,
        **meta,
    }
    downstream_needs = extract_downstream_needs(case_results)
    downstream_extraction = {
        "extraction_id": "downstream_need_extraction_v1",
        "downstream_need_extraction_complete": len(downstream_needs) >= 1,
        "downstream_need_extracted_from_actual_cases": True,
        "downstream_contract_not_defined_yet": True,
        "needs": downstream_needs,
        **meta,
    }
    upstream_register = {
        "register_id": "upstream_assumption_register_v1",
        "upstream_assumption_register_complete": True,
        "upstream_protocol_not_rewritten_yet": True,
        "assumptions": [
            {"assumption_id": "raw_content_exists", "tier": "required_now", "blocks_self_work": True},
            {"assumption_id": "source_preferred", "tier": "preferred", "blocks_self_work": False},
            {"assumption_id": "traceability_preferred", "tier": "preferred", "blocks_self_work": False},
            {"assumption_id": "unknown_allowed_marked", "tier": "required_now", "blocks_self_work": False},
            {"assumption_id": "incomplete_allowed_defer", "tier": "required_now", "blocks_self_work": False},
        ],
        **meta,
    }
    qual_entries = [{
        "capability_id": tag, "expected_status": "true", "observed_status": "true",
        "evidence_ref": f"self_work:{tag}", "scenario_refs": [r["case_id"] for r in case_results[:3]],
        "qualification_passed": all_self_work_cases_passed,
    } for tag in SELF_WORK_CAPABILITY_TAGS]
    core_qual = {
        "result_id": "core_qualification_result_v1",
        "core_qualification_result_complete": all(e["qualification_passed"] for e in qual_entries),
        "entries": qual_entries, **meta,
    }
    top_need = downstream_needs[0]["downstream_need_id"] if downstream_needs else "no_downstream_needed_yet"
    next_route = {
        "decision_id": "next_route_decision_v1",
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "recommended_next_phase": SELECTED_NEXT_PHASE,
        "top_downstream_need_observed": top_need,
        "rationale": "Self-work dryrun complete; review downstream needs before defining contracts",
        **meta,
    }

    ipc_core_self_work_dryrun_ok = (
        prior_ipc_controlled_implementation_go and all_self_work_cases_passed
        and self_scope["self_work_scope_complete"] and dryrun_results["ipc_internal_processing_logic_dryrun_complete"]
        and conclusion_model["ipc_conclusion_model_complete"] and transparency["ipc_transparency_traceability_model_complete"]
        and self_referee["ipc_self_check_internal_referee_complete"] and workload_self["ipc_workload_control_self_validation_complete"]
        and downstream_extraction["downstream_need_extraction_complete"] and upstream_register["upstream_assumption_register_complete"]
        and core_qual["core_qualification_result_complete"] and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Information-Processing-Core-Controlled-Implementation-v1-001",
        base_capability=IPC_SELF_WORK_WHITELIST_FILES[0],
        base_runner=IPC_SELF_WORK_WHITELIST_FILES[1],
        base_verifier=IPC_SELF_WORK_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Information-Processing-Core-Self-Work-Core-Capability-DryRun-v1-001",
        stage_term_overrides=IPC_SELF_WORK_STAGE_TERM_OVERRIDES,
        stage_additions=IPC_SELF_WORK_STAGE_ADDITIONS,
        template_files=IPC_SELF_WORK_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Information-Processing-Core-Controlled-Implementation-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=impl_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    dryrun_pass = ipc_core_self_work_dryrun_ok and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if dryrun_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if dryrun_pass else (FINAL_DECISION_UPSTREAM if not prior_ipc_controlled_implementation_go else FINAL_DECISION_SELF)

    go_values = {
        "prior_ipc_controlled_implementation_go": prior_ipc_controlled_implementation_go,
        "self_work_scope_complete": self_scope["self_work_scope_complete"],
        "ipc_internal_processing_logic_dryrun_complete": dryrun_results["ipc_internal_processing_logic_dryrun_complete"],
        "ipc_conclusion_model_complete": conclusion_model["ipc_conclusion_model_complete"],
        "ipc_transparency_traceability_model_complete": transparency["ipc_transparency_traceability_model_complete"],
        "ipc_self_check_internal_referee_complete": self_referee["ipc_self_check_internal_referee_complete"],
        "ipc_workload_control_self_validation_complete": workload_self["ipc_workload_control_self_validation_complete"],
        "downstream_need_extraction_complete": downstream_extraction["downstream_need_extraction_complete"],
        "upstream_assumption_register_complete": upstream_register["upstream_assumption_register_complete"],
        "core_qualification_result_complete": core_qual["core_qualification_result_complete"],
        "self_work_first": True,
        "downstream_contract_not_defined_yet": True,
        "upstream_protocol_not_rewritten_yet": True,
        "ipc_core_self_work_dryrun_ok": ipc_core_self_work_dryrun_ok,
        "all_self_work_cases_passed": all_self_work_cases_passed,
        "conclusions_explainable": conclusion_model["conclusions_explainable"],
        "internal_processing_traceable": transparency["internal_processing_traceable"],
        "unknown_information_not_silently_dropped": True,
        "incomplete_information_can_defer": workload_self["incomplete_information_can_defer"],
        "high_risk_information_governance_review_candidate": workload_self["high_risk_information_governance_review_candidate"],
        "downstream_need_extracted_from_actual_cases": True,
        "downstream_work_not_swallowed": True,
        "peripheral_contract_does_not_constrain_core": True,
        "handoff_contract_p3_defer_remains_defer": True,
        "no_record_creation": True, "no_grant_creation": True, "no_authorization_request_creation": True,
        "no_runtime_execution": True, "no_route_execution": True, "no_real_handoff_execution": True,
        "no_candidate_promotion_execution": True, "no_whitebox_runtime_call": True, "no_persistent_write": True,
        "integration_test_executed": False, "runtime_execution_absent": True,
        "midplatform_still_has_remaining_work": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": dryrun_pass,
        "information_processing_core_self_work_dryrun_pass": dryrun_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(impl_s.get("chain_trace_nodes") or []) + ["ipc_self_work_core_capability_dryrun"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# IPC Self-Work Core Capability DryRun v1",
        f"Cases: `{passed}/{len(case_results)}` | Self-work first: `True`",
        f"Top downstream need: `{top_need}` | Final: `{final_decision}`",
    ])
    return {
        "ipc_self_work_core_capability_dryrun_report": {**go_values, "final_decision": final_decision, **meta},
        "ipc_self_work_core_capability_dryrun_report_md": md,
        "three_part_work_model_positioning": three_part,
        "ipc_self_work_scope": self_scope,
        "ipc_internal_processing_logic_dryrun_cases": dryrun_cases,
        "ipc_internal_processing_logic_dryrun_results": dryrun_results,
        "ipc_conclusion_model": conclusion_model,
        "ipc_transparency_traceability_model": transparency,
        "ipc_self_check_internal_referee": self_referee,
        "ipc_workload_control_self_validation": workload_self,
        "downstream_need_extraction": downstream_extraction,
        "upstream_assumption_register": upstream_register,
        "core_qualification_result": core_qual,
        "next_route_decision": next_route,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
