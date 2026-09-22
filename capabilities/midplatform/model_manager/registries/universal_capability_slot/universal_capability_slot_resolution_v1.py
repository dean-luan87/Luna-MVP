"""Controlled capability resolution and invocation handoff candidates."""

from __future__ import annotations

import hashlib
from typing import Iterable, Optional, Tuple

from .universal_capability_slot_types_v1 import (
    CapabilityInvocationCandidateV1,
    CapabilityGapCandidateV1,
    CapabilityModuleV1,
    CapabilityRequirementV1,
    CapabilityResolutionCandidateV1,
    CapabilityScopeAssessmentV1,
    UniversalCapabilitySlotV1,
    CapabilityRuntimeAdmissionResultV1,
    CapabilityRuntimeEvaluationProfileV1,
)
from .official_capability_catalog_governance_v1 import (
    CONTROLLED_CAPABILITY_EVALUATION_PROFILE_REF,
    build_controlled_capability_runtime_evaluation_profile_v1,
    build_official_capability_catalog,
)


SCOPE_RESULTS = (
    "IN_SCOPE",
    "OUT_OF_CAPABILITY_SCOPE",
    "INPUT_CONTRACT_UNSUPPORTED",
    "OUTPUT_CONTRACT_UNSUPPORTED",
    "OPERATION_UNSUPPORTED",
    "AUTHORITY_NOT_ALLOWED",
    "PROBLEM_CLASS_UNSUPPORTED",
)

CAPABILITY_CATALOG_REF = "luna-official-capability-catalog"
CAPABILITY_CATALOG_VERSION = "v1"
PRODUCTION_CAPABILITY_EVALUATION_PROFILE_REF = "capability-runtime-profile:production-canonical"
CANONICAL_RUNTIME_SCOPE_BINDING_KEY_LENGTH = 7
CANONICAL_RUNTIME_SCOPE_BINDING_KEY_PREFIX = "runtime-scope:v2"


def _match_module(
    requirement: CapabilityRequirementV1,
    modules: Iterable[CapabilityModuleV1],
) -> Optional[CapabilityModuleV1]:
    module_list = tuple(modules)
    if requirement.requested_module_id:
        return next((item for item in module_list if item.module_id == requirement.requested_module_id), None)
    return next(
        (
            item for item in module_list
            if item.capability_purpose == requirement.purpose
            or requirement.purpose in item.problem_classes
        ),
        None,
    )


def _bound_slot(module_id: str, slots: Iterable[UniversalCapabilitySlotV1]) -> Optional[UniversalCapabilitySlotV1]:
    return next(
        (
            slot for slot in slots
            if slot.current_module_binding
            and slot.current_module_binding.module_id == module_id
        ),
        None,
    )


def resolve_capability_requirement(
    requirement: CapabilityRequirementV1,
    modules: Iterable[CapabilityModuleV1],
    slots: Iterable[UniversalCapabilitySlotV1],
    *,
    resource_ready: bool = True,
    permission_granted: bool = True,
) -> CapabilityResolutionCandidateV1:
    module = _match_module(requirement, modules)
    if module is None:
        return CapabilityResolutionCandidateV1(
            requirement_id=requirement.requirement_id,
            status="UNAVAILABLE_CANDIDATE",
            module_ref=None,
            slot_ref=None,
            implementation_refs=(),
            model_asset_refs=(),
            provider_contract_refs=(),
            reason="CAPABILITY_MODULE_NOT_REGISTERED",
            recovery_available=False,
        )
    if module.lifecycle_state in {"INCOMPATIBLE", "RETIRED", "UNAVAILABLE"}:
        return CapabilityResolutionCandidateV1(
            requirement_id=requirement.requirement_id,
            status="UNAVAILABLE_CANDIDATE",
            module_ref=module.module_id,
            slot_ref=None,
            implementation_refs=module.implementation_refs,
            model_asset_refs=module.model_asset_refs,
            provider_contract_refs=module.provider_contract_refs,
            reason=f"MODULE_LIFECYCLE_{module.lifecycle_state}",
            recovery_available=module.lifecycle_state in {"INCOMPATIBLE", "UNAVAILABLE"},
        )
    if not module.implementation_refs:
        return CapabilityResolutionCandidateV1(
            requirement_id=requirement.requirement_id,
            status="UNAVAILABLE_CANDIDATE",
            module_ref=module.module_id,
            slot_ref=None,
            implementation_refs=(),
            model_asset_refs=module.model_asset_refs,
            provider_contract_refs=module.provider_contract_refs,
            reason="IMPLEMENTATION_REFERENCE_MISSING",
            recovery_available=False,
        )
    slot = _bound_slot(module.module_id, slots)
    if slot is None:
        return CapabilityResolutionCandidateV1(
            requirement_id=requirement.requirement_id,
            status="UNAVAILABLE_CANDIDATE",
            module_ref=module.module_id,
            slot_ref=None,
            implementation_refs=module.implementation_refs,
            model_asset_refs=module.model_asset_refs,
            provider_contract_refs=module.provider_contract_refs,
            reason="MODULE_NOT_BOUND_TO_SLOT",
            recovery_available=module.lifecycle_state in {"AVAILABLE", "ADMITTED", "RECOVERABLE"},
        )
    if not permission_granted:
        reason = "PERMISSION_BLOCKED"
        status = "UNAVAILABLE_CANDIDATE"
    elif not resource_ready:
        reason = "RESOURCE_BLOCKED"
        status = "UNAVAILABLE_CANDIDATE"
    elif slot.lifecycle_state == "SUSPENDED" or module.lifecycle_state == "SUSPENDED":
        reason = "CAPABILITY_SUSPENDED"
        status = "UNAVAILABLE_CANDIDATE"
    elif slot.lifecycle_state == "DEGRADED" or module.lifecycle_state == "DEGRADED":
        reason = "CAPABILITY_DEGRADED_REQUIRES_GOVERNED_USE"
        status = "DEGRADED_CANDIDATE"
    elif slot.lifecycle_state != "BOUND":
        reason = f"SLOT_LIFECYCLE_{slot.lifecycle_state}"
        status = "UNAVAILABLE_CANDIDATE"
    else:
        reason = "CAPABILITY_READY_CONTROLLED_DEPENDENCY_RESOLUTION"
        status = "READY_CANDIDATE"
    return CapabilityResolutionCandidateV1(
        requirement_id=requirement.requirement_id,
        status=status,
        module_ref=module.module_id,
        slot_ref=slot.slot_id,
        implementation_refs=module.implementation_refs,
        model_asset_refs=module.model_asset_refs,
        provider_contract_refs=module.provider_contract_refs,
        reason=reason,
        recovery_available=bool(slot.recovery_refs) or module.lifecycle_state == "RECOVERABLE",
    )


def assess_capability_scope(
    requirement: CapabilityRequirementV1,
    module: Optional[CapabilityModuleV1],
) -> CapabilityScopeAssessmentV1:
    """Validate a structured requirement against the admitted Module scope."""
    if module is None:
        return CapabilityScopeAssessmentV1(
            requirement_ref=requirement.requirement_id,
            module_ref=None,
            scope_result="PROBLEM_CLASS_UNSUPPORTED",
            in_scope=False,
            problem_class_supported=False,
            operation_supported=False,
            input_contract_supported=False,
            output_contract_supported=False,
            authority_supported=False,
            boundary_violation_refs=("boundary:module-not-found",),
            unmet_requirement_refs=("module_ref",),
            reason="CAPABILITY_MODULE_NOT_REGISTERED",
        )
    problem_class = requirement.problem_class or requirement.purpose
    problem_supported = problem_class in module.problem_classes
    operation_supported = bool(requirement.requested_operation) and requirement.requested_operation in module.supported_operation_refs
    input_supported = bool(requirement.input_contract_ref) and requirement.input_contract_ref in module.accepted_input_contract_refs
    output_supported = bool(requirement.expected_output_contract_ref) and requirement.expected_output_contract_ref in module.produced_output_contract_refs
    authority_supported = requirement.required_authority in module.authority_boundary_refs
    requirement_type_supported = requirement.requirement_type in module.accepted_requirement_types
    boundary_refs = []
    unmet_refs = []
    if not problem_supported:
        unmet_refs.append("problem_class")
        boundary_refs.append("boundary:problem-class")
    if not requirement_type_supported:
        unmet_refs.append("requirement_type")
        boundary_refs.append("boundary:requirement-type")
    if not operation_supported:
        unmet_refs.append("requested_operation")
        boundary_refs.append("boundary:operation")
    if not input_supported:
        unmet_refs.append("input_contract_ref")
        boundary_refs.append("boundary:input-contract")
    if not output_supported:
        unmet_refs.append("expected_output_contract_ref")
        boundary_refs.append("boundary:output-contract")
    if not authority_supported:
        unmet_refs.append("required_authority")
        boundary_refs.extend(module.authority_boundary_refs or ("boundary:authority",))
    if not unmet_refs:
        result = "IN_SCOPE"
        reason = "CAPABILITY_REQUIREMENT_WITHIN_MODULE_SCOPE"
    elif not problem_supported:
        result = "PROBLEM_CLASS_UNSUPPORTED"
        reason = "PROBLEM_CLASS_OUTSIDE_MODULE_SCOPE"
    elif not operation_supported:
        result = "OPERATION_UNSUPPORTED"
        reason = "OPERATION_OUTSIDE_MODULE_SCOPE"
    elif not input_supported:
        result = "INPUT_CONTRACT_UNSUPPORTED"
        reason = "INPUT_CONTRACT_OUTSIDE_MODULE_SCOPE"
    elif not output_supported:
        result = "OUTPUT_CONTRACT_UNSUPPORTED"
        reason = "OUTPUT_CONTRACT_OUTSIDE_MODULE_SCOPE"
    elif not authority_supported:
        result = "AUTHORITY_NOT_ALLOWED"
        reason = "REQUIRED_AUTHORITY_OUTSIDE_MODULE_SCOPE"
    else:
        result = "OUT_OF_CAPABILITY_SCOPE"
        reason = "REQUIREMENT_TYPE_OUTSIDE_MODULE_SCOPE"
    return CapabilityScopeAssessmentV1(
        requirement_ref=requirement.requirement_id,
        module_ref=module.module_id,
        scope_result=result,
        in_scope=not unmet_refs,
        problem_class_supported=problem_supported,
        operation_supported=operation_supported,
        input_contract_supported=input_supported,
        output_contract_supported=output_supported,
        authority_supported=authority_supported,
        boundary_violation_refs=tuple(dict.fromkeys(boundary_refs)),
        unmet_requirement_refs=tuple(dict.fromkeys(unmet_refs)),
        reason=reason,
    )


def build_capability_gap_candidate(
    requirement: CapabilityRequirementV1,
    assessment: CapabilityScopeAssessmentV1,
    *,
    rejected_module_refs: Iterable[str] = (),
) -> CapabilityGapCandidateV1:
    return CapabilityGapCandidateV1(
        gap_id=f"gap:{requirement.requirement_id}",
        originating_requirement_ref=requirement.requirement_id,
        rejected_module_refs=tuple(rejected_module_refs),
        unmet_problem_class=requirement.problem_class or requirement.purpose,
        unmet_operation=requirement.requested_operation,
        unmet_contract_refs=assessment.unmet_requirement_refs,
        reason=assessment.reason,
    )


def resolve_scoped_capability_requirement(
    requirement: CapabilityRequirementV1,
    modules: Iterable[CapabilityModuleV1],
    slots: Iterable[UniversalCapabilitySlotV1],
    *,
    resource_ready: bool = True,
    permission_granted: bool = True,
) -> Tuple[CapabilityScopeAssessmentV1, CapabilityResolutionCandidateV1, Optional[CapabilityGapCandidateV1]]:
    """Run scope validation before the existing admission/readiness resolver."""
    module = _match_module(requirement, modules)
    assessment = assess_capability_scope(requirement, module)
    if not assessment.in_scope:
        gap = build_capability_gap_candidate(
            requirement,
            assessment,
            rejected_module_refs=(module.module_id,) if module else (),
        )
        return assessment, CapabilityResolutionCandidateV1(
            requirement_id=requirement.requirement_id,
            status="UNAVAILABLE_CANDIDATE",
            module_ref=module.module_id if module else None,
            slot_ref=None,
            implementation_refs=module.implementation_refs if module else (),
            model_asset_refs=module.model_asset_refs if module else (),
            provider_contract_refs=module.provider_contract_refs if module else (),
            reason=assessment.reason,
            recovery_available=False,
            scope_assessment_ref=f"scope:{requirement.requirement_id}",
            capability_gap_ref=gap.gap_id,
        ), gap
    resolution = resolve_capability_requirement(
        requirement,
        modules,
        slots,
        resource_ready=resource_ready,
        permission_granted=permission_granted,
    )
    return assessment, CapabilityResolutionCandidateV1(
        requirement_id=resolution.requirement_id,
        status=resolution.status,
        module_ref=resolution.module_ref,
        slot_ref=resolution.slot_ref,
        implementation_refs=resolution.implementation_refs,
        model_asset_refs=resolution.model_asset_refs,
        provider_contract_refs=resolution.provider_contract_refs,
        reason=resolution.reason,
        recovery_available=resolution.recovery_available,
        provider_invocation=resolution.provider_invocation,
        model_inference=resolution.model_inference,
        scope_assessment_ref=f"scope:{requirement.requirement_id}",
    ), None


def build_invocation_candidate(
    requirement: CapabilityRequirementV1,
    resolution: CapabilityResolutionCandidateV1,
    *,
    invocation_id: str,
) -> CapabilityInvocationCandidateV1:
    accepted = resolution.status in {"READY_CANDIDATE", "DEGRADED_CANDIDATE"}
    return CapabilityInvocationCandidateV1(
        invocation_id=invocation_id,
        requirement_ref=requirement.requirement_id,
        module_ref=resolution.module_ref,
        slot_ref=resolution.slot_ref,
        execution_boundary_ref=requirement.execution_boundary_ref,
        accepted=accepted,
        reason="INVOCATION_HANDOFF_CANDIDATE" if accepted else "INVOCATION_BLOCKED_BY_RESOLUTION",
    )


def build_scoped_invocation_candidate(
    requirement: CapabilityRequirementV1,
    scope_assessment: CapabilityScopeAssessmentV1,
    resolution: CapabilityResolutionCandidateV1,
    *,
    invocation_id: str,
    module: Optional[CapabilityModuleV1] = None,
    gateway_refs: Iterable[str] = (),
    trace_refs: Iterable[str] = (),
) -> CapabilityInvocationCandidateV1:
    """Create a ready handoff only after scope and readiness are both valid."""
    accepted = scope_assessment.in_scope and resolution.status == "READY_CANDIDATE"
    return CapabilityInvocationCandidateV1(
        invocation_id=invocation_id,
        requirement_ref=requirement.requirement_id,
        module_ref=resolution.module_ref,
        slot_ref=resolution.slot_ref,
        execution_boundary_ref=requirement.execution_boundary_ref,
        accepted=accepted,
        reason="SCOPED_READY_INVOCATION_HANDOFF_CANDIDATE" if accepted else "INVOCATION_BLOCKED_BY_SCOPE_OR_READINESS",
        scope_assessment_ref=f"scope:{requirement.requirement_id}",
        implementation_refs=module.implementation_refs if module else resolution.implementation_refs,
        model_asset_refs=module.model_asset_refs if module else resolution.model_asset_refs,
        provider_contract_refs=module.provider_contract_refs if module else resolution.provider_contract_refs,
        gateway_refs=tuple(gateway_refs),
        trace_refs=tuple(trace_refs),
    )


def evaluate_runtime_capability_admission_v1(
    *,
    binding_key: Tuple[str, ...],
    capability_candidate_ref: str,
    provider_candidate_ref: str,
    execution_instance_preparation_candidate_ref: str,
    profile_ref: object = PRODUCTION_CAPABILITY_EVALUATION_PROFILE_REF,
) -> CapabilityRuntimeAdmissionResultV1:
    """Resolve capability admission from an owner-defined current profile."""

    profile = resolve_capability_runtime_evaluation_profile_v1(profile_ref)
    if profile is None:
        return CapabilityRuntimeAdmissionResultV1(
            result_ref="",
            binding_key=tuple(binding_key),
            capability_candidate_ref=capability_candidate_ref,
            provider_candidate_ref=provider_candidate_ref,
            execution_instance_preparation_candidate_ref=execution_instance_preparation_candidate_ref,
            status="DENIED",
            reason="capability_evaluation_profile_invalid",
            catalog_ref="capability-runtime-evaluation-profiles",
            catalog_version="v1",
            evaluation_profile_ref="",
        )

    digest = hashlib.sha256(
        "|".join(
            (
                *binding_key,
                capability_candidate_ref,
                provider_candidate_ref,
                profile.profile_ref,
                profile.catalog_version,
            )
        ).encode("utf-8")
    ).hexdigest()[:24]
    result_ref = f"capability-runtime-admission:{digest}"
    valid_binding = (
        len(binding_key) == CANONICAL_RUNTIME_SCOPE_BINDING_KEY_LENGTH
        and binding_key[0] == CANONICAL_RUNTIME_SCOPE_BINDING_KEY_PREFIX
        and all(binding_key)
    )
    admitted = valid_binding and capability_candidate_ref in profile.capability_refs
    return CapabilityRuntimeAdmissionResultV1(
        result_ref=result_ref if valid_binding else "",
        binding_key=tuple(binding_key),
        capability_candidate_ref=capability_candidate_ref,
        provider_candidate_ref=provider_candidate_ref,
        execution_instance_preparation_candidate_ref=execution_instance_preparation_candidate_ref,
        status="ADMITTED" if admitted else "DENIED",
        reason="current_capability_profile_match" if admitted else "capability_not_registered_in_selected_profile",
        catalog_ref=profile.catalog_ref,
        catalog_version=profile.catalog_version,
        evaluation_profile_ref=profile.profile_ref,
    )


def resolve_capability_runtime_evaluation_profile_v1(
    profile_ref: object = PRODUCTION_CAPABILITY_EVALUATION_PROFILE_REF,
) -> CapabilityRuntimeEvaluationProfileV1 | None:
    if not isinstance(profile_ref, str) or not profile_ref.strip():
        return None
    if profile_ref == CONTROLLED_CAPABILITY_EVALUATION_PROFILE_REF:
        return build_controlled_capability_runtime_evaluation_profile_v1()
    if profile_ref != PRODUCTION_CAPABILITY_EVALUATION_PROFILE_REF:
        return None
    catalog = build_official_capability_catalog()
    return CapabilityRuntimeEvaluationProfileV1(
        profile_ref=PRODUCTION_CAPABILITY_EVALUATION_PROFILE_REF,
        owner_ref="Capability Admission Governance",
        catalog_ref=CAPABILITY_CATALOG_REF,
        catalog_version=CAPABILITY_CATALOG_VERSION,
        capability_refs=tuple(entry.module_ref for entry in catalog.entries),
        provenance_refs=("provenance:capability-runtime-governance:production",),
        production_canonical=True,
    )
