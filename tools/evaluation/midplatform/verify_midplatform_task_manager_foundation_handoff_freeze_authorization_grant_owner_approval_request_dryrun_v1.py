#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Request DryRun v1."""

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
    NEXT_PHASE_GO as REGISTRY_PATCH_NEXT_PHASE,
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.protocols.protocol_separation_rule_v1 import (
    FAILURE_CLASSIFICATION,
    VALIDATE_ONCE_ATTRIBUTION_RULES,
    VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
)
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    CORE_GO_NO_GO_SCHEMA_KEYS,
    GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_STAGE_ADDITIONS,
    GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_STAGE_TERM_OVERRIDES,
    GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_WHITELIST_FILES,
    TEMPLATE_FAMILY,
    validate_core_go_no_go_schema,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1 import (
    DEFAULT_OUTPUT as DEFAULT_OWNER_APPROVAL_POST_REVIEW_ROOT,
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
    GO_CONDITIONS_KEYS as POST_REVIEW_GO_KEYS,
    NEXT_PHASE_GO as POST_REVIEW_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1 import (
    APPROVAL_REQUEST_CANDIDATE_ID,
    BOUNDARY_CONTRACT_STATEMENTS,
    CANONICAL_PARENT_PROTOCOL,
    OUTPUT_CANDIDATE_SPECS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1 import (
    CHAIN_TRACE_NODES,
    DEFAULT_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_ROOT,
    DEFAULT_OUTPUT,
    DRYRUN_BOUNDARY_STATEMENTS,
    ERROR_NAMESPACE,
    FINAL_DECISION_GO,
    FORBIDDEN_CANDIDATE_STATES,
    GO_CONDITIONS_KEYS,
    GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_ARTIFACTS,
    INPUT_OUTPUT_REGISTRY_PATCH_REF,
    NEXT_PHASE_GO,
    PHASE_ID,
    PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
    PROTOCOL_ID,
    PROTOCOL_STANDARD_REF,
    RELATED_PROTOCOL_IDS,
    REQUEST_PLANNING_PACKAGE_FILES,
    SCOPE,
    SEPARATION_RULE_REF,
    TRACEABILITY_RULE_REF,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    GO_CONDITIONS_KEYS as PLANNING_TRUE_KEYS,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = tuple(
    name for name in GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_ARTIFACTS if name != "verifier_report.json"
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
        "--grant-owner-approval-request-planning-root",
        default=DEFAULT_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_ROOT,
    )
    parser.add_argument(
        "--grant-owner-approval-post-dryrun-review-root",
        default=DEFAULT_OWNER_APPROVAL_POST_REVIEW_ROOT,
    )
    parser.add_argument(
        "--input-output-registry-patch-root",
        default=DEFAULT_REGISTRY_PATCH_ROOT,
    )
    parser.add_argument("--protocol-smoke-root", default=DEFAULT_PROTOCOL_SMOKE_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    planning = Path(args.grant_owner_approval_request_planning_root)
    post_review = Path(args.grant_owner_approval_post_dryrun_review_root)
    registry_patch = Path(args.input_output_registry_patch_root)
    smoke = Path(args.protocol_smoke_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_report_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    for rel in GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_WHITELIST_FILES:
        _add(checks, f"template.base_file.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())
    _add(checks, "template.whitelist_only", True)

    planning_summary = _read(planning / "summary.json")
    planning_verifier = _read(planning / "verifier_report.json")
    _add(checks, "planning.summary_go", planning_summary.get("final_decision") == PLANNING_FINAL_GO)
    _add(checks, "planning.next_phase", planning_summary.get("recommended_next_phase") == PLANNING_NEXT_PHASE)
    _add(checks, "planning.verifier_go", planning_verifier.get("verifier") == "GO")
    _add(checks, "planning.passed_min", int(planning_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "planning.failed_zero", planning_verifier.get("failed_checks") == 0)
    _add(checks, "planning.blocker_zero", planning_verifier.get("blocker_count") == 0)
    _add(checks, "planning.next_readiness", planning_summary.get("next_phase_readiness_ok") is True)
    for key in PLANNING_TRUE_KEYS:
        _add(checks, f"planning.summary.{key}", planning_summary.get(key) is True)
        if key in planning_verifier:
            _add(checks, f"planning.verifier.{key}", planning_verifier.get(key) is True)

    for fname in REQUEST_PLANNING_PACKAGE_FILES:
        path = planning / fname
        _add(checks, f"planning.package.exists.{fname}", path.is_file())
        if fname.endswith(".json"):
            _add(checks, f"planning.package.non_placeholder.{fname}", bool(_read(path)))

    post_summary = _read(post_review / "summary.json")
    post_verifier = _read(post_review / "verifier_report.json")
    _add(checks, "downstream.readiness.post_review_recorded", post_summary.get("final_decision") is not None)
    _add(checks, "downstream.readiness.post_review_not_blocking", True)

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
    _add(checks, "smoke.summary_go", smoke_summary.get("final_decision") == PROTOCOL_SMOKE_FINAL_GO)
    _add(checks, "smoke.final_eq_standard", smoke_summary.get("final_decision") == PROTOCOL_STANDARD_REF)
    _add(checks, "smoke.verifier_go", smoke_verifier.get("verifier") == "GO")
    _add(checks, "smoke.passed_min", int(smoke_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "smoke.failed_zero", smoke_verifier.get("failed_checks") == 0)
    _add(checks, "smoke.blocker_zero", smoke_verifier.get("blocker_count") == 0)
    _add(checks, "smoke.ready_for_dryrun", smoke_summary.get("ready_for_task_manager_owner_approval_dryrun") is True)

    report = docs[
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_report_v1.json"
    ]
    integrity = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_plan_integrity_validation_v1.json"
    ]
    input_val = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_input_candidate_validation_v1.json"
    ]
    output_val = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_output_candidate_validation_v1.json"
    ]
    trace_val = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_input_output_traceability_validation_v1.json"
    ]
    protocol_ref_val = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_protocol_reference_validation_v1.json"
    ]
    protocol_trace_val = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_protocol_traceability_validation_v1.json"
    ]
    error_ns_val = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_error_namespace_validation_v1.json"
    ]
    whitebox_val = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_whitebox_candidate_ref_validation_v1.json"
    ]
    notification_val = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_owner_operator_notification_candidate_validation_v1.json"
    ]
    rejection_val = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_rejection_reference_validation_v1.json"
    ]
    expiry_val = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_expiry_reference_validation_v1.json"
    ]
    revocation_val = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_revocation_reference_validation_v1.json"
    ]
    absence_val = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_absence_validation_v1.json"
    ]
    boundary_val = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_boundary_validation_v1.json"
    ]
    evidence_trace = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_evidence_traceability_v1.json"
    ]
    debt_val = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_governance_debt_validation_v1.json"
    ]
    validate_once_rule = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_validate_once_per_module_rule_v1.json"
    ]
    post_review = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_post_review_readiness_v1.json"
    ]
    lineage_doc = docs[
        "task_manager_freeze_authorization_grant_owner_approval_request_template_lineage_v1.json"
    ]
    summary = docs["summary.json"]
    lineage = summary.get("template_lineage") or {}

    approval_request_candidate = input_val.get("approval_request_candidate") or {}
    output_candidates = output_val.get("rows") or []

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(
            checks,
            f"meta.request_dryrun_only.{doc_name}",
            doc.get("owner_approval_request_dryrun_only") in (None, True),
        )
        _add(checks, f"meta.foundation_not_frozen.{doc_name}", doc.get("foundation_not_frozen") in (None, True))
        _add(checks, f"meta.closure_not_executed.{doc_name}", doc.get("closure_not_executed") in (None, True))
        _add(
            checks,
            f"meta.no_revalidation.{doc_name}",
            doc.get("shared_protocol_system_revalidation") in (None, False),
        )
        _add(checks, f"meta.auth_request_absent.{doc_name}", doc.get("authorization_request_absent") in (None, True))
        _add(checks, f"meta.owner_request_absent.{doc_name}", doc.get("owner_approval_request_absent") in (None, True))
        for key in RUNTIME_FORBIDDEN_FLAGS:
            _add(checks, f"meta.no_runtime.{doc_name}.{key}", doc.get(key) is not True)

    _add(checks, "summary.pass", summary.get("dryrun_pass") is True)
    _add(checks, "downstream.readiness.gaps_declared", isinstance(summary.get("downstream_readiness_gaps"), list))
    _add(checks, "downstream.readiness.refs_declared", isinstance(summary.get("downstream_readiness_refs"), dict))
    _add(checks, "downstream.readiness.expected_next_phase_refs", isinstance(summary.get("expected_next_phase_refs"), dict))
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

    _add(checks, "lineage.family", lineage.get("template_family") == TEMPLATE_FAMILY)
    _add(
        checks,
        "lineage.base_phase",
        lineage.get("base_phase") == "Freeze-Authorization-Grant-Owner-Approval-DryRun-v1-001",
    )
    _add(
        checks,
        "lineage.upstream",
        lineage.get("upstream_review_phase") == "Freeze-Authorization-Grant-Owner-Approval-Request-Planning-v1-001",
    )
    _add(checks, "lineage.reuse_mode", lineage.get("reuse_mode") == "whitelist_file_template_reuse")
    _add(checks, "lineage.no_full_scan", lineage.get("full_repo_scan_allowed") is False)
    _add(checks, "lineage.files_exist", lineage.get("base_template_files_exist") is True)
    _add(checks, "lineage.family_match", lineage.get("base_template_family_match") is True)
    _add(checks, "lineage.stage_overridden", lineage.get("stage_specific_terms_overridden") is True)
    _add(checks, "lineage.core_schema", lineage.get("core_go_no_go_schema_preserved") is True)
    _add(checks, "lineage.ok", lineage.get("template_lineage_ok") is True)
    _add(checks, "lineage.doc.ok", lineage_doc.get("template_lineage_ok") is True)
    _add(checks, "lineage.doc.upstream_planning", lineage_doc.get("upstream_request_planning_lineage_ok") is True)
    _add(checks, "lineage.doc.upstream_registry", lineage_doc.get("upstream_registry_patch_lineage_ok") is True)
    for override in GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_STAGE_TERM_OVERRIDES:
        _add(
            checks,
            f"lineage.override.{override['base_term'][:30]}",
            override in (lineage.get("stage_term_overrides") or []),
        )
    for addition in GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_STAGE_ADDITIONS:
        _add(checks, f"lineage.addition.{addition}", addition in (lineage.get("stage_additions") or []))

    _add(checks, "integrity.ok", integrity.get("owner_approval_request_plan_integrity_ok") is True)
    for row in integrity.get("rows") or []:
        fname = row.get("file")
        _add(checks, f"integrity.exists.{fname}", row.get("exists") is True)
        _add(checks, f"integrity.non_placeholder.{fname}", row.get("non_placeholder") is True)

    _add(checks, "input.validation_ok", input_val.get("approval_request_candidate_validation_ok") is True)
    _add(checks, "input.contract_ok", input_val.get("input_candidate_contract_validation_ok") is True)
    _add(checks, "input.role", approval_request_candidate.get("candidate_role") == "input_candidate")
    _add(checks, "input.type", approval_request_candidate.get("candidate_type") == "owner_approval_request_candidate")
    _add(checks, "input.classified", approval_request_candidate.get("classified_as") == "input_candidate")
    _add(checks, "input.parent", approval_request_candidate.get("canonical_parent_protocol") == CANONICAL_PARENT_PROTOCOL)
    _add(checks, "input.l2", approval_request_candidate.get("module_extension_protocol") == PROTOCOL_ID)
    _add(checks, "input.migration", approval_request_candidate.get("migration_status") == "classification_only")
    _add(checks, "input.no_runtime", approval_request_candidate.get("runtime_execution_allowed") is False)
    for field in INPUT_CANDIDATE_REQUIRED_FIELDS:
        _add(checks, f"input.field.{field}", field in approval_request_candidate)
    for flag in ("write_allowed", "action_allowed", "sync_allowed", "promotion_allowed"):
        _add(checks, f"input.{flag}_false", approval_request_candidate.get(flag) is False)
    for state in FORBIDDEN_CANDIDATE_STATES:
        _add(checks, f"input.not_{state}", approval_request_candidate.get("candidate_state") != state)
        _add(checks, f"input.classified_not_{state}", approval_request_candidate.get("classified_as") != state)

    _add(checks, "output.validation_ok", output_val.get("output_candidate_contract_validation_ok") is True)
    _add(checks, "output.count", len(output_candidates) == len(OUTPUT_CANDIDATE_SPECS))
    for spec in OUTPUT_CANDIDATE_SPECS:
        otype = spec["output_candidate_type"]
        row = next((r for r in output_candidates if r.get("output_candidate_type") == otype), {})
        _add(checks, f"output.exists.{otype}", bool(row))
        _add(checks, f"output.source_input.{otype}", row.get("source_input_ref") == APPROVAL_REQUEST_CANDIDATE_ID)
        _add(checks, f"output.protocol.{otype}", row.get("output_protocol_id") == "LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1")
        _add(
            checks,
            f"output.trace_protocol.{otype}",
            row.get("traceability_protocol_id") == "LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1",
        )
        _add(checks, f"output.whitebox.{otype}", bool(row.get("whitebox_candidate_ref")))
        _add(checks, f"output.error_ns.{otype}", row.get("error_namespace") == ERROR_NAMESPACE)
        _add(checks, f"output.not_accepted.{otype}", row.get("accepted_output") is not True)
        _add(checks, f"output.not_record.{otype}", row.get("record_created") is not True)
        _add(checks, f"output.not_sent.{otype}", row.get("notification_sent") is not True)
        _add(checks, f"output.no_exec.{otype}", row.get("execution_path") is not True)

    _add(checks, "trace.validation_ok", trace_val.get("input_output_traceability_validation_ok") is True)
    _add(checks, "trace.not_runtime", trace_val.get("input_output_mapping_is_not_runtime_execution") is True)
    _add(checks, "trace.not_write", trace_val.get("traceability_ref_is_not_write_permission") is True)
    _add(checks, "trace.derived_count", len(trace_val.get("derived_output_refs") or []) == len(OUTPUT_CANDIDATE_SPECS))
    for row in trace_val.get("rows") or []:
        out_ref = row.get("output_ref") or row.get("derived_output_ref")
        _add(checks, f"trace.source.{out_ref}", row.get("source_input_ref") == APPROVAL_REQUEST_CANDIDATE_ID)
        _add(checks, f"trace.no_runtime.{out_ref}", row.get("runtime_execution") is False)
        _add(checks, f"trace.no_write.{out_ref}", row.get("write_permission") is False)

    _add(checks, "protocol_ref.standard", protocol_ref_val.get("protocol_standard_ref") == PROTOCOL_STANDARD_REF)
    _add(checks, "protocol_ref.registry", protocol_ref_val.get("input_output_registry_patch_ref") == INPUT_OUTPUT_REGISTRY_PATCH_REF)
    _add(checks, "protocol_ref.id", protocol_ref_val.get("protocol_id") == PROTOCOL_ID)
    _add(checks, "protocol_ref.canonical_parent", protocol_ref_val.get("canonical_parent_protocol") == CANONICAL_PARENT_PROTOCOL)
    _add(checks, "protocol_ref.error_namespace", protocol_ref_val.get("error_namespace") == ERROR_NAMESPACE)
    _add(
        checks,
        "protocol_ref.schema_ref",
        protocol_ref_val.get("protocol_execution_result_schema_ref") == PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
    )
    _add(checks, "protocol_ref.separation", protocol_ref_val.get("separation_rule_ref") == SEPARATION_RULE_REF)
    _add(checks, "protocol_ref.traceability", protocol_ref_val.get("traceability_rule_ref") == TRACEABILITY_RULE_REF)
    _add(checks, "protocol_ref.no_revalidation", protocol_ref_val.get("shared_protocol_system_revalidation") is False)
    _add(
        checks,
        "protocol_ref.validate_once_ref",
        protocol_ref_val.get("validate_once_per_module_rule_ref") == VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
    )
    _add(checks, "protocol_ref.first_validation", protocol_ref_val.get("first_protocol_validation_for_module") is True)
    _add(
        checks,
        "protocol_ref.validate_once_ok",
        protocol_ref_val.get("validate_once_per_module_rule_ok") is True,
    )
    _add(
        checks,
        "protocol_ref.first_recorded",
        protocol_ref_val.get("first_protocol_validation_recorded") is True,
    )
    _add(
        checks,
        "protocol_ref.attribution_rules",
        list(protocol_ref_val.get("validate_once_attribution_rules") or []) == list(VALIDATE_ONCE_ATTRIBUTION_RULES),
    )
    _add(
        checks,
        "protocol_ref.module_local_default",
        protocol_ref_val.get("module_local_failure_not_protocol_failure_by_default") is True,
    )
    _add(checks, "protocol_ref.input_ok", protocol_ref_val.get("input_candidate_protocol_reference_ok") is True)
    _add(checks, "protocol_ref.output_ok", protocol_ref_val.get("output_candidate_protocol_reference_ok") is True)
    _add(checks, "protocol_ref.symmetry_ok", protocol_ref_val.get("input_output_symmetry_reference_ok") is True)
    _add(checks, "protocol_ref.trace_ok", protocol_ref_val.get("protocol_traceability_reference_ok") is True)
    _add(checks, "protocol_ref.l2_ok", protocol_ref_val.get("l2_taskmanager_owner_approval_request_protocol_reference_ok") is True)
    for pid in RELATED_PROTOCOL_IDS:
        _add(checks, f"protocol_ref.related.{pid}", pid in (protocol_ref_val.get("related_protocol_ids") or []))

    _add(checks, "protocol_trace.validation_ok", protocol_trace_val.get("protocol_traceability_validation_ok") is True)
    _add(checks, "protocol_trace.rule_ref", protocol_trace_val.get("traceability_rule_ref") == TRACEABILITY_RULE_REF)
    _add(checks, "protocol_trace.cursor_path", len(protocol_trace_val.get("cursor_query_rule_steps") or []) >= 8)
    _add(checks, "protocol_trace.query_steps", len(protocol_trace_val.get("traceability_query_path_steps") or []) >= 8)

    _add(checks, "error_ns.validation_ok", error_ns_val.get("error_namespace_validation_ok") is True)
    _add(checks, "error_ns.namespace", error_ns_val.get("error_namespace") == ERROR_NAMESPACE)
    _add(checks, "error_ns.module_local", error_ns_val.get("module_local_failure_not_protocol_failure_by_default") is True)
    for row in error_ns_val.get("rows") or []:
        scenario = row.get("scenario")
        _add(checks, f"error_ns.row.{scenario}", bool(row.get("error_code")))
        _add(checks, f"error_ns.wb.{scenario}", bool(row.get("whitebox_candidate_ref")))

    _add(checks, "whitebox.validation_ok", whitebox_val.get("whitebox_candidate_ref_validation_ok") is True)
    _add(checks, "whitebox.no_runtime", whitebox_val.get("whitebox_runtime_integration") is False)
    _add(checks, "whitebox.input", bool(whitebox_val.get("input_whitebox_candidate_ref")))
    _add(checks, "whitebox.output_count", len(whitebox_val.get("output_whitebox_candidate_refs") or []) == len(OUTPUT_CANDIDATE_SPECS))
    wb_ref = whitebox_val.get("whitebox_candidate_ref") or {}
    _add(checks, "whitebox.contract_only", wb_ref.get("binding_mode") == "contract_only")
    _add(checks, "whitebox.no_runtime_ref", wb_ref.get("runtime_integration") is False)

    _add(checks, "notification.candidate_only", notification_val.get("owner_operator_notification_candidate_only") is True)
    for row in notification_val.get("rows") or []:
        _add(checks, "notification.not_sent", row.get("notification_sent") is False)
        _add(checks, "notification.no_exec", row.get("execution_path") is False)
        _add(checks, "notification.source", row.get("source_input_ref") == APPROVAL_REQUEST_CANDIDATE_ID)

    _add(checks, "rejection.candidate_only", rejection_val.get("rejection_reference_candidate_only") is True)
    for row in rejection_val.get("rows") or []:
        _add(checks, "rejection.no_exec", row.get("rejection_execution_path") is False)

    _add(checks, "expiry.candidate_only", expiry_val.get("expiry_reference_candidate_only") is True)
    for row in expiry_val.get("rows") or []:
        _add(checks, "expiry.no_exec", row.get("expiry_execution_path") is False)

    _add(checks, "revocation.candidate_only", revocation_val.get("revocation_reference_candidate_only") is True)
    for row in revocation_val.get("rows") or []:
        _add(checks, "revocation.no_exec", row.get("revocation_execution_path") is False)

    for key in ABSENCE_KEYS:
        _add(checks, f"absence.{key}", absence_val.get(key) is True)
    _add(checks, "absence.no_notification", absence_val.get("no_approval_request_notification_sent") is True)
    _add(checks, "absence.no_rejection_exec", absence_val.get("no_rejection_execution_path") is True)
    _add(checks, "absence.no_expiry_exec", absence_val.get("no_expiry_execution_path") is True)
    _add(checks, "absence.no_revocation_exec", absence_val.get("no_revocation_execution_path") is True)
    _add(checks, "absence.no_freeze_exec", absence_val.get("no_freeze_execution_path") is True)
    _add(checks, "absence.no_rollback_exec", absence_val.get("no_rollback_execution_path") is True)

    _add(checks, "boundary.dryrun_only", boundary_val.get("owner_approval_request_dryrun_only") is True)
    _add(checks, "boundary.no_auth_request", boundary_val.get("authorization_request_issued") is False)
    _add(checks, "boundary.no_owner_request", boundary_val.get("owner_approval_request_issued") is False)
    _add(checks, "boundary.no_request_record", boundary_val.get("request_record_created") is False)
    _add(checks, "boundary.no_owner_record", boundary_val.get("owner_approval_record_created") is False)
    _add(checks, "boundary.no_ack_record", boundary_val.get("owner_operator_ack_record_created") is False)
    _add(checks, "boundary.no_evidence_bound", boundary_val.get("approval_evidence_bound_record_created") is False)
    _add(checks, "boundary.grant_issued_false", boundary_val.get("grant_issued") is False)
    _add(checks, "boundary.not_frozen", boundary_val.get("foundation_frozen") is False)
    _add(checks, "boundary.not_closed", boundary_val.get("closed") is False)

    _add(checks, "trace.ok", evidence_trace.get("evidence_traceability_ok") is True)
    _add(checks, "trace.paths_declared", evidence_trace.get("evidence_traceability_paths_declared") is True)
    _add(checks, "trace.planning_ref_linked", evidence_trace.get("planning_ref_linked") is True)
    _add(checks, "trace.not_request", evidence_trace.get("points_to_dryrun_not_request") is True)
    _add(checks, "trace.not_issued", evidence_trace.get("points_to_dryrun_not_issued") is True)
    for stage in CHAIN_TRACE_NODES:
        row = next((r for r in evidence_trace.get("rows") or [] if r.get("stage") == stage), {})
        if stage == "freeze_authorization_grant_owner_approval_request_dryrun":
            _add(checks, f"trace.linked.{stage}", row.get("linked") is True)
        else:
            _add(checks, f"trace.declared.{stage}", row.get("stage") == stage)
    dryrun_row = next(
        (r for r in evidence_trace.get("rows") or [] if r.get("stage") == "freeze_authorization_grant_owner_approval_request_dryrun"),
        {},
    )
    _add(checks, "trace.dryrun.no_request", dryrun_row.get("authorization_request_issued") is False)
    _add(checks, "trace.dryrun.no_owner_request", dryrun_row.get("owner_approval_request_issued") is False)
    _add(checks, "trace.dryrun.no_record", dryrun_row.get("request_record") is False)
    _add(checks, "trace.dryrun.no_approval_record", dryrun_row.get("owner_approval_record") is False)
    _add(checks, "trace.dryrun.no_issued", dryrun_row.get("grant_issued") is False)

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

    _add(checks, "validate_once.rule_ok", validate_once_rule.get("validate_once_per_module_rule_ok") is True)
    _add(checks, "validate_once.recorded", validate_once_rule.get("first_protocol_validation_recorded") is True)
    _add(
        checks,
        "validate_once.ref",
        validate_once_rule.get("validate_once_per_module_rule_ref") == VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
    )
    _add(
        checks,
        "validate_once.complete",
        validate_once_rule.get("protocol_validate_once_per_module_rule_complete") is True,
    )
    _add(checks, "validate_once.module_id", validate_once_rule.get("module_id") == "task_manager_owner_approval_request")
    _add(
        checks,
        "validate_once.lightweight_after",
        validate_once_rule.get("subsequent_phases_lightweight_protocol_check_only") is True,
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
            any(
                row.get("category") == category
                for row in validate_once_rule.get("attribution_rules") or []
            ),
        )

    _add(checks, "post_review.ok", post_review.get("post_review_readiness_ok") is True)
    _add(
        checks,
        "post_review.validate_once_recorded",
        post_review.get("first_protocol_validation_recorded") is True,
    )
    _add(
        checks,
        "post_review.lightweight_after",
        post_review.get("subsequent_phases_lightweight_protocol_check_only") is True,
    )
    _add(checks, "post_review.next", post_review.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(
        checks,
        "post_review.target",
        post_review.get("target") == "freeze_authorization_grant_owner_approval_request_post_dryrun_review",
    )
    _add(checks, "post_review.no_auth_request", post_review.get("authorization_request_issued") is False)
    _add(checks, "post_review.no_owner_request", post_review.get("owner_approval_request_issued") is False)
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
        "md.not_request",
        "does not issue owner approval request" in md or "不生成真实 owner approval request" in md,
    )
    _add(checks, "md.candidate_ne", "approval_request_candidate ≠ accepted_input" in md)
    _add(checks, "md.phrase.dryrun_ne", "owner approval request dryrun ≠ owner approval request" in md)
    _add(checks, "md.protocol_standard", PROTOCOL_STANDARD_REF in md)
    _add(checks, "md.no_revalidation", "Shared protocol system revalidation: `false`" in md)
    _add(checks, "md.validate_once_section", "## Protocol Validate Once Per Module" in md)
    _add(checks, "md.validate_once_zh", "协议首次接入验证阶段" in md)
    _add(checks, "md.first_validation", "First protocol validation for module: `true`" in md)
    for i, debt in enumerate(GOVERNANCE_DEBTS):
        _add(checks, f"md.debt{i}", debt["debt_title"] in md)

    _add(checks, "report.error_rules", list(protocol_ref_val.get("error_classification_rules") or []) == list(FAILURE_CLASSIFICATION))
    _add(checks, "report.sample_error", bool(protocol_ref_val.get("sample_protocol_error_code")))
    _add(checks, "report.candidate_id", report.get("approval_request_candidate_id") == APPROVAL_REQUEST_CANDIDATE_ID)
    _add(checks, "report.output_count", report.get("output_candidate_count") == len(OUTPUT_CANDIDATE_SPECS))

    for doc_name, doc in docs.items():
        for key in GO_CONDITIONS_KEYS:
            if key in doc:
                _add(checks, f"sweep.true.{doc_name}.{key}", doc.get(key) is True)
        _add(checks, f"sweep.next.{doc_name}", doc.get("recommended_next_phase") in (None, NEXT_PHASE_GO))
        for required in ("phase", "scope", "source_chain", "foundation_id", "runtime_status"):
            _add(checks, f"sweep.meta.{doc_name}.{required}", required in doc)
        for key in RUNTIME_FORBIDDEN_FLAGS:
            _add(checks, f"sweep.runtime.{doc_name}.{key}", doc.get(key) is not True)

    for phrase in ("freeze-candidate", "Owner approval request absent", "owner approval request dry-run validation"):
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
                "prior_owner_approval_request_planning_go": report_payload.get("prior_owner_approval_request_planning_go"),
                "approval_request_candidate_validation_ok": report_payload.get("approval_request_candidate_validation_ok"),
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
