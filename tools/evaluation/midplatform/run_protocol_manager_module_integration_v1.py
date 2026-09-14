#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Mapping


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            return parent
    return here.parents[3]


WS_ROOT = _find_ws_root()
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))

from capabilities.midplatform.protocol_manager.module.protocol_manager_module_api_v1 import (
    run_protocol_manager_module_v1,
)


def _version_snapshot() -> Dict[str, Any]:
    return {
        "protocol_registry": {
            "LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1": {
                "protocol_id": "LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1",
                "version": "v1",
                "error_namespace": "LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1::*",
                "lifecycle_state": "active",
            },
            "LUNA-PROTO-L1-CHANGE-CONTROL-V2": {
                "protocol_id": "LUNA-PROTO-L1-CHANGE-CONTROL-V2",
                "version": "v2",
                "error_namespace": "LUNA-PROTO-L1-CHANGE-CONTROL-V2::*",
                "lifecycle_state": "candidate",
            },
        }
    }


def _base_payload(case_id: str) -> Dict[str, Any]:
    return {
        "protocol_request_id": f"protocol_req_{case_id}",
        "operation": "query",
        "protocol_id": "LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1",
        "protocol_type": "interface_contract",
        "protocol_version": "v1",
        "consumer_capability_id": "luna.task_manager",
        "provider_capability_id": "luna.protocol_manager",
        "input_contract_ref": "docs/architecture/LUNA_INTER_MODULE_INFORMATION_FLOW_SPEC_V0.md",
        "output_contract_ref": "docs/architecture/LUNA_INTER_MODULE_INFORMATION_FLOW_SPEC_V0.md",
        "schema_refs": [
            "capabilities/midplatform/protocols/protocol_types_v1.py",
            "capabilities/registry/schemas/capability_module_manifest_schema_v1.json",
        ],
        "error_namespace_ref": "LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1::*",
        "runtime_boundary_ref": "docs/architecture/LUNA_MAINLINE_DESIGN_RUNTIME_BOUNDARY_MATRIX_V0.md",
        "admission_contract_ref": "docs/architecture/capability_registry/luna_capability_module_standard_v1.md",
        "compatibility_target_version": "v1",
        "change_set": {},
        "requested_lifecycle_transition": {"from": "active", "to": "active"},
        "trace_context": {"case_id": case_id},
        "version_snapshot": _version_snapshot(),
    }


def _boundary_preserved(result: Mapping[str, Any]) -> bool:
    required_false = (
        "protocol_asset_modified",
        "runtime_protocol_loaded",
        "dynamic_binding_executed",
        "database_write_executed",
        "state_mutation_executed",
        "fact_admission_executed",
        "action_execution_executed",
        "model_call_executed",
        "external_lookup_executed",
        "production_runtime_executed",
    )
    return all(result.get(k) is False for k in required_false)


def run_integration() -> Dict[str, Any]:
    scenarios: Dict[str, Dict[str, Any]] = {}

    scenarios["valid_protocol_query"] = _base_payload("valid_protocol_query")

    not_found = _base_payload("protocol_not_found")
    not_found["protocol_id"] = "LUNA-PROTO-L1-UNKNOWN-V9"
    scenarios["protocol_not_found"] = not_found

    register_candidate = _base_payload("candidate_registration")
    register_candidate["operation"] = "register_candidate"
    register_candidate["protocol_id"] = "LUNA-PROTO-L2-PERMISSION-ADMISSION-CONTRACT-V1"
    register_candidate["protocol_version"] = "v1"
    scenarios["candidate_registration"] = register_candidate

    exact_match = _base_payload("exact_version_match")
    exact_match["operation"] = "compatibility_check"
    scenarios["exact_version_match"] = exact_match

    backward = _base_payload("backward_compatible")
    backward["operation"] = "compatibility_check"
    backward["protocol_id"] = "LUNA-PROTO-L1-CHANGE-CONTROL-V2"
    backward["protocol_version"] = "v2"
    backward["error_namespace_ref"] = "LUNA-PROTO-L1-CHANGE-CONTROL-V2::*"
    backward["compatibility_target_version"] = "v1"
    scenarios["backward_compatible"] = backward

    adapter_required = _base_payload("adapter_required")
    adapter_required["operation"] = "compatibility_check"
    adapter_required["change_set"] = {"enum_changed": True}
    scenarios["adapter_required"] = adapter_required

    incompatible = _base_payload("incompatible_version")
    incompatible["operation"] = "compatibility_check"
    incompatible["change_set"] = {"runtime_boundary_changed": True}
    scenarios["incompatible_version"] = incompatible

    missing_snapshot = _base_payload("missing_version_snapshot")
    missing_snapshot["operation"] = "compatibility_check"
    missing_snapshot["version_snapshot"] = {}
    missing_snapshot["compatibility_target_version"] = ""
    scenarios["missing_version_snapshot"] = missing_snapshot

    admission_allowed = _base_payload("admission_allowed")
    admission_allowed["operation"] = "admission_check"
    scenarios["admission_allowed"] = admission_allowed

    admission_rejected = _base_payload("admission_rejected")
    admission_rejected["operation"] = "admission_check"
    admission_rejected["admission_contract_ref"] = ""
    scenarios["admission_rejected"] = admission_rejected

    boundary_violation = _base_payload("runtime_boundary_violation")
    boundary_violation["operation"] = "validate"
    boundary_violation["change_set"] = {"runtime_protocol_load_now": True}
    scenarios["runtime_boundary_violation"] = boundary_violation

    error_ns_conflict = _base_payload("error_namespace_conflict")
    error_ns_conflict["operation"] = "validate"
    error_ns_conflict["error_namespace_ref"] = "LUNA-PROTO-L1-OTHER::*"
    scenarios["error_namespace_conflict"] = error_ns_conflict

    non_breaking = _base_payload("non_breaking_change")
    non_breaking["operation"] = "change_review"
    non_breaking["change_set"] = {"input_fields_changed": True}
    scenarios["non_breaking_change"] = non_breaking

    breaking = _base_payload("breaking_change")
    breaking["operation"] = "change_review"
    breaking["change_set"] = {"required_optional_changed": True}
    scenarios["breaking_change"] = breaking

    deprecate = _base_payload("deprecation_candidate")
    deprecate["operation"] = "deprecate_candidate"
    deprecate["requested_lifecycle_transition"] = {"from": "active", "to": "deprecated"}
    scenarios["deprecation_candidate"] = deprecate

    impact = _base_payload("impact_analysis")
    impact["operation"] = "impact_analysis"
    impact["change_set"] = {
        "affected_capability_ids": [
            "luna.task_manager",
            "luna.model_manager",
            "luna.vision_manager",
            "luna.ocr_manager",
            "luna.speech_manager",
        ],
        "affected_protocol_ids": ["LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1"],
        "affected_manifest_refs": [
            "capabilities/registry/manifests/task_manager_manifest_v1.json"
        ],
        "affected_baseline_refs": [
            "capabilities/registry/baselines/task_manager_module_baseline_v1.json"
        ],
    }
    scenarios["impact_analysis"] = impact

    diagnose = _base_payload("diagnostic_only")
    diagnose["operation"] = "diagnose"
    scenarios["diagnostic_only"] = diagnose

    deterministic = _base_payload("deterministic_replay")
    deterministic["operation"] = "validate"
    scenarios["deterministic_replay"] = deterministic

    rows = []
    failed_cases = []
    status_coverage = set()
    trace_present_all = True
    replay_present_all = True
    diagnostics_present_all = True
    boundary_preserved = True
    deterministic_replay = True
    deterministic_trace_ref = None
    deterministic_replay_key = None

    first_det_result = None

    expected_status = {
        "valid_protocol_query": "no_change",
        "protocol_not_found": "protocol_not_found",
        "candidate_registration": "protocol_candidate_registered",
        "exact_version_match": "protocol_valid",
        "backward_compatible": "protocol_valid",
        "adapter_required": "protocol_valid",
        "incompatible_version": "protocol_incompatible",
        "missing_version_snapshot": "protocol_not_found",
        "admission_allowed": "protocol_valid",
        "admission_rejected": "admission_rejected",
        "runtime_boundary_violation": "boundary_violation",
        "error_namespace_conflict": "error_namespace_conflict",
        "non_breaking_change": "change_allowed_candidate",
        "breaking_change": "change_review_required",
        "deprecation_candidate": "deprecation_candidate",
        "impact_analysis": "impact_analysis_ready",
        "diagnostic_only": "diagnostic_only",
        "deterministic_replay": "protocol_valid",
    }

    for case_id, payload in scenarios.items():
        result = run_protocol_manager_module_v1(payload)
        module_status = str(result.get("module_status") or "")
        status_coverage.add(module_status)

        if not str(result.get("trace_ref") or ""):
            trace_present_all = False
        if not str(result.get("replay_key") or ""):
            replay_present_all = False
        if not isinstance(result.get("diagnostics"), dict):
            diagnostics_present_all = False
        if not _boundary_preserved(result):
            boundary_preserved = False

        if case_id == "deterministic_replay":
            first_det_result = result
            second = run_protocol_manager_module_v1(payload)
            deterministic_replay = deterministic_replay and (
                result.get("trace_ref") == second.get("trace_ref")
                and result.get("replay_key") == second.get("replay_key")
            )
            deterministic_trace_ref = result.get("trace_ref")
            deterministic_replay_key = result.get("replay_key")

        case_pass = module_status == expected_status[case_id]
        case_pass = case_pass and bool(result.get("candidate_only"))
        case_pass = case_pass and _boundary_preserved(result)
        case_pass = (
            case_pass
            and bool(result.get("trace_ref"))
            and bool(result.get("replay_key"))
        )
        case_pass = case_pass and isinstance(result.get("diagnostics"), dict)
        if case_id == "deterministic_replay":
            case_pass = case_pass and deterministic_replay

        if not case_pass:
            failed_cases.append(case_id)

        rows.append(
            {
                "case_id": case_id,
                "expected_status": expected_status[case_id],
                "module_status": module_status,
                "passed": case_pass,
                "compatibility_result": (
                    result.get("compatibility_candidate") or {}
                ).get("compatibility_result"),
                "trace_ref": result.get("trace_ref"),
                "replay_key": result.get("replay_key"),
            }
        )

    total_cases = len(scenarios)
    passed_cases = total_cases - len(failed_cases)

    return {
        "phase": "Phase-Luna-Protocol-Manager-Functional-Module-Consolidation-And-Integration-v1-001",
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "failed_cases": failed_cases,
        "status_coverage": sorted(status_coverage),
        "trace_present_all": trace_present_all,
        "replay_present_all": replay_present_all,
        "diagnostics_present_all": diagnostics_present_all,
        "deterministic_replay": deterministic_replay,
        "boundary_preserved": boundary_preserved,
        "rows": rows,
        "deterministic_trace_ref": deterministic_trace_ref,
        "deterministic_replay_key": deterministic_replay_key,
        "integration_pass": passed_cases == total_cases
        and failed_cases == []
        and trace_present_all
        and replay_present_all
        and diagnostics_present_all
        and deterministic_replay
        and boundary_preserved,
    }


def main() -> int:
    report = run_integration()
    output_root = Path(
        "_tmp_eval_out/protocol_manager_module_integration_v1_smoke_v0"
    ).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    output_path = output_root / "protocol_manager_module_integration_v1.json"
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "integration_pass": report["integration_pass"],
                "total_cases": report["total_cases"],
                "passed_cases": report["passed_cases"],
                "failed_cases": report["failed_cases"],
                "status_coverage": report["status_coverage"],
                "trace_present_all": report["trace_present_all"],
                "replay_present_all": report["replay_present_all"],
                "diagnostics_present_all": report["diagnostics_present_all"],
                "deterministic_replay": report["deterministic_replay"],
                "boundary_preserved": report["boundary_preserved"],
                "output": str(output_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if report["integration_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
