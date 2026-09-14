# -*- coding: utf-8 -*-
"""Owner/Operator Approval Protocol Post-DryRun Review v1.

Post-dryrun review only: audit dry-run completeness, authorization non-release,
request/grant/window/abort/scope blocks frozen. Does not grant authorization.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.owner_operator_approval_protocol_planning_v1 import (
    EVIDENCE_AUTH_LINKS,
    FORBIDDEN_SHORTCUTS,
    NON_CLAIM_SCENARIOS,
    VERIFIER_CHECKS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Owner-Operator-Approval-Protocol-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "owner_operator_approval_protocol_post_dryrun_review_only"
SOURCE_CHAIN = "owner_operator_approval_protocol_post_dryrun_review_v1"

SOURCE_PHASE = "Phase-Owner-Operator-Approval-Protocol-DryRun-v1-001"
FINAL_DECISION = "OWNER_OPERATOR_APPROVAL_PROTOCOL_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
NEXT_PHASE = "Phase-Owner-Operator-Approval-Protocol-Roadmap-Decision-v1-001"

DRYRUN_ARTIFACTS: Tuple[Tuple[str, str, int], ...] = (
    ("dry-run policy", "owner_operator_approval_protocol_dryrun_policy_v1.json", 0),
    ("planning artifact completeness dry-run", "owner_operator_planning_artifact_completeness_dryrun_v1.json", 13),
    ("owner identity consumption dry-run", "owner_identity_consumption_dryrun_v1.json", 10),
    ("operator acknowledgement consumption dry-run", "operator_acknowledgement_consumption_dryrun_v1.json", 10),
    ("execution window consumption dry-run", "execution_window_consumption_dryrun_v1.json", 12),
    ("abort authority consumption dry-run", "abort_authority_consumption_dryrun_v1.json", 12),
    ("scope boundary acknowledgement consumption dry-run", "scope_boundary_acknowledgement_consumption_dryrun_v1.json", 12),
    ("authorization dependency consumption dry-run", "authorization_dependency_consumption_dryrun_v1.json", 12),
    ("forbidden shortcut dry-run", "owner_operator_forbidden_shortcut_dryrun_v1.json", 12),
    ("evidence authorization link dry-run", "evidence_authorization_link_dryrun_v1.json", 12),
    ("verifier usage dry-run", "owner_operator_verifier_usage_dryrun_v1.json", 12),
    ("non-claims generation dry-run", "owner_operator_non_claims_generation_dryrun_v1.json", 12),
    ("dry-run readiness decision", "owner_operator_approval_protocol_dryrun_readiness_decision_v1.json", 0),
)

OWNER_APPROVAL_REQUEST_TARGETS: Tuple[str, ...] = (
    "owner_approval_request_sent_now",
    "owner_approval_granted_now",
    "owner_identity_satisfied_now",
    "owner_authority_satisfied_now",
    "owner_approval_artifact_generated_now",
    "owner_approval_timestamp_generated_now",
)

OPERATOR_ACK_REQUEST_TARGETS: Tuple[str, ...] = (
    "operator_acknowledgement_request_sent_now",
    "operator_acknowledgement_granted_now",
    "operator_identity_satisfied_now",
    "operator_scope_acknowledged_now",
    "operator_risk_acknowledged_now",
    "operator_acknowledgement_artifact_generated_now",
)

EXECUTION_WINDOW_TARGETS: Tuple[str, ...] = (
    "execution_window_opened_now",
    "window_start_set_now",
    "window_end_set_now",
    "allowed_operations_active_now",
    "forbidden_operations_enforced_now",
    "execution_committed",
)

ABORT_AUTHORITY_TARGETS: Tuple[str, ...] = (
    "abort_authority_confirmed_now",
    "abort_trigger_active_now",
    "abort_notification_rule_active_now",
    "abort_evidence_capture_rule_active_now",
    "abort_rollback_rule_active_now",
    "abort_post_review_rule_active_now",
)

SCOPE_BOUNDARY_TARGETS: Tuple[str, ...] = (
    "scope_confirmation_accepted_now",
    "protected_boundary_acknowledged_now",
    "HR_boundary_acknowledged_now",
    "DnAE_boundary_acknowledged_now",
    "eval_out_boundary_acknowledged_now",
    "rollback_boundary_acknowledged_now",
)

AUTHORIZATION_GRANT_TARGETS: Tuple[str, ...] = (
    "authorization_granted_now",
    "verifier_rerun_authorized_now",
    "evidence_generation_authorized_now",
    "evidence_acceptance_authorized_now",
    "evidence_registry_generation_authorized_now",
    "restore_map_generation_authorized_now",
    "sandbox_creation_authorized_now",
    "branch_creation_authorized_now",
    "rollback_rehearsal_authorized_now",
    "migration_execution_authorized_now",
    "success_claim_authority_confirmed_now",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _review_meta() -> Dict[str, Any]:
    return {
        "post_dryrun_review_only": True,
        "review_only": True,
        "owner_approval_request_sent_now": False,
        "operator_acknowledgement_request_sent_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "abort_authority_confirmed_now": False,
        "scope_confirmation_accepted_now": False,
        "verifier_rerun_authorized_now": False,
        "evidence_generation_authorized_now": False,
        "evidence_acceptance_authorized_now": False,
        "success_claim_authority_confirmed_now": False,
        "authorization_granted_now": False,
        "evidence_generated_now": False,
        "runtime_evidence_generated_now": False,
        "success_evidence_generated_now": False,
        "evidence_accepted_for_success_claim_now": False,
        "success_claim_allowed": False,
        "evidence_chain_canonicalization_executed_now": False,
        "evidence_registry_generated_now": False,
        "success_claim_gate_generated_now": False,
        "boundary_object_registry_generated_now": False,
        "verifier_modified_now": False,
        "phase_template_modified_now": False,
        "automation_implemented_now": False,
        "documentation_auto_sync_executed_now": False,
        "debt_fix_executed_now": False,
        "runtime_invoked": False,
        "execution_committed": False,
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _review_row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_review_meta()}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _row_count(payload: Dict[str, Any]) -> int:
    if "row_count" in payload:
        return int(payload["row_count"])
    rows = payload.get("rows")
    return len(rows) if isinstance(rows, list) else 0


def _load_upstream(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary = _try_read_json(root / "summary.json") if root else None
    verifier = _try_read_json(root / "verifier_report.json") if root else None
    readiness = _try_read_json(
        root / "owner_operator_approval_protocol_dryrun_readiness_decision_v1.json"
    ) if root else None
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for _, filename, _ in DRYRUN_ARTIFACTS:
            payload = _try_read_json(root / filename)
            if payload is None:
                missing.append(filename)
            else:
                art[filename] = payload
    loaded = summary is not None and verifier is not None and readiness is not None and not missing
    return {
        "root": root,
        "loaded": loaded,
        "summary": summary or {},
        "verifier": verifier or {},
        "readiness": readiness or {},
        "artifacts": art,
        "missing": missing,
    }


def _observed_from_summary(target: str, up_summary: Dict[str, Any], artifacts: Dict[str, Any]) -> bool:
    owner_id = artifacts.get("owner_identity_consumption_dryrun_v1.json") or {}
    operator_ack = artifacts.get("operator_acknowledgement_consumption_dryrun_v1.json") or {}
    window = artifacts.get("execution_window_consumption_dryrun_v1.json") or {}
    abort = artifacts.get("abort_authority_consumption_dryrun_v1.json") or {}
    scope = artifacts.get("scope_boundary_acknowledgement_consumption_dryrun_v1.json") or {}

    direct = {
        "owner_approval_request_sent_now": up_summary.get("owner_approval_request_sent_now"),
        "owner_approval_granted_now": up_summary.get("owner_approval_granted_now"),
        "operator_acknowledgement_request_sent_now": up_summary.get("operator_acknowledgement_request_sent_now"),
        "operator_acknowledgement_granted_now": up_summary.get("operator_acknowledgement_granted_now"),
        "execution_window_opened_now": up_summary.get("execution_window_opened_now"),
        "abort_authority_confirmed_now": up_summary.get("abort_authority_confirmed_now"),
        "scope_confirmation_accepted_now": up_summary.get("scope_confirmation_accepted_now"),
        "authorization_granted_now": up_summary.get("authorization_granted_now"),
        "verifier_rerun_authorized_now": up_summary.get("verifier_rerun_authorized_now"),
        "evidence_generation_authorized_now": up_summary.get("evidence_generation_authorized_now"),
        "evidence_acceptance_authorized_now": up_summary.get("evidence_acceptance_authorized_now"),
        "success_claim_authority_confirmed_now": up_summary.get("success_claim_authority_confirmed_now"),
        "execution_committed": up_summary.get("execution_committed"),
    }
    if target in direct:
        return direct[target] is True

    if target == "owner_identity_satisfied_now":
        return any(r.get("satisfied_now") is True for r in (owner_id.get("rows") or []))
    if target == "owner_authority_satisfied_now":
        return any(r.get("approval_granted_now") is True for r in (owner_id.get("rows") or []))
    if target == "owner_approval_artifact_generated_now":
        return up_summary.get("evidence_generated_now") is True
    if target == "owner_approval_timestamp_generated_now":
        return False

    if target == "operator_identity_satisfied_now":
        return any(r.get("acknowledged_now") is True for r in (operator_ack.get("rows") or []))
    if target == "operator_scope_acknowledged_now":
        row = next((r for r in (operator_ack.get("rows") or []) if r.get("ack_component") == "operator scope acknowledgement"), {})
        return row.get("acknowledged_now") is True or row.get("operator_acknowledgement_granted_now") is True
    if target == "operator_risk_acknowledged_now":
        row = next((r for r in (operator_ack.get("rows") or []) if r.get("ack_component") == "operator risk acknowledgement"), {})
        return row.get("acknowledged_now") is True
    if target == "operator_acknowledgement_artifact_generated_now":
        return up_summary.get("evidence_generated_now") is True

    if target == "window_start_set_now":
        row = next((r for r in (window.get("rows") or []) if r.get("window_component") == "start time"), {})
        return row.get("opened_now") is True or row.get("execution_window_opened_now") is True
    if target == "window_end_set_now":
        row = next((r for r in (window.get("rows") or []) if r.get("window_component") == "end time"), {})
        return row.get("opened_now") is True or row.get("execution_window_opened_now") is True
    if target == "allowed_operations_active_now":
        row = next((r for r in (window.get("rows") or []) if r.get("window_component") == "allowed operations"), {})
        return row.get("execution_window_opened_now") is True
    if target == "forbidden_operations_enforced_now":
        return up_summary.get("execution_window_opened_now") is True

    if target == "abort_trigger_active_now":
        return any(r.get("confirmed_now") is True for r in (abort.get("rows") or []))
    if target == "abort_notification_rule_active_now":
        row = next((r for r in (abort.get("rows") or []) if "notification" in str(r.get("abort_component", ""))), {})
        return row.get("abort_authority_confirmed_now") is True
    if target == "abort_evidence_capture_rule_active_now":
        row = next((r for r in (abort.get("rows") or []) if "evidence capture" in str(r.get("abort_component", ""))), {})
        return row.get("abort_authority_confirmed_now") is True
    if target == "abort_rollback_rule_active_now":
        row = next((r for r in (abort.get("rows") or []) if "rollback" in str(r.get("abort_component", ""))), {})
        return row.get("abort_authority_confirmed_now") is True
    if target == "abort_post_review_rule_active_now":
        row = next((r for r in (abort.get("rows") or []) if "post-review" in str(r.get("abort_component", ""))), {})
        return row.get("abort_authority_confirmed_now") is True

    if target == "protected_boundary_acknowledged_now":
        row = next((r for r in (scope.get("rows") or []) if r.get("scope_boundary_component") == "protected asset boundary"), {})
        return row.get("acknowledged_now") is True or row.get("scope_confirmation_accepted_now") is True
    if target == "HR_boundary_acknowledged_now":
        row = next((r for r in (scope.get("rows") or []) if r.get("scope_boundary_component") == "HR boundary"), {})
        return row.get("acknowledged_now") is True
    if target == "DnAE_boundary_acknowledged_now":
        row = next((r for r in (scope.get("rows") or []) if r.get("scope_boundary_component") == "DnAE boundary"), {})
        return row.get("acknowledged_now") is True
    if target == "eval_out_boundary_acknowledged_now":
        row = next((r for r in (scope.get("rows") or []) if r.get("scope_boundary_component") == "eval_out boundary"), {})
        return row.get("acknowledged_now") is True
    if target == "rollback_boundary_acknowledged_now":
        row = next((r for r in (scope.get("rows") or []) if r.get("scope_boundary_component") == "rollback boundary"), {})
        return row.get("acknowledged_now") is True

    auth_dep = artifacts.get("authorization_dependency_consumption_dryrun_v1.json") or {}
    if target == "evidence_registry_generation_authorized_now":
        row = next((r for r in (auth_dep.get("rows") or []) if "registry" in str(r.get("authorization_dependency", ""))), {})
        return row.get("authorized_now") is True
    if target == "restore_map_generation_authorized_now":
        row = next((r for r in (auth_dep.get("rows") or []) if "restore map" in str(r.get("authorization_dependency", ""))), {})
        return row.get("authorized_now") is True
    if target == "sandbox_creation_authorized_now":
        row = next((r for r in (auth_dep.get("rows") or []) if "sandbox" in str(r.get("authorization_dependency", ""))), {})
        return row.get("authorized_now") is True
    if target == "branch_creation_authorized_now":
        row = next((r for r in (auth_dep.get("rows") or []) if "branch" in str(r.get("authorization_dependency", ""))), {})
        return row.get("authorized_now") is True
    if target == "rollback_rehearsal_authorized_now":
        row = next((r for r in (auth_dep.get("rows") or []) if "rollback" in str(r.get("authorization_dependency", ""))), {})
        return row.get("authorized_now") is True
    if target == "migration_execution_authorized_now":
        row = next((r for r in (auth_dep.get("rows") or []) if "migration" in str(r.get("authorization_dependency", ""))), {})
        return row.get("authorized_now") is True

    return False


def _build_block_review(
    targets: Tuple[str, ...],
    up_summary: Dict[str, Any],
    artifacts: Dict[str, Any],
    *,
    target_key: str = "review_target",
) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for target in targets:
        obs = _observed_from_summary(target, up_summary, artifacts)
        violation = obs is True
        review_pass = not violation
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                **{
                    target_key: target,
                    "expected_value": False,
                    "observed_value": obs,
                    "violation_detected": violation,
                    "review_pass": review_pass,
                    "review_notes": "blocked" if review_pass else "authorization release detected",
                }
            )
        )
    return rows, all_pass


def _build_completeness_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for name, filename, min_count in DRYRUN_ARTIFACTS:
        payload = artifacts.get(filename)
        observed = payload is not None
        count = _row_count(payload) if isinstance(payload, dict) else 0
        schema_ok = observed and isinstance(payload, dict)
        count_ok = min_count == 0 or count >= min_count
        semantic_ok = schema_ok and count_ok
        if isinstance(payload, dict) and "all_pass" in payload:
            semantic_ok = semantic_ok and payload.get("all_pass") is True
        review_pass = observed and schema_ok and count_ok and semantic_ok
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                artifact_name=name,
                expected=True,
                observed=observed,
                schema_minimum_pass=schema_ok,
                count_requirement_pass=count_ok,
                semantic_requirement_pass=semantic_ok,
                review_status="pass" if review_pass else "fail",
                review_notes=f"count={count} min={min_count}",
            )
        )
    return rows, all_pass


def _build_evidence_link_block_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    el = artifacts.get("evidence_authorization_link_dryrun_v1.json") or {}
    el_by = {r.get("evidence_authorization_link"): r for r in (el.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for link, _auth in EVIDENCE_AUTH_LINKS:
        e = el_by.get(link, {})
        review_pass = (
            e.get("authorized_now") is False
            and e.get("evidence_generated_now") is False
            and e.get("success_claim_allowed_now", False) is False
            and e.get("simulated_link_check") is True
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                evidence_authorization_link=link,
                authorized_now=False,
                evidence_generated_now=False,
                success_claim_allowed_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def up_summary_authorization_not_released(row: Dict[str, Any]) -> bool:
    return row.get("enforced_now") is not True


def _build_forbidden_shortcut_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    fs = artifacts.get("owner_operator_forbidden_shortcut_dryrun_v1.json") or {}
    fs_by = {r.get("forbidden_shortcut"): r for r in (fs.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for shortcut, _affected, _nc, _sev in FORBIDDEN_SHORTCUTS:
        f = fs_by.get(shortcut, {})
        review_pass = (
            f.get("simulated_check") is True
            and f.get("enforced_now") is False
            and f.get("verifier_modified_now") is False
            and up_summary_authorization_not_released(f)
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                forbidden_shortcut=shortcut,
                simulated_check_observed=f.get("simulated_check") is True,
                enforced_now=False,
                verifier_modified_now=False,
                authorization_released_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_verifier_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    vu = artifacts.get("owner_operator_verifier_usage_dryrun_v1.json") or {}
    vu_by = {r.get("verifier_check_id"): r for r in (vu.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for vid, name, phases, fields, fail, sev in VERIFIER_CHECKS:
        v = vu_by.get(vid, {})
        review_pass = (
            v.get("simulated_verifier_consumption") is True
            and v.get("verifier_modified_now") is False
            and v.get("enforced_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                verifier_check_id=vid,
                check_name=v.get("check_name") or name,
                simulated_verifier_consumption=v.get("simulated_verifier_consumption") is True,
                verifier_modified_now=False,
                enforced_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_non_claims_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    nc = artifacts.get("owner_operator_non_claims_generation_dryrun_v1.json") or {}
    nc_by = {r.get("scenario"): r for r in (nc.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for scenario, non_claim in NON_CLAIM_SCENARIOS:
        n = nc_by.get(scenario, {})
        review_pass = (
            bool(n.get("required_non_claim"))
            and n.get("simulated_generation") is True
            and n.get("generated_now") is False
            and n.get("template_modified_now", n.get("phase_template_modified_now")) is False
            and n.get("documentation_auto_sync_executed_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                scenario=scenario,
                required_non_claim=n.get("required_non_claim") or non_claim,
                simulated_generation=n.get("simulated_generation") is True,
                generated_now=False,
                template_modified_now=False,
                documentation_auto_sync_executed_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def run_owner_operator_approval_protocol_post_dryrun_review_v1(
    *,
    owner_operator_approval_protocol_dryrun_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(owner_operator_approval_protocol_dryrun_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    artifacts = upstream["artifacts"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream dryrun verifier not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok not true")
    if up_readiness.get("ready_for_owner_operator_approval_protocol_post_dryrun_review") is not True:
        blockers.append("not ready_for_owner_operator_approval_protocol_post_dryrun_review")
    if up_summary.get("owner_operator_protocol_dryrun_only") is not True:
        blockers.append("upstream owner_operator_protocol_dryrun_only not true")
    if up_summary.get("simulated") is not True:
        blockers.append("upstream simulated not true")
    for flag in (
        "owner_approval_request_sent_now",
        "operator_acknowledgement_request_sent_now",
        "owner_approval_granted_now",
        "operator_acknowledgement_granted_now",
        "execution_window_opened_now",
        "abort_authority_confirmed_now",
        "scope_confirmation_accepted_now",
        "verifier_rerun_authorized_now",
        "evidence_generation_authorized_now",
        "evidence_acceptance_authorized_now",
        "success_claim_authority_confirmed_now",
        "authorization_granted_now",
        "evidence_generated_now",
        "success_claim_allowed",
    ):
        if up_summary.get(flag) is not False:
            blockers.append(f"upstream {flag} must be false")
    for flag in (
        "ready_for_owner_approval_request",
        "ready_for_operator_acknowledgement_request",
        "ready_for_owner_approval_grant",
        "ready_for_operator_acknowledgement_grant",
        "ready_for_execution_window_opening",
        "ready_for_abort_authority_confirmation",
        "ready_for_scope_confirmation_acceptance",
        "ready_for_evidence_generation_authorization",
        "ready_for_verifier_rerun_authorization",
        "ready_for_success_claim_authority_confirmation",
        "ready_for_real_rollback_rehearsal_execution",
    ):
        if up_readiness.get(flag) is not False:
            blockers.append(f"upstream readiness {flag} must remain false")
    if up_summary.get("real_migration_execution_allowed") is not False:
        blockers.append("real_migration_execution_allowed must be false")
    if up_summary.get("batch_arming_allowed") is not False:
        blockers.append("batch_arming_allowed must be false")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("governance_constraints_ref mismatch")

    owner_id = artifacts.get("owner_identity_consumption_dryrun_v1.json") or {}
    auth_dep = artifacts.get("authorization_dependency_consumption_dryrun_v1.json") or {}
    evidence_link = artifacts.get("evidence_authorization_link_dryrun_v1.json") or {}
    if any(r.get("satisfied_now") is True for r in (owner_id.get("rows") or [])):
        blockers.append("owner identity satisfied_now must remain false")
    if any(r.get("authorized_now") is True for r in (auth_dep.get("rows") or [])):
        blockers.append("authorization dependency authorized_now must remain false")
    if any(r.get("success_claim_allowed_now") is True for r in (evidence_link.get("rows") or [])):
        blockers.append("evidence link success_claim_allowed_now must remain false")

    comp_rows, comp_pass = _build_completeness_review(artifacts)
    owner_req_rows, owner_req_pass = _build_block_review(
        OWNER_APPROVAL_REQUEST_TARGETS, up_summary, artifacts
    )
    operator_req_rows, operator_req_pass = _build_block_review(
        OPERATOR_ACK_REQUEST_TARGETS, up_summary, artifacts
    )
    window_rows, window_pass = _build_block_review(
        EXECUTION_WINDOW_TARGETS, up_summary, artifacts
    )
    abort_rows, abort_pass = _build_block_review(
        ABORT_AUTHORITY_TARGETS, up_summary, artifacts
    )
    scope_rows, scope_pass = _build_block_review(
        SCOPE_BOUNDARY_TARGETS, up_summary, artifacts
    )
    auth_rows, auth_pass = _build_block_review(
        AUTHORIZATION_GRANT_TARGETS, up_summary, artifacts, target_key="authorization_target"
    )
    evidence_rows, evidence_pass = _build_evidence_link_block_review(artifacts)
    shortcut_rows, shortcut_pass = _build_forbidden_shortcut_review(artifacts)
    vu_rows, vu_pass = _build_verifier_review(artifacts)
    nc_rows, nc_pass = _build_non_claims_review(artifacts)

    review_pass = (
        comp_pass
        and owner_req_pass
        and operator_req_pass
        and window_pass
        and abort_pass
        and scope_pass
        and auth_pass
        and evidence_pass
        and shortcut_pass
        and vu_pass
        and nc_pass
        and not blockers
    )
    boundary_ok = review_pass

    owner_operator_post_dryrun_review_policy = _review_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_owner_operator_approval_protocol_post_dryrun_review_observed=up_readiness.get(
            "ready_for_owner_operator_approval_protocol_post_dryrun_review"
        )
        is True,
    )

    owner_operator_dryrun_completeness_review = {
        "rows": comp_rows,
        "row_count": len(comp_rows),
        "all_pass": comp_pass,
        **_review_meta(),
    }
    owner_approval_request_block_review = {
        "rows": owner_req_rows,
        "row_count": len(owner_req_rows),
        "all_pass": owner_req_pass,
        **_review_meta(),
    }
    operator_acknowledgement_request_block_review = {
        "rows": operator_req_rows,
        "row_count": len(operator_req_rows),
        "all_pass": operator_req_pass,
        **_review_meta(),
    }
    execution_window_block_review = {
        "rows": window_rows,
        "row_count": len(window_rows),
        "all_pass": window_pass,
        **_review_meta(),
    }
    abort_authority_block_review = {
        "rows": abort_rows,
        "row_count": len(abort_rows),
        "all_pass": abort_pass,
        **_review_meta(),
    }
    scope_boundary_acknowledgement_block_review = {
        "rows": scope_rows,
        "row_count": len(scope_rows),
        "all_pass": scope_pass,
        **_review_meta(),
    }
    authorization_grant_block_review = {
        "rows": auth_rows,
        "row_count": len(auth_rows),
        "all_pass": auth_pass,
        **_review_meta(),
    }
    evidence_authorization_link_block_review = {
        "rows": evidence_rows,
        "row_count": len(evidence_rows),
        "all_pass": evidence_pass,
        **_review_meta(),
    }
    owner_operator_forbidden_shortcut_review = {
        "rows": shortcut_rows,
        "row_count": len(shortcut_rows),
        "all_pass": shortcut_pass,
        **_review_meta(),
    }
    owner_operator_verifier_non_modification_review = {
        "rows": vu_rows,
        "row_count": len(vu_rows),
        "all_pass": vu_pass,
        **_review_meta(),
    }
    owner_operator_non_claims_non_write_review = {
        "rows": nc_rows,
        "row_count": len(nc_rows),
        "all_pass": nc_pass,
        **_review_meta(),
    }

    owner_operator_post_dryrun_review_readiness_decision = {
        "ready_for_owner_operator_approval_protocol_roadmap_decision": boundary_ok,
        "ready_for_owner_approval_request": False,
        "ready_for_operator_acknowledgement_request": False,
        "ready_for_owner_approval_grant": False,
        "ready_for_operator_acknowledgement_grant": False,
        "ready_for_execution_window_opening": False,
        "ready_for_abort_authority_confirmation": False,
        "ready_for_scope_confirmation_acceptance": False,
        "ready_for_evidence_generation_authorization": False,
        "ready_for_verifier_rerun_authorization": False,
        "ready_for_success_claim_authority_confirmation": False,
        "ready_for_evidence_generation": False,
        "ready_for_success_claim_allowance": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "post_dryrun_review_completed": boundary_ok,
        "dryrun_completeness_review_pass": comp_pass,
        "owner_approval_request_block_review_pass": owner_req_pass,
        "operator_acknowledgement_request_block_review_pass": operator_req_pass,
        "execution_window_block_review_pass": window_pass,
        "abort_authority_block_review_pass": abort_pass,
        "scope_boundary_acknowledgement_block_review_pass": scope_pass,
        "authorization_grant_block_review_pass": auth_pass,
        "evidence_authorization_link_block_review_pass": evidence_pass,
        "forbidden_shortcut_review_pass": shortcut_pass,
        "verifier_non_modification_review_pass": vu_pass,
        "non_claims_non_write_review_pass": nc_pass,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "authorization_granted_now": False,
        "evidence_generated_now": False,
        "success_claim_allowed": False,
        "final_decision": FINAL_DECISION if boundary_ok else "OWNER_OPERATOR_APPROVAL_PROTOCOL_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "owner_operator_approval_protocol_dryrun_input_loaded": upstream["loaded"],
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "OWNER_OPERATOR_APPROVAL_PROTOCOL_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    return {
        "summary": summary,
        "owner_operator_post_dryrun_review_policy": owner_operator_post_dryrun_review_policy,
        "owner_operator_dryrun_completeness_review": owner_operator_dryrun_completeness_review,
        "owner_approval_request_block_review": owner_approval_request_block_review,
        "operator_acknowledgement_request_block_review": operator_acknowledgement_request_block_review,
        "execution_window_block_review": execution_window_block_review,
        "abort_authority_block_review": abort_authority_block_review,
        "scope_boundary_acknowledgement_block_review": scope_boundary_acknowledgement_block_review,
        "authorization_grant_block_review": authorization_grant_block_review,
        "evidence_authorization_link_block_review": evidence_authorization_link_block_review,
        "owner_operator_forbidden_shortcut_review": owner_operator_forbidden_shortcut_review,
        "owner_operator_verifier_non_modification_review": owner_operator_verifier_non_modification_review,
        "owner_operator_non_claims_non_write_review": owner_operator_non_claims_non_write_review,
        "owner_operator_post_dryrun_review_readiness_decision": owner_operator_post_dryrun_review_readiness_decision,
    }
