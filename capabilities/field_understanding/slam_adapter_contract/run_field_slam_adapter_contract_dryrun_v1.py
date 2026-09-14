# -*- coding: utf-8 -*-
"""Field SLAM Adapter Contract Planning — dry-run runner v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_adapter_contract.field_slam_adapter_contract_dryrun_cases_v1 import (
    FieldSLAMAdapterContractDryRunCase,
    build_all_adapter_contract_cases_v1,
    bundle_from_adapter_contract_case,
)
from capabilities.field_understanding.slam_adapter_contract.field_slam_adapter_contract_registry_v1 import (
    GPL_LICENSE_TYPES,
    OBSERVATION_BACKEND_REFS,
)
from capabilities.field_understanding.slam_adapter_contract.field_slam_adapter_contract_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
    _candidate_only_enforced,
    validate_adapter_contract_case_bundle,
)
from capabilities.field_understanding.slam_adapter_contract.field_slam_adapter_contract_types_v1 import (
    FIELD_SYNTHESIS_ENTRYPOINT,
    GENERIC_SLAM_ADAPTER_CONTRACT_ID,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
)

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "field_slam_adapter_contract_dryrun_v1_smoke_v0"
)
TRACE_FILENAME = "field_slam_adapter_contract_dryrun_trace_v1.json"
SUMMARY_FILENAME = "field_slam_adapter_contract_dryrun_summary_v1.json"

FINAL_DECISION_TRACE_READY = "FIELD_SLAM_ADAPTER_CONTRACT_DRYRUN_TRACE_READY_FOR_VERIFIER"
FINAL_DECISION_RUNNER_FAIL = "FIELD_SLAM_ADAPTER_CONTRACT_DRYRUN_RUNNER_UNEXPECTED_OUTCOME"

TraceDecision = Literal["PASS", "EXPECTED_REJECT", "UNEXPECTED_PASS", "UNEXPECTED_FAIL"]


def classify_trace_decision(expected_ok: bool, actual_ok: bool) -> TraceDecision:
    if expected_ok and actual_ok:
        return "PASS"
    if not expected_ok and not actual_ok:
        return "EXPECTED_REJECT"
    if not expected_ok and actual_ok:
        return "UNEXPECTED_PASS"
    return "UNEXPECTED_FAIL"


def _first_item(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return items[0] if items else {}


def _governance_checkpoints(
    case: FieldSLAMAdapterContractDryRunCase,
    bundle: Dict[str, Any],
) -> Dict[str, bool]:
    adapters = list(bundle.get("adapter_contracts") or ())
    mappings = list(bundle.get("output_mappings") or ())
    license_gates = list(bundle.get("license_gates") or ())
    isolations = list(bundle.get("runtime_isolations") or ())
    admissions = list(bundle.get("backend_admissions") or ())
    providers = list(bundle.get("provider_registrations") or ())

    adapter = _first_item(adapters)
    backend_ref = case.expected_backend_ref or adapter.get("backend_ref", "")

    backend_does_not_bypass_adapter = bool(
        adapter.get("adapter_ref")
        and adapter.get("field_synthesis_entrypoint") == FIELD_SYNTHESIS_ENTRYPOINT
        and adapter.get("license_gate_ref")
        and adapter.get("runtime_isolation_ref")
    )

    gpl_runtime_blocked = all(
        gate.get("commercial_runtime_allowed") is not True
        for gate in license_gates
        if gate.get("license_type") in GPL_LICENSE_TYPES
    ) and all(
        admission.get("runtime_admission_allowed") is not True
        for admission in admissions
        if admission.get("backend_ref") in {"openvins", "vins_fusion", "orb_slam3"}
    )

    observation_runtime_blocked = all(
        admission.get("runtime_admission_allowed") is not True
        for admission in admissions
        if admission.get("backend_ref") in OBSERVATION_BACKEND_REFS
    )

    candidate_only_enforced = _candidate_only_enforced(bundle)
    source_refs_required = all(
        mapping.get("source_refs_required") is True for mapping in mappings
    ) if mappings else True
    mapping_candidate_only = all(
        mapping.get("candidate_only_enforced") is True for mapping in mappings
    ) if mappings else True

    runtime_admission_disabled = all(
        admission.get("runtime_admission_allowed") is not True for admission in admissions
    ) if admissions else True

    commercial_runtime_backends_empty = not any(
        gate.get("commercial_runtime_allowed") is True for gate in license_gates
    )

    health_signal_ok = True
    for provider in providers:
        if provider.get("health_signal_required") is True:
            supported = set(provider.get("supported_candidate_types") or ())
            if "SLAMHealthCandidate" not in supported:
                health_signal_ok = False

    return {
        "backend_does_not_bypass_adapter": backend_does_not_bypass_adapter,
        "field_synthesis_entrypoint_present": adapter.get("field_synthesis_entrypoint")
        == FIELD_SYNTHESIS_ENTRYPOINT,
        "license_gate_present": bool(license_gates),
        "runtime_isolation_present": bool(isolations),
        "gpl_runtime_blocked": gpl_runtime_blocked,
        "observation_runtime_blocked": observation_runtime_blocked,
        "candidate_only_enforced": candidate_only_enforced and mapping_candidate_only,
        "source_refs_required": source_refs_required,
        "runtime_admission_disabled": runtime_admission_disabled,
        "commercial_runtime_backends_empty": commercial_runtime_backends_empty,
        "health_signal_candidate_supported": health_signal_ok,
        "adapter_chain_complete": backend_does_not_bypass_adapter and bool(mappings),
        "backend_ref_matches_case": adapter.get("backend_ref") == backend_ref
        if adapter
        else backend_ref == case.expected_backend_ref,
    }


def build_trace_for_case(
    case: FieldSLAMAdapterContractDryRunCase,
    *,
    actual_ok: bool,
    errors: List[str],
    bundle: Dict[str, Any],
) -> Dict[str, Any]:
    adapters = list(bundle.get("adapter_contracts") or ())
    mappings = list(bundle.get("output_mappings") or ())
    license_gates = list(bundle.get("license_gates") or ())
    isolations = list(bundle.get("runtime_isolations") or ())
    admissions = list(bundle.get("backend_admissions") or ())
    providers = list(bundle.get("provider_registrations") or ())

    adapter = _first_item(adapters)
    license_gate = _first_item(license_gates)
    isolation = _first_item(isolations)
    admission = _first_item(admissions)
    provider = _first_item(providers)

    trace_decision = classify_trace_decision(case.expected_validation_ok, actual_ok)
    matched = trace_decision in ("PASS", "EXPECTED_REJECT")
    checkpoints = _governance_checkpoints(case, bundle)

    luna_candidate_types = sorted(
        {m.get("luna_candidate_type") for m in mappings if m.get("luna_candidate_type")}
    )

    return {
        "case_id": case.case_id,
        "case_name": case.case_name,
        "case_type": case.case_type,
        "case_goal": case.case_goal,
        "expected_notes": list(case.expected_notes),
        "generic_adapter_contract_id": GENERIC_SLAM_ADAPTER_CONTRACT_ID,
        "adapter_chain": {
            "backend_ref": adapter.get("backend_ref") or case.expected_backend_ref,
            "adapter_ref": adapter.get("adapter_ref"),
            "field_synthesis_entrypoint": adapter.get("field_synthesis_entrypoint")
            or FIELD_SYNTHESIS_ENTRYPOINT,
            "adapter_status": adapter.get("adapter_status"),
            "supported_output_candidates": list(adapter.get("supported_output_candidates") or ()),
            "required_output_candidates": list(adapter.get("required_output_candidates") or ()),
            "chain_complete": checkpoints["adapter_chain_complete"],
        },
        "output_mapping": {
            "mapping_count": len(mappings),
            "luna_candidate_types": luna_candidate_types,
            "candidate_only_enforced": all(
                m.get("candidate_only_enforced") is True for m in mappings
            )
            if mappings
            else False,
            "source_refs_required": all(m.get("source_refs_required") is True for m in mappings)
            if mappings
            else False,
        },
        "license_gate": {
            "license_gate_ref": license_gate.get("license_gate_ref"),
            "license_type": license_gate.get("license_type"),
            "license_risk": license_gate.get("license_risk"),
            "commercial_runtime_allowed": license_gate.get("commercial_runtime_allowed"),
            "technical_reference_allowed": license_gate.get("technical_reference_allowed"),
            "review_status": license_gate.get("review_status"),
            "blocked_usage_modes": list(license_gate.get("blocked_usage_modes") or ()),
        },
        "runtime_isolation": {
            "isolation_ref": isolation.get("isolation_ref"),
            "isolation_mode": isolation.get("isolation_mode"),
            "data_exchange_mode": isolation.get("data_exchange_mode"),
            "process_boundary_required": isolation.get("process_boundary_required"),
            "allowed_for_internal_dev": isolation.get("allowed_for_internal_dev"),
            "allowed_for_commercial_runtime": isolation.get("allowed_for_commercial_runtime"),
        },
        "backend_admission": {
            "admission_ref": admission.get("admission_ref"),
            "admission_stage": admission.get("admission_stage") or case.expected_admission_stage,
            "license_gate_passed": admission.get("license_gate_passed"),
            "adapter_contract_passed": admission.get("adapter_contract_passed"),
            "output_mapping_passed": admission.get("output_mapping_passed"),
            "static_validation_passed": admission.get("static_validation_passed"),
            "runtime_admission_allowed": admission.get("runtime_admission_allowed"),
            "blocked_reasons": list(admission.get("blocked_reasons") or ()),
        },
        "provider_registration": {
            "provider_ref": provider.get("provider_ref"),
            "provider_role": provider.get("provider_role"),
            "enabled_by_default": provider.get("enabled_by_default"),
            "supported_candidate_types": list(provider.get("supported_candidate_types") or ()),
            "health_signal_required": provider.get("health_signal_required"),
            "disable_policy": provider.get("disable_policy"),
        },
        "governance_checkpoints": checkpoints,
        "validation": {
            "expected_validation_ok": case.expected_validation_ok,
            "actual_validation_ok": actual_ok,
            "errors": errors,
            "matched_expectation": matched,
        },
        "trace_decision": trace_decision,
    }


def run_single_dryrun_case(case: FieldSLAMAdapterContractDryRunCase) -> Dict[str, Any]:
    bundle = bundle_from_adapter_contract_case(case)
    actual_ok, errors = validate_adapter_contract_case_bundle(bundle)
    return build_trace_for_case(case, actual_ok=actual_ok, errors=errors, bundle=bundle)


def summarize_dryrun_traces(traces: List[Dict[str, Any]]) -> Dict[str, Any]:
    positive_pass = sum(1 for t in traces if t["trace_decision"] == "PASS")
    expected_reject = sum(1 for t in traces if t["trace_decision"] == "EXPECTED_REJECT")
    unexpected_pass = sum(1 for t in traces if t["trace_decision"] == "UNEXPECTED_PASS")
    unexpected_fail = sum(1 for t in traces if t["trace_decision"] == "UNEXPECTED_FAIL")
    positive_cases = [t for t in traces if t["case_type"] == "positive"]
    invalid_cases = [t for t in traces if t["case_type"] == "invalid"]

    runner_ok = (
        positive_pass == 7
        and expected_reject == 5
        and unexpected_pass == 0
        and unexpected_fail == 0
        and len(traces) == 12
    )

    gpl_blocked = all(
        t["governance_checkpoints"].get("gpl_runtime_blocked") is True
        for t in positive_cases
        if t["adapter_chain"].get("backend_ref") in {"openvins", "vins_fusion", "orb_slam3"}
    )
    observation_blocked = all(
        t["governance_checkpoints"].get("observation_runtime_blocked") is True
        for t in positive_cases
        if t["adapter_chain"].get("backend_ref") in OBSERVATION_BACKEND_REFS
    )
    candidate_only = all(
        t["governance_checkpoints"].get("candidate_only_enforced") is True
        for t in positive_cases
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 3 Adapter Contract Dry-run Runner",
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "case_count": len(traces),
        "positive_case_count": len(positive_cases),
        "invalid_case_count": len(invalid_cases),
        "positive_pass_count": positive_pass,
        "invalid_expected_reject_count": expected_reject,
        "unexpected_pass_count": unexpected_pass,
        "unexpected_fail_count": unexpected_fail,
        "trace_count": len(traces),
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "commercial_runtime_backends": [],
        "gpl_runtime_blocked": gpl_blocked,
        "observation_runtime_blocked": observation_blocked,
        "candidate_only_enforced": candidate_only,
        "license_gate_required": True,
        "runtime_isolation_required": True,
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "no_real_backend_connected": NON_EXECUTION_FLAGS.get("no_real_adapter_runtime") is True,
        "no_camera": NON_EXECUTION_FLAGS.get("no_camera_runtime") is True,
        "no_ros": NON_EXECUTION_FLAGS.get("no_ros_runtime") is True,
        "no_runtime_admission": NON_EXECUTION_FLAGS.get("no_runtime_admission") is True,
        "trace_decisions": {t["case_id"]: t["trace_decision"] for t in traces},
        "invalid_case_reviews": {
            "invalid_a_gpl_commercial_runtime": _trace_review(
                traces, "invalid_a_gpl_commercial_runtime", "EXPECTED_REJECT"
            ),
            "invalid_b_backend_bypass_adapter": _trace_review(
                traces, "invalid_b_backend_bypass_adapter", "EXPECTED_REJECT"
            ),
            "invalid_c_output_mapping_not_candidate_only": _trace_review(
                traces, "invalid_c_output_mapping_not_candidate_only", "EXPECTED_REJECT"
            ),
            "invalid_d_observation_runtime_admission": _trace_review(
                traces, "invalid_d_observation_runtime_admission", "EXPECTED_REJECT"
            ),
            "invalid_e_health_signal_without_slam_health": _trace_review(
                traces, "invalid_e_health_signal_without_slam_health", "EXPECTED_REJECT"
            ),
        },
        "final_decision": FINAL_DECISION_TRACE_READY if runner_ok else FINAL_DECISION_RUNNER_FAIL,
    }


def _trace_review(
    traces: List[Dict[str, Any]],
    case_id: str,
    expected_decision: str,
) -> Dict[str, Any]:
    trace = next((t for t in traces if t["case_id"] == case_id), None)
    if trace is None:
        return {"found": False, "expected_decision": expected_decision}
    return {
        "found": True,
        "trace_decision": trace["trace_decision"],
        "matches_expected": trace["trace_decision"] == expected_decision,
        "validation_errors": trace["validation"]["errors"],
        "governance_checkpoints": trace["governance_checkpoints"],
    }


def run_field_slam_adapter_contract_dryrun_v1(
    *,
    output_root: Optional[str] = None,
    write_files: bool = True,
) -> Dict[str, Any]:
    all_cases = build_all_adapter_contract_cases_v1()
    traces = [run_single_dryrun_case(case) for case in all_cases]
    summary = summarize_dryrun_traces(traces)

    resolved_root = str(Path(output_root or DEFAULT_OUTPUT).expanduser().resolve())
    result: Dict[str, Any] = {
        "summary": summary,
        "traces": traces,
        "output_root": resolved_root,
    }

    if write_files:
        out = Path(resolved_root)
        out.mkdir(parents=True, exist_ok=True)
        trace_path = out / TRACE_FILENAME
        summary_path = out / SUMMARY_FILENAME

        trace_doc = {
            "phase_id": PHASE_ID,
            "step": "Step 3 Adapter Contract Dry-run Runner",
            "trace_count": len(traces),
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "traces": traces,
        }
        trace_path.write_text(json.dumps(trace_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        result["output_trace_file"] = str(trace_path)
        result["output_summary_file"] = str(summary_path)

    return result


def main() -> int:
    result = run_field_slam_adapter_contract_dryrun_v1()
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": result["output_root"],
                "output_trace_file": result.get("output_trace_file"),
                "output_summary_file": result.get("output_summary_file"),
                "positive_pass_count": summary["positive_pass_count"],
                "invalid_expected_reject_count": summary["invalid_expected_reject_count"],
                "unexpected_pass_count": summary["unexpected_pass_count"],
                "unexpected_fail_count": summary["unexpected_fail_count"],
                "trace_count": summary["trace_count"],
                "final_decision": summary["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary["final_decision"] == FINAL_DECISION_TRACE_READY else 1


if __name__ == "__main__":
    raise SystemExit(main())
