# -*- coding: utf-8 -*-
"""Field SLAM Adapter Contract Planning — dry-run cases v1."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Dict, List, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_adapter_contract.field_slam_adapter_contract_registry_v1 import (
    GPL_LICENSE_TYPES,
    OBSERVATION_BACKEND_REFS,
    TECHNICAL_REFERENCE_BACKEND_REFS,
    build_backend_admission_candidates_v1,
    build_generic_slam_adapter_contracts_v1,
    build_license_gate_policies_v1,
    build_runtime_isolation_policies_v1,
    build_slam_backend_output_mappings_v1,
    build_spatial_evidence_provider_registrations_v1,
)
from capabilities.field_understanding.slam_adapter_contract.field_slam_adapter_contract_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
    _candidate_only_enforced,
    _gpl_runtime_blocked,
    _observation_runtime_blocked,
    validate_adapter_contract_case_bundle,
)
from capabilities.field_understanding.slam_adapter_contract.field_slam_adapter_contract_types_v1 import (
    ADAPTER_CONTRACT_PRINCIPLE_EN,
    ADAPTER_CONTRACT_PRINCIPLE_ZH,
    FIELD_SYNTHESIS_ENTRYPOINT,
    GENERIC_SLAM_ADAPTER_CONTRACT_ID,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    BackendAdmissionCandidate,
    GenericSLAMAdapterContract,
    LicenseGatePolicy,
    RuntimeIsolationPolicy,
    SLAMBackendOutputMapping,
    SpatialEvidenceProviderRegistration,
    candidate_to_dict,
)

FINAL_DECISION_DRYRUN_CASES_READY_FOR_RUNNER = (
    "FIELD_SLAM_ADAPTER_CONTRACT_DRYRUN_CASES_READY_FOR_RUNNER"
)


@dataclass(frozen=True)
class FieldSLAMAdapterContractDryRunCase:
    case_id: str
    case_name: str
    case_type: str
    case_goal: str
    adapter_contracts: Tuple[GenericSLAMAdapterContract, ...]
    output_mappings: Tuple[SLAMBackendOutputMapping, ...]
    license_gate_policies: Tuple[LicenseGatePolicy, ...]
    runtime_isolation_policies: Tuple[RuntimeIsolationPolicy, ...]
    backend_admission_candidates: Tuple[BackendAdmissionCandidate, ...]
    provider_registrations: Tuple[SpatialEvidenceProviderRegistration, ...]
    expected_validation_ok: bool
    expected_backend_ref: str
    expected_admission_stage: str
    expected_runtime_allowed: bool
    expected_notes: Tuple[str, ...]


def _first_for_backend(
    items: Tuple[Any, ...],
    backend_ref: str,
    *,
    attr: str = "backend_ref",
) -> Tuple[Any, ...]:
    return tuple(item for item in items if getattr(item, attr) == backend_ref)


def _catalog_for_backend(backend_ref: str) -> Dict[str, Tuple[Any, ...]]:
    return {
        "adapter_contracts": _first_for_backend(
            build_generic_slam_adapter_contracts_v1(), backend_ref
        ),
        "output_mappings": _first_for_backend(
            build_slam_backend_output_mappings_v1(), backend_ref
        ),
        "license_gate_policies": _first_for_backend(
            build_license_gate_policies_v1(), backend_ref
        ),
        "runtime_isolation_policies": _first_for_backend(
            build_runtime_isolation_policies_v1(), backend_ref
        ),
        "backend_admission_candidates": _first_for_backend(
            build_backend_admission_candidates_v1(), backend_ref
        ),
        "provider_registrations": _first_for_backend(
            build_spatial_evidence_provider_registrations_v1(), backend_ref
        ),
    }


def _positive_case(
    *,
    case_id: str,
    case_name: str,
    case_goal: str,
    backend_ref: str,
    expected_admission_stage: str,
    expected_notes: Tuple[str, ...],
) -> FieldSLAMAdapterContractDryRunCase:
    catalog = _catalog_for_backend(backend_ref)
    return FieldSLAMAdapterContractDryRunCase(
        case_id=case_id,
        case_name=case_name,
        case_type="positive",
        case_goal=case_goal,
        adapter_contracts=catalog["adapter_contracts"],  # type: ignore[assignment]
        output_mappings=catalog["output_mappings"],  # type: ignore[assignment]
        license_gate_policies=catalog["license_gate_policies"],  # type: ignore[assignment]
        runtime_isolation_policies=catalog["runtime_isolation_policies"],  # type: ignore[assignment]
        backend_admission_candidates=catalog["backend_admission_candidates"],  # type: ignore[assignment]
        provider_registrations=catalog["provider_registrations"],  # type: ignore[assignment]
        expected_validation_ok=True,
        expected_backend_ref=backend_ref,
        expected_admission_stage=expected_admission_stage,
        expected_runtime_allowed=False,
        expected_notes=expected_notes,
    )


def build_case_openvins_technical_reference() -> FieldSLAMAdapterContractDryRunCase:
    return _positive_case(
        case_id="case_01_openvins_technical_reference",
        case_name="OpenVINS technical reference adapter",
        case_goal=(
            "Validate OpenVINS enters adapter planning as GPL technical reference only; "
            "outputs map to Pose/Motion/Health candidates via field_synthesis_v1."
        ),
        backend_ref="openvins",
        expected_admission_stage="technical_reference",
        expected_notes=(
            "GPL backend; commercial_runtime_allowed=false.",
            "isolation_mode=offline_reference_only.",
            "runtime_admission_allowed=false.",
        ),
    )


def build_case_vins_fusion_multi_sensor_reference() -> FieldSLAMAdapterContractDryRunCase:
    return _positive_case(
        case_id="case_02_vins_fusion_multi_sensor_reference",
        case_name="VINS-Fusion multi-sensor technical reference",
        case_goal=(
            "Validate VINS-Fusion as multi-sensor VIO technical reference with "
            "RelocalizationCandidate support; GPL runtime gate blocks commercial runtime."
        ),
        backend_ref="vins_fusion",
        expected_admission_stage="technical_reference",
        expected_notes=(
            "license_risk=high; commercial_runtime_allowed=false.",
            "supported outputs include RelocalizationCandidate.",
        ),
    )


def build_case_orb_slam3_local_map_reference() -> FieldSLAMAdapterContractDryRunCase:
    return _positive_case(
        case_id="case_03_orb_slam3_local_map_reference",
        case_name="ORB-SLAM3 local map / relocalization reference",
        case_goal=(
            "Validate ORB-SLAM3 as P1 reference for LocalMap/Relocalization; "
            "must not confirm destination or enter commercial runtime."
        ),
        backend_ref="orb_slam3",
        expected_admission_stage="technical_reference",
        expected_notes=(
            "LocalMap + Relocalization mapping only through adapter.",
            "No destination confirmation; runtime_admission_allowed=false.",
        ),
    )


def build_case_rtab_map_conditional_license() -> FieldSLAMAdapterContractDryRunCase:
    return _positive_case(
        case_id="case_04_rtab_map_conditional_license",
        case_name="RTAB-Map conditional license technical reference",
        case_goal=(
            "Validate RTAB-Map as RGB-D/graph local map reference with "
            "needs_legal_review license posture; no commercial runtime."
        ),
        backend_ref="rtab_map",
        expected_admission_stage="technical_reference",
        expected_notes=(
            "license_review_status=needs_legal_review.",
            "commercial_runtime_allowed=false; runtime_admission_allowed=false.",
        ),
    )


def build_case_kimera_observation_semantic() -> FieldSLAMAdapterContractDryRunCase:
    return _positive_case(
        case_id="case_05_kimera_observation_semantic",
        case_name="Kimera observation semantic spatial adapter",
        case_goal=(
            "Validate Kimera as metric-semantic observation backend; "
            "semantic_spatial_provider with always_disabled policy."
        ),
        backend_ref="kimera",
        expected_admission_stage="adapter_planning",
        expected_notes=(
            "provider_role=semantic_spatial_provider.",
            "disable_policy=always_disabled; runtime_admission_allowed=false.",
        ),
    )


def build_case_hydra_scene_graph_observation() -> FieldSLAMAdapterContractDryRunCase:
    return _positive_case(
        case_id="case_06_hydra_scene_graph_observation",
        case_name="Hydra scene graph observation adapter",
        case_goal=(
            "Validate Hydra as Field Graph / 3D Scene Graph observation line; "
            "must not enter runtime admission."
        ),
        backend_ref="hydra",
        expected_admission_stage="adapter_planning",
        expected_notes=(
            "FieldGraphCandidate + SemanticMemoryMapCandidate observation only.",
            "scene_graph_observation_provider; runtime_admission_allowed=false.",
        ),
    )


def build_case_grapheqa_observation_only() -> FieldSLAMAdapterContractDryRunCase:
    return _positive_case(
        case_id="case_07_grapheqa_observation_only",
        case_name="GraphEQA observation-only adapter",
        case_goal=(
            "Validate GraphEQA is observation-only; must not act as runtime SLAM backend."
        ),
        backend_ref="grapheqa",
        expected_admission_stage="technical_reference",
        expected_notes=(
            "scene_graph_observation_provider.",
            "runtime_admission_allowed=false; commercial_runtime_allowed=false.",
        ),
    )


def build_invalid_case_gpl_commercial_runtime() -> FieldSLAMAdapterContractDryRunCase:
    catalog = _catalog_for_backend("openvins")
    adapter = catalog["adapter_contracts"][0]
    license_gate = replace(
        catalog["license_gate_policies"][0],
        commercial_runtime_allowed=True,
    )
    admission = replace(
        catalog["backend_admission_candidates"][0],
        admission_stage="commercial_runtime_candidate",
        license_gate_passed=True,
        runtime_admission_allowed=True,
        blocked_reasons=(),
    )
    return FieldSLAMAdapterContractDryRunCase(
        case_id="invalid_a_gpl_commercial_runtime",
        case_name="GPL backend enters commercial runtime",
        case_type="invalid",
        case_goal=(
            "Reject GPL backend with commercial_runtime_allowed=true and "
            "runtime_admission_allowed=true."
        ),
        adapter_contracts=(adapter,),
        output_mappings=catalog["output_mappings"],  # type: ignore[assignment]
        license_gate_policies=(license_gate,),
        runtime_isolation_policies=catalog["runtime_isolation_policies"],  # type: ignore[assignment]
        backend_admission_candidates=(admission,),
        provider_registrations=catalog["provider_registrations"],  # type: ignore[assignment]
        expected_validation_ok=False,
        expected_backend_ref="openvins",
        expected_admission_stage="commercial_runtime_candidate",
        expected_runtime_allowed=True,
        expected_notes=(
            "GPL backend must not commercial_runtime_allowed=true.",
            "commercial_runtime_candidate requires license_gate_passed with GPL block.",
        ),
    )


def build_invalid_case_backend_bypass_adapter() -> FieldSLAMAdapterContractDryRunCase:
    catalog = _catalog_for_backend("openvins")
    adapter = replace(
        catalog["adapter_contracts"][0],
        adapter_ref="",
        field_synthesis_entrypoint="",
        license_gate_ref="",
        runtime_isolation_ref="",
    )
    return FieldSLAMAdapterContractDryRunCase(
        case_id="invalid_b_backend_bypass_adapter",
        case_name="Backend bypasses adapter contract",
        case_type="invalid",
        case_goal=(
            "Reject backend attempting to bypass adapter and field_synthesis entrypoint."
        ),
        adapter_contracts=(adapter,),
        output_mappings=catalog["output_mappings"],  # type: ignore[assignment]
        license_gate_policies=(),  # type: ignore[assignment]
        runtime_isolation_policies=(),  # type: ignore[assignment]
        backend_admission_candidates=catalog["backend_admission_candidates"],  # type: ignore[assignment]
        provider_registrations=catalog["provider_registrations"],  # type: ignore[assignment]
        expected_validation_ok=False,
        expected_backend_ref="openvins",
        expected_admission_stage="technical_reference",
        expected_runtime_allowed=False,
        expected_notes=(
            "backend_bypass_adapter is forbidden.",
            "field_synthesis_entrypoint must exist.",
        ),
    )


def build_invalid_case_output_mapping_not_candidate_only() -> FieldSLAMAdapterContractDryRunCase:
    catalog = _catalog_for_backend("openvins")
    bad_mappings = tuple(
        replace(
            mapping,
            candidate_only_enforced=False,
            source_refs_required=False,
        )
        for mapping in catalog["output_mappings"]
    )
    return FieldSLAMAdapterContractDryRunCase(
        case_id="invalid_c_output_mapping_not_candidate_only",
        case_name="Output mapping without candidate_only enforcement",
        case_type="invalid",
        case_goal=(
            "Reject output mapping when candidate_only_enforced=false or "
            "source_refs_required=false."
        ),
        adapter_contracts=catalog["adapter_contracts"],  # type: ignore[assignment]
        output_mappings=bad_mappings,
        license_gate_policies=catalog["license_gate_policies"],  # type: ignore[assignment]
        runtime_isolation_policies=catalog["runtime_isolation_policies"],  # type: ignore[assignment]
        backend_admission_candidates=catalog["backend_admission_candidates"],  # type: ignore[assignment]
        provider_registrations=catalog["provider_registrations"],  # type: ignore[assignment]
        expected_validation_ok=False,
        expected_backend_ref="openvins",
        expected_admission_stage="technical_reference",
        expected_runtime_allowed=False,
        expected_notes=(
            "OutputMapping must candidate_only_enforced=true.",
            "OutputMapping must source_refs_required=true.",
        ),
    )


def build_invalid_case_observation_runtime_admission() -> FieldSLAMAdapterContractDryRunCase:
    catalog = _catalog_for_backend("grapheqa")
    admission = replace(
        catalog["backend_admission_candidates"][0],
        admission_stage="commercial_runtime_candidate",
        license_gate_passed=True,
        runtime_admission_allowed=True,
        blocked_reasons=(),
    )
    return FieldSLAMAdapterContractDryRunCase(
        case_id="invalid_d_observation_runtime_admission",
        case_name="Observation backend runtime_admission=true",
        case_type="invalid",
        case_goal=(
            "Reject GraphEQA observation backend with runtime_admission_allowed=true."
        ),
        adapter_contracts=catalog["adapter_contracts"],  # type: ignore[assignment]
        output_mappings=catalog["output_mappings"],  # type: ignore[assignment]
        license_gate_policies=catalog["license_gate_policies"],  # type: ignore[assignment]
        runtime_isolation_policies=catalog["runtime_isolation_policies"],  # type: ignore[assignment]
        backend_admission_candidates=(admission,),
        provider_registrations=catalog["provider_registrations"],  # type: ignore[assignment]
        expected_validation_ok=False,
        expected_backend_ref="grapheqa",
        expected_admission_stage="commercial_runtime_candidate",
        expected_runtime_allowed=True,
        expected_notes=(
            "observation backend must not runtime_admission_allowed=true.",
            "GraphEQA must remain observation-only.",
        ),
    )


def build_invalid_case_health_signal_without_slam_health() -> FieldSLAMAdapterContractDryRunCase:
    catalog = _catalog_for_backend("openvins")
    provider = replace(
        catalog["provider_registrations"][0],
        health_signal_required=True,
        supported_candidate_types=("PoseCandidate", "MotionCandidate"),
    )
    return FieldSLAMAdapterContractDryRunCase(
        case_id="invalid_e_health_signal_without_slam_health",
        case_name="health_signal_required without SLAMHealthCandidate",
        case_type="invalid",
        case_goal=(
            "Reject provider when health_signal_required=true but "
            "SLAMHealthCandidate is not in supported_candidate_types."
        ),
        adapter_contracts=catalog["adapter_contracts"],  # type: ignore[assignment]
        output_mappings=catalog["output_mappings"],  # type: ignore[assignment]
        license_gate_policies=catalog["license_gate_policies"],  # type: ignore[assignment]
        runtime_isolation_policies=catalog["runtime_isolation_policies"],  # type: ignore[assignment]
        backend_admission_candidates=catalog["backend_admission_candidates"],  # type: ignore[assignment]
        provider_registrations=(provider,),
        expected_validation_ok=False,
        expected_backend_ref="openvins",
        expected_admission_stage="technical_reference",
        expected_runtime_allowed=False,
        expected_notes=(
            "health_signal_required=true requires SLAMHealthCandidate support.",
        ),
    )


def build_positive_adapter_contract_cases_v1() -> Tuple[FieldSLAMAdapterContractDryRunCase, ...]:
    return (
        build_case_openvins_technical_reference(),
        build_case_vins_fusion_multi_sensor_reference(),
        build_case_orb_slam3_local_map_reference(),
        build_case_rtab_map_conditional_license(),
        build_case_kimera_observation_semantic(),
        build_case_hydra_scene_graph_observation(),
        build_case_grapheqa_observation_only(),
    )


def build_invalid_adapter_contract_cases_v1() -> Tuple[FieldSLAMAdapterContractDryRunCase, ...]:
    return (
        build_invalid_case_gpl_commercial_runtime(),
        build_invalid_case_backend_bypass_adapter(),
        build_invalid_case_output_mapping_not_candidate_only(),
        build_invalid_case_observation_runtime_admission(),
        build_invalid_case_health_signal_without_slam_health(),
    )


def build_all_adapter_contract_cases_v1() -> Tuple[FieldSLAMAdapterContractDryRunCase, ...]:
    return build_positive_adapter_contract_cases_v1() + build_invalid_adapter_contract_cases_v1()


def bundle_from_adapter_contract_case(
    case: FieldSLAMAdapterContractDryRunCase,
) -> Dict[str, object]:
    """Build validator bundle dict for a dry-run case (shared by runner and cases)."""
    return {
        "case_id": case.case_id,
        "case_type": case.case_type,
        "expected_backend_ref": case.expected_backend_ref,
        "expected_admission_stage": case.expected_admission_stage,
        "expected_runtime_allowed": case.expected_runtime_allowed,
        "generic_adapter_contract_id": GENERIC_SLAM_ADAPTER_CONTRACT_ID,
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "adapter_contracts": [candidate_to_dict(a) for a in case.adapter_contracts],
        "output_mappings": [candidate_to_dict(m) for m in case.output_mappings],
        "license_gates": [candidate_to_dict(l) for l in case.license_gate_policies],
        "runtime_isolations": [candidate_to_dict(i) for i in case.runtime_isolation_policies],
        "backend_admissions": [candidate_to_dict(a) for a in case.backend_admission_candidates],
        "provider_registrations": [candidate_to_dict(p) for p in case.provider_registrations],
    }


def validate_adapter_contract_case_ids_unique(
    cases: Tuple[FieldSLAMAdapterContractDryRunCase, ...] | None = None,
) -> Tuple[bool, Tuple[str, ...]]:
    cases = cases or build_all_adapter_contract_cases_v1()
    seen: Dict[str, int] = {}
    duplicates: List[str] = []
    for case in cases:
        seen[case.case_id] = seen.get(case.case_id, 0) + 1
    for case_id, count in seen.items():
        if count > 1:
            duplicates.append(case_id)
    return len(duplicates) == 0, tuple(duplicates)


def _validate_case(case: FieldSLAMAdapterContractDryRunCase) -> Tuple[bool, List[str]]:
    return validate_adapter_contract_case_bundle(bundle_from_adapter_contract_case(case))


def _check_cases(
    cases: Tuple[FieldSLAMAdapterContractDryRunCase, ...],
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


def _positive_governance_ok(positive: Tuple[FieldSLAMAdapterContractDryRunCase, ...]) -> Dict[str, bool]:
    bundles = [bundle_from_adapter_contract_case(case) for case in positive]
    gpl_ok = all(
        gate.get("commercial_runtime_allowed") is not True
        for bundle in bundles
        for gate in bundle.get("license_gates") or []
        if gate.get("license_type") in GPL_LICENSE_TYPES
    )
    gpl_ok = gpl_ok and all(
        admission.get("runtime_admission_allowed") is not True
        for bundle in bundles
        for admission in bundle.get("backend_admissions") or []
        if admission.get("backend_ref") in {"openvins", "vins_fusion", "orb_slam3"}
    )
    observation_ok = all(
        admission.get("runtime_admission_allowed") is not True
        for bundle in bundles
        for admission in bundle.get("backend_admissions") or []
        if admission.get("backend_ref") in OBSERVATION_BACKEND_REFS
    )
    candidate_ok = all(_candidate_only_enforced(bundle) for bundle in bundles)
    return {
        "gpl_runtime_blocked": gpl_ok,
        "observation_runtime_blocked": observation_ok,
        "candidate_only_enforced": candidate_ok,
    }


def summarize_adapter_contract_dryrun_cases_v1() -> Dict[str, Any]:
    positive = build_positive_adapter_contract_cases_v1()
    invalid = build_invalid_adapter_contract_cases_v1()
    all_cases = build_all_adapter_contract_cases_v1()

    unique_ok, duplicates = validate_adapter_contract_case_ids_unique(all_cases)
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
        and len(invalid) == 5
        and unique_ok
        and pos_ok == len(positive)
        and inv_ok == len(invalid)
        and not pos_mismatches
        and not inv_mismatches
        and governance["gpl_runtime_blocked"]
        and governance["observation_runtime_blocked"]
        and governance["candidate_only_enforced"]
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 2 Adapter Contract Dry-run Cases",
        "adapter_contract_principle_en": ADAPTER_CONTRACT_PRINCIPLE_EN,
        "adapter_contract_principle_zh": ADAPTER_CONTRACT_PRINCIPLE_ZH,
        "positive_case_count": len(positive),
        "invalid_case_count": len(invalid),
        "case_count": len(all_cases),
        "positive_case_ids": tuple(c.case_id for c in positive),
        "invalid_case_ids": tuple(c.case_id for c in invalid),
        "case_ids_unique": unique_ok,
        "duplicate_case_ids": duplicates,
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "commercial_runtime_backends": [],
        "technical_reference_backends": list(TECHNICAL_REFERENCE_BACKEND_REFS),
        "observation_backends": list(sorted(OBSERVATION_BACKEND_REFS)),
        "adapter_cases_ok": pos_ok,
        "adapter_invalid_cases_ok": inv_ok,
        "adapter_case_ids_unique_ok": unique_ok,
        "sample_positive_validate_ok": sample_positive_ok,
        "sample_invalid_rejected_ok": sample_invalid_rejected,
        "positive_validation_mismatches": pos_mismatches,
        "invalid_validation_mismatches": inv_mismatches,
        "gpl_runtime_blocked": governance["gpl_runtime_blocked"],
        "observation_runtime_blocked": governance["observation_runtime_blocked"],
        "candidate_only_enforced": governance["candidate_only_enforced"],
        "license_gate_required": True,
        "runtime_isolation_required": True,
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "final_decision": (
            FINAL_DECISION_DRYRUN_CASES_READY_FOR_RUNNER
            if ready
            else "FIELD_SLAM_ADAPTER_CONTRACT_DRYRUN_CASES_NOT_READY"
        ),
    }


def main() -> int:
    summary = summarize_adapter_contract_dryrun_cases_v1()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["final_decision"] == FINAL_DECISION_DRYRUN_CASES_READY_FOR_RUNNER else 1


if __name__ == "__main__":
    raise SystemExit(main())
