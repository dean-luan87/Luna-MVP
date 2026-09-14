"""Resolve minimum situated conditions from the current cognitive need."""

from __future__ import annotations

from typing import Tuple

from .situated_capability_precondition_types_v1 import (
    CapabilityPreconditionDefinitionV1,
    MinimumSituatedConditionRequirementV1,
)


TEXT_PRESENCE_INFORMATION_NEED = "information:text-presence:v1"
PRIMARY_SIGN_TEXT_INFORMATION_NEED = "information:primary-transit-sign-text:v1"

CONDITION_TARGET_VISIBLE = "condition:target-visible:v1"
CONDITION_TARGET_COMPLETE = "condition:target-complete:v1"
CONDITION_TARGET_SCALE_ADEQUATE = "condition:target-scale-adequate:v1"
CONDITION_STABLE_RELATION = "condition:stable-relation:v1"

_MINIMUM_BY_INFORMATION_NEED = {
    TEXT_PRESENCE_INFORMATION_NEED: (
        (CONDITION_TARGET_VISIBLE,),
        (CONDITION_STABLE_RELATION,),
    ),
    PRIMARY_SIGN_TEXT_INFORMATION_NEED: (
        (
            CONDITION_TARGET_VISIBLE,
            CONDITION_TARGET_COMPLETE,
            CONDITION_TARGET_SCALE_ADEQUATE,
            CONDITION_STABLE_RELATION,
        ),
        tuple(),
    ),
}


def resolve_minimum_situated_conditions(
    *,
    capability_definition: CapabilityPreconditionDefinitionV1,
    information_need_ref: str,
    goal_ref: str,
    intent_ref: str = "",
    concern_ref: str = "",
) -> MinimumSituatedConditionRequirementV1:
    """Resolve a requirement; the capability only supplies supported dimensions."""

    if information_need_ref not in _MINIMUM_BY_INFORMATION_NEED:
        raise ValueError(f"no canonical minimum-condition policy for {information_need_ref}")
    required, optional = _MINIMUM_BY_INFORMATION_NEED[information_need_ref]
    supported = set(capability_definition.supported_condition_refs)
    if not set(required).issubset(supported) or not set(optional).issubset(supported):
        raise ValueError(f"capability does not declare support for {information_need_ref} conditions")
    requirement_ref = f"minimum-situated-condition-requirement:{information_need_ref}:{capability_definition.capability_requirement_ref}"
    provenance = (
        f"provenance:minimum-condition-resolution:{information_need_ref}",
        capability_definition.capability_requirement_ref,
        intent_ref,
        concern_ref,
    )
    return MinimumSituatedConditionRequirementV1(
        requirement_ref=requirement_ref,
        capability_requirement_ref=capability_definition.capability_requirement_ref,
        information_need_ref=information_need_ref,
        goal_ref=goal_ref,
        required_condition_refs=required,
        optional_condition_refs=optional,
        source_refs=(
            "capabilities/registry/luna_capability_registry_v1.json",
            "docs/architecture/phase_p1_luna_situated_capability_precondition_cognition_foundation_v1/capability_preconditions.md",
        ),
        provenance_refs=tuple(ref for ref in provenance if ref),
    )


__all__ = [
    "CONDITION_STABLE_RELATION",
    "CONDITION_TARGET_COMPLETE",
    "CONDITION_TARGET_SCALE_ADEQUATE",
    "CONDITION_TARGET_VISIBLE",
    "PRIMARY_SIGN_TEXT_INFORMATION_NEED",
    "TEXT_PRESENCE_INFORMATION_NEED",
    "resolve_minimum_situated_conditions",
]
