# -*- coding: utf-8 -*-
"""Luna Midplatform Owner Approval Request Module-Level Functional Slice Planning v1.

Result-first functional slice planning only. No slice test execution, no real issuance.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_DOC,
    FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_REF,
    MODULE_FIRST_CADENCE_RULE_DOC,
    MODULE_FIRST_DEVELOPMENT_VERIFICATION_CADENCE_RULE_REF,
    REUSE_FIRST_PROTOCOL_ENGINEERING_RULE_REF,
    RESULT_FIRST_MODULE_ENGINEERING_RULE_DOC,
    RESULT_FIRST_MODULE_ENGINEERING_RULE_REF,
    TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_DOC,
    TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_REF,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.owner_approval_request_governance_gate_template_lineage_v1 import (
    OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_STAGE_ADDITIONS,
    OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_STAGE_TERM_OVERRIDES,
    OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_WHITELIST_FILES,
)
from capabilities.midplatform.protocols.protocol_separation_rule_v1 import (
    VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
)
from capabilities.midplatform.protocols.result_first_module_engineering_rule_v1 import (
    build_result_first_module_engineering_rule_document,
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
from capabilities.midplatform.task_manager_owner_approval_request_authorization_preparation_dryrun_v1 import (
    DEFAULT_OUTPUT as DEFAULT_AUTHORIZATION_PREPARATION_DRYRUN_ROOT,
    FINAL_DECISION_GO as AUTHORIZATION_PREPARATION_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as AUTHORIZATION_PREPARATION_DRYRUN_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_owner_approval_request_governance_gate_integrated_implementation_v1 import (
    FINAL_DECISION_GO as INTEGRATED_IMPLEMENTATION_FINAL_GO,
    FUNCTIONAL_SLICE_CHAINS,
    SELECTED_ROUTE,
)

PHASE_ID = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Level-Functional-Slice-Planning-v1-001"
)
SCOPE = "midplatform_task_manager_owner_approval_request_module_level_functional_slice_planning_only"
SOURCE_CHAIN = "midplatform_task_manager_owner_approval_request_module_level_functional_slice_planning_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_READY_FOR_FUNCTIONAL_SLICE_DRYRUN_OR_MODULE_GOVERNANCE_CLOSURE"
)
FINAL_DECISION_UPSTREAM = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_BLOCKED_BY_AUTHORIZATION_PREPARATION_DRYRUN_GAP"
)
FINAL_DECISION_SLICE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_BLOCKED_BY_SLICE_PLAN_GAP"
)
FINAL_DECISION_ABSENCE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_BLOCKED_BY_ABSENCE_DRIFT"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
NEXT_PHASE_A = "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Functional-Slice-DryRun-v1-001"
NEXT_PHASE_B = "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Governance-Closure-v1-001"
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Level-Functional-Slice-Planning-Issue-Review-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_module_level_functional_slice_planning_v1_smoke_v0"
)
PLANNING_GO_NO_GO_PACK = (
    "docs/architecture/evaluation/"
    "LUNA_EVALUATION_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_V1_GO_NO_GO_PACK_V0.md"
)
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_module_level_functional_slice_planning_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_module_level_functional_slice_planning_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_module_level_functional_slice_planning_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/owner_approval_request_governance_gate_template_lineage_v1.py"

PLANNING_ARTIFACTS: Tuple[str, ...] = (
    "module_level_functional_slice_plan_v1.json",
    "module_level_functional_slice_plan_v1.md",
    "functional_slice_registry_v1.json",
    "owner_approval_request_candidate_lifecycle_slice_v1.json",
    "authorization_preparation_lifecycle_slice_v1.json",
    "record_approval_ack_evidence_closure_lifecycle_slice_v1.json",
    "absence_and_rollback_safety_lifecycle_slice_v1.json",
    "result_first_module_engineering_rule_reference_v1.json",
    "functional_slice_next_phase_readiness_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

UPSTREAM_INDEX: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "authorization_preparation_dryrun_report_v1.json",
    "functional_slice_followup_reference_v1.json",
)

SLICE_REQUIRED_FIELDS: Tuple[str, ...] = (
    "slice_id",
    "slice_name",
    "primary_result",
    "entry_condition",
    "input_objects",
    "output_objects",
    "state_path",
    "forbidden_state_transitions",
    "success_criteria",
    "failure_criteria",
    "fallback_or_defer_strategy",
    "required_absence_conditions",
    "protocol_refs_lightweight_only",
    "evidence_refs",
    "file_size_governance_ref",
    "execution_allowed",
    "test_executed",
)

SLICE_ARTIFACT_BY_ID: Dict[str, str] = {
    "owner_approval_request_candidate_lifecycle": "owner_approval_request_candidate_lifecycle_slice_v1.json",
    "authorization_preparation_lifecycle": "authorization_preparation_lifecycle_slice_v1.json",
    "record_approval_ack_evidence_closure_lifecycle": "record_approval_ack_evidence_closure_lifecycle_slice_v1.json",
    "absence_and_rollback_safety_lifecycle": "absence_and_rollback_safety_lifecycle_slice_v1.json",
}

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_authorization_preparation_dryrun_go",
    "functional_slice_plan_complete",
    "functional_slice_registry_complete",
    "owner_approval_request_candidate_lifecycle_slice_complete",
    "authorization_preparation_lifecycle_slice_complete",
    "record_approval_ack_evidence_closure_lifecycle_slice_complete",
    "absence_and_rollback_safety_lifecycle_slice_complete",
    "result_first_rule_ref_ok",
    "module_first_cadence_rule_ref_ok",
    "no_fragmentary_phase_expansion",
    "functional_slice_tests_not_executed",
    "non_execution_boundary_ok",
    "file_size_governance_review_ok",
    "next_phase_readiness_ok",
)

_SLICE_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "slice_id": "owner_approval_request_candidate_lifecycle",
        "slice_name": "Owner Approval Request Candidate Lifecycle",
        "primary_result": "Owner approval request remains candidate through authorization preparation without real request issued.",
        "entry_condition": "Integrated implementation GO and authorization preparation dryrun GO with selected authorization preparation route.",
        "input_objects": [
            "owner_approval_request_candidate",
            "issuance_authorization_preparation_package_candidate",
            "missing_conditions_routing_v1",
        ],
        "output_objects": [
            "owner_approval_request_candidate",
            "authorization_preparation_package_candidate",
            "missing_conditions_routing_outcome",
        ],
        "state_path": [
            "candidate_created",
            "enters_authorization_preparation",
            "remains_candidate",
            "missing_conditions_routed",
            "no_real_request_issued",
        ],
        "forbidden_state_transitions": [
            "candidate_to_real_request_issued",
            "candidate_to_authorization_request_created",
            "candidate_to_grant_issued",
        ],
        "success_criteria": [
            "input candidate preserved as output candidate",
            "authorization preparation package referenced without escalation",
            "missing conditions routed without real issuance",
            "reject_expire_revoke_defer paths documented",
        ],
        "failure_criteria": [
            "real_request_issued",
            "authorization_request_created",
            "candidate_lost_without_routing",
        ],
        "fallback_or_defer_strategy": "Defer to missing_conditions_routing buckets; hold real issuance until explicit authorization preparation closure.",
        "required_absence_conditions": list(ABSENCE_KEYS),
        "evidence_refs": [
            "issuance_authorization_preparation_package_v1",
            "missing_conditions_routing_v1",
            "functional_slice_followup_reference_v1",
        ],
    },
    {
        "slice_id": "authorization_preparation_lifecycle",
        "slice_name": "Authorization Preparation Lifecycle",
        "primary_result": "Authorization preparation package organizes explicit approval and readiness preconditions without real authorization.",
        "entry_condition": "Authorization preparation package candidate validated by dryrun with precondition checklist present.",
        "input_objects": [
            "issuance_authorization_preparation_package_candidate",
            "real_issuance_precondition_checklist_v1",
            "owner_operator_explicit_approval_requirement",
        ],
        "output_objects": [
            "authorization_preparation_package_candidate",
            "precondition_gap_matrix",
            "authorization_readiness_deferred_state",
        ],
        "state_path": [
            "package_still_candidate",
            "explicit_approval_missing",
            "authorization_request_absent",
            "authorization_grant_absent",
            "real_request_issuance_authorized_false",
        ],
        "forbidden_state_transitions": [
            "package_to_authorization_request",
            "package_to_authorization_grant",
            "package_to_real_request_issuance",
        ],
        "success_criteria": [
            "package_still_candidate",
            "explicit_approval_missing_documented",
            "authorization_request_absent",
            "authorization_grant_absent",
            "real_request_issuance_authorized_false",
        ],
        "failure_criteria": [
            "authorization_request_created",
            "grant_issued",
            "real_request_issuance_authorized_true",
        ],
        "fallback_or_defer_strategy": "Route denial_expiry_revocation to reference-only paths; defer authorization request creation.",
        "required_absence_conditions": [
            "authorization_request_absent",
            "grant_absent",
            "request_issued_absent",
            "notification_sent_absent",
        ],
        "evidence_refs": [
            "authorization_preparation_dryrun_report_v1",
            "real_issuance_precondition_checklist_v1",
        ],
    },
    {
        "slice_id": "record_approval_ack_evidence_closure_lifecycle",
        "slice_name": "Record Approval Ack Evidence Closure Lifecycle",
        "primary_result": "Record, approval, ack, and evidence-bound candidates maintain boundary relationships without creation or closure execution.",
        "entry_condition": "Closure boundary artifact from integrated implementation with all core records absent.",
        "input_objects": [
            "request_record_candidate_boundary",
            "approval_record_candidate_boundary",
            "ack_candidate_boundary",
            "evidence_bound_candidate_boundary",
        ],
        "output_objects": [
            "record_creation_preconditions_matrix",
            "closure_deferred_state",
        ],
        "state_path": [
            "request_record_absent",
            "approval_record_absent",
            "ack_record_absent",
            "evidence_bound_record_absent",
            "creation_preconditions_documented",
            "closure_not_executed",
        ],
        "forbidden_state_transitions": [
            "absent_to_request_record_created",
            "absent_to_approval_record_created",
            "absent_to_ack_record_created",
            "absent_to_evidence_bound_created",
            "boundary_to_closure_executed",
        ],
        "success_criteria": [
            "all record types remain absent",
            "creation preconditions enumerated",
            "closure_not_executed",
        ],
        "failure_criteria": [
            "any_record_created",
            "closure_executed",
            "evidence_bound_without_preconditions",
        ],
        "fallback_or_defer_strategy": "Keep candidate-level boundaries; defer closure until authorization preparation and slice dryrun complete.",
        "required_absence_conditions": [
            "request_record_absent",
            "approval_record_absent",
            "ack_record_absent",
            "evidence_bound_record_absent",
            "closure_not_executed",
        ],
        "evidence_refs": [
            "record_approval_ack_evidence_closure_boundary_v1",
            "module_level_functional_slice_test_plan_v1",
        ],
    },
    {
        "slice_id": "absence_and_rollback_safety_lifecycle",
        "slice_name": "Absence And Rollback Safety Lifecycle",
        "primary_result": "Full-chain absence and rollback safety boundaries hold without runtime, adapter, or whitebox integration.",
        "entry_condition": "Authorization preparation dryrun safety boundary validated with absence keys true.",
        "input_objects": [
            "absence_boundary_matrix",
            "rollback_expiry_revocation_reference",
            "runtime_forbidden_flags",
        ],
        "output_objects": [
            "absence_safety_report",
            "rollback_safety_deferred_state",
        ],
        "state_path": [
            "notification_sent_absent",
            "grant_absent",
            "foundation_not_frozen",
            "runtime_execution_absent",
            "module_adapter_implementation_absent",
            "whitebox_runtime_integration_absent",
            "rejection_expiry_revocation_rollback_safe",
        ],
        "forbidden_state_transitions": [
            "absent_to_notification_sent",
            "absent_to_grant",
            "not_frozen_to_foundation_frozen",
            "absent_to_runtime_enabled",
            "absent_to_adapter_implemented",
            "absent_to_whitebox_integrated",
        ],
        "success_criteria": [
            "all required absence conditions true",
            "rollback paths reference-only",
            "no runtime or adapter scope leakage",
        ],
        "failure_criteria": [
            "any_absence_drift",
            "runtime_enabled",
            "foundation_frozen_without_gate",
        ],
        "fallback_or_defer_strategy": "Reject unsafe transitions; route runtime debt to future_runtime_debt bucket; defer rollback rehearsal.",
        "required_absence_conditions": list(ABSENCE_KEYS),
        "evidence_refs": [
            "real_issuance_safety_boundary_validation_v1",
            "authorization_preparation_dryrun_report_v1",
        ],
    },
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(out: Path, upstream: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "functional_slice_planning_only": True,
        "no_fragmentary_phase_expansion": True,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        "output_root": str(out),
        "authorization_preparation_dryrun_root": str(upstream),
    }


def _build_slice(spec: Dict[str, Any], *, meta: Dict[str, Any]) -> Dict[str, Any]:
    slice_id = spec["slice_id"]
    payload: Dict[str, Any] = {
        **spec,
        "protocol_refs_lightweight_only": {
            "result_first_module_engineering_rule_ref": RESULT_FIRST_MODULE_ENGINEERING_RULE_REF,
            "module_first_development_verification_cadence_rule_ref": MODULE_FIRST_DEVELOPMENT_VERIFICATION_CADENCE_RULE_REF,
            "reuse_first_protocol_engineering_rule_ref": REUSE_FIRST_PROTOCOL_ENGINEERING_RULE_REF,
            "validate_once_per_module_rule_ref": VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
            "file_size_module_split_governance_rule_ref": FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_REF,
        },
        "file_size_governance_ref": FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_REF,
        "execution_allowed": False,
        "test_executed": False,
        f"{slice_id}_slice_complete": True,
        **meta,
    }
    return payload


def _slice_complete(slice_doc: Dict[str, Any]) -> bool:
    if not slice_doc:
        return False
    if slice_doc.get("execution_allowed") is not False or slice_doc.get("test_executed") is not False:
        return False
    for field in SLICE_REQUIRED_FIELDS:
        if field in ("execution_allowed", "test_executed"):
            continue
        val = slice_doc.get(field)
        if val is None or val == "" or (isinstance(val, (list, dict, tuple)) and len(val) == 0):
            return False
    return True


def run_task_manager_owner_approval_request_module_level_functional_slice_planning_v1(
    *,
    authorization_preparation_dryrun_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(authorization_preparation_dryrun_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    dryrun_summary = _read_json(upstream / "summary.json")
    dryrun_verifier = _read_json(upstream / "verifier_report.json")
    dryrun_report = _read_json(upstream / UPSTREAM_INDEX[2])
    slice_followup = _read_json(upstream / UPSTREAM_INDEX[3])
    dryrun_file_size = _read_json(upstream / "file_size_governance_review_v1.json")

    impl_root = Path(dryrun_summary.get("integrated_implementation_root") or "").expanduser()
    impl_summary = _read_json(impl_root / "summary.json") if impl_root.is_dir() else {}

    prior_authorization_preparation_dryrun_go = (
        dryrun_summary.get("final_decision") == AUTHORIZATION_PREPARATION_DRYRUN_FINAL_GO
        and dryrun_summary.get("recommended_next_phase") == AUTHORIZATION_PREPARATION_DRYRUN_NEXT_PHASE
        and dryrun_verifier.get("verifier") == "GO"
        and int(dryrun_verifier.get("passed_checks", 0)) >= 260
        and dryrun_summary.get("authorization_preparation_dryrun_pass") is True
        and dryrun_summary.get("selected_route") == SELECTED_ROUTE
        and dryrun_summary.get("no_fragmentary_phase_expansion") is True
        and dryrun_summary.get("real_request_issuance_authorized") is False
    )
    if not prior_authorization_preparation_dryrun_go:
        issues.append("authorization_preparation_dryrun_not_go")

    prior_integrated_implementation_go = (
        prior_authorization_preparation_dryrun_go
        and dryrun_summary.get("prior_integrated_implementation_go") is True
        and impl_summary.get("final_decision") == INTEGRATED_IMPLEMENTATION_FINAL_GO
    )
    if prior_authorization_preparation_dryrun_go and not prior_integrated_implementation_go:
        issues.append("integrated_implementation_upstream_gap")

    slice_chains = list(slice_followup.get("chains") or [])
    functional_slice_tests_not_executed = (
        prior_authorization_preparation_dryrun_go
        and slice_followup.get("functional_slice_followup_ok") is True
        and len(slice_chains) == len(FUNCTIONAL_SLICE_CHAINS)
        and all(not c.get("executed") for c in slice_chains)
    )
    if not functional_slice_tests_not_executed:
        issues.append("functional_slice_followup_gap")

    slices: Dict[str, Dict[str, Any]] = {}
    for spec in _SLICE_SPECS:
        doc = _build_slice(spec, meta=meta)
        slices[spec["slice_id"]] = doc

    slice_complete_flags = {sid: _slice_complete(slices[sid]) for sid in FUNCTIONAL_SLICE_CHAINS}
    for sid, ok in slice_complete_flags.items():
        if not ok:
            issues.append(f"slice_incomplete:{sid}")

    functional_slice_registry_complete = all(slice_complete_flags.values())
    functional_slice_plan_complete = (
        prior_authorization_preparation_dryrun_go
        and functional_slice_registry_complete
        and len(slices) == len(FUNCTIONAL_SLICE_CHAINS)
    )

    result_first_doc = build_result_first_module_engineering_rule_document(
        extra={
            "result_first_rule_ref_ok": True,
            "reuse_first_protocol_engineering_rule_ref": REUSE_FIRST_PROTOCOL_ENGINEERING_RULE_REF,
            "validate_once_per_module_rule_ref": VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
            "shared_protocol_system_revalidation": False,
            "l1_input_output_protocol_revalidation": False,
            **meta,
        }
    )
    result_first_rule_ref_ok = result_first_doc.get("result_first_module_engineering_rule_complete") is True
    module_first_cadence_rule_ref_ok = True

    absence = {key: dryrun_summary.get(key) is True for key in ABSENCE_KEYS}
    non_execution_boundary_ok = (
        prior_authorization_preparation_dryrun_go
        and dryrun_summary.get("non_execution_boundary_ok") is True
        and dryrun_summary.get("real_request_issuance_authorized") is False
        and all(absence.values())
    )
    for flag in RUNTIME_FORBIDDEN_FLAGS:
        if dryrun_summary.get(flag) is True:
            non_execution_boundary_ok = False
            issues.append(f"runtime_flag:{flag}")
            break
    if not non_execution_boundary_ok and "runtime_flag" not in "".join(issues):
        issues.append("non_execution_boundary_gap")

    template_lineage = build_template_lineage(
        base_phase="Owner-Approval-Request-Authorization-Preparation-DryRun-v1-001",
        base_capability=OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_WHITELIST_FILES[0],
        base_runner=OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_WHITELIST_FILES[1],
        base_verifier=OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=PLANNING_GO_NO_GO_PACK,
        stage_phase="Owner-Approval-Request-Module-Level-Functional-Slice-Planning-v1-001",
        stage_term_overrides=OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_STAGE_ADDITIONS,
        template_files=OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Owner-Approval-Request-Authorization-Preparation-DryRun-v1-001",
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
        previous_interruption_type=dryrun_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=dryrun_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=dryrun_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    planning_pass = (
        prior_authorization_preparation_dryrun_go
        and prior_integrated_implementation_go
        and functional_slice_plan_complete
        and functional_slice_registry_complete
        and all(slice_complete_flags.values())
        and result_first_rule_ref_ok
        and module_first_cadence_rule_ref_ok
        and functional_slice_tests_not_executed
        and non_execution_boundary_ok
        and template_lineage.get("template_lineage_ok") is True
        and file_size_governance_review_ok
        and len(issues) == 0
    )
    next_phase_readiness_ok = planning_pass

    if not prior_authorization_preparation_dryrun_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not functional_slice_plan_complete:
        final_decision = FINAL_DECISION_SLICE
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    else:
        final_decision = FINAL_DECISION_GO

    go_values = {
        "prior_authorization_preparation_dryrun_go": prior_authorization_preparation_dryrun_go,
        "prior_integrated_implementation_go": prior_integrated_implementation_go,
        "functional_slice_plan_complete": functional_slice_plan_complete,
        "functional_slice_registry_complete": functional_slice_registry_complete,
        "owner_approval_request_candidate_lifecycle_slice_complete": slice_complete_flags[
            "owner_approval_request_candidate_lifecycle"
        ],
        "authorization_preparation_lifecycle_slice_complete": slice_complete_flags[
            "authorization_preparation_lifecycle"
        ],
        "record_approval_ack_evidence_closure_lifecycle_slice_complete": slice_complete_flags[
            "record_approval_ack_evidence_closure_lifecycle"
        ],
        "absence_and_rollback_safety_lifecycle_slice_complete": slice_complete_flags[
            "absence_and_rollback_safety_lifecycle"
        ],
        "result_first_rule_ref_ok": result_first_rule_ref_ok,
        "module_first_cadence_rule_ref_ok": module_first_cadence_rule_ref_ok,
        "reuse_first_rule_ref_ok": True,
        "validate_once_rule_ref_ok": True,
        "no_fragmentary_phase_expansion": True,
        "functional_slice_tests_not_executed": functional_slice_tests_not_executed,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "functional_slice_planning_pass": planning_pass,
        "real_request_issuance_authorized": False,
        "authorization_request_absent": True,
        "selected_route": SELECTED_ROUTE,
        "template_lineage_ok": template_lineage.get("template_lineage_ok") is True,
        "monolithic_file_absent": file_size_governance_review.get("monolithic_file_absent") is True,
        "full_repo_scan_absent": file_size_governance_review.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size_governance_review.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size_governance_review.get("summary_index_first_reading_ok") is True,
        "limited_directory_scan_ok": file_size_governance_review.get("limited_directory_scan_ok") is True,
        **absence,
    }
    next_phase = NEXT_PHASE_A if planning_pass else NEXT_PHASE_HOLD
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(
            list(dryrun_summary.get("chain_trace_nodes") or [])
            + ["owner_approval_request_module_level_functional_slice_planning"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    registry = {
        "registry_id": "functional_slice_registry_v1",
        "functional_slice_registry_complete": functional_slice_registry_complete,
        "slices": [
            {
                "slice_id": sid,
                "artifact": SLICE_ARTIFACT_BY_ID[sid],
                "execution_allowed": False,
                "test_executed": False,
                "complete": slice_complete_flags[sid],
            }
            for sid in FUNCTIONAL_SLICE_CHAINS
        ],
        **meta,
    }
    plan = {
        "plan_id": "module_level_functional_slice_plan_v1",
        "module_level_functional_slice_plan_complete": functional_slice_plan_complete,
        "primary_objective": "Define result-oriented functional slice verification paths for Task Manager Owner Approval Request governance.",
        "selected_route": SELECTED_ROUTE,
        "slice_ids": list(FUNCTIONAL_SLICE_CHAINS),
        "execution_allowed": False,
        "functional_slice_tests_not_executed": functional_slice_tests_not_executed,
        "top_level_objective_priority_rule_ref": TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_REF,
        "result_first_module_engineering_rule_ref": RESULT_FIRST_MODULE_ENGINEERING_RULE_REF,
        "module_first_development_verification_cadence_rule_ref": MODULE_FIRST_DEVELOPMENT_VERIFICATION_CADENCE_RULE_REF,
        **go_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        "next_phase_candidates": [NEXT_PHASE_A, NEXT_PHASE_B],
        **meta,
    }
    next_phase_readiness = {
        "readiness_id": "functional_slice_next_phase_readiness_v1",
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "recommended_next_phase": next_phase,
        "next_phase_candidates": [
            {"phase_id": NEXT_PHASE_A, "intent": "Execute module-level functional slice dryrun without real issuance"},
            {"phase_id": NEXT_PHASE_B, "intent": "Close module governance if slice dryrun deferred"},
        ],
        "decision_guidance": "Choose functional slice dryrun when slice boundaries need empirical validation; choose module governance closure when planning suffices.",
        **meta,
    }
    result_first_reference = {
        "reference_id": "result_first_module_engineering_rule_reference_v1",
        "result_first_module_engineering_rule_ref": RESULT_FIRST_MODULE_ENGINEERING_RULE_REF,
        "result_first_module_engineering_rule_doc": RESULT_FIRST_MODULE_ENGINEERING_RULE_DOC,
        "top_level_objective_priority_rule_ref": TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_REF,
        "top_level_objective_priority_rule_doc": TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_DOC,
        "module_first_development_verification_cadence_rule_ref": MODULE_FIRST_DEVELOPMENT_VERIFICATION_CADENCE_RULE_REF,
        "module_first_cadence_rule_doc": MODULE_FIRST_CADENCE_RULE_DOC,
        "reuse_first_protocol_engineering_rule_ref": REUSE_FIRST_PROTOCOL_ENGINEERING_RULE_REF,
        "validate_once_per_module_rule_ref": VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
        "file_size_module_split_governance_rule_ref": FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_REF,
        "file_size_module_split_governance_rule_doc": FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_DOC,
        "result_first_rule_ref_ok": result_first_rule_ref_ok,
        "module_first_cadence_rule_ref_ok": module_first_cadence_rule_ref_ok,
        "reuse_first_rule_ref_ok": True,
        "validate_once_rule_ref_ok": True,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        **result_first_doc,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "functional_slice_planning_pass": planning_pass,
        "blocker_count": len(issues),
        "issues": issues,
        **go_values,
        **core_fields,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Module-Level Functional Slice Plan v1",
            "",
            "Result-first functional slice planning. No slice test execution, no real issuance.",
            "",
            f"Selected route: `{SELECTED_ROUTE}`",
            f"Functional slice plan complete: `{functional_slice_plan_complete}`",
            f"Slice count: `{len(FUNCTIONAL_SLICE_CHAINS)}`",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{next_phase}`",
        ]
    )
    return {
        "module_level_functional_slice_plan": plan,
        "module_level_functional_slice_plan_md": markdown,
        "functional_slice_registry": registry,
        "owner_approval_request_candidate_lifecycle_slice": slices["owner_approval_request_candidate_lifecycle"],
        "authorization_preparation_lifecycle_slice": slices["authorization_preparation_lifecycle"],
        "record_approval_ack_evidence_closure_lifecycle_slice": slices[
            "record_approval_ack_evidence_closure_lifecycle"
        ],
        "absence_and_rollback_safety_lifecycle_slice": slices["absence_and_rollback_safety_lifecycle"],
        "result_first_module_engineering_rule_reference": result_first_reference,
        "functional_slice_next_phase_readiness": next_phase_readiness,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
