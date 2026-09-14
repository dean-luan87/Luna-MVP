from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.midplatform.core.context_pcn_intent_mainline.context_pcn_intent_mainline_types_v1 import (
    IntegrationScenarioDirectiveV1,
)


@dataclass(frozen=True)
class ContextPcnIntentFixtureCaseV1:
    case_id: str
    description: str
    directive: IntegrationScenarioDirectiveV1


def _case(
    case_id: str,
    description: str,
    **kwargs: object,
) -> ContextPcnIntentFixtureCaseV1:
    return ContextPcnIntentFixtureCaseV1(
        case_id=case_id,
        description=description,
        directive=IntegrationScenarioDirectiveV1(
            scenario_id=case_id,
            description=description,
            **kwargs,
        ),
    )


def get_context_pcn_intent_fixture_cases_v1() -> Tuple[
    ContextPcnIntentFixtureCaseV1, ...
]:
    return (
        _case("P01", "Context -> PCN -> Intent happy path"),
        _case(
            "P02",
            "Context incomplete -> stop before PCN",
            force_context_incomplete=True,
        ),
        _case(
            "P03",
            "Context handoff missing required ref -> reject",
            remove_context_required_ref=True,
        ),
        _case(
            "P04",
            "Context->PCN version mismatch -> hard block",
            context_to_pcn_version_override="candidate-v2",
        ),
        _case("P05", "PCN receives valid Context -> produce PCN candidate"),
        _case("P06", "PCN incomplete -> stop before Intent", force_pcn_incomplete=True),
        _case(
            "P07",
            "PCN->Intent missing required ref -> reject",
            remove_pcn_required_ref=True,
        ),
        _case(
            "P08",
            "PCN->Intent version mismatch -> hard block",
            pcn_to_intent_version_override="candidate-v2",
        ),
        _case(
            "P09",
            "duplicate Context handoff -> no duplicate PCN candidate",
            duplicate_context_handoff_probe=True,
        ),
        _case(
            "P10",
            "duplicate PCN handoff -> no duplicate Intent candidate",
            duplicate_pcn_handoff_probe=True,
        ),
        _case("P11", "trace continuity Context->PCN->Intent"),
        _case("P12", "provenance reverse lookup Intent->PCN->Context"),
        _case("P13", "Context influence does not mutate Intent directly"),
        _case("P14", "PCN influence does not own Intent"),
        _case(
            "P15",
            "Intent rejection returns controlled error candidate",
            force_intent_reject=True,
        ),
    )
