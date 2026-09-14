"""Pure A3 controlled-skeleton invariants v1."""

from __future__ import annotations

from typing import Tuple

from .cognitive_analysis_types_v1 import CognitiveAnalysisResultV1, ObservationRequestCandidateV1


DIRECT_INPUT_TYPE_V1 = "CurrentCognitiveContextV1"
FIELD_STATE_MUTATION_AUTHORITY_V1 = "FieldStateReducer"
SIMULATION_ONLY_V1 = True
RUNTIME_EXECUTED_V1 = False
OBSERVATION_EXECUTION_ADMITTED_V1 = False
DECISION_BOUNDARY_ADMITTED_V1 = False
STATE_WRITEBACK_ADMITTED_V1 = False

FORBIDDEN_CAPABILITIES_V1 = (
    "raw_observation_access", "model_invocation", "network_access",
    "database_access", "system_time_access", "randomness",
    "uuid_auto_generation", "action_execution", "decision_execution",
    "field_state_writeback", "context_writeback", "snapshot_writeback",
)


def observation_request_invariant_issues_v1(request: ObservationRequestCandidateV1) -> Tuple[str, ...]:
    """Return stable candidate-only violations for one observation request."""
    return ("observation_request_execution_must_be_false",) if request.execution_admitted else ()


def result_boundary_invariant_issues_v1(result: CognitiveAnalysisResultV1) -> Tuple[str, ...]:
    """Return stable non-runtime/writeback violations for one result."""
    issues = []
    if result.decision_boundary_admitted:
        issues.append("decision_boundary_admitted_must_be_false")
    if result.state_writeback_admitted:
        issues.append("state_writeback_admitted_must_be_false")
    if result.runtime_executed:
        issues.append("runtime_executed_must_be_false")
    if not result.simulation_only:
        issues.append("simulation_only_must_be_true")
    return tuple(issues)
