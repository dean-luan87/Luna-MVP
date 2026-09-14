from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.midplatform.core.cognitive_execution_chain.cognitive_execution_chain_types_v1 import (
    IntegrationScenarioDirectiveV1,
)


@dataclass(frozen=True)
class CognitiveExecutionChainFixtureCaseV1:
    case_id: str
    category: str
    description: str
    directive: IntegrationScenarioDirectiveV1


def _case(
    case_id: str, category: str, description: str, **kwargs: object
) -> CognitiveExecutionChainFixtureCaseV1:
    return CognitiveExecutionChainFixtureCaseV1(
        case_id=case_id,
        category=category,
        description=description,
        directive=IntegrationScenarioDirectiveV1(
            scenario_id=case_id,
            category=category,
            description=description,
            **kwargs,
        ),
    )


def get_cognitive_execution_chain_fixtures_v1() -> Tuple[
    CognitiveExecutionChainFixtureCaseV1, ...
]:
    return (
        _case("F01", "forward", "full forward happy path"),
        _case(
            "F02",
            "forward",
            "causal unresolved then decision defer",
            force_causal_uncertainty_high=True,
        ),
        _case(
            "F03", "forward", "decision abstain no action", force_decision_abstain=True
        ),
        _case(
            "F04",
            "forward",
            "decision permission veto no action",
            force_decision_permission_veto=True,
        ),
        _case(
            "F05",
            "forward",
            "action permission revoked no runtime",
            force_action_permission_revoked=True,
        ),
        _case(
            "F06",
            "forward",
            "action stale confirmation no runtime",
            force_action_stale_confirmation=True,
        ),
        _case(
            "F07",
            "forward",
            "runtime admission rejection",
            force_runtime_admission_reject=True,
        ),
        _case(
            "B01",
            "feedback",
            "runtime failure to action reconsideration",
            force_runtime_failure=True,
        ),
        _case(
            "B02",
            "feedback",
            "runtime timeout to action task diagnostics",
            force_runtime_timeout=True,
        ),
        _case(
            "B03",
            "feedback",
            "runtime partial to reconsideration",
            force_runtime_partial=True,
        ),
        _case(
            "B04",
            "feedback",
            "action cancelled to decision reconsideration",
            force_action_cancelled=True,
        ),
        _case(
            "B05",
            "feedback",
            "repeated same failure loop guard stop",
            force_runtime_failure=True,
            repeat_same_failure_probe=True,
        ),
        _case(
            "B06",
            "feedback",
            "no new evidence loop stop",
            force_runtime_failure=True,
            no_new_evidence_probe=True,
        ),
        _case(
            "B07",
            "feedback",
            "permission hard block terminal stop",
            force_action_permission_revoked=True,
            permission_hard_block_probe=True,
        ),
        _case(
            "B08",
            "feedback",
            "retry authority exhausted terminal stop",
            force_runtime_failure=True,
            retry_authority_exhausted_probe=True,
        ),
        _case(
            "C01",
            "compatibility",
            "incompatible version handoff rejected",
            force_version_incompatible_hop="H2",
        ),
        _case(
            "C02",
            "compatibility",
            "missing trace ref rejected",
            force_missing_trace_hop="H3",
        ),
        _case(
            "C03",
            "compatibility",
            "duplicate handoff no duplicate consumption",
            duplicate_handoff_probe=True,
        ),
        _case(
            "C04",
            "compatibility",
            "duplicate action handoff no duplicate execution request",
            duplicate_action_handoff_probe=True,
        ),
        _case(
            "C05",
            "compatibility",
            "duplicate feedback no duplicate reconsideration",
            force_runtime_failure=True,
            duplicate_feedback_probe=True,
        ),
        _case("C06", "compatibility", "provenance reverse lookup complete"),
    )
