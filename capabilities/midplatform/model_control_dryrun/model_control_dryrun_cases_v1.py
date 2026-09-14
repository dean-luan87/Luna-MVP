# -*- coding: utf-8 -*-
"""Midplatform Model Control DryRun — cases v1.

Reads file-based model-control policy bundles, admits each bundle, produces the
midplatform model-control objects (enable / disable / fallback / degraded mode /
license boundary / priority routing / output blocking / availability state control /
reserved-only execution block / candidate output gate / full control bundle), and
runs 11 positive and 12 negative cases. Everything is candidate-only; no model
execution, no inference, no fact admission, no action/speech/navigation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.model_control_dryrun.model_control_dryrun_types_v1 import (
    POLICY_TO_OBJECTS,
    PROHIBITED_REQUEST_FLAGS,
    REJECT_IF_MISSING_FIELDS,
    MidplatformCaseResult,
)

_SAMPLES_DIR = Path(__file__).resolve().parent / "samples"

# positive case_id -> sample file
POSITIVE_SAMPLE_FILES: Dict[str, str] = {
    "model_enable_policy_control": "sample_model_enable_policy_bundle.json",
    "model_disable_policy_control": "sample_model_disable_policy_bundle.json",
    "model_fallback_policy_control": "sample_model_fallback_policy_bundle.json",
    "model_degraded_mode_policy_control": "sample_model_degraded_mode_policy_bundle.json",
    "model_license_boundary_control": "sample_model_license_boundary_policy_bundle.json",
    "model_priority_routing_policy_control": "sample_model_priority_routing_policy_bundle.json",
    "model_output_blocking_policy_control": "sample_model_output_blocking_policy_bundle.json",
    "model_availability_state_control": "sample_model_availability_state_control_bundle.json",
    "reserved_family_execution_block_control": "sample_reserved_family_execution_block_bundle.json",
    "candidate_output_gate_control": "sample_candidate_output_gate_bundle.json",
    "full_midplatform_model_control_bundle": "sample_full_midplatform_model_control_bundle.json",
}

# positive case_id -> control policy id whose objects it produces
CASE_PRODUCED_POLICY: Dict[str, str] = {
    "model_enable_policy_control": "model_enable",
    "model_disable_policy_control": "model_disable",
    "model_fallback_policy_control": "model_fallback",
    "model_degraded_mode_policy_control": "model_degraded_mode",
    "model_license_boundary_control": "model_license_boundary",
    "model_priority_routing_policy_control": "model_priority_routing",
    "model_output_blocking_policy_control": "model_output_blocking",
    "model_availability_state_control": "model_availability_state_control",
    "reserved_family_execution_block_control": "reserved_family_execution_block",
    "candidate_output_gate_control": "candidate_output_gate",
    "full_midplatform_model_control_bundle": "full_model_control_bundle",
}

# negative case_id -> sample file (10 file-based; 2 are in-memory tampered).
INVALID_SAMPLE_FILES: Dict[str, str] = {
    "invalid_disabled_model_output_allowed": "invalid_disabled_model_output_allowed.json",
    "invalid_unlicensed_model_enabled": "invalid_unlicensed_model_enabled.json",
    "invalid_agpl_model_marked_commercial_runtime_ready": "invalid_agpl_model_marked_commercial_runtime_ready.json",
    "invalid_unavailable_model_triggered_download": "invalid_unavailable_model_triggered_download.json",
    "invalid_reserved_family_executed": "invalid_reserved_family_executed.json",
    "invalid_degraded_model_triggers_action": "invalid_degraded_model_triggers_action.json",
    "invalid_blocked_output_enters_field_task_guidance": "invalid_blocked_output_enters_field_task_guidance.json",
    "invalid_priority_routing_bypasses_candidate_gate": "invalid_priority_routing_bypasses_candidate_gate.json",
    "invalid_model_control_triggers_inference": "invalid_model_control_triggers_inference.json",
    "invalid_vla_action_chain_injected": "invalid_vla_action_chain_injected.json",
}

ALL_SAMPLE_FILES: Tuple[str, ...] = (
    tuple(POSITIVE_SAMPLE_FILES.values()) + tuple(INVALID_SAMPLE_FILES.values())
)


def read_local_sample(filename: str) -> Dict[str, Any]:
    return json.loads((_SAMPLES_DIR / filename).read_text(encoding="utf-8"))


def _missing_required_fields(bundle: Dict[str, Any]) -> List[str]:
    missing: List[str] = []
    for f in REJECT_IF_MISSING_FIELDS:
        v = bundle.get(f)
        if (
            v is None
            or (isinstance(v, str) and not v.strip())
            or (isinstance(v, (list, tuple)) and len(v) == 0)
        ):
            missing.append(f)
    return missing


def _prohibited_flags_present(bundle: Dict[str, Any]) -> List[str]:
    return [flag for flag in PROHIBITED_REQUEST_FLAGS if bundle.get(flag) is True]


def admit_control_bundle(bundle: Dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons: List[str] = []
    for m in _missing_required_fields(bundle):
        reasons.append(f"missing_required_field:{m}")
    for p in _prohibited_flags_present(bundle):
        reasons.append(f"prohibited_request:{p}")
    return (len(reasons) == 0), reasons


def produce_objects_for_case(case_id: str) -> List[str]:
    policy_id = CASE_PRODUCED_POLICY.get(case_id, "")
    return list(POLICY_TO_OBJECTS.get(policy_id, ()))


def _run_positive_case(case_id: str) -> MidplatformCaseResult:
    bundle = read_local_sample(POSITIVE_SAMPLE_FILES[case_id])
    accepted, reasons = admit_control_bundle(bundle)
    produced: List[str] = []
    if accepted:
        produced = produce_objects_for_case(case_id)
    expected = produce_objects_for_case(case_id)
    ok = accepted and produced == expected and len(produced) > 0
    return MidplatformCaseResult(
        case_id=case_id,
        case_kind="positive",
        accepted=accepted,
        expected_result="accepted",
        passed=ok,
        policy_id=str(bundle.get("policy_id", "")),
        generated_objects=tuple(produced),
        reject_reasons=tuple(reasons),
        notes=("candidate_only", "no_model_execution", "no_inference", "no_runtime_trigger"),
    )


def _run_negative_file_case(case_id: str, filename: str) -> MidplatformCaseResult:
    bundle = read_local_sample(filename)
    accepted, reasons = admit_control_bundle(bundle)
    return MidplatformCaseResult(
        case_id=case_id,
        case_kind="negative",
        accepted=accepted,
        expected_result="rejected",
        passed=accepted is False,
        policy_id=str(bundle.get("policy_id", "")),
        reject_reasons=tuple(reasons),
    )


def _run_negative_tampered_case(
    case_id: str, base_file: str, injected_flags: Tuple[str, ...]
) -> MidplatformCaseResult:
    bundle = dict(read_local_sample(base_file))
    for flag in injected_flags:
        bundle[flag] = True
    accepted, reasons = admit_control_bundle(bundle)
    return MidplatformCaseResult(
        case_id=case_id,
        case_kind="negative",
        accepted=accepted,
        expected_result="rejected",
        passed=accepted is False,
        policy_id=str(bundle.get("policy_id", "")),
        reject_reasons=tuple(reasons),
        notes=("in_memory_tampered_bundle", f"injected={','.join(injected_flags)}"),
    )


def run_positive_cases() -> Tuple[List[MidplatformCaseResult], List[str]]:
    results: List[MidplatformCaseResult] = [
        _run_positive_case(case_id) for case_id in POSITIVE_SAMPLE_FILES
    ]
    produced: List[str] = []
    for r in results:
        if r.passed:
            produced.extend(r.generated_objects)
    return results, sorted(set(produced))


def run_negative_cases() -> List[MidplatformCaseResult]:
    results: List[MidplatformCaseResult] = [
        _run_negative_file_case(case_id, INVALID_SAMPLE_FILES[case_id])
        for case_id in INVALID_SAMPLE_FILES
    ]
    # Invalid K: model tuning / dataset usage approved (tampered).
    results.append(
        _run_negative_tampered_case(
            "invalid_model_tuning_dataset_usage",
            POSITIVE_SAMPLE_FILES["model_enable_policy_control"],
            ("model_tuning_requested", "dataset_usage_requested", "training_requested"),
        )
    )
    # Invalid L: candidate gate pass treated as fact admission (tampered).
    results.append(
        _run_negative_tampered_case(
            "invalid_gate_pass_treated_as_fact_admission",
            POSITIVE_SAMPLE_FILES["candidate_output_gate_control"],
            ("gate_pass_treated_as_fact_admission", "fact_admission_requested"),
        )
    )
    return results
