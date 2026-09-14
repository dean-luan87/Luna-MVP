"""Twenty-eight cross-module controlled scenarios for the integrated loop."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional, Tuple

from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.integration.b2_current_world_cognitive_state_flow_controlled.b2_current_world_cognitive_state_flow_fixture_v1 import (
    build_real_b1_current_world_v1,
    build_synthetic_current_world_v1,
)


@dataclass(frozen=True)
class IntegratedScenarioV1:
    scenario_id: str
    title: str
    input_mode: str
    current_world_factory: Callable[[], CurrentWorldCandidateV1]
    update_count: int = 0
    sufficient: bool = False
    sufficient_at: int = 0
    hypothesis_change: bool = False
    alternative_need: bool = False
    capability_mode: str = "AVAILABLE"
    execution_outcome: Optional[str] = None
    requirement_satisfaction: Optional[str] = None
    task_contribution: Optional[str] = None
    b4_reconsideration: bool = False
    b4_reobserve: bool = False
    plan_count: int = 7
    expected_final_disposition: str = "INSUFFICIENT"
    expected_next_step: str = "DEFER"
    expected_state_count: int = 1
    expected_reconsideration_count: int = 0
    expected_requirement_disposition: str = "STILL_RELEVANT"


def _real() -> CurrentWorldCandidateV1:
    return build_real_b1_current_world_v1()


def _synthetic() -> CurrentWorldCandidateV1:
    return build_synthetic_current_world_v1()


def _conflicted() -> CurrentWorldCandidateV1:
    return build_synthetic_current_world_v1(conflict=True, alternatives=True)


def build_integrated_scenarios_v1() -> Tuple[IntegratedScenarioV1, ...]:
    """Return integration-focused cases; B1/B2/Capability unit cases stay elsewhere."""
    return (
        IntegratedScenarioV1("I01", "real B1 visual input reaches integrated loop", "REAL_B1_CURRENT_WORLD_INPUT", _real),
        IntegratedScenarioV1("I02", "controlled Current World input reaches integrated loop", "SYNTHETIC_CURRENT_WORLD_INPUT", _synthetic),
        IntegratedScenarioV1("I03", "Current World remains read-only across handoff", "REAL_B1_CURRENT_WORLD_INPUT", _real),
        IntegratedScenarioV1("I04", "B1 to B2 state and Flow references remain linked", "REAL_B1_CURRENT_WORLD_INPUT", _real),
        IntegratedScenarioV1("I05", "insufficient evidence selects the next minimum Need", "REAL_B1_CURRENT_WORLD_INPUT", _real, update_count=1, expected_final_disposition="INSUFFICIENT", expected_next_step="CONTINUE", expected_state_count=2),
        IntegratedScenarioV1("I06", "two insufficient updates advance Need and state version", "SYNTHETIC_CURRENT_WORLD_INPUT", _synthetic, update_count=2, expected_final_disposition="INSUFFICIENT", expected_next_step="CONTINUE", expected_state_count=3),
        IntegratedScenarioV1("I07", "provisional plan candidates remain non-binding", "REAL_B1_CURRENT_WORLD_INPUT", _real),
        IntegratedScenarioV1("I08", "current minimum Need forms a bounded requirement", "REAL_B1_CURRENT_WORLD_INPUT", _real),
        IntegratedScenarioV1("I09", "sufficiency stops the remaining provisional path", "REAL_B1_CURRENT_WORLD_INPUT", _real, update_count=1, sufficient=True, sufficient_at=1, expected_final_disposition="SUFFICIENT", expected_next_step="STOP_SUFFICIENT", expected_state_count=2),
        IntegratedScenarioV1("I10", "unmaterialized candidates after STOP are not failures", "SYNTHETIC_CURRENT_WORLD_INPUT", _synthetic, update_count=1, sufficient=True, sufficient_at=1, expected_final_disposition="SUFFICIENT", expected_next_step="STOP_SUFFICIENT", expected_state_count=2),
        IntegratedScenarioV1("I11", "capability failure does not block already sufficient goal", "REAL_B1_CURRENT_WORLD_INPUT", _real, update_count=1, sufficient=True, sufficient_at=1, execution_outcome="FAILURE", requirement_satisfaction="UNSATISFIED", task_contribution="NO_CONTRIBUTION", expected_final_disposition="SUFFICIENT", expected_next_step="STOP_SUFFICIENT", expected_state_count=2),
        IntegratedScenarioV1("I12", "evidence after sufficiency is ignored", "SYNTHETIC_CURRENT_WORLD_INPUT", _synthetic, update_count=2, sufficient=True, sufficient_at=1, expected_final_disposition="SUFFICIENT", expected_next_step="STOP_SUFFICIENT", expected_state_count=2),
        IntegratedScenarioV1("I13", "new evidence invalidates hypothesis and replans", "REAL_B1_CURRENT_WORLD_INPUT", _real, update_count=1, hypothesis_change=True, alternative_need=True, expected_final_disposition="RECONSIDER", expected_next_step="REPLAN", expected_state_count=2, expected_reconsideration_count=1),
        IntegratedScenarioV1("I14", "hypothesis change materializes only a replacement Need", "SYNTHETIC_CURRENT_WORLD_INPUT", _synthetic, update_count=1, hypothesis_change=True, alternative_need=True, expected_final_disposition="RECONSIDER", expected_next_step="REPLAN", expected_state_count=2, expected_reconsideration_count=1),
        IntegratedScenarioV1("I15", "old requirement is superseded by the new state", "REAL_B1_CURRENT_WORLD_INPUT", _real, update_count=1, hypothesis_change=True, alternative_need=True, expected_final_disposition="RECONSIDER", expected_next_step="REPLAN", expected_state_count=2, expected_reconsideration_count=1, expected_requirement_disposition="SUPERSEDED"),
        IntegratedScenarioV1("I16", "new state changes the subsequent Need path", "SYNTHETIC_CURRENT_WORLD_INPUT", _synthetic, update_count=1, hypothesis_change=True, alternative_need=True, expected_final_disposition="RECONSIDER", expected_next_step="REPLAN", expected_state_count=2, expected_reconsideration_count=1),
        IntegratedScenarioV1("I17", "unavailable capability enters reconsideration", "REAL_B1_CURRENT_WORLD_INPUT", _real, update_count=1, alternative_need=True, capability_mode="UNAVAILABLE", expected_final_disposition="RECONSIDER", expected_next_step="REQUEST_MORE_EVIDENCE", expected_state_count=2, expected_reconsideration_count=1),
        IntegratedScenarioV1("I18", "degraded capability enters reconsideration", "SYNTHETIC_CURRENT_WORLD_INPUT", _synthetic, update_count=1, alternative_need=True, capability_mode="DEGRADED", expected_final_disposition="RECONSIDER", expected_next_step="REQUEST_MORE_EVIDENCE", expected_state_count=2, expected_reconsideration_count=1),
        IntegratedScenarioV1("I19", "out-of-scope capability yields Gap and alternative Need", "REAL_B1_CURRENT_WORLD_INPUT", _real, update_count=1, alternative_need=True, capability_mode="OUT_OF_SCOPE", expected_final_disposition="RECONSIDER", expected_next_step="REQUEST_MORE_EVIDENCE", expected_state_count=2, expected_reconsideration_count=1),
        IntegratedScenarioV1("I20", "unavailable capability without alternative defers safely", "SYNTHETIC_CURRENT_WORLD_INPUT", _synthetic, update_count=1, capability_mode="UNAVAILABLE", plan_count=1, expected_final_disposition="RECONSIDER", expected_next_step="DEFER", expected_state_count=2, expected_reconsideration_count=1),
        IntegratedScenarioV1("I21", "execution SUCCESS remains UNSATISFIED", "REAL_B1_CURRENT_WORLD_INPUT", _real, update_count=1, execution_outcome="SUCCESS", requirement_satisfaction="UNSATISFIED", task_contribution="CONTRIBUTED", expected_final_disposition="RECONSIDER", expected_next_step="REQUEST_MORE_EVIDENCE", expected_state_count=2, expected_reconsideration_count=1),
        IntegratedScenarioV1("I22", "execution, requirement, and task dimensions stay separate", "SYNTHETIC_CURRENT_WORLD_INPUT", _synthetic, update_count=1, execution_outcome="SUCCESS", requirement_satisfaction="UNSATISFIED", task_contribution="CONTRIBUTED", expected_final_disposition="RECONSIDER", expected_next_step="REQUEST_MORE_EVIDENCE", expected_state_count=2, expected_reconsideration_count=1),
        IntegratedScenarioV1("I23", "requirement satisfaction is not cognitive sufficiency", "REAL_B1_CURRENT_WORLD_INPUT", _real, update_count=1, execution_outcome="SUCCESS", requirement_satisfaction="SATISFIED", task_contribution="CONTRIBUTED", expected_final_disposition="INSUFFICIENT", expected_next_step="CONTINUE", expected_state_count=2),
        IntegratedScenarioV1("I24", "capability FAILURE with sufficient evidence still stops", "SYNTHETIC_CURRENT_WORLD_INPUT", _synthetic, update_count=1, sufficient=True, sufficient_at=1, execution_outcome="FAILURE", requirement_satisfaction="UNSATISFIED", task_contribution="NO_CONTRIBUTION", expected_final_disposition="SUFFICIENT", expected_next_step="STOP_SUFFICIENT", expected_state_count=2),
        IntegratedScenarioV1("I25", "B4 reconsideration reference returns to Cognitive Flow", "REAL_B1_CURRENT_WORLD_INPUT", _real, update_count=1, alternative_need=True, capability_mode="UNAVAILABLE", b4_reconsideration=True, expected_final_disposition="RECONSIDER", expected_next_step="REQUEST_MORE_EVIDENCE", expected_state_count=2, expected_reconsideration_count=1),
        IntegratedScenarioV1("I26", "B4 reobserve remains an observation candidate", "SYNTHETIC_CURRENT_WORLD_INPUT", _synthetic, update_count=1, alternative_need=True, capability_mode="DEGRADED", b4_reobserve=True, expected_final_disposition="RECONSIDER", expected_next_step="REQUEST_MORE_EVIDENCE", expected_state_count=2, expected_reconsideration_count=1),
        IntegratedScenarioV1("I27", "trace and provenance refs reverse-link every handoff", "REAL_B1_CURRENT_WORLD_INPUT", _real, update_count=1, alternative_need=True, hypothesis_change=True, expected_final_disposition="RECONSIDER", expected_next_step="REPLAN", expected_state_count=2, expected_reconsideration_count=1),
        IntegratedScenarioV1("I28", "integrated negative guards remain closed", "SYNTHETIC_CURRENT_WORLD_INPUT", _synthetic, update_count=1, expected_final_disposition="INSUFFICIENT", expected_next_step="CONTINUE", expected_state_count=2),
    )


__all__ = ["IntegratedScenarioV1", "build_integrated_scenarios_v1"]
