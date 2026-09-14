"""Controlled admission, binding, lifecycle, and Self projection helpers."""

from __future__ import annotations

from dataclasses import replace
from typing import Iterable, Optional

from .universal_capability_slot_types_v1 import (
    CapabilityBindingCandidateV1,
    CapabilityBindingOutcomeV1,
    CapabilityModuleV1,
    CapabilityRegulationCandidateV1,
    CapabilitySelfViewV1,
    ModuleAdmissionCandidateV1,
    ModuleAdmissionOutcomeV1,
    OfficialCapabilityModuleV1,
    SlotCompatibilityAssessmentV1,
    SlotLifecycleCandidateV1,
    SlotModuleBindingV1,
    UniversalCapabilitySlotV1,
    MODULE_LIFECYCLE_STATES,
    ORIGIN_VALUES,
    REGULATION_ACTIONS,
    REQUIREMENT_CLASSES,
    SLOT_BINDING_STATES,
    SLOT_LIFECYCLE_STATES,
)


def build_module_admission_candidate(module: CapabilityModuleV1) -> ModuleAdmissionCandidateV1:
    return ModuleAdmissionCandidateV1(
        module_id=module.module_id,
        origin=module.origin,
        definition_admission_ref=f"admission:definition:{module.module_id}",
        implementation_admission_ref=f"admission:implementation:{module.module_id}",
        model_provider_admission_ref=f"admission:model-provider:{module.module_id}",
        integrity_refs=module.integrity_refs,
        provenance_refs=module.provenance_refs,
    )


def assess_official_module_admission(
    module: CapabilityModuleV1,
    *,
    constitutional_baseline_met: bool = True,
    approved_provider: bool = True,
    resource_ready: bool = True,
    permission_granted: bool = True,
) -> ModuleAdmissionOutcomeV1:
    definition_admitted = (
        module.origin in ORIGIN_VALUES
        and module.requirement_class in REQUIREMENT_CLASSES
        and bool(module.module_id)
        and bool(module.capability_purpose)
        and module.candidate_only
    )
    if module.origin != "OFFICIAL":
        return ModuleAdmissionOutcomeV1(module.module_id, False, False, False, False, "OFFICIAL_ADMISSION_SCOPE_REJECTED", "AVAILABLE")
    if not definition_admitted:
        return ModuleAdmissionOutcomeV1(module.module_id, False, False, False, False, "MODULE_DEFINITION_INVALID", "AVAILABLE")
    if module.requirement_class == "MANDATORY_SAFETY" and not constitutional_baseline_met:
        return ModuleAdmissionOutcomeV1(module.module_id, False, True, False, False, "SAFETY_BASELINE_NOT_MET", "DEGRADED")
    implementation_admitted = bool(
        module.implementation_refs
        and module.input_contract_refs
        and module.output_contract_refs
        and module.integrity_refs
        and module.provenance_refs
        and module.degradation_policy_refs
        and module.rollback_refs
    )
    if not implementation_admitted:
        return ModuleAdmissionOutcomeV1(module.module_id, False, True, False, False, "IMPLEMENTATION_ADMISSION_MISSING", "AVAILABLE")
    model_provider_admitted = bool(module.model_asset_refs and module.provider_contract_refs and approved_provider)
    if not model_provider_admitted:
        return ModuleAdmissionOutcomeV1(module.module_id, False, True, True, False, "MODEL_PROVIDER_ADMISSION_BLOCKED", "AVAILABLE")
    if not resource_ready:
        return ModuleAdmissionOutcomeV1(module.module_id, False, True, True, True, "RESOURCE_ADMISSION_BLOCKED", "AVAILABLE")
    if not permission_granted:
        return ModuleAdmissionOutcomeV1(module.module_id, False, True, True, True, "PERMISSION_ADMISSION_BLOCKED", "AVAILABLE")
    return ModuleAdmissionOutcomeV1(module.module_id, True, True, True, True, "OFFICIAL_MODULE_ADMITTED_CANDIDATE_ONLY", "ADMITTED")


def assess_slot_compatibility(
    slot: UniversalCapabilitySlotV1,
    module: CapabilityModuleV1,
    admission: ModuleAdmissionOutcomeV1,
    *,
    constitutional_baseline_met: bool = True,
) -> SlotCompatibilityAssessmentV1:
    compatible = (
        admission.accepted
        and slot.current_module_binding is None
        and slot.lifecycle_state in {"EMPTY", "UNBOUND", "RECOVERABLE"}
        and bool(slot.compatibility_refs)
        and bool(module.compatibility_refs)
        and not (module.requirement_class == "MANDATORY_SAFETY" and not constitutional_baseline_met)
    )
    reason = "SLOT_MODULE_COMPATIBLE" if compatible else "SLOT_MODULE_COMPATIBILITY_BLOCKED"
    return SlotCompatibilityAssessmentV1(
        slot_id=slot.slot_id,
        module_id=module.module_id,
        compatible=compatible,
        reason=reason,
        compatibility_refs=tuple(dict.fromkeys(slot.compatibility_refs + module.compatibility_refs)),
    )


def build_binding_candidate(
    slot: UniversalCapabilitySlotV1,
    module: CapabilityModuleV1,
    admission: ModuleAdmissionOutcomeV1,
    assessment: SlotCompatibilityAssessmentV1,
) -> CapabilityBindingCandidateV1:
    accepted = admission.accepted and assessment.compatible and slot.current_module_binding is None
    return CapabilityBindingCandidateV1(
        slot_id=slot.slot_id,
        module_id=module.module_id,
        admission_ref=f"admission:{module.module_id}",
        compatibility_assessment_ref=f"compatibility:{slot.slot_id}:{module.module_id}",
        binding_state="BINDING_CANDIDATE" if accepted else "EMPTY",
    )


def govern_binding(
    slot: UniversalCapabilitySlotV1,
    module: CapabilityModuleV1,
    binding_candidate: CapabilityBindingCandidateV1,
) -> CapabilityBindingOutcomeV1:
    accepted = (
        binding_candidate.binding_state == "BINDING_CANDIDATE"
        and slot.current_module_binding is None
        and module.origin == "OFFICIAL"
    )
    if not accepted:
        return CapabilityBindingOutcomeV1(
            slot_id=slot.slot_id,
            module_id=module.module_id,
            accepted=False,
            reason="BINDING_CANDIDATE_REJECTED",
            binding_state="EMPTY",
            projected_slot=slot,
        )
    binding = SlotModuleBindingV1(
        slot_id=slot.slot_id,
        module_id=module.module_id,
        module_version=module.module_version,
        binding_state="BOUND",
        admission_ref=binding_candidate.admission_ref,
        compatibility_assessment_ref=binding_candidate.compatibility_assessment_ref,
        implementation_refs=module.implementation_refs,
        trace_ref=f"trace:binding:{slot.slot_id}:{module.module_id}",
        provenance_refs=module.provenance_refs,
    )
    projected = replace(
        slot,
        lifecycle_state="BOUND",
        current_module_binding=binding,
        trace_refs=slot.trace_refs + (binding.trace_ref,),
        provenance_refs=tuple(dict.fromkeys(slot.provenance_refs + module.provenance_refs)),
        self_visibility=f"CURRENT:{module.module_id}",
    )
    return CapabilityBindingOutcomeV1(
        slot_id=slot.slot_id,
        module_id=module.module_id,
        accepted=True,
        reason="GOVERNED_BINDING_RESULT_CANDIDATE_ONLY",
        binding_state="BOUND",
        projected_slot=projected,
    )


def request_slot_lifecycle(
    slot: UniversalCapabilitySlotV1,
    requested_state: str,
    *,
    actor: str,
    module: Optional[CapabilityModuleV1] = None,
) -> SlotLifecycleCandidateV1:
    module_is_safety = bool(module and module.requirement_class == "MANDATORY_SAFETY")
    safety_forbidden = module_is_safety and requested_state in {"EMPTY", "UNBOUND", "RECOVERABLE", "RETIRED"}
    valid = requested_state in SLOT_LIFECYCLE_STATES
    accepted = valid and not safety_forbidden and slot.current_module_binding is not None
    if not valid:
        reason = "UNKNOWN_SLOT_LIFECYCLE_STATE"
    elif safety_forbidden:
        reason = "SAFETY_BASELINE_PROTECTED"
    elif not slot.current_module_binding:
        reason = "NO_ACTIVE_BINDING_FOR_TRANSITION"
    else:
        reason = "CONTROLLED_SLOT_LIFECYCLE_CANDIDATE"
    projected = slot
    if accepted:
        history = slot.history_refs
        binding = slot.current_module_binding
        if requested_state in {"UNBOUND", "RECOVERABLE"} and binding is not None:
            history = history + (f"binding-history:{binding.module_id}:{binding.module_version}",)
            projected = replace(
                slot,
                lifecycle_state=requested_state,
                current_module_binding=None,
                history_refs=history,
                self_visibility=f"{requested_state}:{binding.module_id}",
                recovery_refs=slot.recovery_refs + (f"recovery:{binding.module_id}",),
                trace_refs=slot.trace_refs + (f"trace:slot:{slot.slot_id}:{requested_state}",),
            )
        else:
            projected = replace(
                slot,
                lifecycle_state=requested_state,
                self_visibility=f"{requested_state}:{binding.module_id if binding else slot.slot_id}",
                trace_refs=slot.trace_refs + (f"trace:slot:{slot.slot_id}:{requested_state}",),
            )
    return SlotLifecycleCandidateV1(
        slot_id=slot.slot_id,
        requested_state=requested_state,
        accepted=accepted,
        actor=actor,
        reason=reason,
        projected_slot=projected,
    )


def build_capability_self_view(
    modules: Iterable[CapabilityModuleV1],
    slots: Iterable[UniversalCapabilitySlotV1],
    *,
    historical_refs: Iterable[str] = (),
    usage_profile_refs: Iterable[str] = (),
    weakness_candidate_refs: Iterable[str] = (),
    feedback_refs: Iterable[str] = (),
) -> CapabilitySelfViewV1:
    slot_list = tuple(slots)
    module_list = tuple(modules)
    current = []
    unavailable = []
    degraded = []
    suspended = []
    recoverable = []
    potential = []
    historical = list(historical_refs)
    for module in module_list:
        matching = tuple(
            slot for slot in slot_list
            if slot.current_module_binding and slot.current_module_binding.module_id == module.module_id
        )
        if any(slot.lifecycle_state == "DEGRADED" or module.lifecycle_state == "DEGRADED" for slot in matching):
            degraded.append(module.module_id)
        elif any(slot.lifecycle_state == "SUSPENDED" for slot in matching):
            suspended.append(module.module_id)
        elif any(slot.lifecycle_state == "BOUND" for slot in matching):
            current.append(module.module_id)
        elif any(module.module_id in slot.history_refs for slot in slot_list) or module.module_id in historical:
            historical.append(module.module_id)
            recoverable.append(module.module_id)
        elif module.lifecycle_state == "AVAILABLE":
            potential.append(module.module_id)
        else:
            unavailable.append(module.module_id)
    return CapabilitySelfViewV1(
        current_refs=tuple(dict.fromkeys(current)),
        unavailable_refs=tuple(dict.fromkeys(unavailable)),
        degraded_refs=tuple(dict.fromkeys(degraded)),
        suspended_refs=tuple(dict.fromkeys(suspended)),
        recoverable_refs=tuple(dict.fromkeys(recoverable)),
        historical_refs=tuple(dict.fromkeys(historical)),
        potential_refs=tuple(dict.fromkeys(potential)),
        provenance_refs=tuple(
            dict.fromkeys(
                ref
                for module in module_list
                for ref in module.provenance_refs
            )
        ),
        semantic_annotation_refs=tuple(
            dict.fromkeys(
                module.capability_semantic_annotation_ref
                for module in module_list
                if module.capability_semantic_annotation_ref
            )
        ),
        scope_problem_class_refs=tuple(
            dict.fromkeys(
                problem_class
                for module in module_list
                for problem_class in module.problem_classes
            )
        ),
        scope_operation_refs=tuple(
            dict.fromkeys(
                operation
                for module in module_list
                for operation in module.supported_operation_refs
            )
        ),
        scope_boundary_refs=tuple(
            dict.fromkeys(
                boundary
                for module in module_list
                for boundary in module.explicit_boundary_refs
            )
        ),
        usage_profile_refs=tuple(dict.fromkeys(usage_profile_refs)),
        weakness_candidate_refs=tuple(dict.fromkeys(weakness_candidate_refs)),
        feedback_refs=tuple(dict.fromkeys(feedback_refs)),
    )


def build_capability_regulation_candidate(
    *,
    candidate_id: str,
    action: str,
    module_ref: str,
    slot_ref: Optional[str],
    source: str,
    reason: str,
) -> CapabilityRegulationCandidateV1:
    if action not in REGULATION_ACTIONS:
        raise ValueError(f"unsupported capability regulation action: {action}")
    return CapabilityRegulationCandidateV1(
        candidate_id=candidate_id,
        action=action,
        module_ref=module_ref,
        slot_ref=slot_ref,
        source=source,
        reason=reason,
        governance_handoff_ref=f"capability-governance:{candidate_id}",
    )
