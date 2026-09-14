"""Deterministic placeholder activation skeleton for synthetic fixtures."""

from __future__ import annotations

from typing import Dict, Tuple

from .personal_cognitive_activation_types_v1 import (
    ACTIVATION_STATES,
    ActivationCandidate,
    ActivationConstraintReference,
    ActivationProjection,
    ActivationRequest,
)
from .personal_cognitive_network_types_v1 import CognitiveObjectReference


def prepare_activation_candidate_from_fixture(
    request: ActivationRequest,
    source_refs: Tuple[CognitiveObjectReference, ...],
) -> ActivationCandidate:
    resource_label = request.resource_budget_label.upper()
    take = len(source_refs)
    if resource_label == "LOW":
        take = max(1, len(source_refs) // 2)
    selected = source_refs[:take]

    constraints = (
        ActivationConstraintReference(
            constraint_id="constraint-context-resource",
            source="Context+Resource",
            detail=f"budget={request.resource_budget_label}",
        ),
    )
    return ActivationCandidate(
        candidate_id=f"activation-{request.request_id}",
        activation_state=ACTIVATION_STATES[0],
        active_refs=selected,
        constraint_refs=constraints,
        temporal_validity="CURRENT_CONTEXT_WINDOW",
        confidence="candidate",
        uncertainty="preserved",
        fixed_time_threshold_used=False,
        candidate_only=True,
    )


def prepare_activation_projection(
    activation: ActivationCandidate,
    active_link_ids: Tuple[str, ...],
    unresolved_links: Tuple[str, ...],
    resource_constraint_ref: str,
) -> ActivationProjection:
    return ActivationProjection(
        projection_id=f"projection-{activation.candidate_id}",
        activation_ref=activation.candidate_id,
        active_ref_ids=tuple(ref.reference_id for ref in activation.active_refs),
        active_link_ids=active_link_ids,
        unresolved_links=unresolved_links,
        resource_constraint_ref=resource_constraint_ref,
        candidate_only=True,
    )
