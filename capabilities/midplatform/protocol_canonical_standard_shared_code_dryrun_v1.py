# -*- coding: utf-8 -*-
"""Luna Midplatform Protocol Canonical Standard Shared Code DryRun v1.

Validates shared protocol helper/schema/contract modules are reusable by future verifiers.
No runtime execution, no protocol migration, no whitebox runtime integration.
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.protocol_canonical_standard_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    GOVERNANCE_DEBTS,
    GO_CONDITIONS_KEYS as PLANNING_GO_KEYS,
    SHARED_CODE_MODULES,
)
from capabilities.midplatform.protocols.protocol_checker_v1 import run_protocol_checker_flow
from capabilities.midplatform.protocols.protocol_error_codes_v1 import (
    ERROR_CLASSES,
    build_error_code,
    classify_error_class,
    validate_error_code,
)
from capabilities.midplatform.protocols.protocol_execution_result_v1 import (
    ProtocolError,
    REQUIRED_RESULT_KEYS,
    build_protocol_execution_result,
    validate_protocol_execution_result,
)
from capabilities.midplatform.protocols.protocol_health_monitor_contract_v1 import (
    build_health_monitor_contract,
)
from capabilities.midplatform.protocols.protocol_registry_v1 import (
    classify_protocol_layer,
    lookup_protocol,
    register_protocol,
    validate_protocol_header,
)
from capabilities.midplatform.protocols.protocol_types_v1 import (
    ProtocolHeader,
    ProtocolLayer,
    ProtocolRegistryEntry,
    build_protocol_id,
)
from capabilities.midplatform.protocols.protocol_whitebox_binding_v1 import build_whitebox_diagnostic_ref
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Protocol-Canonical-Standard-Shared-Code-DryRun-v1-001"
SCOPE = "midplatform_protocol_canonical_standard_shared_code_dryrun_validation_only"
SOURCE_CHAIN = "midplatform_protocol_canonical_standard_shared_code_dryrun_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_PROTOCOL_CANONICAL_STANDARD_SHARED_CODE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW_OR_TASK_MANAGER_OWNER_APPROVAL_DRYRUN"
)
FINAL_DECISION_BLOCKED = "MIDPLATFORM_PROTOCOL_CANONICAL_STANDARD_SHARED_CODE_DRYRUN_BLOCKED"
NEXT_PHASE_PRIMARY = "Phase-Midplatform-Protocol-Canonical-Standard-Shared-Code-Post-DryRun-Review-v1-001"
NEXT_PHASE_ALT = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-DryRun-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_protocol_canonical_standard_shared_code_dryrun_v1_smoke_v0"
)

SHARED_CODE_WHITELIST: Tuple[str, ...] = SHARED_CODE_MODULES

BOUNDARY_STATEMENTS: Tuple[str, ...] = (
    "shared_code_dryrun != protocol_runtime_execution",
    "protocol_helper_validation != protocol_migration",
    "whitebox_binding_contract != whitebox_runtime_integration",
    "protocol_registry_validation != active_protocol_registry_runtime",
    "standard_checker_flow != runtime_checker_engine",
)

NON_EXECUTION_FLAGS: Tuple[str, ...] = (
    "runtime_execution_enabled",
    "protocol_migration_executed",
    "whitebox_runtime_integrated",
    "module_adapter_implementation_ready",
    "foundation_frozen",
    "closure_executed",
    "grant_issued",
    "owner_approval_record_created",
    "request_record_created",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_protocol_canonical_standard_planning_go",
    "shared_code_imports_ok",
    "protocol_id_builder_ok",
    "protocol_error_code_builder_ok",
    "protocol_header_validation_ok",
    "protocol_execution_result_validation_ok",
    "protocol_error_object_validation_ok",
    "protocol_registry_validation_ok",
    "protocol_checker_flow_validation_ok",
    "whitebox_binding_candidate_validation_ok",
    "health_monitor_contract_validation_ok",
    "existing_protocol_classification_reuse_ok",
    "governance_debt_preserved",
    "runtime_execution_absent",
    "protocol_migration_execution_absent",
    "whitebox_runtime_integration_absent",
    "module_adapter_implementation_absent",
    "foundation_not_frozen",
    "closure_not_executed",
    "grant_not_issued",
    "owner_approval_record_absent",
    "request_record_absent",
    "non_execution_boundary_ok",
    "post_review_readiness_ok",
)

PROTOCOL_ID_TEST_CASES: Tuple[Dict[str, str], ...] = (
    {"layer": "L1", "domain": "RECORD", "name": "LIFECYCLE", "version": "V1"},
    {"layer": "L2", "domain": "TASKMANAGER", "name": "GRANT-REQUEST-RECORD", "version": "V1"},
    {"layer": "L3", "domain": "CAPABILITY", "name": "LOCAL-VERIFIER", "version": "V1"},
)

ERROR_CODE_TEST_CASES: Tuple[Dict[str, Any], ...] = tuple(
    {"protocol_id": "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1", "error_class": cls, "number": 1}
    for cls in ERROR_CLASSES
)

HEADER_REQUIRED_FIELDS: Tuple[str, ...] = (
    "protocol_id",
    "protocol_layer",
    "protocol_domain",
    "protocol_name",
    "protocol_version",
    "governance_level",
    "error_code_namespace",
    "whitebox_binding_required",
)

ERROR_OBJECT_REQUIRED_FIELDS: Tuple[str, ...] = (
    "error_code",
    "error_class",
    "severity",
    "detected_by",
    "phase_id",
    "artifact_ref",
    "field_path",
    "expected",
    "actual",
    "whitebox_trace_ref",
    "diagnostic_node_ref",
    "recommended_action",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(out: Path, planning: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": FOUNDATION_ID,
        "runtime_status": "not_enabled",
        "shared_code_dryrun_only": True,
        "runtime_execution_enabled": False,
        "protocol_migration_executed": False,
        "whitebox_runtime_integrated": False,
        "module_adapter_implementation_ready": False,
        "foundation_frozen": False,
        "closure_executed": False,
        "grant_issued": False,
        "owner_approval_record_created": False,
        "request_record_created": False,
        "output_root": str(out),
        "planning_root": str(planning),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def _validate_imports(repo_root: Path) -> Tuple[bool, List[Dict[str, Any]]]:
    rows: List[Dict[str, Any]] = []
    all_ok = True
    module_map = {
        "protocol_types_v1": "capabilities.midplatform.protocols.protocol_types_v1",
        "protocol_error_codes_v1": "capabilities.midplatform.protocols.protocol_error_codes_v1",
        "protocol_execution_result_v1": "capabilities.midplatform.protocols.protocol_execution_result_v1",
        "protocol_registry_v1": "capabilities.midplatform.protocols.protocol_registry_v1",
        "protocol_checker_v1": "capabilities.midplatform.protocols.protocol_checker_v1",
        "protocol_whitebox_binding_v1": "capabilities.midplatform.protocols.protocol_whitebox_binding_v1",
        "protocol_health_monitor_contract_v1": "capabilities.midplatform.protocols.protocol_health_monitor_contract_v1",
    }
    for fname, mod_path in module_map.items():
        fpath = repo_root / "capabilities/midplatform/protocols" / fname.replace("_v1", "_v1.py").replace(
            "protocol_", "protocol_"
        )
        # resolve from whitelist
        whitelist_path = next((p for p in SHARED_CODE_WHITELIST if fname.replace(".py", "") in p or fname in p), "")
        exists = (repo_root / whitelist_path).is_file() if whitelist_path else False
        imported = False
        error = ""
        try:
            importlib.import_module(mod_path)
            imported = True
        except Exception as exc:  # noqa: BLE001
            error = str(exc)
            all_ok = False
        rows.append({"module": fname, "path": whitelist_path, "exists": exists, "imported": imported, "error": error})
    init_path = "capabilities/midplatform/protocols/__init__.py"
    init_exists = (repo_root / init_path).is_file()
    init_imported = False
    try:
        importlib.import_module("capabilities.midplatform.protocols")
        init_imported = True
    except Exception as exc:  # noqa: BLE001
        all_ok = False
        rows.append({"module": "__init__.py", "path": init_path, "exists": init_exists, "imported": False, "error": str(exc)})
    else:
        rows.append({"module": "__init__.py", "path": init_path, "exists": init_exists, "imported": init_imported, "error": ""})
    return all_ok and init_exists and init_imported, rows


def run_protocol_canonical_standard_shared_code_dryrun_v1(
    *,
    planning_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    planning = Path(planning_root or DEFAULT_PLANNING_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, planning)
    issues: List[str] = []

    plan_summary = _read_json(planning / "summary.json")
    plan_verifier = _read_json(planning / "verifier_report.json")
    classification_registry = _read_json(planning / "existing_protocol_classification_registry_v1.json")
    governance_debt_src = _read_json(planning / "existing_protocol_governance_debt_update_v1.json")

    prior_protocol_canonical_standard_planning_go = (
        plan_summary.get("final_decision") == PLANNING_FINAL_GO
        and plan_verifier.get("verifier") == "GO"
        and int(plan_verifier.get("passed_checks", 0)) >= 420
        and plan_verifier.get("failed_checks") == 0
        and plan_verifier.get("blocker_count") == 0
        and all(plan_summary.get(k) is True for k in PLANNING_GO_KEYS)
    )
    if not prior_protocol_canonical_standard_planning_go:
        issues.append("prior_planning_not_go")

    shared_code_imports_ok, import_rows = _validate_imports(repo_root)
    if not shared_code_imports_ok:
        issues.append("shared_code_import_gap")

    id_rows: List[Dict[str, Any]] = []
    protocol_id_builder_ok = True
    for case in PROTOCOL_ID_TEST_CASES:
        built = build_protocol_id(case["layer"], case["domain"], case["name"], case["version"])
        valid = built.startswith("LUNA-PROTO-") and f"-{case['layer']}-" in built
        id_rows.append({**case, "built_id": built, "valid": valid})
        if not valid:
            protocol_id_builder_ok = False
    if not protocol_id_builder_ok:
        issues.append("protocol_id_builder_gap")

    error_rows: List[Dict[str, Any]] = []
    protocol_error_code_builder_ok = True
    for case in ERROR_CODE_TEST_CASES:
        built = build_error_code(case["protocol_id"], case["error_class"], case["number"])
        valid = validate_error_code(built)
        classified = classify_error_class(built)
        error_rows.append(
            {
                **case,
                "built_code": built,
                "valid": valid,
                "classified": classified.value if classified else None,
            }
        )
        if not valid or classified is None:
            protocol_error_code_builder_ok = False
    if not protocol_error_code_builder_ok:
        issues.append("protocol_error_code_builder_gap")

    header_rows: List[Dict[str, Any]] = []
    protocol_header_validation_ok = True
    for layer in ("L0", "L1", "L2", "L3"):
        pid = build_protocol_id(layer, "TEST", "CONTRACT", "V1")
        header = ProtocolHeader(
            protocol_id=pid,
            protocol_layer=layer,
            protocol_domain="test_contract",
            protocol_name=f"Test {layer} Contract",
            protocol_version="v1",
            governance_level="midplatform_system_protocol" if layer in ("L0", "L1") else "module_protocol",
            error_code_namespace=f"{pid}::*",
            whitebox_binding_required=True,
            runtime_execution_allowed=False,
        )
        valid = validate_protocol_header(header)
        layer_classified = classify_protocol_layer(header.to_dict()) == layer
        header_rows.append(
            {
                "layer": layer,
                "protocol_id": pid,
                "validate_protocol_header": valid,
                "classify_protocol_layer": layer_classified,
                "fields_present": all(getattr(header, f, None) is not None for f in HEADER_REQUIRED_FIELDS if f != "error_code_namespace") and bool(header.error_code_namespace),
            }
        )
        if not valid or not layer_classified:
            protocol_header_validation_ok = False
    invalid_header = ProtocolHeader(
        protocol_id="INVALID",
        protocol_layer="L1",
        protocol_domain="x",
        protocol_name="x",
        protocol_version="v1",
        governance_level="x",
        runtime_execution_allowed=True,
    )
    header_rows.append({"layer": "invalid", "validate_protocol_header": validate_protocol_header(invalid_header) is False})
    if validate_protocol_header(invalid_header):
        protocol_header_validation_ok = False
    if not protocol_header_validation_ok:
        issues.append("protocol_header_validation_gap")

    sample_pid = "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1"
    exec_result = build_protocol_execution_result(sample_pid)
    exec_dict = exec_result.to_dict()
    inner = exec_dict.get("protocol_execution_result") or {}
    protocol_execution_result_validation_ok = validate_protocol_execution_result(exec_dict) and all(
        k in inner for k in REQUIRED_RESULT_KEYS
    )
    if not protocol_execution_result_validation_ok:
        issues.append("protocol_execution_result_gap")

    sample_error = ProtocolError(
        error_code=build_error_code(sample_pid, "CONST", 1),
        error_class="constitutional_violation",
        severity="blocker",
        detected_by="dryrun",
        phase_id=PHASE_ID,
        artifact_ref="summary.json",
        field_path="go_conditions.request_record_absent",
        expected=True,
        actual=False,
        whitebox_trace_ref="wb://dryrun",
        diagnostic_node_ref="diag://dryrun",
        recommended_action="block_and_quarantine",
    )
    error_dict = sample_error.to_dict()
    protocol_error_object_validation_ok = all(f in error_dict for f in ERROR_OBJECT_REQUIRED_FIELDS)
    if not protocol_error_object_validation_ok:
        issues.append("protocol_error_object_gap")

    registry_rows: List[Dict[str, Any]] = []
    protocol_registry_validation_ok = True
    test_entries = [
        ProtocolRegistryEntry(
            protocol_name="Record Lifecycle Protocol",
            suggested_protocol_id="LUNA-PROTO-L1-RECORD-LIFECYCLE-V1",
            layer="L1",
            domain="record_lifecycle",
            status="dryrun_test",
            current_handling="local_registry_only",
            canonical_required=True,
            module_extension_allowed=True,
            whitebox_binding_required=True,
            error_namespace="LUNA-PROTO-L1-RECORD-LIFECYCLE-V1::*",
            must_not_implement_now=True,
        ),
        ProtocolRegistryEntry(
            protocol_name="Task Manager Grant Request Record Protocol",
            suggested_protocol_id="LUNA-PROTO-L2-TASKMANAGER-GRANT-REQUEST-RECORD-V1",
            layer="L2",
            domain="taskmanager",
            status="dryrun_test",
            current_handling="local_registry_only",
            canonical_required=True,
            module_extension_allowed=True,
            whitebox_binding_required=True,
            error_namespace="LUNA-PROTO-L2-TASKMANAGER-GRANT-REQUEST-RECORD-V1::*",
            must_not_implement_now=True,
        ),
        ProtocolRegistryEntry(
            protocol_name="Local Verifier Capability Contract",
            suggested_protocol_id="LUNA-PROTO-L3-CAPABILITY-LOCAL-VERIFIER-V1",
            layer="L3",
            domain="capability",
            status="dryrun_test",
            current_handling="local_registry_only",
            canonical_required=True,
            module_extension_allowed=False,
            whitebox_binding_required=True,
            error_namespace="LUNA-PROTO-L3-CAPABILITY-LOCAL-VERIFIER-V1::*",
            must_not_implement_now=True,
        ),
    ]
    for entry in test_entries:
        registered = register_protocol(entry)
        looked_up = lookup_protocol(entry.suggested_protocol_id)
        ok = looked_up is not None and looked_up.get("suggested_protocol_id") == entry.suggested_protocol_id
        registry_rows.append(
            {
                "layer": entry.layer,
                "protocol_id": entry.suggested_protocol_id,
                "register_ok": bool(registered),
                "lookup_ok": ok,
                "migration_executed": False,
            }
        )
        if not ok:
            protocol_registry_validation_ok = False
    if not protocol_registry_validation_ok:
        issues.append("protocol_registry_gap")

    checker_result = run_protocol_checker_flow(
        protocol_id=sample_pid,
        constitution_violations=None,
        artifacts_complete=True,
        upstream_go=True,
        evidence_chain_complete=True,
        schema_valid=True,
        naming_valid=True,
        drift_detected=False,
        whitebox_trace_ref="wb://dryrun-check",
        whitebox_diagnostic_ref="diag://dryrun-check",
    )
    checker_inner = checker_result.get("protocol_execution_result") or {}
    protocol_checker_flow_validation_ok = (
        validate_protocol_execution_result(checker_result)
        and checker_inner.get("overall_result") == "PASS"
        and "runtime" not in json.dumps(checker_result).lower()
    )
    if not protocol_checker_flow_validation_ok:
        issues.append("protocol_checker_flow_gap")

    wb_ref = build_whitebox_diagnostic_ref(
        phase_id=PHASE_ID,
        protocol_id=sample_pid,
        error_code=build_error_code(sample_pid, "WB", 1),
        artifact_ref="summary.json",
        field_path="go_conditions.whitebox_binding_candidate_validation_ok",
    )
    whitebox_binding_candidate_validation_ok = (
        wb_ref.get("binding_mode") == "contract_only"
        and wb_ref.get("runtime_integration") is False
        and wb_ref.get("whitebox_trace_ref", "").startswith("wb://")
        and wb_ref.get("diagnostic_node_ref", "").startswith("diag://")
    )
    if not whitebox_binding_candidate_validation_ok:
        issues.append("whitebox_binding_gap")

    health_contract = build_health_monitor_contract(sample_pid)
    health_monitor_contract_validation_ok = (
        health_contract.get("runtime_monitoring_enabled") is False
        and health_contract.get("supervision_mode") == "planning_contract_only"
        and bool(health_contract.get("dimensions"))
    )
    if not health_monitor_contract_validation_ok:
        issues.append("health_monitor_gap")

    all_entries = (
        (classification_registry.get("L1_system_protocols") or [])
        + (classification_registry.get("L2_task_manager_protocols") or [])
        + (classification_registry.get("L2_future_module_protocols") or [])
    )
    wb_map_src = _read_json(planning / "existing_protocol_whitebox_binding_candidate_map_v1.json")
    wb_entries = {e.get("protocol_id"): e for e in (wb_map_src.get("entries") or [])}
    classification_rows: List[Dict[str, Any]] = []
    existing_protocol_classification_reuse_ok = len(all_entries) >= 29
    for entry in all_entries:
        pid = entry.get("suggested_protocol_id", "")
        ns = entry.get("error_namespace", "")
        wb = wb_entries.get(pid, {})
        row_ok = bool(pid) and bool(ns) and pid.startswith("LUNA-PROTO-") and bool(wb.get("whitebox_binding_candidate"))
        classification_rows.append(
            {
                "protocol_id": pid,
                "error_namespace": ns,
                "whitebox_binding_candidate": wb.get("whitebox_binding_candidate"),
                "mapped_ok": row_ok,
            }
        )
        if not row_ok:
            existing_protocol_classification_reuse_ok = False
    if not existing_protocol_classification_reuse_ok:
        issues.append("classification_reuse_gap")

    debts = governance_debt_src.get("debts") or list(GOVERNANCE_DEBTS)
    required_titles = [d["debt_title"] for d in GOVERNANCE_DEBTS]
    debt_rows: List[Dict[str, Any]] = []
    governance_debt_preserved = len(debts) >= 6
    for title in required_titles:
        match = next((d for d in debts if d.get("debt_title") == title), {})
        ok = (
            bool(match)
            and match.get("priority") == "P1"
            and match.get("classification") == "L1 Midplatform System Protocols"
            and match.get("must_not_implement_now") is True
        )
        debt_rows.append({"debt_title": title, "preserved": ok, **{k: match.get(k) for k in ("priority", "must_not_implement_now")}})
        if not ok:
            governance_debt_preserved = False
    if not governance_debt_preserved:
        issues.append("governance_debt_gap")

    runtime_execution_absent = meta["runtime_execution_enabled"] is False
    protocol_migration_execution_absent = meta["protocol_migration_executed"] is False
    whitebox_runtime_integration_absent = meta["whitebox_runtime_integrated"] is False
    module_adapter_implementation_absent = meta["module_adapter_implementation_ready"] is False
    foundation_not_frozen = meta["foundation_frozen"] is False
    closure_not_executed = meta["closure_executed"] is False
    grant_not_issued = meta["grant_issued"] is False
    owner_approval_record_absent = meta["owner_approval_record_created"] is False
    request_record_absent = meta["request_record_created"] is False
    non_execution_boundary_ok = all(meta.get(f) is False for f in NON_EXECUTION_FLAGS)

    post_review_readiness_ok = (
        prior_protocol_canonical_standard_planning_go
        and shared_code_imports_ok
        and protocol_id_builder_ok
        and protocol_error_code_builder_ok
        and protocol_header_validation_ok
        and protocol_execution_result_validation_ok
        and protocol_error_object_validation_ok
        and protocol_registry_validation_ok
        and protocol_checker_flow_validation_ok
        and whitebox_binding_candidate_validation_ok
        and health_monitor_contract_validation_ok
        and existing_protocol_classification_reuse_ok
        and governance_debt_preserved
        and non_execution_boundary_ok
    )

    go_values = {
        "prior_protocol_canonical_standard_planning_go": prior_protocol_canonical_standard_planning_go,
        "shared_code_imports_ok": shared_code_imports_ok,
        "protocol_id_builder_ok": protocol_id_builder_ok,
        "protocol_error_code_builder_ok": protocol_error_code_builder_ok,
        "protocol_header_validation_ok": protocol_header_validation_ok,
        "protocol_execution_result_validation_ok": protocol_execution_result_validation_ok,
        "protocol_error_object_validation_ok": protocol_error_object_validation_ok,
        "protocol_registry_validation_ok": protocol_registry_validation_ok,
        "protocol_checker_flow_validation_ok": protocol_checker_flow_validation_ok,
        "whitebox_binding_candidate_validation_ok": whitebox_binding_candidate_validation_ok,
        "health_monitor_contract_validation_ok": health_monitor_contract_validation_ok,
        "existing_protocol_classification_reuse_ok": existing_protocol_classification_reuse_ok,
        "governance_debt_preserved": governance_debt_preserved,
        "runtime_execution_absent": runtime_execution_absent,
        "protocol_migration_execution_absent": protocol_migration_execution_absent,
        "whitebox_runtime_integration_absent": whitebox_runtime_integration_absent,
        "module_adapter_implementation_absent": module_adapter_implementation_absent,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "grant_not_issued": grant_not_issued,
        "owner_approval_record_absent": owner_approval_record_absent,
        "request_record_absent": request_record_absent,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "post_review_readiness_ok": post_review_readiness_ok,
    }

    dryrun_pass = len(issues) == 0 and all(go_values.values())
    final_decision = FINAL_DECISION_GO if dryrun_pass else FINAL_DECISION_BLOCKED
    next_phase = NEXT_PHASE_PRIMARY if dryrun_pass else "Phase-Midplatform-Protocol-Canonical-Standard-Shared-Code-DryRun-Issue-Review-v1-001"

    dryrun_report = {
        "report_id": "protocol_shared_code_dryrun_report_v1",
        "boundary_statements": list(BOUNDARY_STATEMENTS),
        "whitelist_modules": list(SHARED_CODE_WHITELIST),
        "validation_summary": go_values,
        "issues": issues,
        "dryrun_pass": dryrun_pass,
        "final_decision": final_decision,
        "recommended_next_phase_primary": NEXT_PHASE_PRIMARY,
        "recommended_next_phase_alt": NEXT_PHASE_ALT,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_pass": dryrun_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "go_conditions": go_values,
        "final_decision": final_decision,
        "recommended_next_phase_primary": NEXT_PHASE_PRIMARY,
        "recommended_next_phase_alt": NEXT_PHASE_ALT,
        **go_values,
        **meta,
    }

    markdown = "\n".join(
        [
            "# Protocol Shared Code DryRun Report v1",
            "",
            "This phase validates shared protocol helper/schema/contract modules only. It does not execute protocol runtime or migrate historical protocols.",
            "",
            "本阶段仅执行 shared code dry-run validation，不实现协议 runtime，不迁移历史协议，不接入真实 whitebox。",
            "",
            f"Prior planning GO: `{prior_protocol_canonical_standard_planning_go}`",
            f"Shared code imports OK: `{shared_code_imports_ok}`",
            f"Protocol ID builder OK: `{protocol_id_builder_ok}`",
            f"Error code builder OK: `{protocol_error_code_builder_ok}`",
            f"Checker flow OK: `{protocol_checker_flow_validation_ok}`",
            f"Classification reuse OK (29 protocols): `{existing_protocol_classification_reuse_ok}`",
            f"Governance debt preserved: `{governance_debt_preserved}`",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{next_phase}`",
            "",
            "## Boundary Statements",
            *[f"- {s}" for s in BOUNDARY_STATEMENTS],
        ]
    )

    return {
        "protocol_shared_code_dryrun_report": dryrun_report,
        "protocol_shared_code_dryrun_report_md": markdown,
        "protocol_shared_code_import_validation": {
            "validation_id": "protocol_shared_code_import_validation_v1",
            "rows": import_rows,
            "shared_code_imports_ok": shared_code_imports_ok,
            **meta,
        },
        "protocol_id_builder_validation": {
            "validation_id": "protocol_id_builder_validation_v1",
            "format": "LUNA-PROTO-{LAYER}-{DOMAIN}-{NAME}-V{VERSION}",
            "rows": id_rows,
            "protocol_id_builder_ok": protocol_id_builder_ok,
            **meta,
        },
        "protocol_error_code_builder_validation": {
            "validation_id": "protocol_error_code_builder_validation_v1",
            "format": "{PROTOCOL_ID}::{ERROR_CLASS}-{NUMBER}",
            "error_classes": list(ERROR_CLASSES),
            "rows": error_rows,
            "protocol_error_code_builder_ok": protocol_error_code_builder_ok,
            **meta,
        },
        "protocol_header_validation": {
            "validation_id": "protocol_header_validation_v1",
            "required_fields": list(HEADER_REQUIRED_FIELDS),
            "rows": header_rows,
            "protocol_header_validation_ok": protocol_header_validation_ok,
            **meta,
        },
        "protocol_execution_result_validation": {
            "validation_id": "protocol_execution_result_validation_v1",
            "required_keys": list(REQUIRED_RESULT_KEYS),
            "example": exec_dict,
            "protocol_execution_result_validation_ok": protocol_execution_result_validation_ok,
            **meta,
        },
        "protocol_error_object_validation": {
            "validation_id": "protocol_error_object_validation_v1",
            "required_fields": list(ERROR_OBJECT_REQUIRED_FIELDS),
            "example": error_dict,
            "protocol_error_object_validation_ok": protocol_error_object_validation_ok,
            **meta,
        },
        "protocol_registry_validation": {
            "validation_id": "protocol_registry_validation_v1",
            "local_registry_only": True,
            "protocol_migration_executed": False,
            "rows": registry_rows,
            "protocol_registry_validation_ok": protocol_registry_validation_ok,
            **meta,
        },
        "protocol_checker_flow_validation": {
            "validation_id": "protocol_checker_flow_validation_v1",
            "dryrun_helper_only": True,
            "runtime_triggered": False,
            "result": checker_result,
            "protocol_checker_flow_validation_ok": protocol_checker_flow_validation_ok,
            **meta,
        },
        "protocol_whitebox_binding_candidate_validation": {
            "validation_id": "protocol_whitebox_binding_candidate_validation_v1",
            "candidate_ref_only": True,
            "example": wb_ref,
            "whitebox_binding_candidate_validation_ok": whitebox_binding_candidate_validation_ok,
            **meta,
        },
        "protocol_health_monitor_contract_validation": {
            "validation_id": "protocol_health_monitor_contract_validation_v1",
            "contract": health_contract,
            "health_monitor_contract_validation_ok": health_monitor_contract_validation_ok,
            **meta,
        },
        "existing_protocol_classification_reuse_validation": {
            "validation_id": "existing_protocol_classification_reuse_validation_v1",
            "total_protocols": len(all_entries),
            "rows": classification_rows,
            "existing_protocol_classification_reuse_ok": existing_protocol_classification_reuse_ok,
            **meta,
        },
        "protocol_governance_debt_preservation": {
            "preservation_id": "protocol_governance_debt_preservation_v1",
            "rows": debt_rows,
            "governance_debt_preserved": governance_debt_preserved,
            **meta,
        },
        "protocol_shared_code_non_runtime_constraints": {
            "constraints_id": "protocol_shared_code_non_runtime_constraints_v1",
            "boundary_statements": list(BOUNDARY_STATEMENTS),
            "forbidden_flags": {f: meta.get(f) is False for f in NON_EXECUTION_FLAGS},
            "non_execution_boundary_ok": non_execution_boundary_ok,
            **meta,
        },
        "protocol_shared_code_post_review_readiness": {
            "readiness_id": "protocol_shared_code_post_review_readiness_v1",
            "recommended_next_phase_primary": NEXT_PHASE_PRIMARY,
            "recommended_next_phase_alt": NEXT_PHASE_ALT,
            "post_review_readiness_ok": post_review_readiness_ok,
            "runtime_execution_enabled": False,
            "protocol_migration_executed": False,
            "whitebox_runtime_integrated": False,
            **meta,
        },
        "summary": summary,
    }
