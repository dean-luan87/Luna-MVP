# -*- coding: utf-8 -*-
"""Field SLAM Interface Contract — dry-run verifier v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_interface.field_slam_interface_registry_v1 import (
    FORBIDDEN_SLAM_POLICIES,
    SLAM_EVIDENCE_GOVERNANCE_CHAIN,
)
from capabilities.field_understanding.slam_interface.field_slam_interface_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
)
from capabilities.field_understanding.slam_interface.field_slam_interface_types_v1 import (
    PHASE_ID,
)

DEFAULT_INPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_slam_interface_dryrun_v1_smoke_v0"
)
TRACE_FILENAME = "field_slam_interface_dryrun_trace_v1.json"
SUMMARY_FILENAME = "field_slam_interface_dryrun_summary_v1.json"
VERIFICATION_FILENAME = "field_slam_interface_dryrun_verification_v1.json"

EXPECTED_SUMMARY_FINAL_DECISION = "FIELD_SLAM_INTERFACE_DRYRUN_TRACE_READY_FOR_VERIFIER"
FINAL_DECISION_GO = "FIELD_SLAM_INTERFACE_DRYRUN_VERIFIER_GO"
FINAL_DECISION_BLOCKED = "FIELD_SLAM_INTERFACE_DRYRUN_VERIFIER_BLOCKED"

VALID_TRACE_DECISIONS = frozenset(
    {"PASS", "EXPECTED_REJECT", "UNEXPECTED_PASS", "UNEXPECTED_FAIL"}
)

REQUIRED_TRACE_SECTIONS = (
    "case_id",
    "case_name",
    "case_type",
    "case_goal",
    "slam_evidence_governance_chain",
    "governance_checkpoints",
    "pose_evidence",
    "motion_evidence",
    "spatial_anchor_evidence",
    "local_map_evidence",
    "slam_health",
    "map_drift",
    "relocalization",
    "field_integration",
    "forbidden_policy_check",
    "validation",
    "trace_decision",
)

CASE_3_ID = "case_03_slam_tracking_degraded"
CASE_5_ID = "case_05_local_map_drift_high"
CASE_6_ID = "case_06_stationary_near_zone_no_escalation"
INVALID_C_ID = "invalid_c_tracking_lost_still_ready"
INVALID_D_ID = "invalid_d_anchor_confirms_destination"

EXPECTED_POSITIVE_COUNT = 6
EXPECTED_INVALID_COUNT = 4
EXPECTED_TRACE_COUNT = 10
EXPECTED_VALIDATOR_RULES = 17


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


def verify_summary_counts(summary: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    expectations = {
        "case_count": EXPECTED_TRACE_COUNT,
        "positive_case_count": EXPECTED_POSITIVE_COUNT,
        "invalid_case_count": EXPECTED_INVALID_COUNT,
        "positive_pass_count": EXPECTED_POSITIVE_COUNT,
        "invalid_expected_reject_count": EXPECTED_INVALID_COUNT,
        "unexpected_pass_count": 0,
        "unexpected_fail_count": 0,
        "trace_count": EXPECTED_TRACE_COUNT,
        "validator_rules": EXPECTED_VALIDATOR_RULES,
        "final_decision": EXPECTED_SUMMARY_FINAL_DECISION,
    }
    for key, expected in expectations.items():
        actual = summary.get(key)
        if actual == expected:
            passed.append(f"summary.{key}={expected}")
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
            f"case_type_distribution=positive:{EXPECTED_POSITIVE_COUNT},invalid:{EXPECTED_INVALID_COUNT}"
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


def verify_slam_governance_chain(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    expected_chain = list(SLAM_EVIDENCE_GOVERNANCE_CHAIN)

    for trace in traces:
        case_id = trace.get("case_id", "<unknown>")
        chain = trace.get("slam_evidence_governance_chain")
        checkpoints = trace.get("governance_checkpoints")

        if chain != expected_chain:
            failed.append(f"{case_id}.slam_evidence_governance_chain_mismatch")
        else:
            passed.append(f"{case_id}.slam_evidence_governance_chain_ok=true")

        if not isinstance(checkpoints, dict):
            failed.append(f"{case_id}.governance_checkpoints_missing")
            continue

        traversed = checkpoints.get("slam_evidence_chain_traversed")
        if traversed != expected_chain:
            failed.append(f"{case_id}.slam_evidence_chain_traversed_mismatch")
        else:
            passed.append(f"{case_id}.slam_evidence_chain_traversed_ok=true")

    return len(failed) == 0, passed, failed


def verify_no_unexpected_trace_results(
    unexpected_pass: int,
    unexpected_fail: int,
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    if unexpected_pass == 0 and unexpected_fail == 0:
        passed.append("no_unexpected_trace_results=true")
    else:
        if unexpected_pass:
            failed.append(f"unexpected_pass_count={unexpected_pass}")
        if unexpected_fail:
            failed.append(f"unexpected_fail_count={unexpected_fail}")
    return len(failed) == 0, passed, failed


def verify_forbidden_policy_rejection(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    invalid_traces = [t for t in traces if t.get("case_type") == "invalid"]
    positive_traces = [t for t in traces if t.get("case_type") == "positive"]

    for trace in positive_traces:
        case_id = trace.get("case_id", "<unknown>")
        forbidden = (trace.get("forbidden_policy_check") or {}).get("forbidden_policies_detected") or []
        if forbidden:
            failed.append(f"{case_id}.forbidden_policy_on_positive={forbidden!r}")

    invalid_with_forbidden = 0
    for trace in invalid_traces:
        case_id = trace.get("case_id", "<unknown>")
        forbidden = (trace.get("forbidden_policy_check") or {}).get("forbidden_policies_detected") or []
        field_policy = (trace.get("field_integration") or {}).get("expected_policy")
        if forbidden or field_policy in FORBIDDEN_SLAM_POLICIES:
            invalid_with_forbidden += 1
            passed.append(f"{case_id}.forbidden_policy_detected_in_invalid_case=true")
        elif case_id == INVALID_C_ID:
            passed.append(f"{case_id}.validation_reject_without_forbidden_policy=true")
            invalid_with_forbidden += 1
        else:
            failed.append(f"{case_id}.invalid_case_missing_forbidden_policy_signal")

    if invalid_with_forbidden >= len(invalid_traces) - 1:
        passed.append("forbidden_policy_rejection_ok=true")
    else:
        failed.append(f"invalid_forbidden_coverage={invalid_with_forbidden}/{len(invalid_traces)}")

    positive_clean = all(
        not (t.get("forbidden_policy_check") or {}).get("forbidden_policies_detected")
        for t in positive_traces
    )
    if not positive_clean:
        failed.append("positive_traces_must_not_have_forbidden_policies")

    ok = len(failed) == 0
    return ok, passed, failed


def verify_case_3_tracking_degraded(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, CASE_3_ID)
    if trace is None:
        return False, passed, [f"{CASE_3_ID}.missing"]

    field_int = trace.get("field_integration") or {}
    slam_health = trace.get("slam_health") or {}
    tracking_statuses = slam_health.get("tracking_statuses") or []

    checks = [
        trace.get("trace_decision") == "PASS",
        field_int.get("expected_policy") == "downweight_spatial_evidence",
        "tracking_degraded" in tracking_statuses,
        slam_health.get("degraded") is True,
    ]
    if all(checks):
        passed.append("case_3.tracking_degraded_downweight_ok=true")
    else:
        if trace.get("trace_decision") != "PASS":
            failed.append(f"case_3.trace_decision={trace.get('trace_decision')!r}")
        if field_int.get("expected_policy") != "downweight_spatial_evidence":
            failed.append(f"case_3.expected_policy={field_int.get('expected_policy')!r}")
        if "tracking_degraded" not in tracking_statuses:
            failed.append(f"case_3.tracking_statuses={tracking_statuses!r}")

    return len(failed) == 0, passed, failed


def verify_case_5_high_drift(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, CASE_5_ID)
    if trace is None:
        return False, passed, [f"{CASE_5_ID}.missing"]

    field_int = trace.get("field_integration") or {}
    local_map = trace.get("local_map_evidence") or {}
    map_drift = trace.get("map_drift") or {}
    drift_risks = (local_map.get("drift_risks") or []) + (map_drift.get("drift_risks") or [])

    checks = [
        trace.get("trace_decision") == "PASS",
        field_int.get("expected_policy") == "needs_more_observation",
        "high" in drift_risks,
        field_int.get("action_readiness_in_bundle") == "needs_more_observation",
    ]
    if all(checks):
        passed.append("case_5.high_drift_needs_more_observation_ok=true")
    else:
        if trace.get("trace_decision") != "PASS":
            failed.append(f"case_5.trace_decision={trace.get('trace_decision')!r}")
        if field_int.get("expected_policy") != "needs_more_observation":
            failed.append(f"case_5.expected_policy={field_int.get('expected_policy')!r}")
        if "high" not in drift_risks:
            failed.append(f"case_5.drift_risks={drift_risks!r}")

    return len(failed) == 0, passed, failed


def verify_case_6_stationary_near_zone(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, CASE_6_ID)
    if trace is None:
        return False, passed, [f"{CASE_6_ID}.missing"]

    field_int = trace.get("field_integration") or {}
    motion = trace.get("motion_evidence") or {}
    motion_states = motion.get("motion_states") or []
    checkpoints = trace.get("governance_checkpoints") or {}

    checks = [
        trace.get("trace_decision") == "PASS",
        "stationary" in motion_states,
        field_int.get("expected_policy") == "influence_only",
        checkpoints.get("stationary_near_no_immediate_risk_escalation") is True,
        motion.get("direct_action_generated") is False,
    ]
    if all(checks):
        passed.append("case_6.stationary_near_no_escalation_ok=true")
    else:
        if trace.get("trace_decision") != "PASS":
            failed.append(f"case_6.trace_decision={trace.get('trace_decision')!r}")
        if "stationary" not in motion_states:
            failed.append(f"case_6.motion_states={motion_states!r}")
        if field_int.get("expected_policy") != "influence_only":
            failed.append(f"case_6.expected_policy={field_int.get('expected_policy')!r}")

    return len(failed) == 0, passed, failed


def verify_invalid_c_tracking_lost_ready_action(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_C_ID)
    if trace is None:
        return False, passed, [f"{INVALID_C_ID}.missing"]

    slam_health = trace.get("slam_health") or {}
    field_int = trace.get("field_integration") or {}
    tracking_statuses = slam_health.get("tracking_statuses") or []

    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        "tracking_lost" in tracking_statuses,
        slam_health.get("tracking_lost") is True,
        field_int.get("action_readiness_in_bundle") == "ready_for_action_decision",
        (trace.get("validation") or {}).get("actual_validation_ok") is False,
    ]
    if all(checks):
        passed.append("invalid_c.tracking_lost_ready_action_rejected=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_c.trace_decision={trace.get('trace_decision')!r}")
        if "tracking_lost" not in tracking_statuses:
            failed.append(f"invalid_c.tracking_statuses={tracking_statuses!r}")

    return len(failed) == 0, passed, failed


def verify_invalid_d_confirm_destination(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_D_ID)
    if trace is None:
        return False, passed, [f"{INVALID_D_ID}.missing"]

    forbidden = (trace.get("forbidden_policy_check") or {}).get("forbidden_policies_detected") or []
    anchor = trace.get("spatial_anchor_evidence") or {}

    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        "slam_confirm_destination" in forbidden,
        anchor.get("direct_destination_confirmed") is True,
        (trace.get("validation") or {}).get("actual_validation_ok") is False,
    ]
    if all(checks):
        passed.append("invalid_d.slam_confirm_destination_rejected=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_d.trace_decision={trace.get('trace_decision')!r}")
        if "slam_confirm_destination" not in forbidden:
            failed.append(f"invalid_d.forbidden_policies_detected={forbidden!r}")

    return len(failed) == 0, passed, failed


def verify_field_slam_interface_dryrun_v1(
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

    governance_ok, p, f = verify_slam_governance_chain(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    unexpected_ok, p, f = verify_no_unexpected_trace_results(unexpected_pass, unexpected_fail)
    all_passed.extend(p)
    all_failed.extend(f)

    forbidden_ok, p, f = verify_forbidden_policy_rejection(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    case_3_ok, p, f = verify_case_3_tracking_degraded(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    case_5_ok, p, f = verify_case_5_high_drift(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    case_6_ok, p, f = verify_case_6_stationary_near_zone(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_c_ok, p, f = verify_invalid_c_tracking_lost_ready_action(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_d_ok, p, f = verify_invalid_d_confirm_destination(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    blocker_count = len(all_failed)
    go_ok = (
        summary_ok
        and trace_count_ok
        and summary.get("positive_pass_count") == EXPECTED_POSITIVE_COUNT
        and summary.get("invalid_expected_reject_count") == EXPECTED_INVALID_COUNT
        and unexpected_pass == 0
        and unexpected_fail == 0
        and blocker_count == 0
        and governance_ok
        and forbidden_ok
        and case_3_ok
        and case_5_ok
        and case_6_ok
        and invalid_c_ok
        and invalid_d_ok
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Step 4 Dry-run Verifier",
        "input_trace_file": str(trace_path),
        "input_summary_file": str(summary_path),
        "summary_check_ok": summary_ok,
        "trace_count_check_ok": trace_count_ok,
        "case_id_unique_check_ok": case_id_unique_ok,
        "trace_decision_check_ok": trace_decision_ok,
        "required_sections_check_ok": sections_ok,
        "slam_governance_chain_check_ok": governance_ok,
        "forbidden_policy_check_ok": forbidden_ok,
        "case_3_tracking_degraded_check_ok": case_3_ok,
        "case_5_high_drift_check_ok": case_5_ok,
        "case_6_stationary_check_ok": case_6_ok,
        "invalid_c_tracking_lost_check_ok": invalid_c_ok,
        "invalid_d_confirm_destination_check_ok": invalid_d_ok,
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
    result = verify_field_slam_interface_dryrun_v1()
    print(
        json.dumps(
            {
                "input_trace_file": result["input_trace_file"],
                "input_summary_file": result["input_summary_file"],
                "output_verification_file": result.get("output_verification_file"),
                "summary_check_ok": result["summary_check_ok"],
                "trace_count_check_ok": result["trace_count_check_ok"],
                "case_3_tracking_degraded_check_ok": result["case_3_tracking_degraded_check_ok"],
                "case_5_high_drift_check_ok": result["case_5_high_drift_check_ok"],
                "case_6_stationary_check_ok": result["case_6_stationary_check_ok"],
                "invalid_c_tracking_lost_check_ok": result["invalid_c_tracking_lost_check_ok"],
                "invalid_d_confirm_destination_check_ok": result["invalid_d_confirm_destination_check_ok"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
