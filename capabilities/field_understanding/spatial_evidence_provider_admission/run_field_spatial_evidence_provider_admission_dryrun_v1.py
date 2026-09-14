# -*- coding: utf-8 -*-
"""Field Spatial Evidence Provider Admission Planning — dry-run runner v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_dryrun_cases_v1 import (
    FieldSpatialEvidenceProviderAdmissionDryRunCase,
    build_all_provider_admission_cases_v1,
    bundle_from_provider_admission_case,
)
from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_registry_v1 import (
    BLOCKED_RUNTIME_PROVIDER_REFS,
    GPL_BACKEND_REFS,
    OBSERVATION_ONLY_PROVIDER_REFS,
    build_provider_admission_planning_matrix_v1,
)
from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
    _gpl_commercial_blocked,
    _observation_runtime_blocked,
    validate_provider_admission_case_bundle,
    validate_required_candidates_subset_of_supported,
)
from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_types_v1 import (
    ADMISSION_PRINCIPLE_ZH,
    FIELD_SYNTHESIS_ENTRYPOINT,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
)

DEFAULT_OUTPUT = (
    _REPO_ROOT / "_tmp_eval_out" / "field_spatial_evidence_provider_admission_dryrun_v1_smoke_v0"
)
TRACE_FILENAME = "field_spatial_evidence_provider_admission_dryrun_trace_v1.json"
SUMMARY_FILENAME = "field_spatial_evidence_provider_admission_dryrun_summary_v1.json"

FINAL_DECISION_TRACE_READY = (
    "FIELD_SPATIAL_EVIDENCE_PROVIDER_ADMISSION_DRYRUN_TRACE_READY_FOR_VERIFIER"
)
FINAL_DECISION_RUNNER_FAIL = (
    "FIELD_SPATIAL_EVIDENCE_PROVIDER_ADMISSION_DRYRUN_RUNNER_UNEXPECTED_OUTCOME"
)

TraceDecision = Literal["PASS", "EXPECTED_REJECT", "UNEXPECTED_PASS", "UNEXPECTED_FAIL"]

_PLANNING_DECISION = build_provider_admission_planning_matrix_v1().get("decision") or {}


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


def _planning_decision_snapshot() -> Dict[str, Any]:
    return {
        "runtime_admission_candidates": list(
            _PLANNING_DECISION.get("runtime_admission_candidates") or ()
        ),
        "commercial_runtime_candidates": list(
            _PLANNING_DECISION.get("commercial_runtime_candidates") or ()
        ),
        "blocked_runtime_providers": list(
            _PLANNING_DECISION.get("blocked_runtime_providers")
            or sorted(BLOCKED_RUNTIME_PROVIDER_REFS)
        ),
        "observation_only_providers": list(
            _PLANNING_DECISION.get("observation_only_providers")
            or sorted(OBSERVATION_ONLY_PROVIDER_REFS)
        ),
        "fallback_required": _PLANNING_DECISION.get("fallback_required") is True,
        "health_gate_required": _PLANNING_DECISION.get("health_gate_required") is True,
        "provider_replaceability_required": (
            _PLANNING_DECISION.get("provider_replaceability_required") is True
        ),
    }


def _governance_checkpoints(
    bundle: Dict[str, Any],
) -> Dict[str, bool]:
    policies = list(bundle.get("admission_policies") or ())
    profiles = list(bundle.get("capability_profiles") or ())
    admissions = list(bundle.get("runtime_admission_candidates") or ())

    policy = _first_item(policies)
    profile = _first_item(profiles)
    admission = _first_item(admissions)

    adapter_passed = admission.get("adapter_contract_passed") is True
    runtime_disabled = admission.get("runtime_admission_allowed") is not True

    candidates_covered = True
    if policy and profile:
        ok, _ = validate_required_candidates_subset_of_supported(policy, profile)
        candidates_covered = ok

    candidate_only_items = policies + profiles + list(bundle.get("health_gates") or ()) + list(
        bundle.get("fallback_policies") or ()
    ) + admissions
    candidate_only_preserved = all(item.get("candidate_only") is True for item in candidate_only_items)

    planning = _planning_decision_snapshot()

    return {
        "adapter_contract_passed_does_not_imply_runtime_enabled": (
            adapter_passed and runtime_disabled
        ),
        "runtime_admission_still_disabled": runtime_disabled,
        "commercial_runtime_candidates_empty": not planning["commercial_runtime_candidates"],
        "field_synthesis_entrypoint_locked": policy.get("field_synthesis_entrypoint")
        == FIELD_SYNTHESIS_ENTRYPOINT,
        "gpl_commercial_blocked": _gpl_commercial_blocked(bundle),
        "observation_runtime_blocked": _observation_runtime_blocked(bundle),
        "health_gate_required": planning["health_gate_required"],
        "fallback_required": planning["fallback_required"],
        "required_candidates_covered_by_profile": candidates_covered,
        "candidate_only_preserved": candidate_only_preserved,
    }


def build_trace_for_case(
    case: FieldSpatialEvidenceProviderAdmissionDryRunCase,
    *,
    actual_ok: bool,
    errors: List[str],
    bundle: Dict[str, Any],
) -> Dict[str, Any]:
    policies = list(bundle.get("admission_policies") or ())
    profiles = list(bundle.get("capability_profiles") or ())
    health_gates = list(bundle.get("health_gates") or ())
    fallbacks = list(bundle.get("fallback_policies") or ())
    admissions = list(bundle.get("runtime_admission_candidates") or ())

    policy = _first_item(policies)
    profile = _first_item(profiles)
    health = _first_item(health_gates)
    fallback = _first_item(fallbacks)
    admission = _first_item(admissions)

    trace_decision = classify_trace_decision(case.expected_validation_ok, actual_ok)
    matched = trace_decision in ("PASS", "EXPECTED_REJECT")
    checkpoints = _governance_checkpoints(bundle)

    return {
        "case_id": case.case_id,
        "case_name": case.case_name,
        "case_type": case.case_type,
        "case_goal": case.case_goal,
        "provider_policy": {
            "provider_ref": policy.get("provider_ref") or case.expected_provider_ref,
            "backend_ref": policy.get("backend_ref"),
            "adapter_ref": policy.get("adapter_ref"),
            "provider_role": policy.get("provider_role"),
            "admission_mode": policy.get("admission_mode") or case.expected_admission_mode,
            "allowed_runtime_scope": policy.get("allowed_runtime_scope"),
            "field_synthesis_entrypoint": policy.get("field_synthesis_entrypoint")
            or FIELD_SYNTHESIS_ENTRYPOINT,
            "runtime_admission_allowed": policy.get("runtime_admission_allowed"),
            "commercial_runtime_allowed": policy.get("commercial_runtime_allowed"),
        },
        "capability_profile": {
            "supported_candidate_types": list(profile.get("supported_candidate_types") or ()),
            "required_input_modes": list(profile.get("required_input_modes") or ()),
            "supported_runtime_modes": list(profile.get("supported_runtime_modes") or ()),
            "health_signal_supported": profile.get("health_signal_supported"),
            "wearable_fit": profile.get("wearable_fit"),
            "offline_fit": profile.get("offline_fit"),
        },
        "health_gate": {
            "required_health_signals": list(health.get("required_health_signals") or ()),
            "degraded_conditions": list(health.get("degraded_conditions") or ()),
            "blocked_conditions": list(health.get("blocked_conditions") or ()),
            "confidence_floor": health.get("confidence_floor"),
            "tracking_lost_policy": health.get("tracking_lost_policy"),
            "degradation_output_policy": health.get("degradation_output_policy"),
        },
        "fallback_policy": {
            "fallback_policy_ref": fallback.get("fallback_policy_ref"),
            "fallback_provider_refs": list(fallback.get("fallback_provider_refs") or ()),
            "fallback_mode": fallback.get("fallback_mode"),
            "preserve_source_chain": fallback.get("preserve_source_chain"),
            "preserve_conflict_refs": fallback.get("preserve_conflict_refs"),
        },
        "runtime_admission": {
            "admission_stage": admission.get("admission_stage"),
            "license_gate_passed": admission.get("license_gate_passed"),
            "adapter_contract_passed": admission.get("adapter_contract_passed"),
            "provider_policy_passed": admission.get("provider_policy_passed"),
            "capability_profile_passed": admission.get("capability_profile_passed"),
            "health_gate_passed": admission.get("health_gate_passed"),
            "fallback_policy_passed": admission.get("fallback_policy_passed"),
            "static_validation_passed": admission.get("static_validation_passed"),
            "runtime_admission_allowed": admission.get("runtime_admission_allowed"),
            "blocked_reasons": list(admission.get("blocked_reasons") or ()),
        },
        "planning_decision": _planning_decision_snapshot(),
        "governance_checkpoints": checkpoints,
        "validation": {
            "expected_validation_ok": case.expected_validation_ok,
            "actual_validation_ok": actual_ok,
            "errors": errors,
            "matched_expectation": matched,
        },
        "trace_decision": trace_decision,
    }


def run_single_dryrun_case(
    case: FieldSpatialEvidenceProviderAdmissionDryRunCase,
) -> Dict[str, Any]:
    bundle = bundle_from_provider_admission_case(case)
    actual_ok, errors = validate_provider_admission_case_bundle(bundle)
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
        and expected_reject == 6
        and unexpected_pass == 0
        and unexpected_fail == 0
        and len(traces) == 13
    )

    planning = _planning_decision_snapshot()
    gpl_blocked = all(
        t["governance_checkpoints"].get("gpl_commercial_blocked") is True
        for t in positive_cases
        if t["provider_policy"].get("backend_ref") in GPL_BACKEND_REFS
    )
    observation_blocked = all(
        t["governance_checkpoints"].get("observation_runtime_blocked") is True
        for t in positive_cases
        if t["provider_policy"].get("provider_ref") in OBSERVATION_ONLY_PROVIDER_REFS
    )
    runtime_empty = all(
        t["governance_checkpoints"].get("runtime_admission_still_disabled") is True
        for t in positive_cases
    )
    commercial_empty = planning["commercial_runtime_candidates"] == []

    return {
        "phase_id": PHASE_ID,
        "step": "Step 3 Provider Admission Dry-run Runner",
        "admission_principle_zh": ADMISSION_PRINCIPLE_ZH,
        "case_count": len(traces),
        "positive_case_count": len(positive_cases),
        "invalid_case_count": len(invalid_cases),
        "positive_pass_count": positive_pass,
        "invalid_expected_reject_count": expected_reject,
        "unexpected_pass_count": unexpected_pass,
        "unexpected_fail_count": unexpected_fail,
        "trace_count": len(traces),
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "runtime_admission_candidates_empty": runtime_empty
        and not planning["runtime_admission_candidates"],
        "commercial_runtime_candidates_empty": commercial_empty,
        "gpl_commercial_blocked": gpl_blocked,
        "observation_runtime_blocked": observation_blocked,
        "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT,
        "health_gate_required": planning["health_gate_required"],
        "fallback_required": planning["fallback_required"],
        "provider_replaceability_required": planning["provider_replaceability_required"],
        "no_real_provider_connected": NON_EXECUTION_FLAGS.get("no_real_provider_runtime") is True,
        "no_real_backend_connected": NON_EXECUTION_FLAGS.get("no_real_slam_backend") is True,
        "no_camera": NON_EXECUTION_FLAGS.get("no_camera_runtime") is True,
        "no_ros": NON_EXECUTION_FLAGS.get("no_ros_runtime") is True,
        "no_runtime_admission": NON_EXECUTION_FLAGS.get("no_runtime_admission") is True,
        "trace_decisions": {t["case_id"]: t["trace_decision"] for t in traces},
        "invalid_case_reviews": {
            "invalid_a_gpl_provider_commercial_runtime": _trace_review(
                traces, "invalid_a_gpl_provider_commercial_runtime", "EXPECTED_REJECT"
            ),
            "invalid_b_observation_provider_runtime_admission": _trace_review(
                traces, "invalid_b_observation_provider_runtime_admission", "EXPECTED_REJECT"
            ),
            "invalid_c_runtime_admission_without_health_gate": _trace_review(
                traces, "invalid_c_runtime_admission_without_health_gate", "EXPECTED_REJECT"
            ),
            "invalid_d_fallback_required_missing_policy": _trace_review(
                traces, "invalid_d_fallback_required_missing_policy", "EXPECTED_REJECT"
            ),
            "invalid_e_field_synthesis_entrypoint_bypass": _trace_review(
                traces, "invalid_e_field_synthesis_entrypoint_bypass", "EXPECTED_REJECT"
            ),
            "invalid_f_required_candidates_not_in_profile": _trace_review(
                traces, "invalid_f_required_candidates_not_in_profile", "EXPECTED_REJECT"
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


def run_field_spatial_evidence_provider_admission_dryrun_v1(
    *,
    output_root: Optional[str] = None,
    write_files: bool = True,
) -> Dict[str, Any]:
    all_cases = build_all_provider_admission_cases_v1()
    traces = [run_single_dryrun_case(case) for case in all_cases]
    summary = summarize_dryrun_traces(traces)

    resolved_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    result: Dict[str, Any] = {
        "summary": summary,
        "traces": traces,
        "output_root": str(resolved_root),
    }

    if write_files:
        resolved_root.mkdir(parents=True, exist_ok=True)
        trace_path = resolved_root / TRACE_FILENAME
        summary_path = resolved_root / SUMMARY_FILENAME

        trace_doc = {
            "phase_id": PHASE_ID,
            "step": "Step 3 Provider Admission Dry-run Runner",
            "admission_principle_zh": ADMISSION_PRINCIPLE_ZH,
            "trace_count": len(traces),
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "traces": traces,
        }
        trace_path.write_text(
            json.dumps(trace_doc, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        summary_path.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        result["output_trace_file"] = str(trace_path)
        result["output_summary_file"] = str(summary_path)

    return result


def main() -> int:
    result = run_field_spatial_evidence_provider_admission_dryrun_v1()
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
