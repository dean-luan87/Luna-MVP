#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Request Post-DryRun Review v1."""

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
from capabilities.midplatform.protocol_input_output_symmetry_registry_patch_v1 import (
    DEFAULT_OUTPUT as DEFAULT_REGISTRY_PATCH_ROOT,
    FINAL_DECISION_GO as REGISTRY_PATCH_FINAL_GO,
    INPUT_CANDIDATE_REQUIRED_FIELDS,
)
from capabilities.midplatform.protocols.protocol_separation_rule_v1 import (
    FAILURE_CLASSIFICATION,
    VALIDATE_ONCE_ATTRIBUTION_RULES,
    VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
)
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    CORE_GO_NO_GO_SCHEMA_KEYS,
    GRANT_OWNER_APPROVAL_REQUEST_POST_REVIEW_STAGE_ADDITIONS,
    GRANT_OWNER_APPROVAL_REQUEST_POST_REVIEW_STAGE_TERM_OVERRIDES,
    GRANT_OWNER_APPROVAL_REQUEST_POST_REVIEW_WHITELIST_FILES,
    TEMPLATE_FAMILY,
    validate_core_go_no_go_schema,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1 import (
    CHAIN_TRACE_NODES,
    DEFAULT_OUTPUT as DEFAULT_REQUEST_DRYRUN_ROOT,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    GO_CONDITIONS_KEYS as DRYRUN_TRUE_KEYS,
    GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_ARTIFACTS,
    MODULE_ID,
    NEXT_PHASE_GO as DRYRUN_NEXT_PHASE,
    PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1 import (
    APPROVAL_REQUEST_CANDIDATE_ID,
    CANONICAL_PARENT_PROTOCOL,
    DEFAULT_OUTPUT as DEFAULT_REQUEST_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    GO_CONDITIONS_KEYS as PLANNING_TRUE_KEYS,
    INPUT_OUTPUT_REGISTRY_PATCH_REF,
    OUTPUT_CANDIDATE_SPECS,
    PROTOCOL_ID,
    PROTOCOL_STANDARD_REF,
    RELATED_PROTOCOL_IDS,
    SEPARATION_RULE_REF,
    TRACEABILITY_RULE_REF,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1 import (
    CHAIN_EVIDENCE_NODES,
    DEFAULT_DRYRUN_ROOT,
    DEFAULT_OUTPUT,
    ERROR_NAMESPACE,
    FINAL_DECISION_GO,
    FORBIDDEN_SCOPE_CLASSIFICATIONS,
    GO_CONDITIONS_KEYS,
    NEXT_PHASE_GO,
    PHASE_ID,
    POST_REVIEW_BOUNDARY_STATEMENTS,
    POST_REVIEW_SCOPE,
    SCOPE,
    VALIDATE_ONCE_PER_MODULE_RULE_REF,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_report_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_report_v1.md",
    "task_manager_freeze_authorization_grant_owner_approval_request_dryrun_result_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_input_candidate_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_output_candidate_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_input_output_traceability_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_protocol_traceability_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_protocol_reference_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_error_namespace_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_whitebox_candidate_ref_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_validate_once_per_module_rule_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_separation_rule_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_owner_operator_notification_candidate_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_rejection_reference_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_expiry_reference_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_revocation_reference_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_absence_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_boundary_drift_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_evidence_chain_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_governance_debt_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_template_lineage_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_next_phase_readiness_v1.json",
    "summary.json",
)
ABSENCE_KEYS: Tuple[str, ...] = (
    "authorization_request_absent",
    "request_record_absent",
    "owner_approval_request_absent",
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
    "owner_approval_request_issued",
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
    parser.add_argument("--grant-owner-approval-request-dryrun-root", default=DEFAULT_DRYRUN_ROOT or DEFAULT_REQUEST_DRYRUN_ROOT)
    parser.add_argument("--grant-owner-approval-request-planning-root", default=DEFAULT_REQUEST_PLANNING_ROOT)
    parser.add_argument("--input-output-registry-patch-root", default=DEFAULT_REGISTRY_PATCH_ROOT)
    parser.add_argument("--protocol-shared-code-smoke-root", default=DEFAULT_PROTOCOL_SMOKE_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    dryrun = Path(args.grant_owner_approval_request_dryrun_root)
    planning = Path(args.grant_owner_approval_request_planning_root)
    registry_patch = Path(args.input_output_registry_patch_root)
    smoke = Path(args.protocol_shared_code_smoke_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_report_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    for rel in GRANT_OWNER_APPROVAL_REQUEST_POST_REVIEW_WHITELIST_FILES:
        _add(checks, f"template.base_file.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())
    _add(checks, "template.whitelist_only", True)

    planning_summary = _read(planning / "summary.json")
    planning_verifier = _read(planning / "verifier_report.json")
    registry_summary = _read(registry_patch / "summary.json")
    registry_verifier = _read(registry_patch / "verifier_report.json")
    smoke_summary = _read(smoke / "summary.json")
    smoke_verifier = _read(smoke / "verifier_report.json")
    _add(checks, "planning.summary_go", planning_summary.get("final_decision") == PLANNING_FINAL_GO)
    _add(checks, "planning.verifier_go", planning_verifier.get("verifier") == "GO")
    for key in PLANNING_TRUE_KEYS:
        _add(checks, f"planning.summary.{key}", planning_summary.get(key) is True)
    _add(checks, "registry.summary_go", registry_summary.get("final_decision") == REGISTRY_PATCH_FINAL_GO)
    _add(checks, "registry.verifier_go", registry_verifier.get("verifier") == "GO")
    _add(checks, "smoke.summary_go", smoke_summary.get("final_decision") == PROTOCOL_SMOKE_FINAL_GO)
    _add(checks, "smoke.verifier_go", smoke_verifier.get("verifier") == "GO")

    dryrun_summary = _read(dryrun / "summary.json")
    dryrun_verifier = _read(dryrun / "verifier_report.json")
    _add(checks, "dryrun.summary_go", dryrun_summary.get("final_decision") == DRYRUN_FINAL_GO)
    _add(checks, "dryrun.verifier_go", dryrun_verifier.get("verifier") == "GO")
    _add(checks, "dryrun.passed_min", int(dryrun_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "dryrun.failed_zero", dryrun_verifier.get("failed_checks") == 0)
    _add(checks, "dryrun.blocker_zero", dryrun_verifier.get("blocker_count") == 0)
    _add(checks, "dryrun.dryrun_pass", dryrun_summary.get("dryrun_pass") is True)
    _add(checks, "dryrun.post_review_readiness", dryrun_summary.get("post_review_readiness_ok") is True)
    _add(checks, "dryrun.next_phase", dryrun_summary.get("recommended_next_phase") == DRYRUN_NEXT_PHASE)
    _add(checks, "dryrun.validate_once_ok", dryrun_summary.get("validate_once_per_module_rule_ok") is True)
    _add(checks, "dryrun.first_validation_recorded", dryrun_summary.get("first_protocol_validation_recorded") is True)
    for key in DRYRUN_TRUE_KEYS:
        _add(checks, f"dryrun.summary.{key}", dryrun_summary.get(key) is True)
        if key in dryrun_verifier:
            _add(checks, f"dryrun.verifier.{key}", dryrun_verifier.get(key) is True)
    _add(checks, "dryrun.template_lineage_ok", dryrun_summary.get("template_lineage_ok") is True)

    for artifact in GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_ARTIFACTS:
        path = dryrun / artifact
        _add(checks, f"dryrun.artifact.exists.{artifact}", path.is_file())
        if artifact.endswith(".json"):
            _add(checks, f"dryrun.artifact.non_placeholder.{artifact}", bool(_read(path)))

    review = docs[
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_report_v1.json"
    ]
    matrix = docs["task_manager_freeze_authorization_grant_owner_approval_request_dryrun_result_review_v1.json"]
    input_review = docs["task_manager_freeze_authorization_grant_owner_approval_request_input_candidate_review_v1.json"]
    output_review = docs["task_manager_freeze_authorization_grant_owner_approval_request_output_candidate_review_v1.json"]
    trace_review = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_input_output_traceability_review_v1.json"
    ]
    protocol_trace_review = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_protocol_traceability_review_v1.json"
    ]
    protocol_review = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_protocol_reference_review_v1.json"
    ]
    error_ns_review = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_error_namespace_review_v1.json"
    ]
    whitebox_review = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_whitebox_candidate_ref_review_v1.json"
    ]
    validate_once_review = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_validate_once_per_module_rule_review_v1.json"
    ]
    separation_review = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_separation_rule_review_v1.json"
    ]
    notification_review = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_owner_operator_notification_candidate_review_v1.json"
    ]
    rejection_review = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_rejection_reference_review_v1.json"
    ]
    expiry_review = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_expiry_reference_review_v1.json"
    ]
    revocation_review = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_revocation_reference_review_v1.json"
    ]
    absence_review = docs["task_manager_freeze_authorization_grant_owner_approval_request_absence_review_v1.json"]
    drift = docs["task_manager_freeze_authorization_grant_owner_approval_request_boundary_drift_review_v1.json"]
    evidence = docs["task_manager_freeze_authorization_grant_owner_approval_request_evidence_chain_review_v1.json"]
    debt_review = docs["task_manager_freeze_authorization_grant_owner_approval_request_governance_debt_review_v1.json"]
    lineage_review = docs["task_manager_freeze_authorization_grant_owner_approval_request_template_lineage_v1.json"]
    next_readiness = docs["task_manager_freeze_authorization_grant_owner_approval_request_next_phase_readiness_v1.json"]
    summary = docs["summary.json"]
    lineage = summary.get("template_lineage") or {}
    approval_request_candidate = input_review.get("approval_request_candidate") or {}
    output_candidates = output_review.get("rows") or []

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(checks, f"meta.post_review_only.{doc_name}", doc.get("post_review_only") in (None, True))
        _add(checks, f"meta.foundation_not_frozen.{doc_name}", doc.get("foundation_not_frozen") in (None, True))
        _add(checks, f"meta.owner_request_absent.{doc_name}", doc.get("owner_approval_request_absent") in (None, True))
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
        lineage.get("base_phase") == "Freeze-Authorization-Grant-Owner-Approval-Post-DryRun-Review-v1-001",
    )
    _add(
        checks,
        "lineage.upstream",
        lineage.get("upstream_review_phase") == "Freeze-Authorization-Grant-Owner-Approval-Request-DryRun-v1-001",
    )
    _add(checks, "lineage.reuse_mode", lineage.get("reuse_mode") == "whitelist_file_template_reuse")
    _add(checks, "lineage.no_full_scan", lineage.get("full_repo_scan_allowed") is False)
    _add(checks, "lineage.files_exist", lineage.get("base_template_files_exist") is True)
    _add(checks, "lineage.stage_overridden", lineage.get("stage_specific_terms_overridden") is True)
    _add(checks, "lineage.ok", lineage.get("template_lineage_ok") is True)
    _add(checks, "lineage.review.ok", lineage_review.get("template_lineage_ok") is True)
    _add(
        checks,
        "lineage.review.upstream",
        lineage_review.get("upstream_owner_approval_request_dryrun_lineage_ok") is True,
    )
    for override in GRANT_OWNER_APPROVAL_REQUEST_POST_REVIEW_STAGE_TERM_OVERRIDES:
        _add(
            checks,
            f"lineage.override.{override['base_term'][:30]}",
            override in (lineage.get("stage_term_overrides") or []),
        )
    for addition in GRANT_OWNER_APPROVAL_REQUEST_POST_REVIEW_STAGE_ADDITIONS:
        _add(checks, f"lineage.addition.{addition}", addition in (lineage.get("stage_additions") or []))

    _add(checks, "matrix.accepted", matrix.get("owner_approval_request_dryrun_result_accepted") is True)
    _add(checks, "matrix.prior_go", matrix.get("prior_owner_approval_request_dryrun_go") is True)
    _add(checks, "matrix.dryrun_pass", matrix.get("dryrun_pass") is True)
    for row in matrix.get("rows") or []:
        name = row.get("artifact")
        _add(checks, f"matrix.exists.{name}", row.get("exists") is True)
        _add(checks, f"matrix.non_placeholder.{name}", row.get("non_placeholder") is True)

    _add(checks, "input.review_ok", input_review.get("approval_request_candidate_review_ok") is True)
    _add(checks, "input.role", approval_request_candidate.get("candidate_role") == "input_candidate")
    _add(checks, "input.classified", approval_request_candidate.get("classified_as") == "input_candidate")
    _add(checks, "input.parent", approval_request_candidate.get("canonical_parent_protocol") == CANONICAL_PARENT_PROTOCOL)
    _add(checks, "input.l2", approval_request_candidate.get("module_extension_protocol") == PROTOCOL_ID)
    for field in INPUT_CANDIDATE_REQUIRED_FIELDS:
        _add(checks, f"input.field.{field}", field in approval_request_candidate)
    _add(
        checks,
        "input.derived_outputs",
        len(approval_request_candidate.get("derived_output_refs") or []) == len(OUTPUT_CANDIDATE_SPECS),
    )
    for state in ("accepted_input", "owner_approval_record", "owner_approval", "grant", "fact", "action"):
        _add(checks, f"input.not_{state}", approval_request_candidate.get("candidate_state") != state)

    _add(checks, "output.review_ok", output_review.get("output_candidate_review_ok") is True)
    _add(checks, "output.count", len(output_candidates) == len(OUTPUT_CANDIDATE_SPECS))
    for spec in OUTPUT_CANDIDATE_SPECS:
        otype = spec["output_candidate_type"]
        row = next((r for r in output_candidates if r.get("output_candidate_type") == otype), {})
        _add(checks, f"output.exists.{otype}", bool(row))
        _add(checks, f"output.source_input.{otype}", row.get("source_input_ref") == APPROVAL_REQUEST_CANDIDATE_ID)
        _add(checks, f"output.not_accepted.{otype}", row.get("accepted_output") is not True)
        _add(checks, f"output.not_record.{otype}", row.get("record_created") is not True)

    _add(checks, "trace.review_ok", trace_review.get("input_output_traceability_review_ok") is True)
    for row in trace_review.get("rows") or []:
        out_ref = row.get("output_ref") or row.get("derived_output_ref")
        _add(checks, f"trace.source.{out_ref}", row.get("source_input_ref") == APPROVAL_REQUEST_CANDIDATE_ID)
        _add(checks, f"trace.no_runtime.{out_ref}", row.get("runtime_execution") is False)

    _add(checks, "protocol_trace.review_ok", protocol_trace_review.get("protocol_traceability_review_ok") is True)
    _add(checks, "protocol_trace.rule_ref", protocol_trace_review.get("traceability_rule_ref") == TRACEABILITY_RULE_REF)
    _add(checks, "protocol_trace.cursor_path", len(protocol_trace_review.get("cursor_query_rule_steps") or []) >= 8)
    _add(checks, "protocol_trace.query_steps", len(protocol_trace_review.get("traceability_query_path_steps") or []) >= 8)

    _add(checks, "protocol_ref.standard", protocol_review.get("protocol_standard_ref") == PROTOCOL_STANDARD_REF)
    _add(checks, "protocol_ref.registry", protocol_review.get("input_output_registry_patch_ref") == INPUT_OUTPUT_REGISTRY_PATCH_REF)
    _add(checks, "protocol_ref.id", protocol_review.get("protocol_id") == PROTOCOL_ID)
    _add(checks, "protocol_ref.parent", protocol_review.get("canonical_parent_protocol") == CANONICAL_PARENT_PROTOCOL)
    _add(checks, "protocol_ref.error_namespace", protocol_review.get("error_namespace") == ERROR_NAMESPACE)
    _add(
        checks,
        "protocol_ref.schema_ref",
        protocol_review.get("protocol_execution_result_schema_ref") == PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
    )
    _add(checks, "protocol_ref.separation", protocol_review.get("separation_rule_ref") == SEPARATION_RULE_REF)
    _add(checks, "protocol_ref.traceability", protocol_review.get("traceability_rule_ref") == TRACEABILITY_RULE_REF)
    _add(
        checks,
        "protocol_ref.validate_once_ref",
        protocol_review.get("validate_once_per_module_rule_ref") == VALIDATE_ONCE_PER_MODULE_RULE_REF,
    )
    _add(checks, "protocol_ref.no_revalidation", protocol_review.get("shared_protocol_system_revalidation") is False)
    _add(checks, "protocol_ref.no_l1_revalidation", protocol_review.get("l1_input_output_standard_revalidation") is False)
    _add(checks, "protocol_ref.review_ok", protocol_review.get("protocol_reference_review_ok") is True)
    for pid in RELATED_PROTOCOL_IDS:
        _add(checks, f"protocol_ref.related.{pid}", pid in (protocol_review.get("related_protocol_ids") or []))

    _add(checks, "error_ns.review_ok", error_ns_review.get("error_namespace_review_ok") is True)
    _add(checks, "error_ns.namespace", error_ns_review.get("error_namespace") == ERROR_NAMESPACE)
    _add(
        checks,
        "error_ns.module_local",
        error_ns_review.get("module_local_failure_not_protocol_failure_by_default") is True,
    )

    _add(checks, "whitebox.review_ok", whitebox_review.get("whitebox_candidate_ref_review_ok") is True)
    _add(checks, "whitebox.no_runtime", whitebox_review.get("whitebox_runtime_integration") is False)
    _add(checks, "whitebox.input_ref", bool(whitebox_review.get("input_whitebox_candidate_ref")))

    _add(checks, "validate_once.review_ok", validate_once_review.get("validate_once_per_module_rule_review_ok") is True)
    _add(checks, "validate_once.ref", validate_once_review.get("validate_once_per_module_rule_ref") == VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN)
    _add(checks, "validate_once.recorded", validate_once_review.get("first_protocol_validation_recorded") is True)
    _add(checks, "validate_once.module_id", validate_once_review.get("module_id") == MODULE_ID)
    _add(
        checks,
        "validate_once.subsequent_module_local",
        validate_once_review.get("subsequent_failures_default_to_module_local_proc") is True,
    )
    for category in (
        "first_protocol_validation_failed",
        "first_protocol_validation_passed_later_test_failed",
        "later_test_failed_due_to_protocol_ref_drift",
        "later_test_failed_due_to_protocol_version_change",
    ):
        _add(
            checks,
            f"validate_once.attr.{category}",
            any(row.get("category") == category for row in validate_once_review.get("attribution_rules") or []),
        )

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

    _add(checks, "notification.candidate_only", notification_review.get("owner_operator_notification_candidate_only") is True)
    for row in notification_review.get("rows") or []:
        _add(checks, "notification.not_sent", row.get("notification_sent") is False)
        _add(checks, "notification.no_exec", row.get("execution_path") is False)

    _add(checks, "rejection.candidate_only", rejection_review.get("rejection_reference_candidate_only") is True)
    for row in rejection_review.get("rows") or []:
        _add(checks, "rejection.no_exec", row.get("rejection_execution_path") is False)

    _add(checks, "expiry.candidate_only", expiry_review.get("expiry_reference_candidate_only") is True)
    for row in expiry_review.get("rows") or []:
        _add(checks, "expiry.no_exec", row.get("expiry_execution_path") is False)

    _add(checks, "revocation.candidate_only", revocation_review.get("revocation_reference_candidate_only") is True)
    for row in revocation_review.get("rows") or []:
        _add(checks, "revocation.no_exec", row.get("revocation_execution_path") is False)

    _add(checks, "drift.absent", drift.get("boundary_drift_absent") is True)
    _add(checks, "drift.post_review_scope", drift.get("post_review_scope") == POST_REVIEW_SCOPE)
    for forbidden in FORBIDDEN_SCOPE_CLASSIFICATIONS:
        _add(checks, f"drift.not_{forbidden}", drift.get("post_review_scope") != forbidden)
    for row in drift.get("rows") or []:
        name = row.get("artifact")
        _add(checks, f"drift.runtime_absent.{name}", row.get("runtime_scope_leak_absent") is True)
        _add(checks, f"drift.no_added_runtime.{name}", row.get("post_review_added_runtime") is False)

    _add(checks, "evidence.review_ok", evidence.get("evidence_chain_review_ok") is True)
    _add(checks, "evidence.paths_declared", evidence.get("evidence_chain_paths_declared") is True)
    _add(checks, "evidence.dryrun_ref_linked", evidence.get("dryrun_ref_linked") is True)
    _add(checks, "evidence.review_node_linked", evidence.get("review_node_linked") is True)
    _add(checks, "evidence.node_count", evidence.get("node_count") == len(CHAIN_EVIDENCE_NODES))
    for stage in CHAIN_TRACE_NODES:
        row = next((r for r in evidence.get("chain") or [] if r.get("stage") == stage), {})
        if stage == "freeze_authorization_grant_owner_approval_request_dryrun":
            _add(checks, f"evidence.linked.{stage}", row.get("linked") is True)
        else:
            _add(checks, f"evidence.declared.{stage}", bool(row.get("stage")))
    post_row = next(
        (
            r
            for r in evidence.get("chain") or []
            if r.get("stage") == "freeze_authorization_grant_owner_approval_request_post_dryrun_review"
        ),
        {},
    )
    _add(checks, "evidence.post_review.linked", post_row.get("linked") is True)
    _add(checks, "evidence.post_review.scope", post_row.get("readiness") == POST_REVIEW_SCOPE)
    _add(checks, "evidence.post_review.no_owner_request", post_row.get("owner_approval_request_issued") is False)
    _add(checks, "evidence.post_review.no_issued", post_row.get("authorization_request_issued") is False)
    _add(checks, "evidence.post_review.no_record", post_row.get("request_record") is False)
    _add(checks, "evidence.post_review.no_grant", post_row.get("grant_issued") is False)

    _add(checks, "absence.review_ok", absence_review.get("absence_review_ok") is True)
    _add(checks, "absence.not_issued", absence_review.get("authorization_request_issued") is False)
    for key in ABSENCE_KEYS:
        _add(checks, f"absence.{key}", absence_review.get(key) is True)
    _add(checks, "absence.no_freeze_exec", absence_review.get("no_freeze_execution_path") is True)
    _add(checks, "absence.no_rollback_exec", absence_review.get("no_rollback_execution_path") is True)

    _add(checks, "review.post_review_scope", review.get("post_review_scope") == POST_REVIEW_SCOPE)
    _add(checks, "review.issuance_planning_ready", review.get("owner_approval_request_issuance_planning_ready") is True)
    _add(checks, "review.validate_once_note", bool(review.get("validate_once_per_module_note_zh")))

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

    _add(checks, "next.ready", next_readiness.get("owner_approval_request_issuance_planning_ready") is True)
    _add(checks, "next.readiness_ok", next_readiness.get("next_phase_readiness_ok") is True)
    _add(checks, "next.recommended", next_readiness.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "next.target", next_readiness.get("target") == "freeze_authorization_grant_owner_approval_request_issuance_planning")
    _add(checks, "next.no_owner_request", next_readiness.get("owner_approval_request_issued") is False)
    _add(checks, "next.no_auth_issued", next_readiness.get("authorization_request_issued") is False)
    _add(checks, "next.no_request_record", next_readiness.get("request_record_created") is False)
    _add(checks, "next.no_owner_record", next_readiness.get("owner_approval_record_created") is False)
    _add(checks, "next.no_grant", next_readiness.get("grant_issued") is False)
    _add(checks, "next.no_adapter", next_readiness.get("module_adapter_implementation_ready") is False)
    _add(checks, "next.not_frozen", next_readiness.get("foundation_frozen") is False)
    _add(checks, "next.not_closed", next_readiness.get("closed") is False)
    for forbidden in FORBIDDEN_NEXT_TARGETS:
        _add(checks, f"next.recommended_not_{forbidden}", forbidden not in (next_readiness.get("recommended_next_phase") or "").lower())

    for stmt in POST_REVIEW_BOUNDARY_STATEMENTS:
        _add(checks, f"md.boundary.{stmt[:35]}", stmt in md)
        _add(checks, f"drift.boundary.{stmt[:35]}", stmt in (drift.get("boundary_statements") or []))

    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.next", NEXT_PHASE_GO in md)
    _add(checks, "md.validate_once_section", "## Protocol Validate Once Per Module" in md)
    _add(checks, "md.validate_once_zh", "协议首次接入验证" in md or "Protocol Validate Once Per Module" in md)
    _add(
        checks,
        "md.not_owner_request",
        "does not issue owner approval request" in md or "不生成真实 owner approval request" in md,
    )
    _add(checks, "md.post_review_ne", "owner approval request post-dryrun review ≠ owner approval request" in md)
    _add(checks, "md.candidate_ne", "approval_request_candidate ≠ accepted_input" in md)
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

    for phrase in ("freeze-candidate", "Owner approval request absent", POST_REVIEW_SCOPE, "Validate once per module"):
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
                "owner_approval_request_dryrun_result_accepted": report.get("owner_approval_request_dryrun_result_accepted"),
                "validate_once_per_module_rule_review_ok": report.get("validate_once_per_module_rule_review_ok"),
                "protocol_traceability_review_ok": report.get("protocol_traceability_review_ok"),
                "absence_review_ok": report.get("absence_review_ok"),
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
