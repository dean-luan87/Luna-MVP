"""Compact B3 fixtures; real cases use validated B2-shaped references only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.midplatform.core.cognitive_state_formation.integration.b2_current_world_cognitive_state_flow_controlled.b2_current_world_cognitive_state_flow_fixture_v1 import (
    build_real_b1_current_world_v1,
    build_synthetic_current_world_v1,
)

from .b3_cognitive_state_intent_decision_task_types_v1 import (
    B2CognitiveStateFlowReferenceV1,
)


@dataclass(frozen=True)
class B3FixtureCaseV1:
    case_id: str
    title: str
    real: bool = False
    intent_scenario_id: str = "B3_NORMAL"
    observation_need: bool = False
    permission_allowed: bool = True
    safety_allowed: bool = True
    hard_constraints_ok: bool = True
    evidence_ready: bool = True
    high_uncertainty: bool = False
    competing_hypotheses: bool = False
    resource_pressure_level: str = "NORMAL"
    multiple_intents: bool = False
    dominance: bool = False
    cancellation: bool = False
    expects_task: bool = True
    expected_decision_outcome: str = "SELECTED"


def _source(case_id: str, real: bool, *, observation_need: bool, conflict: bool = False) -> B2CognitiveStateFlowReferenceV1:
    world = build_real_b1_current_world_v1() if real else build_synthetic_current_world_v1(
        conflict=conflict,
        alternatives=case_id in {"B3-06", "B3-11"},
    )
    prefix = "real" if real else "synthetic"
    obs = tuple(world.observation_refs)
    return B2CognitiveStateFlowReferenceV1(
        case_id=case_id,
        mode="REAL_B2_COGNITIVE_STATE_FLOW_INPUT" if real else "SYNTHETIC_COGNITIVE_STATE_FLOW",
        cognitive_state_ref=f"cognitive-state:{prefix}:{case_id}",
        cognitive_flow_ref=f"cognitive-flow:{prefix}:{case_id}",
        attention_refs=(f"attention:{prefix}:{case_id}:primary", f"attention:{prefix}:{case_id}:alternative")
        if case_id == "B3-06" else (f"attention:{prefix}:{case_id}",),
        hypothesis_refs=(f"hypothesis:{prefix}:{case_id}",),
        alternative_hypothesis_refs=(f"hypothesis:{prefix}:{case_id}:alternative",)
        if case_id in {"B3-06", "B3-12"} else (),
        observation_need_refs=(f"observation-need:{case_id}",) if observation_need else (),
        current_world_ref=world.current_world_id,
        context_refs=world.context_refs,
        field_refs=world.field_state_refs,
        pcn_refs=world.pcn_refs,
        uncertainty_refs=tuple(dict.fromkeys((*world.uncertainty_refs, f"uncertainty:{case_id}"))),
        conflict_refs=tuple(dict.fromkeys((*world.conflict_refs, f"conflict:{case_id}"))) if conflict else world.conflict_refs,
        temporal_refs=world.temporal_refs,
        trace_ref=f"trace:{prefix}:{case_id}",
        provenance_refs=tuple(dict.fromkeys((*world.provenance_refs, f"provenance:{prefix}:{case_id}:b2"))),
    )


def build_b3_cases_v1() -> Tuple[B3FixtureCaseV1, ...]:
    return (
        B3FixtureCaseV1("B3-01", "real B2 cognitive input accepted", real=True),
        B3FixtureCaseV1("B3-02", "cognitive input remains read-only", real=True),
        B3FixtureCaseV1("B3-03", "Intent influence/reference created", real=True),
        B3FixtureCaseV1("B3-04", "Cognitive State does not own Intent", real=True),
        B3FixtureCaseV1("B3-05", "Potential Intent remains distinct from active Intent", real=True),
        B3FixtureCaseV1(
            "B3-06", "multiple intents preserved", intent_scenario_id="B3-06_FAMILY_FIELD_LONG_TERM",
            multiple_intents=True, real=True,
        ),
        B3FixtureCaseV1(
            "B3-07", "dominance remains Intent Governance-owned", intent_scenario_id="B3-07_DOMINANCE",
            dominance=True, real=True,
        ),
        B3FixtureCaseV1(
            "B3-08", "observation need can defer progression", observation_need=True,
            expected_decision_outcome="REQUEST_MORE_EVIDENCE", expects_task=False, real=True,
        ),
        B3FixtureCaseV1("B3-09", "Intent Governance result created", real=True),
        B3FixtureCaseV1("B3-10", "Decision input created", real=True),
        B3FixtureCaseV1("B3-11", "Decision Candidate created", real=True),
        B3FixtureCaseV1(
            "B3-12", "Decision may DEFER/ABSTAIN/RECONSIDER", high_uncertainty=True,
            expected_decision_outcome="DEFER", expects_task=False, real=True,
        ),
        B3FixtureCaseV1("B3-13", "Decision is not Action", real=True),
        B3FixtureCaseV1(
            "B3-14", "safety/permission veto preserved", permission_allowed=False,
            expected_decision_outcome="CONSTRAINED", expects_task=False, real=True,
        ),
        B3FixtureCaseV1(
            "B3-15", "resource constraints preserved", resource_pressure_level="DEGRADED", real=True,
        ),
        B3FixtureCaseV1("B3-16", "Decision-to-Task canonical handoff created", real=True),
        B3FixtureCaseV1("B3-17", "TaskCandidate created", real=True),
        B3FixtureCaseV1("B3-18", "Task readiness candidate created", real=True),
        B3FixtureCaseV1("B3-19", "Task is not Action execution", real=True),
        B3FixtureCaseV1("B3-20", "cancellation/interruption boundary preserved", cancellation=True, real=True),
        B3FixtureCaseV1("B3-21", "no Runtime execution", real=True),
        B3FixtureCaseV1("B3-22", "trace/provenance complete", real=True),
        B3FixtureCaseV1("B3-23", "no semantic compression", real=True),
        B3FixtureCaseV1("B3-24", "synthetic regression preserved"),
        B3FixtureCaseV1("B3-25", "differential governance compatibility", real=True),
        B3FixtureCaseV1("B3-26", "real B2 Cognitive-to-Intent-to-Decision-to-Task candidate", real=True),
    )


def build_case_source(case: B3FixtureCaseV1) -> B2CognitiveStateFlowReferenceV1:
    return _source(
        case.case_id,
        case.real,
        observation_need=case.observation_need,
        conflict=case.multiple_intents,
    )
