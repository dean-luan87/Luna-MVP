# -*- coding: utf-8 -*-
"""Field Spatial Evidence Provider Admission Planning — dry-run cases v1."""

from __future__ import annotations

import json
import sys
from dataclasses import replace
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_registry_v1 import (
    GPL_BACKEND_REFS,
    OBSERVATION_ONLY_PROVIDER_REFS,
    get_provider_planning_bundle_v1,
)
from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
    _gpl_commercial_blocked,
    _observation_runtime_blocked,
    validate_provider_admission_case_bundle,
)
from capabilities.field_understanding.spatial_evidence_provider_admission.field_spatial_evidence_provider_admission_types_v1 import (
    ADMISSION_PRINCIPLE_EN,
    ADMISSION_PRINCIPLE_ZH,
    FIELD_SYNTHESIS_ENTRYPOINT,
    PHASE_ID,
    ProviderAdmissionPlanningDecision,
    ProviderCapabilityProfile,
    ProviderDisableDecision,
    ProviderFallbackPolicy,
    ProviderHealthGate,
    ProviderRuntimeAdmissionCandidate,
    SpatialEvidenceProviderAdmissionPolicy,
    candidate_to_dict,
)

FINAL_DECISION_DRYRUN_CASES_READY_FOR_RUNNER = (
    "FIELD_SPATIAL_EVIDENCE_PROVIDER_ADMISSION_DRYRUN_CASES_READY_FOR_RUNNER"
)


@dataclass(frozen=True)
class FieldSpatialEvidenceProviderAdmissionDryRunCase:
    case_id: str
    case_name: str
    case_type: str  # positive | invalid
    case_goal: str
    admission_policies: Tuple[SpatialEvidenceProviderAdmissionPolicy, ...]
    capability_profiles: Tuple[ProviderCapabilityProfile, ...]
    health_gates: Tuple[ProviderHealthGate, ...]
    fallback_policies: Tuple[ProviderFallbackPolicy, ...]
    runtime_admission_candidates: Tuple[ProviderRuntimeAdmissionCandidate, ...]
    disable_decisions: Tuple[ProviderDisableDecision, ...]
    planning_decisions: Tuple[ProviderAdmissionPlanningDecision, ...]
    expected_validation_ok: bool
    expected_provider_ref: str
    expected_admission_mode: str
    expected_runtime_allowed: bool
    expected_notes: Tuple[str, ...]


def _bundle_parts(
    provider_ref: str,
) -> Tuple[
    SpatialEvidenceProviderAdmissionPolicy,
    ProviderCapabilityProfile,
    ProviderHealthGate,
    ProviderFallbackPolicy,
    ProviderRuntimeAdmissionCandidate,
]:
    return get_provider_planning_bundle_v1(provider_ref)


def _positive_case(
    *,
    case_id: str,
    case_name: str,
    case_goal: str,
    provider_ref: str,
    expected_admission_mode: str,
    expected_notes: Tuple[str, ...],
) -> FieldSpatialEvidenceProviderAdmissionDryRunCase:
    policy, profile, health, fallback, admission = _bundle_parts(provider_ref)
    return FieldSpatialEvidenceProviderAdmissionDryRunCase(
        case_id=case_id,
        case_name=case_name,
        case_type="positive",
        case_goal=case_goal,
        admission_policies=(policy,),
        capability_profiles=(profile,),
        health_gates=(health,),
        fallback_policies=(fallback,),
        runtime_admission_candidates=(admission,),
        disable_decisions=(),
        planning_decisions=(),
        expected_validation_ok=True,
        expected_provider_ref=provider_ref,
        expected_admission_mode=expected_admission_mode,
        expected_runtime_allowed=False,
        expected_notes=expected_notes,
    )


def _invalid_case(
    *,
    case_id: str,
    case_name: str,
    case_goal: str,
    provider_ref: str,
    expected_admission_mode: str,
    expected_notes: Tuple[str, ...],
    policy: SpatialEvidenceProviderAdmissionPolicy,
    profile: ProviderCapabilityProfile,
    health: ProviderHealthGate,
    fallback: ProviderFallbackPolicy,
    admission: ProviderRuntimeAdmissionCandidate,
) -> FieldSpatialEvidenceProviderAdmissionDryRunCase:
    return FieldSpatialEvidenceProviderAdmissionDryRunCase(
        case_id=case_id,
        case_name=case_name,
        case_type="invalid",
        case_goal=case_goal,
        admission_policies=(policy,),
        capability_profiles=(profile,),
        health_gates=(health,),
        fallback_policies=(fallback,),
        runtime_admission_candidates=(admission,),
        disable_decisions=(),
        planning_decisions=(),
        expected_validation_ok=False,
        expected_provider_ref=provider_ref,
        expected_admission_mode=expected_admission_mode,
        expected_runtime_allowed=False,
        expected_notes=expected_notes,
    )


def build_case_01_openvins_technical_reference() -> FieldSpatialEvidenceProviderAdmissionDryRunCase:
    return _positive_case(
        case_id="case_01_openvins_technical_reference",
        case_name="OpenVINS provider technical reference only",
        case_goal=(
            "Validate OpenVINS as pose/motion technical reference provider; "
            "must not enter runtime admission."
        ),
        provider_ref="provider_openvins",
        expected_admission_mode="technical_reference_only",
        expected_notes=(
            "provider_role=pose_motion_provider.",
            "allowed_runtime_scope=offline_reference.",
            "runtime_admission_allowed=false; commercial_runtime_allowed=false.",
        ),
    )


def build_case_02_vins_fusion_technical_reference() -> FieldSpatialEvidenceProviderAdmissionDryRunCase:
    return _positive_case(
        case_id="case_02_vins_fusion_technical_reference",
        case_name="VINS-Fusion provider technical reference only",
        case_goal=(
            "Validate VINS-Fusion as multi-sensor pose/motion technical reference; "
            "runtime admission remains blocked."
        ),
        provider_ref="provider_vins_fusion",
        expected_admission_mode="technical_reference_only",
        expected_notes=(
            "required_candidate_types include Pose/Motion/SLAMHealth.",
            "runtime_admission_allowed=false.",
        ),
    )


def build_case_03_orb_slam3_local_map_reference() -> FieldSpatialEvidenceProviderAdmissionDryRunCase:
    return _positive_case(
        case_id="case_03_orb_slam3_local_map_reference",
        case_name="ORB-SLAM3 local map / relocalization provider blocked",
        case_goal=(
            "Validate ORB-SLAM3 as LocalMap/Relocalization technical reference; "
            "must not enter runtime admission."
        ),
        provider_ref="provider_orb_slam3",
        expected_admission_mode="technical_reference_only",
        expected_notes=(
            "provider_role=local_map_provider.",
            "required_candidate_types include LocalMap/Relocalization/SLAMHealth.",
            "runtime_admission_allowed=false.",
        ),
    )


def build_case_04_rtab_map_legal_review_blocked() -> FieldSpatialEvidenceProviderAdmissionDryRunCase:
    return _positive_case(
        case_id="case_04_rtab_map_legal_review_blocked",
        case_name="RTAB-Map local map provider legal review blocked",
        case_goal=(
            "Validate RTAB-Map remains technical reference only while license/legal "
            "review is incomplete; runtime blocked."
        ),
        provider_ref="provider_rtab_map",
        expected_admission_mode="technical_reference_only",
        expected_notes=(
            "license_gate_passed=false on admission candidate.",
            "blocked_reasons include license_gate_needs_legal_review.",
            "runtime_admission_allowed=false.",
        ),
    )


def build_case_05_kimera_observation_only() -> FieldSpatialEvidenceProviderAdmissionDryRunCase:
    return _positive_case(
        case_id="case_05_kimera_observation_only",
        case_name="Kimera semantic spatial observation only",
        case_goal=(
            "Validate Kimera as semantic spatial observation provider; "
            "must not enter runtime admission."
        ),
        provider_ref="provider_kimera",
        expected_admission_mode="observation_only",
        expected_notes=(
            "provider_role=semantic_spatial_provider.",
            "allowed_runtime_scope=observation_only.",
            "runtime_admission_allowed=false.",
        ),
    )


def build_case_06_hydra_observation_only() -> FieldSpatialEvidenceProviderAdmissionDryRunCase:
    return _positive_case(
        case_id="case_06_hydra_observation_only",
        case_name="Hydra scene graph observation only",
        case_goal=(
            "Validate Hydra as Field Graph / Scene Graph observation provider; "
            "must not enter runtime admission."
        ),
        provider_ref="provider_hydra",
        expected_admission_mode="observation_only",
        expected_notes=(
            "provider_role=scene_graph_observation_provider.",
            "required_candidate_types include FieldGraph/SemanticMemoryMap.",
            "runtime_admission_allowed=false.",
        ),
    )


def build_case_07_grapheqa_observation_only() -> FieldSpatialEvidenceProviderAdmissionDryRunCase:
    return _positive_case(
        case_id="case_07_grapheqa_observation_only",
        case_name="GraphEQA observation only, not runtime provider",
        case_goal=(
            "Validate GraphEQA as embodied scene graph QA observation only; "
            "must not receive runtime admission."
        ),
        provider_ref="provider_grapheqa",
        expected_admission_mode="observation_only",
        expected_notes=(
            "observation_only provider.",
            "runtime_admission_allowed=false; commercial_runtime_allowed=false.",
        ),
    )


def build_invalid_case_a_gpl_commercial_runtime() -> FieldSpatialEvidenceProviderAdmissionDryRunCase:
    policy, profile, health, fallback, admission = _bundle_parts("provider_openvins")
    policy = replace(
        policy,
        admission_mode="commercial_runtime_candidate",
        allowed_runtime_scope="commercial_runtime",
        commercial_runtime_allowed=True,
        runtime_admission_allowed=True,
    )
    admission = replace(
        admission,
        runtime_admission_allowed=True,
        license_gate_passed=False,
    )
    return _invalid_case(
        case_id="invalid_a_gpl_provider_commercial_runtime",
        case_name="GPL provider commercial runtime",
        case_goal=(
            "Reject GPL OpenVINS provider when commercial_runtime_allowed=true "
            "and runtime admission is requested."
        ),
        provider_ref="provider_openvins",
        expected_admission_mode="commercial_runtime_candidate",
        expected_notes=(
            "gpl_provider_commercial_runtime_not_allowed.",
            "commercial_runtime_requires_license_gate_passed.",
        ),
        policy=policy,
        profile=profile,
        health=health,
        fallback=fallback,
        admission=admission,
    )


def build_invalid_case_b_observation_runtime_admission() -> FieldSpatialEvidenceProviderAdmissionDryRunCase:
    policy, profile, health, fallback, admission = _bundle_parts("provider_grapheqa")
    policy = replace(policy, runtime_admission_allowed=True)
    admission = replace(admission, runtime_admission_allowed=True)
    return _invalid_case(
        case_id="invalid_b_observation_provider_runtime_admission",
        case_name="observation provider runtime admission",
        case_goal=(
            "Reject GraphEQA observation-only provider when runtime_admission_allowed=true."
        ),
        provider_ref="provider_grapheqa",
        expected_admission_mode="observation_only",
        expected_notes=(
            "observation_provider_runtime_admission_not_allowed.",
            "GraphEQA must not receive runtime admission.",
        ),
        policy=policy,
        profile=profile,
        health=health,
        fallback=fallback,
        admission=admission,
    )


def build_invalid_case_c_runtime_without_health_gate() -> FieldSpatialEvidenceProviderAdmissionDryRunCase:
    policy, profile, health, fallback, admission = _bundle_parts("provider_openvins")
    policy = replace(policy, runtime_admission_allowed=True)
    admission = replace(
        admission,
        runtime_admission_allowed=True,
        health_gate_passed=False,
    )
    return _invalid_case(
        case_id="invalid_c_runtime_admission_without_health_gate",
        case_name="runtime admission without health gate",
        case_goal=(
            "Reject provider runtime admission when health_gate_passed=false; "
            "runtime must not bypass health gate."
        ),
        provider_ref="provider_openvins",
        expected_admission_mode="technical_reference_only",
        expected_notes=(
            "runtime_admission_requires_health_gate_passed.",
            "provider runtime must not bypass health gate.",
        ),
        policy=policy,
        profile=profile,
        health=health,
        fallback=fallback,
        admission=admission,
    )


def build_invalid_case_d_missing_fallback_policy() -> FieldSpatialEvidenceProviderAdmissionDryRunCase:
    policy, profile, health, fallback, admission = _bundle_parts("provider_vins_fusion")
    policy = replace(
        policy,
        fallback_policy_ref="",
        runtime_admission_allowed=True,
    )
    admission = replace(
        admission,
        runtime_admission_allowed=True,
        fallback_policy_passed=False,
    )
    return _invalid_case(
        case_id="invalid_d_fallback_required_missing_policy",
        case_name="fallback required but missing fallback policy",
        case_goal=(
            "Reject provider when fallback_policy_ref is empty and fallback gate fails."
        ),
        provider_ref="provider_vins_fusion",
        expected_admission_mode="technical_reference_only",
        expected_notes=(
            "fallback_policy_ref_required.",
            "runtime provider must not miss fallback policy.",
        ),
        policy=policy,
        profile=profile,
        health=health,
        fallback=fallback,
        admission=admission,
    )


def build_invalid_case_e_bad_field_synthesis_entrypoint() -> FieldSpatialEvidenceProviderAdmissionDryRunCase:
    policy, profile, health, fallback, admission = _bundle_parts("provider_orb_slam3")
    policy = replace(policy, field_synthesis_entrypoint="direct_action_v1")
    return _invalid_case(
        case_id="invalid_e_field_synthesis_entrypoint_bypass",
        case_name="field_synthesis entrypoint bypass",
        case_goal=(
            "Reject provider when field_synthesis_entrypoint is not field_synthesis_v1."
        ),
        provider_ref="provider_orb_slam3",
        expected_admission_mode="technical_reference_only",
        expected_notes=(
            "field_synthesis_entrypoint_must_be_field_synthesis_v1.",
            "provider must not bypass field synthesis.",
        ),
        policy=policy,
        profile=profile,
        health=health,
        fallback=fallback,
        admission=admission,
    )


def build_invalid_case_f_required_candidates_not_supported() -> FieldSpatialEvidenceProviderAdmissionDryRunCase:
    policy, profile, health, fallback, admission = _bundle_parts("provider_rtab_map")
    policy = replace(
        policy,
        required_candidate_types=("PoseCandidate", "SLAMHealthCandidate"),
    )
    profile = replace(profile, supported_candidate_types=("PoseCandidate",))
    return _invalid_case(
        case_id="invalid_f_required_candidates_not_in_profile",
        case_name="required candidate types not in capability profile",
        case_goal=(
            "Reject provider when required_candidate_types are not covered by "
            "supported_candidate_types."
        ),
        provider_ref="provider_rtab_map",
        expected_admission_mode="technical_reference_only",
        expected_notes=(
            "required_not_supported:SLAMHealthCandidate.",
            "health_signal_required must support corresponding health candidate.",
        ),
        policy=policy,
        profile=profile,
        health=health,
        fallback=fallback,
        admission=admission,
    )


def build_positive_provider_admission_cases_v1() -> Tuple[FieldSpatialEvidenceProviderAdmissionDryRunCase, ...]:
    return (
        build_case_01_openvins_technical_reference(),
        build_case_02_vins_fusion_technical_reference(),
        build_case_03_orb_slam3_local_map_reference(),
        build_case_04_rtab_map_legal_review_blocked(),
        build_case_05_kimera_observation_only(),
        build_case_06_hydra_observation_only(),
        build_case_07_grapheqa_observation_only(),
    )


def build_invalid_provider_admission_cases_v1() -> Tuple[FieldSpatialEvidenceProviderAdmissionDryRunCase, ...]:
    return (
        build_invalid_case_a_gpl_commercial_runtime(),
        build_invalid_case_b_observation_runtime_admission(),
        build_invalid_case_c_runtime_without_health_gate(),
        build_invalid_case_d_missing_fallback_policy(),
        build_invalid_case_e_bad_field_synthesis_entrypoint(),
        build_invalid_case_f_required_candidates_not_supported(),
    )


def build_all_provider_admission_cases_v1() -> Tuple[FieldSpatialEvidenceProviderAdmissionDryRunCase, ...]:
    return build_positive_provider_admission_cases_v1() + build_invalid_provider_admission_cases_v1()


def bundle_from_provider_admission_case(
    case: FieldSpatialEvidenceProviderAdmissionDryRunCase,
) -> Dict[str, object]:
    """Build validator bundle dict for a dry-run case (shared by runner and cases)."""
    return {
        "case_id": case.case_id,
        "case_type": case.case_type,
        "expected_provider_ref": case.expected_provider_ref,
        "expected_admission_mode": case.expected_admission_mode,
        "expected_runtime_allowed": case.expected_runtime_allowed,
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "admission_policies": [candidate_to_dict(p) for p in case.admission_policies],
        "capability_profiles": [candidate_to_dict(p) for p in case.capability_profiles],
        "health_gates": [candidate_to_dict(h) for h in case.health_gates],
        "fallback_policies": [candidate_to_dict(f) for f in case.fallback_policies],
        "runtime_admission_candidates": [
            candidate_to_dict(a) for a in case.runtime_admission_candidates
        ],
        "disable_decisions": [candidate_to_dict(d) for d in case.disable_decisions],
        "planning_decisions": [candidate_to_dict(d) for d in case.planning_decisions],
    }


def validate_provider_admission_case_ids_unique(
    cases: Tuple[FieldSpatialEvidenceProviderAdmissionDryRunCase, ...] | None = None,
) -> Tuple[bool, Tuple[str, ...]]:
    cases = cases or build_all_provider_admission_cases_v1()
    seen: Dict[str, int] = {}
    duplicates: List[str] = []
    for case in cases:
        seen[case.case_id] = seen.get(case.case_id, 0) + 1
    for case_id, count in seen.items():
        if count > 1:
            duplicates.append(case_id)
    return len(duplicates) == 0, tuple(duplicates)


def _validate_case(case: FieldSpatialEvidenceProviderAdmissionDryRunCase) -> Tuple[bool, List[str]]:
    return validate_provider_admission_case_bundle(bundle_from_provider_admission_case(case))


def _check_cases(
    cases: Tuple[FieldSpatialEvidenceProviderAdmissionDryRunCase, ...],
    *,
    expect_valid: bool,
) -> Tuple[int, List[str]]:
    ok_count = 0
    mismatches: List[str] = []
    for case in cases:
        valid, issues = _validate_case(case)
        if valid == expect_valid:
            ok_count += 1
        else:
            mismatches.append(
                f"{case.case_id}:expected_valid={expect_valid}:actual_valid={valid}:issues={issues}"
            )
    return ok_count, mismatches


def _positive_governance_ok(
    positive: Tuple[FieldSpatialEvidenceProviderAdmissionDryRunCase, ...],
) -> Dict[str, bool]:
    bundles = [bundle_from_provider_admission_case(case) for case in positive]
    gpl_ok = all(_gpl_commercial_blocked(bundle) for bundle in bundles)
    observation_ok = all(_observation_runtime_blocked(bundle) for bundle in bundles)
    runtime_empty = all(
        admission.get("runtime_admission_allowed") is not True
        for bundle in bundles
        for admission in bundle.get("runtime_admission_candidates") or []
    )
    commercial_empty = all(
        policy.get("commercial_runtime_allowed") is not True
        for bundle in bundles
        for policy in bundle.get("admission_policies") or []
        if policy.get("backend_ref") in GPL_BACKEND_REFS
        or policy.get("provider_ref") in OBSERVATION_ONLY_PROVIDER_REFS
    )
    field_synthesis_locked = all(
        policy.get("field_synthesis_entrypoint") == FIELD_SYNTHESIS_ENTRYPOINT
        for bundle in bundles
        for policy in bundle.get("admission_policies") or []
    )
    return {
        "gpl_commercial_blocked": gpl_ok,
        "observation_runtime_blocked": observation_ok,
        "runtime_admission_candidates_empty": runtime_empty,
        "commercial_runtime_candidates_empty": commercial_empty,
        "field_synthesis_entrypoint_locked": field_synthesis_locked,
    }


def summarize_provider_admission_dryrun_cases_v1() -> Dict[str, Any]:
    positive = build_positive_provider_admission_cases_v1()
    invalid = build_invalid_provider_admission_cases_v1()
    all_cases = build_all_provider_admission_cases_v1()

    unique_ok, duplicates = validate_provider_admission_case_ids_unique(all_cases)
    pos_ok, pos_mismatches = _check_cases(positive, expect_valid=True)
    inv_ok, inv_mismatches = _check_cases(invalid, expect_valid=False)

    sample_positive_ok = False
    sample_invalid_rejected = False
    if positive:
        sample_positive_ok, _ = _validate_case(positive[0])
    if invalid:
        invalid_ok, _ = _validate_case(invalid[0])
        sample_invalid_rejected = not invalid_ok

    governance = _positive_governance_ok(positive)

    ready = (
        len(positive) == 7
        and len(invalid) == 6
        and unique_ok
        and pos_ok == len(positive)
        and inv_ok == len(invalid)
        and not pos_mismatches
        and not inv_mismatches
        and sample_positive_ok
        and sample_invalid_rejected
        and governance["gpl_commercial_blocked"]
        and governance["observation_runtime_blocked"]
        and governance["runtime_admission_candidates_empty"]
        and governance["commercial_runtime_candidates_empty"]
        and governance["field_synthesis_entrypoint_locked"]
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 2 Provider Admission Dry-run Cases",
        "admission_principle_en": ADMISSION_PRINCIPLE_EN,
        "admission_principle_zh": ADMISSION_PRINCIPLE_ZH,
        "positive_case_count": len(positive),
        "invalid_case_count": len(invalid),
        "case_count": len(all_cases),
        "positive_case_ids": tuple(c.case_id for c in positive),
        "invalid_case_ids": tuple(c.case_id for c in invalid),
        "case_ids_unique": unique_ok,
        "duplicate_case_ids": duplicates,
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "provider_cases_ok": pos_ok,
        "provider_invalid_cases_ok": inv_ok,
        "provider_case_ids_unique_ok": unique_ok,
        "sample_positive_validate_ok": sample_positive_ok,
        "sample_invalid_rejected_ok": sample_invalid_rejected,
        "positive_validation_mismatches": pos_mismatches,
        "invalid_validation_mismatches": inv_mismatches,
        "runtime_admission_candidates_empty": governance["runtime_admission_candidates_empty"],
        "commercial_runtime_candidates_empty": governance["commercial_runtime_candidates_empty"],
        "gpl_commercial_blocked": governance["gpl_commercial_blocked"],
        "observation_runtime_blocked": governance["observation_runtime_blocked"],
        "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT,
        "health_gate_required": True,
        "fallback_required": True,
        "provider_replaceability_required": True,
        "final_decision": (
            FINAL_DECISION_DRYRUN_CASES_READY_FOR_RUNNER
            if ready
            else "FIELD_SPATIAL_EVIDENCE_PROVIDER_ADMISSION_DRYRUN_CASES_NOT_READY"
        ),
    }


def main() -> int:
    summary = summarize_provider_admission_dryrun_cases_v1()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return (
        0
        if summary["final_decision"] == FINAL_DECISION_DRYRUN_CASES_READY_FOR_RUNNER
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
