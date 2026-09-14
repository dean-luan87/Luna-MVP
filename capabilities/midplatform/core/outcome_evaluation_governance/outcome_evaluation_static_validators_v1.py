"""Pure validators for candidate-only Outcome Evaluation output."""

from .outcome_evaluation_core_types_v1 import OutcomeEvaluationOutputV1
from .outcome_evaluation_registry_v1 import COMPARABILITY_STATES, DEVIATION_STATUSES, RECOMMENDATIONS


def validate_output(output: OutcomeEvaluationOutputV1) -> tuple[str, ...]:
    issues: list[str] = []
    if output.comparability.state not in COMPARABILITY_STATES:
        issues.append("invalid_comparability_state")
    if output.deviation.status not in DEVIATION_STATUSES:
        issues.append("invalid_deviation_status")
    if output.reconsideration is not None and output.reconsideration.recommendation not in RECOMMENDATIONS:
        issues.append("invalid_reconsideration_recommendation")
    if output.evaluation.candidate_only is not True:
        issues.append("evaluation_not_candidate_only")
    if output.evaluation.truth_declared is not False:
        issues.append("evaluation_declares_truth")
    if output.evaluation.mutation_authority is not False:
        issues.append("evaluation_has_mutation_authority")
    if output.trace.provenance_grants_authority is not False:
        issues.append("provenance_grants_authority")
    if output.reconsideration is not None and output.reconsideration.executes_reconsideration:
        issues.append("reconsideration_executed")
    if output.learning_signal is not None and output.learning_signal.learning_executed:
        issues.append("learning_executed")
    if output.observation_need is not None and output.observation_need.provider_invocation:
        issues.append("provider_invoked")
    if any(value is not False for value in output.guards.values()):
        issues.append("negative_guard_open")
    return tuple(issues)
