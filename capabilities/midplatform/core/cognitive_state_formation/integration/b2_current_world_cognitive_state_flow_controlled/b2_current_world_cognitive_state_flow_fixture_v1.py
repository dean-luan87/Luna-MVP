"""Compact B2 fixtures for real-B1 and synthetic Current World inputs."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Tuple

from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)


@dataclass(frozen=True)
class B2FixtureCaseV1:
    case_id: str
    title: str
    mode: str
    current_world: CurrentWorldCandidateV1
    engine_scenario_id: str = "S01"
    flow_scenario_id: str = "C01"


def _world(
    world_id: str,
    *,
    context: str,
    observation: str,
    uncertainty: Tuple[str, ...] = (),
    conflict: Tuple[str, ...] = (),
    provenance: Tuple[str, ...] = (),
    source_version: str = "b1-current-world-candidate-v1",
) -> CurrentWorldCandidateV1:
    return CurrentWorldCandidateV1(
        current_world_id=world_id,
        attention_refs=(),
        active_hypothesis_refs=(),
        alternative_hypothesis_refs=(),
        context_refs=(context,),
        field_state_refs=(),
        pcn_refs=(f"pcn:{world_id}",),
        intent_refs=(f"intent:{world_id}",),
        observation_refs=(observation,),
        uncertainty_refs=uncertainty,
        conflict_refs=conflict,
        temporal_refs=(f"temporal:{world_id}", f"observed:{world_id}"),
        source_versions={"current_world": source_version, "context": "v1"},
        world_state_kind_candidate="CONFLICTED" if conflict else "PARTIAL",
        world_stability_candidate="LOW" if conflict or uncertainty else "MEDIUM",
        trace_ref=f"trace:{world_id}",
        provenance_refs=provenance or (f"provenance:{world_id}",),
        candidate_only=True,
        field_mutation=False,
        field_entity_creation=False,
        field_confidence_mutation=False,
        field_transition=False,
        event_admission=False,
        reducer_invocation_as_mutation_authority=False,
        field_truth_declaration=False,
    )


def build_real_b1_current_world_v1() -> CurrentWorldCandidateV1:
    """A validated B1-shaped candidate reference; no provider is invoked."""

    return _world(
        "current-world:B1-23-real-yolo11n",
        context="context:B1-23",
        observation="visual-evidence:yolo11n:B1-23:001",
        uncertainty=("uncertainty:B1-23",),
        provenance=(
            "provenance:model-manager:B1-23",
            "provenance:provider:B1-23",
            "provenance:frame:B1-23",
            "trace:current-world:B1-23",
        ),
    )


def build_synthetic_current_world_v1(
    *, conflict: bool = False, alternatives: bool = False
) -> CurrentWorldCandidateV1:
    world = _world(
        "current-world:synthetic:B2",
        context="context:synthetic:B2",
        observation="observation:synthetic:B2",
        uncertainty=("uncertainty:synthetic:B2",) if conflict else (),
        conflict=("contradiction:synthetic:B2",) if conflict else (),
        source_version="synthetic-current-world-v1",
    )
    if not alternatives:
        return world
    return replace(
        world,
        alternative_hypothesis_refs=(
            "hypothesis:synthetic:B2:alternative:1",
            "hypothesis:synthetic:B2:alternative:2",
        ),
    )


def build_b2_cases_v1() -> Tuple[B2FixtureCaseV1, ...]:
    real = build_real_b1_current_world_v1()
    synthetic = build_synthetic_current_world_v1()
    conflicted = build_synthetic_current_world_v1(conflict=True)
    alternatives = build_synthetic_current_world_v1(alternatives=True)
    titles = {
        "B2-01": "real Current World accepted",
        "B2-02": "Current World remains read-only",
        "B2-03": "Cognitive State candidate created",
        "B2-04": "Cognitive State is not World truth",
        "B2-05": "Attention candidate created",
        "B2-06": "Attention is not provider execution",
        "B2-07": "Hypothesis candidate created",
        "B2-08": "Hypothesis is not fact",
        "B2-09": "supporting references preserved",
        "B2-10": "uncertainty preserved",
        "B2-11": "conflict and contradiction preserved",
        "B2-12": "alternative hypothesis boundary",
        "B2-13": "PCN remains read-only",
        "B2-14": "Intent refs remain read-only",
        "B2-15": "Observation Need candidate may be expressed",
        "B2-16": "Observation Need does not execute provider",
        "B2-17": "Cognitive Flow transition created",
        "B2-18": "previous and current state trace preserved",
        "B2-19": "no Decision mutation",
        "B2-20": "no Task or Action mutation",
        "B2-21": "no semantic compression",
        "B2-22": "synthetic cognitive regression preserved",
        "B2-23": "differential governance compatibility",
        "B2-24": "real B1 Current World to Cognitive Flow candidate",
    }
    cases = []
    for case_id, title in titles.items():
        world = real
        mode = "REAL_B1_CURRENT_WORLD_INPUT"
        state_scenario = "S01"
        flow_scenario = "C01"
        if case_id == "B2-11":
            world = conflicted
            mode = "SYNTHETIC_CURRENT_WORLD"
            state_scenario = "S02"
            flow_scenario = "C05"
        elif case_id == "B2-12":
            world = alternatives
            mode = "SYNTHETIC_CURRENT_WORLD"
            state_scenario = "S03"
            flow_scenario = "C05"
        elif case_id == "B2-22":
            world = synthetic
            mode = "SYNTHETIC_CURRENT_WORLD"
        elif case_id in {"B2-15", "B2-16"}:
            flow_scenario = "C05"
        cases.append(
            B2FixtureCaseV1(
                case_id=case_id,
                title=title,
                mode=mode,
                current_world=world,
                engine_scenario_id=state_scenario,
                flow_scenario_id=flow_scenario,
            )
        )
    return tuple(cases)


__all__ = [
    "B2FixtureCaseV1",
    "build_b2_cases_v1",
    "build_real_b1_current_world_v1",
    "build_synthetic_current_world_v1",
]
