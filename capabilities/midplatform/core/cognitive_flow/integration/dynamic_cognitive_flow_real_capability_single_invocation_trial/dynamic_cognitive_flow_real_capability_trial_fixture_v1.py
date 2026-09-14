"""Twenty-two cross-module scenarios for the one-invocation trial."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class RealCapabilityTrialScenarioV1:
    scenario_id: str
    title: str
    update_count: int = 0
    sufficient_at: int = 0
    hypothesis_change: bool = False
    alternative_need: bool = False
    expected_final_disposition: str = "INSUFFICIENT"
    expected_next_step: str = "DEFER"
    expected_state_count: int = 1
    expected_reconsideration_count: int = 0


def build_real_capability_trial_scenarios_v1() -> Tuple[RealCapabilityTrialScenarioV1, ...]:
    return (
        RealCapabilityTrialScenarioV1("RCT-01", "Brain Need forms DETECT_OBJECT requirement"),
        RealCapabilityTrialScenarioV1("RCT-02", "Scope accepts object_detection"),
        RealCapabilityTrialScenarioV1("RCT-03", "Resolution maps capability to model contract"),
        RealCapabilityTrialScenarioV1("RCT-04", "Provider admission uses resolved YOLO11n path"),
        RealCapabilityTrialScenarioV1("RCT-05", "real provider invocation count is one"),
        RealCapabilityTrialScenarioV1("RCT-06", "single frame boundary is preserved"),
        RealCapabilityTrialScenarioV1("RCT-07", "real visual evidence returns"),
        RealCapabilityTrialScenarioV1("RCT-08", "evidence passes Observation Gateway admission"),
        RealCapabilityTrialScenarioV1("RCT-09", "B1 Current World receives candidate evidence"),
        RealCapabilityTrialScenarioV1("RCT-10", "B2 Cognitive State receives updated evidence reference"),
        RealCapabilityTrialScenarioV1("RCT-11", "real evidence can remain cognitively insufficient", update_count=1, expected_final_disposition="RECONSIDER", expected_next_step="REQUEST_MORE_EVIDENCE", expected_state_count=2, expected_reconsideration_count=1),
        RealCapabilityTrialScenarioV1("RCT-12", "controlled sufficiency can stop remaining candidates", update_count=1, sufficient_at=1, expected_final_disposition="SUFFICIENT", expected_next_step="STOP_SUFFICIENT", expected_state_count=2),
        RealCapabilityTrialScenarioV1("RCT-13", "new evidence changes next-step disposition", update_count=1, hypothesis_change=True, alternative_need=True, expected_final_disposition="RECONSIDER", expected_next_step="REPLAN", expected_state_count=2, expected_reconsideration_count=1),
        RealCapabilityTrialScenarioV1("RCT-14", "insufficient result does not trigger second provider call", update_count=1, expected_final_disposition="RECONSIDER", expected_next_step="REQUEST_MORE_EVIDENCE", expected_state_count=2, expected_reconsideration_count=1),
        RealCapabilityTrialScenarioV1("RCT-15", "sufficient result blocks second provider call", update_count=2, sufficient_at=1, expected_final_disposition="SUFFICIENT", expected_next_step="STOP_SUFFICIENT", expected_state_count=2),
        RealCapabilityTrialScenarioV1("RCT-16", "remaining plan candidates stay non-binding", update_count=1, expected_final_disposition="RECONSIDER", expected_next_step="REQUEST_MORE_EVIDENCE", expected_state_count=2, expected_reconsideration_count=1),
        RealCapabilityTrialScenarioV1("RCT-17", "provider evidence is not World Truth"),
        RealCapabilityTrialScenarioV1("RCT-18", "Brain does not select provider/model identity directly"),
        RealCapabilityTrialScenarioV1("RCT-19", "no Action execution follows the trial", update_count=1, expected_final_disposition="RECONSIDER", expected_next_step="REQUEST_MORE_EVIDENCE", expected_state_count=2, expected_reconsideration_count=1),
        RealCapabilityTrialScenarioV1("RCT-20", "no Learning or Memory mutation follows the trial"),
        RealCapabilityTrialScenarioV1("RCT-21", "trace and provenance remain reverse-linkable"),
        RealCapabilityTrialScenarioV1("RCT-22", "global single-invocation and candidate-only guards"),
    )


__all__ = ["RealCapabilityTrialScenarioV1", "build_real_capability_trial_scenarios_v1"]
