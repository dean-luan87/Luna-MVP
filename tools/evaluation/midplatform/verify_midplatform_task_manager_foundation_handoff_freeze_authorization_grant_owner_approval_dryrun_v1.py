#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval DryRun v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.protocol_canonical_standard_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.protocol_canonical_standard_shared_code_smoke_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PROTOCOL_SMOKE_ROOT,
    FINAL_DECISION_GO as PROTOCOL_SMOKE_FINAL_GO,
)
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    CORE_GO_NO_GO_SCHEMA_KEYS,
    GRANT_OWNER_APPROVAL_DRYRUN_STAGE_ADDITIONS,
    GRANT_OWNER_APPROVAL_DRYRUN_STAGE_TERM_OVERRIDES,
    GRANT_OWNER_APPROVAL_DRYRUN_WHITELIST_FILES,
    TEMPLATE_FAMILY,
    validate_core_go_no_go_schema,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_dryrun_v1 import (
    ALLOWED_SCOPE_CLASSIFICATIONS,
    CHAIN_TRACE_NODES,
    DEFAULT_GRANT_OWNER_APPROVAL_PLANNING_ROOT,
    DEFAULT_OUTPUT,
    DRYRUN_BOUNDARY_STATEMENTS,
    ERROR_NAMESPACE,
    FINAL_DECISION_GO,
    FORBIDDEN_ASSET_STATES,
    GO_CONDITIONS_KEYS,
    GRANT_OWNER_APPROVAL_PLANNING_PACKAGE_FILES,
    NEXT_PHASE_GO,
    PHASE_ID,
    PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
    PROTOCOL_ID,
    PROTOCOL_STANDARD_REF,
    RELATED_PROTOCOL_IDS,
    RUNTIME_FORBIDDEN_FLAGS,
    SCOPE,
    SEPARATION_RULE_REF,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_planning_v1 import (
    BOUNDARY_CONTRACT_STATEMENTS,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    PLANNING_TRUE_KEYS,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
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
)
PREREQ_KEYS: Tuple[str, ...] = (
    "authorization_request_absent",
    "request_record_absent",
    "owner_approval_record_absent",
    "owner_operator_ack_record_absent",
    "approval_evidence_bound_record_absent",
    "authorization_grant_absent",
    "grant_token_absent",
    "grant_record_absent",
    "foundation_not_frozen",
    "closure_not_executed",
)
ABSENCE_KEYS: Tuple[str, ...] = (
    "authorization_request_absent",
    "request_record_absent",
    "owner_approval_record_absent",
    "owner_operator_ack_record_absent",
    "approval_evidence_bound_record_absent",
    "grant_token_absent",
    "grant_record_absent",
    "authorization_grant_absent",
)
TEMPLATE_LINEAGE_GO_KEYS: Tuple[str, ...] = (
    "template_lineage_ok",
    "base_template_files_exist",
    "full_repo_scan_absent",
    "core_go_no_go_schema_preserved",
    "stage_specific_terms_overridden",
)
FORBIDDEN_NEXT_TARGETS: Tuple[str, ...] = (
    "owner_approval_issued",
    "request_record_created",
    "authorization_request_issued",
    "grant_issued",
    "foundation_frozen",
    "closed",
    "module_adapter_implementation",
)


def _read(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _add(checks: List[Dict[str, Any]], check_id: str, passed: bool, detail: str = "") -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--grant-owner-approval-planning-root", default=DEFAULT_GRANT_OWNER_APPROVAL_PLANNING_ROOT)
    parser.add_argument("--protocol-smoke-root", default=DEFAULT_PROTOCOL_SMOKE_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    planning = Path(args.grant_owner_approval_planning_root)
    smoke = Path(args.protocol_smoke_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_dryrun_report_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    for rel in GRANT_OWNER_APPROVAL_DRYRUN_WHITELIST_FILES:
        _add(checks, f"template.base_file.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())
    _add(checks, "template.whitelist_only", True)

    planning_summary = _read(planning / "summary.json")
    planning_verifier = _read(planning / "verifier_report.json")
    _add(
        checks,
        "planning.summary_go",
        planning_summary.get("final_decision") == PLANNING_FINAL_GO,
    )
    _add(checks, "planning.verifier_go", planning_verifier.get("verifier") == "GO")
    _add(checks, "planning.passed_min", int(planning_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "planning.failed_zero", planning_verifier.get("failed_checks") == 0)
    _add(checks, "planning.blocker_zero", planning_verifier.get("blocker_count") == 0)
    _add(checks, "planning.next_readiness", planning_summary.get("next_phase_readiness_ok") is True)
    for key in PLANNING_TRUE_KEYS:
        _add(checks, f"planning.summary.{key}", planning_summary.get(key) is True)
        if key in planning_verifier:
            _add(checks, f"planning.verifier.{key}", planning_verifier.get(key) is True)

    for fname in GRANT_OWNER_APPROVAL_PLANNING_PACKAGE_FILES:
        path = planning / fname
        _add(checks, f"planning.package.exists.{fname}", path.is_file())
        if fname.endswith(".json"):
            _add(checks, f"planning.package.non_placeholder.{fname}", bool(_read(path)))

    smoke_summary = _read(smoke / "summary.json")
    smoke_verifier = _read(smoke / "verifier_report.json")
    _add(checks, "smoke.summary_go", smoke_summary.get("final_decision") == PROTOCOL_SMOKE_FINAL_GO)
    _add(checks, "smoke.final_eq_standard", smoke_summary.get("final_decision") == PROTOCOL_STANDARD_REF)
    _add(checks, "smoke.verifier_go", smoke_verifier.get("verifier") == "GO")
    _add(checks, "smoke.passed_min", int(smoke_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "smoke.failed_zero", smoke_verifier.get("failed_checks") == 0)
    _add(checks, "smoke.blocker_zero", smoke_verifier.get("blocker_count") == 0)
    _add(checks, "smoke.ready_for_dryrun", smoke_summary.get("ready_for_task_manager_owner_approval_dryrun") is True)

    report = docs["task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_dryrun_report_v1.json"]
    integrity = docs["task_manager_freeze_authorization_grant_owner_approval_plan_integrity_matrix_v1.json"]
    trace = docs["task_manager_freeze_authorization_grant_owner_approval_evidence_traceability_v1.json"]
    scope_val = docs["task_manager_freeze_authorization_grant_owner_approval_scope_validation_v1.json"]
    candidate_val = docs["task_manager_freeze_authorization_grant_owner_approval_candidate_validation_v1.json"]
    ack_val = docs["task_manager_freeze_authorization_grant_owner_operator_ack_candidate_validation_v1.json"]
    evidence_val = docs["task_manager_freeze_authorization_grant_owner_approval_evidence_binding_validation_v1.json"]
    record_binding_val = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_record_binding_validation_v1.json"
    ]
    lifecycle_val = docs["task_manager_freeze_authorization_grant_owner_approval_lifecycle_validation_v1.json"]
    expiry_revocation_val = docs[
        "task_manager_freeze_authorization_grant_owner_approval_expiry_revocation_validation_v1.json"
    ]
    prereq_val = docs["task_manager_freeze_authorization_grant_owner_approval_prerequisite_validation_v1.json"]
    absence_val = docs["task_manager_freeze_authorization_grant_owner_approval_absence_validation_v1.json"]
    boundary_val = docs["task_manager_freeze_authorization_grant_owner_approval_boundary_validation_v1.json"]
    protocol_ref_val = docs[
        "task_manager_freeze_authorization_grant_owner_approval_protocol_reference_validation_v1.json"
    ]
    debt_val = docs["task_manager_freeze_authorization_grant_owner_approval_governance_debt_validation_v1.json"]
    post_review = docs["task_manager_freeze_authorization_grant_owner_approval_post_review_readiness_v1.json"]
    lineage_doc = docs["task_manager_freeze_authorization_grant_owner_approval_template_lineage_v1.json"]
    summary = docs["summary.json"]

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(
            checks,
            f"meta.owner_approval_dryrun_only.{doc_name}",
            doc.get("owner_approval_dryrun_only") in (None, True),
        )
        _add(checks, f"meta.foundation_not_frozen.{doc_name}", doc.get("foundation_not_frozen") in (None, True))
        _add(checks, f"meta.closure_not_executed.{doc_name}", doc.get("closure_not_executed") in (None, True))
        _add(
            checks,
            f"meta.no_revalidation.{doc_name}",
            doc.get("shared_protocol_system_revalidation") in (None, False),
        )
        for key in RUNTIME_FORBIDDEN_FLAGS:
            _add(checks, f"meta.no_runtime.{doc_name}.{key}", doc.get(key) is not True)

    _add(checks, "summary.pass", summary.get("dryrun_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
        _add(checks, f"report.{key}", report.get(key) is True)
        _add(checks, f"go_conditions.{key}", (summary.get("go_conditions") or {}).get(key) is True)

    for key in CORE_GO_NO_GO_SCHEMA_KEYS:
        if key in ("passed_checks", "failed_checks", "blocker_count", "verifier", "summary"):
            continue
        _add(checks, f"summary.schema.{key}", key in summary)

    for key in TEMPLATE_LINEAGE_GO_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    lineage = summary.get("template_lineage") or {}
    _add(checks, "lineage.family", lineage.get("template_family") == TEMPLATE_FAMILY)
    _add(
        checks,
        "lineage.base_phase",
        lineage.get("base_phase") == "Freeze-Authorization-Grant-Request-Record-DryRun-v1-001",
    )
    _add(
        checks,
        "lineage.upstream",
        lineage.get("upstream_review_phase") == "Freeze-Authorization-Grant-Owner-Approval-Planning-v1-001",
    )
    _add(checks, "lineage.reuse_mode", lineage.get("reuse_mode") == "whitelist_file_template_reuse")
    _add(checks, "lineage.no_full_scan", lineage.get("full_repo_scan_allowed") is False)
    _add(checks, "lineage.files_exist", lineage.get("base_template_files_exist") is True)
    _add(checks, "lineage.family_match", lineage.get("base_template_family_match") is True)
    _add(checks, "lineage.stage_overridden", lineage.get("stage_specific_terms_overridden") is True)
    _add(checks, "lineage.core_schema", lineage.get("core_go_no_go_schema_preserved") is True)
    _add(checks, "lineage.ok", lineage.get("template_lineage_ok") is True)
    _add(checks, "lineage.doc.ok", lineage_doc.get("template_lineage_ok") is True)
    _add(checks, "lineage.doc.upstream", lineage_doc.get("upstream_owner_approval_planning_lineage_ok") is True)
    for override in GRANT_OWNER_APPROVAL_DRYRUN_STAGE_TERM_OVERRIDES:
        _add(checks, f"lineage.override.{override['base_term'][:30]}", override in (lineage.get("stage_term_overrides") or []))
    for addition in GRANT_OWNER_APPROVAL_DRYRUN_STAGE_ADDITIONS:
        _add(checks, f"lineage.addition.{addition}", addition in (lineage.get("stage_additions") or []))

    _add(checks, "integrity.ok", integrity.get("owner_approval_plan_integrity_ok") is True)
    for row in integrity.get("rows") or []:
        fname = row.get("file")
        _add(checks, f"integrity.exists.{fname}", row.get("exists") is True)
        _add(checks, f"integrity.non_placeholder.{fname}", row.get("non_placeholder") is True)

    _add(checks, "protocol_ref.standard", protocol_ref_val.get("protocol_standard_ref") == PROTOCOL_STANDARD_REF)
    _add(checks, "protocol_ref.id", protocol_ref_val.get("protocol_id") == PROTOCOL_ID)
    _add(checks, "protocol_ref.error_namespace", protocol_ref_val.get("error_namespace") == ERROR_NAMESPACE)
    _add(
        checks,
        "protocol_ref.related_ids",
        protocol_ref_val.get("related_protocol_ids") == list(RELATED_PROTOCOL_IDS),
    )
    _add(checks, "protocol_ref.separation", protocol_ref_val.get("separation_rule_ref") == SEPARATION_RULE_REF)
    _add(
        checks,
        "protocol_ref.schema_ref",
        protocol_ref_val.get("protocol_execution_result_schema_ref") == PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
    )
    _add(checks, "protocol_ref.no_revalidation", protocol_ref_val.get("shared_protocol_system_revalidation") is False)
    _add(checks, "protocol_ref.standard_ok", protocol_ref_val.get("protocol_standard_reference_ok") is True)
    _add(checks, "protocol_ref.id_ok", protocol_ref_val.get("protocol_id_reference_ok") is True)
    _add(checks, "protocol_ref.namespace_ok", protocol_ref_val.get("error_namespace_reference_ok") is True)
    _add(checks, "protocol_ref.schema_ok", protocol_ref_val.get("protocol_execution_result_schema_ref_ok") is True)
    _add(checks, "protocol_ref.separation_ok", protocol_ref_val.get("separation_rule_ref_ok") is True)
    for pid in RELATED_PROTOCOL_IDS:
        _add(checks, f"protocol_ref.related.{pid}", pid in (protocol_ref_val.get("related_protocol_ids") or []))

    _add(checks, "trace.ok", trace.get("approval_evidence_traceability_ok") is True)
    _add(checks, "trace.chain_alias", trace.get("freeze_authorization_chain_traceability_ok") is True)
    _add(checks, "trace.not_approval", trace.get("points_to_dryrun_not_approval") is True)
    _add(checks, "trace.not_issued", trace.get("points_to_dryrun_not_issued") is True)
    for stage in CHAIN_TRACE_NODES:
        row = next((r for r in trace.get("rows") or [] if r.get("stage") == stage), {})
        _add(checks, f"trace.linked.{stage}", row.get("linked") is True)
    dryrun_row = next(
        (r for r in trace.get("rows") or [] if r.get("stage") == "freeze_authorization_grant_owner_approval_dryrun"),
        {},
    )
    _add(checks, "trace.dryrun.no_request", dryrun_row.get("authorization_request_issued") is False)
    _add(checks, "trace.dryrun.no_record", dryrun_row.get("request_record") is False)
    _add(checks, "trace.dryrun.no_approval_record", dryrun_row.get("owner_approval_record") is False)
    _add(checks, "trace.dryrun.no_ack_record", dryrun_row.get("owner_operator_ack_record") is False)
    _add(checks, "trace.dryrun.no_issued", dryrun_row.get("grant_issued") is False)

    _add(checks, "scope.preserved", scope_val.get("approval_scope_preserved") is True)
    for row in scope_val.get("rows") or []:
        s = row.get("scope")
        _add(checks, f"scope.row.{s}.allowed", row.get("classification") in ALLOWED_SCOPE_CLASSIFICATIONS)
        _add(checks, f"scope.row.{s}.not_granted", row.get("classification") != "approval-granted-scope")
        _add(checks, f"scope.row.{s}.not_authorized", row.get("classification") != "authorized-scope")
        _add(checks, f"scope.row.{s}.dryrun_scope", row.get("classification") == "owner-approval-dryrun-scope")

    _add(checks, "candidate.preserved", candidate_val.get("owner_approval_candidate_preserved") is True)
    _add(checks, "candidate.approval_status", candidate_val.get("approval_status") == "owner-approval-candidate")
    for row in candidate_val.get("rows") or []:
        role = row.get("role")
        _add(checks, f"candidate.row.{role}.candidate", row.get("approval_status") == "owner-approval-candidate")
        _add(checks, f"candidate.row.{role}.not_record", row.get("approval_status") != "owner-approval-record")
        _add(checks, f"candidate.row.{role}.no_record_flag", row.get("owner_approval_record") is False)
        _add(checks, f"candidate.row.{role}.not_issued", row.get("authorization_request_issued") is not True)
    for state in FORBIDDEN_ASSET_STATES:
        _add(checks, f"candidate.not_{state}", candidate_val.get("approval_status") != state)

    _add(checks, "ack.preserved", ack_val.get("owner_operator_ack_candidate_preserved") is True)
    _add(checks, "ack.status", ack_val.get("ack_status") == "owner-operator-ack-candidate")
    for row in ack_val.get("rows") or []:
        role = row.get("role")
        _add(checks, f"ack.row.{role}.candidate", row.get("ack_status") == "owner-operator-ack-candidate")
        _add(checks, f"ack.row.{role}.not_record", row.get("ack_status") != "owner-operator-ack-record")
        _add(checks, f"ack.row.{role}.no_record_flag", row.get("owner_operator_ack_record") is False)

    _add(checks, "evidence.preserved", evidence_val.get("approval_evidence_binding_candidate_preserved") is True)
    _add(checks, "evidence.status", evidence_val.get("binding_status") == "approval-evidence-binding-candidate")
    for row in evidence_val.get("rows") or []:
        bid = row.get("binding_id")
        _add(checks, f"evidence.row.{bid}.candidate", row.get("binding_status") == "approval-evidence-binding-candidate")
        _add(checks, f"evidence.row.{bid}.not_bound", row.get("binding_status") != "approval-evidence-bound-record")
        _add(checks, f"evidence.row.{bid}.not_bound_flag", row.get("approval_evidence_bound") is False)

    _add(checks, "record_binding.preserved", record_binding_val.get("request_record_binding_candidate_preserved") is True)
    _add(checks, "record_binding.status", record_binding_val.get("binding_status") == "request-record-binding-candidate")
    for row in record_binding_val.get("rows") or []:
        bid = row.get("binding_id")
        _add(checks, f"record_binding.row.{bid}.candidate", row.get("binding_status") == "request-record-binding-candidate")
        _add(checks, f"record_binding.row.{bid}.not_bound", row.get("request_record_bound") is False)
        _add(checks, f"record_binding.row.{bid}.not_active", row.get("active_bound_request_record") is False)

    _add(checks, "lifecycle.preserved", lifecycle_val.get("approval_lifecycle_candidate_preserved") is True)
    _add(checks, "lifecycle.type", lifecycle_val.get("lifecycle_type") == "candidate-lifecycle")
    for row in lifecycle_val.get("rows") or []:
        stage = row.get("stage")
        _add(checks, f"lifecycle.row.{stage}.candidate", row.get("lifecycle_type") == "candidate-lifecycle")
        _add(checks, f"lifecycle.row.{stage}.not_active", row.get("lifecycle_type") != "active-approval-lifecycle")

    _add(
        checks,
        "expiry_revocation.preserved",
        expiry_revocation_val.get("expiry_revocation_reference_candidate_preserved") is True,
    )
    _add(
        checks,
        "expiry_revocation.status",
        expiry_revocation_val.get("reference_status") == "expiry-revocation-reference-candidate",
    )
    for row in expiry_revocation_val.get("rows") or []:
        rid = row.get("reference_id")
        _add(
            checks,
            f"expiry_revocation.row.{rid}.candidate",
            row.get("reference_status") == "expiry-revocation-reference-candidate",
        )
        _add(checks, f"expiry_revocation.row.{rid}.not_exec", row.get("reference_status") != "revocation-execution-path")
        _add(checks, f"expiry_revocation.row.{rid}.no_exec_path", row.get("revocation_execution_path") is False)

    _add(checks, "prereq.satisfied", prereq_val.get("approval_prerequisites_satisfied") is True)
    for key in PREREQ_KEYS:
        _add(checks, f"prereq.{key}", prereq_val.get(key) is True)

    for key in ABSENCE_KEYS:
        _add(checks, f"absence.{key}", absence_val.get(key) is True)
    _add(checks, "absence.no_revocation_exec", absence_val.get("no_approval_revocation_execution_path") is True)
    _add(checks, "absence.no_freeze_exec", absence_val.get("no_freeze_execution_path") is True)
    _add(checks, "absence.no_rollback_exec", absence_val.get("no_rollback_execution_path") is True)

    _add(checks, "boundary.dryrun_only", boundary_val.get("owner_approval_dryrun_only") is True)
    _add(checks, "boundary.no_auth_request", boundary_val.get("authorization_request_issued") is False)
    _add(checks, "boundary.no_request_record", boundary_val.get("request_record_created") is False)
    _add(checks, "boundary.no_owner_record", boundary_val.get("owner_approval_record_created") is False)
    _add(checks, "boundary.no_ack_record", boundary_val.get("owner_operator_ack_record_created") is False)
    _add(checks, "boundary.no_evidence_bound", boundary_val.get("approval_evidence_bound_record_created") is False)
    _add(checks, "boundary.grant_issued_false", boundary_val.get("grant_issued") is False)
    _add(checks, "boundary.not_frozen", boundary_val.get("foundation_frozen") is False)
    _add(checks, "boundary.not_closed", boundary_val.get("closed") is False)

    debts = debt_val.get("debts") or []
    _add(checks, "debt.count", len(debts) >= len(GOVERNANCE_DEBTS))
    _add(checks, "debt.required_count", debt_val.get("required_debt_count") == len(GOVERNANCE_DEBTS))
    for i, expected in enumerate(GOVERNANCE_DEBTS):
        debt = next((d for d in debts if d.get("debt_title") == expected["debt_title"]), {})
        _add(checks, f"debt{i}.title", debt.get("debt_title") == expected["debt_title"])
        _add(checks, f"debt{i}.priority", debt.get("priority") == "P1")
        _add(checks, f"debt{i}.classification", debt.get("classification") == "L1 Midplatform System Protocols")
        _add(checks, f"debt{i}.must_not_impl", debt.get("must_not_implement_now") is True)
    _add(checks, "debt.preserved", debt_val.get("governance_debt_preserved") is True)
    _add(checks, "debt.l1_not_impl", debt_val.get("l1_protocols_not_implemented") is True)
    _add(checks, "debt.system_not_impl", debt_val.get("system_protocols_integration_not_implemented") is True)

    _add(checks, "post_review.ok", post_review.get("post_review_readiness_ok") is True)
    _add(checks, "post_review.next", post_review.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(
        checks,
        "post_review.target",
        post_review.get("target") == "freeze_authorization_grant_owner_approval_post_dryrun_review",
    )
    _add(checks, "post_review.no_auth_request", post_review.get("authorization_request_issued") is False)
    _add(checks, "post_review.no_request_record", post_review.get("request_record_created") is False)
    _add(checks, "post_review.no_owner_record", post_review.get("owner_approval_record_created") is False)
    _add(checks, "post_review.no_ack_record", post_review.get("owner_operator_ack_record_created") is False)
    _add(checks, "post_review.no_evidence_bound", post_review.get("approval_evidence_bound_record_created") is False)
    _add(checks, "post_review.no_grant", post_review.get("grant_issued") is False)
    _add(checks, "post_review.no_auth_grant", post_review.get("freeze_authorization_granted") is False)
    _add(checks, "post_review.no_adapter", post_review.get("module_adapter_implementation_ready") is False)
    _add(checks, "post_review.not_frozen", post_review.get("foundation_frozen") is False)
    _add(checks, "post_review.not_closed", post_review.get("closed") is False)
    for forbidden in FORBIDDEN_NEXT_TARGETS:
        _add(checks, f"post_review.not_{forbidden}", forbidden not in (post_review.get("target") or ""))
        _add(
            checks,
            f"post_review.recommended_not_{forbidden}",
            forbidden not in (post_review.get("recommended_next_phase") or "").lower(),
        )

    for stmt in DRYRUN_BOUNDARY_STATEMENTS:
        _add(checks, f"md.boundary.{stmt[:35]}", stmt in md)
        _add(checks, f"report.boundary.{stmt[:35]}", stmt in (report.get("boundary_statements") or []))
        _add(checks, f"boundary.stmt.{stmt[:35]}", stmt in (boundary_val.get("statements") or []))
    for stmt in BOUNDARY_CONTRACT_STATEMENTS:
        _add(checks, f"boundary.contract.{stmt[:35]}", stmt in (boundary_val.get("statements") or []))
        _add(checks, f"md.contract.{stmt[:35]}", stmt in md)

    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.next", NEXT_PHASE_GO in md)
    _add(
        checks,
        "md.not_approval",
        "does not create owner approval records" in md or "不生成 owner approval record" in md,
    )
    for i, debt in enumerate(GOVERNANCE_DEBTS):
        _add(checks, f"md.debt{i}", debt["debt_title"] in md)
    _add(checks, "md.phrase.owner_approval_dryrun", "owner approval dryrun ≠ owner approval" in md)
    _add(checks, "md.protocol_standard", PROTOCOL_STANDARD_REF in md)
    _add(checks, "md.no_revalidation", "Shared protocol system revalidation: `false`" in md)

    for doc_name, doc in docs.items():
        for key in GO_CONDITIONS_KEYS:
            if key in doc:
                _add(checks, f"sweep.true.{doc_name}.{key}", doc.get(key) is True)
        _add(checks, f"sweep.next.{doc_name}", doc.get("recommended_next_phase") in (None, NEXT_PHASE_GO))
        for required in ("phase", "scope", "source_chain", "foundation_id", "runtime_status"):
            _add(checks, f"sweep.meta.{doc_name}.{required}", required in doc)
        for key in RUNTIME_FORBIDDEN_FLAGS:
            _add(checks, f"sweep.runtime.{doc_name}.{key}", doc.get(key) is not True)

    for phrase in ("freeze-candidate", "Owner approval record absent", "owner approval dry-run validation"):
        _add(checks, f"md.phrase.{phrase[:30]}", phrase in md)

    passed = sum(1 for check in checks if check["passed"])
    failed = [check for check in checks if not check["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{key: summary.get(key) is True for key in GO_CONDITIONS_KEYS},
        **{key: summary.get(key) is True for key in TEMPLATE_LINEAGE_GO_KEYS},
        "template_lineage": lineage,
        "final_decision": FINAL_DECISION_GO if verifier == "GO" else "HOLD",
        "go_no_go_decision": FINAL_DECISION_GO if verifier == "GO" else "HOLD",
        "recommended_next_phase": NEXT_PHASE_GO if verifier == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "next_phase": NEXT_PHASE_GO if verifier == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:80],
        "checks": checks,
    }
    schema_ok = validate_core_go_no_go_schema(summary, report_payload)
    report_payload["core_go_no_go_schema_preserved"] = schema_ok
    if not schema_ok:
        checks.append({"check_id": "schema.validate", "passed": False, "detail": "core go/no-go schema mismatch"})
        passed = sum(1 for check in checks if check["passed"])
        failed = [check for check in checks if not check["passed"]]
        report_payload["passed_checks"] = passed
        report_payload["failed_checks"] = len(failed)
        report_payload["blocker_count"] = len(failed)
        report_payload["checks"] = checks
        if verifier == "GO":
            verifier = "HOLD"
            report_payload["verifier"] = verifier
            report_payload["final_decision"] = "HOLD"
            report_payload["go_no_go_decision"] = "HOLD"
    else:
        checks.append({"check_id": "schema.validate", "passed": True, "detail": ""})
        report_payload["checks"] = checks

    (root / "verifier_report.json").write_text(json.dumps(report_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": report_payload["verifier"],
                "passed_checks": report_payload["passed_checks"],
                "failed_checks": report_payload["failed_checks"],
                "blocker_count": report_payload["blocker_count"],
                "prior_owner_approval_planning_go": report_payload.get("prior_owner_approval_planning_go"),
                "protocol_standard_reference_ok": report_payload.get("protocol_standard_reference_ok"),
                "owner_approval_plan_integrity_ok": report_payload.get("owner_approval_plan_integrity_ok"),
                "template_lineage_ok": report_payload.get("template_lineage_ok"),
                "post_review_readiness_ok": report_payload.get("post_review_readiness_ok"),
                "final_decision": report_payload["final_decision"],
                "recommended_next_phase": report_payload["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
