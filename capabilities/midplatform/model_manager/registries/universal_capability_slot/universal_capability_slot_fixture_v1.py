"""Controlled synthetic scenarios for the Universal Slot foundation."""

from __future__ import annotations

from dataclasses import replace
from typing import Dict, Iterable, List, Tuple

from .universal_capability_slot_governance_v1 import (
    assess_official_module_admission,
    assess_slot_compatibility,
    build_binding_candidate,
    build_capability_regulation_candidate,
    build_capability_self_view,
    build_module_admission_candidate,
    govern_binding,
    request_slot_lifecycle,
)
from .universal_capability_slot_resolution_v1 import (
    build_invocation_candidate,
    resolve_capability_requirement,
)
from .universal_capability_slot_types_v1 import (
    CapabilityModuleV1,
    CapabilityRequirementV1,
    OfficialCapabilityModuleV1,
    UniversalCapabilitySlotV1,
)


def _module(
    module_id: str,
    purpose: str,
    requirement_class: str,
    *,
    lifecycle_state: str = "AVAILABLE",
    implementation_refs: Tuple[str, ...] = ("impl:controlled-v1",),
    knowledge_dependency_refs: Tuple[str, ...] = (),
    origin: str = "OFFICIAL",
) -> CapabilityModuleV1:
    values = dict(
        module_id=module_id,
        capability_purpose=purpose,
        problem_classes=(purpose, "controlled-capability-resolution"),
        origin=origin,
        requirement_class=requirement_class,
        module_version="v1",
        lifecycle_state=lifecycle_state,
        implementation_refs=implementation_refs,
        input_contract_refs=("CapabilityRequirementV1",),
        output_contract_refs=("CapabilityEvidenceCandidateV1",),
        provider_contract_refs=(f"provider-contract:{module_id}",),
        model_asset_refs=(f"model-asset:{module_id}",),
        resource_refs=("resource-profile:controlled",),
        permission_refs=("permission:capability-governance",),
        compatibility_refs=("compatibility:universal-slot-v1",),
        integrity_refs=(f"integrity:{module_id}",),
        provenance_refs=(f"provenance:{module_id}",),
        degradation_policy_refs=(f"degradation:{module_id}",),
        rollback_refs=(f"rollback:{module_id}",),
        self_visibility=f"self:capability:{module_id}",
        knowledge_dependency_refs=knowledge_dependency_refs,
    )
    if origin == "OFFICIAL":
        return OfficialCapabilityModuleV1(**values)
    return CapabilityModuleV1(**values)


def build_modules() -> Tuple[CapabilityModuleV1, ...]:
    return (
        _module("official.safety.environment", "safety_environment_awareness", "MANDATORY_SAFETY"),
        _module("official.system.sensor_health", "visual_sensor_health", "SYSTEM_REQUIRED", lifecycle_state="ACTIVE"),
        _module("official.enhanced_ocr", "enhanced_ocr", "OPTIONAL"),
        _module("official.face_recognition", "face_recognition", "OPTIONAL", lifecycle_state="ACTIVE"),
        _module("official.special_segmentation", "specialized_segmentation", "OPTIONAL", lifecycle_state="INCOMPATIBLE"),
        _module("official.missing_implementation", "missing_implementation", "OPTIONAL", implementation_refs=()),
        _module(
            "official.knowledge_dependent",
            "knowledge_dependent_capability",
            "OPTIONAL",
            knowledge_dependency_refs=("knowledge-ref:future-only",),
        ),
        _module(
            "market.future_module",
            "market_future_capability",
            "OPTIONAL",
            origin="MARKET",
        ),
    )


def _slot(slot_id: str, lifecycle_state: str = "EMPTY") -> UniversalCapabilitySlotV1:
    return UniversalCapabilitySlotV1(
        slot_id=slot_id,
        slot_version="v1",
        lifecycle_state=lifecycle_state,
        current_module_binding=None,
        compatibility_refs=("compatibility:universal-slot-v1",),
        resource_refs=("resource-profile:controlled",),
        permission_refs=("permission:capability-governance",),
        health_refs=(f"health:{slot_id}",),
        provenance_refs=(f"provenance:{slot_id}",),
        history_refs=(),
        recovery_refs=(),
        trace_refs=(f"trace:slot:{slot_id}",),
        self_visibility="EMPTY",
    )


def _admit_and_bind(module: CapabilityModuleV1, slot: UniversalCapabilitySlotV1):
    admission = assess_official_module_admission(module)
    assessment = assess_slot_compatibility(slot, module, admission)
    binding_candidate = build_binding_candidate(slot, module, admission, assessment)
    binding_outcome = govern_binding(slot, module, binding_candidate)
    return admission, assessment, binding_candidate, binding_outcome


def _requirement(requirement_id: str, purpose: str, *, module_id: str | None = None) -> CapabilityRequirementV1:
    return CapabilityRequirementV1(
        requirement_id=requirement_id,
        requested_module_id=module_id,
        purpose=purpose,
        task_context="controlled-foundation-scenario",
        required_semantic_depth="minimum-contract-depth",
        permission_refs=("permission:capability-governance",),
        resource_refs=("resource-profile:controlled",),
        execution_boundary_ref="existing-capability-execution-provider-boundary",
    )


def _case(case_id: str, title: str, passed: bool, details: Dict[str, object]) -> Dict[str, object]:
    return {"case_id": case_id, "title": title, "passed": bool(passed), "details": details}


def build_case_results() -> List[Dict[str, object]]:
    modules = build_modules()
    safety, system, ocr, face, segmentation, missing_impl, knowledge, market = modules
    empty_slot = _slot("slot-001")
    safety_admission, safety_assessment, safety_binding_candidate, safety_binding = _admit_and_bind(safety, empty_slot)
    safety_slot = safety_binding.projected_slot
    system_admission, system_assessment, system_binding_candidate, system_binding = _admit_and_bind(system, _slot("slot-002"))
    system_slot = system_binding.projected_slot
    face_admission, face_assessment, face_binding_candidate, face_binding = _admit_and_bind(face, _slot("slot-003"))
    face_slot = face_binding.projected_slot
    face_unbound = request_slot_lifecycle(face_slot, "UNBOUND", actor="USER_REQUEST", module=face)
    face_recoverable = request_slot_lifecycle(face_slot, "RECOVERABLE", actor="BRAIN_SELF_REGULATION", module=face)
    face_suspended = request_slot_lifecycle(face_slot, "SUSPENDED", actor="BRAIN_SELF_REGULATION", module=face)
    rebound = _admit_and_bind(face, face_unbound.projected_slot)
    degraded_face = replace(face, lifecycle_state="DEGRADED")
    degraded_slot = replace(face_slot, lifecycle_state="DEGRADED", health_refs=face_slot.health_refs + ("health:degraded",))

    safety_requirement = _requirement("req:safety", safety.capability_purpose, module_id=safety.module_id)
    face_requirement = _requirement("req:face", face.capability_purpose, module_id=face.module_id)
    ocr_requirement = _requirement("req:ocr", ocr.capability_purpose, module_id=ocr.module_id)
    degraded_requirement = _requirement("req:degraded", degraded_face.capability_purpose, module_id=degraded_face.module_id)
    visual_requirement = replace(face_requirement, requirement_id="req:visual", execution_boundary_ref="Observation Gateway / FPO")

    safety_resolution = resolve_capability_requirement(safety_requirement, modules, (safety_slot, system_slot, face_slot))
    face_resolution = resolve_capability_requirement(face_requirement, modules, (safety_slot, system_slot, face_slot))
    ocr_resolution = resolve_capability_requirement(ocr_requirement, modules, (safety_slot, system_slot, face_unbound.projected_slot))
    degraded_resolution = resolve_capability_requirement(degraded_requirement, (degraded_face,), (degraded_slot,))
    permission_blocked = resolve_capability_requirement(face_requirement, modules, (face_slot,), permission_granted=False)
    resource_blocked = resolve_capability_requirement(face_requirement, modules, (face_slot,), resource_ready=False)
    missing_resolution = resolve_capability_requirement(_requirement("req:missing", missing_impl.capability_purpose, module_id=missing_impl.module_id), modules, (empty_slot,))
    invocation = build_invocation_candidate(visual_requirement, face_resolution, invocation_id="invoke:visual:001")
    self_current = build_capability_self_view(modules, (safety_slot, system_slot, face_slot))
    self_historical = build_capability_self_view(modules, (face_unbound.projected_slot,), historical_refs=(face.module_id,))
    self_recoverable = build_capability_self_view(modules, (face_recoverable.projected_slot,), historical_refs=(face.module_id,))
    market_admission = assess_official_module_admission(market)
    market_regulation = build_capability_regulation_candidate(
        candidate_id="regulation:market:001",
        action="ACQUIRE",
        module_ref=market.module_id,
        slot_ref=None,
        source="BRAIN_SELF_REGULATION",
        reason="reserved_market_origin_without_market_admission",
    )

    cases = [
        _case("UCS-01", "empty universal slot", empty_slot.lifecycle_state == "EMPTY" and empty_slot.current_module_binding is None and not empty_slot.slot_semantic_authority, {"slot_id": empty_slot.slot_id}),
        _case("UCS-02", "official module admission", safety_admission.accepted and safety_admission.lifecycle_state == "ADMITTED", {"module_id": safety.module_id, "reason": safety_admission.reason}),
        _case("UCS-03", "official module binding", safety_binding.accepted and safety_slot.lifecycle_state == "BOUND" and safety_slot.current_module_binding.module_id == safety.module_id, {"slot_id": safety_slot.slot_id}),
        _case("UCS-04", "slot identity survives unbind", face_unbound.accepted and face_unbound.projected_slot.slot_id == face_slot.slot_id and face_unbound.projected_slot.current_module_binding is None, {"slot_id": face_unbound.projected_slot.slot_id}),
        _case("UCS-05", "module rebind", rebound[3].accepted and rebound[3].projected_slot.slot_id == face_slot.slot_id, {"binding_state": rebound[3].binding_state}),
        _case("UCS-06", "optional module unavailable", ocr_resolution.status == "UNAVAILABLE_CANDIDATE" and ocr_resolution.reason == "MODULE_NOT_BOUND_TO_SLOT", {"reason": ocr_resolution.reason}),
        _case("UCS-07", "optional module available", face_resolution.status == "READY_CANDIDATE" and face_resolution.slot_ref == face_slot.slot_id, {"slot_ref": face_resolution.slot_ref}),
        _case("UCS-08", "system-required module", system.requirement_class == "SYSTEM_REQUIRED" and system_admission.accepted and system_slot.current_module_binding.module_id == system.module_id, {"module_id": system.module_id}),
        _case("UCS-09", "mandatory safety module", safety.requirement_class == "MANDATORY_SAFETY" and safety_binding.accepted, {"requirement_class": safety.requirement_class}),
        _case("UCS-10", "user safety removal rejected", not request_slot_lifecycle(safety_slot, "UNBOUND", actor="USER_REQUEST", module=safety).accepted, {"safety_baseline_bypass": False}),
        _case("UCS-11", "Brain safety removal candidate rejected", not request_slot_lifecycle(safety_slot, "RECOVERABLE", actor="BRAIN_SELF_REGULATION", module=safety).accepted, {"brain_direct_mutation": False}),
        _case("UCS-12", "optional module suspension", face_suspended.accepted and face_suspended.projected_slot.lifecycle_state == "SUSPENDED", {"state": face_suspended.projected_slot.lifecycle_state}),
        _case("UCS-13", "optional module release/unbind", face_unbound.accepted and face_unbound.projected_slot.lifecycle_state == "UNBOUND", {"state": face_unbound.projected_slot.lifecycle_state}),
        _case("UCS-14", "recoverable module", face_recoverable.accepted and face_recoverable.projected_slot.lifecycle_state == "RECOVERABLE" and bool(face_recoverable.projected_slot.recovery_refs), {"recovery_refs": face_recoverable.projected_slot.recovery_refs}),
        _case("UCS-15", "degraded module", degraded_resolution.status == "DEGRADED_CANDIDATE" and degraded_resolution.reason.startswith("CAPABILITY_DEGRADED"), {"status": degraded_resolution.status}),
        _case("UCS-16", "incompatible module", resolve_capability_requirement(_requirement("req:incompatible", segmentation.capability_purpose, module_id=segmentation.module_id), modules, (empty_slot,)).reason == "MODULE_LIFECYCLE_INCOMPATIBLE", {"module_id": segmentation.module_id}),
        _case("UCS-17", "permission blocked", permission_blocked.reason == "PERMISSION_BLOCKED" and permission_blocked.status == "UNAVAILABLE_CANDIDATE", {"reason": permission_blocked.reason}),
        _case("UCS-18", "resource blocked", resource_blocked.reason == "RESOURCE_BLOCKED" and resource_blocked.status == "UNAVAILABLE_CANDIDATE", {"reason": resource_blocked.reason}),
        _case("UCS-19", "implementation missing", not assess_official_module_admission(missing_impl).accepted and missing_resolution.reason == "IMPLEMENTATION_REFERENCE_MISSING", {"reason": missing_resolution.reason}),
        _case("UCS-20", "provider/model dependency reference", face_resolution.model_asset_refs == face.model_asset_refs and face_resolution.provider_contract_refs == face.provider_contract_refs, {"model_refs": face_resolution.model_asset_refs, "provider_refs": face_resolution.provider_contract_refs}),
        _case("UCS-21", "capability ready candidate", safety_resolution.status == "READY_CANDIDATE" and safety_resolution.candidate_only and not safety_resolution.provider_invocation, {"status": safety_resolution.status}),
        _case("UCS-22", "capability unavailable candidate", ocr_resolution.status == "UNAVAILABLE_CANDIDATE" and ocr_resolution.candidate_only, {"status": ocr_resolution.status}),
        _case("UCS-23", "invocation candidate", invocation.accepted and invocation.candidate_only and invocation.execution_boundary_ref == "Observation Gateway / FPO", {"invocation_id": invocation.invocation_id}),
        _case("UCS-24", "no provider execution", not invocation.real_provider_invocation and not invocation.runtime_execution and not invocation.model_inference, {"provider_invocation": False, "runtime_execution": False}),
        _case("UCS-25", "Capability Self current visibility", face.module_id in self_current.current_refs and safety.module_id in self_current.current_refs, {"current_refs": self_current.current_refs}),
        _case("UCS-26", "Capability Self historical visibility", face.module_id in self_historical.historical_refs and face.module_id not in self_historical.current_refs, {"historical_refs": self_historical.historical_refs}),
        _case("UCS-27", "Capability Self recoverable visibility", face.module_id in self_recoverable.recoverable_refs and face.module_id not in self_recoverable.current_refs, {"recoverable_refs": self_recoverable.recoverable_refs}),
        _case("UCS-28", "Market origin deferred", not market_admission.accepted and market_admission.reason == "OFFICIAL_ADMISSION_SCOPE_REJECTED" and market_regulation.candidate_only, {"market_implementation": False}),
        _case("UCS-29", "knowledge remains separate", knowledge.knowledge_dependency_refs and knowledge.module_world_truth_authority is False and not hasattr(knowledge, "knowledge_implementation"), {"knowledge_refs": knowledge.knowledge_dependency_refs}),
        _case("UCS-30", "visual capability remains reference case", invocation.execution_boundary_ref == "Observation Gateway / FPO" and not invocation.observation_gateway_bypass, {"gateway_boundary": invocation.execution_boundary_ref}),
    ]
    return cases


def build_runner_result() -> Dict[str, object]:
    cases = build_case_results()
    failed = [item["case_id"] for item in cases if not item["passed"]]
    return {
        "phase": "Phase-Luna-Brain-Universal-Capability-Slot-Official-Capability-Foundation-Controlled-Implementation-v1-001",
        "mode": "CONTROLLED_CANDIDATE_ONLY",
        "owner": "Capability Registry / Capability Governance",
        "scenario_count": len(cases),
        "all_cases_passed": not failed,
        "failed_case_ids": failed,
        "universal_slot_implemented": True,
        "official_module_supported": True,
        "capability_resolution_supported": True,
        "invocation_candidate_supported": True,
        "capability_self_view_supported": True,
        "brain_regulation_interface_reserved": True,
        "runtime_execution": False,
        "real_provider_invocation": False,
        "model_inference": False,
        "real_download": False,
        "real_install": False,
        "real_activation": False,
        "real_upgrade": False,
        "real_rollback": False,
        "brain_direct_capability_mutation": False,
        "user_direct_capability_mutation": False,
        "safety_baseline_bypass": False,
        "slot_semantic_authority": False,
        "slot_world_truth_authority": False,
        "module_world_truth_authority": False,
        "parallel_capability_registry": False,
        "parallel_model_manager": False,
        "parallel_capability_self_owner": False,
        "specialized_universal_slot": False,
        "learning_execution": False,
        "memory_mutation": False,
        "knowledge_implementation": False,
        "srsk_implementation": False,
        "semantic_folding_execution": False,
        "semantic_expansion_execution": False,
        "market_capability_implementation": False,
        "capability_value_scoring": False,
        "automatic_capability_optimization": False,
        "automatic_capability_uninstall": False,
        "automatic_capability_acquisition": False,
        "candidate_only": True,
        "cases": cases,
    }
