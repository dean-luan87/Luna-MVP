"""Reference-only runtime observation ingress integration types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.midplatform.core.observation_gateway.observation_gateway_core_types_v1 import (
    RuntimeObservationEnvelopeV1,
)


@dataclass(frozen=True)
class RuntimeObservationIngressCaseV1:
    case_id: str
    title: str
    observation: RuntimeObservationEnvelopeV1
    context_ref: str
    pcn_ref: str
    intent_ref: str
    role_refs: Tuple[str, ...] = ()
    task_refs: Tuple[str, ...] = ()
    goal_refs: Tuple[str, ...] = ()
    concern_refs: Tuple[str, ...] = ()
    information_need_refs: Tuple[str, ...] = ()
    field_refs: Tuple[str, ...] = ()
    relation_refs: Tuple[str, ...] = ()
    required_information_refs: Tuple[str, ...] = ()
    available_information_refs: Tuple[str, ...] = ()
    evidence_information_refs: Tuple[Tuple[str, Tuple[str, ...]], ...] = ()
    inherited_information_refs: Tuple[str, ...] = ()
    route_to_orchestration: bool = True
    candidate_only: bool = True
    synthetic_only: bool = False
    controlled_integration_only: bool = True
    cycle_index: int = 1
    prior_current_world_ref: str | None = None
    prior_hypothesis_refs: Tuple[str, ...] = ()
    prior_information_gap_ref: str | None = None
    prior_reobservation_ref: str | None = None
    prior_next_cycle_ingress_ref: str | None = None
    prior_sufficiency_candidate: object | None = None
    prior_information_gap_candidate: object | None = None
    prior_reobservation_candidate: object | None = None
