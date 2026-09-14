# -*- coding: utf-8 -*-
"""Midplatform Model Data Handling DryRun — cases v1.

Reads file-based multi-model candidate handling bundles, admits each bundle,
produces the midplatform data-handling objects (ingress / normalization / source-
chain aggregation / confidence aggregation / conflict / uncertainty / unavailable-
reserved-degraded / evidence bundle / candidate lifecycle / Field-Task-Guidance
support), and runs 10 positive and 12 negative cases. Everything is candidate-only;
no real inference, no fact admission, no action/speech/navigation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.model_data_handling_dryrun.model_data_handling_dryrun_types_v1 import (
    ALL_PRODUCED_OBJECTS,
    POLICY_BOUNDARY,
    POLICY_TO_OBJECTS,
    PROHIBITED_REQUEST_FLAGS,
    REJECT_IF_MISSING_FIELDS,
    MidplatformCaseResult,
)

_SAMPLES_DIR = Path(__file__).resolve().parent / "samples"

# positive case_id -> (sample file, policy_ids covered)
POSITIVE_SAMPLE_FILES: Dict[str, str] = {
    "multi_model_candidate_ingress_handling": "sample_multi_model_candidate_ingress_bundle.json",
    "candidate_normalization_handling": "sample_candidate_normalization_bundle.json",
    "source_chain_aggregation_handling": "sample_source_chain_aggregation_bundle.json",
    "confidence_policy_aggregation_handling": "sample_confidence_policy_aggregation_bundle.json",
    "conflict_uncertainty_handling": "sample_conflict_uncertainty_handling_bundle.json",
    "unavailable_reserved_degraded_handling": "sample_unavailable_reserved_degraded_bundle.json",
    "evidence_bundle_composition_handling": "sample_evidence_bundle_composition.json",
    "candidate_lifecycle_handling": "sample_candidate_lifecycle_bundle.json",
    "field_task_guidance_support_bundle_handling": "sample_field_task_guidance_support_bundle.json",
    "full_midplatform_model_data_handling_bundle": "sample_full_midplatform_model_data_handling_bundle.json",
}

# Which policy objects each positive case is expected to produce.
CASE_PRODUCED_POLICIES: Dict[str, Tuple[str, ...]] = {
    "multi_model_candidate_ingress_handling": ("candidate_ingress",),
    "candidate_normalization_handling": ("candidate_normalization",),
    "source_chain_aggregation_handling": ("source_chain_aggregation",),
    "confidence_policy_aggregation_handling": ("confidence_policy_aggregation",),
    "conflict_uncertainty_handling": ("conflict_handling", "uncertainty_handling"),
    "unavailable_reserved_degraded_handling": ("unavailable_reserved_degraded_handling",),
    "evidence_bundle_composition_handling": ("evidence_bundle_composition",),
    "candidate_lifecycle_handling": ("candidate_lifecycle",),
    "field_task_guidance_support_bundle_handling": ("field_task_guidance_support_bundle",),
    # the full bundle aggregates every policy's produced objects
    "full_midplatform_model_data_handling_bundle": (
        "candidate_ingress",
        "candidate_normalization",
        "source_chain_aggregation",
        "confidence_policy_aggregation",
        "conflict_handling",
        "uncertainty_handling",
        "unavailable_reserved_degraded_handling",
        "evidence_bundle_composition",
        "candidate_lifecycle",
        "field_task_guidance_support_bundle",
    ),
}

# negative case_id -> sample file (10 file-based; 2 are in-memory tampered).
INVALID_SAMPLE_FILES: Dict[str, str] = {
    "invalid_missing_source_chain": "invalid_missing_source_chain_bundle.json",
    "invalid_missing_candidate_refs": "invalid_missing_candidate_refs_bundle.json",
    "invalid_missing_confidence_policy_ref": "invalid_missing_confidence_policy_bundle.json",
    "invalid_untrusted_candidate_fact_admission": "invalid_untrusted_candidate_fact_admission.json",
    "invalid_conflict_resolved_as_fact": "invalid_conflict_resolved_as_fact.json",
    "invalid_unavailable_model_treated_as_blocker": "invalid_unavailable_model_treated_as_blocker.json",
    "invalid_reserved_family_executed": "invalid_reserved_family_executed.json",
    "invalid_direct_field_task_guidance_bypass": "invalid_direct_field_task_guidance_bypass.json",
    "invalid_action_speech_navigation_trigger": "invalid_action_speech_navigation_trigger.json",
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
    present: List[str] = []
    for flag in PROHIBITED_REQUEST_FLAGS:
        if bundle.get(flag) is True:
            present.append(flag)
    return present


def admit_handling_bundle(bundle: Dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons: List[str] = []
    for m in _missing_required_fields(bundle):
        reasons.append(f"missing_required_field:{m}")
    for p in _prohibited_flags_present(bundle):
        reasons.append(f"prohibited_request:{p}")
    return (len(reasons) == 0), reasons


def produce_objects_for_case(case_id: str) -> List[str]:
    produced: List[str] = []
    for policy_id in CASE_PRODUCED_POLICIES.get(case_id, ()):
        produced.extend(POLICY_TO_OBJECTS.get(policy_id, ()))
    return produced


def _run_positive_case(case_id: str) -> MidplatformCaseResult:
    bundle = read_local_sample(POSITIVE_SAMPLE_FILES[case_id])
    accepted, reasons = admit_handling_bundle(bundle)
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
        notes=("candidate_only", "no_fact_admission", "no_real_inference"),
    )


def _run_negative_file_case(case_id: str, filename: str) -> MidplatformCaseResult:
    bundle = read_local_sample(filename)
    accepted, reasons = admit_handling_bundle(bundle)
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
    accepted, reasons = admit_handling_bundle(bundle)
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
    # Invalid K: model tuning / dataset usage requested (tampered).
    results.append(
        _run_negative_tampered_case(
            "invalid_model_tuning_dataset_usage",
            POSITIVE_SAMPLE_FILES["candidate_normalization_handling"],
            ("model_tuning_requested", "dataset_usage_requested", "training_requested"),
        )
    )
    # Invalid L: blocked / expired candidate revived without governance (tampered).
    results.append(
        _run_negative_tampered_case(
            "invalid_blocked_expired_candidate_revival",
            POSITIVE_SAMPLE_FILES["candidate_lifecycle_handling"],
            ("blocked_expired_candidate_revived_without_governance",),
        )
    )
    return results
