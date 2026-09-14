# -*- coding: utf-8 -*-
"""Shared Provider Runtime Governance Skeleton — dry-run verifier v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_types_v1 import (
    DOMAIN_SPATIAL_EVIDENCE,
    DOMAIN_VISION_OCR,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_DRYRUN_TRACE_READY_FOR_VERIFIER,
    FINAL_DECISION_DRYRUN_VERIFIER_BLOCKED,
    FINAL_DECISION_DRYRUN_VERIFIER_GO,
    PHASE_ID,
    SHARED_MANAGER_REF,
)

DEFAULT_INPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "shared_provider_runtime_governance_dryrun_v1_smoke_v0"
)
TRACE_FILENAME = "provider_runtime_governance_dryrun_trace_v1.json"
SUMMARY_FILENAME = "provider_runtime_governance_dryrun_summary_v1.json"
VERIFICATION_FILENAME = "provider_runtime_governance_dryrun_verification_v1.json"

EXPECTED_POSITIVE_COUNT = 10
EXPECTED_INVALID_COUNT = 7
EXPECTED_TRACE_COUNT = 17
EXPECTED_VALIDATOR_RULES = len(VALIDATOR_RULE_IDS)

VALID_TRACE_DECISIONS = frozenset(
    {"PASS", "EXPECTED_REJECT", "UNEXPECTED_PASS", "UNEXPECTED_FAIL"}
)

REQUIRED_TRACE_SECTIONS = (
    "case_id",
    "case_name",
    "case_type",
    "case_goal",
    "manager",
    "domain_profile",
    "registry",
    "enable_disable",
    "runtime_state",
    "health_and_fallback",
    "runtime_admission",
    "governance_checkpoints",
    "validation",
    "trace_decision",
)

INVALID_A_ID = "invalid_a_default_enabled_provider"
INVALID_B_ID = "invalid_b_runtime_activation_allowed"
INVALID_C_ID = "invalid_c_missing_domain_profile"
INVALID_D_ID = "invalid_d_direct_action_forbidden"
INVALID_E_ID = "invalid_e_fallback_no_source_chain"
INVALID_F_ID = "invalid_f_spatial_bypass_field_synthesis"
INVALID_G_ID = "invalid_g_vision_ocr_spatial_candidate_pollution"

_SPATIAL_POLLUTION_CANDIDATES = frozenset({"PoseCandidate", "SLAMHealthCandidate"})
_FORBIDDEN_DIRECT_POLICIES = (
    "manager_direct_action",
    "manager_direct_speech",
    "manager_direct_fact_write",
)


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


def _errors_contain_any(errors: List[Any], needles: Tuple[str, ...]) -> bool:
    return any(_errors_contain(errors, needle) for needle in needles)


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
        "shared_provider_runtime_governance_ready": True,
        "vision_ocr_compatibility_preserved": True,
        "spatial_evidence_profile_supported": True,
        "no_domain_specific_manager_duplication": True,
        "runtime_activation_allowed": False,
        "provider_runtime_enabled": False,
        "candidate_only_enforced": True,
        "domain_profile_required": True,
        "final_decision": FINAL_DECISION_DRYRUN_TRACE_READY_FOR_VERIFIER,
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

    if trace_doc.get("phase_id") == PHASE_ID:
        passed.append("trace_doc.phase_id_ok=true")
    else:
        failed.append(
            f"trace_doc.phase_id: expected={PHASE_ID!r}, actual={trace_doc.get('phase_id')!r}"
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


def verify_runtime_still_disabled(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    for trace in traces:
        if trace.get("case_type") != "positive":
            continue
        case_id = trace.get("case_id", "<unknown>")
        manager = trace.get("manager") or {}
        runtime_state = trace.get("runtime_state") or {}
        checkpoints = trace.get("governance_checkpoints") or {}

        still_disabled = (
            manager.get("runtime_activation_allowed") is not True
            and manager.get("provider_runtime_enabled") is not True
            and runtime_state.get("provider_runtime_enabled") is not True
            and checkpoints.get("runtime_activation_still_disabled") is True
            and checkpoints.get("provider_runtime_still_disabled") is True
        )
        if still_disabled:
            passed.append(f"{case_id}.runtime_still_disabled=true")
        else:
            failed.append(
                f"{case_id}.runtime_not_disabled: manager={manager!r}, "
                f"runtime_state={runtime_state!r}"
            )

    return len(failed) == 0, passed, failed


def verify_domain_profile_presence(traces: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    for trace in traces:
        if trace.get("case_type") != "positive":
            continue
        case_id = trace.get("case_id", "<unknown>")
        profile = trace.get("domain_profile") or {}
        checkpoints = trace.get("governance_checkpoints") or {}

        present = (
            profile.get("domain_profile_present") is True
            and bool(profile.get("domain_profile_ref"))
            and bool(profile.get("domain_id"))
            and checkpoints.get("domain_profile_required") is True
        )
        if present:
            passed.append(f"{case_id}.domain_profile_present=true")
        else:
            failed.append(f"{case_id}.domain_profile_missing={profile!r}")

    return len(failed) == 0, passed, failed


def verify_spatial_evidence_profile_boundary(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    spatial_positive = [
        t
        for t in traces
        if t.get("case_type") == "positive"
        and (t.get("domain_profile") or {}).get("domain_id") == DOMAIN_SPATIAL_EVIDENCE
    ]
    if not spatial_positive:
        failed.append("spatial_evidence_positive_cases_missing")
        return False, passed, failed

    for trace in spatial_positive:
        case_id = trace.get("case_id", "<unknown>")
        profile = trace.get("domain_profile") or {}
        manager = trace.get("manager") or {}
        checkpoints = trace.get("governance_checkpoints") or {}

        boundary_ok = (
            profile.get("domain_id") == DOMAIN_SPATIAL_EVIDENCE
            and profile.get("synthesis_entrypoint") == FIELD_SYNTHESIS_ENTRYPOINT
            and manager.get("runtime_activation_allowed") is not True
            and manager.get("provider_runtime_enabled") is not True
            and checkpoints.get("spatial_evidence_profile_supported") is True
            and SHARED_MANAGER_REF in str(manager.get("manager_ref") or "")
        )
        if boundary_ok:
            passed.append(f"{case_id}.spatial_evidence_boundary_ok=true")
        else:
            failed.append(
                f"{case_id}.spatial_evidence_boundary_failed: profile={profile!r}, "
                f"manager={manager!r}"
            )

    return len(failed) == 0, passed, failed


def verify_vision_ocr_compatibility_boundary(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    vision_positive = [
        t
        for t in traces
        if t.get("case_type") == "positive"
        and (t.get("domain_profile") or {}).get("domain_id") == DOMAIN_VISION_OCR
    ]
    if not vision_positive:
        failed.append("vision_ocr_positive_cases_missing")
        return False, passed, failed

    for trace in vision_positive:
        case_id = trace.get("case_id", "<unknown>")
        profile = trace.get("domain_profile") or {}
        checkpoints = trace.get("governance_checkpoints") or {}
        declared = set(profile.get("candidate_types") or ())

        no_spatial_pollution = not any(
            ctype in declared for ctype in _SPATIAL_POLLUTION_CANDIDATES
        )
        boundary_ok = (
            profile.get("domain_id") == DOMAIN_VISION_OCR
            and checkpoints.get("vision_ocr_compatibility_preserved") is True
            and no_spatial_pollution
            and (trace.get("manager") or {}).get("runtime_activation_allowed") is not True
        )
        if boundary_ok:
            passed.append(f"{case_id}.vision_ocr_boundary_ok=true")
        else:
            failed.append(
                f"{case_id}.vision_ocr_boundary_failed: profile={profile!r}, "
                f"checkpoints={checkpoints!r}"
            )

    return len(failed) == 0, passed, failed


def verify_no_domain_specific_manager_duplication(
    traces: List[Dict[str, Any]],
    summary: Dict[str, Any],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    if summary.get("no_domain_specific_manager_duplication") is not True:
        failed.append("summary.no_domain_specific_manager_duplication=false")
    else:
        passed.append("summary.no_domain_specific_manager_duplication=true")

    for trace in traces:
        if trace.get("case_type") != "positive":
            continue
        case_id = trace.get("case_id", "<unknown>")
        manager_ref = str((trace.get("manager") or {}).get("manager_ref") or "")
        checkpoints = trace.get("governance_checkpoints") or {}

        if not manager_ref:
            profile_only_ok = (
                checkpoints.get("no_domain_specific_manager_duplication") is True
                and (trace.get("domain_profile") or {}).get("domain_profile_present") is True
            )
            if profile_only_ok:
                passed.append(f"{case_id}.shared_manager_skeleton_profile_only=true")
            else:
                failed.append(
                    f"{case_id}.profile_only_case_missing_shared_skeleton_checkpoints"
                )
            continue

        uses_shared = (
            SHARED_MANAGER_REF in manager_ref
            and checkpoints.get("no_domain_specific_manager_duplication") is True
            and "spatial_evidence_provider_manager" not in manager_ref
            and "vision_ocr_provider_manager" not in manager_ref
        )
        if uses_shared:
            passed.append(f"{case_id}.shared_manager_skeleton=true")
        else:
            failed.append(f"{case_id}.domain_specific_manager_detected: ref={manager_ref!r}")

    return len(failed) == 0, passed, failed


def verify_invalid_a_default_enable_block(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_A_ID)
    if trace is None:
        return False, passed, [f"{INVALID_A_ID}.missing"]

    registry = trace.get("registry") or {}
    validation = trace.get("validation") or {}
    errors = validation.get("errors") or []

    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        registry.get("enabled_by_default_count", 0) >= 1
        or registry.get("runtime_enable_allowed_count", 0) >= 1,
        validation.get("actual_validation_ok") is False,
        _errors_contain(errors, "enabled_by_default")
        or _errors_contain(errors, "runtime_enable_allowed"),
    ]
    if all(checks):
        passed.append("invalid_a.default_enable_blocked=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_a.trace_decision={trace.get('trace_decision')!r}")
        if registry.get("enabled_by_default_count", 0) < 1 and registry.get(
            "runtime_enable_allowed_count", 0
        ) < 1:
            failed.append(f"invalid_a.registry_counts={registry!r}")
        if not (
            _errors_contain(errors, "enabled_by_default")
            or _errors_contain(errors, "runtime_enable_allowed")
        ):
            failed.append(f"invalid_a.errors_missing_enable_block={errors!r}")

    return len(failed) == 0, passed, failed


def verify_invalid_b_runtime_activation_block(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_B_ID)
    if trace is None:
        return False, passed, [f"{INVALID_B_ID}.missing"]

    manager = trace.get("manager") or {}
    runtime_state = trace.get("runtime_state") or {}
    validation = trace.get("validation") or {}
    errors = validation.get("errors") or []

    activation_open = (
        manager.get("runtime_activation_allowed") is True
        or manager.get("provider_runtime_enabled") is True
        or runtime_state.get("provider_runtime_enabled") is True
    )
    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        activation_open,
        validation.get("actual_validation_ok") is False,
        _errors_contain(errors, "runtime_activation_allowed")
        or _errors_contain(errors, "provider_runtime_enabled"),
    ]
    if all(checks):
        passed.append("invalid_b.runtime_activation_blocked=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_b.trace_decision={trace.get('trace_decision')!r}")
        if not activation_open:
            failed.append(f"invalid_b.activation_not_open={manager!r}")
        if not (
            _errors_contain(errors, "runtime_activation_allowed")
            or _errors_contain(errors, "provider_runtime_enabled")
        ):
            failed.append(f"invalid_b.errors_missing_activation_block={errors!r}")

    return len(failed) == 0, passed, failed


def verify_invalid_c_domain_profile_missing_block(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_C_ID)
    if trace is None:
        return False, passed, [f"{INVALID_C_ID}.missing"]

    profile = trace.get("domain_profile") or {}
    validation = trace.get("validation") or {}
    errors = validation.get("errors") or []

    profile_missing = (
        profile.get("domain_profile_present") is False
        or not profile.get("domain_profile_ref")
        or not profile.get("domain_id")
    )
    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        profile_missing,
        validation.get("actual_validation_ok") is False,
        _errors_contain(errors, "domain_profile"),
    ]
    if all(checks):
        passed.append("invalid_c.domain_profile_missing_blocked=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_c.trace_decision={trace.get('trace_decision')!r}")
        if not profile_missing:
            failed.append(f"invalid_c.domain_profile_present={profile!r}")
        if not _errors_contain(errors, "domain_profile"):
            failed.append(f"invalid_c.errors_missing_profile_block={errors!r}")

    return len(failed) == 0, passed, failed


def verify_invalid_d_direct_output_block(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_D_ID)
    if trace is None:
        return False, passed, [f"{INVALID_D_ID}.missing"]

    validation = trace.get("validation") or {}
    errors = validation.get("errors") or []
    checkpoints = trace.get("governance_checkpoints") or {}

    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        _errors_contain_any(errors, _FORBIDDEN_DIRECT_POLICIES),
        validation.get("actual_validation_ok") is False,
        checkpoints.get("no_direct_action") is False
        or checkpoints.get("no_direct_speech") is False
        or checkpoints.get("no_direct_fact_write") is False
        or _errors_contain_any(errors, _FORBIDDEN_DIRECT_POLICIES),
    ]
    if all(checks):
        passed.append("invalid_d.direct_output_blocked=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_d.trace_decision={trace.get('trace_decision')!r}")
        if not _errors_contain_any(errors, _FORBIDDEN_DIRECT_POLICIES):
            failed.append(f"invalid_d.errors_missing_direct_policy={errors!r}")

    return len(failed) == 0, passed, failed


def verify_invalid_e_fallback_source_chain_block(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_E_ID)
    if trace is None:
        return False, passed, [f"{INVALID_E_ID}.missing"]

    health_fallback = trace.get("health_and_fallback") or {}
    validation = trace.get("validation") or {}
    errors = validation.get("errors") or []
    checkpoints = trace.get("governance_checkpoints") or {}

    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        health_fallback.get("source_chain_preserved") is False,
        checkpoints.get("fallback_preserves_source_chain") is False,
        validation.get("actual_validation_ok") is False,
        _errors_contain(errors, "preserve_source_chain"),
    ]
    if all(checks):
        passed.append("invalid_e.fallback_source_chain_blocked=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_e.trace_decision={trace.get('trace_decision')!r}")
        if health_fallback.get("source_chain_preserved") is not False:
            failed.append(f"invalid_e.source_chain_preserved={health_fallback!r}")
        if not _errors_contain(errors, "preserve_source_chain"):
            failed.append(f"invalid_e.errors_missing_source_chain={errors!r}")

    return len(failed) == 0, passed, failed


def verify_invalid_f_spatial_synthesis_bypass_block(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_F_ID)
    if trace is None:
        return False, passed, [f"{INVALID_F_ID}.missing"]

    manager = trace.get("manager") or {}
    profile = trace.get("domain_profile") or {}
    validation = trace.get("validation") or {}
    errors = validation.get("errors") or []

    domain_ok = (
        manager.get("domain_id") == DOMAIN_SPATIAL_EVIDENCE
        or profile.get("domain_id") == DOMAIN_SPATIAL_EVIDENCE
    )
    bypass_signal = (
        _errors_contain(errors, "synthesis_entrypoint")
        or profile.get("synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT
    )
    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        domain_ok,
        bypass_signal,
        validation.get("actual_validation_ok") is False,
    ]
    if all(checks):
        passed.append("invalid_f.spatial_synthesis_bypass_blocked=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_f.trace_decision={trace.get('trace_decision')!r}")
        if not domain_ok:
            failed.append(f"invalid_f.domain_id_mismatch={manager!r},{profile!r}")
        if not bypass_signal:
            failed.append(f"invalid_f.synthesis_bypass_not_detected={errors!r}")

    return len(failed) == 0, passed, failed


def verify_invalid_g_vision_ocr_spatial_pollution_block(
    traces: List[Dict[str, Any]],
) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []
    trace = _trace_by_id(traces, INVALID_G_ID)
    if trace is None:
        return False, passed, [f"{INVALID_G_ID}.missing"]

    profile = trace.get("domain_profile") or {}
    validation = trace.get("validation") or {}
    errors = validation.get("errors") or []
    checkpoints = trace.get("governance_checkpoints") or {}

    pollution_errors = (
        _errors_contain(errors, "PoseCandidate")
        or _errors_contain(errors, "SLAMHealthCandidate")
        or _errors_contain(errors, "candidate_not_in_domain_profile")
    )
    checks = [
        trace.get("trace_decision") == "EXPECTED_REJECT",
        profile.get("domain_id") == DOMAIN_VISION_OCR,
        pollution_errors,
        validation.get("actual_validation_ok") is False,
        checkpoints.get("vision_ocr_compatibility_preserved") is False,
    ]
    if all(checks):
        passed.append("invalid_g.vision_ocr_spatial_pollution_blocked=true")
    else:
        if trace.get("trace_decision") != "EXPECTED_REJECT":
            failed.append(f"invalid_g.trace_decision={trace.get('trace_decision')!r}")
        if profile.get("domain_id") != DOMAIN_VISION_OCR:
            failed.append(f"invalid_g.domain_id={profile.get('domain_id')!r}")
        if not pollution_errors:
            failed.append(f"invalid_g.errors_missing_spatial_pollution={errors!r}")

    return len(failed) == 0, passed, failed


def verify_provider_runtime_governance_dryrun_v1(
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

    runtime_still_disabled_ok, p, f = verify_runtime_still_disabled(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    domain_profile_presence_ok, p, f = verify_domain_profile_presence(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    spatial_boundary_ok, p, f = verify_spatial_evidence_profile_boundary(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    vision_boundary_ok, p, f = verify_vision_ocr_compatibility_boundary(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    no_dup_ok, p, f = verify_no_domain_specific_manager_duplication(traces, summary)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_a_ok, p, f = verify_invalid_a_default_enable_block(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_b_ok, p, f = verify_invalid_b_runtime_activation_block(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_c_ok, p, f = verify_invalid_c_domain_profile_missing_block(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_d_ok, p, f = verify_invalid_d_direct_output_block(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_e_ok, p, f = verify_invalid_e_fallback_source_chain_block(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_f_ok, p, f = verify_invalid_f_spatial_synthesis_bypass_block(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    invalid_g_ok, p, f = verify_invalid_g_vision_ocr_spatial_pollution_block(traces)
    all_passed.extend(p)
    all_failed.extend(f)

    blocker_count = len(all_failed)
    go_ok = (
        summary_ok
        and trace_count_ok
        and case_id_unique_ok
        and trace_decision_ok
        and sections_ok
        and runtime_still_disabled_ok
        and domain_profile_presence_ok
        and spatial_boundary_ok
        and vision_boundary_ok
        and no_dup_ok
        and invalid_a_ok
        and invalid_b_ok
        and invalid_c_ok
        and invalid_d_ok
        and invalid_e_ok
        and invalid_f_ok
        and invalid_g_ok
        and unexpected_pass == 0
        and unexpected_fail == 0
        and blocker_count == 0
    )

    verification: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Step 4 Shared Provider Runtime Governance Dry-run Verifier",
        "input_root": str(root),
        "input_trace_file": str(trace_path),
        "input_summary_file": str(summary_path),
        "summary_check_ok": summary_ok,
        "trace_count_check_ok": trace_count_ok,
        "case_id_unique_check_ok": case_id_unique_ok,
        "trace_decision_check_ok": trace_decision_ok,
        "required_sections_check_ok": sections_ok,
        "runtime_still_disabled_check_ok": runtime_still_disabled_ok,
        "domain_profile_presence_check_ok": domain_profile_presence_ok,
        "spatial_evidence_profile_boundary_check_ok": spatial_boundary_ok,
        "vision_ocr_compatibility_boundary_check_ok": vision_boundary_ok,
        "no_domain_specific_manager_duplication_check_ok": no_dup_ok,
        "invalid_a_default_enable_check_ok": invalid_a_ok,
        "invalid_b_runtime_activation_check_ok": invalid_b_ok,
        "invalid_c_domain_profile_missing_check_ok": invalid_c_ok,
        "invalid_d_direct_output_check_ok": invalid_d_ok,
        "invalid_e_fallback_source_chain_check_ok": invalid_e_ok,
        "invalid_f_spatial_synthesis_bypass_check_ok": invalid_f_ok,
        "invalid_g_vision_ocr_spatial_pollution_check_ok": invalid_g_ok,
        "positive_pass_count": summary.get("positive_pass_count"),
        "invalid_expected_reject_count": summary.get("invalid_expected_reject_count"),
        "unexpected_pass_count": unexpected_pass,
        "unexpected_fail_count": unexpected_fail,
        "trace_count": len(traces),
        "validator_rules": EXPECTED_VALIDATOR_RULES,
        "blocker_count": blocker_count,
        "passed_checks": all_passed,
        "failed_checks": all_failed,
        "final_decision": (
            FINAL_DECISION_DRYRUN_VERIFIER_GO if go_ok else FINAL_DECISION_DRYRUN_VERIFIER_BLOCKED
        ),
    }

    if write_file:
        out_path = root / VERIFICATION_FILENAME
        out_path.write_text(
            json.dumps(verification, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        verification["output_verification_file"] = str(out_path)

    return verification


def main() -> int:
    try:
        verification = verify_provider_runtime_governance_dryrun_v1()
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1

    print(
        json.dumps(
            {
                "input_root": verification.get("input_root"),
                "output_verification_file": verification.get("output_verification_file"),
                "summary_check_ok": verification["summary_check_ok"],
                "trace_count_check_ok": verification["trace_count_check_ok"],
                "trace_decision_check_ok": verification["trace_decision_check_ok"],
                "runtime_still_disabled_check_ok": verification["runtime_still_disabled_check_ok"],
                "vision_ocr_compatibility_boundary_check_ok": verification[
                    "vision_ocr_compatibility_boundary_check_ok"
                ],
                "spatial_evidence_profile_boundary_check_ok": verification[
                    "spatial_evidence_profile_boundary_check_ok"
                ],
                "blocker_count": verification["blocker_count"],
                "final_decision": verification["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verification["final_decision"] == FINAL_DECISION_DRYRUN_VERIFIER_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
