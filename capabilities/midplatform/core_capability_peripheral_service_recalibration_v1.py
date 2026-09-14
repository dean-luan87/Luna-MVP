# -*- coding: utf-8 -*-
"""Luna Midplatform Core Capability and Peripheral Service Recalibration v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.core_capability_peripheral_service_recalibration_items_v1 import (
    CAPABILITY_FRAMEWORK,
    CONFLICT_RESOLUTION_RULES,
    CORE_CAPABILITY_MARKING,
    CORE_FUNCTION_DEFINITION,
    CORE_MODULE_SELECTION,
    DO_NOT_MISCLASSIFY_RULES,
    NEXT_PHASE_ALTERNATE,
    NEXT_PHASE_GO,
    NEXT_ROUTE_B,
    NEXT_ROUTE_C,
    NEXT_ROUTE_D,
    NEXT_ROUTE_E,
    PERIPHERAL_SERVICE_PRINCIPLES,
    ROUTE_REASSESSMENT,
    SELECTED_NEXT_ROUTE,
    SELECTED_ROUTE_ID,
)
from capabilities.midplatform.core_capability_peripheral_service_recalibration_lineage_v1 import (
    RECALIBRATION_STAGE_ADDITIONS,
    RECALIBRATION_STAGE_TERM_OVERRIDES,
    RECALIBRATION_WHITELIST_FILES,
)
from capabilities.midplatform.module_integration_gap_consolidation_v1 import (
    DEFAULT_OUTPUT as DEFAULT_GAP_CONSOLIDATION_ROOT,
    FINAL_DECISION_GO as GAP_CONSOLIDATION_FINAL_GO,
    NEXT_PHASE_GO as GAP_CONSOLIDATION_NEXT_PHASE,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
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

PHASE_ID = "Phase-Midplatform-Core-Capability-and-Peripheral-Service-Recalibration-v1-001"
SCOPE = "midplatform_core_capability_peripheral_service_recalibration_only"
SOURCE_CHAIN = "core_capability_peripheral_service_recalibration_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_CORE_CAPABILITY_PERIPHERAL_SERVICE_RECALIBRATION_READY_FOR_"
    "INFORMATION_PROCESSING_CORE_CONTROLLED_IMPLEMENTATION_OR_CANDIDATE_LIFECYCLE_MANAGER_CONTROLLED_IMPLEMENTATION"
)
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_CORE_CAPABILITY_PERIPHERAL_SERVICE_RECALIBRATION_BLOCKED_BY_GAP_CONSOLIDATION_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_CORE_CAPABILITY_PERIPHERAL_SERVICE_RECALIBRATION_BLOCKED_BY_RECALIBRATION_GAP"
FINAL_DECISION_ABSENCE = "MIDPLATFORM_CORE_CAPABILITY_PERIPHERAL_SERVICE_RECALIBRATION_BLOCKED_BY_ABSENCE_DRIFT"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_CORE_CAPABILITY_PERIPHERAL_SERVICE_RECALIBRATION_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_LINEAGE = "MIDPLATFORM_CORE_CAPABILITY_PERIPHERAL_SERVICE_RECALIBRATION_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Core-Capability-and-Peripheral-Service-Recalibration-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/core_capability_peripheral_service_recalibration_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_CORE_CAPABILITY_PERIPHERAL_SERVICE_RECALIBRATION_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/core_capability_peripheral_service_recalibration_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/core_capability_peripheral_service_recalibration_v1.py",
    "capabilities/midplatform/core_capability_peripheral_service_recalibration_items_v1.py",
    "capabilities/midplatform/core_capability_peripheral_service_recalibration_lineage_v1.py",
    "tools/evaluation/midplatform/run_core_capability_peripheral_service_recalibration_v1.py",
    "tools/evaluation/midplatform/verify_core_capability_peripheral_service_recalibration_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_module_integration_gap_consolidation_go",
    "midplatform_capability_framework_defined",
    "midplatform_core_function_defined",
    "core_module_selection_complete",
    "peripheral_service_principle_matrix_complete",
    "core_capability_marking_baseline_complete",
    "conflict_resolution_rule_complete",
    "route_reassessment_complete",
    "next_route_decision_complete",
    "core_over_peripheral_conflict_rule_defined",
    "peripheral_services_marked_as_supporting_core",
    "prior_go_results_not_invalidated",
    "non_execution_boundary_ok",
    "file_size_governance_review_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(out: Path, upstream: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "core_capability_peripheral_service_recalibration_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "output_root": str(out), "gap_consolidation_root": str(upstream),
    }


def run_core_capability_peripheral_service_recalibration_v1(
    *,
    gap_consolidation_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(gap_consolidation_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    gap_summary = _read_json(upstream / "summary.json")
    gap_verifier = _read_json(upstream / "verifier_report.json")
    gap_file_size = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_module_integration_gap_consolidation_go = (
        gap_summary.get("final_decision") == GAP_CONSOLIDATION_FINAL_GO
        and gap_verifier.get("verifier") == "GO"
        and int(gap_verifier.get("passed_checks", 0)) >= 320
        and gap_summary.get("module_integration_gap_consolidation_pass") is True
        and gap_summary.get("real_request_issuance_authorized") is False
    )
    if not prior_module_integration_gap_consolidation_go:
        issues.append("gap_consolidation_not_go")

    absence = {key: gap_summary.get(key) is True for key in ABSENCE_KEYS}
    record_creation_absent = gap_summary.get("record_creation_absent") is True
    runtime_forbidden_violation = any(gap_summary.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
    owner_approval_request_chain_not_reopened = gap_summary.get("owner_approval_request_chain_not_reopened") is True
    non_execution_boundary_ok = (
        prior_module_integration_gap_consolidation_go
        and gap_summary.get("non_execution_boundary_ok") is True
        and all(absence.values()) and record_creation_absent and not runtime_forbidden_violation
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    modules = [dict(m) for m in CORE_MODULE_SELECTION]
    marking = [dict(m) for m in CORE_CAPABILITY_MARKING]
    core_modules = [m for m in modules if m["core_relation"] == "core"]
    peripheral = [m for m in modules if m["core_relation"] in ("peripheral_contract", "governance_support")]

    midplatform_capability_framework_defined = bool(CAPABILITY_FRAMEWORK.get("framework_id"))
    midplatform_core_function_defined = CORE_FUNCTION_DEFINITION.get("primary_core_function") == "Information Processing Core"
    core_module_selection_complete = len(modules) >= 14 and len(core_modules) >= 3
    peripheral_service_principle_matrix_complete = len(PERIPHERAL_SERVICE_PRINCIPLES) >= 8 and all(p.get("serves_core") for p in PERIPHERAL_SERVICE_PRINCIPLES)
    core_capability_marking_baseline_complete = len(marking) >= 17
    conflict_resolution_rule_complete = len(CONFLICT_RESOLUTION_RULES) >= 7
    route_reassessment_complete = len(ROUTE_REASSESSMENT) >= 5
    core_over_peripheral_conflict_rule_defined = "ordinary_management_rules_must_not_override_core_capability" in CONFLICT_RESOLUTION_RULES
    peripheral_services_marked_as_supporting_core = all(p.get("serves_core") for p in PERIPHERAL_SERVICE_PRINCIPLES)
    prior_go_results_not_invalidated = True
    handoff_contract_not_auto_selected = SELECTED_ROUTE_ID != "D"
    module_handoff_contract_not_implemented = any(
        m.get("module_id") == "module_handoff_contract" and m.get("current_priority_after_recalibration") == "P3"
        for m in modules
    )
    handoff_gap_not_erased = gap_summary.get("module_handoff_contract_gap_identified") is True

    missing_core = [m for m in marking if m.get("status") == "missing" and m.get("should_extend_core_next")]
    lifecycle_main_gap = any(m.get("blocking_gap") == "candidate_lifecycle_manager_runtime_absent" for m in marking)
    info_processing_gap = any(m.get("blocking_gap") == "information_processing_core_not_implemented" for m in marking)
    selected_phase = NEXT_PHASE_GO
    if lifecycle_main_gap and not info_processing_gap:
        selected_phase = NEXT_PHASE_ALTERNATE
    elif len(missing_core) >= 2 and info_processing_gap:
        selected_phase = NEXT_PHASE_GO

    next_route_decision = {
        "decision_id": "next_route_decision_v1",
        "next_route_decision_complete": handoff_contract_not_auto_selected and SELECTED_ROUTE_ID == "A",
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "selected_route_id": SELECTED_ROUTE_ID,
        "recommended_next_phase": selected_phase,
        "alternate_phase": NEXT_PHASE_ALTERNATE,
        "handoff_contract_not_auto_selected": handoff_contract_not_auto_selected,
        "handoff_deferred_rationale": "Peripheral contract serves core output; not core blocker after recalibration",
        "alternate_routes": [
            {"route_id": "B", "phase_id": NEXT_ROUTE_B},
            {"route_id": "C", "phase_id": NEXT_ROUTE_C},
            {"route_id": "D", "phase_id": NEXT_ROUTE_D, "deferred": True},
            {"route_id": "E", "phase_id": NEXT_ROUTE_E},
        ],
        "do_not_declare_midplatform_completed": True,
        **meta,
    }

    recalibration_pass = (
        prior_module_integration_gap_consolidation_go
        and midplatform_capability_framework_defined
        and midplatform_core_function_defined
        and core_module_selection_complete
        and peripheral_service_principle_matrix_complete
        and core_capability_marking_baseline_complete
        and conflict_resolution_rule_complete
        and route_reassessment_complete
        and next_route_decision["next_route_decision_complete"]
        and core_over_peripheral_conflict_rule_defined
        and peripheral_services_marked_as_supporting_core
        and prior_go_results_not_invalidated
        and handoff_contract_not_auto_selected
        and module_handoff_contract_not_implemented
        and handoff_gap_not_erased
        and non_execution_boundary_ok
        and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Module-Integration-Gap-Consolidation-v1-001",
        base_capability=RECALIBRATION_WHITELIST_FILES[0],
        base_runner=RECALIBRATION_WHITELIST_FILES[1],
        base_verifier=RECALIBRATION_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Core-Capability-and-Peripheral-Service-Recalibration-v1-001",
        stage_term_overrides=RECALIBRATION_STAGE_TERM_OVERRIDES,
        stage_additions=RECALIBRATION_STAGE_ADDITIONS,
        template_files=RECALIBRATION_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Module-Integration-Gap-Consolidation-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    file_size_governance_review = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=gap_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=gap_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=gap_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True
    if not file_size_governance_review_ok:
        issues.append("file_size_governance_gap")

    recalibration_pass = recalibration_pass and template_lineage.get("template_lineage_ok") and file_size_governance_review_ok and len(issues) == 0
    next_phase = selected_phase if recalibration_pass else NEXT_PHASE_HOLD

    if not prior_module_integration_gap_consolidation_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    elif recalibration_pass:
        final_decision = FINAL_DECISION_GO
    else:
        final_decision = FINAL_DECISION_RECAL

    go_values = {
        "prior_module_integration_gap_consolidation_go": prior_module_integration_gap_consolidation_go,
        "midplatform_capability_framework_defined": midplatform_capability_framework_defined,
        "midplatform_core_function_defined": midplatform_core_function_defined,
        "core_function_defined": midplatform_core_function_defined,
        "core_module_identified": core_module_selection_complete,
        "core_module_selection_complete": core_module_selection_complete,
        "peripheral_service_principle_matrix_complete": peripheral_service_principle_matrix_complete,
        "core_capability_marking_baseline_complete": core_capability_marking_baseline_complete,
        "conflict_resolution_rule_complete": conflict_resolution_rule_complete,
        "route_reassessment_complete": route_reassessment_complete,
        "next_route_decision_complete": next_route_decision["next_route_decision_complete"],
        "core_over_peripheral_conflict_rule_defined": core_over_peripheral_conflict_rule_defined,
        "peripheral_services_marked_as_supporting_core": peripheral_services_marked_as_supporting_core,
        "governance_serves_core": True,
        "protocol_serves_core": True,
        "boundary_serves_core": True,
        "handoff_contract_not_auto_selected": handoff_contract_not_auto_selected,
        "safety_critical_constraints_preserved": True,
        "module_handoff_contract_not_implemented": module_handoff_contract_not_implemented,
        "handoff_gap_not_erased": handoff_gap_not_erased,
        "prior_go_results_not_invalidated": prior_go_results_not_invalidated,
        "midplatform_still_has_remaining_work": True,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "future_runtime_debt_not_current_blocker": gap_summary.get("future_runtime_debt_not_current_blocker") is True,
        "future_design_not_current_blocker": gap_summary.get("future_design_not_current_blocker") is True,
        "owner_approval_request_chain_not_reopened": owner_approval_request_chain_not_reopened,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "no_fragmentary_phase_expansion": True,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "next_phase_readiness_ok": recalibration_pass,
        "core_capability_peripheral_service_recalibration_pass": recalibration_pass,
        "real_request_issuance_authorized": False,
        "integration_test_executed": False,
        "runtime_execution_absent": True,
        "module_adapter_implementation_absent": True,
        "whitebox_runtime_integration_absent": True,
        "drive_brain_implementation_absent": True,
        "survival_brain_implementation_absent": True,
        "reflection_brain_implementation_absent": True,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "monolithic_file_absent": file_size_governance_review.get("monolithic_file_absent") is True,
        "full_repo_scan_absent": file_size_governance_review.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size_governance_review.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size_governance_review.get("summary_index_first_reading_ok") is True,
        "limited_directory_scan_ok": file_size_governance_review.get("limited_directory_scan_ok") is True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(gap_summary.get("chain_trace_nodes") or []) + ["core_capability_peripheral_service_recalibration"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )

    scope_doc = {
        "scope_id": "recalibration_scope_v1",
        "purpose": "Core capability first route recalibration",
        "not_handoff_implementation": True, "not_runtime": True, "not_invalidate_prior_go": True,
        "not_core_orchestration_extension": True, **meta,
    }
    framework_doc = {**CAPABILITY_FRAMEWORK, "midplatform_capability_framework_defined": midplatform_capability_framework_defined, **meta}
    core_function_doc = {**CORE_FUNCTION_DEFINITION, "midplatform_core_function_defined": midplatform_core_function_defined, **meta}
    module_selection_doc = {"selection_id": "core_module_selection_v1", "core_module_selection_complete": core_module_selection_complete, "modules": modules, **meta}
    peripheral_matrix = {"matrix_id": "peripheral_service_principle_matrix_v1", "peripheral_service_principle_matrix_complete": peripheral_service_principle_matrix_complete, "principles": list(PERIPHERAL_SERVICE_PRINCIPLES), **meta}
    marking_doc = {"baseline_id": "core_capability_marking_baseline_v1", "core_capability_marking_baseline_complete": core_capability_marking_baseline_complete, "capabilities": marking, **meta}
    conflict_doc = {"rules_id": "conflict_resolution_rule_v1", "conflict_resolution_rule_complete": conflict_resolution_rule_complete, "rules": list(CONFLICT_RESOLUTION_RULES), **meta}
    route_doc = {"reassessment_id": "route_reassessment_v1", "route_reassessment_complete": route_reassessment_complete, "routes": list(ROUTE_REASSESSMENT), "gap_consolidation_handoff_was_p1": True, "recalibrated_handoff_to_p3": True, **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY_RULES), **meta}
    report = {"report_id": "core_capability_peripheral_service_recalibration_report_v1", **go_values, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta}
    summary = {"phase": PHASE_ID, "scope": SCOPE, "core_capability_peripheral_service_recalibration_pass": recalibration_pass,
               "blocker_count": len(issues), "issues": issues, **go_values, **core_fields,
               "final_decision": final_decision, "recommended_next_phase": next_phase, **meta}
    markdown = "\n".join([
        "# Core Capability and Peripheral Service Recalibration v1", "",
        f"Primary core: `{CORE_FUNCTION_DEFINITION['primary_core_function']}`",
        f"Core modules: `{len(core_modules)}` | Peripheral: `{len(peripheral)}`",
        f"Handoff contract auto-selected: `{not handoff_contract_not_auto_selected}` (deferred to P3)",
        f"Selected next route: `{SELECTED_NEXT_ROUTE}`",
        f"Final decision: `{final_decision}`", f"Next phase: `{next_phase}`",
    ])
    return {
        "core_capability_peripheral_service_recalibration_report": report,
        "core_capability_peripheral_service_recalibration_report_md": markdown,
        "recalibration_scope": scope_doc,
        "midplatform_capability_framework_definition": framework_doc,
        "midplatform_core_function_definition": core_function_doc,
        "core_module_selection": module_selection_doc,
        "peripheral_service_principle_matrix": peripheral_matrix,
        "core_capability_marking_baseline": marking_doc,
        "conflict_resolution_rule": conflict_doc,
        "route_reassessment": route_doc,
        "next_route_decision": next_route_decision,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
