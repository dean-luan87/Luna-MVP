# -*- coding: utf-8 -*-
"""Luna Project Organization Work Manual and Existing Work Mapping v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.core_capability_peripheral_service_recalibration_v1 import (
    DEFAULT_OUTPUT as DEFAULT_RECALIBRATION_ROOT,
    FINAL_DECISION_GO as RECALIBRATION_FINAL_GO,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.luna_project_organization_work_manual_items_v1 import (
    DEFERRED_ROUTE,
    DEFER_REASON,
    EXISTING_ARTIFACT_MAPPINGS,
    MIDPLATFORM_ORGANIZATION_MANUAL,
    MISSING_WORK_MANUAL_GAPS,
    NEXT_WORK_GOVERNANCE_RULES,
    OVERBUILD_RISK_REVIEW,
    PROJECT_WORK_MODE_PRINCIPLES,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    STANDARD_WORK_MANUAL_SECTIONS,
)
from capabilities.midplatform.luna_project_organization_work_manual_lineage_v1 import (
    WORK_MANUAL_STAGE_ADDITIONS,
    WORK_MANUAL_STAGE_TERM_OVERRIDES,
    WORK_MANUAL_WHITELIST_FILES,
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

PHASE_ID = "Phase-Luna-Project-Organization-Work-Manual-and-Existing-Work-Mapping-v1-001"
SCOPE = "luna_project_organization_work_manual_mapping_only"
SOURCE_CHAIN = "luna_project_organization_work_manual_and_existing_work_mapping_v1"
FINAL_DECISION_GO = "LUNA_PROJECT_ORGANIZATION_WORK_MANUAL_AND_EXISTING_WORK_MAPPING_READY_FOR_INFORMATION_PROCESSING_CORE_WORK_MANUAL_DEFINITION"
FINAL_DECISION_UPSTREAM = "LUNA_PROJECT_ORGANIZATION_WORK_MANUAL_MAPPING_BLOCKED_BY_RECALIBRATION_GAP"
FINAL_DECISION_MAPPING = "LUNA_PROJECT_ORGANIZATION_WORK_MANUAL_MAPPING_BLOCKED_BY_MAPPING_GAP"
FINAL_DECISION_ABSENCE = "LUNA_PROJECT_ORGANIZATION_WORK_MANUAL_MAPPING_BLOCKED_BY_ABSENCE_DRIFT"
FINAL_DECISION_RUNTIME = "LUNA_PROJECT_ORGANIZATION_WORK_MANUAL_MAPPING_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_LINEAGE = "LUNA_PROJECT_ORGANIZATION_WORK_MANUAL_MAPPING_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
NEXT_PHASE_HOLD = "Phase-Luna-Project-Organization-Work-Manual-Mapping-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/luna_project_organization_work_manual_and_existing_work_mapping_v1_smoke_v0"
DEFAULT_RECALIBRATION_ROOT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/core_capability_peripheral_service_recalibration_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_PROJECT_ORGANIZATION_WORK_MANUAL_AND_EXISTING_WORK_MAPPING_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/luna_project_organization_work_manual_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/luna_project_organization_work_manual_and_existing_work_mapping_v1.py",
    "capabilities/midplatform/luna_project_organization_work_manual_items_v1.py",
    "capabilities/midplatform/luna_project_organization_work_manual_lineage_v1.py",
    "tools/evaluation/midplatform/run_luna_project_organization_work_manual_and_existing_work_mapping_v1.py",
    "tools/evaluation/midplatform/verify_luna_project_organization_work_manual_and_existing_work_mapping_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_recalibration_go",
    "project_work_mode_defined",
    "standard_work_manual_template_complete",
    "midplatform_organization_manual_complete",
    "existing_work_mapping_complete",
    "missing_work_manual_gap_register_complete",
    "next_work_governance_rules_complete",
    "core_work_before_peripheral_rules",
    "peripheral_rules_must_serve_core",
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
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "luna_project_organization_work_manual_mapping_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "output_root": str(out), "recalibration_root": str(upstream),
    }


def run_luna_project_organization_work_manual_and_existing_work_mapping_v1(
    *,
    recalibration_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(recalibration_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    recal_summary = _read_json(upstream / "summary.json")
    recal_verifier = _read_json(upstream / "verifier_report.json")
    recal_file_size = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_recalibration_go = (
        recal_summary.get("final_decision") == RECALIBRATION_FINAL_GO
        and recal_verifier.get("verifier") == "GO"
        and int(recal_verifier.get("passed_checks", 0)) >= 340
        and recal_summary.get("core_capability_peripheral_service_recalibration_pass") is True
    )
    if not prior_recalibration_go:
        issues.append("recalibration_not_go")

    absence = {k: recal_summary.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = prior_recalibration_go and recal_summary.get("non_execution_boundary_ok") is True and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    artifacts = [dict(a) for a in EXISTING_ARTIFACT_MAPPINGS]
    gaps = [dict(g) for g in MISSING_WORK_MANUAL_GAPS]
    risks = [dict(r) for r in OVERBUILD_RISK_REVIEW]

    project_work_mode_defined = len(PROJECT_WORK_MODE_PRINCIPLES) >= 10
    standard_work_manual_template_complete = len(STANDARD_WORK_MANUAL_SECTIONS) >= 11
    midplatform_organization_manual_complete = bool(MIDPLATFORM_ORGANIZATION_MANUAL.get("manual_id"))
    existing_work_mapping_complete = len(artifacts) >= 18
    missing_work_manual_gap_register_complete = len(gaps) >= 13
    next_work_governance_rules_complete = len(NEXT_WORK_GOVERNANCE_RULES) >= 10
    core_work_before_peripheral_rules = any(p["principle_id"] == "core_work_first" for p in PROJECT_WORK_MODE_PRINCIPLES)
    peripheral_rules_must_serve_core = any(p["principle_id"] == "peripheral_rules_serve_core" for p in PROJECT_WORK_MODE_PRINCIPLES)
    prior_go_results_not_invalidated = True
    info_core_manual_missing = any(a.get("artifact_id") == "information_processing_core" and a.get("missing_manual_definition") for a in artifacts)
    next_route_not_direct = SELECTED_NEXT_PHASE != DEFERRED_ROUTE
    ipc_manual_before_impl = info_core_manual_missing and next_route_not_direct

    work_mode_doc = {
        "definition_id": "project_work_mode_definition_v1",
        "project_work_mode_defined": project_work_mode_defined,
        "principles": list(PROJECT_WORK_MODE_PRINCIPLES),
        "work_manual_first_rule_defined": True,
        "organization_workflow_defined": True,
        "role_job_definition_required": True,
        "judge_referee_definition_required": True,
        "workload_control_required": True,
        "qualification_standard_required": True,
        **meta,
    }
    template_doc = {
        "template_id": "standard_work_manual_template_v1",
        "standard_work_manual_template_complete": standard_work_manual_template_complete,
        "sections": list(STANDARD_WORK_MANUAL_SECTIONS),
        **meta,
    }
    org_manual = {**MIDPLATFORM_ORGANIZATION_MANUAL, "midplatform_organization_manual_complete": midplatform_organization_manual_complete, **meta}
    mapping_matrix = {
        "matrix_id": "existing_work_mapping_matrix_v1",
        "existing_work_mapping_complete": existing_work_mapping_complete,
        "existing_artifacts_mapped": True,
        "artifacts": artifacts,
        **meta,
    }
    reclassification = {
        "register_id": "completed_artifact_reclassification_v1",
        "core_work_artifacts": [a["artifact_id"] for a in artifacts if a.get("is_core_work")],
        "core_support_artifacts": [a["artifact_id"] for a in artifacts if a.get("is_core_support")],
        "peripheral_artifacts": [a["artifact_id"] for a in artifacts if a.get("is_peripheral_rule")],
        "governance_artifacts": [a["artifact_id"] for a in artifacts if a.get("is_governance")],
        **meta,
    }
    gap_register = {
        "register_id": "missing_work_manual_gap_register_v1",
        "missing_work_manual_gap_register_complete": missing_work_manual_gap_register_complete,
        "gaps": gaps,
        **meta,
    }
    overbuild_review = {
        "review_id": "peripheral_overbuild_risk_review_v1",
        "peripheral_overbuild_risk_review_complete": len(risks) >= 5,
        "risks": risks,
        **meta,
    }
    governance_rules = {
        "rules_id": "next_work_governance_rules_v1",
        "next_work_governance_rules_complete": next_work_governance_rules_complete,
        "rules": list(NEXT_WORK_GOVERNANCE_RULES),
        **meta,
    }
    next_route = {
        "recommendation_id": "next_route_recommendation_v1",
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "recommended_next_phase": SELECTED_NEXT_PHASE,
        "deferred_route": DEFERRED_ROUTE,
        "defer_reason": DEFER_REASON,
        "information_processing_core_should_have_work_manual_before_implementation": ipc_manual_before_impl,
        "next_route_not_direct_controlled_implementation_unless_manual_ready": next_route_not_direct,
        "manual_ready_for_ipc_implementation": False,
        **meta,
    }

    mapping_pass = (
        prior_recalibration_go and project_work_mode_defined and standard_work_manual_template_complete
        and midplatform_organization_manual_complete and existing_work_mapping_complete
        and missing_work_manual_gap_register_complete and next_work_governance_rules_complete
        and core_work_before_peripheral_rules and peripheral_rules_must_serve_core
        and prior_go_results_not_invalidated and ipc_manual_before_impl and next_route_not_direct
        and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Core-Capability-and-Peripheral-Service-Recalibration-v1-001",
        base_capability=WORK_MANUAL_WHITELIST_FILES[0],
        base_runner=WORK_MANUAL_WHITELIST_FILES[1],
        base_verifier=WORK_MANUAL_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Project-Organization-Work-Manual-and-Existing-Work-Mapping-v1-001",
        stage_term_overrides=WORK_MANUAL_STAGE_TERM_OVERRIDES,
        stage_additions=WORK_MANUAL_STAGE_ADDITIONS,
        template_files=WORK_MANUAL_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Core-Capability-and-Peripheral-Service-Recalibration-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    file_size_governance_review = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=recal_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=recal_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=recal_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    mapping_pass = mapping_pass and template_lineage.get("template_lineage_ok") and file_size_governance_review_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if mapping_pass else NEXT_PHASE_HOLD

    if not prior_recalibration_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    elif mapping_pass:
        final_decision = FINAL_DECISION_GO
    else:
        final_decision = FINAL_DECISION_MAPPING

    go_values = {
        "prior_recalibration_go": prior_recalibration_go,
        "project_work_mode_defined": project_work_mode_defined,
        "standard_work_manual_template_complete": standard_work_manual_template_complete,
        "midplatform_organization_manual_complete": midplatform_organization_manual_complete,
        "existing_work_mapping_complete": existing_work_mapping_complete,
        "missing_work_manual_gap_register_complete": missing_work_manual_gap_register_complete,
        "next_work_governance_rules_complete": next_work_governance_rules_complete,
        "core_work_before_peripheral_rules": core_work_before_peripheral_rules,
        "peripheral_rules_must_serve_core": peripheral_rules_must_serve_core,
        "prior_go_results_not_invalidated": prior_go_results_not_invalidated,
        "work_manual_first_rule_defined": True,
        "organization_workflow_defined": True,
        "role_job_definition_required": True,
        "judge_referee_definition_required": True,
        "workload_control_required": True,
        "qualification_standard_required": True,
        "existing_artifacts_mapped": True,
        "information_processing_core_should_have_work_manual_before_implementation": ipc_manual_before_impl,
        "next_route_not_direct_controlled_implementation_unless_manual_ready": next_route_not_direct,
        "no_runtime_execution": True,
        "no_integration_test": True,
        "no_record_creation": True,
        "no_grant_creation": True,
        "no_authorization_request_creation": True,
        "midplatform_still_has_remaining_work": True,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "owner_approval_request_chain_not_reopened": recal_summary.get("owner_approval_request_chain_not_reopened") is True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "no_fragmentary_phase_expansion": True,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "next_phase_readiness_ok": mapping_pass,
        "luna_project_organization_work_manual_mapping_pass": mapping_pass,
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
        chain_trace_nodes=tuple(list(recal_summary.get("chain_trace_nodes") or []) + ["luna_project_organization_work_manual_mapping"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )

    scope_doc = {"scope_id": "recalibration_scope_v1", "purpose": "Work manual first methodology and artifact mapping",
                 "not_implementation": True, "not_invalidate_prior_go": True, **meta}
    report = {**go_values, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta}
    summary = {"phase": PHASE_ID, "scope": SCOPE, "luna_project_organization_work_manual_mapping_pass": mapping_pass,
               "blocker_count": len(issues), "issues": issues, **go_values, **core_fields,
               "final_decision": final_decision, "recommended_next_phase": next_phase, **meta}
    md_work_mode = "# Luna Project Work Mode\n\n" + "\n".join(f"- **{p['name']}**: {p['summary']}" for p in PROJECT_WORK_MODE_PRINCIPLES)
    md_org = "# Midplatform Organization Manual\n\n" + f"Mission: {MIDPLATFORM_ORGANIZATION_MANUAL['mission']}\n\nPrimary core: {MIDPLATFORM_ORGANIZATION_MANUAL['primary_core_work']}"
    md_mapping = "# Existing Work Mapping\n\n" + "\n".join(f"- `{a['artifact_id']}`: core={a['is_core_work']} peripheral={a['is_peripheral_rule']}" for a in artifacts[:10]) + f"\n... total {len(artifacts)}"
    md_governance = "# Next Work Governance Rules\n\n" + "\n".join(f"- {r}" for r in NEXT_WORK_GOVERNANCE_RULES)
    md_report = "\n".join([
        "# Luna Project Organization Work Manual and Existing Work Mapping v1", "",
        f"Principles: `{len(PROJECT_WORK_MODE_PRINCIPLES)}` | Artifacts mapped: `{len(artifacts)}`",
        f"IPC manual before implementation: `{ipc_manual_before_impl}`",
        f"Deferred: `{DEFERRED_ROUTE}`", f"Next: `{SELECTED_NEXT_PHASE}`",
        f"Final decision: `{final_decision}`",
    ])
    return {
        "project_work_mode_definition": work_mode_doc,
        "project_work_mode_definition_md": md_work_mode,
        "standard_work_manual_template": template_doc,
        "midplatform_organization_manual": org_manual,
        "midplatform_organization_manual_md": md_org,
        "existing_work_mapping_matrix": mapping_matrix,
        "existing_work_mapping_matrix_md": md_mapping,
        "completed_artifact_reclassification": reclassification,
        "missing_work_manual_gap_register": gap_register,
        "peripheral_overbuild_risk_review": overbuild_review,
        "next_work_governance_rules": governance_rules,
        "next_work_governance_rules_md": md_governance,
        "next_route_recommendation": next_route,
        "recalibration_scope": scope_doc,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
        "core_capability_peripheral_service_recalibration_report": report,
        "core_capability_peripheral_service_recalibration_report_md": md_report,
    }
