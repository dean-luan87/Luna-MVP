# -*- coding: utf-8 -*-
"""Field Spatial Evidence Provider Admission Planning — dry-run verifier v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
)
from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_types_v1 import (
    FIELD_SYNTHESIS_ENTRYPOINT,
    PHASE_ID,
)

DEFAULT_INPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "field_spatial_evidence_provider_admission_dryrun_v1_smoke_v0"
)
TRACE_FILENAME = "field_spatial_evidence_provider_admission_dryrun_trace_v1.json"
SUMMARY_FILENAME = "field_spatial_evidence_provider_admission_dryrun_summary_v1.json"
VERIFICATION_FILENAME = "field_spatial_evidence_provider_admission_dryrun_verification_v1.json"

EXPECTED_SUMMARY_FINAL_DECISION = (
    "FIELD_SPATIAL_EVIDENCE_PROVIDER_ADMISSION_DRYRUN_TRACE_READY_FOR_VERIFIER"
)
FINAL_DECISION_GO = "FIELD_SPATIAL_EVIDENCE_PROVIDER_ADMISSION_DRYRUN_VERIFIER_GO"
FINAL_DECISION_BLOCKED = "FIELD_SPATIAL_EVIDENCE_PROVIDER_ADMISSION_DRYRUN_VERIFIER_BLOCKED"

VALID_TRACE_DECISIONS = frozenset(
    {"PASS", "EXPECTED_REJECT", "UNEXPECTED_PASS", "UNEXPECTED_FAIL"}
)

REQUIRED_TRACE_SECTIONS = (
    "case_id",
    "case_name",
    "case_type",
    "case_goal",
    "provider_policy",
    "capability_profile",
    "health_gate",
    "fallback_policy",
    "runtime_admission",
    "planning_decision",
    "governance_checkpoints",
    "validation",
    "trace_decision",
)

INVALID_A_ID = "invalid_a_gpl_provider_commercial_runtime"
INVALID_B_ID = "invalid_b_observation_provider_runtime_admission"
INVALID_C_ID = "invalid_c_runtime_admission_without_health_gate"
INVALID_D_ID = "invalid_d_fallback_required_missing_policy"
INVALID_E_ID = "invalid_e_field_synthesis_entrypoint_bypass"
INVALID_F_ID = "invalid_f_required_candidates_not_in_profile"

EXPECTED_POSITIVE_COUNT = 7
EXPECTED_INVALID_COUNT = 6
EXPECTED_TRACE_COUNT = 13
EXPECTED_VALIDATOR_RULES = 20


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
        "runtime_admission_candidates_empty": True,
        "commercial_runtime_candidates_empty": True,
        "gpl_commercial_blocked": True,
        "observation_runtime_blocked": True,
        "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT,
        "health_gate_required": True,
        "fallback_required": True,
        "provider_replaceability_required": True,
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


def verify_positive_runtime_still_disabled(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    for trace in traces:
        if trace.get("case_type") != "positive":
            continue
        case_id = trace.get("case_id", "<unknown>")
        policy = trace.get("provider_policy") or {}
        admission = trace.get("runtime_admission") or {}
        checkpoints = trace.get("governance_checkpoints") or {}

        policy_runtime = policy.get("runtime_admission_allowed")
        admission_runtime = admission.get("runtime_admission_allowed")
        still_disabled = (
            policy_runtime is not True
            and admission_runtime is not True
            and checkpoints.get("runtime_admission_still_disabled") is True
        )
        if still_disabled:
            passed.append(f"{case_id}.runtime_admission_still_disabled=true")
        else:
            failed.append(
                f"{case_id}.runtime_admission_not_disabled: "
                f"policy={policy_runtime!r}, admission={admission_runtime!r}"
            )

    return len(failed) == 0, passed, failed


def verify_field_synthesis_entrypoint_locked(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    for trace in traces:
        if trace.get("case_type") != "positive":
            continue
        case_id = trace.get("case_id", "<unknown>")
        policy = trace.get("provider_policy") or {}
        checkpoints = trace.get("governance_checkpoints") or {}

        entrypoint = policy.get("field_synthesis_entrypoint")
        locked = (
            entrypoint == FIELD_SYNTHESIS_ENTRYPOINT
            and checkpoints.get("field_synthesis_entrypoint_locked") is True
        )
        if locked:
            passed.append(f"{case_id}.field_synthesis_entrypoint_locked=true")
        else:
            failed.append(
                f"{case_id}.field_synthesis_entrypoint: expected={FIELD_SYNTHESIS_ENTRYPOINT!r}, "
                f"actual={entrypoint!r}"
            )

    return len(failed) == 0, passed, failed


def verify_health_gate_and_fallback_gate(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    health_ok_all = True
    fallback_ok_all = True

    for trace in traces:
        if trace.get("case_type") != "positive":
            continue
        case_id = trace.get("case_id", "<unknown>")
        health = trace.get("health_gate") or {}
        fallback = trace.get("fallback_policy") or {}
        planning = trace.get("planning_decision") or {}
        checkpoints = trace.get("governance_checkpoints") or {}

        health_ok = (
            bool(health.get("required_health_signals"))
            and health.get("tracking_lost_policy")
            and health.get("degradation_output_policy")
            and checkpoints.get("health_gate_required") is True
            and planning.get("health_gate_required") is True
        )
        fallback_ok = (
            bool(fallback.get("fallback_policy_ref"))
            and fallback.get("preserve_source_chain") is True
            and fallback.get("preserve_conflict_refs") is True
            and checkpoints.get("fallback_required") is True
            and planning.get("fallback_required") is True
        )

        if health_ok:
            passed.append(f"{case_id}.health_gate_ok=true")
        else:
            health_ok_all = False
            failed.append(f"{case_id}.health_gate_incomplete={health!r}")

        if fallback_ok:
            passed.append(f"{case_id}.fallback_gate_ok=true")
        else:
            fallback_ok_all = False
            failed.append(f"{case_id}.fallback_gate_incomplete={fallback!r}")

    return health_ok_all, fallback_ok_all, passed, failed


def verify_capability_coverage(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    for trace in traces:
        if trace.get("case_type") != "positive":
            continue
        case_id = trace.get("case_id", "<unknown>")
        checkpoints = trace.get("governance_checkpoints") or {}
        profile = trace.get("capability_profile") or {}

        covered = checkpoints.get("required_candidates_covered_by_profile") is True
        supported = profile.get("supported_candidate_types") or []
        if covered and supported:
            passed.append(f"{case_id}.capability_coverage_ok=true")
        else:
            failed.append(
                f"{case_id}.capability_coverage_failed: "
                f"covered={covered!r}, supported={supported!r}"
            )

    return len(failed) == 0, passed, failed


def verify_invalid_a_gpl_commercial_block(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_A_ID)
    if trace is None:
        return False, passed, [f"{INVALID_A_ID}.missing"]

    policy = trace.get("provider_policy") or {}
    validation = trace.get("validation") or {}
    errors = validation.get("errors") or []

    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        policy.get("commercial_runtime_allowed") is True,
        policy.get("admission_mode") == "commercial_runtime_candidate",
        _errors_contain(errors, "gpl_provider_commercial_runtime_not_allowed"),
        validation.get("actual_validation_ok") is False,
    ]
    if all(checks):
        passed.append("invalid_a.gpl_commercial_runtime_rejected=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_a.trace_decision={trace.get('trace_decision')!r}")
        if not _errors_contain(errors, "gpl_provider_commercial_runtime_not_allowed"):
            failed.append(f"invalid_a.errors_missing_gpl_block={errors!r}")

    return len(failed) == 0, passed, failed


def verify_invalid_b_observation_runtime_block(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_B_ID)
    if trace is None:
        return False, passed, [f"{INVALID_B_ID}.missing"]

    policy = trace.get("provider_policy") or {}
    admission = trace.get("runtime_admission") or {}
    validation = trace.get("validation") or {}
    errors = validation.get("errors") or []

    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        policy.get("admission_mode") == "observation_only",
        admission.get("runtime_admission_allowed") is True,
        _errors_contain(errors, "observation_provider_runtime_admission_not_allowed"),
        validation.get("actual_validation_ok") is False,
    ]
    if all(checks):
        passed.append("invalid_b.observation_runtime_admission_rejected=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_b.trace_decision={trace.get('trace_decision')!r}")
        if policy.get("admission_mode") != "observation_only":
            failed.append(f"invalid_b.admission_mode={policy.get('admission_mode')!r}")
        if admission.get("runtime_admission_allowed") is not True:
            failed.append(
                f"invalid_b.runtime_admission_allowed="
                f"{admission.get('runtime_admission_allowed')!r}"
            )

    return len(failed) == 0, passed, failed


def verify_invalid_c_health_gate_block(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_C_ID)
    if trace is None:
        return False, passed, [f"{INVALID_C_ID}.missing"]

    admission = trace.get("runtime_admission") or {}
    validation = trace.get("validation") or {}
    errors = validation.get("errors") or []

    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        admission.get("runtime_admission_allowed") is True,
        admission.get("health_gate_passed") is False,
        _errors_contain(errors, "runtime_admission_requires_health_gate_passed"),
        validation.get("actual_validation_ok") is False,
    ]
    if all(checks):
        passed.append("invalid_c.health_gate_bypass_rejected=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_c.trace_decision={trace.get('trace_decision')!r}")
        if admission.get("runtime_admission_allowed") is not True:
            failed.append(
                f"invalid_c.runtime_admission_allowed="
                f"{admission.get('runtime_admission_allowed')!r}"
            )
        if admission.get("health_gate_passed") is not False:
            failed.append(
                f"invalid_c.health_gate_passed={admission.get('health_gate_passed')!r}"
            )

    return len(failed) == 0, passed, failed


def verify_invalid_d_fallback_missing_block(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_D_ID)
    if trace is None:
        return False, passed, [f"{INVALID_D_ID}.missing"]

    fallback = trace.get("fallback_policy") or {}
    admission = trace.get("runtime_admission") or {}
    validation = trace.get("validation") or {}
    errors = validation.get("errors") or []

    fallback_missing = (
        not fallback.get("fallback_policy_ref")
        or admission.get("fallback_policy_passed") is False
    )

    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        fallback_missing,
        _errors_contain(errors, "fallback_policy_ref_required")
        or _errors_contain(errors, "runtime_admission_requires_fallback_policy_passed"),
        validation.get("actual_validation_ok") is False,
    ]
    if all(checks):
        passed.append("invalid_d.fallback_missing_rejected=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_d.trace_decision={trace.get('trace_decision')!r}")
        if not fallback_missing:
            failed.append(
                f"invalid_d.fallback_present: ref={fallback.get('fallback_policy_ref')!r}, "
                f"passed={admission.get('fallback_policy_passed')!r}"
            )

    return len(failed) == 0, passed, failed


def verify_invalid_e_field_synthesis_bypass_block(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_E_ID)
    if trace is None:
        return False, passed, [f"{INVALID_E_ID}.missing"]

    policy = trace.get("provider_policy") or {}
    validation = trace.get("validation") or {}
    errors = validation.get("errors") or {}

    entrypoint = policy.get("field_synthesis_entrypoint")
    bypassed = entrypoint != FIELD_SYNTHESIS_ENTRYPOINT

    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        bypassed,
        _errors_contain(errors, "field_synthesis_entrypoint_must_be_field_synthesis_v1"),
        validation.get("actual_validation_ok") is False,
    ]
    if all(checks):
        passed.append("invalid_e.field_synthesis_bypass_rejected=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_e.trace_decision={trace.get('trace_decision')!r}")
        if not bypassed:
            failed.append(f"invalid_e.field_synthesis_entrypoint={entrypoint!r}")

    return len(failed) == 0, passed, failed


def verify_invalid_f_capability_coverage_block(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_F_ID)
    if trace is None:
        return False, passed, [f"{INVALID_F_ID}.missing"]

    profile = trace.get("capability_profile") or {}
    checkpoints = trace.get("governance_checkpoints") or {}
    validation = trace.get("validation") or {}
    errors = validation.get("errors") or []

    supported = set(profile.get("supported_candidate_types") or ())
    coverage_failed = checkpoints.get("required_candidates_covered_by_profile") is False

    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        coverage_failed,
        _errors_contain(errors, "required_not_supported"),
        validation.get("actual_validation_ok") is False,
        "SLAMHealthCandidate" not in supported,
    ]
    if all(checks):
        passed.append("invalid_f.capability_coverage_rejected=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_f.trace_decision={trace.get('trace_decision')!r}")
        if not coverage_failed:
            failed.append(
                f"invalid_f.required_candidates_covered_by_profile="
                f"{checkpoints.get('required_candidates_covered_by_profile')!r}"
            )

    return len(failed) == 0, passed, failed


def verify_field_spatial_evidence_provider_admission_dryrun_v1(
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

    positive_runtime_ok, p, f = verify_positive_runtime_still_disabled(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    field_synthesis_ok, p, f = verify_field_synthesis_entrypoint_locked(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    health_gate_ok, fallback_gate_ok, p, f = verify_health_gate_and_fallback_gate(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    capability_coverage_ok, p, f = verify_capability_coverage(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_a_ok, p, f = verify_invalid_a_gpl_commercial_block(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_b_ok, p, f = verify_invalid_b_observation_runtime_block(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_c_ok, p, f = verify_invalid_c_health_gate_block(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_d_ok, p, f = verify_invalid_d_fallback_missing_block(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_e_ok, p, f = verify_invalid_e_field_synthesis_bypass_block(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_f_ok, p, f = verify_invalid_f_capability_coverage_block(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    blocker_count = len(all_failed)
    go_ok = (
        summary_ok
        and trace_count_ok
        and case_id_unique_ok
        and trace_decision_ok
        and sections_ok
        and positive_runtime_ok
        and field_synthesis_ok
        and health_gate_ok
        and fallback_gate_ok
        and capability_coverage_ok
        and invalid_a_ok
        and invalid_b_ok
        and invalid_c_ok
        and invalid_d_ok
        and invalid_e_ok
        and invalid_f_ok
        and summary.get("positive_pass_count") == EXPECTED_POSITIVE_COUNT
        and summary.get("invalid_expected_reject_count") == EXPECTED_INVALID_COUNT
        and unexpected_pass == 0
        and unexpected_fail == 0
        and blocker_count == 0
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Step 4 Provider Admission Dry-run Verifier",
        "input_trace_file": str(trace_path),
        "input_summary_file": str(summary_path),
        "summary_check_ok": summary_ok,
        "trace_count_check_ok": trace_count_ok,
        "case_id_unique_check_ok": case_id_unique_ok,
        "trace_decision_check_ok": trace_decision_ok,
        "required_sections_check_ok": sections_ok,
        "positive_runtime_still_disabled_check_ok": positive_runtime_ok,
        "field_synthesis_entrypoint_locked_check_ok": field_synthesis_ok,
        "health_gate_check_ok": health_gate_ok,
        "fallback_gate_check_ok": fallback_gate_ok,
        "capability_coverage_check_ok": capability_coverage_ok,
        "invalid_a_gpl_commercial_check_ok": invalid_a_ok,
        "invalid_b_observation_runtime_check_ok": invalid_b_ok,
        "invalid_c_health_gate_check_ok": invalid_c_ok,
        "invalid_d_fallback_missing_check_ok": invalid_d_ok,
        "invalid_e_field_synthesis_bypass_check_ok": invalid_e_ok,
        "invalid_f_capability_coverage_check_ok": invalid_f_ok,
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
    result = verify_field_spatial_evidence_provider_admission_dryrun_v1()
    print(
        json.dumps(
            {
                "input_trace_file": result["input_trace_file"],
                "input_summary_file": result["input_summary_file"],
                "output_verification_file": result.get("output_verification_file"),
                "summary_check_ok": result["summary_check_ok"],
                "trace_count_check_ok": result["trace_count_check_ok"],
                "invalid_a_gpl_commercial_check_ok": result["invalid_a_gpl_commercial_check_ok"],
                "invalid_b_observation_runtime_check_ok": result[
                    "invalid_b_observation_runtime_check_ok"
                ],
                "invalid_c_health_gate_check_ok": result["invalid_c_health_gate_check_ok"],
                "invalid_d_fallback_missing_check_ok": result["invalid_d_fallback_missing_check_ok"],
                "invalid_e_field_synthesis_bypass_check_ok": result[
                    "invalid_e_field_synthesis_bypass_check_ok"
                ],
                "invalid_f_capability_coverage_check_ok": result[
                    "invalid_f_capability_coverage_check_ok"
                ],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
