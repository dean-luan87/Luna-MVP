# -*- coding: utf-8 -*-
"""Information Processing Core Work Manual Definition v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.information_processing_core_work_manual_items_v1 import (
    CORE_WORK_DEFINITION,
    EXTERNAL_WORKFLOW,
    FUTURE_EXPANSION,
    GOVERNANCE_SERVICE_RULES,
    INFORMATION_TYPES,
    INTERNAL_WORKFLOW_STEPS,
    JUDGE_REFEREE_RULES,
    ORGANIZATION_CONTEXT,
    QUALIFICATION_STANDARD,
    ROLE_JOB_DEFINITION,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    WORK_DETAIL_ITEMS,
    WORKLOAD_CONTROL,
)
from capabilities.midplatform.information_processing_core_work_manual_lineage_v1 import (
    IPC_WORK_MANUAL_STAGE_ADDITIONS,
    IPC_WORK_MANUAL_STAGE_TERM_OVERRIDES,
    IPC_WORK_MANUAL_WHITELIST_FILES,
)
from capabilities.midplatform.luna_project_organization_work_manual_and_existing_work_mapping_v1 import (
    DEFAULT_OUTPUT as DEFAULT_WORK_MANUAL_MAPPING_ROOT,
    FINAL_DECISION_GO as WORK_MANUAL_MAPPING_FINAL_GO,
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

PHASE_ID = "Phase-Midplatform-Information-Processing-Core-Work-Manual-Definition-v1-001"
SCOPE = "information_processing_core_work_manual_definition_only"
SOURCE_CHAIN = "information_processing_core_work_manual_definition_v1"
FINAL_DECISION_GO = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_WORK_MANUAL_READY_FOR_CONTROLLED_IMPLEMENTATION"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_WORK_MANUAL_BLOCKED_BY_WORK_MANUAL_MAPPING_GAP"
FINAL_DECISION_MANUAL = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_WORK_MANUAL_BLOCKED_BY_MANUAL_GAP"
FINAL_DECISION_ABSENCE = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_WORK_MANUAL_BLOCKED_BY_ABSENCE_DRIFT"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_WORK_MANUAL_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_LINEAGE = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_WORK_MANUAL_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Information-Processing-Core-Work-Manual-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/information_processing_core_work_manual_definition_v1_smoke_v0"
DEFAULT_WORK_MANUAL_MAPPING_ROOT = DEFAULT_WORK_MANUAL_MAPPING_ROOT
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_INFORMATION_PROCESSING_CORE_WORK_MANUAL_DEFINITION_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/information_processing_core_work_manual_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/information_processing_core_work_manual_definition_v1.py",
    "capabilities/midplatform/information_processing_core_work_manual_items_v1.py",
    "capabilities/midplatform/information_processing_core_work_manual_lineage_v1.py",
    "tools/evaluation/midplatform/run_information_processing_core_work_manual_definition_v1.py",
    "tools/evaluation/midplatform/verify_information_processing_core_work_manual_definition_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_project_work_manual_go",
    "information_processing_core_work_manual_complete",
    "organization_context_complete",
    "core_work_definition_complete",
    "role_job_definition_complete",
    "internal_external_workflow_complete",
    "judge_referee_rules_complete",
    "workload_control_complete",
    "qualification_standard_complete",
    "future_expansion_complete",
    "implementation_readiness_ok",
    "peripheral_rules_serve_core",
    "prior_go_results_not_invalidated",
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
        "information_processing_core_work_manual_definition_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "output_root": str(out),
        "work_manual_mapping_root": str(upstream),
    }


def run_information_processing_core_work_manual_definition_v1(
    *,
    work_manual_mapping_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(work_manual_mapping_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    wm_summary = _read_json(upstream / "summary.json")
    wm_verifier = _read_json(upstream / "verifier_report.json")
    wm_file_size = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_project_work_manual_go = (
        wm_summary.get("final_decision") == WORK_MANUAL_MAPPING_FINAL_GO
        and wm_verifier.get("verifier") == "GO"
        and int(wm_verifier.get("passed_checks", 0)) >= 340
        and wm_summary.get("luna_project_organization_work_manual_mapping_pass") is True
    )
    if not prior_project_work_manual_go:
        issues.append("work_manual_mapping_not_go")

    absence = {k: wm_summary.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = (
        prior_project_work_manual_go
        and wm_summary.get("non_execution_boundary_ok") is True
        and all(absence.values())
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    organization_context_complete = bool(ORGANIZATION_CONTEXT.get("context_id"))
    core_work_definition_complete = len(CORE_WORK_DEFINITION.get("core_work_items") or ()) >= 10
    role_job_definition_complete = bool(ROLE_JOB_DEFINITION.get("job_title"))
    work_detail_complete = len(WORK_DETAIL_ITEMS) >= 11
    internal_workflow_complete = len(INTERNAL_WORKFLOW_STEPS) >= 12
    external_workflow_complete = bool(EXTERNAL_WORKFLOW.get("workflow_id"))
    judge_referee_rules_complete = bool(JUDGE_REFEREE_RULES.get("rules_id"))
    workload_control_complete = bool(WORKLOAD_CONTROL.get("control_id"))
    qualification_standard_complete = len(QUALIFICATION_STANDARD.get("minimum_capability_tags") or ()) >= 12
    future_expansion_complete = len(FUTURE_EXPANSION.get("reserved") or ()) >= 10
    peripheral_rules_serve_core = GOVERNANCE_SERVICE_RULES.get("peripheral_contract_does_not_constrain_core") is True
    information_type_registry_defined = len(INFORMATION_TYPES) >= 11
    prior_go_results_not_invalidated = True

    org_ctx = {**ORGANIZATION_CONTEXT, "organization_context_complete": organization_context_complete, **meta}
    core_work = {**CORE_WORK_DEFINITION, "core_work_definition_complete": core_work_definition_complete, **meta}
    role_job = {
        **ROLE_JOB_DEFINITION,
        "role_job_definition_complete": role_job_definition_complete,
        "information_processing_core_identified_as_primary_core": True,
        **meta,
    }
    work_detail = {
        "detail_id": "work_detail_v1",
        "work_detail_complete": work_detail_complete,
        "information_types": list(INFORMATION_TYPES),
        "information_type_registry_defined": information_type_registry_defined,
        "items": list(WORK_DETAIL_ITEMS),
        **meta,
    }
    internal_wf = {
        "workflow_id": "internal_workflow_v1",
        "internal_workflow_complete": internal_workflow_complete,
        "workflow_before_protocol": True,
        "steps": list(INTERNAL_WORKFLOW_STEPS),
        **meta,
    }
    external_wf = {
        **EXTERNAL_WORKFLOW,
        "external_workflow_complete": external_workflow_complete,
        **meta,
    }
    judge_rules = {**JUDGE_REFEREE_RULES, "judge_referee_rules_complete": judge_referee_rules_complete, **meta}
    gov_rules = {**GOVERNANCE_SERVICE_RULES, "peripheral_rules_serve_core": peripheral_rules_serve_core, **meta}
    workload = {**WORKLOAD_CONTROL, "workload_control_complete": workload_control_complete, **meta}
    qualification = {**QUALIFICATION_STANDARD, "qualification_standard_complete": qualification_standard_complete, **meta}
    future_exp = {**FUTURE_EXPANSION, "future_expansion_complete": future_expansion_complete, **meta}

    internal_external_workflow_complete = internal_workflow_complete and external_workflow_complete
    information_processing_core_work_manual_complete = (
        organization_context_complete
        and core_work_definition_complete
        and role_job_definition_complete
        and work_detail_complete
        and internal_external_workflow_complete
        and judge_referee_rules_complete
        and workload_control_complete
        and qualification_standard_complete
        and future_expansion_complete
    )

    implementation_readiness = {
        "review_id": "implementation_readiness_review_v1",
        "implementation_readiness_ok": information_processing_core_work_manual_complete and prior_project_work_manual_go,
        "no_controlled_implementation_created": True,
        "no_runtime_execution": True,
        "no_integration_test": True,
        "no_record_creation": True,
        "no_grant_creation": True,
        "no_authorization_request_creation": True,
        "manual_ready_for_controlled_implementation": information_processing_core_work_manual_complete,
        "module_handoff_contract_not_required": True,
        "integration_contract_not_required": True,
        **meta,
    }
    next_route = {
        "decision_id": "next_route_decision_v1",
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "recommended_next_phase": SELECTED_NEXT_PHASE,
        "next_phase_readiness_ok": information_processing_core_work_manual_complete and prior_project_work_manual_go,
        **meta,
    }

    manual_pass = (
        prior_project_work_manual_go
        and information_processing_core_work_manual_complete
        and peripheral_rules_serve_core
        and non_execution_boundary_ok
        and information_type_registry_defined
        and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Luna-Project-Organization-Work-Manual-and-Existing-Work-Mapping-v1-001",
        base_capability=IPC_WORK_MANUAL_WHITELIST_FILES[0],
        base_runner=IPC_WORK_MANUAL_WHITELIST_FILES[1],
        base_verifier=IPC_WORK_MANUAL_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Information-Processing-Core-Work-Manual-Definition-v1-001",
        stage_term_overrides=IPC_WORK_MANUAL_STAGE_TERM_OVERRIDES,
        stage_additions=IPC_WORK_MANUAL_STAGE_ADDITIONS,
        template_files=IPC_WORK_MANUAL_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Luna-Project-Organization-Work-Manual-and-Existing-Work-Mapping-v1-001",
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

    manual_pass = manual_pass and template_lineage.get("template_lineage_ok") and file_size_governance_review_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if manual_pass else NEXT_PHASE_HOLD

    if not prior_project_work_manual_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    elif manual_pass:
        final_decision = FINAL_DECISION_GO
    else:
        final_decision = FINAL_DECISION_MANUAL

    go_values = {
        "prior_project_work_manual_go": prior_project_work_manual_go,
        "information_processing_core_work_manual_complete": information_processing_core_work_manual_complete,
        "organization_context_complete": organization_context_complete,
        "core_work_definition_complete": core_work_definition_complete,
        "role_job_definition_complete": role_job_definition_complete,
        "internal_external_workflow_complete": internal_external_workflow_complete,
        "judge_referee_rules_complete": judge_referee_rules_complete,
        "workload_control_complete": workload_control_complete,
        "qualification_standard_complete": qualification_standard_complete,
        "future_expansion_complete": future_expansion_complete,
        "implementation_readiness_ok": implementation_readiness.get("implementation_readiness_ok") is True,
        "peripheral_rules_serve_core": peripheral_rules_serve_core,
        "prior_go_results_not_invalidated": prior_go_results_not_invalidated,
        "information_processing_core_identified_as_primary_core": True,
        "workflow_before_protocol": True,
        "judge_referee_definition_complete": judge_referee_rules_complete,
        "workload_control_defined": workload_control_complete,
        "qualification_standard_defined": qualification_standard_complete,
        "module_handoff_contract_not_required_for_information_classification": True,
        "integration_contract_not_required_for_information_classification": True,
        "information_type_registry_defined": information_type_registry_defined,
        "unknown_information_allowed": True,
        "non_execution_boundary_preserved": non_execution_boundary_ok,
        "no_controlled_implementation_created": True,
        "no_runtime_execution": True,
        "no_integration_test": True,
        "no_record_creation": True,
        "no_grant_creation": True,
        "no_authorization_request_creation": True,
        "no_runtime_route": True,
        "no_candidate_promotion": True,
        "no_adapter_whitebox": True,
        "midplatform_still_has_remaining_work": True,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "owner_approval_request_chain_not_reopened": wm_summary.get("owner_approval_request_chain_not_reopened") is True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "no_fragmentary_phase_expansion": True,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "next_phase_readiness_ok": manual_pass,
        "information_processing_core_work_manual_definition_pass": manual_pass,
        "real_request_issuance_authorized": False,
        "integration_test_executed": False,
        "runtime_execution_absent": True,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "monolithic_file_absent": file_size_governance_review.get("monolithic_file_absent") is True,
        "full_repo_scan_absent": file_size_governance_review.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size_governance_review.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size_governance_review.get("summary_index_first_reading_ok") is True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(wm_summary.get("chain_trace_nodes") or []) + ["information_processing_core_work_manual_definition"]),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "information_processing_core_work_manual_definition_pass": manual_pass,
        "blocker_count": len(issues),
        "issues": issues,
        **go_values,
        **core_fields,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    md_report = "\n".join([
        "# Information Processing Core Work Manual Definition v1",
        "",
        f"Organization: `{ORGANIZATION_CONTEXT['organization']}`",
        f"Primary core: `{CORE_WORK_DEFINITION['primary_core_function']}`",
        f"Job title: `{ROLE_JOB_DEFINITION['job_title']}`",
        f"Information types: `{len(INFORMATION_TYPES)}`",
        f"Internal workflow steps: `{len(INTERNAL_WORKFLOW_STEPS)}`",
        f"Minimum capability tags: `{len(QUALIFICATION_STANDARD['minimum_capability_tags'])}`",
        f"Next: `{SELECTED_NEXT_PHASE}`",
        f"Final decision: `{final_decision}`",
    ])
    md_org = "# Organization Context\n\n" + f"Organization: {ORGANIZATION_CONTEXT['organization']}\nStage: {ORGANIZATION_CONTEXT['stage_positioning']}"
    md_role = "# Role / Job Definition\n\n" + f"Mission: {ROLE_JOB_DEFINITION['job_mission']}\nMetaphors: {', '.join(ROLE_JOB_DEFINITION['job_metaphors'])}"
    md_work = "# Work Detail\n\n" + "\n".join(f"- `{t}`" for t in INFORMATION_TYPES)
    md_internal = "# Internal Workflow\n\n" + "\n".join(f"- {s['step_id']}: {s['input']} -> {s['output']}" for s in INTERNAL_WORKFLOW_STEPS)
    md_external = "# External Workflow\n\n" + f"To lifecycle: {EXTERNAL_WORKFLOW['to_lifecycle_manager_when']}\nTo orchestration: {EXTERNAL_WORKFLOW['to_core_orchestration_when']}"
    report = {**go_values, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta}

    return {
        "organization_context": org_ctx,
        "organization_context_md": md_org,
        "core_work_definition": core_work,
        "role_job_definition": role_job,
        "role_job_definition_md": md_role,
        "work_detail": work_detail,
        "work_detail_md": md_work,
        "internal_workflow": internal_wf,
        "internal_workflow_md": md_internal,
        "external_workflow": external_wf,
        "external_workflow_md": md_external,
        "judge_referee_rules": judge_rules,
        "governance_protocol_boundary_service_rules": gov_rules,
        "workload_control": workload,
        "qualification_standard": qualification,
        "future_expansion": future_exp,
        "implementation_readiness_review": implementation_readiness,
        "next_route_decision": next_route,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
        "information_processing_core_work_manual_report": report,
        "information_processing_core_work_manual_report_md": md_report,
    }
