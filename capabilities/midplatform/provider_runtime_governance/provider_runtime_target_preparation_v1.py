"""Candidate-only preparation of governed Provider runtime targets.

This module belongs to the Provider Governance boundary.  It projects an
FPO admission-compatibility candidate through an explicit, read-only provider
mapping.  It does not bind a provider, create a runtime identity, reserve a
slot, or invoke a runtime.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Iterable, Optional, Tuple

from capabilities.midplatform.field_perception_orchestrator.integration.perception_routing_admission_compatibility_v1 import (
    PerceptionRoutingAdmissionCompatibilityCandidateV1,
)


OWNER = "Provider Governance"
SUPPORTED_AVAILABILITY_STATUSES = ("AVAILABLE", "UNAVAILABLE", "DEGRADED", "UNKNOWN")
SUPPORTED_ADMISSION_STATUSES = ("ADMITTED", "NOT_ADMITTED")
FORMATION_STATUSES = (
    "PROVIDER_TARGET_CANDIDATES_FORMED",
    "NO_PROVIDER_TARGET_CANDIDATE",
    "NO_PROVIDER_MAPPING",
    "NO_MATCHING_PROVIDER",
    "PROVIDER_UNAVAILABLE",
    "PROVIDER_NOT_ADMITTED",
    "PROVIDER_TARGET_COMPATIBILITY_GAP",
    "INVALID_INPUT",
)


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


@dataclass(frozen=True)
class GovernedProviderRuntimeTargetMappingV1:
    """Explicit controlled mapping, not a provider-selection result."""

    mapping_ref: str
    source_admission_compatibility_candidate_ref: str
    capability_class_ref: str
    provider_candidate_ref: str
    provider_class_ref: str
    provider_mapping_basis_refs: Tuple[str, ...]
    provider_admission_refs: Tuple[str, ...]
    provider_availability_refs: Tuple[str, ...]
    availability_status: str
    admission_status: str
    eligible: bool
    source_model_ref: Optional[str] = None
    candidate_only: bool = True
    read_only: bool = True


@dataclass(frozen=True)
class ProviderRuntimeTargetPreparationCandidateV1:
    """One future-runtime target candidate; never a binding."""

    provider_target_candidate_ref: str
    source_admission_compatibility_candidate_ref: str
    source_perception_routing_candidate_ref: str
    source_observation_demand_ref: str
    source_capability_requirement_ref: str
    source_capability_resolution_candidate_ref: str
    capability_candidate_ref: str
    capability_class_ref: str
    provider_candidate_ref: str
    provider_class_ref: str
    source_model_ref: Optional[str]
    provider_mapping_basis_refs: Tuple[str, ...]
    provider_admission_refs: Tuple[str, ...]
    provider_availability_refs: Tuple[str, ...]
    observation_class: str
    observation_target_refs: Tuple[str, ...]
    observation_constraint_refs: Tuple[str, ...]
    expected_information_contribution_refs: Tuple[str, ...]
    information_need_refs: Tuple[str, ...]
    information_gap_refs: Tuple[str, ...]
    source_strategy_ref: str
    source_branch_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    context_refs: Tuple[str, ...]
    lineage_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    owner_ref: str = OWNER
    candidate_only: bool = True
    read_only: bool = True
    truth_declared: bool = False
    world_truth_declared: bool = False
    provider_binding: bool = False
    model_binding: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    execution_instance_created: bool = False
    provider_session_started: bool = False
    runtime_admission_requested: bool = False
    runtime_admission_executed: bool = False
    gateway_submission: bool = False
    capability_activation: bool = False
    capability_reservation: bool = False
    slot_reservation: bool = False
    resource_scheduling: bool = False
    observation_execution: bool = False
    admitted_action_ref: Optional[str] = None
    working_envelope_ref: Optional[str] = None
    working_envelope_version_ref: Optional[str] = None


@dataclass(frozen=True)
class ProviderRuntimeTargetPreparationInputV1:
    preparation_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    compatibility_candidates: Tuple[
        PerceptionRoutingAdmissionCompatibilityCandidateV1, ...
    ] = field(default_factory=tuple)
    provider_mappings: Tuple[GovernedProviderRuntimeTargetMappingV1, ...] = field(
        default_factory=tuple
    )
    context_refs: Tuple[str, ...] = field(default_factory=tuple)
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
    admitted_action_ref: Optional[str] = None
    working_envelope_ref: Optional[str] = None
    working_envelope_version_ref: Optional[str] = None


@dataclass(frozen=True)
class ProviderRuntimeTargetPreparationResultV1:
    preparation_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    formation_status: str
    input_compatibility_candidate_refs: Tuple[str, ...]
    input_provider_mapping_refs: Tuple[str, ...]
    provider_target_candidate_refs: Tuple[str, ...]
    targets: Tuple[ProviderRuntimeTargetPreparationCandidateV1, ...]
    excluded_compatibility_candidate_refs: Tuple[str, ...]
    owner_ref: str
    context_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    read_only: bool = True
    provider_binding: bool = False
    model_binding: bool = False
    execution_instance_created: bool = False
    provider_session_started: bool = False
    runtime_admission_requested: bool = False
    runtime_admission_executed: bool = False
    gateway_submission: bool = False
    capability_activation: bool = False
    capability_reservation: bool = False
    slot_reservation: bool = False
    resource_scheduling: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    observation_execution: bool = False
    truth_declared: bool = False
    world_truth_declared: bool = False
    validation_errors: Tuple[str, ...] = ()
    admitted_action_ref: Optional[str] = None
    working_envelope_ref: Optional[str] = None
    working_envelope_version_ref: Optional[str] = None


def _candidate_ref(preparation_ref: str, compatibility_ref: str, provider_ref: str, mapping_ref: str) -> str:
    key = f"{preparation_ref}|{compatibility_ref}|{provider_ref}|{mapping_ref}"
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:24]
    return f"provider-runtime-target:candidate:{digest}"


def _compatibility_refs(
    value: object,
) -> Tuple[str, ...]:
    if not isinstance(value, tuple):
        return ()
    return tuple(
        item.admission_compatibility_candidate_ref
        for item in value
        if isinstance(item, PerceptionRoutingAdmissionCompatibilityCandidateV1)
    )


def _mapping_refs(value: object) -> Tuple[str, ...]:
    if not isinstance(value, tuple):
        return ()
    return tuple(
        item.mapping_ref
        for item in value
        if isinstance(item, GovernedProviderRuntimeTargetMappingV1)
    )


def _result(
    request: ProviderRuntimeTargetPreparationInputV1,
    status: str,
    compatibility_refs: Tuple[str, ...],
    mapping_refs: Tuple[str, ...],
    targets: Tuple[ProviderRuntimeTargetPreparationCandidateV1, ...],
    errors: Tuple[str, ...] = (),
) -> ProviderRuntimeTargetPreparationResultV1:
    target_sources = {item.source_admission_compatibility_candidate_ref for item in targets}
    preparation_ref = getattr(request, "preparation_ref", "")
    parent_problem_ref = getattr(request, "parent_cognitive_problem_ref", "")
    source_state_ref = getattr(request, "source_state_ref", "")
    context_refs = getattr(request, "context_refs", ())
    request_provenance_refs = getattr(request, "provenance_refs", ())
    request_trace_ref = getattr(request, "trace_ref", "")
    return ProviderRuntimeTargetPreparationResultV1(
        preparation_ref=preparation_ref,
        parent_cognitive_problem_ref=parent_problem_ref,
        source_state_ref=source_state_ref,
        formation_status=status,
        input_compatibility_candidate_refs=compatibility_refs,
        input_provider_mapping_refs=mapping_refs,
        provider_target_candidate_refs=tuple(item.provider_target_candidate_ref for item in targets),
        targets=targets,
        excluded_compatibility_candidate_refs=tuple(
            ref for ref in compatibility_refs if ref not in target_sources
        ),
        owner_ref=OWNER,
        context_refs=context_refs,
        provenance_refs=_unique(
            ("provenance:provider-runtime-target-preparation:v1", *request_provenance_refs)
        ),
        trace_ref=request_trace_ref or f"trace:{preparation_ref}",
        validation_errors=errors,
        admitted_action_ref=getattr(request, "admitted_action_ref", None),
        working_envelope_ref=getattr(request, "working_envelope_ref", None),
        working_envelope_version_ref=getattr(
            request, "working_envelope_version_ref", None
        ),
    )


def _validate(request: ProviderRuntimeTargetPreparationInputV1) -> Tuple[str, ...]:
    errors = []
    if not isinstance(request, ProviderRuntimeTargetPreparationInputV1):
        return ("request_type_invalid",)
    if not request.preparation_ref:
        errors.append("preparation_ref_missing")
    if not request.trace_ref:
        errors.append("trace_ref_missing")
    if not request.candidate_only:
        errors.append("preparation_not_candidate_only")
    canonical_scope = (
        request.admitted_action_ref,
        request.working_envelope_ref,
        request.working_envelope_version_ref,
    )
    if any(value is not None for value in canonical_scope) and not all(
        isinstance(value, str) and value.strip() for value in canonical_scope
    ):
        errors.append("canonical_runtime_scope_incomplete")
    if not isinstance(request.compatibility_candidates, tuple):
        errors.append("compatibility_candidates_must_be_tuple")
    if not isinstance(request.provider_mappings, tuple):
        errors.append("provider_mappings_must_be_tuple")
    if errors:
        return tuple(dict.fromkeys(errors))

    compatibility_refs = _compatibility_refs(request.compatibility_candidates)
    if len(set(compatibility_refs)) != len(compatibility_refs):
        errors.append("duplicate_compatibility_candidate_ref")
    for item in request.compatibility_candidates:
        if not isinstance(item, PerceptionRoutingAdmissionCompatibilityCandidateV1):
            errors.append("invalid_compatibility_candidate_type")
            continue
        required = (
            item.admission_compatibility_candidate_ref,
            item.source_perception_routing_candidate_ref,
            item.source_observation_demand_ref,
            item.source_capability_requirement_ref,
            item.source_capability_resolution_candidate_ref,
            item.capability_candidate_ref,
            item.capability_class_ref,
            item.trace_ref,
        )
        if not all(required):
            errors.append(
                f"compatibility_candidate_lineage_incomplete:{item.admission_compatibility_candidate_ref}"
            )
        if (
            not item.candidate_only
            or not item.read_only
            or item.truth_declared
            or item.world_truth_declared
            or item.provider_binding
            or item.model_binding
            or item.provider_invocation
            or item.model_invocation
            or item.runtime_admission_requested
            or item.runtime_admission_executed
            or item.gateway_submission
            or item.capability_activation
            or item.capability_reservation
            or item.slot_reservation
            or item.resource_scheduling
            or item.observation_execution
        ):
            errors.append(
                f"invalid_compatibility_candidate_flags:{item.admission_compatibility_candidate_ref}"
            )
        if item.source_observation_demand_ref not in item.lineage_refs:
            errors.append(f"demand_lineage_missing:{item.admission_compatibility_candidate_ref}")
        if item.source_capability_resolution_candidate_ref not in item.lineage_refs:
            errors.append(f"resolution_lineage_missing:{item.admission_compatibility_candidate_ref}")

    mapping_pairs = []
    mapping_refs = _mapping_refs(request.provider_mappings)
    if len(set(mapping_refs)) != len(mapping_refs):
        errors.append("duplicate_provider_mapping_ref")
    for mapping in request.provider_mappings:
        if not isinstance(mapping, GovernedProviderRuntimeTargetMappingV1):
            errors.append("invalid_provider_mapping_type")
            continue
        if not all(
            (
                mapping.mapping_ref,
                mapping.source_admission_compatibility_candidate_ref,
                mapping.capability_class_ref,
                mapping.provider_candidate_ref,
                mapping.provider_class_ref,
                mapping.provider_mapping_basis_refs,
                mapping.provider_admission_refs,
                mapping.provider_availability_refs,
                mapping.availability_status,
                mapping.admission_status,
            )
        ):
            errors.append(f"provider_mapping_incomplete:{mapping.mapping_ref}")
        if not mapping.candidate_only or not mapping.read_only:
            errors.append(f"provider_mapping_not_candidate_only:{mapping.mapping_ref}")
        if mapping.availability_status not in SUPPORTED_AVAILABILITY_STATUSES:
            errors.append(f"unsupported_availability_status:{mapping.mapping_ref}")
        if mapping.admission_status not in SUPPORTED_ADMISSION_STATUSES:
            errors.append(f"unsupported_admission_status:{mapping.mapping_ref}")
        if mapping.source_admission_compatibility_candidate_ref not in compatibility_refs:
            errors.append(f"mapping_source_compatibility_missing:{mapping.mapping_ref}")
        pair = (
            mapping.source_admission_compatibility_candidate_ref,
            mapping.provider_candidate_ref,
        )
        mapping_pairs.append(pair)
    if len(set(mapping_pairs)) != len(mapping_pairs):
        errors.append("duplicate_provider_candidate_for_compatibility")
    return tuple(dict.fromkeys(errors))


def form_provider_runtime_target_candidates(
    request: ProviderRuntimeTargetPreparationInputV1,
) -> ProviderRuntimeTargetPreparationResultV1:
    """Form all explicitly mapped target candidates without binding or execution."""

    compatibility_refs = _compatibility_refs(getattr(request, "compatibility_candidates", ()))
    mapping_refs = _mapping_refs(getattr(request, "provider_mappings", ()))
    errors = _validate(request)
    if errors:
        return _result(request, "INVALID_INPUT", compatibility_refs, mapping_refs, (), errors)
    if not compatibility_refs:
        return _result(
            request,
            "NO_PROVIDER_TARGET_CANDIDATE",
            (),
            mapping_refs,
            (),
        )

    mapping_by_source = {}
    for mapping in request.provider_mappings:
        mapping_by_source.setdefault(
            mapping.source_admission_compatibility_candidate_ref, []
        ).append(mapping)

    targets = []
    errors = []
    outcome_statuses = []
    for compatibility in request.compatibility_candidates:
        source_ref = compatibility.admission_compatibility_candidate_ref
        mappings = mapping_by_source.get(source_ref, [])
        if not mappings:
            outcome_statuses.append("NO_PROVIDER_MAPPING")
            continue
        for mapping in mappings:
            if mapping.capability_class_ref != compatibility.capability_class_ref:
                outcome_statuses.append("NO_MATCHING_PROVIDER")
                continue
            if mapping.availability_status != "AVAILABLE":
                outcome_statuses.append("PROVIDER_UNAVAILABLE")
                continue
            if mapping.admission_status != "ADMITTED" or not mapping.eligible:
                outcome_statuses.append("PROVIDER_NOT_ADMITTED")
                continue
            target_ref = _candidate_ref(
                request.preparation_ref,
                source_ref,
                mapping.provider_candidate_ref,
                mapping.mapping_ref,
            )
            targets.append(
                ProviderRuntimeTargetPreparationCandidateV1(
                    provider_target_candidate_ref=target_ref,
                    source_admission_compatibility_candidate_ref=source_ref,
                    source_perception_routing_candidate_ref=compatibility.source_perception_routing_candidate_ref,
                    source_observation_demand_ref=compatibility.source_observation_demand_ref,
                    source_capability_requirement_ref=compatibility.source_capability_requirement_ref,
                    source_capability_resolution_candidate_ref=compatibility.source_capability_resolution_candidate_ref,
                    capability_candidate_ref=compatibility.capability_candidate_ref,
                    capability_class_ref=compatibility.capability_class_ref,
                    provider_candidate_ref=mapping.provider_candidate_ref,
                    provider_class_ref=mapping.provider_class_ref,
                    source_model_ref=mapping.source_model_ref,
                    provider_mapping_basis_refs=mapping.provider_mapping_basis_refs,
                    provider_admission_refs=mapping.provider_admission_refs,
                    provider_availability_refs=mapping.provider_availability_refs,
                    observation_class=compatibility.observation_class,
                    observation_target_refs=compatibility.observation_target_refs,
                    observation_constraint_refs=compatibility.observation_constraint_refs,
                    expected_information_contribution_refs=compatibility.expected_information_contribution_refs,
                    information_need_refs=compatibility.information_need_refs,
                    information_gap_refs=compatibility.information_gap_refs,
                    source_strategy_ref=compatibility.source_strategy_ref,
                    source_branch_ref=compatibility.source_branch_ref,
                    parent_cognitive_problem_ref=compatibility.parent_cognitive_problem_ref,
                    source_state_ref=compatibility.source_state_ref,
                    context_refs=_unique((*request.context_refs, *compatibility.context_refs)),
                    lineage_refs=_unique(
                        (
                            *compatibility.lineage_refs,
                            source_ref,
                            mapping.mapping_ref,
                            mapping.provider_candidate_ref,
                            target_ref,
                        )
                    ),
                    provenance_refs=_unique(
                        (*compatibility.provenance_refs, *request.provenance_refs)
                    ),
                    trace_ref=request.trace_ref or compatibility.trace_ref,
                    admitted_action_ref=request.admitted_action_ref,
                    working_envelope_ref=request.working_envelope_ref,
                    working_envelope_version_ref=request.working_envelope_version_ref,
                )
            )

    if targets:
        return _result(
            request,
            "PROVIDER_TARGET_CANDIDATES_FORMED",
            compatibility_refs,
            mapping_refs,
            tuple(targets),
            tuple(errors),
        )
    status = outcome_statuses[0] if outcome_statuses else "NO_PROVIDER_TARGET_CANDIDATE"
    return _result(request, status, compatibility_refs, mapping_refs, (), tuple(errors))


__all__ = [
    "OWNER",
    "SUPPORTED_AVAILABILITY_STATUSES",
    "SUPPORTED_ADMISSION_STATUSES",
    "FORMATION_STATUSES",
    "GovernedProviderRuntimeTargetMappingV1",
    "ProviderRuntimeTargetPreparationCandidateV1",
    "ProviderRuntimeTargetPreparationInputV1",
    "ProviderRuntimeTargetPreparationResultV1",
    "form_provider_runtime_target_candidates",
]
