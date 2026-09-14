# -*- coding: utf-8 -*-
"""Shared Provider Runtime Governance Skeleton — dry-run cases v1."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Dict, List, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.provider_runtime_governance.domain_profiles.spatial_evidence_provider_governance_profile_v1 import (
    build_spatial_evidence_domain_governance_catalog_v1,
    build_spatial_evidence_governance_manager_v1,
    build_spatial_evidence_provider_governance_profile_v1,
)
from capabilities.midplatform.provider_runtime_governance.domain_profiles.vision_ocr_governance_compatibility_v1 import (
    build_vision_ocr_combined_governance_profile_v1,
    verify_vision_ocr_compatibility_v1,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_registry_v1 import (
    REQUIRED_CHECKS,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
    _no_domain_specific_manager_duplication,
    validate_provider_runtime_governance_case_bundle,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_types_v1 import (
    DOMAIN_SHARED,
    DOMAIN_SPATIAL_EVIDENCE,
    DOMAIN_VISION_OCR,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_DRYRUN_CASES_READY_FOR_RUNNER,
    GOVERNANCE_PRINCIPLE_ZH,
    MIDPLATFORM_SYNTHESIS_ENTRYPOINT,
    PHASE_ID,
    SHARED_MANAGER_REF,
    ProviderDisableRequest,
    ProviderDomainGovernanceProfile,
    ProviderEnableRequest,
    ProviderFallbackRoute,
    ProviderHealthSnapshot,
    ProviderManagerDecision,
    ProviderRegistryEntry,
    ProviderRuntimeAdmissionCheck,
    ProviderRuntimeGovernanceManager,
    ProviderRuntimeState,
    candidate_to_dict,
)

@dataclass(frozen=True)
class SharedProviderRuntimeGovernanceDryRunCase:
    case_id: str
    case_name: str
    case_type: str
    case_goal: str
    managers: Tuple[ProviderRuntimeGovernanceManager, ...]
    registry_entries: Tuple[ProviderRegistryEntry, ...]
    enable_requests: Tuple[ProviderEnableRequest, ...]
    disable_requests: Tuple[ProviderDisableRequest, ...]
    runtime_states: Tuple[ProviderRuntimeState, ...]
    health_snapshots: Tuple[ProviderHealthSnapshot, ...]
    fallback_routes: Tuple[ProviderFallbackRoute, ...]
    runtime_admission_checks: Tuple[ProviderRuntimeAdmissionCheck, ...]
    manager_decisions: Tuple[ProviderManagerDecision, ...]
    domain_profiles: Tuple[ProviderDomainGovernanceProfile, ...]
    expected_validation_ok: bool
    expected_domain_id: str
    expected_runtime_enabled: bool
    expected_notes: Tuple[str, ...]


def _shared_domain_profile() -> ProviderDomainGovernanceProfile:
    return ProviderDomainGovernanceProfile(
        profile_ref="shared_governance_profile_v1",
        domain_id=DOMAIN_SHARED,
        domain_name="Shared Governance",
        admission_layer_ref="provider_runtime_governance_registry_v1",
        synthesis_entrypoint=MIDPLATFORM_SYNTHESIS_ENTRYPOINT,
        provider_refs=("shared_mock_provider",),
        supported_output_candidate_types=("GenericCandidate",),
        domain_risk_tags=("shared_skeleton_only",),
        uses_shared_manager_skeleton=True,
    )


def _shared_manager() -> ProviderRuntimeGovernanceManager:
    return ProviderRuntimeGovernanceManager(
        manager_ref=f"{SHARED_MANAGER_REF}_{DOMAIN_SHARED}",
        domain_id=DOMAIN_SHARED,
        manager_status="planning",
        managed_provider_refs=("shared_mock_provider",),
        default_enabled_provider_refs=(),
        default_disabled_provider_refs=("shared_mock_provider",),
        synthesis_entrypoint=MIDPLATFORM_SYNTHESIS_ENTRYPOINT,
        runtime_activation_allowed=False,
        provider_runtime_enabled=False,
    )


def _shared_registry_entry() -> ProviderRegistryEntry:
    return ProviderRegistryEntry(
        registry_entry_ref="registry_entry_shared_mock",
        domain_id=DOMAIN_SHARED,
        provider_ref="shared_mock_provider",
        backend_ref="mock",
        adapter_ref="mock_adapter",
        provider_role="mock_provider",
        registration_status="registered_candidate",
        admission_policy_ref="admission_policy_shared_mock",
        health_gate_ref="health_gate_shared_mock",
        fallback_policy_ref="fallback_shared_mock",
        enabled_by_default=False,
        runtime_enable_allowed=False,
        supported_output_candidate_types=("GenericCandidate",),
    )


def _shared_runtime_state() -> ProviderRuntimeState:
    return ProviderRuntimeState(
        runtime_state_ref="runtime_state_shared_mock",
        domain_id=DOMAIN_SHARED,
        provider_ref="shared_mock_provider",
        runtime_status="disabled",
        health_status="healthy",
        fallback_status="not_required",
        output_status="no_output",
        last_health_signal_ref="health_snapshot_shared_mock",
        source_chain_preserved=True,
    )


def _shared_fallback_route() -> ProviderFallbackRoute:
    return ProviderFallbackRoute(
        fallback_route_ref="fallback_route_shared_mock",
        domain_id=DOMAIN_SHARED,
        provider_ref="shared_mock_provider",
        fallback_provider_refs=("mock_spatial_provider",),
        fallback_mode="switch_to_mock",
        trigger_conditions=("tracking_lost",),
        preserve_source_chain=True,
        preserve_conflict_refs=True,
    )


def _shared_admission_check() -> ProviderRuntimeAdmissionCheck:
    return ProviderRuntimeAdmissionCheck(
        admission_check_ref="admission_check_shared_mock",
        domain_id=DOMAIN_SHARED,
        provider_ref="shared_mock_provider",
        admission_stage="planning_only",
        license_gate_passed=True,
        adapter_contract_passed=True,
        provider_admission_gate_passed=True,
        health_gate_passed=True,
        fallback_gate_passed=True,
        synthesis_gate_passed=True,
        static_validation_passed=True,
        runtime_admission_allowed=False,
        blocked_reasons=("planning_only_no_runtime_admission",),
    )


def _planning_decision(
    *,
    decision_ref: str,
    domain_id: str,
    provider_refs: Tuple[str, ...],
) -> ProviderManagerDecision:
    return ProviderManagerDecision(
        decision_ref=decision_ref,
        manager_ref=SHARED_MANAGER_REF,
        domain_id=domain_id,
        registered_provider_refs=provider_refs,
        runtime_enabled_provider_refs=(),
        default_disabled_provider_refs=provider_refs,
        enable_request_refs=(),
        disable_request_refs=(),
        fallback_route_refs=(),
        runtime_activation_allowed=False,
        provider_runtime_enabled=False,
        final_decision="shared_dryrun_case_planning_only",
    )


def _vision_ocr_profile() -> ProviderDomainGovernanceProfile:
    stub = build_vision_ocr_combined_governance_profile_v1()
    return ProviderDomainGovernanceProfile(
        profile_ref=stub["profile_ref"],
        domain_id=stub["domain_id"],
        domain_name=stub["domain_name"],
        admission_layer_ref=stub["admission_layer_ref"],
        synthesis_entrypoint=stub["synthesis_entrypoint"],
        provider_refs=tuple(stub["provider_refs"]),
        supported_output_candidate_types=tuple(stub["supported_output_candidate_types"]),
        domain_risk_tags=tuple(stub["domain_risk_tags"]),
        uses_shared_manager_skeleton=True,
    )


def _case(
    *,
    case_id: str,
    case_name: str,
    case_type: str,
    case_goal: str,
    expected_domain_id: str,
    expected_notes: Tuple[str, ...],
    managers: Tuple[ProviderRuntimeGovernanceManager, ...],
    registry_entries: Tuple[ProviderRegistryEntry, ...],
    enable_requests: Tuple[ProviderEnableRequest, ...] = (),
    disable_requests: Tuple[ProviderDisableRequest, ...] = (),
    runtime_states: Tuple[ProviderRuntimeState, ...] = (),
    health_snapshots: Tuple[ProviderHealthSnapshot, ...] = (),
    fallback_routes: Tuple[ProviderFallbackRoute, ...] = (),
    runtime_admission_checks: Tuple[ProviderRuntimeAdmissionCheck, ...] = (),
    manager_decisions: Tuple[ProviderManagerDecision, ...] = (),
    domain_profiles: Tuple[ProviderDomainGovernanceProfile, ...],
    expected_validation_ok: bool | None = None,
) -> SharedProviderRuntimeGovernanceDryRunCase:
    if expected_validation_ok is None:
        expected_validation_ok = case_type == "positive"
    return SharedProviderRuntimeGovernanceDryRunCase(
        case_id=case_id,
        case_name=case_name,
        case_type=case_type,
        case_goal=case_goal,
        managers=managers,
        registry_entries=registry_entries,
        enable_requests=enable_requests,
        disable_requests=disable_requests,
        runtime_states=runtime_states,
        health_snapshots=health_snapshots,
        fallback_routes=fallback_routes,
        runtime_admission_checks=runtime_admission_checks,
        manager_decisions=manager_decisions,
        domain_profiles=domain_profiles,
        expected_validation_ok=expected_validation_ok,
        expected_domain_id=expected_domain_id,
        expected_runtime_enabled=False,
        expected_notes=expected_notes,
    )


def build_case_common_01_registered_default_disabled() -> SharedProviderRuntimeGovernanceDryRunCase:
    profile = _shared_domain_profile()
    entry = _shared_registry_entry()
    return _case(
        case_id="case_common_01_registered_default_disabled",
        case_name="provider registered but default disabled",
        case_type="positive",
        case_goal="Validate shared registry can register provider without default enablement.",
        expected_domain_id=DOMAIN_SHARED,
        expected_notes=(
            "enabled_by_default=false.",
            "runtime_enable_allowed=false.",
            "provider_runtime_enabled=false.",
        ),
        managers=(_shared_manager(),),
        registry_entries=(entry,),
        runtime_states=(_shared_runtime_state(),),
        domain_profiles=(profile,),
    )


def build_case_common_02_enable_request_candidate_only() -> SharedProviderRuntimeGovernanceDryRunCase:
    profile = _shared_domain_profile()
    enable = ProviderEnableRequest(
        enable_request_ref="enable_request_shared_candidate",
        domain_id=DOMAIN_SHARED,
        provider_ref="shared_mock_provider",
        requested_scope="dryrun_only",
        requested_by="test_harness",
        reason="shared_enable_request_candidate_only",
        required_checks=REQUIRED_CHECKS,
        approval_required=True,
        execution_allowed=False,
    )
    return _case(
        case_id="case_common_02_enable_request_candidate_only",
        case_name="enable request candidate only",
        case_type="positive",
        case_goal="Validate enable request remains candidate with execution_allowed=false.",
        expected_domain_id=DOMAIN_SHARED,
        expected_notes=(
            "execution_allowed=false.",
            "approval_required=true.",
            "runtime_activation_allowed=false.",
        ),
        managers=(_shared_manager(),),
        registry_entries=(_shared_registry_entry(),),
        enable_requests=(enable,),
        domain_profiles=(profile,),
    )


def build_case_common_03_disable_request_planned_not_executed() -> SharedProviderRuntimeGovernanceDryRunCase:
    profile = _shared_domain_profile()
    disable = ProviderDisableRequest(
        disable_request_ref="disable_request_shared_planned",
        domain_id=DOMAIN_SHARED,
        provider_ref="shared_mock_provider",
        disable_reason="planning_default_disabled",
        disable_scope="provider_only",
        fallback_required=True,
        preserve_source_chain=True,
        execution_allowed=False,
    )
    return _case(
        case_id="case_common_03_disable_request_planned_not_executed",
        case_name="disable request planned not executed",
        case_type="positive",
        case_goal="Validate disable request can be planned without executing runtime.",
        expected_domain_id=DOMAIN_SHARED,
        expected_notes=(
            "fallback_required=true.",
            "preserve_source_chain=true.",
            "execution_allowed=false.",
        ),
        managers=(_shared_manager(),),
        registry_entries=(_shared_registry_entry(),),
        disable_requests=(disable,),
        domain_profiles=(profile,),
    )


def build_case_common_04_health_snapshot_degrade_disable() -> SharedProviderRuntimeGovernanceDryRunCase:
    profile = _shared_domain_profile()
    lost = ProviderHealthSnapshot(
        health_snapshot_ref="health_snapshot_tracking_lost",
        domain_id=DOMAIN_SHARED,
        provider_ref="shared_mock_provider",
        signal_name="tracking_status",
        signal_value="tracking_lost",
        confidence=0.2,
        source_freshness="stale",
        health_decision="disable_provider",
        degradation_required=False,
        disable_required=True,
    )
    drift = ProviderHealthSnapshot(
        health_snapshot_ref="health_snapshot_high_drift",
        domain_id=DOMAIN_SHARED,
        provider_ref="shared_mock_provider",
        signal_name="drift_risk",
        signal_value="high",
        confidence=0.45,
        source_freshness="fresh",
        health_decision="degrade_candidate_output",
        degradation_required=True,
        disable_required=False,
    )
    return _case(
        case_id="case_common_04_health_snapshot_degrade_disable",
        case_name="health snapshot degrade and disable candidates",
        case_type="positive",
        case_goal="Validate health snapshot rules for tracking_lost and high_drift.",
        expected_domain_id=DOMAIN_SHARED,
        expected_notes=(
            "tracking_lost requires disable_required=true.",
            "high_drift requires degradation_required=true.",
            "confidence within 0~1.",
        ),
        managers=(_shared_manager(),),
        registry_entries=(_shared_registry_entry(),),
        health_snapshots=(lost, drift),
        domain_profiles=(profile,),
    )


def build_case_common_05_fallback_route_preserves_chain() -> SharedProviderRuntimeGovernanceDryRunCase:
    profile = _shared_domain_profile()
    return _case(
        case_id="case_common_05_fallback_route_preserves_chain",
        case_name="fallback route preserves source chain",
        case_type="positive",
        case_goal="Validate fallback route preserves source chain and conflict refs.",
        expected_domain_id=DOMAIN_SHARED,
        expected_notes=(
            "preserve_source_chain=true.",
            "preserve_conflict_refs=true.",
        ),
        managers=(_shared_manager(),),
        registry_entries=(_shared_registry_entry(),),
        fallback_routes=(_shared_fallback_route(),),
        domain_profiles=(profile,),
    )


def build_case_common_06_admission_check_not_runtime_enabled() -> SharedProviderRuntimeGovernanceDryRunCase:
    profile = _shared_domain_profile()
    decision = _planning_decision(
        decision_ref="manager_decision_common_06",
        domain_id=DOMAIN_SHARED,
        provider_refs=("shared_mock_provider",),
    )
    return _case(
        case_id="case_common_06_admission_check_not_runtime_enabled",
        case_name="runtime admission check not runtime enabled",
        case_type="positive",
        case_goal=(
            "Validate runtime admission check exists while runtime_enabled_provider_refs "
            "remain empty."
        ),
        expected_domain_id=DOMAIN_SHARED,
        expected_notes=(
            "runtime_admission_check exists.",
            "runtime_enabled_provider_refs=[].",
            "provider_runtime_enabled=false.",
        ),
        managers=(_shared_manager(),),
        registry_entries=(_shared_registry_entry(),),
        runtime_admission_checks=(_shared_admission_check(),),
        manager_decisions=(decision,),
        domain_profiles=(profile,),
    )


def build_case_spatial_01_profile_attached() -> SharedProviderRuntimeGovernanceDryRunCase:
    catalog = build_spatial_evidence_domain_governance_catalog_v1()
    profile = build_spatial_evidence_provider_governance_profile_v1()
    manager = build_spatial_evidence_governance_manager_v1()
    entry = ProviderRegistryEntry(**catalog["registry_entries"][0])  # type: ignore[arg-type]
    return _case(
        case_id="case_spatial_01_profile_attached",
        case_name="Spatial Evidence profile attached to shared skeleton",
        case_type="positive",
        case_goal=(
            "Validate spatial_evidence domain profile connects to shared governance "
            "with field_synthesis_v1."
        ),
        expected_domain_id=DOMAIN_SPATIAL_EVIDENCE,
        expected_notes=(
            "synthesis_entrypoint=field_synthesis_v1.",
            "provider_openvins registered.",
            "runtime_activation_allowed=false.",
        ),
        managers=(manager,),
        registry_entries=(entry,),
        runtime_states=(ProviderRuntimeState(**catalog["runtime_states"][0]),),  # type: ignore[arg-type]
        domain_profiles=(profile,),
    )


def build_case_spatial_02_inherits_admission_boundaries() -> SharedProviderRuntimeGovernanceDryRunCase:
    catalog = build_spatial_evidence_domain_governance_catalog_v1()
    profile = build_spatial_evidence_provider_governance_profile_v1()
    manager = build_spatial_evidence_governance_manager_v1()
    decision = _planning_decision(
        decision_ref="manager_decision_spatial_02",
        domain_id=DOMAIN_SPATIAL_EVIDENCE,
        provider_refs=profile.provider_refs,
    )
    admission = ProviderRuntimeAdmissionCheck(**catalog["admission_checks"][0])  # type: ignore[arg-type]
    return _case(
        case_id="case_spatial_02_inherits_admission_boundaries",
        case_name="Spatial Evidence inherits Provider Admission boundaries",
        case_type="positive",
        case_goal=(
            "Validate spatial profile preserves admission frozen boundaries: no runtime "
            "enablement, field_synthesis_v1 only, candidate_only."
        ),
        expected_domain_id=DOMAIN_SPATIAL_EVIDENCE,
        expected_notes=(
            "runtime_enabled_provider_refs=[].",
            "field_synthesis_v1_only=true.",
            "candidate_only_chain_preserved=true.",
        ),
        managers=(manager,),
        registry_entries=tuple(
            ProviderRegistryEntry(**item)  # type: ignore[arg-type]
            for item in catalog["registry_entries"][:2]
        ),
        runtime_admission_checks=(admission,),
        manager_decisions=(decision,),
        domain_profiles=(profile,),
    )


def build_case_vision_ocr_01_compatibility_aligned() -> SharedProviderRuntimeGovernanceDryRunCase:
    profile = _vision_ocr_profile()
    manager = ProviderRuntimeGovernanceManager(
        manager_ref=f"{SHARED_MANAGER_REF}_{DOMAIN_VISION_OCR}",
        domain_id=DOMAIN_VISION_OCR,
        manager_status="planning",
        managed_provider_refs=profile.provider_refs,
        default_enabled_provider_refs=(),
        default_disabled_provider_refs=profile.provider_refs,
        synthesis_entrypoint=MIDPLATFORM_SYNTHESIS_ENTRYPOINT,
        runtime_activation_allowed=False,
        provider_runtime_enabled=False,
    )
    entry = ProviderRegistryEntry(
        registry_entry_ref="registry_entry_vision_mock",
        domain_id=DOMAIN_VISION_OCR,
        provider_ref="vision_provider_mock_fixture",
        backend_ref="vision_mock",
        adapter_ref="vision_mock_adapter",
        provider_role="mock_provider",
        registration_status="registered_candidate",
        admission_policy_ref="admission_policy_vision_mock",
        health_gate_ref="health_gate_vision_mock",
        fallback_policy_ref="fallback_vision_mock",
        enabled_by_default=False,
        runtime_enable_allowed=False,
        supported_output_candidate_types=("DetectionCandidate", "TrackingCandidate"),
    )
    return _case(
        case_id="case_vision_ocr_01_compatibility_aligned",
        case_name="Vision/OCR compatibility profile aligned",
        case_type="positive",
        case_goal=(
            "Validate vision_ocr domain profile aligns with provider_abstraction_standard_v1."
        ),
        expected_domain_id=DOMAIN_VISION_OCR,
        expected_notes=(
            "provider_abstraction_standard_v1 compatible.",
            "candidate_output_only=true.",
            "runtime_activation_allowed=false.",
        ),
        managers=(manager,),
        registry_entries=(entry,),
        runtime_states=(
            ProviderRuntimeState(
                runtime_state_ref="runtime_state_vision_mock",
                domain_id=DOMAIN_VISION_OCR,
                provider_ref="vision_provider_mock_fixture",
                runtime_status="disabled",
                health_status="healthy",
                fallback_status="not_required",
                output_status="candidate_output_only",
                last_health_signal_ref="health_snapshot_vision_mock",
                source_chain_preserved=True,
            ),
        ),
        domain_profiles=(profile,),
    )


def build_case_vision_ocr_02_no_spatial_pollution() -> SharedProviderRuntimeGovernanceDryRunCase:
    profile = _vision_ocr_profile()
    entry = ProviderRegistryEntry(
        registry_entry_ref="registry_entry_ocr_mock",
        domain_id=DOMAIN_VISION_OCR,
        provider_ref="ocr_provider_mock_fixture",
        backend_ref="ocr_mock",
        adapter_ref="ocr_mock_adapter",
        provider_role="mock_provider",
        registration_status="registered_candidate",
        admission_policy_ref="admission_policy_ocr_mock",
        health_gate_ref="health_gate_ocr_mock",
        fallback_policy_ref="fallback_ocr_mock",
        enabled_by_default=False,
        runtime_enable_allowed=False,
        supported_output_candidate_types=("ocr_result_candidate", "roi_candidate"),
    )
    spatial_types = {"PoseCandidate", "SLAMHealthCandidate"}
    assert not spatial_types.intersection(set(profile.supported_output_candidate_types))
    return _case(
        case_id="case_vision_ocr_02_no_spatial_pollution",
        case_name="Vision/OCR not polluted by Spatial Evidence rules",
        case_type="positive",
        case_goal=(
            "Validate vision_ocr profile declares its own candidate types without "
            "requiring PoseCandidate or SLAMHealthCandidate."
        ),
        expected_domain_id=DOMAIN_VISION_OCR,
        expected_notes=(
            "no PoseCandidate required.",
            "no SLAMHealthCandidate required.",
            "domain-specific candidate types only.",
        ),
        managers=(),
        registry_entries=(entry,),
        domain_profiles=(profile,),
    )


def build_invalid_case_a_default_enabled() -> SharedProviderRuntimeGovernanceDryRunCase:
    profile = _shared_domain_profile()
    entry = replace(_shared_registry_entry(), enabled_by_default=True, runtime_enable_allowed=True)
    return _case(
        case_id="invalid_a_default_enabled_provider",
        case_name="default enabled provider",
        case_type="invalid",
        case_goal="Reject provider registered with enabled_by_default=true.",
        expected_domain_id=DOMAIN_SHARED,
        expected_notes=("enabled_by_default_must_be_false.",),
        managers=(_shared_manager(),),
        registry_entries=(entry,),
        domain_profiles=(profile,),
    )


def build_invalid_case_b_runtime_activation_allowed() -> SharedProviderRuntimeGovernanceDryRunCase:
    profile = _shared_domain_profile()
    manager = replace(
        _shared_manager(),
        runtime_activation_allowed=True,
        provider_runtime_enabled=True,
    )
    return _case(
        case_id="invalid_b_runtime_activation_allowed",
        case_name="planning runtime_activation_allowed=true",
        case_type="invalid",
        case_goal="Reject planning manager with runtime activation enabled.",
        expected_domain_id=DOMAIN_SHARED,
        expected_notes=("runtime_activation_allowed_must_be_false_in_planning.",),
        managers=(manager,),
        registry_entries=(_shared_registry_entry(),),
        domain_profiles=(profile,),
    )


def build_invalid_case_c_missing_domain_profile() -> SharedProviderRuntimeGovernanceDryRunCase:
    return _case(
        case_id="invalid_c_missing_domain_profile",
        case_name="provider registered without domain profile",
        case_type="invalid",
        case_goal="Reject registry entry without matching domain profile binding.",
        expected_domain_id=DOMAIN_SHARED,
        expected_notes=("domain_profile_required_when_registry_entries_present.",),
        managers=(_shared_manager(),),
        registry_entries=(_shared_registry_entry(),),
        domain_profiles=(),
    )


def build_invalid_case_d_direct_action() -> SharedProviderRuntimeGovernanceDryRunCase:
    profile = _shared_domain_profile()
    enable = ProviderEnableRequest(
        enable_request_ref="enable_request_direct_action",
        domain_id=DOMAIN_SHARED,
        provider_ref="shared_mock_provider",
        requested_scope="dryrun_only",
        requested_by="runtime_manager",
        reason="manager_direct_action attempted",
        required_checks=REQUIRED_CHECKS,
        approval_required=False,
        execution_allowed=False,
    )
    return _case(
        case_id="invalid_d_direct_action_forbidden",
        case_name="forbidden direct action policy",
        case_type="invalid",
        case_goal="Reject enable request referencing forbidden manager_direct_action.",
        expected_domain_id=DOMAIN_SHARED,
        expected_notes=("forbidden_provider_manager_policy_present:manager_direct_action",),
        managers=(_shared_manager(),),
        registry_entries=(_shared_registry_entry(),),
        enable_requests=(enable,),
        domain_profiles=(profile,),
    )


def build_invalid_case_e_fallback_no_source_chain() -> SharedProviderRuntimeGovernanceDryRunCase:
    profile = _shared_domain_profile()
    route = replace(_shared_fallback_route(), preserve_source_chain=False)
    return _case(
        case_id="invalid_e_fallback_no_source_chain",
        case_name="fallback without source chain",
        case_type="invalid",
        case_goal="Reject fallback route when preserve_source_chain=false.",
        expected_domain_id=DOMAIN_SHARED,
        expected_notes=("preserve_source_chain_required.",),
        managers=(_shared_manager(),),
        registry_entries=(_shared_registry_entry(),),
        fallback_routes=(route,),
        domain_profiles=(profile,),
    )


def build_invalid_case_f_spatial_bypass_synthesis() -> SharedProviderRuntimeGovernanceDryRunCase:
    profile = build_spatial_evidence_provider_governance_profile_v1()
    manager = replace(
        build_spatial_evidence_governance_manager_v1(),
        synthesis_entrypoint="direct_action_v1",
    )
    catalog = build_spatial_evidence_domain_governance_catalog_v1()
    entry = ProviderRegistryEntry(**catalog["registry_entries"][0])  # type: ignore[arg-type]
    return _case(
        case_id="invalid_f_spatial_bypass_field_synthesis",
        case_name="Spatial Evidence bypass field_synthesis_v1",
        case_type="invalid",
        case_goal="Reject spatial_evidence manager with non-field synthesis entrypoint.",
        expected_domain_id=DOMAIN_SPATIAL_EVIDENCE,
        expected_notes=("synthesis_entrypoint_not_registered.",),
        managers=(manager,),
        registry_entries=(entry,),
        domain_profiles=(profile,),
    )


def build_invalid_case_g_vision_ocr_spatial_pollution() -> SharedProviderRuntimeGovernanceDryRunCase:
    profile = _vision_ocr_profile()
    entry = ProviderRegistryEntry(
        registry_entry_ref="registry_entry_vision_ocr_spatial_pollution",
        domain_id=DOMAIN_VISION_OCR,
        provider_ref="vision_provider_mock_fixture",
        backend_ref="vision_mock",
        adapter_ref="vision_mock_adapter",
        provider_role="mock_provider",
        registration_status="registered_candidate",
        admission_policy_ref="admission_policy_vision_mock",
        health_gate_ref="health_gate_vision_mock",
        fallback_policy_ref="fallback_vision_mock",
        enabled_by_default=False,
        runtime_enable_allowed=False,
        supported_output_candidate_types=("PoseCandidate", "SLAMHealthCandidate"),
    )
    return _case(
        case_id="invalid_g_vision_ocr_spatial_candidate_pollution",
        case_name="Vision/OCR wrongly requires Spatial candidates",
        case_type="invalid",
        case_goal=(
            "Reject vision_ocr registry entry declaring Spatial-only candidates not "
            "supported by domain profile."
        ),
        expected_domain_id=DOMAIN_VISION_OCR,
        expected_notes=(
            "candidate_not_in_domain_profile:PoseCandidate.",
            "candidate_not_in_domain_profile:SLAMHealthCandidate.",
        ),
        managers=(),
        registry_entries=(entry,),
        domain_profiles=(profile,),
    )


def build_positive_shared_provider_runtime_governance_cases_v1() -> Tuple[
    SharedProviderRuntimeGovernanceDryRunCase, ...
]:
    return (
        build_case_common_01_registered_default_disabled(),
        build_case_common_02_enable_request_candidate_only(),
        build_case_common_03_disable_request_planned_not_executed(),
        build_case_common_04_health_snapshot_degrade_disable(),
        build_case_common_05_fallback_route_preserves_chain(),
        build_case_common_06_admission_check_not_runtime_enabled(),
        build_case_spatial_01_profile_attached(),
        build_case_spatial_02_inherits_admission_boundaries(),
        build_case_vision_ocr_01_compatibility_aligned(),
        build_case_vision_ocr_02_no_spatial_pollution(),
    )


def build_invalid_shared_provider_runtime_governance_cases_v1() -> Tuple[
    SharedProviderRuntimeGovernanceDryRunCase, ...
]:
    return (
        build_invalid_case_a_default_enabled(),
        build_invalid_case_b_runtime_activation_allowed(),
        build_invalid_case_c_missing_domain_profile(),
        build_invalid_case_d_direct_action(),
        build_invalid_case_e_fallback_no_source_chain(),
        build_invalid_case_f_spatial_bypass_synthesis(),
        build_invalid_case_g_vision_ocr_spatial_pollution(),
    )


def build_all_shared_provider_runtime_governance_cases_v1() -> Tuple[
    SharedProviderRuntimeGovernanceDryRunCase, ...
]:
    return (
        build_positive_shared_provider_runtime_governance_cases_v1()
        + build_invalid_shared_provider_runtime_governance_cases_v1()
    )


def bundle_from_shared_provider_runtime_governance_case(
    case: SharedProviderRuntimeGovernanceDryRunCase,
) -> Dict[str, object]:
    return {
        "case_id": case.case_id,
        "case_type": case.case_type,
        "expected_domain_id": case.expected_domain_id,
        "expected_runtime_enabled": case.expected_runtime_enabled,
        "managers": [candidate_to_dict(m) for m in case.managers],
        "domain_profiles": [candidate_to_dict(p) for p in case.domain_profiles],
        "registry_entries": [candidate_to_dict(e) for e in case.registry_entries],
        "enable_requests": [candidate_to_dict(r) for r in case.enable_requests],
        "disable_requests": [candidate_to_dict(r) for r in case.disable_requests],
        "runtime_states": [candidate_to_dict(s) for s in case.runtime_states],
        "health_snapshots": [candidate_to_dict(h) for h in case.health_snapshots],
        "fallback_routes": [candidate_to_dict(r) for r in case.fallback_routes],
        "runtime_admission_checks": [candidate_to_dict(c) for c in case.runtime_admission_checks],
        "manager_decisions": [candidate_to_dict(d) for d in case.manager_decisions],
    }


def validate_shared_provider_runtime_governance_case_ids_unique(
    cases: Tuple[SharedProviderRuntimeGovernanceDryRunCase, ...] | None = None,
) -> Tuple[bool, Tuple[str, ...]]:
    cases = cases or build_all_shared_provider_runtime_governance_cases_v1()
    seen: Dict[str, int] = {}
    duplicates: List[str] = []
    for case in cases:
        seen[case.case_id] = seen.get(case.case_id, 0) + 1
    for case_id, count in seen.items():
        if count > 1:
            duplicates.append(case_id)
    return len(duplicates) == 0, tuple(duplicates)


def _validate_case(case: SharedProviderRuntimeGovernanceDryRunCase) -> Tuple[bool, List[str]]:
    return validate_provider_runtime_governance_case_bundle(
        bundle_from_shared_provider_runtime_governance_case(case)
    )


def _check_cases(
    cases: Tuple[SharedProviderRuntimeGovernanceDryRunCase, ...],
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


def summarize_shared_provider_runtime_governance_dryrun_cases_v1() -> Dict[str, Any]:
    positive = build_positive_shared_provider_runtime_governance_cases_v1()
    invalid = build_invalid_shared_provider_runtime_governance_cases_v1()
    all_cases = build_all_shared_provider_runtime_governance_cases_v1()

    unique_ok, duplicates = validate_shared_provider_runtime_governance_case_ids_unique(all_cases)
    pos_ok, pos_mismatches = _check_cases(positive, expect_valid=True)
    inv_ok, inv_mismatches = _check_cases(invalid, expect_valid=False)

    sample_positive_ok = False
    sample_invalid_rejected = False
    if positive:
        sample_positive_ok, _ = _validate_case(positive[0])
    if invalid:
        invalid_ok, _ = _validate_case(invalid[0])
        sample_invalid_rejected = not invalid_ok

    vision_ocr_ok, _, _ = verify_vision_ocr_compatibility_v1()
    no_dup = _no_domain_specific_manager_duplication()
    spatial_supported = any(
        profile.domain_id == DOMAIN_SPATIAL_EVIDENCE
        for case in positive
        for profile in case.domain_profiles
    )

    ready = (
        len(positive) == 10
        and len(invalid) == 7
        and unique_ok
        and pos_ok == len(positive)
        and inv_ok == len(invalid)
        and not pos_mismatches
        and not inv_mismatches
        and sample_positive_ok
        and sample_invalid_rejected
        and vision_ocr_ok
        and no_dup
        and spatial_supported
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 2 Shared Provider Runtime Governance Dry-run Cases",
        "governance_principle_zh": GOVERNANCE_PRINCIPLE_ZH,
        "positive_case_count": len(positive),
        "invalid_case_count": len(invalid),
        "case_count": len(all_cases),
        "positive_case_ids": tuple(c.case_id for c in positive),
        "invalid_case_ids": tuple(c.case_id for c in invalid),
        "case_ids_unique": unique_ok,
        "duplicate_case_ids": duplicates,
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "shared_provider_cases_ok": pos_ok,
        "shared_provider_invalid_cases_ok": inv_ok,
        "shared_provider_case_ids_unique_ok": unique_ok,
        "sample_positive_validate_ok": sample_positive_ok,
        "sample_invalid_rejected_ok": sample_invalid_rejected,
        "positive_validation_mismatches": pos_mismatches,
        "invalid_validation_mismatches": inv_mismatches,
        "shared_provider_runtime_governance_ready": ready,
        "vision_ocr_compatibility_preserved": vision_ocr_ok,
        "spatial_evidence_profile_supported": spatial_supported,
        "no_domain_specific_manager_duplication": no_dup,
        "runtime_activation_allowed": False,
        "provider_runtime_enabled": False,
        "candidate_only_enforced": True,
        "domain_profile_required": True,
        "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT,
        "final_decision": (
            FINAL_DECISION_DRYRUN_CASES_READY_FOR_RUNNER
            if ready
            else "SHARED_PROVIDER_RUNTIME_GOVERNANCE_DRYRUN_CASES_NOT_READY"
        ),
    }


def main() -> int:
    summary = summarize_shared_provider_runtime_governance_dryrun_cases_v1()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["final_decision"] == FINAL_DECISION_DRYRUN_CASES_READY_FOR_RUNNER else 1


if __name__ == "__main__":
    raise SystemExit(main())
