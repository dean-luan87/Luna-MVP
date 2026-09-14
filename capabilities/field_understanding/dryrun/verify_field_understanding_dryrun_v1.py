# -*- coding: utf-8 -*-
"""Field-Oriented Egocentric Action Understanding — dry-run verifier v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.core.field_understanding_registry_v1 import (
    FIELD_SYNTHESIS_CHAIN,
    PROHIBITED_FIELD_REVISION_POLICIES,
    PROHIBITED_FIELD_TYPES_FROM_ISOLATED_FACT,
)
from capabilities.field_understanding.core.field_understanding_types_v1 import (
    PHASE_ID,
)

DEFAULT_INPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_understanding_dryrun_v1_smoke_v0"
)
TRACE_FILENAME = "field_understanding_dryrun_trace_v1.json"
SUMMARY_FILENAME = "field_understanding_dryrun_summary_v1.json"
VERIFICATION_FILENAME = "field_understanding_dryrun_verification_v1.json"

EXPECTED_SUMMARY_FINAL_DECISION = "FIELD_UNDERSTANDING_DRYRUN_TRACE_READY_FOR_VERIFIER"
FINAL_DECISION_GO = "FIELD_UNDERSTANDING_DRYRUN_VERIFIER_GO"
FINAL_DECISION_BLOCKED = "FIELD_UNDERSTANDING_DRYRUN_VERIFIER_BLOCKED"

VALID_TRACE_DECISIONS = frozenset(
    {"PASS", "EXPECTED_REJECT", "UNEXPECTED_PASS", "UNEXPECTED_FAIL"}
)

REQUIRED_TRACE_SECTIONS = (
    "field_context",
    "governance_chain",
    "governance_checkpoints",
    "static_dynamic_split",
    "semantic_governance",
    "fact_influence_governance",
    "map_alignment",
    "action_distance",
    "fusion",
    "validation",
    "trace_decision",
)

CASE_9_ID = "case_09_user_exit_fact_influences_field"
CASE_10_ID = "case_10_metro_train_display_influences_field_state"

EXPECTED_POSITIVE_COUNT = 10
EXPECTED_INVALID_COUNT = 5
EXPECTED_TRACE_COUNT = 15


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

    summary_trace_count = summary.get("trace_count")
    if summary_trace_count == len(traces):
        passed.append("summary.trace_count_matches_trace_doc=true")
    else:
        failed.append(
            f"summary.trace_count mismatch: summary={summary_trace_count}, "
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


def verify_governance_chain(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    expected_chain = list(FIELD_SYNTHESIS_CHAIN)

    for trace in traces:
        case_id = trace.get("case_id", "<unknown>")
        chain = trace.get("governance_chain")
        checkpoints = trace.get("governance_checkpoints")

        if chain != expected_chain:
            failed.append(f"{case_id}.governance_chain_mismatch")
        else:
            passed.append(f"{case_id}.governance_chain_ok=true")

        if not isinstance(checkpoints, dict):
            failed.append(f"{case_id}.governance_checkpoints_missing")
            continue

        traversed = checkpoints.get("field_synthesis_chain_traversed")
        if traversed != expected_chain:
            failed.append(f"{case_id}.field_synthesis_chain_traversed_mismatch")
        else:
            passed.append(f"{case_id}.field_synthesis_chain_traversed_ok=true")

    return len(failed) == 0, passed, failed


def verify_no_forbidden_override_policy(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, int, List[str], List[str]]:
    """Count forbidden policies on positive traces only; invalid cases may carry them by design."""
    failed: List[str] = []
    passed: List[str] = []
    forbidden_count = 0

    for trace in traces:
        if trace.get("case_type") != "positive":
            continue
        case_id = trace.get("case_id", "<unknown>")
        fig = trace.get("fact_influence_governance") or {}
        policy = fig.get("field_revision_policy")
        field_type = (trace.get("field_context") or {}).get("field_type")

        if policy in PROHIBITED_FIELD_REVISION_POLICIES:
            forbidden_count += 1
            failed.append(f"{case_id}.forbidden_policy_on_positive={policy!r}")
        if field_type in PROHIBITED_FIELD_TYPES_FROM_ISOLATED_FACT:
            forbidden_count += 1
            failed.append(f"{case_id}.prohibited_field_type_on_positive={field_type!r}")

        checkpoints = trace.get("governance_checkpoints") or {}
        if checkpoints.get("prohibited_override_policy_absent") is False:
            failed.append(f"{case_id}.prohibited_override_policy_absent=false")

    ok = forbidden_count == 0
    if ok:
        passed.append("forbidden_policy_count=0")
    return ok, forbidden_count, passed, failed


def verify_case_9_fact_influence(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, CASE_9_ID)
    if trace is None:
        return False, passed, [f"{CASE_9_ID}.missing"]

    fig = trace.get("fact_influence_governance") or {}
    fusion = trace.get("fusion") or {}

    checks = [
        ("field_revision_policy", "influence_only", fig.get("field_revision_policy")),
        ("fact_influence_level", "strong", fig.get("fact_influence_level")),
        ("action_readiness", "needs_more_observation", fusion.get("action_readiness")),
    ]
    for name, expected, actual in checks:
        if actual == expected:
            passed.append(f"case_9.{name}={expected}")
        else:
            failed.append(f"case_9.{name}: expected={expected!r}, actual={actual!r}")

    dims = set(fig.get("affected_field_dimensions") or [])
    if "field_attention" in dims:
        passed.append("case_9.affected_field_dimensions_contains_field_attention=true")
    else:
        failed.append(f"case_9.affected_field_dimensions missing field_attention: {sorted(dims)!r}")

    policy = fig.get("field_revision_policy")
    if policy in PROHIBITED_FIELD_REVISION_POLICIES:
        failed.append(f"case_9.forbidden_policy={policy!r}")
    else:
        passed.append("case_9.no_forbidden_override_policy=true")

    field_type = (trace.get("field_context") or {}).get("field_type")
    if field_type == "confirmed_exit_field":
        failed.append("case_9.field_type_must_not_be_confirmed_exit_field")
    else:
        passed.append(f"case_9.field_type_not_confirmed_exit={field_type!r}")

    return len(failed) == 0, passed, failed


def verify_case_10_field_context(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, CASE_10_ID)
    if trace is None:
        return False, passed, [f"{CASE_10_ID}.missing"]

    field_ctx = trace.get("field_context") or {}
    fig = trace.get("fact_influence_governance") or {}

    field_type = field_ctx.get("field_type")
    if field_type == "metro_station":
        passed.append("case_10.field_type=metro_station")
    else:
        failed.append(f"case_10.field_type: expected='metro_station', actual={field_type!r}")

    if field_type == "display_screen":
        failed.append("case_10.field_type_must_not_be_display_screen")
    else:
        passed.append("case_10.field_type_not_display_screen=true")

    if fig.get("fact_influence_level") == "strong":
        passed.append("case_10.fact_influence_level=strong")
    else:
        failed.append(
            f"case_10.fact_influence_level: expected='strong', "
            f"actual={fig.get('fact_influence_level')!r}"
        )

    required_dims = {"field_action_logic", "field_state", "field_task_relevance"}
    dims = set(fig.get("affected_field_dimensions") or [])
    missing_dims = required_dims - dims
    if not missing_dims:
        passed.append("case_10.affected_field_dimensions_complete=true")
    else:
        failed.append(f"case_10.affected_field_dimensions missing={sorted(missing_dims)!r}")

    if fig.get("field_type_preserved") is True:
        passed.append("case_10.field_type_preserved=true")
    else:
        failed.append("case_10.field_type_preserved=false")

    if fig.get("direct_override_blocked") is True:
        passed.append("case_10.direct_override_blocked=true")
    else:
        failed.append("case_10.direct_override_blocked=false")

    return len(failed) == 0, passed, failed


def verify_field_understanding_dryrun_v1(
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

    governance_ok, p, f = verify_governance_chain(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    forbidden_ok, forbidden_policy_count, p, f = verify_no_forbidden_override_policy(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    case_9_ok, p, f = verify_case_9_fact_influence(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    case_10_ok, p, f = verify_case_10_field_context(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    governance_checkpoint_ok = sections_ok and governance_ok

    blocker_count = len(all_failed)
    go_ok = (
        summary_ok
        and trace_count_ok
        and summary.get("positive_pass_count") == EXPECTED_POSITIVE_COUNT
        and summary.get("invalid_expected_reject_count") == EXPECTED_INVALID_COUNT
        and unexpected_pass == 0
        and unexpected_fail == 0
        and blocker_count == 0
        and case_9_ok
        and case_10_ok
        and forbidden_policy_count == 0
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
        "governance_checkpoint_check_ok": governance_checkpoint_ok,
        "case_9_governance_check_ok": case_9_ok,
        "case_10_governance_check_ok": case_10_ok,
        "forbidden_policy_count": forbidden_policy_count,
        "unexpected_pass_count": unexpected_pass,
        "unexpected_fail_count": unexpected_fail,
        "blocker_count": blocker_count,
        "failed_checks": all_failed,
        "passed_checks": all_passed,
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
    result = verify_field_understanding_dryrun_v1()
    print(
        json.dumps(
            {
                "input_trace_file": result["input_trace_file"],
                "input_summary_file": result["input_summary_file"],
                "output_verification_file": result.get("output_verification_file"),
                "summary_check_ok": result["summary_check_ok"],
                "trace_count_check_ok": result["trace_count_check_ok"],
                "case_9_governance_check_ok": result["case_9_governance_check_ok"],
                "case_10_governance_check_ok": result["case_10_governance_check_ok"],
                "forbidden_policy_count": result["forbidden_policy_count"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
