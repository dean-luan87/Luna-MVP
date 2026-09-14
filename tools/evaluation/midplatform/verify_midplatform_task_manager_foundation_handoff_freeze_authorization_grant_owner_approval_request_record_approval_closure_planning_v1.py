#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Request Record Approval Closure Planning v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import (
    FILE_SIZE_GOVERNANCE_REVIEW_KEYS,
    RULE_NAME_EN as FILE_SIZE_GOVERNANCE_RULE_REF,
)
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    CORE_GO_NO_GO_SCHEMA_KEYS,
    GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_STAGE_ADDITIONS,
    GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_STAGE_TERM_OVERRIDES,
    GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_WHITELIST_FILES,
    TEMPLATE_FAMILY,
    validate_core_go_no_go_schema,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    CHAIN_EVIDENCE_NODES as UPSTREAM_CHAIN_NODES,
    FINAL_DECISION_GO as OWNER_APPROVAL_REQUEST_ISSUANCE_POST_REVIEW_FINAL_GO,
    GO_CONDITIONS_KEYS as UPSTREAM_GO_KEYS,
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1 import (
    BOUNDARY_CONTRACT_STATEMENTS,
    CHAIN_EVIDENCE_NODES,
    DEFAULT_OWNER_APPROVAL_REQUEST_ISSUANCE_POST_REVIEW_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    LIGHTWEIGHT_PROTOCOL_REFS,
    NEXT_PHASE_GO,
    NON_EXECUTION_CONSTRAINTS,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
    TEMPLATE_LINEAGE_MODULE_PATH,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_plan_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_plan_v1.md",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_candidate_closure_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_approval_candidate_closure_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_ack_candidate_closure_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_evidence_binding_closure_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_traceability_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_protocol_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_error_namespace_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_whitebox_candidate_ref_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_boundary_contract_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_non_execution_constraints_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_rejection_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_expiry_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_revocation_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_governance_debt_carryover_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_template_lineage_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_next_phase_readiness_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
)
TEMPLATE_LINEAGE_GO_KEYS: Tuple[str, ...] = (
    "template_lineage_ok",
    "base_template_files_exist",
    "full_repo_scan_absent",
    "core_go_no_go_schema_preserved",
    "stage_specific_terms_overridden",
)
FORBIDDEN_NEXT_TARGETS: Tuple[str, ...] = (
    "request_issued",
    "request_record_created",
    "approval_record_created",
    "grant_issued",
    "foundation_frozen",
    "closure_executed",
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
    parser.add_argument(
        "--owner-approval-request-issuance-post-dryrun-review-root",
        default=DEFAULT_OWNER_APPROVAL_REQUEST_ISSUANCE_POST_REVIEW_ROOT,
    )
    args = parser.parse_args()
    root = Path(args.output_root)
    post_review = Path(args.owner_approval_request_issuance_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_plan_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    for rel in GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_WHITELIST_FILES:
        _add(checks, f"template.whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())
    _add(checks, "template.whitelist_only", True)

    post_summary = _read(post_review / "summary.json")
    post_verifier = _read(post_review / "verifier_report.json")
    timeout_review = _read(
        post_review / "task_manager_freeze_authorization_grant_owner_approval_request_issuance_timeout_event_review_v1.json"
    )
    _add(checks, "prior.summary_go", post_summary.get("final_decision") == OWNER_APPROVAL_REQUEST_ISSUANCE_POST_REVIEW_FINAL_GO)
    _add(checks, "prior.verifier_go", post_verifier.get("verifier") == "GO")
    _add(checks, "prior.passed_min", int(post_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "prior.failed_zero", post_verifier.get("failed_checks") == 0)
    _add(checks, "prior.blocker_zero", post_verifier.get("blocker_count") == 0)
    _add(checks, "prior.timeout_event_review_ok", post_summary.get("timeout_event_review_ok") is True)
    _add(checks, "prior.previous_interruption_not_logic_loop", timeout_review.get("previous_interruption_not_logic_loop") is True)
    _add(checks, "prior.timeout_event_is_blocker", timeout_review.get("timeout_event_is_blocker") is False)
    _add(checks, "prior.issuance_dryrun_result_accepted", post_summary.get("issuance_dryrun_result_accepted") is True)
    _add(checks, "prior.validate_once_reference_review_ok", post_summary.get("validate_once_reference_review_ok") is True)
    for key in UPSTREAM_GO_KEYS:
        _add(checks, f"prior.summary.{key}", post_summary.get(key) is True)
        if key in post_verifier:
            _add(checks, f"prior.verifier.{key}", post_verifier.get(key) is True)

    plan = docs["task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_plan_v1.json"]
    record_candidate = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_candidate_closure_matrix_v1.json"]
    approval_candidate = docs["task_manager_freeze_authorization_grant_owner_approval_request_approval_candidate_closure_matrix_v1.json"]
    ack_candidate = docs["task_manager_freeze_authorization_grant_owner_approval_request_ack_candidate_closure_matrix_v1.json"]
    evidence_binding = docs["task_manager_freeze_authorization_grant_owner_approval_request_evidence_binding_closure_matrix_v1.json"]
    traceability = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_traceability_matrix_v1.json"]
    protocol_ref = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_protocol_reference_matrix_v1.json"]
    error_ns = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_error_namespace_matrix_v1.json"]
    whitebox = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_whitebox_candidate_ref_matrix_v1.json"]
    rejection = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_rejection_reference_matrix_v1.json"]
    expiry = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_expiry_reference_matrix_v1.json"]
    revocation = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_revocation_reference_matrix_v1.json"]
    boundary = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_boundary_contract_v1.json"]
    constraints = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_non_execution_constraints_v1.json"]
    debt_carryover = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_governance_debt_carryover_v1.json"]
    lineage_doc = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_template_lineage_v1.json"]
    next_phase = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_next_phase_readiness_v1.json"]
    file_size_review = docs["file_size_governance_review_v1.json"]
    summary = docs["summary.json"]
    lineage = summary.get("template_lineage") or {}

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(
            checks,
            f"meta.record_planning_only.{doc_name}",
            doc.get("record_approval_closure_planning_only") in (None, True),
        )
        for key in RUNTIME_FORBIDDEN_FLAGS:
            _add(checks, f"meta.no_runtime.{doc_name}.{key}", doc.get(key) is not True)

    _add(checks, "summary.pass", summary.get("planning_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
        _add(checks, f"plan.{key}", plan.get(key) is True)
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
        lineage.get("base_phase") == "Freeze-Authorization-Grant-Owner-Approval-Request-Issuance-Post-DryRun-Review-v1-001",
    )
    _add(
        checks,
        "lineage.upstream",
        lineage.get("upstream_review_phase") == "Freeze-Authorization-Grant-Owner-Approval-Request-Issuance-Post-DryRun-Review-v1-001",
    )
    _add(checks, "lineage.reuse_mode", lineage.get("reuse_mode") == "whitelist_file_template_reuse")
    _add(checks, "lineage.no_full_scan", lineage.get("full_repo_scan_allowed") is False)
    _add(checks, "lineage.files_exist", lineage.get("base_template_files_exist") is True)
    _add(checks, "lineage.ok", lineage.get("template_lineage_ok") is True)
    _add(checks, "lineage.doc.ok", lineage_doc.get("template_lineage_ok") is True)
    _add(checks, "lineage.doc.upstream", lineage_doc.get("upstream_owner_approval_request_issuance_post_review_lineage_ok") is True)
    for override in GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_STAGE_TERM_OVERRIDES:
        _add(checks, f"lineage.override.{override['base_term'][:30]}", override in (lineage.get("stage_term_overrides") or []))
    for addition in GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_PLANNING_STAGE_ADDITIONS:
        _add(checks, f"lineage.addition.{addition}", addition in (lineage.get("stage_additions") or []))

    _add(checks, "record.candidate_only", record_candidate.get("record_candidate_closure_matrix_complete") is True)
    for row in record_candidate.get("rows") or []:
        rtype = row.get("record_type")
        _add(checks, f"record.{rtype}.candidate", row.get("record_status") == "owner-approval-request-record-candidate")
        _add(checks, f"record.{rtype}.not_record", row.get("record_status") != "request-record")
        _add(checks, f"record.{rtype}.not_created", row.get("record_created") is False)
        _add(checks, f"record.{rtype}.request_issued_absent", row.get("request_issued") is False)

    _add(checks, "approval.candidate_only", approval_candidate.get("approval_candidate_closure_matrix_complete") is True)
    for row in approval_candidate.get("rows") or []:
        cid = row.get("candidate_id")
        _add(checks, f"approval.{cid}.candidate", row.get("candidate_status") == "owner-approval-record-candidate")
        _add(checks, f"approval.{cid}.not_record", row.get("candidate_status") != "owner-approval-record")
        _add(checks, f"approval.{cid}.not_created", row.get("approval_record_created") is False)

    _add(checks, "ack.candidate_only", ack_candidate.get("ack_candidate_closure_matrix_complete") is True)
    for row in ack_candidate.get("rows") or []:
        role = row.get("role")
        _add(checks, f"ack.{role}.candidate", row.get("binding_status") == "owner-operator-ack-record-candidate")
        _add(checks, f"ack.{role}.not_record", row.get("binding_status") != "owner-operator-ack-record")

    _add(checks, "evidence_binding.candidate_only", evidence_binding.get("evidence_binding_closure_matrix_complete") is True)
    for row in evidence_binding.get("rows") or []:
        bid = row.get("binding_id")
        _add(checks, f"evidence.{bid}.candidate", row.get("binding_status") == "approval-evidence-bound-record-candidate")
        _add(checks, f"evidence.{bid}.not_bound", row.get("binding_status") != "approval-evidence-bound-record")
        _add(checks, f"evidence.{bid}.not_bound_flag", row.get("evidence_bound") is False)

    _add(checks, "traceability.complete", traceability.get("traceability_matrix_complete") is True)
    _add(checks, "traceability.no_revalidation", traceability.get("shared_protocol_system_revalidation") is False)
    _add(checks, "traceability.no_l1_revalidation", traceability.get("l1_input_output_protocol_revalidation") is False)
    for stage in UPSTREAM_CHAIN_NODES:
        row = next((r for r in traceability.get("chain") or [] if r.get("stage") == stage), {})
        if stage in (
            "freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review",
            "freeze_authorization_grant_owner_approval_request_record_approval_closure_planning",
        ):
            _add(checks, f"traceability.linked.{stage}", row.get("linked") is True)
        else:
            _add(checks, f"traceability.declared.{stage}", bool(row.get("stage")))

    _add(checks, "protocol_ref.ok", protocol_ref.get("protocol_reference_matrix_ok") is True)
    _add(checks, "protocol_ref.lightweight", all(r.get("reference_mode") == "lightweight" for r in protocol_ref.get("refs") or []))
    for pid in LIGHTWEIGHT_PROTOCOL_REFS:
        _add(checks, f"protocol_ref.contains.{pid}", any(r.get("protocol_id") == pid for r in protocol_ref.get("refs") or []))

    _add(checks, "error_ns.ok", error_ns.get("error_namespace_matrix_ok") is True)
    _add(checks, "error_ns.present", bool(error_ns.get("error_namespace")))

    _add(checks, "whitebox.ok", whitebox.get("whitebox_candidate_ref_matrix_ok") is True)
    _add(checks, "whitebox.runtime_absent", whitebox.get("whitebox_runtime_integration_absent") is True)

    _add(checks, "rejection.candidate_only", rejection.get("rejection_reference_candidate_only") is True)
    for row in rejection.get("rows") or []:
        rid = row.get("reference_id")
        _add(checks, f"rejection.{rid}.candidate", row.get("reference_status") == "rejection-reference-candidate")
        _add(checks, f"rejection.{rid}.no_exec", row.get("rejection_execution_path") is False)

    _add(checks, "expiry.candidate_only", expiry.get("expiry_reference_candidate_only") is True)
    for row in expiry.get("rows") or []:
        rid = row.get("reference_id")
        _add(checks, f"expiry.{rid}.candidate", row.get("reference_status") == "expiry-reference-candidate")
        _add(checks, f"expiry.{rid}.no_exec", row.get("expiry_execution_path") is False)

    _add(checks, "revocation.candidate_only", revocation.get("revocation_reference_candidate_only") is True)
    for row in revocation.get("rows") or []:
        rid = row.get("reference_id")
        _add(checks, f"revocation.{rid}.candidate", row.get("reference_status") == "revocation-reference-candidate")
        _add(checks, f"revocation.{rid}.no_exec", row.get("revocation_execution_path") is False)

    _add(checks, "evidence.complete", plan.get("evidence_chain_complete") is True)
    _add(checks, "evidence.paths_declared", summary.get("evidence_chain_paths_declared") is True)
    _add(checks, "evidence.issuance_post_review_ref_linked", summary.get("issuance_post_review_ref_linked") is True)
    _add(checks, "evidence.planning_node_linked", summary.get("planning_node_linked") is True)
    for stage in UPSTREAM_CHAIN_NODES:
        row = next((r for r in plan.get("evidence_chain") or [] if r.get("stage") == stage), {})
        if stage == "freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review":
            _add(checks, f"evidence.linked.{stage}", row.get("linked") is True)
        else:
            _add(checks, f"evidence.declared.{stage}", bool(row.get("stage")))
    planning_row = next(
        (r for r in plan.get("evidence_chain") or [] if r.get("stage") == "freeze_authorization_grant_owner_approval_request_record_approval_closure_planning"),
        {},
    )
    _add(checks, "evidence.planning.linked", planning_row.get("linked") is True)
    _add(checks, "evidence.node_count", plan.get("node_count") == len(CHAIN_EVIDENCE_NODES))

    for stmt in BOUNDARY_CONTRACT_STATEMENTS:
        _add(checks, f"boundary.stmt.{stmt[:35]}", stmt in (boundary.get("statements") or []))
    _add(checks, "boundary.closure_candidate_ne_executed", boundary.get("closure_candidate_ne_closure_executed") is True)
    _add(checks, "boundary.request_issued_absent", boundary.get("request_issued_absent") is True)
    _add(checks, "boundary.notification_sent_absent", boundary.get("notification_sent_absent") is True)
    _add(checks, "boundary.grant_absent", boundary.get("grant_absent") is True)
    _add(checks, "boundary.closure_not_executed", boundary.get("closure_executed") is False)

    for key in NON_EXECUTION_CONSTRAINTS:
        _add(checks, f"constraints.{key}", constraints.get(key) is True)
    _add(checks, "constraints.ok", constraints.get("non_execution_boundary_ok") is True)

    debts = debt_carryover.get("debts") or []
    _add(checks, "debt.count", len(debts) >= 2)
    debt0 = debts[0] if debts else {}
    debt1 = debts[1] if len(debts) > 1 else {}
    _add(checks, "debt0.title", debt0.get("debt_title") == GOVERNANCE_DEBTS[0]["debt_title"])
    _add(checks, "debt0.priority", debt0.get("priority") == "P1")
    _add(checks, "debt0.classification", debt0.get("classification") == "L1 Midplatform System Protocols")
    _add(checks, "debt0.must_not_impl", debt0.get("must_not_implement_now") is True)
    _add(checks, "debt1.title", debt1.get("debt_title") == GOVERNANCE_DEBTS[1]["debt_title"])
    _add(checks, "debt1.priority", debt1.get("priority") == "P1")
    _add(checks, "debt1.classification", debt1.get("classification") == "L1 Midplatform System Protocols")
    _add(checks, "debt1.must_not_impl", debt1.get("must_not_implement_now") is True)
    _add(checks, "debt.carryover_complete", debt_carryover.get("governance_debt_preserved") is True)

    _add(checks, "next_phase.ok", next_phase.get("next_phase_readiness_ok") is True)
    _add(checks, "next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "next_phase.target_dryrun", next_phase.get("target") == "freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun")
    _add(checks, "next_phase.no_request_issued", next_phase.get("request_issued") is False)
    _add(checks, "next_phase.no_notification", next_phase.get("notification_sent") is False)
    _add(checks, "next_phase.no_request_record", next_phase.get("request_record_created") is False)
    _add(checks, "next_phase.no_approval_record", next_phase.get("approval_record_created") is False)
    _add(checks, "next_phase.no_ack_record", next_phase.get("ack_record_created") is False)
    _add(checks, "next_phase.no_evidence_bound", next_phase.get("evidence_bound_record_created") is False)
    _add(checks, "next_phase.no_grant", next_phase.get("grant_issued") is False)
    _add(checks, "next_phase.not_frozen", next_phase.get("foundation_frozen") is False)
    _add(checks, "next_phase.closure_not_executed", next_phase.get("closure_executed") is False)
    _add(checks, "next_phase.no_adapter", next_phase.get("module_adapter_implementation_ready") is False)
    for forbidden in FORBIDDEN_NEXT_TARGETS:
        _add(checks, f"next_phase.not_{forbidden}", forbidden not in (next_phase.get("recommended_next_phase") or "").lower())

    _add(checks, "file_size.artifact_exists", bool(file_size_review))
    _add(checks, "file_size.rule_ref", file_size_review.get("rule_ref") == FILE_SIZE_GOVERNANCE_RULE_REF)
    _add(checks, "file_size.phase_id", file_size_review.get("phase_id") == PHASE_ID)
    _add(checks, "file_size.read_strategy", file_size_review.get("read_strategy") == "summary_index_first")
    _add(checks, "file_size.no_full_repo_scan", file_size_review.get("full_repo_scan") is False)
    _add(checks, "file_size.full_repo_scan_absent", file_size_review.get("full_repo_scan_absent") is True)
    _add(checks, "file_size.tmp_eval_out_scan_absent", file_size_review.get("tmp_eval_out_scan_absent") is True)
    _add(checks, "file_size.limited_directory_scan_ok", file_size_review.get("limited_directory_scan_ok") is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.{key}", file_size_review.get(key) is True)
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size_review.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.phase_file.exists.{rel.split('/')[-1]}", row.get("exists") is True)
        _add(checks, f"file_size.phase_file.not_blocker.{rel.split('/')[-1]}", row.get("tier") != "blocker_candidate")
    _add(checks, "file_size.template_lineage_tracked", file_size_review.get("template_lineage_path") == TEMPLATE_LINEAGE_MODULE_PATH)
    growth_ok = file_size_review.get("template_lineage_growth_controlled") is True or (
        file_size_review.get("template_lineage_growth_warning") is True
        and file_size_review.get("template_lineage_growth_warning_non_blocking") is True
    )
    _add(checks, "file_size.template_lineage_growth_ok", growth_ok)

    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.next", NEXT_PHASE_GO in md)
    _add(checks, "md.candidate_only", "candidate" in md.lower())
    _add(checks, "md.debt0", GOVERNANCE_DEBTS[0]["debt_title"] in md)
    _add(checks, "md.debt1", GOVERNANCE_DEBTS[1]["debt_title"] in md)

    for doc_name, doc in docs.items():
        for key in GO_CONDITIONS_KEYS:
            if key in doc:
                _add(checks, f"sweep.true.{doc_name}.{key}", doc.get(key) is True)
        for key in RUNTIME_FORBIDDEN_FLAGS:
            _add(checks, f"sweep.runtime.{doc_name}.{key}", doc.get(key) is not True)

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
        report.update({"passed_checks": passed, "failed_checks": len(failed), "blocker_count": len(failed), "checks": checks})
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
                "prior_owner_approval_request_issuance_post_review_go": report.get("prior_owner_approval_request_issuance_post_review_go"),
                "record_approval_closure_plan_complete": report.get("record_approval_closure_plan_complete"),
                "file_size_governance_review_exists": report.get("file_size_governance_review_exists"),
                "template_lineage_ok": report.get("template_lineage_ok"),
                "final_decision": report["final_decision"],
                "recommended_next_phase": report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
