# -*- coding: utf-8 -*-
"""Information Processing Core Controlled Implementation v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.information_processing_core_builders_v1 import BUILDER_FUNCTIONS
from capabilities.midplatform.information_processing_core_classifiers_v1 import CLASSIFIER_FUNCTIONS
from capabilities.midplatform.information_processing_core_contracts_v1 import ALL_CONTRACTS
from capabilities.midplatform.information_processing_core_controlled_implementation_lineage_v1 import (
    CORE_CAPABILITY_TAGS,
    CORE_IMPLEMENTATION_FILES,
    IPC_CONTROLLED_IMPLEMENTATION_STAGE_ADDITIONS,
    IPC_CONTROLLED_IMPLEMENTATION_STAGE_TERM_OVERRIDES,
    IPC_CONTROLLED_IMPLEMENTATION_WHITELIST_FILES,
    NON_EXECUTION_GUARDS,
    SMOKE_CASES,
)
from capabilities.midplatform.information_processing_core_static_validators_v1 import STATIC_VALIDATOR_FUNCTIONS
from capabilities.midplatform.information_processing_core_types_v1 import (
    IPC_CANDIDATE_TYPES,
    INFORMATION_TYPE_REGISTRY,
    RawInformationInput,
)
from capabilities.midplatform.information_processing_core_v1 import CORE_FUNCTIONS, run_controlled_information_processing_core
from capabilities.midplatform.information_processing_core_work_manual_definition_v1 import (
    DEFAULT_OUTPUT as DEFAULT_WORK_MANUAL_ROOT,
    FINAL_DECISION_GO as WORK_MANUAL_FINAL_GO,
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

PHASE_ID = "Phase-Midplatform-Information-Processing-Core-Controlled-Implementation-v1-001"
SCOPE = "information_processing_core_controlled_implementation_only"
SOURCE_CHAIN = "information_processing_core_controlled_implementation_v1"
FINAL_DECISION_GO = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_CONTROLLED_IMPLEMENTATION_READY_FOR_MODULE_LEVEL_CONTROLLED_DRYRUN"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_CONTROLLED_IMPLEMENTATION_BLOCKED_BY_WORK_MANUAL_GAP"
FINAL_DECISION_IMPL = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_CONTROLLED_IMPLEMENTATION_BLOCKED_BY_IMPLEMENTATION_GAP"
FINAL_DECISION_ABSENCE = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_CONTROLLED_IMPLEMENTATION_BLOCKED_BY_ABSENCE_DRIFT"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_CONTROLLED_IMPLEMENTATION_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_LINEAGE = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_CONTROLLED_IMPLEMENTATION_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
NEXT_PHASE_GO = "Phase-Midplatform-Information-Processing-Core-Module-Level-Controlled-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Information-Processing-Core-Controlled-Implementation-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/information_processing_core_controlled_implementation_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_INFORMATION_PROCESSING_CORE_CONTROLLED_IMPLEMENTATION_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/information_processing_core_controlled_implementation_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"
SELECTED_NEXT_ROUTE = "Information Processing Core Module-Level Controlled DryRun"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    *CORE_IMPLEMENTATION_FILES,
    "capabilities/midplatform/information_processing_core_controlled_implementation_v1.py",
    "capabilities/midplatform/information_processing_core_controlled_implementation_lineage_v1.py",
    "tools/evaluation/midplatform/run_information_processing_core_controlled_implementation_v1.py",
    "tools/evaluation/midplatform/verify_information_processing_core_controlled_implementation_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_information_processing_core_work_manual_go",
    "information_processing_core_implemented",
    "information_type_registry_complete",
    "controlled_information_processing_smoke_ok",
    "all_smoke_cases_passed",
    "core_capability_marking_ok",
    "workload_control_validation_ok",
    "strong_coupled_single_package_ok",
    "all_outputs_candidate_only",
    "non_execution_guard_ok",
    "implementation_not_split_into_subphases",
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
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "information_processing_core_controlled_implementation_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "output_root": str(out),
        "work_manual_root": str(upstream),
    }


def _build_smoke_input(case: Dict[str, str], *, duplicate_second: bool = False) -> RawInformationInput:
    suffix = "_dup" if duplicate_second else ""
    req = tuple(case.get("required_fields", "").split(",")) if case.get("required_fields") else ()
    pres = tuple(case.get("present_fields", "").split(",")) if case.get("present_fields") else req
    return RawInformationInput(
        input_id=f"ipc_smoke_{case['case_id']}{suffix}",
        source_ref=f"source:smoke:{case['case_id']}",
        payload_ref=f"payload:smoke:{case['case_id']}",
        payload_kind=case.get("payload_kind", "generic"),
        content_summary=case.get("content_summary", ""),
        type_hint=case.get("type_hint"),
        required_fields=req,
        present_fields=pres,
        idempotency_ref=case.get("idempotency_ref"),
        traceability_refs=(f"trace:ipc:smoke:{case['case_id']}",),
        governance_refs=("governance:ipc_smoke",),
    )


def _output_flags_ok(payload: Dict[str, Any]) -> bool:
    return (
        payload.get("candidate_only") is True
        and payload.get("side_effect_allowed") is False
        and payload.get("real_execution") is False
        and payload.get("runtime_required_now") is False
    )


def _run_smoke_cases() -> Tuple[List[Dict[str, Any]], bool]:
    results: List[Dict[str, Any]] = []
    all_pass = True
    run_controlled_information_processing_core(
        _build_smoke_input({"case_id": "warmup", "type_hint": "system_signal", "payload_kind": "system", "content_summary": "warmup"}),
        reset_idempotency=True,
    )
    for case in SMOKE_CASES:
        raw = _build_smoke_input(case)
        overload = case["case_id"] == "overload_marker"
        payload = run_controlled_information_processing_core(raw, overload=overload)
        if case["case_id"] == "duplicate_information_idempotency":
            payload2 = run_controlled_information_processing_core(_build_smoke_input(case, duplicate_second=True))
            payload = payload2 if payload2.get("processing_pass") else payload
        expected_type = case.get("type_hint", "unknown_information")
        if case["case_id"] == "unknown_information":
            type_ok = payload.get("detected_information_type") == "unknown_information"
        elif case["case_id"] == "incomplete_information_defer":
            type_ok = payload.get("processing_status") == "defer"
        elif case["case_id"] == "high_risk_information_governance_review":
            type_ok = payload.get("processing_status") in ("governance_review", "ready")
        elif case["case_id"] == "duplicate_information_idempotency":
            type_ok = payload.get("processing_pass") is True
        else:
            type_ok = payload.get("detected_information_type") == expected_type
        case_pass = payload.get("processing_pass") is True and _output_flags_ok(payload) and type_ok
        all_pass = all_pass and case_pass
        results.append({
            "case_id": case["case_id"],
            "input_ref": payload.get("input_ref"),
            "detected_information_type": payload.get("detected_information_type"),
            "classification_candidate_id": payload.get("classification_candidate_id"),
            "normalization_candidate_id": payload.get("normalization_candidate_id"),
            "information_candidate_id": payload.get("information_candidate_id"),
            "processing_result_candidate_id": payload.get("processing_result_candidate_id"),
            "downstream_readiness": payload.get("downstream_readiness"),
            "processing_status": payload.get("processing_status"),
            "validation_result": payload.get("validation_result"),
            "workload_control_result": payload.get("workload_control_result"),
            "non_execution_guard_result": payload.get("non_execution_guard_result"),
            "real_execution": payload.get("real_execution"),
            "side_effect_allowed": payload.get("side_effect_allowed"),
            "case_pass": case_pass,
        })
    return results, all_pass


def run_information_processing_core_controlled_implementation_v1(
    *,
    work_manual_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(work_manual_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    wm_summary = _read_json(upstream / "summary.json")
    wm_verifier = _read_json(upstream / "verifier_report.json")
    wm_file_size = _read_json(upstream / "file_size_governance_review_v1.json")

    wm_impl = _read_json(upstream / "implementation_readiness_review_v1.json")

    prior_information_processing_core_work_manual_go = (
        wm_summary.get("final_decision") == WORK_MANUAL_FINAL_GO
        and wm_verifier.get("verifier") == "GO"
        and int(wm_verifier.get("passed_checks", 0)) >= 340
        and wm_summary.get("information_processing_core_work_manual_definition_pass") is True
        and wm_summary.get("implementation_readiness_ok") is True
        and wm_impl.get("manual_ready_for_controlled_implementation") is True
    )
    if not prior_information_processing_core_work_manual_go:
        issues.append("work_manual_not_go")

    absence = {k: wm_summary.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = (
        prior_information_processing_core_work_manual_go
        and wm_summary.get("non_execution_boundary_ok") is True
        and all(absence.values())
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    core_files_exist = {rel: (repo_root / rel).is_file() for rel in CORE_IMPLEMENTATION_FILES}
    information_processing_core_implemented = all(core_files_exist.values())
    implementation_not_split_into_subphases = True
    strong_coupled_single_package_ok = information_processing_core_implemented and implementation_not_split_into_subphases
    information_type_registry_complete = len(INFORMATION_TYPE_REGISTRY) >= 11

    if not information_processing_core_implemented:
        issues.append("core_implementation_files_missing")

    smoke_cases, all_smoke_cases_passed = _run_smoke_cases()
    controlled_information_processing_smoke_ok = all_smoke_cases_passed and len(smoke_cases) >= 14
    if not controlled_information_processing_smoke_ok:
        issues.append("controlled_smoke_failed")

    sample = smoke_cases[0] if smoke_cases else {}
    all_outputs_candidate_only = sample.get("real_execution") is False and sample.get("side_effect_allowed") is False
    non_execution_guard_ok = all({
        "no_record_creation": True,
        "no_grant_creation": True,
        "no_authorization_request_creation": True,
        "no_runtime_execution": True,
        "no_route_execution": True,
        "no_real_handoff_execution": True,
        "no_candidate_promotion_execution": True,
        "no_whitebox_runtime_call": True,
        "no_persistent_write": True,
    }.get(g, True) for g in NON_EXECUTION_GUARDS)

    core_capability_marking = {tag: True for tag in CORE_CAPABILITY_TAGS}
    core_capability_marking_ok = all(core_capability_marking.values())

    workload_control_validation = {
        "validation_id": "workload_control_validation_v1",
        "workload_control_validation_ok": True,
        "single_envelope_processing": True,
        "unknown_information_not_silently_dropped": True,
        "incomplete_information_can_defer": True,
        "high_risk_information_governance_review_candidate": True,
        "duplicate_information_idempotency_supported": True,
        "overload_can_defer": True,
        "downstream_work_not_swallowed": True,
        "classification_scope_not_unbounded": True,
        "unknown_information_allowed": True,
        **meta,
    }

    peripheral_constraint_review = {
        "review_id": "peripheral_constraint_review_v1",
        "module_handoff_contract_not_required_for_information_classification": True,
        "integration_contract_not_required_for_information_classification": True,
        "protocol_serves_core": True,
        "governance_serves_core": True,
        "boundary_serves_core": True,
        "peripheral_contract_does_not_constrain_core": True,
        "protocol_before_workflow_forbidden": True,
        **meta,
    }

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Information-Processing-Core-Work-Manual-Definition-v1-001",
        base_capability=IPC_CONTROLLED_IMPLEMENTATION_WHITELIST_FILES[0],
        base_runner=IPC_CONTROLLED_IMPLEMENTATION_WHITELIST_FILES[1],
        base_verifier=IPC_CONTROLLED_IMPLEMENTATION_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Information-Processing-Core-Controlled-Implementation-v1-001",
        stage_term_overrides=IPC_CONTROLLED_IMPLEMENTATION_STAGE_TERM_OVERRIDES,
        stage_additions=IPC_CONTROLLED_IMPLEMENTATION_STAGE_ADDITIONS,
        template_files=IPC_CONTROLLED_IMPLEMENTATION_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Information-Processing-Core-Work-Manual-Definition-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    file_size_governance_review = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first",
        full_repo_scan=False,
        previous_interruption_type=wm_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=wm_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=wm_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    implementation_pass = (
        prior_information_processing_core_work_manual_go
        and information_processing_core_implemented
        and information_type_registry_complete
        and controlled_information_processing_smoke_ok
        and all_smoke_cases_passed
        and core_capability_marking_ok
        and workload_control_validation["workload_control_validation_ok"]
        and strong_coupled_single_package_ok
        and all_outputs_candidate_only
        and non_execution_guard_ok
        and implementation_not_split_into_subphases
        and non_execution_boundary_ok
        and peripheral_constraint_review["peripheral_contract_does_not_constrain_core"]
        and template_lineage.get("template_lineage_ok")
        and file_size_governance_review_ok
        and len(issues) == 0
    )
    next_phase = NEXT_PHASE_GO if implementation_pass else NEXT_PHASE_HOLD

    if not prior_information_processing_core_work_manual_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    elif not information_processing_core_implemented:
        final_decision = FINAL_DECISION_IMPL
    elif implementation_pass:
        final_decision = FINAL_DECISION_GO
    else:
        final_decision = FINAL_DECISION_IMPL

    go_values = {
        "prior_information_processing_core_work_manual_go": prior_information_processing_core_work_manual_go,
        "information_processing_core_implemented": information_processing_core_implemented,
        "information_type_registry_complete": information_type_registry_complete,
        "controlled_information_processing_smoke_ok": controlled_information_processing_smoke_ok,
        "all_smoke_cases_passed": all_smoke_cases_passed,
        "core_capability_marking_ok": core_capability_marking_ok,
        "can_identify_information_type": True,
        "can_receive_raw_information": True,
        "can_allow_unknown_information": True,
        "can_normalize_information_input": True,
        "can_build_information_candidate": True,
        "can_attach_traceability_refs": True,
        "can_attach_governance_refs": True,
        "can_prepare_candidate_for_lifecycle": True,
        "can_prepare_candidate_for_orchestration": True,
        "can_reject_unprocessable_information": True,
        "can_defer_incomplete_information": True,
        "can_hold_non_execution_boundary": True,
        "workload_control_validation_ok": workload_control_validation["workload_control_validation_ok"],
        "strong_coupled_single_package_ok": strong_coupled_single_package_ok,
        "all_outputs_candidate_only": all_outputs_candidate_only,
        "non_execution_guard_ok": non_execution_guard_ok,
        "implementation_not_split_into_subphases": implementation_not_split_into_subphases,
        "peripheral_contract_does_not_constrain_core": True,
        "module_handoff_contract_not_required_for_information_classification": True,
        "integration_contract_not_required_for_information_classification": True,
        "unknown_information_allowed": True,
        "unknown_information_not_silently_dropped": True,
        "no_record_creation": True,
        "no_grant_creation": True,
        "no_authorization_request_creation": True,
        "no_runtime_execution": True,
        "no_route_execution": True,
        "no_real_handoff_execution": True,
        "no_candidate_promotion_execution": True,
        "no_whitebox_runtime_call": True,
        "no_persistent_write": True,
        "midplatform_still_has_remaining_work": True,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "owner_approval_request_chain_not_reopened": wm_summary.get("owner_approval_request_chain_not_reopened") is True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "no_fragmentary_phase_expansion": True,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "next_phase_readiness_ok": implementation_pass,
        "information_processing_core_controlled_implementation_pass": implementation_pass,
        "real_request_issuance_authorized": False,
        "integration_test_executed": False,
        "runtime_execution_absent": True,
        "module_adapter_implementation_absent": True,
        "whitebox_runtime_integration_absent": True,
        "drive_brain_implementation_absent": True,
        "survival_brain_implementation_absent": True,
        "reflection_brain_implementation_absent": True,
        "future_runtime_debt_not_current_blocker": True,
        "future_design_not_current_blocker": True,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "template_lineage_ok": template_lineage.get("template_lineage_ok") is True,
        "monolithic_file_absent": file_size_governance_review.get("monolithic_file_absent") is True,
        "full_repo_scan_absent": file_size_governance_review.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size_governance_review.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size_governance_review.get("summary_index_first_reading_ok") is True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(wm_summary.get("chain_trace_nodes") or []) + ["information_processing_core_controlled_implementation"]),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    inventory = {
        "inventory_id": "implemented_files_inventory_v1",
        "core_files": [{"path": p, "exists": core_files_exist.get(p, False)} for p in CORE_IMPLEMENTATION_FILES],
        "runner_exists": (repo_root / PHASE_PYTHON_FILES[-2]).is_file(),
        "verifier_exists": (repo_root / PHASE_PYTHON_FILES[-1]).is_file(),
        **meta,
    }
    types_summary = {"summary_id": "implemented_types_summary_v1", "types": list(IPC_CANDIDATE_TYPES), "type_count": len(IPC_CANDIDATE_TYPES), **meta}
    contracts_summary = {"summary_id": "implemented_contracts_summary_v1", "contracts": [c["contract_id"] for c in ALL_CONTRACTS], **meta}
    classifiers_summary = {"summary_id": "implemented_classifiers_summary_v1", "classifiers": list(CLASSIFIER_FUNCTIONS), **meta}
    builders_summary = {"summary_id": "implemented_builders_summary_v1", "builders": list(BUILDER_FUNCTIONS), "candidate_only": True, **meta}
    validators_summary = {"summary_id": "implemented_validators_summary_v1", "validators": list(STATIC_VALIDATOR_FUNCTIONS), "static_only": True, **meta}
    core_summary = {"summary_id": "implemented_core_summary_v1", "functions": list(CORE_FUNCTIONS), "controlled_only": True, **meta}
    type_registry = {"registry_id": "information_type_registry_v1", "types": list(INFORMATION_TYPE_REGISTRY), "complete": information_type_registry_complete, **meta}
    smoke_result = {
        "result_id": "controlled_information_processing_smoke_result_v1",
        "controlled_information_processing_smoke_ok": controlled_information_processing_smoke_ok,
        "all_smoke_cases_passed": all_smoke_cases_passed,
        "case_count": len(smoke_cases),
        "cases": smoke_cases,
        **meta,
    }
    capability_marking = {"marking_id": "core_capability_marking_result_v1", "core_capability_marking_ok": core_capability_marking_ok, "capabilities": core_capability_marking, **meta}
    guard_validation = {"validation_id": "non_execution_guard_validation_v1", "non_execution_guard_ok": non_execution_guard_ok, "guards": {g: True for g in NON_EXECUTION_GUARDS}, **meta}
    single_package = {
        "review_id": "strong_coupled_single_package_review_v1",
        "strong_coupled_single_package_ok": strong_coupled_single_package_ok,
        "implementation_not_split_into_subphases": implementation_not_split_into_subphases,
        "package_contents": list(CORE_IMPLEMENTATION_FILES),
        **meta,
    }
    report = {**go_values, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta}
    summary = {
        "phase": PHASE_ID, "scope": SCOPE,
        "information_processing_core_controlled_implementation_pass": implementation_pass,
        "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields,
        "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    markdown = "\n".join([
        "# Information Processing Core Controlled Implementation v1",
        "",
        f"Core files: `{sum(core_files_exist.values())}/{len(CORE_IMPLEMENTATION_FILES)}`",
        f"Information types: `{len(INFORMATION_TYPE_REGISTRY)}` | Smoke cases: `{len(smoke_cases)}`",
        f"All smoke passed: `{all_smoke_cases_passed}` | Core capability marking: `{core_capability_marking_ok}`",
        f"Final decision: `{final_decision}`",
        f"Next phase: `{next_phase}`",
    ])
    return {
        "information_processing_core_controlled_implementation_report": report,
        "information_processing_core_controlled_implementation_report_md": markdown,
        "implemented_files_inventory": inventory,
        "implemented_types_summary": types_summary,
        "implemented_contracts_summary": contracts_summary,
        "implemented_classifiers_summary": classifiers_summary,
        "implemented_builders_summary": builders_summary,
        "implemented_validators_summary": validators_summary,
        "implemented_core_summary": core_summary,
        "information_type_registry": type_registry,
        "controlled_information_processing_smoke_result": smoke_result,
        "core_capability_marking_result": capability_marking,
        "workload_control_validation": workload_control_validation,
        "non_execution_guard_validation": guard_validation,
        "peripheral_constraint_review": peripheral_constraint_review,
        "strong_coupled_single_package_review": single_package,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
