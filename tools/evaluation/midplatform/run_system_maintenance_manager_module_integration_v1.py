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

from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_module_api_v1 import (
    run_system_maintenance_manager_module_v1,
)
from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_manager_module_types_v1 import (
    BOUNDARY_FALSE_FIELDS,
)


def _base_payload(case_id: str) -> Dict[str, Any]:
    return {
        "maintenance_request_id": f"maint_req_{case_id}",
        "source_capability_id": "luna.task_manager",
        "source_module_version": "v1",
        "anomaly_type": "module_runtime_anomaly",
        "observed_status": "degraded",
        "expected_status": "candidate_ready",
        "diagnostics": {"supporting_signals": ["sig_a"], "contradicting_signals": []},
        "trace_ref": f"trace_src_{case_id}",
        "replay_key": f"replay_src_{case_id}",
        "manifest_ref": "capabilities/registry/manifests/task_manager_manifest_v1.json",
        "baseline_ref": "capabilities/registry/baselines/task_manager_module_baseline_v1.json",
        "protocol_refs": ["task_protocol_v1"],
        "model_asset_refs": ["model_asset_v1"],
        "dependency_refs": ["luna.model_manager"],
        "timestamp": "2026-07-16T10:00:00Z",
        "runtime_mode": "CALIBRATION",
    }


def _boundary_preserved(result: Mapping[str, Any]) -> bool:
    return all(result.get(k) is False for k in BOUNDARY_FALSE_FIELDS)


def run_integration() -> Dict[str, Any]:
    scenarios: Dict[str, Dict[str, Any]] = {}

    c1 = _base_payload("module_integration_failure")
    c1["anomaly_type"] = "module_integration_failure"
    scenarios["module integration failure"] = c1

    c2 = _base_payload("unexpected_module_status")
    c2["anomaly_type"] = "unexpected_module_status"
    scenarios["unexpected module status"] = c2

    c3 = _base_payload("missing_trace")
    c3["anomaly_type"] = "trace_missing"
    c3["trace_ref"] = ""
    scenarios["missing trace"] = c3

    c4 = _base_payload("replay_mismatch")
    c4["anomaly_type"] = "replay_mismatch"
    scenarios["replay mismatch"] = c4

    c5 = _base_payload("determinism_drift")
    c5["anomaly_type"] = "determinism_drift"
    c5["diagnostics"] = {"determinism_drift": True, "supporting_signals": ["drift"]}
    scenarios["determinism drift"] = c5

    c6 = _base_payload("boundary_violation")
    c6["anomaly_type"] = "boundary_violation"
    scenarios["boundary violation"] = c6

    c7 = _base_payload("baseline_exact_match")
    c7["anomaly_type"] = "module_runtime_anomaly"
    scenarios["baseline exact match"] = c7

    c8 = _base_payload("baseline_behavior_drift")
    c8["anomaly_type"] = "baseline_behavior_drift"
    scenarios["baseline behavior drift"] = c8

    c9 = _base_payload("baseline_missing")
    c9["anomaly_type"] = "baseline_behavior_drift"
    c9["baseline_ref"] = ""
    scenarios["baseline missing"] = c9

    c10 = _base_payload("protocol_version_drift")
    c10["anomaly_type"] = "protocol_version_drift"
    scenarios["protocol version drift"] = c10

    c11 = _base_payload("protocol_schema_mismatch")
    c11["anomaly_type"] = "protocol_schema_mismatch"
    scenarios["protocol schema mismatch"] = c11

    c12 = _base_payload("protocol_deprecation_conflict")
    c12["anomaly_type"] = "protocol_deprecation_conflict"
    scenarios["protocol deprecation conflict"] = c12

    c13 = _base_payload("model_asset_missing")
    c13["anomaly_type"] = "model_asset_missing"
    scenarios["model asset missing"] = c13

    c14 = _base_payload("model_unavailable")
    c14["anomaly_type"] = "model_asset_unavailable"
    scenarios["model unavailable"] = c14

    c15 = _base_payload("model_capability_mismatch")
    c15["anomaly_type"] = "model_capability_mismatch"
    scenarios["model capability mismatch"] = c15

    c16 = _base_payload("model_resource_insufficient")
    c16["anomaly_type"] = "model_resource_insufficient"
    scenarios["model resource insufficient"] = c16

    c17 = _base_payload("model_ownership_conflict")
    c17["anomaly_type"] = "model_ownership_conflict"
    scenarios["model ownership conflict"] = c17

    c18 = _base_payload("dependency_unavailable")
    c18["anomaly_type"] = "dependency_unavailable"
    c18["dependency_refs"] = ["missing:luna.protocol_manager"]
    scenarios["dependency unavailable"] = c18

    c19 = _base_payload("registry_manifest_mismatch")
    c19["anomaly_type"] = "manifest_registry_mismatch"
    scenarios["registry/manifest mismatch"] = c19

    c20 = _base_payload("multiple_correlated_faults")
    c20["anomaly_type"] = "baseline_behavior_drift"
    c20["dependency_refs"] = ["missing:luna.model_manager"]
    scenarios["multiple correlated faults"] = c20

    c21 = _base_payload("insufficient_evidence")
    c21["anomaly_type"] = "unknown_anomaly"
    c21["diagnostics"] = {}
    c21["trace_ref"] = ""
    c21["replay_key"] = ""
    scenarios["insufficient evidence"] = c21

    c22 = _base_payload("no_fault_detected")
    c22["anomaly_type"] = "module_runtime_anomaly"
    c22["diagnostics"] = {"supporting_signals": []}
    c22["dependency_refs"] = []
    c22["protocol_refs"] = []
    c22["model_asset_refs"] = []
    c22["runtime_mode"] = "NORMAL_RUNTIME"
    scenarios["no fault detected"] = c22

    expected_status = {
        "module integration failure": "fault_localized",
        "unexpected module status": "fault_localized",
        "missing trace": "fault_partially_localized",
        "replay mismatch": "fault_partially_localized",
        "determinism drift": "fault_partially_localized",
        "boundary violation": "fault_localized",
        "baseline exact match": "fault_partially_localized",
        "baseline behavior drift": "baseline_drift_detected",
        "baseline missing": "manual_review_required",
        "protocol version drift": "protocol_drift_detected",
        "protocol schema mismatch": "protocol_drift_detected",
        "protocol deprecation conflict": "protocol_drift_detected",
        "model asset missing": "model_asset_issue_detected",
        "model unavailable": "model_asset_issue_detected",
        "model capability mismatch": "model_asset_issue_detected",
        "model resource insufficient": "model_asset_issue_detected",
        "model ownership conflict": "model_asset_issue_detected",
        "dependency unavailable": "dependency_issue_detected",
        "registry/manifest mismatch": "multiple_fault_domains_detected",
        "multiple correlated faults": "baseline_drift_detected",
        "insufficient evidence": "insufficient_evidence",
        "no fault detected": "fault_partially_localized",
    }

    protocol_expected = {
        "protocol version drift",
        "protocol schema mismatch",
        "protocol deprecation conflict",
        "registry/manifest mismatch",
    }
    model_expected = {
        "model asset missing",
        "model unavailable",
        "model capability mismatch",
        "model resource insufficient",
        "model ownership conflict",
    }
    baseline_expected = {
        "baseline exact match",
        "baseline behavior drift",
        "baseline missing",
        "registry/manifest mismatch",
        "multiple correlated faults",
    }
    task_expected = set(scenarios.keys()) - {"no fault detected"}

    rows = []
    failed_cases = []
    diagnostics_present_all = True
    trace_present_all = True
    replay_present_all = True
    deterministic_replay = True
    primary_capability_present_when_fault_localized = True
    protocol_result_present_when_expected = True
    model_asset_result_present_when_expected = True
    baseline_result_present_when_expected = True
    task_handoff_candidate_present_when_expected = True
    boundary_preserved = True
    unhandled_exceptions = 0

    for case_id, payload in scenarios.items():
        try:
            result = run_system_maintenance_manager_module_v1(payload)
        except Exception:  # noqa: BLE001
            result = {"maintenance_status": "internal_error"}
            unhandled_exceptions += 1

        status = str(result.get("maintenance_status") or "")
        if not isinstance(result.get("diagnostics"), dict):
            diagnostics_present_all = False
        if not str(result.get("trace_ref") or ""):
            trace_present_all = False
        if not str(result.get("replay_key") or ""):
            replay_present_all = False
        if not _boundary_preserved(result):
            boundary_preserved = False

        if status in {
            "fault_localized",
            "fault_partially_localized",
            "baseline_drift_detected",
            "protocol_drift_detected",
            "model_asset_issue_detected",
            "dependency_issue_detected",
            "multiple_fault_domains_detected",
        } and not str(result.get("primary_capability_candidate") or ""):
            primary_capability_present_when_fault_localized = False

        if case_id in protocol_expected:
            proto = dict(result.get("protocol_drift_result") or {})
            if not isinstance(proto, dict) or not bool(
                proto.get("protocol_check_executed", False)
            ):
                protocol_result_present_when_expected = False

        if case_id in model_expected:
            model = dict(result.get("model_asset_result") or {})
            if not isinstance(model, dict) or not bool(
                model.get("model_check_executed", False)
            ):
                model_asset_result_present_when_expected = False

        if case_id in baseline_expected:
            baseline = str(result.get("baseline_calibration_result") or "")
            if baseline == "":
                baseline_result_present_when_expected = False

        if case_id in task_expected and not isinstance(
            result.get("task_handoff_candidate"), dict
        ):
            task_handoff_candidate_present_when_expected = False

        case_pass = status == expected_status[case_id]
        case_pass = case_pass and isinstance(result.get("diagnostics"), dict)
        case_pass = (
            case_pass
            and bool(result.get("trace_ref"))
            and bool(result.get("replay_key"))
        )
        case_pass = case_pass and _boundary_preserved(result)

        if case_id == "no fault detected":
            rerun = run_system_maintenance_manager_module_v1(payload)
            deterministic_replay = deterministic_replay and (
                result.get("maintenance_status") == rerun.get("maintenance_status")
                and result.get("trace_ref") == rerun.get("trace_ref")
                and result.get("replay_key") == rerun.get("replay_key")
            )
            case_pass = case_pass and deterministic_replay

        if not case_pass:
            failed_cases.append(case_id)

        rows.append(
            {
                "case_id": case_id,
                "expected_status": expected_status[case_id],
                "maintenance_status": status,
                "passed": case_pass,
                "trace_ref": result.get("trace_ref"),
                "replay_key": result.get("replay_key"),
            }
        )

    total_cases = len(scenarios)
    passed_cases = total_cases - len(failed_cases)
    return {
        "phase": "Phase-Luna-System-Maintenance-Manager-Functional-Module-Consolidation-And-Integration-v1-001",
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "failed_cases": failed_cases,
        "diagnostics_present_all": diagnostics_present_all,
        "trace_present_all": trace_present_all,
        "replay_present_all": replay_present_all,
        "deterministic_replay": deterministic_replay,
        "primary_capability_present_when_fault_localized": primary_capability_present_when_fault_localized,
        "protocol_result_present_when_expected": protocol_result_present_when_expected,
        "model_asset_result_present_when_expected": model_asset_result_present_when_expected,
        "baseline_result_present_when_expected": baseline_result_present_when_expected,
        "task_handoff_candidate_present_when_expected": task_handoff_candidate_present_when_expected,
        "boundary_preserved": boundary_preserved,
        "unhandled_exceptions": unhandled_exceptions,
        "rows": rows,
        "integration_pass": passed_cases == total_cases
        and failed_cases == []
        and diagnostics_present_all
        and trace_present_all
        and replay_present_all
        and deterministic_replay
        and primary_capability_present_when_fault_localized
        and protocol_result_present_when_expected
        and model_asset_result_present_when_expected
        and baseline_result_present_when_expected
        and task_handoff_candidate_present_when_expected
        and boundary_preserved
        and unhandled_exceptions == 0,
    }


def main() -> int:
    report = run_integration()
    output_root = Path(
        "_tmp_eval_out/system_maintenance_manager_module_integration_v1_smoke_v0"
    ).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    output_path = output_root / "system_maintenance_manager_module_integration_v1.json"
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
                "diagnostics_present_all": report["diagnostics_present_all"],
                "trace_present_all": report["trace_present_all"],
                "replay_present_all": report["replay_present_all"],
                "deterministic_replay": report["deterministic_replay"],
                "primary_capability_present_when_fault_localized": report[
                    "primary_capability_present_when_fault_localized"
                ],
                "protocol_result_present_when_expected": report[
                    "protocol_result_present_when_expected"
                ],
                "model_asset_result_present_when_expected": report[
                    "model_asset_result_present_when_expected"
                ],
                "baseline_result_present_when_expected": report[
                    "baseline_result_present_when_expected"
                ],
                "task_handoff_candidate_present_when_expected": report[
                    "task_handoff_candidate_present_when_expected"
                ],
                "boundary_preserved": report["boundary_preserved"],
                "unhandled_exceptions": report["unhandled_exceptions"],
                "output": str(output_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if report["integration_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
