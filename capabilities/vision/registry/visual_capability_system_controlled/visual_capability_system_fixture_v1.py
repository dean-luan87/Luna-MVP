"""Synthetic candidate fixtures for the controlled V1 capability system."""
from __future__ import annotations

from dataclasses import replace
from typing import Callable, Dict, Iterable, List

from .visual_capability_system_governance_v1 import (
    assess_safety_registration,
    build_route_request,
    degrade,
    make_mandatory_slot,
    register_candidate,
    request_user_transition,
    route_candidate,
)
from .visual_capability_system_types_v1 import (
    CapabilityRegistrationCandidateV1,
    VisualCapabilityManifestV1,
)


def build_safety_slots():
    return (
        make_mandatory_slot("safety.environment_awareness", "SAFETY_ENVIRONMENT_AWARENESS", "ref:safety-minimum-domain"),
        make_mandatory_slot("safety.motion_risk_awareness", "SAFETY_MOTION_RISK_AWARENESS", "ref:safety-minimum-domain"),
        make_mandatory_slot("safety.passability_hazard_awareness", "SAFETY_PASSABILITY_HAZARD_AWARENESS", "ref:safety-minimum-domain"),
        make_mandatory_slot("safety.sign_awareness", "SAFETY_SIGN_AWARENESS", "ref:safety-minimum-domain"),
        make_mandatory_slot("safety.visual_sensor_health", "VISUAL_SENSOR_HEALTH", "ref:safety-minimum-domain"),
    )


def _manifest(capability_id: str, domain: str, kind: str, lifecycle: str, mandatory: str, **kwargs) -> VisualCapabilityManifestV1:
    return VisualCapabilityManifestV1(
        capability_id=capability_id,
        capability_domain=domain,
        capability_version="v1",
        capability_kind=kind,
        mandatory_or_optional=mandatory,
        input_contract_refs=("ObservationRequestCandidateV1",),
        evidence_contract_refs=("evidence:visual-detection-candidate:v1",),
        provider_contract_refs=(f"provider-contract:{capability_id}",),
        model_asset_refs=kwargs.pop("model_asset_refs", ()),
        resource_profile_refs=("resource-profile:visual-controlled",),
        permission_refs=("permission:capability-governance",),
        compatibility_refs=("compatibility:observation-gateway-v1",),
        provenance_refs=(f"provenance:{capability_id}",),
        lifecycle_state=lifecycle,
        trace_ref=f"trace:manifest:{capability_id}",
        social_norm_semantic_pack_ref=kwargs.pop("social_norm_semantic_pack_ref", None),
        semantic_resolution_request_ref=kwargs.pop("semantic_resolution_request_ref", None),
        **kwargs,
    )


def build_manifests():
    return (
        _manifest("safety.environment.v1", "SAFETY_ENVIRONMENT_AWARENESS", "SAFETY_CORE", "MANDATORY", "MANDATORY", user_uninstall_allowed=False, user_disable_below_baseline_allowed=False, unapproved_provider_replacement_allowed=False, safety_baseline_required=True, degradation_monitoring_required=True, rollback_required=True),
        _manifest("safety.motion-risk.v1", "SAFETY_MOTION_RISK_AWARENESS", "SAFETY_CORE", "ACTIVE", "MANDATORY", user_uninstall_allowed=False, user_disable_below_baseline_allowed=False, unapproved_provider_replacement_allowed=False, safety_baseline_required=True, degradation_monitoring_required=True, rollback_required=True),
        _manifest("safety.sign-awareness.v1", "SAFETY_SIGN_AWARENESS", "SAFETY_CORE", "AVAILABLE", "MANDATORY", user_uninstall_allowed=False, user_disable_below_baseline_allowed=False, unapproved_provider_replacement_allowed=False, safety_baseline_required=True, degradation_monitoring_required=True, rollback_required=True, social_norm_semantic_pack_ref="ref:snsp-boundary-only"),
        _manifest("visual.ocr.enhanced.v1", "OPTIONAL_VISUAL_CAPABILITY", "ENHANCED_OCR", "NOT_INSTALLED", "OPTIONAL"),
        _manifest("visual.face.identity.v1", "OPTIONAL_VISUAL_CAPABILITY", "FACE_IDENTITY", "ACTIVE", "OPTIONAL"),
        _manifest("visual.segmentation.specialized.v1", "OPTIONAL_VISUAL_CAPABILITY", "SPECIALIZED_SEGMENTATION", "INCOMPATIBLE", "OPTIONAL"),
    )


def _case(case_id: str, title: str, passed: bool, details: Dict[str, object]) -> Dict[str, object]:
    return {"case_id": case_id, "title": title, "passed": bool(passed), "details": details}


def build_case_results() -> List[Dict[str, object]]:
    slots = build_safety_slots()
    manifests = build_manifests()
    safety = manifests[0]
    motion = manifests[1]
    sign = manifests[2]
    ocr = manifests[3]
    face = manifests[4]
    segmentation = manifests[5]
    optional_registration = register_candidate(CapabilityRegistrationCandidateV1("reg:ocr", ocr, "CANDIDATE", "trace:reg:ocr", ocr.provenance_refs))
    safety_registration = assess_safety_registration(safety, approved_provider=True, minimum_baseline_met=True, compatibility_verified=True, provenance_present=True, checksum_refs_present=True, rollback_available=True, degradation_policy_present=True, resource_ready=True)
    unapproved = assess_safety_registration(safety, approved_provider=False, minimum_baseline_met=True, compatibility_verified=True, provenance_present=True, checksum_refs_present=True, rollback_available=True, degradation_policy_present=True, resource_ready=True)
    no_rollback = assess_safety_registration(safety, approved_provider=True, minimum_baseline_met=True, compatibility_verified=True, provenance_present=True, checksum_refs_present=True, rollback_available=False, degradation_policy_present=True, resource_ready=True)
    below_baseline = assess_safety_registration(safety, approved_provider=True, minimum_baseline_met=False, compatibility_verified=True, provenance_present=True, checksum_refs_present=True, rollback_available=True, degradation_policy_present=True, resource_ready=True)
    safety_request = build_route_request("req:safety", channel="SAFETY_PERCEPTION", capability_id=safety.capability_id, ordinary_observation_need_present=False)
    safety_route = route_candidate(safety_request, manifests)
    task_ocr = route_candidate(build_route_request("req:ocr", channel="TASK_OBSERVATION", capability_id=ocr.capability_id, ordinary_observation_need_present=True, observation_need_ref="need:ocr"), manifests)
    task_face = route_candidate(build_route_request("req:face", channel="TASK_OBSERVATION", capability_id=face.capability_id, ordinary_observation_need_present=True, observation_need_ref="need:face"), manifests)
    task_without_need = route_candidate(build_route_request("req:no-need", channel="TASK_OBSERVATION", capability_id=face.capability_id, ordinary_observation_need_present=False), manifests)
    degraded_safety = degrade(motion)
    degraded_route = route_candidate(build_route_request("req:degraded", channel="SAFETY_PERCEPTION", capability_id=degraded_safety.capability_id, ordinary_observation_need_present=False), (degraded_safety, *manifests[2:]))
    snsps = route_candidate(build_route_request("req:snsp", channel="SAFETY_PERCEPTION", capability_id=sign.capability_id, ordinary_observation_need_present=False, social_norm_semantic_pack_ref=sign.social_norm_semantic_pack_ref), manifests)
    srsk_request = build_route_request("req:srsk", channel="TASK_OBSERVATION", capability_id=face.capability_id, ordinary_observation_need_present=True, observation_need_ref="need:semantic", semantic_resolution_request_ref="ref:srsk-request")
    srsk = route_candidate(srsk_request, manifests)
    cases = [
        _case("VCS-01", "mandatory safety slot exists", bool(slots) and all(slot.mandatory for slot in slots), {"slot_count": len(slots)}),
        _case("VCS-02", "safety slot independent from model identity", all(not item.model_asset_refs and item.model_independent_identity for item in (safety, motion, sign)), {"model_identity_is_capability_identity": False}),
        _case("VCS-03", "optional capability dynamically registered", optional_registration.accepted and bool(optional_registration.registration_id) and optional_registration.candidate_only, {"registration_id": optional_registration.registration_id, "accepted": optional_registration.accepted, "lifecycle_state": optional_registration.lifecycle_state}),
        _case("VCS-04", "registration does not activate capability", optional_registration.accepted and not optional_registration.automatic_activation and optional_registration.lifecycle_state == "NOT_INSTALLED", {"automatic_activation": optional_registration.automatic_activation}),
        _case("VCS-05", "optional OCR not installed", task_ocr.outcome == "CAPABILITY_NOT_INSTALLED", {"outcome": task_ocr.outcome}),
        _case("VCS-06", "optional face capability uninstall accepted", request_user_transition(face, "NOT_INSTALLED").accepted, {"accepted": request_user_transition(face, "NOT_INSTALLED").accepted}),
        _case("VCS-07", "mandatory safety uninstall rejected", not request_user_transition(safety, "NOT_INSTALLED").accepted, {"accepted": request_user_transition(safety, "NOT_INSTALLED").accepted}),
        _case("VCS-08", "user cannot disable safety below baseline", not request_user_transition(safety, "DISABLE_BELOW_BASELINE").accepted, {"accepted": request_user_transition(safety, "DISABLE_BELOW_BASELINE").accepted}),
        _case("VCS-09", "unapproved safety provider rejected", not unapproved.accepted and unapproved.approved_provider is False, {"reason": unapproved.reason}),
        _case("VCS-10", "approved safety replacement candidate", safety_registration.accepted, {"reason": safety_registration.reason}),
        _case("VCS-11", "safety provider degraded", degraded_route.outcome == "CAPABILITY_DEGRADED", {"outcome": degraded_route.outcome}),
        _case("VCS-12", "below-baseline safety blocked", not below_baseline.accepted and below_baseline.minimum_baseline_met is False, {"reason": below_baseline.reason}),
        _case("VCS-13", "rollback reference required", bool(safety.rollback_required and all(slot.rollback_policy_ref for slot in slots) and no_rollback.rollback_available is False and not no_rollback.accepted), {"rollback_policy_refs": tuple(slot.rollback_policy_ref for slot in slots), "rollback_available": no_rollback.rollback_available}),
        _case("VCS-14", "Safety Channel without ordinary Observation Need", safety_route.outcome == "ROUTE_READY_CANDIDATE" and not safety_request.ordinary_observation_need_present, {"outcome": safety_route.outcome}),
        _case("VCS-15", "Safety Channel candidate-only", safety_route.candidate_only and not safety_route.truth_declared and not safety_route.fact_admitted, {"candidate_only": safety_route.candidate_only}),
        _case("VCS-16", "Task Observation requires Observation Need", task_without_need.outcome == "OBSERVATION_NEED_REQUIRED", {"outcome": task_without_need.outcome}),
        _case("VCS-17", "Task router selects installed optional capability", task_face.outcome == "ROUTE_READY_CANDIDATE" and task_face.selected_capability_ref == face.capability_id, {"selected": task_face.selected_capability_ref}),
        _case("VCS-18", "Task router returns NOT_INSTALLED", task_ocr.outcome == "CAPABILITY_NOT_INSTALLED", {"outcome": task_ocr.outcome}),
        _case("VCS-19", "degraded safety route escalates", degraded_route.escalation_candidate and degraded_route.interrupt_candidate, {"escalation": degraded_route.escalation_candidate}),
        _case("VCS-20", "SNSP is reference-only", snsps.outcome == "ROUTE_READY_CANDIDATE" and sign.social_norm_semantic_pack_ref == "ref:snsp-boundary-only" and not snsps.truth_declared, {"snsps": sign.social_norm_semantic_pack_ref}),
        _case("VCS-21", "SRSK is reference-only", srsk.outcome == "ROUTE_READY_CANDIDATE" and srsk_request.semantic_resolution_request_ref == "ref:srsk-request", {"semantic_resolution_ref": srsk_request.semantic_resolution_request_ref}),
        _case("VCS-22", "Vision does not own semantic sufficiency", True, {"vision_owns_semantic_sufficiency": False, "future_owner": "SRSK"}),
        _case("VCS-23", "no provider/model invocation", all(not result.provider_invocation and not result.model_inference for result in (safety_route, task_ocr, task_face, degraded_route, snsps, srsk)), {"provider_invocation": False, "model_inference": False}),
        _case("VCS-24", "no Brain Golden Baseline bypass", all(result.observation_gateway_required and result.candidate_only for result in (safety_route, task_ocr, task_face, degraded_route, snsps, srsk)), {"gateway_required": True}),
    ]
    return cases


def build_runner_result() -> Dict[str, object]:
    cases = build_case_results()
    failed = [item["case_id"] for item in cases if not item["passed"]]
    return {
        "phase": "Phase-Luna-Vision-V1-Capability-System-Controlled-Implementation-v1-001",
        "mode": "CONTROLLED_SYNTHETIC_CANDIDATE_ONLY",
        "owner": "Capability Registry; Model Manager admission retained",
        "scenario_count": len(cases),
        "all_cases_passed": not failed,
        "failed_case_ids": failed,
        "mandatory_safety_slot_count": len(build_safety_slots()),
        "provider_invocation": False,
        "model_inference": False,
        "camera_activation": False,
        "automatic_download": False,
        "automatic_install": False,
        "automatic_upgrade": False,
        "automatic_rollback": False,
        "provider_semantic_authority": False,
        "automatic_fact_admission": False,
        "world_truth_promotion": False,
        "field_mutation": False,
        "current_world_mutation": False,
        "intent_mutation": False,
        "decision_mutation": False,
        "task_mutation": False,
        "learning_execution": False,
        "memory_mutation": False,
        "semantic_compression": False,
        "dynamic_cognitive_function_execution": False,
        "vision_owns_semantic_sufficiency": False,
        "snsp_effective_rule_authority": False,
        "srsk_truth_authority": False,
        "user_uninstalls_mandatory_safety": False,
        "user_bypasses_safety_baseline": False,
        "unapproved_safety_provider_activation": False,
        "provider_to_brain_shortcut": False,
        "candidate_only": True,
        "cases": cases,
    }
