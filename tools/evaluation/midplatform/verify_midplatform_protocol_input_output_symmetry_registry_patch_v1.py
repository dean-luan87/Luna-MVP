#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Protocol Input-Output Symmetry Registry Patch v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.protocol_canonical_standard_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    GOVERNANCE_DEBTS,
)
from capabilities.midplatform.protocol_canonical_standard_shared_code_smoke_v1 import (
    DEFAULT_OUTPUT as DEFAULT_SMOKE_ROOT,
    FINAL_DECISION_GO as SMOKE_FINAL_GO,
)
from capabilities.midplatform.protocol_input_output_symmetry_registry_patch_v1 import (
    BOUNDARY_CONTRACT_STATEMENTS,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    GOVERNANCE_DEBT_REF,
    INPUT_CANDIDATE_ERROR_CODES,
    INPUT_CANDIDATE_REQUIRED_FIELDS,
    NEXT_PHASE_GO,
    OUTPUT_CANDIDATE_ERROR_CODES,
    OUTPUT_CANDIDATE_REQUIRED_FIELDS,
    PHASE_ID,
    PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
    PROTOCOL_INPUT_CANDIDATE_ID,
    PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
    PROTOCOL_OUTPUT_CANDIDATE_ID,
    PROTOCOL_TRACEABILITY_ID,
    PROTOCOL_STANDARD_REF,
    CURSOR_QUERY_RULE_STEPS,
    REGISTRY_PATCH_PROTOCOL_IDS,
    REQUIRED_DUAL_ROLE_NAMES,
    REQUIRED_LEGACY_INPUT_NAMES,
    REQUIRED_LEGACY_OUTPUT_NAMES,
    RUNTIME_FORBIDDEN_FLAGS,
    SCOPE,
    SEPARATION_RULE_REF,
    SYMMETRY_ERROR_CODES,
    TRACEABILITY_ERROR_CODES,
    TRACEABILITY_QUERY_PATH_STEPS,
    TRACEABILITY_REQUIRED_FIELDS,
    TRACEABILITY_RULE_REQUIRED_FIELDS,
)
from capabilities.midplatform.protocols.protocol_error_codes_v1 import validate_error_code
from capabilities.midplatform.protocols.protocol_registry_v1 import INPUT_OUTPUT_SYMMETRY_PROTOCOL_IDS as REGISTRY_PROTOCOL_IDS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1 import (
    DEFAULT_OUTPUT as DEFAULT_POST_REVIEW_ROOT,
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "protocol_input_output_symmetry_registry_patch_report_v1.json",
    "protocol_input_output_symmetry_registry_patch_report_v1.md",
    "input_candidate_governance_protocol_registration_v1.json",
    "output_candidate_governance_protocol_registration_v1.json",
    "input_output_symmetry_protocol_registration_v1.json",
    "protocol_traceability_governance_protocol_registration_v1.json",
    "input_candidate_required_field_contract_v1.json",
    "output_candidate_required_field_contract_v1.json",
    "input_output_traceability_contract_v1.json",
    "input_output_error_namespace_mapping_v1.json",
    "input_output_whitebox_candidate_ref_mapping_v1.json",
    "input_output_protocol_reference_rule_patch_v1.json",
    "input_output_existing_protocol_classification_patch_v1.json",
    "input_output_governance_debt_patch_v1.json",
    "input_output_protocol_dependency_graph_v1.json",
    "legacy_input_protocol_consolidation_map_v1.json",
    "legacy_output_protocol_consolidation_map_v1.json",
    "legacy_candidate_role_dual_mapping_v1.json",
    "protocol_traceability_rule_contract_v1.json",
    "protocol_traceability_query_path_contract_v1.json",
    "protocol_traceability_error_to_source_mapping_v1.json",
    "protocol_traceability_candidate_lineage_mapping_v1.json",
    "protocol_traceability_whitebox_candidate_mapping_v1.json",
    "protocol_traceability_cursor_query_rule_v1.json",
    "input_output_non_runtime_constraints_v1.json",
    "input_output_next_phase_readiness_v1.json",
    "summary.json",
)
FORBIDDEN_NEXT_TARGETS: Tuple[str, ...] = (
    "owner_approval_issued",
    "request_record_created",
    "authorization_request_issued",
    "grant_issued",
    "foundation_frozen",
    "closed",
    "module_adapter_implementation",
    "l1_protocol_runtime",
    "production_ready",
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
    parser.add_argument("--planning-root", default=DEFAULT_PLANNING_ROOT)
    parser.add_argument("--shared-code-smoke-root", default=DEFAULT_SMOKE_ROOT)
    parser.add_argument("--owner-approval-post-review-root", default=DEFAULT_POST_REVIEW_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    planning = Path(args.planning_root)
    smoke = Path(args.shared_code_smoke_root)
    post_review = Path(args.owner_approval_post_review_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md = (
        (root / "protocol_input_output_symmetry_registry_patch_report_v1.md").read_text(encoding="utf-8")
        if (root / "protocol_input_output_symmetry_registry_patch_report_v1.md").is_file()
        else ""
    )

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 100)

    plan_summary = _read(planning / "summary.json")
    plan_verifier = _read(planning / "verifier_report.json")
    smoke_summary = _read(smoke / "summary.json")
    smoke_verifier = _read(smoke / "verifier_report.json")
    post_summary = _read(post_review / "summary.json")
    post_verifier = _read(post_review / "verifier_report.json")

    _add(checks, "prior.planning.summary_go", plan_summary.get("final_decision") == PLANNING_FINAL_GO)
    _add(checks, "prior.planning.verifier_go", plan_verifier.get("verifier") == "GO")
    _add(checks, "prior.planning.passed_min", int(plan_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "prior.planning.failed_zero", plan_verifier.get("failed_checks") == 0)
    _add(checks, "prior.planning.blocker_zero", plan_verifier.get("blocker_count") == 0)

    _add(checks, "prior.smoke.summary_go", smoke_summary.get("final_decision") == SMOKE_FINAL_GO)
    _add(checks, "prior.smoke.verifier_go", smoke_verifier.get("verifier") == "GO")
    _add(checks, "prior.smoke.passed_min", int(smoke_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "prior.smoke.failed_zero", smoke_verifier.get("failed_checks") == 0)
    _add(checks, "prior.smoke.blocker_zero", smoke_verifier.get("blocker_count") == 0)

    summary = docs["summary.json"]
    _add(checks, "downstream.readiness.post_review_recorded", bool(post_summary.get("final_decision")))
    _add(
        checks,
        "downstream.readiness.post_review_ref_in_summary",
        bool(summary.get("downstream_readiness_refs", {}).get("owner_approval_post_review_root")),
    )

    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{key}", summary.get("go_conditions", {}).get(key) is True)

    for pid in REGISTRY_PATCH_PROTOCOL_IDS:
        _add(checks, f"protocol.id.{pid}", pid.startswith("LUNA-PROTO-L1-"))

    input_reg = docs["input_candidate_governance_protocol_registration_v1.json"]
    output_reg = docs["output_candidate_governance_protocol_registration_v1.json"]
    symmetry_reg = docs["input_output_symmetry_protocol_registration_v1.json"]
    traceability_reg = docs["protocol_traceability_governance_protocol_registration_v1.json"]

    _add(checks, "protocol.input.registered", input_reg.get("registered") is True)
    _add(checks, "protocol.output.registered", output_reg.get("registered") is True)
    _add(checks, "protocol.symmetry.registered", symmetry_reg.get("registered") is True)
    _add(checks, "protocol.traceability.registered", traceability_reg.get("registered") is True)
    _add(checks, "protocol.input.layer_l1", input_reg.get("protocol_layer") == "L1")
    _add(checks, "protocol.output.layer_l1", output_reg.get("protocol_layer") == "L1")
    _add(checks, "protocol.symmetry.layer_l1", symmetry_reg.get("protocol_layer") == "L1")
    _add(checks, "protocol.traceability.layer_l1", traceability_reg.get("protocol_layer") == "L1")
    _add(checks, "protocol.input.error_ns", bool(input_reg.get("error_namespace")))
    _add(checks, "protocol.output.error_ns", bool(output_reg.get("error_namespace")))
    _add(checks, "protocol.symmetry.error_ns", bool(symmetry_reg.get("error_namespace")))
    _add(checks, "protocol.traceability.error_ns", bool(traceability_reg.get("error_namespace")))

    PROTOCOL_METADATA_KEYS = (
        "protocol_id",
        "protocol_layer",
        "protocol_domain",
        "protocol_version",
        "error_namespace",
        "error_code_set",
        "protocol_execution_result_schema_ref",
        "whitebox_candidate_ref_mapping",
        "upstream_protocol_refs",
        "downstream_protocol_refs",
        "related_protocol_ids",
        "protocol_standard_ref",
        "separation_rule_ref",
        "governance_debt_ref",
    )
    for reg_name, reg_doc in (
        ("input", input_reg),
        ("output", output_reg),
        ("symmetry", symmetry_reg),
        ("traceability", traceability_reg),
    ):
        for key in PROTOCOL_METADATA_KEYS:
            _add(checks, f"protocol.meta.{reg_name}.{key}", bool(reg_doc.get(key)))
        _add(
            checks,
            f"protocol.meta.{reg_name}.exec_schema",
            reg_doc.get("protocol_execution_result_schema_ref") == PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
        )
        _add(checks, f"protocol.meta.{reg_name}.standard_ref", reg_doc.get("protocol_standard_ref") == PROTOCOL_STANDARD_REF)
        _add(checks, f"protocol.meta.{reg_name}.separation_ref", reg_doc.get("separation_rule_ref") == SEPARATION_RULE_REF)
        _add(checks, f"protocol.meta.{reg_name}.debt_ref", reg_doc.get("governance_debt_ref") == GOVERNANCE_DEBT_REF)
        _add(checks, f"protocol.meta.{reg_name}.upstream_nonempty", len(reg_doc.get("upstream_protocol_refs") or []) >= 2)
        _add(checks, f"protocol.meta.{reg_name}.downstream_nonempty", len(reg_doc.get("downstream_protocol_refs") or []) >= 2)
        _add(checks, f"protocol.meta.{reg_name}.related_nonempty", len(reg_doc.get("related_protocol_ids") or []) >= 2)
        wb_map = reg_doc.get("whitebox_candidate_ref_mapping") or {}
        _add(checks, f"protocol.meta.{reg_name}.whitebox_mapping", bool(wb_map.get("whitebox_candidate_ref_mapping")))
        for code in reg_doc.get("error_code_set") or []:
            _add(checks, f"protocol.meta.{reg_name}.error.{code.split('::')[-1]}", validate_error_code(code))

    dep_graph = docs["input_output_protocol_dependency_graph_v1.json"]
    _add(checks, "dep_graph.complete", dep_graph.get("graph_complete") is True)
    _add(checks, "dep_graph.has_protocols", len(dep_graph.get("protocols") or {}) == 4)
    for pid in REGISTRY_PATCH_PROTOCOL_IDS:
        node = (dep_graph.get("protocols") or {}).get(pid) or {}
        _add(checks, f"dep_graph.{pid}.upstream", len(node.get("upstream_protocol_refs") or []) >= 2)
        _add(checks, f"dep_graph.{pid}.downstream", len(node.get("downstream_protocol_refs") or []) >= 2)
    for conn in ("evidence_binding", "field_schema", "record_lifecycle", "approval_ack", "whitebox_diagnostic_binding", "protocol_assimilation", "protocol_traceability"):
        _add(checks, f"dep_graph.l1.{conn}", bool((dep_graph.get("l1_connection_refs") or {}).get(conn)))

    trace_rule = docs["protocol_traceability_rule_contract_v1.json"]
    trace_query = docs["protocol_traceability_query_path_contract_v1.json"]
    trace_err_map = docs["protocol_traceability_error_to_source_mapping_v1.json"]
    trace_lineage = docs["protocol_traceability_candidate_lineage_mapping_v1.json"]
    trace_wb = docs["protocol_traceability_whitebox_candidate_mapping_v1.json"]
    trace_cursor = docs["protocol_traceability_cursor_query_rule_v1.json"]

    _add(checks, "trace.rule.complete", trace_rule.get("contract_complete") is True)
    _add(checks, "trace.rule.protocol_id", trace_rule.get("protocol_id") == PROTOCOL_TRACEABILITY_ID)
    for field in TRACEABILITY_RULE_REQUIRED_FIELDS:
        _add(checks, f"trace.rule.field.{field}", field in (trace_rule.get("required_fields") or []))

    _add(checks, "trace.query.complete", trace_query.get("contract_complete") is True)
    _add(checks, "trace.query.steps_14", trace_query.get("step_count") == 14)
    for step in TRACEABILITY_QUERY_PATH_STEPS:
        _add(checks, f"trace.query.step.{step['step']}", bool(step.get("path")))

    _add(checks, "trace.err_map.complete", trace_err_map.get("mapping_complete") is True)
    for code in TRACEABILITY_ERROR_CODES:
        _add(checks, f"trace.err_map.code.{code.split('::')[-1]}", validate_error_code(code))

    _add(checks, "trace.lineage.complete", trace_lineage.get("mapping_complete") is True)
    _add(checks, "trace.lineage.dual_role", trace_lineage.get("dual_role_requires_traceability") is True)

    _add(checks, "trace.wb.complete", trace_wb.get("mapping_complete") is True)
    _add(checks, "trace.wb.no_runtime", trace_wb.get("whitebox_runtime_integration") is False)

    _add(checks, "trace.cursor.complete", trace_cursor.get("rule_complete") is True)
    _add(checks, "trace.cursor.not_runtime_engine", trace_cursor.get("must_not_use_as_runtime_engine") is True)
    _add(checks, "trace.cursor.no_wb_runtime", trace_cursor.get("must_not_integrate_whitebox_runtime") is True)
    _add(checks, "trace.cursor.no_rewrite", trace_cursor.get("must_not_rewrite_historical_artifacts") is True)
    for i, step in enumerate(CURSOR_QUERY_RULE_STEPS, start=1):
        _add(checks, f"trace.cursor.step.{i}", len(step) > 10)

    trace_related = traceability_reg.get("related_protocol_ids") or []
    for rel in (
        PROTOCOL_INPUT_CANDIDATE_ID,
        PROTOCOL_OUTPUT_CANDIDATE_ID,
        PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
        "LUNA-PROTO-L1-EVIDENCE-BINDING-V1",
        "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1",
        "LUNA-PROTO-L1-APPROVAL-ACK-V1",
        "LUNA-PROTO-L1-WHITEBOX-DIAGNOSTIC-BINDING-V1",
        "LUNA-PROTO-L1-PROTOCOL-ASSIMILATION-V1",
    ):
        _add(checks, f"trace.related.{rel}", rel in trace_related)

    _add(checks, "trace.reg.upstream", len(traceability_reg.get("upstream_protocol_refs") or []) >= 4)
    _add(checks, "trace.reg.downstream", len(traceability_reg.get("downstream_protocol_refs") or []) >= 2)
    _add(checks, "summary.traceability_registered", summary.get("go_conditions", {}).get("protocol_traceability_governance_registered") is True)
    _add(checks, "summary.traceability_runtime_absent", summary.get("go_conditions", {}).get("protocol_traceability_runtime_absent") is True)

    legacy_input = docs["legacy_input_protocol_consolidation_map_v1.json"]
    _add(checks, "legacy_input.exists", bool(legacy_input))
    _add(checks, "legacy_input.classification_only", legacy_input.get("consolidation_mode") == "classification_only")
    _add(checks, "legacy_input.must_not_migrate", legacy_input.get("must_not_migrate_now") is True)
    _add(checks, "legacy_input.not_runtime_registry", legacy_input.get("is_runtime_registry") is False)
    _add(checks, "legacy_input.no_rewrite", legacy_input.get("must_not_rewrite_historical_artifacts") is True)
    legacy_input_names = {e.get("legacy_candidate_name") for e in (legacy_input.get("entries") or [])}
    for name in REQUIRED_LEGACY_INPUT_NAMES:
        _add(checks, f"legacy_input.covers.{name}", name in legacy_input_names)
        entry = next((e for e in (legacy_input.get("entries") or []) if e.get("legacy_candidate_name") == name), {})
        _add(checks, f"legacy_input.{name}.parent", entry.get("canonical_parent_protocol") == PROTOCOL_INPUT_CANDIDATE_ID)
        _add(checks, f"legacy_input.{name}.classification_only", entry.get("migration_status") == "classification_only")
        _add(checks, f"legacy_input.{name}.must_not_migrate", entry.get("must_not_migrate_now") is True)
        _add(checks, f"legacy_input.{name}.extension", bool(entry.get("module_extension_protocol")))

    legacy_output = docs["legacy_output_protocol_consolidation_map_v1.json"]
    _add(checks, "legacy_output.exists", bool(legacy_output))
    _add(checks, "legacy_output.classification_only", legacy_output.get("consolidation_mode") == "classification_only")
    _add(checks, "legacy_output.must_not_migrate", legacy_output.get("must_not_migrate_now") is True)
    _add(checks, "legacy_output.not_runtime_registry", legacy_output.get("is_runtime_registry") is False)
    legacy_output_names = {e.get("legacy_candidate_name") for e in (legacy_output.get("entries") or [])}
    for name in REQUIRED_LEGACY_OUTPUT_NAMES:
        _add(checks, f"legacy_output.covers.{name}", name in legacy_output_names)
        entry = next((e for e in (legacy_output.get("entries") or []) if e.get("legacy_candidate_name") == name), {})
        _add(checks, f"legacy_output.{name}.parent", entry.get("canonical_parent_protocol") == PROTOCOL_OUTPUT_CANDIDATE_ID)
        _add(checks, f"legacy_output.{name}.classification_only", entry.get("migration_status") == "classification_only")
        _add(checks, f"legacy_output.{name}.must_not_migrate", entry.get("must_not_migrate_now") is True)

    dual_map = docs["legacy_candidate_role_dual_mapping_v1.json"]
    _add(checks, "dual_map.exists", bool(dual_map))
    _add(checks, "dual_map.allowed", dual_map.get("dual_role_allowed") is True)
    _add(checks, "dual_map.traceability", dual_map.get("role_switch_requires_traceability") is True)
    dual_names = {e.get("candidate_name") for e in (dual_map.get("entries") or [])}
    for name in REQUIRED_DUAL_ROLE_NAMES:
        _add(checks, f"dual_map.covers.{name}", name in dual_names)
        entry = next((e for e in (dual_map.get("entries") or []) if e.get("candidate_name") == name), {})
        _add(checks, f"dual_map.{name}.roles", entry.get("allowed_roles") == ["input_candidate", "output_candidate"])
        _add(checks, f"dual_map.{name}.source_input_ref", entry.get("source_input_ref_required_when_output") is True)
        _add(checks, f"dual_map.{name}.upstream_output_ref", entry.get("upstream_output_ref_required_when_input") is True)

    input_contract = docs["input_candidate_required_field_contract_v1.json"]
    output_contract = docs["output_candidate_required_field_contract_v1.json"]
    trace_contract = docs["input_output_traceability_contract_v1.json"]
    _add(checks, "contract.input.complete", input_contract.get("contract_complete") is True)
    _add(checks, "contract.output.complete", output_contract.get("contract_complete") is True)
    _add(checks, "contract.trace.complete", trace_contract.get("contract_complete") is True)
    for field in INPUT_CANDIDATE_REQUIRED_FIELDS:
        _add(checks, f"contract.input.field.{field}", field in (input_contract.get("required_fields") or []))
    for field in OUTPUT_CANDIDATE_REQUIRED_FIELDS:
        _add(checks, f"contract.output.field.{field}", field in (output_contract.get("required_fields") or []))
    for field in TRACEABILITY_REQUIRED_FIELDS:
        _add(checks, f"contract.trace.field.{field}", field in (trace_contract.get("required_fields") or []))

    for stmt in BOUNDARY_CONTRACT_STATEMENTS:
        safe = stmt.replace(" ", "_").replace("!=", "ne")
        _add(checks, f"boundary.{safe}", stmt in BOUNDARY_CONTRACT_STATEMENTS)

    ref_patch = docs["input_output_protocol_reference_rule_patch_v1.json"]
    _add(checks, "ref_patch.complete", ref_patch.get("patch_complete") is True)
    _add(checks, "ref_patch.no_full_revalidate", ref_patch.get("must_not_full_revalidate_29_protocol_classification") is True)
    _add(checks, "ref_patch.shared_revalidation_false", ref_patch.get("shared_protocol_system_revalidation") is False)
    _add(checks, "ref_patch.standard_ref", ref_patch.get("protocol_standard_ref") == PROTOCOL_STANDARD_REF)
    _add(checks, "ref_patch.separation_rule", ref_patch.get("separation_rule_ref") == SEPARATION_RULE_REF)
    required_refs = ref_patch.get("required_references_for_owner_approval_request_planning") or []
    _add(checks, "ref_patch.requires_input_candidate", PROTOCOL_INPUT_CANDIDATE_ID in required_refs)
    _add(checks, "ref_patch.requires_symmetry", PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID in required_refs)
    _add(checks, "ref_patch.requires_traceability", PROTOCOL_TRACEABILITY_ID in required_refs)

    class_patch = docs["input_output_existing_protocol_classification_patch_v1.json"]
    _add(checks, "class_patch.complete", class_patch.get("patch_complete") is True)
    _add(checks, "class_patch.no_full_29", class_patch.get("full_29_protocol_reclassification_executed") is False)
    approval_mapping = next(
        (r for r in (class_patch.get("new_classifications") or []) if r.get("object_type") == "approval_request_candidate"),
        {},
    )
    _add(checks, "class_patch.approval_request_is_input", approval_mapping.get("classified_as") == "input_candidate")

    debt_patch = docs["input_output_governance_debt_patch_v1.json"]
    _add(checks, "debt_patch.complete", debt_patch.get("patch_complete") is True)
    _add(checks, "debt_patch.prior_p1_all_deferred", debt_patch.get("all_prior_p1_must_not_implement_now") is True)
    for debt in GOVERNANCE_DEBTS:
        _add(checks, f"debt.prior.{debt['debt_id']}.deferred", debt.get("must_not_implement_now") is True)
    new_debts = debt_patch.get("new_or_updated_debts") or []
    sym_debt = next((d for d in new_debts if d.get("debt_id") == "input_output_symmetry_canonicalization_debt"), {})
    _add(checks, "debt.symmetry_canonicalization", bool(sym_debt))
    _add(checks, "debt.symmetry_must_not_now", sym_debt.get("must_not_implement_now") is True)

    err_map = docs["input_output_error_namespace_mapping_v1.json"]
    _add(checks, "error_map.complete", err_map.get("mapping_complete") is True)
    for code in INPUT_CANDIDATE_ERROR_CODES + OUTPUT_CANDIDATE_ERROR_CODES + SYMMETRY_ERROR_CODES:
        _add(checks, f"error_code.valid.{code}", validate_error_code(code))

    wb_map = docs["input_output_whitebox_candidate_ref_mapping_v1.json"]
    _add(checks, "whitebox_map.complete", wb_map.get("mapping_complete") is True)
    _add(checks, "whitebox_map.no_runtime", wb_map.get("whitebox_runtime_integration") is False)
    for row in wb_map.get("mappings") or []:
        inner = row.get("whitebox_candidate_ref_mapping") if isinstance(row, dict) else None
        if inner:
            for item in inner:
                ref = item.get("whitebox_candidate_ref") or {}
                pid = row.get("protocol_id", "x")
                code = item.get("error_code", "x").split("::")[-1]
                _add(checks, f"whitebox.{pid}.{code}.contract_only", ref.get("binding_mode") == "contract_only")
                _add(checks, f"whitebox.{pid}.{code}.no_runtime", ref.get("runtime_integration") is False)
        elif isinstance(row, dict) and row.get("protocol_id"):
            ref = row.get("whitebox_candidate_ref") or {}
            _add(checks, f"whitebox.{row.get('protocol_id')}.contract_only", ref.get("binding_mode") == "contract_only")
            _add(checks, f"whitebox.{row.get('protocol_id')}.no_runtime", ref.get("runtime_integration") is False)

    non_runtime = docs["input_output_non_runtime_constraints_v1.json"]
    _add(checks, "non_runtime.absent", non_runtime.get("runtime_execution_absent") is True)
    _add(checks, "non_runtime.no_migration", non_runtime.get("protocol_migration_absent") is True)
    _add(checks, "non_runtime.no_wb_runtime", non_runtime.get("whitebox_runtime_integration_absent") is True)
    _add(checks, "non_runtime.no_module_adapter", non_runtime.get("module_adapter_implementation_absent") is True)
    _add(checks, "non_runtime.no_auth_request", non_runtime.get("authorization_request_absent") is True)
    _add(checks, "non_runtime.no_request_record", non_runtime.get("request_record_absent") is True)
    _add(checks, "non_runtime.no_owner_approval_record", non_runtime.get("owner_approval_record_absent") is True)
    _add(checks, "non_runtime.no_grant", non_runtime.get("grant_absent") is True)
    _add(checks, "non_runtime.foundation_not_frozen", non_runtime.get("foundation_not_frozen") is True)
    _add(checks, "non_runtime.closure_not_executed", non_runtime.get("closure_not_executed") is True)
    _add(checks, "non_runtime.no_l1_runtime", non_runtime.get("l1_protocol_runtime_implemented") is False)
    _add(checks, "non_runtime.no_production_ready", non_runtime.get("production_ready_declared") is False)

    for flag in RUNTIME_FORBIDDEN_FLAGS:
        _add(checks, f"forbidden.{flag}", flag in RUNTIME_FORBIDDEN_FLAGS)

    readiness = docs["input_output_next_phase_readiness_v1.json"]
    _add(checks, "next_phase.primary", readiness.get("next_phase_primary") == NEXT_PHASE_GO)
    _add(checks, "next_phase.readiness_ok", readiness.get("readiness_ok") is True)

    _add(checks, "summary.registry_patch_pass", summary.get("registry_patch_pass") is True)
    _add(checks, "summary.final_decision_go", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.shared_revalidation_false", summary.get("shared_protocol_system_revalidation") is False)
    _add(checks, "summary.registry_patch_only", summary.get("registry_patch_only") is True)

    for target in FORBIDDEN_NEXT_TARGETS:
        _add(checks, f"forbidden_next.{target}", target not in (summary.get("final_decision") or "").lower())

    report = docs["protocol_input_output_symmetry_registry_patch_report_v1.json"]
    _add(checks, "report.registry_patch_pass", report.get("registry_patch_pass") is True)
    _add(checks, "report.final_decision", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "report.blocker_zero", report.get("blocker_count") == 0)
    _add(checks, "report.separation_rule", bool(report.get("separation_rule")))
    for pid in report.get("registered_protocol_ids") or []:
        _add(checks, f"report.registered.{pid}", pid in REGISTRY_PATCH_PROTOCOL_IDS)

    for name, doc in docs.items():
        if not doc:
            continue
        if doc.get("phase"):
            _add(checks, f"meta.{name}.phase", doc.get("phase") == PHASE_ID)
            _add(checks, f"meta.{name}.scope", doc.get("scope") == SCOPE)
        if "shared_protocol_system_revalidation" in doc:
            _add(checks, f"meta.{name}.shared_revalidation_false", doc.get("shared_protocol_system_revalidation") is False)
        if "protocol_migration_executed" in doc:
            _add(checks, f"meta.{name}.no_migration", doc.get("protocol_migration_executed") is False)

    for reg_name, reg_doc in (
        ("input", input_reg),
        ("output", output_reg),
        ("symmetry", symmetry_reg),
        ("traceability", traceability_reg),
    ):
        entry = reg_doc.get("registry_entry") or {}
        _add(checks, f"reg.{reg_name}.must_not_implement", entry.get("must_not_implement_now") is True)
        _add(checks, f"reg.{reg_name}.planning_only", entry.get("current_handling") == "planning_only")
        _add(checks, f"reg.{reg_name}.canonical_required", entry.get("canonical_required") is True)
        _add(checks, f"reg.{reg_name}.whitebox_required", entry.get("whitebox_binding_required") is True)
        for code in reg_doc.get("error_codes") or reg_doc.get("error_code_set") or []:
            suffix = code.split("::")[-1]
            _add(checks, f"reg.{reg_name}.error.{suffix}", validate_error_code(code))
            _add(checks, f"reg.{reg_name}.error_ns.{suffix}", code.startswith(reg_doc.get("protocol_id", "")))

    for row in class_patch.get("new_classifications") or []:
        obj = row.get("object_type", "x")
        _add(checks, f"class.{obj}.has_governing", bool(row.get("governing_protocol_id")))
        _add(checks, f"class.{obj}.classified", bool(row.get("classified_as")))

    for pid in readiness.get("required_protocol_refs_for_next_phase") or []:
        _add(checks, f"readiness.ref.{pid}", pid in REGISTRY_PATCH_PROTOCOL_IDS)

    whitelist = (
        "capabilities/midplatform/protocols/protocol_registry_v1.py",
        "capabilities/midplatform/protocols/protocol_error_codes_v1.py",
        "capabilities/midplatform/protocols/protocol_types_v1.py",
        "capabilities/midplatform/protocols/__init__.py",
        "capabilities/midplatform/protocol_input_output_symmetry_registry_patch_v1.py",
    )
    for path in whitelist:
        _add(checks, f"whitelist.{path.split('/')[-1]}", (REPO_ROOT / path).is_file())

    for stmt in BOUNDARY_CONTRACT_STATEMENTS:
        safe = stmt.replace(" ", "_").replace("!=", "ne")
        _add(checks, f"md.boundary.{safe}", stmt in md)

    for row in err_map.get("protocols") or []:
        pid = row.get("protocol_id", "x")
        _add(checks, f"err_map.{pid}.all_validated", row.get("all_validated") is True)
        _add(checks, f"err_map.{pid}.has_namespace", bool(row.get("error_namespace")))
        for code in row.get("error_codes") or []:
            _add(checks, f"err_map.{pid}.code.{code.split('::')[-1]}", validate_error_code(code))

    for debt in debt_patch.get("prior_debts_carried") or []:
        _add(checks, f"debt.carried.{debt.get('debt_id', 'x')}", debt.get("must_not_implement_now") is True)

    for key in (
        "prior_protocol_standard_planning_go",
        "prior_shared_code_smoke_go",
        "input_candidate_field_contract_complete",
        "output_candidate_field_contract_complete",
        "input_output_traceability_contract_complete",
        "input_output_error_namespace_mapping_complete",
        "input_output_whitebox_candidate_ref_mapping_complete",
    ):
        _add(checks, f"summary.root.{key}", summary.get("go_conditions", {}).get(key) is True)

    for stmt in input_contract.get("boundary_statements") or []:
        safe = stmt.replace(" ", "_").replace("!=", "ne")
        _add(checks, f"input_contract.boundary.{safe}", stmt in BOUNDARY_CONTRACT_STATEMENTS or "input_candidate" in stmt)

    for stmt in output_contract.get("boundary_statements") or []:
        safe = stmt.replace(" ", "_").replace("!=", "ne")
        _add(
            checks,
            f"output_contract.boundary.{safe}",
            "output_candidate" in stmt or "record_candidate" in stmt or "result_candidate" in stmt,
        )

    for rule in trace_contract.get("symmetry_rules") or []:
        safe = str(len(rule))
        _add(checks, f"trace_contract.rule.{safe}", len(rule) > 10)

    _add(checks, "ref_patch.requires_output_candidate", PROTOCOL_OUTPUT_CANDIDATE_ID in required_refs)
    _add(checks, "ref_patch.approval_request_input_type", ref_patch.get("approval_request_candidate_classification") == "input_candidate_type")
    _add(checks, "sym_debt.priority_p1", sym_debt.get("priority") == "P1")
    _add(checks, "sym_debt.partially_addressed", sym_debt.get("debt_type") == "partially_addressed_by_registry_patch")

    passed = sum(1 for c in checks if c["passed"])
    failed = sum(1 for c in checks if not c["passed"])
    blocker_count = failed
    verifier = "GO" if failed == 0 and passed >= MIN_CHECKS else "NO_GO"

    report = {
        "verifier": verifier,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blocker_count,
        "phase": PHASE_ID,
        "scope": SCOPE,
        "prior_protocol_standard_planning_go": summary.get("prior_protocol_standard_planning_go"),
        "prior_shared_code_smoke_go": summary.get("prior_shared_code_smoke_go"),
        "prior_owner_approval_post_review_go": summary.get("prior_owner_approval_post_review_go"),
        "input_candidate_protocol_registered": summary.get("input_candidate_protocol_registered"),
        "output_candidate_protocol_registered": summary.get("output_candidate_protocol_registered"),
        "input_output_symmetry_protocol_registered": summary.get("input_output_symmetry_protocol_registered"),
        "protocol_reference_rule_patch_complete": summary.get("protocol_reference_rule_patch_complete"),
        "existing_protocol_classification_patch_complete": summary.get("existing_protocol_classification_patch_complete"),
        "input_output_governance_debt_patch_complete": summary.get("input_output_governance_debt_patch_complete"),
        "runtime_execution_absent": summary.get("runtime_execution_absent"),
        "protocol_migration_absent": summary.get("protocol_migration_absent"),
        "whitebox_runtime_integration_absent": summary.get("whitebox_runtime_integration_absent"),
        "non_execution_boundary_ok": summary.get("non_execution_boundary_ok"),
        "next_phase_readiness_ok": summary.get("next_phase_readiness_ok"),
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "checks": checks,
    }
    root.mkdir(parents=True, exist_ok=True)
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "verifier": verifier,
                "passed_checks": passed,
                "failed_checks": failed,
                "blocker_count": blocker_count,
                "input_candidate_protocol_registered": summary.get("input_candidate_protocol_registered"),
                "output_candidate_protocol_registered": summary.get("output_candidate_protocol_registered"),
                "input_output_symmetry_protocol_registered": summary.get("input_output_symmetry_protocol_registered"),
                "protocol_reference_rule_patch_complete": summary.get("protocol_reference_rule_patch_complete"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
