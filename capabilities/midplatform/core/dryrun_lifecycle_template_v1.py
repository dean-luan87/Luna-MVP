# -*- coding: utf-8 -*-
"""Phase-Midplatform-DryRun-Lifecycle-Template-v1-001.

Shared rules and lightweight helpers for midplatform dry-run lifecycle phases.
Modules may import helpers here; this file does not import module-specific runners.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, FrozenSet, Iterable, List, Mapping, Optional, Sequence, Tuple

PHASE_TEMPLATE_ID = "Phase-Midplatform-DryRun-Lifecycle-Template-v1-001"

# ---------------------------------------------------------------------------
# Lifecycle variants (pick one per phase; do not mix without explicit reason)
# ---------------------------------------------------------------------------

LIFECYCLE_FULL_STEPS: Tuple[str, ...] = (
    "Step 1 Types / Registry / Validators",
    "Step 2 Dry-run Cases",
    "Step 3 Runner + Trace",
    "Step 4 Verifier",
    "Step 5 Post-DryRun Review",
    "Handoff",
)

LIFECYCLE_COMPRESSED_STEPS: Tuple[str, ...] = (
    "Step 1 Static Baseline",
    "Step 2 Cases",
    "Step 3 Runner + Trace",
    "Step 4 Verify + Review",
    "Handoff",
)

LIFECYCLE_MATRIX_STEPS: Tuple[str, ...] = (
    "Matrix",
    "Review",
    "Handoff",
)

# ---------------------------------------------------------------------------
# Binding rules (all midplatform dry-run phases should follow)
# ---------------------------------------------------------------------------

DRYRUN_LIFECYCLE_RULES: Tuple[str, ...] = (
    "runner_must_not_define_rules_only_call_validators",
    "verifier_must_not_import_runner_only_read_trace_summary_json",
    "review_must_not_rerun_runner_or_verifier_only_read_json",
    "cases_and_runner_must_share_bundle_from_case",
    "lightweight_phases_may_merge_verifier_and_review",
    "non_execution_matrix_phases_need_not_use_full_five_step_chain",
    "final_decision_naming_must_be_consistent_per_module",
    "failed_checks_blocker_count_unexpected_count_must_be_unified",
)

# ---------------------------------------------------------------------------
# final_decision naming pattern
# ---------------------------------------------------------------------------
# {MODULE_PREFIX}_PLANNING_READY_FOR_DRYRUN_CASES
# {MODULE_PREFIX}_DRYRUN_CASES_READY_FOR_RUNNER
# {MODULE_PREFIX}_DRYRUN_TRACE_READY_FOR_VERIFIER
# {MODULE_PREFIX}_DRYRUN_VERIFIER_GO | _BLOCKED          (full lifecycle only)
# {MODULE_PREFIX}_POST_DRYRUN_REVIEW_GO | _BLOCKED       (review / compressed close)
# {MODULE_PREFIX}_HANDOFF_GO | _BLOCKED                   (optional handoff)

VALID_TRACE_DECISIONS: FrozenSet[str] = frozenset(
    {"PASS", "EXPECTED_REJECT", "UNEXPECTED_PASS", "UNEXPECTED_FAIL"}
)


def load_json_file(path: Path) -> Dict[str, Any]:
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        raise ValueError(f"failed to load json: {path}: {exc}") from exc
    if not isinstance(doc, dict):
        raise ValueError(f"expected dict at root: {path}")
    return doc


def write_json_file(path: Path, doc: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(doc), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def verify_summary_boolean_flags(
    summary: Mapping[str, Any],
    *,
    flags_false: Sequence[str] = (),
    flags_true: Sequence[str] = (),
) -> Tuple[bool, List[str]]:
    failed: List[str] = []
    for key in flags_false:
        if summary.get(key) is not False:
            failed.append(f"summary.{key}: expected=False, actual={summary.get(key)!r}")
    for key in flags_true:
        if summary.get(key) is not True:
            failed.append(f"summary.{key}: expected=True, actual={summary.get(key)!r}")
    return len(failed) == 0, failed


def verify_summary_counts(
    summary: Mapping[str, Any],
    expectations: Mapping[str, Any],
) -> Tuple[bool, List[str]]:
    failed: List[str] = []
    for key, expected in expectations.items():
        actual = summary.get(key)
        if actual != expected:
            failed.append(f"summary.{key}: expected={expected!r}, actual={actual!r}")
    return len(failed) == 0, failed


def verify_trace_list(
    trace_doc: Mapping[str, Any],
    *,
    expected_count: int,
    phase_id: Optional[str] = None,
) -> Tuple[bool, List[Dict[str, Any]], List[str]]:
    failed: List[str] = []
    traces = trace_doc.get("traces")
    if not isinstance(traces, list):
        return False, [], ["trace_doc.traces: missing or not a list"]

    if len(traces) != expected_count:
        failed.append(f"trace_count: expected={expected_count}, actual={len(traces)}")

    case_ids = [t.get("case_id") for t in traces if isinstance(t, dict)]
    if len(case_ids) != len(set(case_ids)):
        failed.append(f"case_id_not_unique: count={len(case_ids)}, unique={len(set(case_ids))}")

    if phase_id is not None and trace_doc.get("phase_id") != phase_id:
        failed.append(
            f"trace_doc.phase_id: expected={phase_id!r}, actual={trace_doc.get('phase_id')!r}"
        )

    return len(failed) == 0, traces, failed


def verify_trace_decision_distribution(
    traces: Iterable[Mapping[str, Any]],
    *,
    expected_positive_pass: int,
    expected_invalid_reject: int,
) -> Tuple[bool, int, int, List[str]]:
    failed: List[str] = []
    unexpected_pass = 0
    unexpected_fail = 0
    positive_pass = 0
    invalid_reject = 0

    for trace in traces:
        case_id = trace.get("case_id", "<unknown>")
        case_type = trace.get("case_type")
        decision = trace.get("trace_decision")

        if decision not in VALID_TRACE_DECISIONS:
            failed.append(f"{case_id}.trace_decision_invalid={decision!r}")
            continue

        if decision == "UNEXPECTED_PASS":
            unexpected_pass += 1
            failed.append(f"{case_id}.trace_decision=UNEXPECTED_PASS")
        elif decision == "UNEXPECTED_FAIL":
            unexpected_fail += 1
            failed.append(f"{case_id}.trace_decision=UNEXPECTED_FAIL")
        elif case_type == "positive":
            if decision == "PASS":
                positive_pass += 1
            else:
                failed.append(f"{case_id}.positive_not_pass={decision!r}")
        elif case_type == "invalid":
            if decision == "EXPECTED_REJECT":
                invalid_reject += 1
            else:
                failed.append(f"{case_id}.invalid_not_expected_reject={decision!r}")

    if positive_pass != expected_positive_pass:
        failed.append(
            f"positive_pass_count: expected={expected_positive_pass}, actual={positive_pass}"
        )
    if invalid_reject != expected_invalid_reject:
        failed.append(
            f"invalid_expected_reject_count: expected={expected_invalid_reject}, "
            f"actual={invalid_reject}"
        )

    ok = len(failed) == 0 and unexpected_pass == 0 and unexpected_fail == 0
    return ok, unexpected_pass, unexpected_fail, failed


def verify_invalid_cases_expected_reject(
    traces: Iterable[Mapping[str, Any]],
    invalid_case_ids: Sequence[str],
) -> Tuple[bool, List[str]]:
    by_id = {
        trace.get("case_id"): trace
        for trace in traces
        if isinstance(trace, dict) and trace.get("case_id")
    }
    failed: List[str] = []
    for case_id in invalid_case_ids:
        trace = by_id.get(case_id)
        if trace is None:
            failed.append(f"{case_id}.missing")
            continue
        if trace.get("case_type") != "invalid":
            failed.append(f"{case_id}.case_type_not_invalid={trace.get('case_type')!r}")
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"{case_id}.trace_decision={trace.get('trace_decision')!r}")
    return len(failed) == 0, failed


def build_outcome_doc(
    *,
    phase_id: str,
    step: str,
    input_root: str,
    input_trace_file: str,
    input_summary_file: str,
    output_file: str,
    verification_ok: bool,
    review_ok: bool,
    summary: Mapping[str, Any],
    trace_count: int,
    unexpected_pass_count: int,
    unexpected_fail_count: int,
    failed_checks: List[str],
    go_decision: str,
    blocked_decision: str,
    extra_fields: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    blocker_count = len(failed_checks)
    go_ok = verification_ok and review_ok and blocker_count == 0
    doc: Dict[str, Any] = {
        "phase_id": phase_id,
        "step": step,
        "lifecycle_template_id": PHASE_TEMPLATE_ID,
        "lifecycle_variant": "compressed_verify_and_review",
        "input_root": input_root,
        "input_trace_file": input_trace_file,
        "input_summary_file": input_summary_file,
        "output_file": output_file,
        "verification_ok": verification_ok,
        "review_ok": review_ok,
        "trace_count": trace_count,
        "positive_pass_count": summary.get("positive_pass_count"),
        "invalid_expected_reject_count": summary.get("invalid_expected_reject_count"),
        "unexpected_pass_count": unexpected_pass_count,
        "unexpected_fail_count": unexpected_fail_count,
        "runtime_execution_allowed": summary.get("runtime_execution_allowed"),
        "provider_activation_allowed": summary.get("provider_activation_allowed"),
        "fallback_execution_allowed": summary.get("fallback_execution_allowed"),
        "output_dispatch_allowed": summary.get("output_dispatch_allowed"),
        "real_provider_connected": summary.get("real_provider_connected"),
        "spatial_evidence_boundary_preserved": summary.get("spatial_evidence_boundary_preserved"),
        "vision_ocr_boundary_preserved": summary.get("vision_ocr_boundary_preserved"),
        "no_domain_specific_manager_duplication": summary.get(
            "no_domain_specific_manager_duplication"
        ),
        "candidate_only_enforced": summary.get("candidate_only_enforced"),
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "final_decision": go_decision if go_ok else blocked_decision,
    }
    if extra_fields:
        doc.update(dict(extra_fields))
    return doc
