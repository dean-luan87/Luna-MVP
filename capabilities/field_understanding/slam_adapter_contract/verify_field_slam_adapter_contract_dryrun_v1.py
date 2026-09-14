# -*- coding: utf-8 -*-
"""Field SLAM Adapter Contract Planning — dry-run verifier v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_adapter_contract.field_slam_adapter_contract_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
)
from capabilities.field_understanding.slam_adapter_contract.field_slam_adapter_contract_types_v1 import (
    FIELD_SYNTHESIS_ENTRYPOINT,
    PHASE_ID,
)

DEFAULT_INPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "field_slam_adapter_contract_dryrun_v1_smoke_v0"
)
TRACE_FILENAME = "field_slam_adapter_contract_dryrun_trace_v1.json"
SUMMARY_FILENAME = "field_slam_adapter_contract_dryrun_summary_v1.json"
VERIFICATION_FILENAME = "field_slam_adapter_contract_dryrun_verification_v1.json"

EXPECTED_SUMMARY_FINAL_DECISION = (
    "FIELD_SLAM_ADAPTER_CONTRACT_DRYRUN_TRACE_READY_FOR_VERIFIER"
)
FINAL_DECISION_GO = "FIELD_SLAM_ADAPTER_CONTRACT_DRYRUN_VERIFIER_GO"
FINAL_DECISION_BLOCKED = "FIELD_SLAM_ADAPTER_CONTRACT_DRYRUN_VERIFIER_BLOCKED"

VALID_TRACE_DECISIONS = frozenset(
    {"PASS", "EXPECTED_REJECT", "UNEXPECTED_PASS", "UNEXPECTED_FAIL"}
)

REQUIRED_TRACE_SECTIONS = (
    "case_id",
    "case_name",
    "case_type",
    "case_goal",
    "adapter_chain",
    "output_mapping",
    "license_gate",
    "runtime_isolation",
    "backend_admission",
    "provider_registration",
    "governance_checkpoints",
    "validation",
    "trace_decision",
)

INVALID_A_ID = "invalid_a_gpl_commercial_runtime"
INVALID_B_ID = "invalid_b_backend_bypass_adapter"
INVALID_C_ID = "invalid_c_output_mapping_not_candidate_only"
INVALID_D_ID = "invalid_d_observation_runtime_admission"
INVALID_E_ID = "invalid_e_health_signal_without_slam_health"

EXPECTED_POSITIVE_COUNT = 7
EXPECTED_INVALID_COUNT = 5
EXPECTED_TRACE_COUNT = 12
EXPECTED_VALIDATOR_RULES = 18


def load_json_file(path: Path) -> Dict[str, Any]:
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        raise ValueError(f"failed to load json: {path}: {exc}") from exc
    if not isinstance(doc, dict):
        raise ValueError(f"expected dict at root: {path}")
    return doc


def _trace_by_id(traces: List[Dict[str, Any]], case_id: str) -> Optional[Dict[str, Any]]:
    for trace in traces:
        if trace.get("case_id") == case_id:
            return trace
    return None


def _errors_contain(errors: List[Any], needle: str) -> bool:
    return any(needle in str(err) for err in errors)


def verify_summary_counts(summary: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    expectations: Dict[str, Any] = {
        "case_count": EXPECTED_TRACE_COUNT,
        "positive_case_count": EXPECTED_POSITIVE_COUNT,
        "invalid_case_count": EXPECTED_INVALID_COUNT,
        "positive_pass_count": EXPECTED_POSITIVE_COUNT,
        "invalid_expected_reject_count": EXPECTED_INVALID_COUNT,
        "unexpected_pass_count": 0,
        "unexpected_fail_count": 0,
        "trace_count": EXPECTED_TRACE_COUNT,
        "validator_rules": EXPECTED_VALIDATOR_RULES,
        "commercial_runtime_backends": [],
        "gpl_runtime_blocked": True,
        "observation_runtime_blocked": True,
        "candidate_only_enforced": True,
        "license_gate_required": True,
        "runtime_isolation_required": True,
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "final_decision": EXPECTED_SUMMARY_FINAL_DECISION,
    }

    for key, expected in expectations.items():
        actual = summary.get(key)
        if actual == expected:
            passed.append(f"summary.{key}={expected!r}")
        else:
            failed.append(f"summary.{key}: expected={expected!r}, actual={actual!r}")

    return len(failed) == 0, passed, failed


def verify_trace_count_and_case_ids(
    trace_doc: Dict[str, Any],
    summary: Dict[str, Any],
) -> Tuple[bool, bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    traces = trace_doc.get("traces")
    if not isinstance(traces, list):
        failed.append("trace_doc.traces: missing or not a list")
        return False, False, passed, failed

    trace_count_ok = len(traces) == EXPECTED_TRACE_COUNT
    if trace_count_ok:
        passed.append(f"trace_count={EXPECTED_TRACE_COUNT}")
    else:
        failed.append(
            f"trace_count: expected={EXPECTED_TRACE_COUNT}, actual={len(traces)}"
        )

    case_ids = [t.get("case_id") for t in traces if isinstance(t, dict)]
    unique_ok = len(case_ids) == len(set(case_ids)) == EXPECTED_TRACE_COUNT
    if unique_ok:
        passed.append("case_id_unique=true")
    else:
        failed.append(
            f"case_id_unique: count={len(case_ids)}, unique={len(set(case_ids))}"
        )

    positive_count = sum(1 for t in traces if t.get("case_type") == "positive")
    invalid_count = sum(1 for t in traces if t.get("case_type") == "invalid")
    if positive_count == EXPECTED_POSITIVE_COUNT and invalid_count == EXPECTED_INVALID_COUNT:
        passed.append(
            f"case_type_distribution=positive:{EXPECTED_POSITIVE_COUNT},"
            f"invalid:{EXPECTED_INVALID_COUNT}"
        )
    else:
        failed.append(
            f"case_type_distribution: expected positive={EXPECTED_POSITIVE_COUNT}, "
            f"invalid={EXPECTED_INVALID_COUNT}; actual positive={positive_count}, "
            f"invalid={invalid_count}"
        )

    if summary.get("trace_count") == len(traces):
        passed.append("summary.trace_count_matches_trace_doc=true")
    else:
        failed.append(
            f"summary.trace_count mismatch: summary={summary.get('trace_count')}, "
            f"trace_doc={len(traces)}"
        )

    if trace_doc.get("field_synthesis_entrypoint") == FIELD_SYNTHESIS_ENTRYPOINT:
        passed.append("trace_doc.field_synthesis_entrypoint_ok=true")
    else:
        failed.append(
            f"trace_doc.field_synthesis_entrypoint: expected={FIELD_SYNTHESIS_ENTRYPOINT!r}, "
            f"actual={trace_doc.get('field_synthesis_entrypoint')!r}"
        )

    return trace_count_ok, unique_ok, passed, failed


def verify_trace_decisions(traces: List[Dict[str, Any]]) -> Tuple[bool, int, int, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    unexpected_pass = 0
    unexpected_fail = 0

    for trace in traces:
        case_id = trace.get("case_id", "<unknown>")
        case_type = trace.get("case_type")
        decision = trace.get("trace_decision")

        if decision not in VALID_TRACE_DECISIONS:
            failed.append(f"{case_id}.trace_decision_invalid: {decision!r}")
            continue

        if decision == "UNEXPECTED_PASS":
            unexpected_pass += 1
            failed.append(f"{case_id}.trace_decision=UNEXPECTED_PASS")
        elif decision == "UNEXPECTED_FAIL":
            unexpected_fail += 1
            failed.append(f"{case_id}.trace_decision=UNEXPECTED_FAIL")
        elif case_type == "positive" and decision != "PASS":
            failed.append(f"{case_id}.positive_not_pass: {decision!r}")
        elif case_type == "invalid" and decision != "EXPECTED_REJECT":
            failed.append(f"{case_id}.invalid_not_expected_reject: {decision!r}")
        else:
            passed.append(f"{case_id}.trace_decision={decision}")

    ok = len(failed) == 0 and unexpected_pass == 0 and unexpected_fail == 0
    if ok:
        passed.append("trace_decision_distribution_ok=true")
    return ok, unexpected_pass, unexpected_fail, passed, failed


def verify_required_trace_sections(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    for trace in traces:
        case_id = trace.get("case_id", "<unknown>")
        missing = [s for s in REQUIRED_TRACE_SECTIONS if s not in trace]
        if missing:
            failed.append(f"{case_id}.missing_sections={missing}")
        else:
            passed.append(f"{case_id}.required_sections_present=true")

    return len(failed) == 0, passed, failed


def verify_adapter_chain_integrity(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    for trace in traces:
        case_id = trace.get("case_id", "<unknown>")
        if trace.get("case_type") != "positive":
            continue

        adapter_chain = trace.get("adapter_chain") or {}
        checks = [
            bool(adapter_chain.get("adapter_ref")),
            bool(adapter_chain.get("backend_ref")),
            adapter_chain.get("field_synthesis_entrypoint") == FIELD_SYNTHESIS_ENTRYPOINT,
            adapter_chain.get("chain_complete") is True,
            bool(adapter_chain.get("supported_output_candidates")),
            bool(adapter_chain.get("required_output_candidates")),
        ]
        if all(checks):
            passed.append(f"{case_id}.adapter_chain_integrity_ok=true")
        else:
            failed.append(f"{case_id}.adapter_chain_integrity_failed={adapter_chain!r}")

    return len(failed) == 0, passed, failed


def verify_license_gate_and_runtime_isolation(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    license_ok_all = True
    isolation_ok_all = True

    for trace in traces:
        case_id = trace.get("case_id", "<unknown>")
        if trace.get("case_type") != "positive":
            continue

        license_gate = trace.get("license_gate") or {}
        isolation = trace.get("runtime_isolation") or {}
        checkpoints = trace.get("governance_checkpoints") or {}

        license_ok = (
            license_gate.get("license_gate_ref")
            and license_gate.get("license_type")
            and license_gate.get("commercial_runtime_allowed") is False
            and checkpoints.get("license_gate_present") is True
        )
        isolation_ok = (
            isolation.get("isolation_ref")
            and isolation.get("isolation_mode")
            and isolation.get("allowed_for_commercial_runtime") is False
            and checkpoints.get("runtime_isolation_present") is True
        )

        if license_ok:
            passed.append(f"{case_id}.license_gate_ok=true")
        else:
            license_ok_all = False
            failed.append(f"{case_id}.license_gate_incomplete={license_gate!r}")

        if isolation_ok:
            passed.append(f"{case_id}.runtime_isolation_ok=true")
        else:
            isolation_ok_all = False
            failed.append(f"{case_id}.runtime_isolation_incomplete={isolation!r}")

    return license_ok_all, isolation_ok_all, passed, failed


def verify_governance_checkpoints(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    required_positive_flags = (
        "backend_does_not_bypass_adapter",
        "field_synthesis_entrypoint_present",
        "license_gate_present",
        "runtime_isolation_present",
        "candidate_only_enforced",
        "source_refs_required",
        "runtime_admission_disabled",
        "commercial_runtime_backends_empty",
    )

    for trace in traces:
        case_id = trace.get("case_id", "<unknown>")
        if trace.get("case_type") != "positive":
            continue

        checkpoints = trace.get("governance_checkpoints") or {}
        missing_false = [k for k in required_positive_flags if checkpoints.get(k) is not True]
        if missing_false:
            failed.append(f"{case_id}.governance_checkpoints_false={missing_false}")
        else:
            passed.append(f"{case_id}.governance_checkpoints_ok=true")

        backend_ref = (trace.get("adapter_chain") or {}).get("backend_ref")
        if backend_ref in {"openvins", "vins_fusion", "orb_slam3"}:
            if checkpoints.get("gpl_runtime_blocked") is not True:
                failed.append(f"{case_id}.gpl_runtime_blocked_false")
            else:
                passed.append(f"{case_id}.gpl_runtime_blocked=true")

        if backend_ref in {"kimera", "hydra", "grapheqa"}:
            if checkpoints.get("observation_runtime_blocked") is not True:
                failed.append(f"{case_id}.observation_runtime_blocked_false")
            else:
                passed.append(f"{case_id}.observation_runtime_blocked=true")

    return len(failed) == 0, passed, failed


def verify_invalid_a_gpl_runtime_block(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_A_ID)
    if trace is None:
        return False, passed, [f"{INVALID_A_ID}.missing"]

    validation = trace.get("validation") or {}
    errors = validation.get("errors") or []
    license_gate = trace.get("license_gate") or {}

    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        license_gate.get("commercial_runtime_allowed") is True,
        license_gate.get("license_type") in {"gpl_3", "gpl_v3"},
        _errors_contain(errors, "gpl_backend_commercial_runtime_not_allowed"),
        validation.get("actual_validation_ok") is False,
    ]
    if all(checks):
        passed.append("invalid_a.gpl_commercial_runtime_rejected=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_a.trace_decision={trace.get('trace_decision')!r}")
        if not _errors_contain(errors, "gpl_backend_commercial_runtime_not_allowed"):
            failed.append(f"invalid_a.errors_missing_gpl_block={errors!r}")

    return len(failed) == 0, passed, failed


def verify_invalid_b_adapter_bypass_block(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_B_ID)
    if trace is None:
        return False, passed, [f"{INVALID_B_ID}.missing"]

    adapter_chain = trace.get("adapter_chain") or {}
    checkpoints = trace.get("governance_checkpoints") or {}
    validation = trace.get("validation") or {}

    adapter_ref_missing = not adapter_chain.get("adapter_ref")
    entrypoint_missing = (
        not adapter_chain.get("field_synthesis_entrypoint")
        or checkpoints.get("field_synthesis_entrypoint_present") is False
    )

    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        adapter_chain.get("chain_complete") is False,
        adapter_ref_missing or entrypoint_missing,
        checkpoints.get("backend_does_not_bypass_adapter") is False,
        validation.get("actual_validation_ok") is False,
    ]
    if all(checks):
        passed.append("invalid_b.adapter_bypass_rejected=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_b.trace_decision={trace.get('trace_decision')!r}")
        if adapter_chain.get("chain_complete") is not False:
            failed.append(f"invalid_b.chain_complete={adapter_chain.get('chain_complete')!r}")

    return len(failed) == 0, passed, failed


def verify_invalid_c_candidate_only_block(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_C_ID)
    if trace is None:
        return False, passed, [f"{INVALID_C_ID}.missing"]

    output_mapping = trace.get("output_mapping") or {}
    validation = trace.get("validation") or {}
    errors = validation.get("errors") or []

    mapping_bad = (
        output_mapping.get("candidate_only_enforced") is False
        or output_mapping.get("source_refs_required") is False
    )

    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        mapping_bad,
        _errors_contain(errors, "candidate_only_enforced")
        or _errors_contain(errors, "source_refs_required"),
        validation.get("actual_validation_ok") is False,
    ]
    if all(checks):
        passed.append("invalid_c.candidate_only_mapping_rejected=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_c.trace_decision={trace.get('trace_decision')!r}")
        if not mapping_bad:
            failed.append(f"invalid_c.output_mapping={output_mapping!r}")

    return len(failed) == 0, passed, failed


def verify_invalid_d_observation_runtime_block(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_D_ID)
    if trace is None:
        return False, passed, [f"{INVALID_D_ID}.missing"]

    admission = trace.get("backend_admission") or {}
    provider = trace.get("provider_registration") or {}
    validation = trace.get("validation") or {}
    errors = validation.get("errors") or []

    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        admission.get("runtime_admission_allowed") is True,
        provider.get("provider_role") == "scene_graph_observation_provider",
        (trace.get("adapter_chain") or {}).get("backend_ref") == "grapheqa",
        _errors_contain(errors, "observation_backend_runtime_admission_not_allowed"),
        validation.get("actual_validation_ok") is False,
    ]
    if all(checks):
        passed.append("invalid_d.observation_runtime_admission_rejected=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_d.trace_decision={trace.get('trace_decision')!r}")
        if admission.get("runtime_admission_allowed") is not True:
            failed.append(
                f"invalid_d.runtime_admission_allowed="
                f"{admission.get('runtime_admission_allowed')!r}"
            )

    return len(failed) == 0, passed, failed


def verify_invalid_e_health_signal_block(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_E_ID)
    if trace is None:
        return False, passed, [f"{INVALID_E_ID}.missing"]

    provider = trace.get("provider_registration") or {}
    validation = trace.get("validation") or {}
    errors = validation.get("errors") or []
    supported = list(provider.get("supported_candidate_types") or [])

    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        provider.get("health_signal_required") is True,
        "SLAMHealthCandidate" not in supported,
        _errors_contain(errors, "health_signal_requires_slam_health_candidate"),
        validation.get("actual_validation_ok") is False,
    ]
    if all(checks):
        passed.append("invalid_e.health_signal_without_slam_health_rejected=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_e.trace_decision={trace.get('trace_decision')!r}")
        if "SLAMHealthCandidate" in supported:
            failed.append(f"invalid_e.supported_candidate_types={supported!r}")

    return len(failed) == 0, passed, failed


def verify_field_slam_adapter_contract_dryrun_v1(
    *,
    input_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    root = Path(input_root or DEFAULT_INPUT_ROOT).expanduser().resolve()
    trace_path = root / TRACE_FILENAME
    summary_path = root / SUMMARY_FILENAME

    trace_doc = load_json_file(trace_path)
    summary = load_json_file(summary_path)
    traces = trace_doc.get("traces") or []
    if not isinstance(traces, list):
        traces = []

    all_passed: List[str] = []
    all_failed: List[str] = []

    summary_ok, p, f = verify_summary_counts(summary)
    all_passed.extend(p)
    all_failed.extend(f)

    trace_count_ok, case_id_unique_ok, p, f = verify_trace_count_and_case_ids(trace_doc, summary)
    all_passed.extend(p)
    all_failed.extend(f)

    trace_decision_ok, unexpected_pass, unexpected_fail, p, f = verify_trace_decisions(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    sections_ok, p, f = verify_required_trace_sections(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    adapter_chain_ok, p, f = verify_adapter_chain_integrity(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    license_gate_ok, runtime_isolation_ok, p, f = verify_license_gate_and_runtime_isolation(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    governance_ok, p, f = verify_governance_checkpoints(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_a_ok, p, f = verify_invalid_a_gpl_runtime_block(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_b_ok, p, f = verify_invalid_b_adapter_bypass_block(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_c_ok, p, f = verify_invalid_c_candidate_only_block(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_d_ok, p, f = verify_invalid_d_observation_runtime_block(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_e_ok, p, f = verify_invalid_e_health_signal_block(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    blocker_count = len(all_failed)
    go_ok = (
        summary_ok
        and trace_count_ok
        and case_id_unique_ok
        and trace_decision_ok
        and sections_ok
        and adapter_chain_ok
        and license_gate_ok
        and runtime_isolation_ok
        and governance_ok
        and invalid_a_ok
        and invalid_b_ok
        and invalid_c_ok
        and invalid_d_ok
        and invalid_e_ok
        and summary.get("positive_pass_count") == EXPECTED_POSITIVE_COUNT
        and summary.get("invalid_expected_reject_count") == EXPECTED_INVALID_COUNT
        and unexpected_pass == 0
        and unexpected_fail == 0
        and blocker_count == 0
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Step 4 Adapter Contract Dry-run Verifier",
        "input_trace_file": str(trace_path),
        "input_summary_file": str(summary_path),
        "summary_check_ok": summary_ok,
        "trace_count_check_ok": trace_count_ok,
        "case_id_unique_check_ok": case_id_unique_ok,
        "trace_decision_check_ok": trace_decision_ok,
        "required_sections_check_ok": sections_ok,
        "adapter_chain_integrity_check_ok": adapter_chain_ok,
        "license_gate_check_ok": license_gate_ok,
        "runtime_isolation_check_ok": runtime_isolation_ok,
        "governance_checkpoints_check_ok": governance_ok,
        "invalid_a_gpl_runtime_check_ok": invalid_a_ok,
        "invalid_b_adapter_bypass_check_ok": invalid_b_ok,
        "invalid_c_candidate_only_check_ok": invalid_c_ok,
        "invalid_d_observation_runtime_check_ok": invalid_d_ok,
        "invalid_e_health_signal_check_ok": invalid_e_ok,
        "unexpected_pass_count": unexpected_pass,
        "unexpected_fail_count": unexpected_fail,
        "blocker_count": blocker_count,
        "failed_checks": all_failed,
        "passed_checks": all_passed,
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "final_decision": FINAL_DECISION_GO if go_ok else FINAL_DECISION_BLOCKED,
    }

    if write_file:
        out_path = root / VERIFICATION_FILENAME
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        result["output_verification_file"] = str(out_path)

    return result


def main() -> int:
    result = verify_field_slam_adapter_contract_dryrun_v1()
    print(
        json.dumps(
            {
                "input_trace_file": result["input_trace_file"],
                "input_summary_file": result["input_summary_file"],
                "output_verification_file": result.get("output_verification_file"),
                "summary_check_ok": result["summary_check_ok"],
                "trace_count_check_ok": result["trace_count_check_ok"],
                "invalid_a_gpl_runtime_check_ok": result["invalid_a_gpl_runtime_check_ok"],
                "invalid_b_adapter_bypass_check_ok": result["invalid_b_adapter_bypass_check_ok"],
                "invalid_c_candidate_only_check_ok": result["invalid_c_candidate_only_check_ok"],
                "invalid_d_observation_runtime_check_ok": result[
                    "invalid_d_observation_runtime_check_ok"
                ],
                "invalid_e_health_signal_check_ok": result["invalid_e_health_signal_check_ok"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
