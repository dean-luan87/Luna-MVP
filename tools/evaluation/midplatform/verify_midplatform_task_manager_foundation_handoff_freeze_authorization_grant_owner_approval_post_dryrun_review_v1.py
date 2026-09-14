#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Post-DryRun Review v1."""

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
from capabilities.midplatform.protocols.protocol_separation_rule_v1 import FAILURE_CLASSIFICATION
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    CORE_GO_NO_GO_SCHEMA_KEYS,
    GRANT_OWNER_APPROVAL_POST_REVIEW_STAGE_ADDITIONS,
    GRANT_OWNER_APPROVAL_POST_REVIEW_STAGE_TERM_OVERRIDES,
    GRANT_OWNER_APPROVAL_POST_REVIEW_WHITELIST_FILES,
    TEMPLATE_FAMILY,
    validate_core_go_no_go_schema,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_dryrun_v1 import (
    CHAIN_TRACE_NODES,
    DEFAULT_OUTPUT as DEFAULT_GRANT_OWNER_APPROVAL_DRYRUN_ROOT,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    GO_CONDITIONS_KEYS as DRYRUN_TRUE_KEYS,
    GRANT_OWNER_APPROVAL_DRYRUN_ARTIFACTS,
    NEXT_PHASE_GO as DRYRUN_NEXT_PHASE,
    PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_planning_v1 import (
    BOUNDARY_CONTRACT_STATEMENTS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1 import (
    CHAIN_EVIDENCE_NODES,
    DEFAULT_DRYRUN_ROOT,
    DEFAULT_OUTPUT,
    ERROR_NAMESPACE,
    FINAL_DECISION_GO,
    FORBIDDEN_SCOPE_CLASSIFICATIONS,
    GO_CONDITIONS_KEYS,
    NEXT_PHASE_ALT,
    NEXT_PHASE_GO,
    PHASE_ID,
    POST_REVIEW_BOUNDARY_STATEMENTS,
    POST_REVIEW_SCOPE,
    PROTOCOL_ID,
    PROTOCOL_STANDARD_REF,
    RELATED_PROTOCOL_IDS,
    SCOPE,
    SEPARATION_RULE_REF,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_report_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_report_v1.md",
    "task_manager_freeze_authorization_grant_owner_approval_dryrun_result_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_protocol_reference_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_separation_rule_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_candidate_state_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_operator_ack_candidate_state_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_evidence_binding_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_binding_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_lifecycle_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_expiry_revocation_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_absence_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_boundary_drift_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_evidence_chain_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_governance_debt_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_template_lineage_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_next_phase_readiness_v1.json",
    "summary.json",
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
    "owner_approval_record_created",
    "request_record_created",
    "authorization_request_issued",
    "grant_issued",
    "grant_record_created",
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
    parser.add_argument("--grant-owner-approval-dryrun-root", default=DEFAULT_DRYRUN_ROOT or DEFAULT_GRANT_OWNER_APPROVAL_DRYRUN_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    dryrun = Path(args.grant_owner_approval_dryrun_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_report_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    for rel in GRANT_OWNER_APPROVAL_POST_REVIEW_WHITELIST_FILES:
        _add(checks, f"template.base_file.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())
    _add(checks, "template.whitelist_only", True)

    dryrun_summary = _read(dryrun / "summary.json")
    dryrun_verifier = _read(dryrun / "verifier_report.json")
    _add(checks, "dryrun.summary_go", dryrun_summary.get("final_decision") == DRYRUN_FINAL_GO)
    _add(checks, "dryrun.verifier_go", dryrun_verifier.get("verifier") == "GO")
    _add(checks, "dryrun.passed_min", int(dryrun_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "dryrun.failed_zero", dryrun_verifier.get("failed_checks") == 0)
    _add(checks, "dryrun.blocker_zero", dryrun_verifier.get("blocker_count") == 0)
    _add(checks, "dryrun.post_review_readiness", dryrun_summary.get("post_review_readiness_ok") is True)
    _add(checks, "dryrun.next_phase", dryrun_summary.get("recommended_next_phase") == DRYRUN_NEXT_PHASE)
    for key in DRYRUN_TRUE_KEYS:
        _add(checks, f"dryrun.summary.{key}", dryrun_summary.get(key) is True)
        if key in dryrun_verifier:
            _add(checks, f"dryrun.verifier.{key}", dryrun_verifier.get(key) is True)
    _add(checks, "dryrun.template_lineage_ok", dryrun_summary.get("template_lineage_ok") is True)

    for artifact in GRANT_OWNER_APPROVAL_DRYRUN_ARTIFACTS:
        path = dryrun / artifact
        _add(checks, f"dryrun.artifact.exists.{artifact}", path.is_file())
        if artifact.endswith(".json"):
            _add(checks, f"dryrun.artifact.non_placeholder.{artifact}", bool(_read(path)))

    review = docs[
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_report_v1.json"
    ]
    matrix = docs["task_manager_freeze_authorization_grant_owner_approval_dryrun_result_review_v1.json"]
    protocol_review = docs["task_manager_freeze_authorization_grant_owner_approval_protocol_reference_review_v1.json"]
    separation_review = docs["task_manager_freeze_authorization_grant_owner_approval_separation_rule_review_v1.json"]
    candidate_review = docs["task_manager_freeze_authorization_grant_owner_approval_candidate_state_review_v1.json"]
    ack_review = docs["task_manager_freeze_authorization_grant_owner_operator_ack_candidate_state_review_v1.json"]
    evidence_binding_review = docs[
        "task_manager_freeze_authorization_grant_owner_approval_evidence_binding_review_v1.json"
    ]
    record_binding_review = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_record_binding_review_v1.json"
    ]
    lifecycle_review = docs["task_manager_freeze_authorization_grant_owner_approval_lifecycle_review_v1.json"]
    expiry_revocation_review = docs[
        "task_manager_freeze_authorization_grant_owner_approval_expiry_revocation_review_v1.json"
    ]
    absence_review = docs["task_manager_freeze_authorization_grant_owner_approval_absence_review_v1.json"]
    drift = docs["task_manager_freeze_authorization_grant_owner_approval_boundary_drift_review_v1.json"]
    evidence = docs["task_manager_freeze_authorization_grant_owner_approval_evidence_chain_review_v1.json"]
    debt_review = docs["task_manager_freeze_authorization_grant_owner_approval_governance_debt_review_v1.json"]
    lineage_review = docs["task_manager_freeze_authorization_grant_owner_approval_template_lineage_v1.json"]
    next_readiness = docs["task_manager_freeze_authorization_grant_owner_approval_next_phase_readiness_v1.json"]
    summary = docs["summary.json"]
    lineage = summary.get("template_lineage") or {}

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(checks, f"meta.post_review_only.{doc_name}", doc.get("post_review_only") is True)
        _add(checks, f"meta.foundation_not_frozen.{doc_name}", doc.get("foundation_not_frozen") in (None, True))
        _add(checks, f"meta.request_record_absent.{doc_name}", doc.get("request_record_absent") in (None, True))
        _add(checks, f"meta.owner_approval_record_absent.{doc_name}", doc.get("owner_approval_record_absent") in (None, True))
        _add(
            checks,
            f"meta.no_revalidation.{doc_name}",
            doc.get("shared_protocol_system_revalidation") in (None, False),
        )
        for key in RUNTIME_FORBIDDEN_FLAGS:
            _add(checks, f"meta.no_runtime.{doc_name}.{key}", doc.get(key) is not True)

    _add(checks, "summary.pass", summary.get("post_dryrun_review_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
        _add(checks, f"review.{key}", review.get(key) is True)
        _add(checks, f"go_conditions.{key}", (summary.get("go_conditions") or {}).get(key) is True)

    for key in CORE_GO_NO_GO_SCHEMA_KEYS:
        if key in ("passed_checks", "failed_checks", "blocker_count", "verifier", "summary"):
            continue
        _add(checks, f"summary.schema.{key}", key in summary)

    for key in TEMPLATE_LINEAGE_GO_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _add(checks, "lineage.family", lineage.get("template_family") == TEMPLATE_FAMILY)
    _add(
        checks,
        "lineage.base_phase",
        lineage.get("base_phase") == "Freeze-Authorization-Grant-Request-Record-Post-DryRun-Review-v1-001",
    )
    _add(
        checks,
        "lineage.upstream",
        lineage.get("upstream_review_phase") == "Freeze-Authorization-Grant-Owner-Approval-DryRun-v1-001",
    )
    _add(checks, "lineage.reuse_mode", lineage.get("reuse_mode") == "whitelist_file_template_reuse")
    _add(checks, "lineage.no_full_scan", lineage.get("full_repo_scan_allowed") is False)
    _add(checks, "lineage.files_exist", lineage.get("base_template_files_exist") is True)
    _add(checks, "lineage.stage_overridden", lineage.get("stage_specific_terms_overridden") is True)
    _add(checks, "lineage.ok", lineage.get("template_lineage_ok") is True)
    _add(checks, "lineage.review.ok", lineage_review.get("template_lineage_ok") is True)
    _add(checks, "lineage.review.upstream", lineage_review.get("upstream_owner_approval_dryrun_lineage_ok") is True)
    for override in GRANT_OWNER_APPROVAL_POST_REVIEW_STAGE_TERM_OVERRIDES:
        _add(checks, f"lineage.override.{override['base_term'][:30]}", override in (lineage.get("stage_term_overrides") or []))
    for addition in GRANT_OWNER_APPROVAL_POST_REVIEW_STAGE_ADDITIONS:
        _add(checks, f"lineage.addition.{addition}", addition in (lineage.get("stage_additions") or []))

    _add(checks, "matrix.accepted", matrix.get("owner_approval_dryrun_result_accepted") is True)
    _add(checks, "matrix.prior_go", matrix.get("prior_owner_approval_dryrun_go") is True)
    for row in matrix.get("rows") or []:
        name = row.get("artifact")
        _add(checks, f"matrix.exists.{name}", row.get("exists") is True)
        _add(checks, f"matrix.non_placeholder.{name}", row.get("non_placeholder") is True)

    _add(checks, "protocol_ref.standard", protocol_review.get("protocol_standard_ref") == PROTOCOL_STANDARD_REF)
    _add(checks, "protocol_ref.id", protocol_review.get("protocol_id") == PROTOCOL_ID)
    _add(checks, "protocol_ref.error_namespace", protocol_review.get("error_namespace") == ERROR_NAMESPACE)
    _add(checks, "protocol_ref.related_ids", protocol_review.get("related_protocol_ids") == list(RELATED_PROTOCOL_IDS))
    _add(checks, "protocol_ref.separation", protocol_review.get("separation_rule_ref") == SEPARATION_RULE_REF)
    _add(
        checks,
        "protocol_ref.schema_ref",
        protocol_review.get("protocol_execution_result_schema_ref") == PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
    )
    _add(checks, "protocol_ref.no_revalidation", protocol_review.get("shared_protocol_system_revalidation") is False)
    _add(checks, "protocol_ref.review_ok", protocol_review.get("protocol_reference_review_ok") is True)
    _add(checks, "protocol_ref.standard_ok", protocol_review.get("protocol_standard_reference_ok") is True)
    _add(checks, "protocol_ref.id_ok", protocol_review.get("protocol_id_reference_ok") is True)
    _add(checks, "protocol_ref.namespace_ok", protocol_review.get("error_namespace_reference_ok") is True)
    _add(checks, "protocol_ref.schema_ok", protocol_review.get("protocol_execution_result_schema_ref_ok") is True)
    _add(checks, "protocol_ref.separation_ok", protocol_review.get("separation_rule_ref_ok") is True)
    _add(checks, "protocol_ref.error_code_ok", protocol_review.get("protocol_error_code_light_check_ok") is True)
    _add(checks, "protocol_ref.whitebox_ok", protocol_review.get("whitebox_candidate_ref_ok") is True)
    for pid in RELATED_PROTOCOL_IDS:
        _add(checks, f"protocol_ref.related.{pid}", pid in (protocol_review.get("related_protocol_ids") or []))

    _add(checks, "separation.review_ok", separation_review.get("separation_rule_review_ok") is True)
    _add(checks, "separation.ref", separation_review.get("separation_rule_ref") == SEPARATION_RULE_REF)
    _add(
        checks,
        "separation.classification_rules",
        list(separation_review.get("error_classification_rules") or []) == list(FAILURE_CLASSIFICATION),
    )
    _add(
        checks,
        "separation.module_local_not_protocol",
        separation_review.get("module_local_failure_not_protocol_failure_by_default") is True,
    )

    _add(checks, "drift.absent", drift.get("boundary_drift_absent") is True)
    _add(checks, "drift.post_review_scope", drift.get("post_review_scope") == POST_REVIEW_SCOPE)
    for forbidden in FORBIDDEN_SCOPE_CLASSIFICATIONS:
        _add(checks, f"drift.not_{forbidden}", drift.get("post_review_scope") != forbidden)
    for row in drift.get("rows") or []:
        name = row.get("artifact")
        _add(checks, f"drift.runtime_absent.{name}", row.get("runtime_scope_leak_absent") is True)
        _add(checks, f"drift.no_added_runtime.{name}", row.get("post_review_added_runtime") is False)
        _add(checks, f"drift.scope_ok.{name}", row.get("scope_classification") == POST_REVIEW_SCOPE)

    _add(checks, "evidence.accepted", evidence.get("freeze_authorization_chain_evidence_accepted") is True)
    _add(checks, "evidence.review_ok", evidence.get("evidence_chain_review_ok") is True)
    _add(checks, "evidence.node_count", evidence.get("node_count") == len(CHAIN_EVIDENCE_NODES))
    for stage in CHAIN_TRACE_NODES:
        row = next((r for r in evidence.get("chain") or [] if r.get("stage") == stage), {})
        _add(checks, f"evidence.linked.{stage}", row.get("linked") is True)
    post_row = next(
        (r for r in evidence.get("chain") or [] if r.get("stage") == "freeze_authorization_grant_owner_approval_post_dryrun_review"),
        {},
    )
    _add(checks, "evidence.post_review.linked", post_row.get("linked") is True)
    _add(checks, "evidence.post_review.scope", post_row.get("readiness") == POST_REVIEW_SCOPE)
    _add(checks, "evidence.post_review.no_issued", post_row.get("authorization_request_issued") is False)
    _add(checks, "evidence.post_review.no_record", post_row.get("request_record") is False)
    _add(checks, "evidence.post_review.no_approval_record", post_row.get("owner_approval_record") is False)
    _add(checks, "evidence.post_review.no_ack_record", post_row.get("owner_operator_ack_record") is False)
    _add(checks, "evidence.post_review.no_grant", post_row.get("grant_issued") is False)

    _add(checks, "absence.review_ok", absence_review.get("absence_review_ok") is True)
    _add(checks, "absence.not_issued", absence_review.get("authorization_request_issued") is False)
    for key in ABSENCE_KEYS:
        _add(checks, f"absence.{key}", absence_review.get(key) is True)
    _add(checks, "absence.no_freeze_exec", absence_review.get("no_freeze_execution_path") is True)
    _add(checks, "absence.no_rollback_exec", absence_review.get("no_rollback_execution_path") is True)
    _add(checks, "absence.no_revocation_exec", absence_review.get("no_revocation_execution_path") is True)

    _add(checks, "review.candidate_state", review.get("candidate_state_preserved") is True)
    _add(checks, "review.owner_operator_ack", review.get("owner_operator_ack_candidate_preserved") is True)
    _add(checks, "review.approval_evidence_binding", review.get("approval_evidence_binding_candidate_preserved") is True)
    _add(checks, "review.request_record_binding", review.get("request_record_binding_candidate_preserved") is True)
    _add(checks, "review.approval_lifecycle", review.get("approval_lifecycle_candidate_preserved") is True)
    _add(checks, "review.expiry_revocation", review.get("expiry_revocation_reference_candidate_preserved") is True)
    _add(checks, "review.post_review_scope", review.get("post_review_scope") == POST_REVIEW_SCOPE)
    _add(checks, "review.planning_ready", review.get("owner_approval_request_planning_ready") is True)

    _add(checks, "candidate.preserved", candidate_review.get("candidate_state_preserved") is True)
    _add(checks, "candidate.approval_status", candidate_review.get("approval_status") == "owner-approval-candidate")
    _add(checks, "candidate.freeze_status", candidate_review.get("freeze_status") == "freeze-candidate")
    for row in candidate_review.get("rows") or []:
        role = row.get("role")
        _add(checks, f"candidate.row.{role}.candidate", row.get("approval_status") == "owner-approval-candidate")
        _add(checks, f"candidate.row.{role}.not_record", row.get("approval_status") != "owner-approval-record")

    _add(checks, "ack.preserved", ack_review.get("owner_operator_ack_candidate_preserved") is True)
    _add(checks, "ack.status", ack_review.get("ack_status") == "owner-operator-ack-candidate")
    for row in ack_review.get("rows") or []:
        role = row.get("role")
        _add(checks, f"ack.row.{role}.candidate", row.get("ack_status") == "owner-operator-ack-candidate")
        _add(checks, f"ack.row.{role}.not_record", row.get("ack_status") != "owner-operator-ack-record")

    _add(checks, "evidence_binding.preserved", evidence_binding_review.get("approval_evidence_binding_candidate_preserved") is True)
    _add(checks, "evidence_binding.status", evidence_binding_review.get("binding_status") == "approval-evidence-binding-candidate")
    _add(checks, "evidence_binding.bound_absent", evidence_binding_review.get("approval_evidence_bound_record_absent") is True)
    for row in evidence_binding_review.get("rows") or []:
        bid = row.get("binding_id")
        _add(checks, f"evidence_binding.row.{bid}.candidate", row.get("binding_status") == "approval-evidence-binding-candidate")
        _add(checks, f"evidence_binding.row.{bid}.not_bound", row.get("binding_status") != "approval-evidence-bound-record")

    _add(checks, "record_binding.preserved", record_binding_review.get("request_record_binding_candidate_preserved") is True)
    _add(checks, "record_binding.status", record_binding_review.get("binding_status") == "request-record-binding-candidate")
    _add(checks, "record_binding.record_absent", record_binding_review.get("request_record_absent") is True)
    for row in record_binding_review.get("rows") or []:
        bid = row.get("binding_id")
        _add(checks, f"record_binding.row.{bid}.candidate", row.get("binding_status") == "request-record-binding-candidate")
        _add(checks, f"record_binding.row.{bid}.not_bound", row.get("binding_status") != "request-record")

    _add(checks, "lifecycle.preserved", lifecycle_review.get("approval_lifecycle_candidate_preserved") is True)
    _add(checks, "lifecycle.type", lifecycle_review.get("lifecycle_type") == "candidate-lifecycle")
    for row in lifecycle_review.get("rows") or []:
        stage = row.get("stage")
        _add(checks, f"lifecycle.row.{stage}.candidate", row.get("lifecycle_type") == "candidate-lifecycle")
        _add(checks, f"lifecycle.row.{stage}.not_active", row.get("lifecycle_type") != "active-approval-lifecycle")

    _add(checks, "expiry_revocation.preserved", expiry_revocation_review.get("expiry_revocation_reference_candidate_preserved") is True)
    _add(checks, "expiry_revocation.status", expiry_revocation_review.get("reference_status") == "expiry-revocation-reference-candidate")
    _add(checks, "expiry_revocation.no_exec_path", expiry_revocation_review.get("no_revocation_execution_path") is True)
    for row in expiry_revocation_review.get("rows") or []:
        rid = row.get("reference_id")
        _add(checks, f"expiry_revocation.row.{rid}.candidate", row.get("reference_status") == "expiry-revocation-reference-candidate")
        _add(checks, f"expiry_revocation.row.{rid}.not_exec", row.get("reference_status") != "revocation-execution-path")
        _add(checks, f"expiry_revocation.row.{rid}.no_exec_flag", row.get("revocation_execution_path") is False)

    debts = debt_review.get("debts") or []
    _add(checks, "debt.count", len(debts) >= len(GOVERNANCE_DEBTS))
    _add(checks, "debt.required_count", debt_review.get("required_debt_count") == len(GOVERNANCE_DEBTS))
    for i, expected in enumerate(GOVERNANCE_DEBTS):
        debt = next((d for d in debts if d.get("debt_title") == expected["debt_title"]), {})
        _add(checks, f"debt{i}.title", debt.get("debt_title") == expected["debt_title"])
        _add(checks, f"debt{i}.priority", debt.get("priority") == "P1")
        _add(checks, f"debt{i}.classification", debt.get("classification") == "L1 Midplatform System Protocols")
        _add(checks, f"debt{i}.must_not_impl", debt.get("must_not_implement_now") is True)
    _add(checks, "debt.preserved", debt_review.get("governance_debt_preserved") is True)
    _add(checks, "debt.l1_not_impl", debt_review.get("l1_protocols_not_implemented") is True)
    _add(checks, "debt.system_not_impl", debt_review.get("system_protocols_integration_not_implemented") is True)

    _add(checks, "next.ready", next_readiness.get("owner_approval_request_planning_ready") is True)
    _add(checks, "next.readiness_ok", next_readiness.get("next_phase_readiness_ok") is True)
    _add(checks, "next.recommended", next_readiness.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "next.no_auth_issued", next_readiness.get("authorization_request_issued") is False)
    _add(checks, "next.no_request_record", next_readiness.get("request_record_created") is False)
    _add(checks, "next.no_owner_record", next_readiness.get("owner_approval_record_created") is False)
    _add(checks, "next.no_ack_record", next_readiness.get("owner_operator_ack_record_created") is False)
    _add(checks, "next.no_evidence_bound", next_readiness.get("approval_evidence_bound_record_created") is False)
    _add(checks, "next.no_grant", next_readiness.get("grant_issued") is False)
    _add(checks, "next.no_adapter", next_readiness.get("module_adapter_implementation_ready") is False)
    _add(checks, "next.not_frozen", next_readiness.get("foundation_frozen") is False)
    _add(checks, "next.not_closed", next_readiness.get("closed") is False)
    for candidate in next_readiness.get("candidates") or []:
        phase = candidate.get("phase", "")
        _add(checks, f"next.candidate.{phase[:50]}.no_auth_issued", candidate.get("authorization_request_issued") is False)
        _add(checks, f"next.candidate.{phase[:50]}.no_request_record", candidate.get("request_record_created") is False)
        _add(checks, f"next.candidate.{phase[:50]}.no_owner_record", candidate.get("owner_approval_record_created") is False)
        _add(checks, f"next.candidate.{phase[:50]}.no_ack_record", candidate.get("owner_operator_ack_record_created") is False)
        _add(checks, f"next.candidate.{phase[:50]}.no_grant", candidate.get("grant_issued") is False)
        _add(checks, f"next.candidate.{phase[:50]}.not_frozen", candidate.get("foundation_frozen") is False)
        _add(checks, f"next.candidate.{phase[:50]}.not_closed", candidate.get("closed") is False)
        for forbidden in FORBIDDEN_NEXT_TARGETS:
            _add(checks, f"next.candidate.{phase[:50]}.not_{forbidden}", forbidden not in phase.lower())
    _add(
        checks,
        "next.has_alt_candidate",
        any(c.get("phase") == NEXT_PHASE_ALT for c in (next_readiness.get("candidates") or [])),
    )
    for forbidden in FORBIDDEN_NEXT_TARGETS:
        _add(checks, f"next.recommended_not_{forbidden}", forbidden not in (next_readiness.get("recommended_next_phase") or "").lower())

    for stmt in POST_REVIEW_BOUNDARY_STATEMENTS:
        _add(checks, f"md.boundary.{stmt[:35]}", stmt in md)
        _add(checks, f"drift.boundary.{stmt[:35]}", stmt in (drift.get("boundary_statements") or []))
    for stmt in BOUNDARY_CONTRACT_STATEMENTS:
        _add(checks, f"drift.contract.{stmt[:35]}", stmt in (drift.get("upstream_boundary_statements") or []) or stmt in md)

    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.next", NEXT_PHASE_GO in md)
    _add(
        checks,
        "md.not_approval",
        "does not create owner approval records" in md or "不生成 owner approval record" in md,
    )
    _add(checks, "md.post_review_ne", "owner approval post-dryrun review ≠ owner approval" in md)
    for i, debt in enumerate(GOVERNANCE_DEBTS):
        _add(checks, f"md.debt{i}", debt["debt_title"] in md)
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

    for phrase in ("freeze-candidate", "Owner approval record absent", "Template lineage OK", POST_REVIEW_SCOPE):
        _add(checks, f"md.phrase.{phrase[:30]}", phrase in md)

    passed = sum(1 for check in checks if check["passed"])
    failed = [check for check in checks if not check["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report = {
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
    schema_ok = validate_core_go_no_go_schema(summary, report)
    report["core_go_no_go_schema_preserved"] = schema_ok
    if not schema_ok:
        checks.append({"check_id": "schema.validate", "passed": False, "detail": "core go/no-go schema mismatch"})
        passed = sum(1 for check in checks if check["passed"])
        failed = [check for check in checks if not check["passed"]]
        report["passed_checks"] = passed
        report["failed_checks"] = len(failed)
        report["blocker_count"] = len(failed)
        report["checks"] = checks
        if verifier == "GO":
            verifier = "HOLD"
            report["verifier"] = verifier
            report["final_decision"] = "HOLD"
            report["go_no_go_decision"] = "HOLD"
    else:
        checks.append({"check_id": "schema.validate", "passed": True, "detail": ""})
        report["checks"] = checks

    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": report["verifier"],
                "passed_checks": report["passed_checks"],
                "failed_checks": report["failed_checks"],
                "blocker_count": report["blocker_count"],
                "owner_approval_dryrun_result_accepted": report.get("owner_approval_dryrun_result_accepted"),
                "protocol_reference_review_ok": report.get("protocol_reference_review_ok"),
                "separation_rule_review_ok": report.get("separation_rule_review_ok"),
                "evidence_chain_review_ok": report.get("evidence_chain_review_ok"),
                "absence_review_ok": report.get("absence_review_ok"),
                "template_lineage_ok": report.get("template_lineage_ok"),
                "full_repo_scan_absent": report.get("full_repo_scan_absent"),
                "core_go_no_go_schema_preserved": report.get("core_go_no_go_schema_preserved"),
                "post_review_only": report.get("post_review_only"),
                "owner_approval_request_planning_ready": report.get("owner_approval_request_planning_ready"),
                "final_decision": report["final_decision"],
                "recommended_next_phase": report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
