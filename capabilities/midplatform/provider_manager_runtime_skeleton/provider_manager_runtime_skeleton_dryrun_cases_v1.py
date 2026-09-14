# -*- coding: utf-8 -*-
"""Provider Manager Runtime Skeleton — dry-run cases v1."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Dict, List, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.provider_manager_runtime_skeleton.provider_manager_runtime_skeleton_registry_v1 import (
    ACTIVATION_GATE_REQUIRED_CHECKS,
    build_provider_manager_runtime_skeleton_matrix_v1,
)
from capabilities.midplatform.provider_manager_runtime_skeleton.provider_manager_runtime_skeleton_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
    _no_domain_specific_manager_duplication,
    validate_provider_manager_runtime_skeleton_case_bundle,
)
from capabilities.midplatform.provider_manager_runtime_skeleton.provider_manager_runtime_skeleton_types_v1 import (
    DOMAIN_SPATIAL_EVIDENCE,
    DOMAIN_VISION_OCR,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_DRYRUN_CASES_READY_FOR_RUNNER,
    MIDPLATFORM_SYNTHESIS_ENTRYPOINT,
    PHASE_ID,
    RUNTIME_SKELETON_PRINCIPLE_ZH,
    RUNTIME_SKELETON_REF,
    SHARED_GOVERNANCE_SOURCE_REF,
    ProviderActivationGate,
    ProviderFallbackExecutorCandidate,
    ProviderManagerRuntimeSkeleton,
    ProviderOutputDispatchCandidate,
    ProviderRuntimeDecision,
    ProviderRuntimeHealthLoop,
    ProviderRuntimeSkeletonPlanningDecision,
    RuntimeProviderRegistry,
    candidate_to_dict,
)


@dataclass(frozen=True)
class ProviderManagerRuntimeSkeletonDryRunCase:
    case_id: str
    case_name: str
    case_type: str
    case_goal: str
    runtime_skeletons: Tuple[ProviderManagerRuntimeSkeleton, ...]
    runtime_registries: Tuple[RuntimeProviderRegistry, ...]
    activation_gates: Tuple[ProviderActivationGate, ...]
    health_loops: Tuple[ProviderRuntimeHealthLoop, ...]
    fallback_executor_candidates: Tuple[ProviderFallbackExecutorCandidate, ...]
    output_dispatch_candidates: Tuple[ProviderOutputDispatchCandidate, ...]
    runtime_decisions: Tuple[ProviderRuntimeDecision, ...]
    planning_decisions: Tuple[ProviderRuntimeSkeletonPlanningDecision, ...]
    expected_validation_ok: bool
    expected_domain_id: str
    expected_runtime_execution_allowed: bool
    expected_notes: Tuple[str, ...]


def _matrix() -> Dict[str, Any]:
    return build_provider_manager_runtime_skeleton_matrix_v1()


def _domain_profiles() -> Dict[str, Any]:
    return dict(_matrix().get("domain_profiles") or {})


def _skeleton() -> ProviderManagerRuntimeSkeleton:
    return ProviderManagerRuntimeSkeleton(**_matrix()["runtime_skeleton"])


def _spatial_registry() -> RuntimeProviderRegistry:
    return RuntimeProviderRegistry(**_matrix()["runtime_registries"][0])


def _vision_registry() -> RuntimeProviderRegistry:
    return RuntimeProviderRegistry(**_matrix()["runtime_registries"][1])


def _spatial_gate() -> ProviderActivationGate:
    return ProviderActivationGate(**_matrix()["activation_gates"][0])


def _vision_gate() -> ProviderActivationGate:
    return ProviderActivationGate(**_matrix()["activation_gates"][1])


def _spatial_health_loop() -> ProviderRuntimeHealthLoop:
    return ProviderRuntimeHealthLoop(**_matrix()["health_loops"][0])


def _spatial_fallback() -> ProviderFallbackExecutorCandidate:
    return ProviderFallbackExecutorCandidate(**_matrix()["fallback_executor_candidates"][0])


def _spatial_dispatch() -> ProviderOutputDispatchCandidate:
    return ProviderOutputDispatchCandidate(**_matrix()["output_dispatch_candidates"][0])


def _vision_dispatch() -> ProviderOutputDispatchCandidate:
    return ProviderOutputDispatchCandidate(**_matrix()["output_dispatch_candidates"][1])


def _spatial_runtime_decision() -> ProviderRuntimeDecision:
    return ProviderRuntimeDecision(**_matrix()["runtime_decisions"][0])


def _planning_decision() -> ProviderRuntimeSkeletonPlanningDecision:
    return ProviderRuntimeSkeletonPlanningDecision(**_matrix()["planning_decision"])


def _case(
    *,
    case_id: str,
    case_name: str,
    case_type: str,
    case_goal: str,
    expected_domain_id: str,
    expected_notes: Tuple[str, ...],
    runtime_skeletons: Tuple[ProviderManagerRuntimeSkeleton, ...] = (),
    runtime_registries: Tuple[RuntimeProviderRegistry, ...] = (),
    activation_gates: Tuple[ProviderActivationGate, ...] = (),
    health_loops: Tuple[ProviderRuntimeHealthLoop, ...] = (),
    fallback_executor_candidates: Tuple[ProviderFallbackExecutorCandidate, ...] = (),
    output_dispatch_candidates: Tuple[ProviderOutputDispatchCandidate, ...] = (),
    runtime_decisions: Tuple[ProviderRuntimeDecision, ...] = (),
    planning_decisions: Tuple[ProviderRuntimeSkeletonPlanningDecision, ...] = (),
    expected_validation_ok: bool | None = None,
    expected_runtime_execution_allowed: bool = False,
) -> ProviderManagerRuntimeSkeletonDryRunCase:
    if expected_validation_ok is None:
        expected_validation_ok = case_type == "positive"
    return ProviderManagerRuntimeSkeletonDryRunCase(
        case_id=case_id,
        case_name=case_name,
        case_type=case_type,
        case_goal=case_goal,
        runtime_skeletons=runtime_skeletons,
        runtime_registries=runtime_registries,
        activation_gates=activation_gates,
        health_loops=health_loops,
        fallback_executor_candidates=fallback_executor_candidates,
        output_dispatch_candidates=output_dispatch_candidates,
        runtime_decisions=runtime_decisions,
        planning_decisions=planning_decisions,
        expected_validation_ok=expected_validation_ok,
        expected_domain_id=expected_domain_id,
        expected_runtime_execution_allowed=expected_runtime_execution_allowed,
        expected_notes=expected_notes,
    )


def build_case_pos_01_spatial_registry_disabled() -> ProviderManagerRuntimeSkeletonDryRunCase:
    registry = replace(_spatial_registry(), registration_status="disabled")
    return _case(
        case_id="case_pos_01_spatial_registry_disabled",
        case_name="Spatial Evidence provider registered but disabled",
        case_type="positive",
        case_goal="Validate spatial_evidence provider can register in runtime registry while remaining disabled.",
        expected_domain_id=DOMAIN_SPATIAL_EVIDENCE,
        expected_notes=(
            "registration_status=disabled.",
            "provider_activation_allowed=false.",
            "runtime_execution_allowed=false.",
        ),
        runtime_registries=(registry,),
    )


def build_case_pos_02_vision_ocr_registry_disabled() -> ProviderManagerRuntimeSkeletonDryRunCase:
    registry = replace(_vision_registry(), registration_status="disabled")
    return _case(
        case_id="case_pos_02_vision_ocr_registry_disabled",
        case_name="Vision/OCR provider registered but disabled",
        case_type="positive",
        case_goal="Validate vision_ocr provider can register in runtime registry while remaining disabled.",
        expected_domain_id=DOMAIN_VISION_OCR,
        expected_notes=(
            "registration_status=disabled.",
            "provider_activation_allowed=false.",
            "real_provider_connected=false.",
        ),
        runtime_registries=(registry,),
    )


def build_case_pos_03_activation_gate_planning_only() -> ProviderManagerRuntimeSkeletonDryRunCase:
    gate = replace(
        _spatial_gate(),
        gates_passed=("license_gate", "adapter_contract_gate"),
        all_gates_passed=False,
        provider_activation_allowed=False,
        activation_decision_candidate="activation_blocked_pending_gates",
    )
    return _case(
        case_id="case_pos_03_activation_gate_planning_only",
        case_name="ActivationGate planning only",
        case_type="positive",
        case_goal="Validate activation gates remain planning candidates and never allow activation.",
        expected_domain_id=DOMAIN_SPATIAL_EVIDENCE,
        expected_notes=(
            "required_gates includes license/adapter/admission/health/fallback/owner_approval.",
            "provider_activation_allowed=false.",
            "all_gates_passed=false.",
        ),
        activation_gates=(gate,),
    )


def build_case_pos_04_health_loop_decision_candidate() -> ProviderManagerRuntimeSkeletonDryRunCase:
    loop = replace(
        _spatial_health_loop(),
        health_decision_candidate="disable_provider_candidate",
        runtime_disable_executed=False,
        direct_runtime_disable_allowed=False,
    )
    return _case(
        case_id="case_pos_04_health_loop_decision_candidate",
        case_name="HealthLoop emits decision candidate only",
        case_type="positive",
        case_goal="Validate health loop generates decision candidate without directly disabling runtime.",
        expected_domain_id=DOMAIN_SPATIAL_EVIDENCE,
        expected_notes=(
            "health_decision_candidate=disable_provider_candidate.",
            "runtime_disable_executed=false.",
            "direct_runtime_disable_allowed=false.",
        ),
        health_loops=(loop,),
    )


def build_case_pos_05_fallback_executor_candidate_only() -> ProviderManagerRuntimeSkeletonDryRunCase:
    fallback = replace(
        _spatial_fallback(),
        fallback_executed=False,
        fallback_execution_allowed=False,
        preserve_source_chain=True,
    )
    return _case(
        case_id="case_pos_05_fallback_executor_candidate_only",
        case_name="FallbackExecutorCandidate only",
        case_type="positive",
        case_goal="Validate fallback executor remains candidate-only and does not execute fallback.",
        expected_domain_id=DOMAIN_SPATIAL_EVIDENCE,
        expected_notes=(
            "fallback_execution_allowed=false.",
            "fallback_executed=false.",
            "preserve_source_chain=true.",
        ),
        fallback_executor_candidates=(fallback,),
    )


def build_case_pos_06_output_dispatch_candidate_only() -> ProviderManagerRuntimeSkeletonDryRunCase:
    dispatch = _spatial_dispatch()
    return _case(
        case_id="case_pos_06_output_dispatch_candidate_only",
        case_name="OutputDispatchCandidate only",
        case_type="positive",
        case_goal="Validate output dispatch allows candidate output only without direct action/speech/fact.",
        expected_domain_id=DOMAIN_SPATIAL_EVIDENCE,
        expected_notes=(
            "output_dispatch_allowed=false.",
            "direct_action_allowed=false.",
            "direct_speech_allowed=false.",
            "direct_fact_write_allowed=false.",
        ),
        output_dispatch_candidates=(dispatch,),
    )


def build_case_pos_07_spatial_field_synthesis_dispatch() -> ProviderManagerRuntimeSkeletonDryRunCase:
    dispatch = replace(
        _spatial_dispatch(),
        synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        output_candidate_types=("PoseCandidate", "LocalMapCandidate", "SLAMHealthCandidate"),
    )
    return _case(
        case_id="case_pos_07_spatial_field_synthesis_dispatch",
        case_name="Spatial output dispatch to field_synthesis_v1",
        case_type="positive",
        case_goal="Validate spatial_evidence output dispatch routes to field_synthesis_v1 only.",
        expected_domain_id=DOMAIN_SPATIAL_EVIDENCE,
        expected_notes=(
            "synthesis_entrypoint=field_synthesis_v1.",
            "spatial candidate types preserved.",
        ),
        output_dispatch_candidates=(dispatch,),
    )


def build_case_pos_08_vision_ocr_abstraction_dispatch() -> ProviderManagerRuntimeSkeletonDryRunCase:
    dispatch = replace(
        _vision_dispatch(),
        synthesis_entrypoint=MIDPLATFORM_SYNTHESIS_ENTRYPOINT,
        output_candidate_types=("DetectionCandidate", "ocr_result_candidate"),
    )
    return _case(
        case_id="case_pos_08_vision_ocr_abstraction_dispatch",
        case_name="Vision/OCR abstraction-compatible dispatch",
        case_type="positive",
        case_goal=(
            "Validate vision_ocr output dispatch uses midplatform_synthesis_v1 and "
            "provider_abstraction_standard_v1 compatible candidates."
        ),
        expected_domain_id=DOMAIN_VISION_OCR,
        expected_notes=(
            "synthesis_entrypoint=midplatform_synthesis_v1.",
            "no PoseCandidate required.",
            "no SLAMHealthCandidate required.",
        ),
        output_dispatch_candidates=(dispatch,),
    )


def build_case_pos_09_runtime_decision_composite() -> ProviderManagerRuntimeSkeletonDryRunCase:
    gate = _spatial_gate()
    loop = _spatial_health_loop()
    fallback = _spatial_fallback()
    dispatch = _spatial_dispatch()
    decision = replace(
        _spatial_runtime_decision(),
        decision_type="composite_runtime_candidate",
        decision_status="candidate_only",
        runtime_execution_allowed=False,
        provider_activation_allowed=False,
        fallback_execution_allowed=False,
        output_dispatch_allowed=False,
        decision_candidate_ref=gate.gate_ref,
    )
    return _case(
        case_id="case_pos_09_runtime_decision_composite",
        case_name="ProviderRuntimeDecision composite candidate",
        case_type="positive",
        case_goal=(
            "Validate ProviderRuntimeDecision aggregates activation/health/fallback/output "
            "candidates while execution remains false."
        ),
        expected_domain_id=DOMAIN_SPATIAL_EVIDENCE,
        expected_notes=(
            "runtime_execution_allowed=false.",
            "provider_activation_allowed=false.",
            "fallback_execution_allowed=false.",
            "output_dispatch_allowed=false.",
        ),
        activation_gates=(gate,),
        health_loops=(loop,),
        fallback_executor_candidates=(fallback,),
        output_dispatch_candidates=(dispatch,),
        runtime_decisions=(decision,),
        planning_decisions=(_planning_decision(),),
    )


def build_invalid_case_a_runtime_execution_allowed() -> ProviderManagerRuntimeSkeletonDryRunCase:
    skeleton = replace(_skeleton(), runtime_execution_allowed=True)
    return _case(
        case_id="invalid_a_runtime_execution_allowed",
        case_name="runtime_execution_allowed=true",
        case_type="invalid",
        case_goal="Reject skeleton when runtime_execution_allowed=true in planning.",
        expected_domain_id=DOMAIN_SPATIAL_EVIDENCE,
        expected_notes=("runtime_execution_allowed_must_be_false.",),
        runtime_skeletons=(skeleton,),
        expected_validation_ok=False,
    )


def build_invalid_case_b_provider_activation_allowed() -> ProviderManagerRuntimeSkeletonDryRunCase:
    gate = replace(_spatial_gate(), provider_activation_allowed=True)
    return _case(
        case_id="invalid_b_provider_activation_allowed",
        case_name="provider_activation_allowed=true",
        case_type="invalid",
        case_goal="Reject activation gate when provider_activation_allowed=true.",
        expected_domain_id=DOMAIN_SPATIAL_EVIDENCE,
        expected_notes=("provider_activation_allowed_must_be_false.",),
        activation_gates=(gate,),
        expected_validation_ok=False,
    )


def build_invalid_case_c_fallback_execution_allowed() -> ProviderManagerRuntimeSkeletonDryRunCase:
    fallback = replace(_spatial_fallback(), fallback_execution_allowed=True)
    return _case(
        case_id="invalid_c_fallback_execution_allowed",
        case_name="fallback_execution_allowed=true",
        case_type="invalid",
        case_goal="Reject fallback executor when fallback_execution_allowed=true.",
        expected_domain_id=DOMAIN_SPATIAL_EVIDENCE,
        expected_notes=("fallback_execution_allowed_must_be_false.",),
        fallback_executor_candidates=(fallback,),
        expected_validation_ok=False,
    )


def build_invalid_case_d_output_dispatch_allowed() -> ProviderManagerRuntimeSkeletonDryRunCase:
    dispatch = replace(_spatial_dispatch(), output_dispatch_allowed=True)
    return _case(
        case_id="invalid_d_output_dispatch_allowed",
        case_name="output_dispatch_allowed=true",
        case_type="invalid",
        case_goal="Reject output dispatch when output_dispatch_allowed=true.",
        expected_domain_id=DOMAIN_SPATIAL_EVIDENCE,
        expected_notes=("output_dispatch_allowed_must_be_false.",),
        output_dispatch_candidates=(dispatch,),
        expected_validation_ok=False,
    )


def build_invalid_case_e_real_provider_connected() -> ProviderManagerRuntimeSkeletonDryRunCase:
    skeleton = replace(_skeleton(), real_provider_connected=True)
    registry = replace(_spatial_registry(), real_provider_connected=True)
    return _case(
        case_id="invalid_e_real_provider_connected",
        case_name="real_provider_connected=true",
        case_type="invalid",
        case_goal="Reject planning artifacts when real_provider_connected=true.",
        expected_domain_id=DOMAIN_SPATIAL_EVIDENCE,
        expected_notes=("real_provider_connected_must_be_false.",),
        runtime_skeletons=(skeleton,),
        runtime_registries=(registry,),
        expected_validation_ok=False,
    )


def build_invalid_case_f_health_loop_direct_disable() -> ProviderManagerRuntimeSkeletonDryRunCase:
    loop = replace(
        _spatial_health_loop(),
        runtime_disable_executed=True,
        direct_runtime_disable_allowed=True,
        health_decision_candidate="block_runtime_candidate",
    )
    return _case(
        case_id="invalid_f_health_loop_direct_disable",
        case_name="health loop directly disables runtime",
        case_type="invalid",
        case_goal="Reject health loop that directly disables runtime instead of emitting candidate.",
        expected_domain_id=DOMAIN_SPATIAL_EVIDENCE,
        expected_notes=(
            "health_loop_runtime_disable_executed_not_allowed.",
            "health_loop_direct_runtime_disable_not_allowed.",
        ),
        health_loops=(loop,),
        expected_validation_ok=False,
    )


def build_invalid_case_g_direct_output_paths() -> ProviderManagerRuntimeSkeletonDryRunCase:
    dispatch = replace(
        _spatial_dispatch(),
        direct_action_allowed=True,
    )
    return _case(
        case_id="invalid_g_direct_output_paths",
        case_name="output dispatch direct action path",
        case_type="invalid",
        case_goal="Reject output dispatch that allows direct action/speech/fact write paths.",
        expected_domain_id=DOMAIN_SPATIAL_EVIDENCE,
        expected_notes=("direct_action_allowed_must_be_false.",),
        output_dispatch_candidates=(dispatch,),
        expected_validation_ok=False,
    )


def build_invalid_case_h_vision_ocr_spatial_pollution() -> ProviderManagerRuntimeSkeletonDryRunCase:
    registry = replace(
        _vision_registry(),
        supported_output_candidate_types=(
            "DetectionCandidate",
            "PoseCandidate",
            "SLAMHealthCandidate",
        ),
    )
    dispatch = replace(
        _vision_dispatch(),
        output_candidate_types=("PoseCandidate", "SLAMHealthCandidate"),
    )
    return _case(
        case_id="invalid_h_vision_ocr_spatial_pollution",
        case_name="Vision/OCR polluted by Spatial candidates",
        case_type="invalid",
        case_goal=(
            "Reject vision_ocr registry/dispatch that wrongly requires PoseCandidate / "
            "SLAMHealthCandidate not declared by domain profile."
        ),
        expected_domain_id=DOMAIN_VISION_OCR,
        expected_notes=(
            "candidate_not_in_domain_profile:PoseCandidate.",
            "candidate_not_in_domain_profile:SLAMHealthCandidate.",
        ),
        runtime_registries=(registry,),
        output_dispatch_candidates=(dispatch,),
        expected_validation_ok=False,
    )


def build_positive_provider_manager_runtime_skeleton_cases_v1() -> Tuple[
    ProviderManagerRuntimeSkeletonDryRunCase, ...
]:
    return (
        build_case_pos_01_spatial_registry_disabled(),
        build_case_pos_02_vision_ocr_registry_disabled(),
        build_case_pos_03_activation_gate_planning_only(),
        build_case_pos_04_health_loop_decision_candidate(),
        build_case_pos_05_fallback_executor_candidate_only(),
        build_case_pos_06_output_dispatch_candidate_only(),
        build_case_pos_07_spatial_field_synthesis_dispatch(),
        build_case_pos_08_vision_ocr_abstraction_dispatch(),
        build_case_pos_09_runtime_decision_composite(),
    )


def build_invalid_provider_manager_runtime_skeleton_cases_v1() -> Tuple[
    ProviderManagerRuntimeSkeletonDryRunCase, ...
]:
    return (
        build_invalid_case_a_runtime_execution_allowed(),
        build_invalid_case_b_provider_activation_allowed(),
        build_invalid_case_c_fallback_execution_allowed(),
        build_invalid_case_d_output_dispatch_allowed(),
        build_invalid_case_e_real_provider_connected(),
        build_invalid_case_f_health_loop_direct_disable(),
        build_invalid_case_g_direct_output_paths(),
        build_invalid_case_h_vision_ocr_spatial_pollution(),
    )


def build_all_provider_manager_runtime_skeleton_cases_v1() -> Tuple[
    ProviderManagerRuntimeSkeletonDryRunCase, ...
]:
    return (
        build_positive_provider_manager_runtime_skeleton_cases_v1()
        + build_invalid_provider_manager_runtime_skeleton_cases_v1()
    )


def bundle_from_provider_manager_runtime_skeleton_case(
    case: ProviderManagerRuntimeSkeletonDryRunCase,
) -> Dict[str, object]:
    return {
        "case_id": case.case_id,
        "case_type": case.case_type,
        "expected_domain_id": case.expected_domain_id,
        "expected_runtime_execution_allowed": case.expected_runtime_execution_allowed,
        "domain_profiles": _domain_profiles(),
        "runtime_skeletons": [candidate_to_dict(s) for s in case.runtime_skeletons],
        "runtime_registries": [candidate_to_dict(r) for r in case.runtime_registries],
        "activation_gates": [candidate_to_dict(g) for g in case.activation_gates],
        "health_loops": [candidate_to_dict(h) for h in case.health_loops],
        "fallback_executor_candidates": [
            candidate_to_dict(f) for f in case.fallback_executor_candidates
        ],
        "output_dispatch_candidates": [
            candidate_to_dict(d) for d in case.output_dispatch_candidates
        ],
        "runtime_decisions": [candidate_to_dict(d) for d in case.runtime_decisions],
        "planning_decisions": [candidate_to_dict(d) for d in case.planning_decisions],
    }


def validate_provider_manager_runtime_skeleton_case_ids_unique(
    cases: Tuple[ProviderManagerRuntimeSkeletonDryRunCase, ...] | None = None,
) -> Tuple[bool, Tuple[str, ...]]:
    cases = cases or build_all_provider_manager_runtime_skeleton_cases_v1()
    seen: Dict[str, int] = {}
    duplicates: List[str] = []
    for case in cases:
        seen[case.case_id] = seen.get(case.case_id, 0) + 1
    for case_id, count in seen.items():
        if count > 1:
            duplicates.append(case_id)
    return len(duplicates) == 0, tuple(duplicates)


def _validate_case(case: ProviderManagerRuntimeSkeletonDryRunCase) -> Tuple[bool, List[str]]:
    return validate_provider_manager_runtime_skeleton_case_bundle(
        bundle_from_provider_manager_runtime_skeleton_case(case)
    )


def _check_cases(
    cases: Tuple[ProviderManagerRuntimeSkeletonDryRunCase, ...],
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


def summarize_provider_manager_runtime_skeleton_dryrun_cases_v1() -> Dict[str, Any]:
    positive = build_positive_provider_manager_runtime_skeleton_cases_v1()
    invalid = build_invalid_provider_manager_runtime_skeleton_cases_v1()
    all_cases = build_all_provider_manager_runtime_skeleton_cases_v1()

    unique_ok, duplicates = validate_provider_manager_runtime_skeleton_case_ids_unique(all_cases)
    pos_ok, pos_mismatches = _check_cases(positive, expect_valid=True)
    inv_ok, inv_mismatches = _check_cases(invalid, expect_valid=False)

    sample_positive_ok = False
    sample_invalid_rejected = False
    if positive:
        sample_positive_ok, _ = _validate_case(positive[0])
    if invalid:
        invalid_ok, _ = _validate_case(invalid[0])
        sample_invalid_rejected = not invalid_ok

    no_dup = _no_domain_specific_manager_duplication()
    spatial_boundary = any(
        c.case_id == "case_pos_07_spatial_field_synthesis_dispatch" for c in positive
    )
    vision_boundary = any(
        c.case_id == "case_pos_08_vision_ocr_abstraction_dispatch" for c in positive
    )

    ready = (
        len(positive) == 9
        and len(invalid) == 8
        and len(all_cases) == 17
        and unique_ok
        and pos_ok == len(positive)
        and inv_ok == len(invalid)
        and not pos_mismatches
        and not inv_mismatches
        and sample_positive_ok
        and sample_invalid_rejected
        and no_dup
        and spatial_boundary
        and vision_boundary
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 2 Provider Manager Runtime Skeleton Dry-run Cases",
        "runtime_skeleton_principle_zh": RUNTIME_SKELETON_PRINCIPLE_ZH,
        "positive_case_count": len(positive),
        "invalid_case_count": len(invalid),
        "case_count": len(all_cases),
        "positive_case_ids": tuple(c.case_id for c in positive),
        "invalid_case_ids": tuple(c.case_id for c in invalid),
        "case_ids_unique": unique_ok,
        "duplicate_case_ids": list(duplicates),
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "runtime_skeleton_cases_ok": pos_ok,
        "runtime_skeleton_invalid_cases_ok": inv_ok,
        "runtime_skeleton_case_ids_unique_ok": unique_ok,
        "sample_positive_validate_ok": sample_positive_ok,
        "sample_invalid_rejected_ok": sample_invalid_rejected,
        "positive_validation_mismatches": pos_mismatches,
        "invalid_validation_mismatches": inv_mismatches,
        "runtime_execution_allowed": False,
        "provider_activation_allowed": False,
        "fallback_execution_allowed": False,
        "output_dispatch_allowed": False,
        "real_provider_connected": False,
        "candidate_only_enforced": True,
        "spatial_evidence_boundary_preserved": spatial_boundary,
        "vision_ocr_boundary_preserved": vision_boundary,
        "no_domain_specific_manager_duplication": no_dup,
        "activation_gate_required_checks": list(ACTIVATION_GATE_REQUIRED_CHECKS),
        "shared_governance_source_ref": SHARED_GOVERNANCE_SOURCE_REF,
        "runtime_skeleton_ref": RUNTIME_SKELETON_REF,
        "final_decision": (
            FINAL_DECISION_DRYRUN_CASES_READY_FOR_RUNNER
            if ready
            else "PROVIDER_MANAGER_RUNTIME_SKELETON_DRYRUN_CASES_NOT_READY"
        ),
    }


def main() -> int:
    summary = summarize_provider_manager_runtime_skeleton_dryrun_cases_v1()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["final_decision"] == FINAL_DECISION_DRYRUN_CASES_READY_FOR_RUNNER else 1


if __name__ == "__main__":
    raise SystemExit(main())
