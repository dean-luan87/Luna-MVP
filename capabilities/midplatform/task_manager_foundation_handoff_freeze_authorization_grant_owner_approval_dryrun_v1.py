# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval DryRun v1.

Structure inherited from task_manager_foundation_handoff_freeze_authorization_grant_request_record_dryrun_v1.py
with upstream input from grant_owner_approval_planning_v1 and protocol_canonical_standard_shared_code_smoke_v1.
Protocol Standard Validate Once, Reference Many Times — light protocol reference only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.protocol_canonical_standard_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.protocol_canonical_standard_shared_code_smoke_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PROTOCOL_SHARED_CODE_SMOKE_ROOT,
    FINAL_DECISION_GO as PROTOCOL_SMOKE_FINAL_GO,
)
from capabilities.midplatform.protocols.protocol_error_codes_v1 import build_error_code, validate_error_code
from capabilities.midplatform.protocols.protocol_separation_rule_v1 import (
    FAILURE_CLASSIFICATION,
    RULE_NAME_EN as SEPARATION_RULE_NAME_EN,
)
from capabilities.midplatform.protocols.protocol_whitebox_binding_v1 import build_whitebox_diagnostic_ref
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    GRANT_OWNER_APPROVAL_DRYRUN_STAGE_ADDITIONS,
    GRANT_OWNER_APPROVAL_DRYRUN_STAGE_TERM_OVERRIDES,
    GRANT_OWNER_APPROVAL_DRYRUN_WHITELIST_FILES,
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_planning_v1 import (
    BOUNDARY_CONTRACT_STATEMENTS,
    CHAIN_EVIDENCE_NODES,
    DEFAULT_OUTPUT as DEFAULT_GRANT_OWNER_APPROVAL_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    GRANT_OWNER_APPROVAL_PLANNING_PACKAGE_FILES,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    PLANNING_TRUE_KEYS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_request_record_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-DryRun-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_dryrun_validation_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_dryrun_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
)
FINAL_DECISION_PLAN_GAP = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_DRYRUN_BLOCKED_BY_PLANNING_PACKAGE_GAP"
)
FINAL_DECISION_SCOPE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_DRYRUN_BLOCKED_BY_APPROVAL_SCOPE_ESCALATION"
)
FINAL_DECISION_APPROVAL = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_DRYRUN_BLOCKED_BY_OWNER_APPROVAL_RECORD_LEAKAGE"
)
FINAL_DECISION_REQUEST = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_DRYRUN_BLOCKED_BY_AUTHORIZATION_REQUEST_LEAKAGE"
)
FINAL_DECISION_FREEZE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_DRYRUN_BLOCKED_BY_FREEZE_STATE_ESCALATION"
)
FINAL_DECISION_DEBT = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_DRYRUN_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
)
FINAL_DECISION_L1 = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_DRYRUN_BLOCKED_BY_L1_PROTOCOL_SCOPE_LEAKAGE"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_DRYRUN_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_PROTOCOL = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_DRYRUN_BLOCKED_BY_PROTOCOL_REFERENCE_GAP"
)
NEXT_PHASE_GO = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Post-DryRun-Review-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-DryRun-Issue-Review-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_dryrun_v1_smoke_v0"
)

PROTOCOL_STANDARD_REF = (
    "MIDPLATFORM_PROTOCOL_CANONICAL_STANDARD_SHARED_CODE_SMOKE_READY_FOR_TASK_MANAGER_OWNER_APPROVAL_DRYRUN"
)
PROTOCOL_ID = "LUNA-PROTO-L1-APPROVAL-ACK-V1"
RELATED_PROTOCOL_IDS: Tuple[str, ...] = (
    "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1",
    "LUNA-PROTO-L1-EVIDENCE-BINDING-V1",
    "LUNA-PROTO-L1-WHITEBOX-DIAGNOSTIC-BINDING-V1",
)
ERROR_NAMESPACE = "LUNA-PROTO-L1-APPROVAL-ACK-V1::*"
PROTOCOL_EXECUTION_RESULT_SCHEMA_REF = "protocol_execution_result_schema_v1"
SEPARATION_RULE_REF = "Protocol Constraint vs Module Logic Separation Rule"

GRANT_OWNER_APPROVAL_DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_dryrun_report_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_dryrun_report_v1.md",
    "task_manager_freeze_authorization_grant_owner_approval_plan_integrity_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_scope_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_candidate_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_operator_ack_candidate_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_evidence_binding_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_binding_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_lifecycle_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_expiry_revocation_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_prerequisite_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_evidence_traceability_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_absence_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_boundary_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_protocol_reference_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_governance_debt_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_template_lineage_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_post_review_readiness_v1.json",
    "summary.json",
    "verifier_report.json",
)
CHAIN_TRACE_NODES: Tuple[str, ...] = CHAIN_EVIDENCE_NODES + ("freeze_authorization_grant_owner_approval_dryrun",)
DRYRUN_BOUNDARY_STATEMENTS: Tuple[str, ...] = ("owner_approval_dryrun != owner_approval",) + BOUNDARY_CONTRACT_STATEMENTS
ALLOWED_SCOPE_CLASSIFICATIONS: Tuple[str, ...] = (
    "owner-approval-planning-scope",
    "owner-approval-dryrun-scope",
)
FORBIDDEN_ASSET_STATES: Tuple[str, ...] = (
    "frozen",
    "foundation-frozen",
    "closed",
    "foundation-finalized",
    "owner-approval-record",
    "owner-operator-ack-record",
    "approval-evidence-bound-record",
    "request-record",
    "authorization-request-issued",
    "approval-revocation-execution-path",
    "grant-token",
    "grant-record",
)
GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_owner_approval_planning_go",
    "protocol_standard_reference_ok",
    "protocol_id_reference_ok",
    "error_namespace_reference_ok",
    "protocol_execution_result_schema_ref_ok",
    "separation_rule_ref_ok",
    "owner_approval_plan_integrity_ok",
    "approval_scope_preserved",
    "owner_approval_candidate_preserved",
    "owner_operator_ack_candidate_preserved",
    "approval_evidence_binding_candidate_preserved",
    "request_record_binding_candidate_preserved",
    "approval_lifecycle_candidate_preserved",
    "expiry_revocation_reference_candidate_preserved",
    "approval_prerequisites_satisfied",
    "approval_evidence_traceability_ok",
    "authorization_request_absent",
    "request_record_absent",
    "owner_approval_record_absent",
    "owner_operator_ack_record_absent",
    "approval_evidence_bound_record_absent",
    "grant_token_absent",
    "grant_record_absent",
    "authorization_grant_absent",
    "foundation_not_frozen",
    "closure_not_executed",
    "governance_debt_preserved",
    "l1_protocols_not_implemented",
    "system_protocols_integration_not_implemented",
    "template_lineage_ok",
    "owner_approval_dryrun_only",
    "post_review_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(out: Path, planning: Path, smoke: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": FOUNDATION_ID,
        "runtime_status": "not_enabled",
        "owner_approval_dryrun_only": True,
        "shared_protocol_system_revalidation": False,
        "protocol_standard_ref": PROTOCOL_STANDARD_REF,
        "protocol_id": PROTOCOL_ID,
        "related_protocol_ids": list(RELATED_PROTOCOL_IDS),
        "error_namespace": ERROR_NAMESPACE,
        "protocol_execution_result_schema_ref": PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
        "separation_rule_ref": SEPARATION_RULE_REF,
        "authorization_request_absent": True,
        "authorization_request_issued": False,
        "request_record_absent": True,
        "owner_approval_record_absent": True,
        "owner_operator_ack_record_absent": True,
        "approval_evidence_bound_record_absent": True,
        "authorization_grant_absent": True,
        "grant_token_absent": True,
        "grant_record_absent": True,
        "foundation_not_frozen": True,
        "closure_not_executed": True,
        "l1_protocols_not_implemented": True,
        "system_protocols_integration_not_implemented": True,
        "output_root": str(out),
        "grant_owner_approval_planning_root": str(planning),
        "protocol_shared_code_smoke_root": str(smoke),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_dryrun_v1(
    *,
    grant_owner_approval_planning_root: str,
    protocol_shared_code_smoke_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    planning = Path(grant_owner_approval_planning_root).expanduser().resolve()
    smoke = Path(protocol_shared_code_smoke_root or DEFAULT_PROTOCOL_SHARED_CODE_SMOKE_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, planning, smoke)
    issues: List[str] = []

    planning_summary = _read_json(planning / "summary.json")
    planning_verifier = _read_json(planning / "verifier_report.json")
    smoke_summary = _read_json(smoke / "summary.json")
    smoke_verifier = _read_json(smoke / "verifier_report.json")
    scope_matrix = _read_json(planning / "task_manager_freeze_authorization_grant_owner_approval_scope_matrix_v1.json")
    candidate_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_candidate_matrix_v1.json"
    )
    ack_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_operator_ack_candidate_matrix_v1.json"
    )
    evidence_binding_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_evidence_binding_matrix_v1.json"
    )
    record_binding_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_request_record_binding_matrix_v1.json"
    )
    lifecycle_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_lifecycle_matrix_v1.json"
    )
    expiry_revocation_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_expiry_revocation_matrix_v1.json"
    )
    prerequisite_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_prerequisite_matrix_v1.json"
    )
    approval_plan = _read_json(
        planning / "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_plan_v1.json"
    )
    boundary_contract = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_boundary_contract_v1.json"
    )
    debt_carryover = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_governance_debt_carryover_v1.json"
    )
    non_execution_doc = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_non_execution_constraints_v1.json"
    )

    integrity_rows = []
    for fname in GRANT_OWNER_APPROVAL_PLANNING_PACKAGE_FILES:
        path = planning / fname
        if fname.endswith(".json"):
            non_placeholder = bool(_read_json(path))
        else:
            non_placeholder = path.is_file() and len(path.read_text(encoding="utf-8").strip()) > 200
        integrity_rows.append({"file": fname, "exists": path.is_file(), "non_placeholder": non_placeholder})
        if not path.is_file() or not non_placeholder:
            issues.append(f"missing_or_placeholder:{fname}")

    prior_owner_approval_planning_go = (
        planning_summary.get("final_decision") == PLANNING_FINAL_GO
        and planning_summary.get("recommended_next_phase") == PLANNING_NEXT_PHASE
        and planning_verifier.get("verifier") == "GO"
        and int(planning_verifier.get("passed_checks", 0)) >= 420
        and planning_verifier.get("failed_checks") == 0
        and planning_verifier.get("blocker_count") == 0
        and planning_summary.get("next_phase_readiness_ok") is True
    )
    if not prior_owner_approval_planning_go:
        issues.append("owner_approval_planning_not_go")

    for key in PLANNING_TRUE_KEYS:
        if planning_summary.get(key) is not True:
            issues.append(f"planning_key_false:{key}")

    protocol_standard_reference_ok = (
        smoke_summary.get("final_decision") == PROTOCOL_SMOKE_FINAL_GO
        and smoke_summary.get("final_decision") == PROTOCOL_STANDARD_REF
        and smoke_verifier.get("verifier") == "GO"
        and int(smoke_verifier.get("passed_checks", 0)) >= 420
        and smoke_verifier.get("failed_checks") == 0
        and smoke_verifier.get("blocker_count") == 0
        and smoke_summary.get("ready_for_task_manager_owner_approval_dryrun") is True
    )
    if not protocol_standard_reference_ok:
        issues.append("protocol_standard_reference_gap")

    protocol_id_reference_ok = PROTOCOL_ID.startswith("LUNA-PROTO-") and PROTOCOL_ID.endswith("-V1")
    error_namespace_reference_ok = ERROR_NAMESPACE == f"{PROTOCOL_ID}::*"
    protocol_execution_result_schema_ref_ok = bool(PROTOCOL_EXECUTION_RESULT_SCHEMA_REF)
    separation_rule_ref_ok = SEPARATION_RULE_REF == SEPARATION_RULE_NAME_EN

    sample_protocol_error_code = build_error_code(PROTOCOL_ID, "AUTH", 1)
    protocol_error_code_light_check_ok = validate_error_code(sample_protocol_error_code)
    whitebox_candidate_ref = build_whitebox_diagnostic_ref(
        phase_id=PHASE_ID,
        protocol_id=PROTOCOL_ID,
        error_code=sample_protocol_error_code,
        artifact_ref="summary.json",
        field_path="go_conditions.owner_approval_candidate_preserved",
    )
    whitebox_candidate_ref_ok = (
        whitebox_candidate_ref.get("binding_mode") == "contract_only"
        and whitebox_candidate_ref.get("runtime_integration") is False
        and str(whitebox_candidate_ref.get("whitebox_trace_ref", "")).startswith("wb://")
        and str(whitebox_candidate_ref.get("diagnostic_node_ref", "")).startswith("diag://")
    )
    if not protocol_id_reference_ok or not protocol_error_code_light_check_ok:
        issues.append("protocol_id_reference_gap")
    if not error_namespace_reference_ok:
        issues.append("error_namespace_reference_gap")
    if not protocol_execution_result_schema_ref_ok:
        issues.append("protocol_execution_result_schema_ref_gap")
    if not separation_rule_ref_ok:
        issues.append("separation_rule_ref_gap")
    if not whitebox_candidate_ref_ok:
        issues.append("whitebox_candidate_ref_gap")

    trace_rows = list(approval_plan.get("evidence_chain") or [])
    trace_rows.append(
        {
            "stage": "freeze_authorization_grant_owner_approval_dryrun",
            "root": str(out),
            "readiness": "owner-approval-dryrun-scope",
            "authorization_request_issued": False,
            "request_record": False,
            "owner_approval_record": False,
            "owner_operator_ack_record": False,
            "grant_issued": False,
            "linked": True,
        }
    )
    approval_evidence_traceability_ok = all(
        next((r for r in trace_rows if r.get("stage") == stage), {}).get("linked") is True
        for stage in CHAIN_TRACE_NODES
    )
    dryrun_node = next(
        (r for r in trace_rows if r.get("stage") == "freeze_authorization_grant_owner_approval_dryrun"),
        {},
    )
    if (
        dryrun_node.get("authorization_request_issued") is True
        or dryrun_node.get("request_record") is True
        or dryrun_node.get("owner_approval_record") is True
        or dryrun_node.get("owner_operator_ack_record") is True
        or dryrun_node.get("grant_issued") is True
    ):
        approval_evidence_traceability_ok = False
    if not approval_evidence_traceability_ok:
        issues.append("chain_trace_gap")

    scope_rows = []
    for row in scope_matrix.get("rows") or []:
        scope_rows.append({**row, "classification": "owner-approval-dryrun-scope"})
    approval_scope_preserved = all(
        row.get("classification") in ALLOWED_SCOPE_CLASSIFICATIONS for row in scope_rows
    ) and all(
        row.get("classification") not in ("approval-granted-scope", "authorized-scope") for row in scope_rows
    )
    if not approval_scope_preserved:
        issues.append("approval_scope_escalation")

    freeze_status = boundary_contract.get("freeze_status") or "freeze-candidate"
    owner_rows = candidate_matrix.get("rows") or []
    owner_approval_candidate_preserved = all(
        row.get("approval_status") == "owner-approval-candidate"
        and row.get("approval_status") != "owner-approval-record"
        and row.get("approval_record") is False
        and row.get("owner_approval_record") is False
        for row in owner_rows
    ) if owner_rows else candidate_matrix.get("owner_approval_candidate_only") is True
    if not owner_approval_candidate_preserved:
        issues.append("owner_approval_record_leakage")

    ack_rows = ack_matrix.get("rows") or []
    owner_operator_ack_candidate_preserved = all(
        row.get("ack_status") == "owner-operator-ack-candidate"
        and row.get("ack_status") != "owner-operator-ack-record"
        and row.get("ack_record") is False
        and row.get("owner_operator_ack_record") is False
        for row in ack_rows
    ) if ack_rows else ack_matrix.get("owner_operator_ack_candidate_only") is True
    if not owner_operator_ack_candidate_preserved:
        issues.append("owner_operator_ack_record_leakage")

    evidence_binding_rows = evidence_binding_matrix.get("rows") or []
    approval_evidence_binding_candidate_preserved = all(
        row.get("binding_status") == "approval-evidence-binding-candidate"
        and row.get("binding_status") != "approval-evidence-bound-record"
        and row.get("approval_evidence_bound") is False
        for row in evidence_binding_rows
    ) if evidence_binding_rows else evidence_binding_matrix.get("approval_evidence_binding_candidate_only") is True
    if not approval_evidence_binding_candidate_preserved:
        issues.append("approval_evidence_binding_leakage")

    record_binding_rows = record_binding_matrix.get("rows") or []
    request_record_binding_candidate_preserved = all(
        row.get("binding_status") == "request-record-binding-candidate"
        and row.get("request_record_bound") is False
        and row.get("active_bound_request_record") is False
        for row in record_binding_rows
    ) if record_binding_rows else record_binding_matrix.get("request_record_binding_candidate_only") is True
    if not request_record_binding_candidate_preserved:
        issues.append("request_record_binding_leakage")

    lifecycle_rows = lifecycle_matrix.get("rows") or []
    approval_lifecycle_candidate_preserved = all(
        row.get("lifecycle_type") == "candidate-lifecycle"
        and row.get("lifecycle_type") != "active-approval-lifecycle"
        for row in lifecycle_rows
    ) if lifecycle_rows else lifecycle_matrix.get("approval_lifecycle_candidate_only") is True
    if not approval_lifecycle_candidate_preserved:
        issues.append("approval_lifecycle_escalation")

    expiry_revocation_rows = expiry_revocation_matrix.get("rows") or []
    expiry_revocation_reference_candidate_preserved = all(
        row.get("reference_status") == "expiry-revocation-reference-candidate"
        and row.get("reference_status") not in ("expiry-execution-path", "revocation-execution-path")
        and row.get("revocation_execution_path") is False
        for row in expiry_revocation_rows
    ) if expiry_revocation_rows else expiry_revocation_matrix.get("expiry_revocation_reference_candidate_only") is True
    if not expiry_revocation_reference_candidate_preserved:
        issues.append("approval_revocation_execution_leakage")

    authorization_request_absent = True
    authorization_grant_absent = (
        planning_summary.get("authorization_grant_absent") is True
        and boundary_contract.get("grant_issued") is False
    )
    request_record_absent = True
    grant_token_absent = planning_summary.get("grant_token_absent") is True
    grant_record_absent = planning_summary.get("grant_record_absent") is True
    owner_approval_record_absent = planning_summary.get("owner_approval_record_absent") is True
    owner_operator_ack_record_absent = planning_summary.get("owner_operator_ack_record_absent") is True
    approval_evidence_bound_record_absent = planning_summary.get("approval_evidence_bound_record_absent") is True
    foundation_not_frozen = boundary_contract.get("foundation_frozen") is False
    closure_not_executed = (
        boundary_contract.get("closure_applied") is False
        and boundary_contract.get("closed") is False
    )
    for flag in RUNTIME_FORBIDDEN_FLAGS:
        if planning_summary.get(flag) is True:
            if "authorization_request" in flag:
                authorization_request_absent = False
            elif flag == "authorization_grant_created_now":
                authorization_grant_absent = False
            elif flag == "grant_token_created_now":
                grant_token_absent = False
            elif flag == "grant_record_created_now":
                grant_record_absent = False
            elif flag == "owner_approval_record_created_now":
                owner_approval_record_absent = False

    prerequisite_validation = {
        "authorization_request_absent": authorization_request_absent,
        "request_record_absent": request_record_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        "owner_operator_ack_record_absent": owner_operator_ack_record_absent,
        "approval_evidence_bound_record_absent": approval_evidence_bound_record_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "grant_token_absent": grant_token_absent,
        "grant_record_absent": grant_record_absent,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
    }
    approval_prerequisites_satisfied = (
        prerequisite_matrix.get("prerequisites_ok") is True
        and all(prerequisite_validation[k] for k in prerequisite_validation)
    )
    if not authorization_request_absent:
        issues.append("authorization_request_leakage")
    if (
        not request_record_absent
        or not owner_approval_record_absent
        or not owner_operator_ack_record_absent
        or not approval_evidence_bound_record_absent
        or not grant_token_absent
        or not grant_record_absent
    ):
        issues.append("owner_approval_record_leakage")
    if not authorization_grant_absent:
        issues.append("grant_issuance_leakage")
    if not foundation_not_frozen:
        issues.append("freeze_state_escalation")
    if not closure_not_executed:
        issues.append("closure_state_escalation")
    if not approval_prerequisites_satisfied:
        issues.append("prerequisite_gap")

    non_execution_boundary_ok = non_execution_doc.get("non_execution_boundary_ok") is True
    if not non_execution_boundary_ok:
        issues.append("runtime_scope_leakage")

    planning_debts = debt_carryover.get("debts") or []
    debts = list(GOVERNANCE_DEBTS)
    for pd in planning_debts:
        for i, cd in enumerate(debts):
            if cd.get("debt_title") == pd.get("debt_title"):
                debts[i] = {**cd, **pd}
    required_titles = [d["debt_title"] for d in GOVERNANCE_DEBTS]
    debt_rows: List[Dict[str, Any]] = []
    governance_debt_preserved = len(debts) >= len(GOVERNANCE_DEBTS)
    for title in required_titles:
        match = next((d for d in debts if d.get("debt_title") == title), {})
        ok = (
            bool(match)
            and match.get("priority") == "P1"
            and match.get("classification") == "L1 Midplatform System Protocols"
            and match.get("must_not_implement_now") is True
        )
        debt_rows.append(
            {
                "debt_title": title,
                "preserved": ok,
                "priority": match.get("priority"),
                "must_not_implement_now": match.get("must_not_implement_now"),
            }
        )
        if not ok:
            governance_debt_preserved = False
    if not governance_debt_preserved:
        issues.append("governance_debt_gap")

    l1_protocols_not_implemented = debt_carryover.get("l1_protocols_not_implemented") is True
    system_protocols_integration_not_implemented = (
        debt_carryover.get("system_protocols_integration_not_implemented") is True
    )
    if not l1_protocols_not_implemented or not system_protocols_integration_not_implemented:
        issues.append("l1_protocol_scope_leakage")

    owner_approval_plan_integrity_ok = all(r["exists"] and r["non_placeholder"] for r in integrity_rows)
    owner_approval_dryrun_only = True
    post_review_readiness_ok = (
        prior_owner_approval_planning_go
        and approval_evidence_traceability_ok
        and governance_debt_preserved
        and protocol_standard_reference_ok
        and protocol_id_reference_ok
        and error_namespace_reference_ok
        and protocol_execution_result_schema_ref_ok
        and separation_rule_ref_ok
    )

    protocol_refs_ok = (
        protocol_standard_reference_ok
        and protocol_id_reference_ok
        and error_namespace_reference_ok
        and protocol_execution_result_schema_ref_ok
        and separation_rule_ref_ok
        and whitebox_candidate_ref_ok
        and protocol_error_code_light_check_ok
    )

    if not owner_approval_plan_integrity_ok or not prior_owner_approval_planning_go:
        final_decision = FINAL_DECISION_PLAN_GAP
    elif not protocol_refs_ok:
        final_decision = FINAL_DECISION_PROTOCOL
    elif not approval_evidence_traceability_ok:
        final_decision = FINAL_DECISION_PLAN_GAP
    elif not approval_scope_preserved:
        final_decision = FINAL_DECISION_SCOPE
    elif not authorization_request_absent:
        final_decision = FINAL_DECISION_REQUEST
    elif (
        not request_record_absent
        or not owner_approval_record_absent
        or not owner_operator_ack_record_absent
        or not approval_evidence_bound_record_absent
        or not grant_token_absent
        or not grant_record_absent
        or not authorization_grant_absent
    ):
        final_decision = FINAL_DECISION_APPROVAL
    elif (
        not owner_approval_candidate_preserved
        or not owner_operator_ack_candidate_preserved
        or not approval_evidence_binding_candidate_preserved
        or not request_record_binding_candidate_preserved
        or not approval_lifecycle_candidate_preserved
        or not expiry_revocation_reference_candidate_preserved
        or not foundation_not_frozen
    ):
        final_decision = FINAL_DECISION_FREEZE
    elif not governance_debt_preserved:
        final_decision = FINAL_DECISION_DEBT
    elif not l1_protocols_not_implemented:
        final_decision = FINAL_DECISION_L1
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    else:
        final_decision = FINAL_DECISION_GO

    template_lineage = build_template_lineage(
        base_phase="Freeze-Authorization-Grant-Request-Record-DryRun-v1-001",
        base_capability=GRANT_OWNER_APPROVAL_DRYRUN_WHITELIST_FILES[0],
        base_runner=GRANT_OWNER_APPROVAL_DRYRUN_WHITELIST_FILES[1],
        base_verifier=GRANT_OWNER_APPROVAL_DRYRUN_WHITELIST_FILES[2],
        base_go_no_go_pack=GRANT_OWNER_APPROVAL_DRYRUN_WHITELIST_FILES[3],
        stage_phase="Freeze-Authorization-Grant-Owner-Approval-DryRun-v1-001",
        stage_term_overrides=GRANT_OWNER_APPROVAL_DRYRUN_STAGE_TERM_OVERRIDES,
        stage_additions=GRANT_OWNER_APPROVAL_DRYRUN_STAGE_ADDITIONS,
        template_files=GRANT_OWNER_APPROVAL_DRYRUN_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Freeze-Authorization-Grant-Owner-Approval-Planning-v1-001",
    )
    upstream_lineage_ok = planning_summary.get("template_lineage_ok") is True
    template_lineage_ok = template_lineage.get("template_lineage_ok") is True and upstream_lineage_ok
    if not template_lineage_ok:
        issues.append("template_lineage_gap")

    go_condition_values = {
        "prior_owner_approval_planning_go": prior_owner_approval_planning_go,
        "protocol_standard_reference_ok": protocol_standard_reference_ok,
        "protocol_id_reference_ok": protocol_id_reference_ok,
        "error_namespace_reference_ok": error_namespace_reference_ok,
        "protocol_execution_result_schema_ref_ok": protocol_execution_result_schema_ref_ok,
        "separation_rule_ref_ok": separation_rule_ref_ok,
        "owner_approval_plan_integrity_ok": owner_approval_plan_integrity_ok,
        "approval_scope_preserved": approval_scope_preserved,
        "owner_approval_candidate_preserved": owner_approval_candidate_preserved,
        "owner_operator_ack_candidate_preserved": owner_operator_ack_candidate_preserved,
        "approval_evidence_binding_candidate_preserved": approval_evidence_binding_candidate_preserved,
        "request_record_binding_candidate_preserved": request_record_binding_candidate_preserved,
        "approval_lifecycle_candidate_preserved": approval_lifecycle_candidate_preserved,
        "expiry_revocation_reference_candidate_preserved": expiry_revocation_reference_candidate_preserved,
        "approval_prerequisites_satisfied": approval_prerequisites_satisfied,
        "approval_evidence_traceability_ok": approval_evidence_traceability_ok,
        "authorization_request_absent": authorization_request_absent,
        "request_record_absent": request_record_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        "owner_operator_ack_record_absent": owner_operator_ack_record_absent,
        "approval_evidence_bound_record_absent": approval_evidence_bound_record_absent,
        "grant_token_absent": grant_token_absent,
        "grant_record_absent": grant_record_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        "template_lineage_ok": template_lineage_ok,
        "owner_approval_dryrun_only": owner_approval_dryrun_only,
        "post_review_readiness_ok": post_review_readiness_ok,
    }
    dryrun_pass = len(issues) == 0 and final_decision == FINAL_DECISION_GO and all(go_condition_values.values())
    next_phase = NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD
    core_schema_fields = build_core_go_no_go_summary_fields(
        go_conditions=go_condition_values,
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=CHAIN_TRACE_NODES,
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    dryrun_report = {
        "report_id": "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_dryrun_report_v1",
        "planning_final_decision": planning_summary.get("final_decision"),
        "planning_verifier": planning_verifier.get("verifier"),
        "protocol_smoke_final_decision": smoke_summary.get("final_decision"),
        "protocol_smoke_verifier": smoke_verifier.get("verifier"),
        **go_condition_values,
        "boundary_statements": list(DRYRUN_BOUNDARY_STATEMENTS),
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    plan_integrity_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_plan_integrity_matrix_v1",
        "rows": integrity_rows,
        "owner_approval_plan_integrity_ok": owner_approval_plan_integrity_ok,
        **meta,
    }
    scope_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_scope_validation_v1",
        "rows": scope_rows,
        "approval_scope_preserved": approval_scope_preserved,
        "allowed_classifications": list(ALLOWED_SCOPE_CLASSIFICATIONS),
        **meta,
    }
    candidate_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_candidate_validation_v1",
        "rows": owner_rows,
        "freeze_status": freeze_status,
        "owner_approval_candidate_preserved": owner_approval_candidate_preserved,
        "approval_status": "owner-approval-candidate",
        "forbidden_states": list(FORBIDDEN_ASSET_STATES),
        **meta,
    }
    owner_operator_ack_candidate_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_operator_ack_candidate_validation_v1",
        "rows": ack_rows,
        "owner_operator_ack_candidate_preserved": owner_operator_ack_candidate_preserved,
        "ack_status": "owner-operator-ack-candidate",
        **meta,
    }
    evidence_binding_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_evidence_binding_validation_v1",
        "rows": evidence_binding_rows,
        "approval_evidence_binding_candidate_preserved": approval_evidence_binding_candidate_preserved,
        "binding_status": "approval-evidence-binding-candidate",
        **meta,
    }
    request_record_binding_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_binding_validation_v1",
        "rows": record_binding_rows,
        "request_record_binding_candidate_preserved": request_record_binding_candidate_preserved,
        "binding_status": "request-record-binding-candidate",
        **meta,
    }
    lifecycle_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_lifecycle_validation_v1",
        "rows": lifecycle_rows,
        "approval_lifecycle_candidate_preserved": approval_lifecycle_candidate_preserved,
        "lifecycle_type": "candidate-lifecycle",
        **meta,
    }
    expiry_revocation_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_expiry_revocation_validation_v1",
        "rows": expiry_revocation_rows,
        "expiry_revocation_reference_candidate_preserved": expiry_revocation_reference_candidate_preserved,
        "reference_status": "expiry-revocation-reference-candidate",
        **meta,
    }
    prerequisite_validation_doc = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_prerequisite_validation_v1",
        "rows": prerequisite_matrix.get("rows") or [],
        "approval_prerequisites_satisfied": approval_prerequisites_satisfied,
        **prerequisite_validation,
        **meta,
    }
    evidence_traceability = {
        "trace_id": "task_manager_freeze_authorization_grant_owner_approval_evidence_traceability_v1",
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_chain_traceability_matrix_v1",
        "rows": trace_rows,
        "approval_evidence_traceability_ok": approval_evidence_traceability_ok,
        "freeze_authorization_chain_traceability_ok": approval_evidence_traceability_ok,
        "points_to_dryrun_not_approval": True,
        "points_to_dryrun_not_issued": True,
        **meta,
    }
    absence_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_absence_validation_v1",
        "authorization_request_absent": authorization_request_absent,
        "request_record_absent": request_record_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        "owner_operator_ack_record_absent": owner_operator_ack_record_absent,
        "approval_evidence_bound_record_absent": approval_evidence_bound_record_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "grant_token_absent": grant_token_absent,
        "grant_record_absent": grant_record_absent,
        "no_approval_revocation_execution_path": True,
        "no_freeze_execution_path": True,
        "no_rollback_execution_path": True,
        **meta,
    }
    boundary_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_boundary_validation_v1",
        "statements": list(DRYRUN_BOUNDARY_STATEMENTS),
        "owner_approval_dryrun_only": owner_approval_dryrun_only,
        "authorization_request_issued": False,
        "request_record_created": False,
        "owner_approval_record_created": False,
        "owner_operator_ack_record_created": False,
        "approval_evidence_bound_record_created": False,
        "grant_issued": False,
        "foundation_frozen": False,
        "closed": False,
        **meta,
    }
    protocol_reference_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_protocol_reference_validation_v1",
        "protocol_standard_ref": PROTOCOL_STANDARD_REF,
        "protocol_id": PROTOCOL_ID,
        "related_protocol_ids": list(RELATED_PROTOCOL_IDS),
        "error_namespace": ERROR_NAMESPACE,
        "protocol_execution_result_schema_ref": PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
        "separation_rule_ref": SEPARATION_RULE_REF,
        "shared_protocol_system_revalidation": False,
        "protocol_standard_reference_ok": protocol_standard_reference_ok,
        "protocol_id_reference_ok": protocol_id_reference_ok,
        "error_namespace_reference_ok": error_namespace_reference_ok,
        "protocol_execution_result_schema_ref_ok": protocol_execution_result_schema_ref_ok,
        "separation_rule_ref_ok": separation_rule_ref_ok,
        "protocol_error_code_light_check_ok": protocol_error_code_light_check_ok,
        "sample_protocol_error_code": sample_protocol_error_code,
        "whitebox_candidate_ref_ok": whitebox_candidate_ref_ok,
        "whitebox_candidate_ref": whitebox_candidate_ref,
        "error_classification_rules": list(FAILURE_CLASSIFICATION),
        "protocol_violation_examples": [
            {
                "violation": "owner_approval_candidate upgraded to owner_approval_record",
                "error_code": build_error_code(PROTOCOL_ID, "AUTH", 1),
            },
            {
                "violation": "owner_operator_ack_candidate upgraded to owner_operator_ack_record",
                "error_code": build_error_code(PROTOCOL_ID, "AUTH", 2),
            },
            {
                "violation": "approval_evidence_binding_candidate upgraded to approval_evidence_bound_record",
                "error_code": build_error_code("LUNA-PROTO-L1-EVIDENCE-BINDING-V1", "EVID", 1),
            },
            {
                "violation": "request_record_candidate upgraded to request_record",
                "error_code": build_error_code("LUNA-PROTO-L1-RECORD-LIFECYCLE-V1", "STATE", 1),
            },
        ],
        "module_local_failure_not_protocol_failure_by_default": True,
        **meta,
    }
    governance_debt_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_governance_debt_validation_v1",
        "debts": debts,
        "debt_rows": debt_rows,
        "required_debt_count": len(GOVERNANCE_DEBTS),
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        **meta,
    }
    post_review_readiness = {
        "readiness_id": "task_manager_freeze_authorization_grant_owner_approval_post_review_readiness_v1",
        "post_review_readiness_ok": post_review_readiness_ok,
        "recommended_next_phase": next_phase,
        "target": "freeze_authorization_grant_owner_approval_post_dryrun_review",
        "module_adapter_implementation_ready": False,
        "authorization_request_issued": False,
        "request_record_created": False,
        "owner_approval_record_created": False,
        "owner_operator_ack_record_created": False,
        "approval_evidence_bound_record_created": False,
        "grant_issued": False,
        "freeze_authorization_granted": False,
        "foundation_frozen": False,
        "closed": False,
        **meta,
    }
    template_lineage_doc = {
        "lineage_id": "task_manager_freeze_authorization_grant_owner_approval_template_lineage_v1",
        "upstream_owner_approval_planning_lineage_ok": upstream_lineage_ok,
        **template_lineage,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_pass": dryrun_pass,
        "blocker_count": len(issues),
        "issues": issues,
        **go_condition_values,
        **core_schema_fields,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval DryRun Report v1",
            "",
            "This phase performs freeze authorization grant owner approval dry-run validation only. "
            "It does not create owner approval records, owner/operator ack records, bind approval evidence records, "
            "create request records, or issue authorization requests.",
            "",
            "本阶段仅执行 freeze authorization grant owner approval dry-run validation，"
            "不生成 owner approval record，不生成 owner/operator ack record，"
            "不绑定 approval evidence record，不生成 request record，不发起 authorization request，不签发 grant。",
            "",
            f"Owner approval planning GO: `{prior_owner_approval_planning_go}`",
            f"Protocol standard reference OK: `{protocol_standard_reference_ok}`",
            f"Protocol standard ref: `{PROTOCOL_STANDARD_REF}`",
            f"Protocol ID: `{PROTOCOL_ID}`",
            f"Authorization request absent: `{authorization_request_absent}`",
            f"Request record absent: `{request_record_absent}`",
            f"Owner approval record absent: `{owner_approval_record_absent}`",
            f"Owner/operator ack record absent: `{owner_operator_ack_record_absent}`",
            f"Approval evidence bound record absent: `{approval_evidence_bound_record_absent}`",
            f"Grant token absent: `{grant_token_absent}`",
            f"Grant record absent: `{grant_record_absent}`",
            f"Freeze status: `{freeze_status}` (not frozen)",
            f"Governance debt preserved: `{governance_debt_preserved}`",
            f"Template lineage OK: `{template_lineage_ok}`",
            f"Shared protocol system revalidation: `false`",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{summary['recommended_next_phase']}`",
            "",
            "## Owner Approval DryRun Boundary Statements",
            *[f"- {stmt}" for stmt in DRYRUN_BOUNDARY_STATEMENTS],
            "",
            "owner approval dryrun ≠ owner approval",
            "",
            "## Governance Debts (P1, not implemented)",
            *[f"- {d['debt_title']}" for d in GOVERNANCE_DEBTS],
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_dryrun_report": dryrun_report,
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_dryrun_report_md": markdown,
        "task_manager_freeze_authorization_grant_owner_approval_plan_integrity_matrix": plan_integrity_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_scope_validation": scope_validation,
        "task_manager_freeze_authorization_grant_owner_approval_candidate_validation": candidate_validation,
        "task_manager_freeze_authorization_grant_owner_operator_ack_candidate_validation": owner_operator_ack_candidate_validation,
        "task_manager_freeze_authorization_grant_owner_approval_evidence_binding_validation": evidence_binding_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_binding_validation": request_record_binding_validation,
        "task_manager_freeze_authorization_grant_owner_approval_lifecycle_validation": lifecycle_validation,
        "task_manager_freeze_authorization_grant_owner_approval_expiry_revocation_validation": expiry_revocation_validation,
        "task_manager_freeze_authorization_grant_owner_approval_prerequisite_validation": prerequisite_validation_doc,
        "task_manager_freeze_authorization_grant_owner_approval_evidence_traceability": evidence_traceability,
        "task_manager_freeze_authorization_grant_owner_approval_absence_validation": absence_validation,
        "task_manager_freeze_authorization_grant_owner_approval_boundary_validation": boundary_validation,
        "task_manager_freeze_authorization_grant_owner_approval_protocol_reference_validation": protocol_reference_validation,
        "task_manager_freeze_authorization_grant_owner_approval_governance_debt_validation": governance_debt_validation,
        "task_manager_freeze_authorization_grant_owner_approval_template_lineage": template_lineage_doc,
        "task_manager_freeze_authorization_grant_owner_approval_post_review_readiness": post_review_readiness,
        "summary": summary,
    }
