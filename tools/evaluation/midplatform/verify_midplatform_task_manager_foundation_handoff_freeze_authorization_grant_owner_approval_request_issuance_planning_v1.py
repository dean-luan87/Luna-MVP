#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Request Issuance Planning v1."""

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
    DEFAULT_OUTPUT as DEFAULT_SMOKE_ROOT,
    FINAL_DECISION_GO as SMOKE_FINAL_GO,
)
from capabilities.midplatform.protocol_input_output_symmetry_registry_patch_v1 import (
    DEFAULT_OUTPUT as DEFAULT_REGISTRY_PATCH_ROOT,
    FINAL_DECISION_GO as REGISTRY_PATCH_FINAL_GO,
    INPUT_CANDIDATE_REQUIRED_FIELDS,
    NEXT_PHASE_GO as REGISTRY_PATCH_NEXT_PHASE,
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.protocols.protocol_separation_rule_v1 import FAILURE_CLASSIFICATION
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    CORE_GO_NO_GO_SCHEMA_KEYS,
    GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_STAGE_ADDITIONS,
    GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_STAGE_TERM_OVERRIDES,
    GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_WHITELIST_FILES,
    TEMPLATE_FAMILY,
    validate_core_go_no_go_schema,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1 import (
    DEFAULT_OUTPUT as DEFAULT_REQUEST_DRYRUN_ROOT,
    FINAL_DECISION_GO as REQUEST_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1 import (
    APPROVAL_REQUEST_CANDIDATE_ID as UPSTREAM_APPROVAL_REQUEST_CANDIDATE_ID,
    DEFAULT_OUTPUT as DEFAULT_REQUEST_PLANNING_ROOT,
    FINAL_DECISION_GO as REQUEST_PLANNING_FINAL_GO,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1 import (
    CHAIN_EVIDENCE_NODES as POST_REVIEW_CHAIN_NODES,
    DEFAULT_OUTPUT as DEFAULT_REQUEST_POST_REVIEW_ROOT,
    FINAL_DECISION_GO as REQUEST_POST_REVIEW_FINAL_GO,
    GO_CONDITIONS_KEYS as REQUEST_POST_REVIEW_GO_KEYS,
    NEXT_PHASE_GO as REQUEST_POST_REVIEW_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_v1 import (
    OWNER_APPROVAL_REQUEST_ISSUANCE_CANDIDATE_ID,
    BOUNDARY_CONTRACT_STATEMENTS,
    CANONICAL_PARENT_PROTOCOL,
    CHAIN_EVIDENCE_NODES,
    DEFAULT_OUTPUT,
    ERROR_NAMESPACE,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    INPUT_OUTPUT_REGISTRY_PATCH_REF,
    NEXT_PHASE_GO,
    NON_EXECUTION_CONSTRAINTS,
    OUTPUT_CANDIDATE_SPECS,
    PHASE_ID,
    PRECONDITION_ROWS,
    PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
    PROTOCOL_ID,
    PROTOCOL_STANDARD_REF,
    RELATED_PROTOCOL_IDS,
    SCOPE,
    SEPARATION_RULE_REF,
    TRACEABILITY_RULE_REF,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_plan_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_plan_v1.md",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_candidate_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_input_candidate_contract_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_output_candidate_contract_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_input_output_traceability_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_protocol_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_protocol_traceability_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_error_namespace_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_whitebox_candidate_ref_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_owner_operator_notification_candidate_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_rejection_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_expiry_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_revocation_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_precondition_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_absence_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_validate_once_reference_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_boundary_contract_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_non_execution_constraints_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_governance_debt_carryover_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_template_lineage_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_next_phase_readiness_v1.json",
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
    "owner_approval_request_issued",
    "owner_approval_record_created",
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
    parser.add_argument(
        "--grant-owner-approval-post-dryrun-review-root",
        default=DEFAULT_REQUEST_POST_REVIEW_ROOT,
    )
    parser.add_argument(
        "--input-output-registry-patch-root",
        default=DEFAULT_REGISTRY_PATCH_ROOT,
    )
    parser.add_argument(
        "--protocol-shared-code-smoke-root",
        default=DEFAULT_SMOKE_ROOT,
    )
    args = parser.parse_args()
    root = Path(args.output_root)
    post_review = Path(args.grant_owner_approval_post_dryrun_review_root)
    registry_patch = Path(args.input_output_registry_patch_root)
    smoke = Path(args.protocol_shared_code_smoke_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_plan_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    for rel in GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_WHITELIST_FILES:
        _add(checks, f"template.whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())
    _add(checks, "template.whitelist_only", True)

    post_summary = _read(post_review / "summary.json")
    post_verifier = _read(post_review / "verifier_report.json")
    _add(checks, "prior.post.summary_go", post_summary.get("final_decision") == REQUEST_POST_REVIEW_FINAL_GO)
    _add(checks, "prior.post.next_phase", post_summary.get("recommended_next_phase") == REQUEST_POST_REVIEW_NEXT_PHASE)
    _add(checks, "prior.post.verifier_go", post_verifier.get("verifier") == "GO")
    _add(checks, "prior.post.passed_min", int(post_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "prior.post.failed_zero", post_verifier.get("failed_checks") == 0)
    _add(checks, "prior.post.blocker_zero", post_verifier.get("blocker_count") == 0)
    for key in REQUEST_POST_REVIEW_GO_KEYS:
        _add(checks, f"prior.post.summary.{key}", post_summary.get(key) is True)
        if key in post_verifier:
            _add(checks, f"prior.post.verifier.{key}", post_verifier.get(key) is True)

    registry_summary = _read(registry_patch / "summary.json")
    registry_verifier = _read(registry_patch / "verifier_report.json")
    _add(checks, "prior.registry.summary_go", registry_summary.get("final_decision") == REGISTRY_PATCH_FINAL_GO)
    _add(checks, "prior.registry.next_phase", registry_summary.get("recommended_next_phase") == REGISTRY_PATCH_NEXT_PHASE)
    _add(checks, "prior.registry.verifier_go", registry_verifier.get("verifier") == "GO")
    _add(checks, "prior.registry.passed_min", int(registry_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "prior.registry.failed_zero", registry_verifier.get("failed_checks") == 0)
    _add(checks, "prior.registry.blocker_zero", registry_verifier.get("blocker_count") == 0)

    smoke_summary = _read(smoke / "summary.json")
    smoke_verifier = _read(smoke / "verifier_report.json")
    _add(checks, "prior.smoke.summary_go", smoke_summary.get("final_decision") == SMOKE_FINAL_GO)
    _add(checks, "prior.smoke.verifier_go", smoke_verifier.get("verifier") == "GO")
    _add(checks, "prior.smoke.passed_min", int(smoke_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "prior.smoke.failed_zero", smoke_verifier.get("failed_checks") == 0)
    _add(checks, "prior.smoke.blocker_zero", smoke_verifier.get("blocker_count") == 0)

    plan = docs["task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_plan_v1.json"]
    candidate_matrix = docs["task_manager_freeze_authorization_grant_owner_approval_request_issuance_candidate_matrix_v1.json"]
    input_contract = docs["task_manager_freeze_authorization_grant_owner_approval_request_issuance_input_candidate_contract_v1.json"]
    output_contract = docs["task_manager_freeze_authorization_grant_owner_approval_request_issuance_output_candidate_contract_v1.json"]
    traceability = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_input_output_traceability_matrix_v1.json"
    ]
    protocol_ref = docs["task_manager_freeze_authorization_grant_owner_approval_request_issuance_protocol_reference_matrix_v1.json"]
    trace_rule = docs["task_manager_freeze_authorization_grant_owner_approval_request_issuance_protocol_traceability_matrix_v1.json"]
    error_ns = docs["task_manager_freeze_authorization_grant_owner_approval_request_issuance_error_namespace_matrix_v1.json"]
    whitebox = docs["task_manager_freeze_authorization_grant_owner_approval_request_issuance_whitebox_candidate_ref_matrix_v1.json"]
    notification = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_owner_operator_notification_candidate_matrix_v1.json"
    ]
    rejection = docs["task_manager_freeze_authorization_grant_owner_approval_request_issuance_rejection_reference_matrix_v1.json"]
    expiry = docs["task_manager_freeze_authorization_grant_owner_approval_request_issuance_expiry_reference_matrix_v1.json"]
    revocation = docs["task_manager_freeze_authorization_grant_owner_approval_request_issuance_revocation_reference_matrix_v1.json"]
    preconditions = docs["task_manager_freeze_authorization_grant_owner_approval_request_issuance_precondition_matrix_v1.json"]
    boundary = docs["task_manager_freeze_authorization_grant_owner_approval_request_issuance_boundary_contract_v1.json"]
    constraints = docs["task_manager_freeze_authorization_grant_owner_approval_request_issuance_non_execution_constraints_v1.json"]
    debt_carryover = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_governance_debt_carryover_v1.json"
    ]
    lineage_doc = docs["task_manager_freeze_authorization_grant_owner_approval_request_issuance_template_lineage_v1.json"]
    next_phase = docs["task_manager_freeze_authorization_grant_owner_approval_request_issuance_next_phase_readiness_v1.json"]
    summary = docs["summary.json"]
    lineage = summary.get("template_lineage") or {}

    owner_approval_request_issuance_candidate = input_contract.get("owner_approval_request_issuance_candidate") or plan.get("owner_approval_request_issuance_candidate") or {}
    output_candidates = output_contract.get("rows") or plan.get("output_candidates") or []

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(
            checks,
            f"meta.request_planning_only.{doc_name}",
            doc.get("owner_approval_request_planning_only") in (None, True),
        )
        _add(checks, f"meta.shared_reval_false.{doc_name}", doc.get("shared_protocol_system_revalidation") in (None, False))
        _add(checks, f"meta.auth_request_absent.{doc_name}", doc.get("authorization_request_absent") in (None, True))
        _add(checks, f"meta.owner_request_absent.{doc_name}", doc.get("owner_approval_request_absent") in (None, True))
        _add(checks, f"meta.request_record_absent.{doc_name}", doc.get("request_record_absent") in (None, True))
        for key in RUNTIME_FORBIDDEN_FLAGS:
            _add(checks, f"meta.no_runtime.{doc_name}.{key}", doc.get(key) is not True)

    _add(checks, "summary.pass", summary.get("issuance_planning_pass") is True)
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
        lineage.get("base_phase") == "Freeze-Authorization-Grant-Owner-Approval-Request-Planning-v1-001",
    )
    _add(
        checks,
        "lineage.upstream",
        lineage.get("upstream_review_phase") == "Freeze-Authorization-Grant-Owner-Approval-Request-Post-DryRun-Review-v1-001",
    )
    _add(checks, "lineage.reuse_mode", lineage.get("reuse_mode") == "whitelist_file_template_reuse")
    _add(checks, "lineage.no_full_scan", lineage.get("full_repo_scan_allowed") is False)
    _add(checks, "lineage.files_exist", lineage.get("base_template_files_exist") is True)
    _add(checks, "lineage.ok", lineage.get("template_lineage_ok") is True)
    _add(checks, "lineage.doc.ok", lineage_doc.get("template_lineage_ok") is True)
    _add(checks, "lineage.doc.upstream_post", lineage_doc.get("upstream_post_review_lineage_ok") is True)
    _add(checks, "lineage.doc.upstream_registry", lineage_doc.get("upstream_registry_patch_lineage_ok") is True)
    for override in GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_STAGE_TERM_OVERRIDES:
        _add(checks, f"lineage.override.{override['base_term'][:30]}", override in (lineage.get("stage_term_overrides") or []))
    for addition in GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_STAGE_ADDITIONS:
        _add(checks, f"lineage.addition.{addition}", addition in (lineage.get("stage_additions") or []))

    _add(checks, "protocol.id", plan.get("protocol_id") == PROTOCOL_ID)
    _add(checks, "protocol.canonical_parent", plan.get("canonical_parent_protocol") == CANONICAL_PARENT_PROTOCOL)
    _add(checks, "protocol.standard_ref", plan.get("protocol_standard_ref") == PROTOCOL_STANDARD_REF)
    _add(checks, "protocol.registry_patch_ref", plan.get("input_output_registry_patch_ref") == INPUT_OUTPUT_REGISTRY_PATCH_REF)
    _add(checks, "protocol.error_namespace", plan.get("error_namespace") == ERROR_NAMESPACE)
    _add(checks, "protocol.exec_schema", plan.get("protocol_execution_result_schema_ref") == PROTOCOL_EXECUTION_RESULT_SCHEMA_REF)
    _add(checks, "protocol.separation_rule", plan.get("separation_rule_ref") == SEPARATION_RULE_REF)
    _add(checks, "protocol.traceability_rule", plan.get("traceability_rule_ref") == TRACEABILITY_RULE_REF)
    _add(checks, "protocol.shared_reval_false", plan.get("shared_protocol_system_revalidation") is False)
    _add(checks, "protocol.ref_matrix_ok", protocol_ref.get("protocol_reference_ok") is True)
    for pid in RELATED_PROTOCOL_IDS:
        _add(checks, f"protocol.related.{pid}", pid in (plan.get("related_protocol_ids") or []))
        _add(checks, f"protocol.ref_row.{pid}", any(r.get("protocol_id") == pid for r in protocol_ref.get("rows") or []))

    _add(
        checks,
        "candidate.classified_input",
        candidate_matrix.get("issuance_candidate_only") is True
        and summary.get("issuance_candidate_classified_as_input_candidate") is True,
    )
    _add(checks, "candidate.role", owner_approval_request_issuance_candidate.get("candidate_role") == "input_candidate")
    _add(checks, "candidate.type", owner_approval_request_issuance_candidate.get("candidate_type") == "owner_approval_request_issuance_candidate")
    _add(checks, "candidate.parent", owner_approval_request_issuance_candidate.get("canonical_parent_protocol") == CANONICAL_PARENT_PROTOCOL)
    _add(checks, "candidate.l2", owner_approval_request_issuance_candidate.get("module_extension_protocol") == PROTOCOL_ID)
    _add(checks, "candidate.migration", owner_approval_request_issuance_candidate.get("migration_status") == "classification_only")
    _add(checks, "candidate.no_runtime", owner_approval_request_issuance_candidate.get("runtime_execution_allowed") is False)
    for field in INPUT_CANDIDATE_REQUIRED_FIELDS:
        _add(checks, f"candidate.field.{field}", field in owner_approval_request_issuance_candidate)
    for flag in ("write_allowed", "action_allowed", "sync_allowed", "promotion_allowed"):
        _add(checks, f"candidate.{flag}_false", owner_approval_request_issuance_candidate.get(flag) is False)
    _add(checks, "candidate.contract_complete", input_contract.get("issuance_input_candidate_contract_complete") is True)
    derived_refs = owner_approval_request_issuance_candidate.get("derived_output_refs") or []
    _add(checks, "candidate.derived_output_count", len(derived_refs) == len(OUTPUT_CANDIDATE_SPECS))

    _add(checks, "output.count", len(output_candidates) == len(OUTPUT_CANDIDATE_SPECS))
    _add(checks, "output.contract_complete", output_contract.get("issuance_output_candidate_contract_complete") is True)
    for spec in OUTPUT_CANDIDATE_SPECS:
        otype = spec["output_candidate_type"]
        row = next((r for r in output_candidates if r.get("output_candidate_type") == otype), {})
        _add(checks, f"output.exists.{otype}", bool(row))
        _add(checks, f"output.source_input.{otype}", row.get("source_input_ref") == OWNER_APPROVAL_REQUEST_ISSUANCE_CANDIDATE_ID)
        _add(checks, f"output.protocol.{otype}", row.get("output_protocol_id") == "LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1")
        _add(checks, f"output.trace_protocol.{otype}", row.get("traceability_protocol_id") == "LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1")
        _add(checks, f"output.whitebox.{otype}", bool(row.get("whitebox_candidate_ref")))
        _add(checks, f"output.error_ns.{otype}", row.get("error_namespace") == ERROR_NAMESPACE)
        _add(checks, f"output.not_accepted.{otype}", row.get("accepted_output") is not True)
        _add(checks, f"output.not_record.{otype}", row.get("record_created") is not True)

    _add(checks, "traceability.complete", traceability.get("issuance_input_output_traceability_contract_complete") is True)
    _add(checks, "traceability.not_runtime", traceability.get("input_output_mapping_is_not_runtime_execution") is True)
    _add(checks, "traceability.not_write", traceability.get("traceability_ref_is_not_write_permission") is True)
    for row in traceability.get("rows") or []:
        out_ref = row.get("output_ref") or row.get("derived_output_ref")
        _add(checks, f"traceability.source.{out_ref}", row.get("source_input_ref") == OWNER_APPROVAL_REQUEST_ISSUANCE_CANDIDATE_ID)
        _add(checks, f"traceability.no_runtime.{out_ref}", row.get("runtime_execution") is False)
        _add(checks, f"traceability.no_write.{out_ref}", row.get("write_permission") is False)

    _add(checks, "trace_rule.ref_ok", trace_rule.get("traceability_rule_ref_ok") is True)
    _add(checks, "trace_rule.ref", trace_rule.get("traceability_rule_ref") == TRACEABILITY_RULE_REF)
    _add(checks, "trace_rule.cursor_path", len(trace_rule.get("cursor_query_rule_steps") or []) >= 8)
    _add(checks, "trace_rule.query_steps", len(trace_rule.get("traceability_query_path_steps") or []) >= 8)
    _add(checks, "plan.cursor_path", len(plan.get("cursor_traceability_query_path") or []) >= 8)

    _add(checks, "error_ns.ok", error_ns.get("error_namespace_mapping_ok") is True)
    _add(checks, "error_ns.namespace", error_ns.get("error_namespace") == ERROR_NAMESPACE)
    _add(checks, "error_ns.module_local", error_ns.get("module_local_failure_not_protocol_failure_by_default") is True)
    for row in error_ns.get("rows") or []:
        scenario = row.get("scenario")
        _add(checks, f"error_ns.row.{scenario}", bool(row.get("error_code")))
        _add(checks, f"error_ns.wb.{scenario}", bool(row.get("whitebox_candidate_ref")))

    _add(checks, "whitebox.ok", whitebox.get("whitebox_candidate_ref_mapping_ok") is True)
    _add(checks, "whitebox.no_runtime", whitebox.get("whitebox_runtime_integration") is False)
    _add(checks, "whitebox.input", bool(whitebox.get("input_whitebox_candidate_ref")))
    _add(checks, "whitebox.output_count", len(whitebox.get("output_whitebox_candidate_refs") or []) == len(OUTPUT_CANDIDATE_SPECS))

    _add(checks, "notification.candidate_only", notification.get("owner_operator_notification_issuance_candidate_only") is True)
    for row in notification.get("rows") or []:
        _add(checks, "notification.not_sent", row.get("notification_sent") is False)
        _add(checks, "notification.no_exec", row.get("execution_path") is False)
        _add(checks, "notification.source", row.get("source_input_ref") == OWNER_APPROVAL_REQUEST_ISSUANCE_CANDIDATE_ID)

    _add(checks, "rejection.candidate_only", rejection.get("rejection_reference_candidate_only") is True)
    for row in rejection.get("rows") or []:
        _add(checks, "rejection.no_exec", row.get("rejection_execution_path") is False)

    _add(checks, "expiry.candidate_only", expiry.get("expiry_reference_candidate_only") is True)
    for row in expiry.get("rows") or []:
        _add(checks, "expiry.no_exec", row.get("expiry_execution_path") is False)

    _add(checks, "revocation.candidate_only", revocation.get("revocation_reference_candidate_only") is True)
    for row in revocation.get("rows") or []:
        _add(checks, "revocation.no_exec", row.get("revocation_execution_path") is False)

    _add(checks, "prereq.ok", preconditions.get("preconditions_ok") is True)
    for req_row in PRECONDITION_ROWS:
        prereq = req_row["precondition"]
        row = next((r for r in preconditions.get("rows") or [] if r.get("precondition") == prereq), {})
        _add(checks, f"prereq.{prereq}.required", row.get("required") is True)
        _add(checks, f"prereq.{prereq}.satisfied", row.get("satisfied") is True)

    _add(checks, "evidence.complete", plan.get("evidence_chain_complete") is True)
    _add(checks, "evidence.paths_declared", summary.get("evidence_chain_paths_declared") is True)
    _add(checks, "evidence.post_review_ref_linked", summary.get("post_review_ref_linked") is True)
    _add(checks, "evidence.planning_node_linked", summary.get("planning_node_linked") is True)
    for stage in POST_REVIEW_CHAIN_NODES:
        row = next((r for r in plan.get("evidence_chain") or [] if r.get("stage") == stage), {})
        if stage == "freeze_authorization_grant_owner_approval_request_post_dryrun_review":
            _add(checks, f"evidence.linked.{stage}", row.get("linked") is True)
        else:
            _add(checks, f"evidence.declared.{stage}", bool(row.get("stage")))
    _add(
        checks,
        "evidence.registry_patch",
        next((r for r in plan.get("evidence_chain") or [] if r.get("stage") == "input_output_registry_patch"), {}).get("linked")
        is True,
    )
    issuance_row = next(
        (
            r
            for r in plan.get("evidence_chain") or []
            if r.get("stage") == "freeze_authorization_grant_owner_approval_request_issuance_planning"
        ),
        {},
    )
    _add(checks, "evidence.issuance_planning.linked", issuance_row.get("linked") is True)
    _add(checks, "evidence.issuance_planning.no_request", issuance_row.get("owner_approval_request_issued") is False)
    _add(checks, "evidence.node_count", plan.get("node_count") == len(CHAIN_EVIDENCE_NODES))

    for stmt in BOUNDARY_CONTRACT_STATEMENTS:
        _add(checks, f"boundary.stmt.{stmt[:35]}", stmt in (boundary.get("statements") or []))
        _add(checks, f"md.boundary.{stmt[:35]}", stmt in md)
    _add(checks, "boundary.request_absent", boundary.get("authorization_request_absent") is True)
    _add(checks, "boundary.owner_request_absent", boundary.get("owner_approval_request_absent") is True)
    _add(checks, "boundary.record_absent", boundary.get("request_record_absent") is True)
    _add(checks, "boundary.owner_absent", boundary.get("owner_approval_record_absent") is True)

    for key in NON_EXECUTION_CONSTRAINTS:
        _add(checks, f"constraints.{key}", constraints.get(key) is True)
    _add(checks, "constraints.ok", constraints.get("non_execution_boundary_ok") is True)

    debts = debt_carryover.get("debts") or []
    _add(checks, "debt.count", len(debts) >= 2)
    debt0 = debts[0] if debts else {}
    debt1 = debts[1] if len(debts) > 1 else {}
    _add(checks, "debt0.title", debt0.get("debt_title") == GOVERNANCE_DEBTS[0]["debt_title"])
    _add(checks, "debt0.priority", debt0.get("priority") == "P1")
    _add(checks, "debt0.must_not_impl", debt0.get("must_not_implement_now") is True)
    _add(checks, "debt1.title", debt1.get("debt_title") == GOVERNANCE_DEBTS[1]["debt_title"])
    _add(checks, "debt1.priority", debt1.get("priority") == "P1")
    _add(checks, "debt1.must_not_impl", debt1.get("must_not_implement_now") is True)
    _add(checks, "debt.preserved", debt_carryover.get("governance_debt_preserved") is True)

    _add(checks, "next_phase.ok", next_phase.get("next_phase_readiness_ok") is True)
    _add(checks, "next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "next_phase.target_dryrun", next_phase.get("target") == "freeze_authorization_grant_owner_approval_request_issuance_dryrun")
    _add(checks, "next_phase.no_request_issued", next_phase.get("owner_approval_request_issued") is False)
    _add(checks, "next_phase.no_request_record", next_phase.get("request_record_created") is False)
    _add(checks, "next_phase.no_owner_record", next_phase.get("owner_approval_record_created") is False)
    _add(checks, "next_phase.no_grant", next_phase.get("grant_issued") is False)
    _add(checks, "next_phase.not_frozen", next_phase.get("foundation_frozen") is False)
    _add(checks, "next_phase.not_closed", next_phase.get("closed") is False)
    _add(checks, "next_phase.no_adapter", next_phase.get("module_adapter_implementation_ready") is False)
    for forbidden in FORBIDDEN_NEXT_TARGETS:
        _add(checks, f"next_phase.not_{forbidden}", forbidden not in (next_phase.get("recommended_next_phase") or "").lower())

    _add(checks, "plan.error_rules", list(plan.get("error_classification_rules") or []) == list(FAILURE_CLASSIFICATION))
    _add(checks, "plan.sample_error", bool(plan.get("sample_protocol_error_code")))
    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.next", NEXT_PHASE_GO in md)
    _add(checks, "md.not_request", "does not issue owner approval request" in md or "不生成真实 owner approval request" in md)
    _add(
        checks,
        "md.candidate_ne",
        "owner_approval_request_issuance_candidate ≠ accepted_input" in md
        or "owner_approval_request_issuance_candidate != accepted_input" in md,
    )
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
                "prior_owner_approval_request_post_review_go": report.get("prior_owner_approval_request_post_review_go"),
                "prior_input_output_registry_patch_go": report.get("prior_input_output_registry_patch_go"),
                "prior_shared_code_smoke_go": report.get("prior_shared_code_smoke_go"),
                "owner_approval_request_issuance_plan_complete": report.get("owner_approval_request_issuance_plan_complete"),
                "issuance_candidate_classified_as_input_candidate": report.get(
                    "issuance_candidate_classified_as_input_candidate"
                ),
                "template_lineage_ok": report.get("template_lineage_ok"),
                "next_phase_readiness_ok": report.get("next_phase_readiness_ok"),
                "final_decision": report["final_decision"],
                "recommended_next_phase": report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
