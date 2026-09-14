from __future__ import annotations

from typing import Any, Dict, Iterable, Tuple

from .policy_evaluation_types_v1 import ConditionResult, ConditionRule, EvaluationInput


def _path_get(payload: Dict[str, Any], path: str) -> Tuple[bool, Any]:
    if not path:
        return False, None
    cur: Any = payload
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return False, None
    return True, cur


def _as_set(value: Any) -> set:
    if value is None:
        return set()
    if isinstance(value, (tuple, list, set)):
        return set(value)
    return {value}


def evaluate_operator(operator: str, actual: Any, expected: Any) -> bool:
    if operator == "equals":
        return actual == expected
    if operator == "not_equals":
        return actual != expected
    if operator == "in":
        return actual in _as_set(expected)
    if operator == "not_in":
        return actual not in _as_set(expected)
    if operator == "greater_than":
        return (
            isinstance(actual, (int, float))
            and isinstance(expected, (int, float))
            and actual > expected
        )
    if operator == "greater_than_or_equal":
        return (
            isinstance(actual, (int, float))
            and isinstance(expected, (int, float))
            and actual >= expected
        )
    if operator == "less_than":
        return (
            isinstance(actual, (int, float))
            and isinstance(expected, (int, float))
            and actual < expected
        )
    if operator == "less_than_or_equal":
        return (
            isinstance(actual, (int, float))
            and isinstance(expected, (int, float))
            and actual <= expected
        )
    if operator == "exists":
        return actual is not None
    if operator == "not_exists":
        return actual is None
    if operator == "all_of":
        return _as_set(expected).issubset(_as_set(actual))
    if operator == "any_of":
        return len(_as_set(expected).intersection(_as_set(actual))) > 0
    if operator == "none_of":
        return len(_as_set(expected).intersection(_as_set(actual))) == 0
    if operator == "minimum_count":
        return (
            isinstance(actual, (list, tuple, set))
            and isinstance(expected, (int, float))
            and len(actual) >= int(expected)
        )
    if operator == "maximum_count":
        return (
            isinstance(actual, (list, tuple, set))
            and isinstance(expected, (int, float))
            and len(actual) <= int(expected)
        )
    return False


def evaluate_condition_rule(
    rule: ConditionRule, evaluation_input: EvaluationInput
) -> ConditionResult:
    payload = {
        "state_type": evaluation_input.state_type,
        "policy_id": evaluation_input.policy_id,
        "admitted_events": evaluation_input.admitted_events,
        "existing_state_snapshot": evaluation_input.existing_state_snapshot,
        "temporal_snapshot": evaluation_input.temporal_snapshot,
        "confidence_policy_snapshot": evaluation_input.confidence_policy_snapshot,
        "conflict_snapshot": evaluation_input.conflict_snapshot,
        "owner_correction_snapshot": evaluation_input.owner_correction_snapshot,
        "overlay_snapshot": evaluation_input.overlay_snapshot,
        "provenance_snapshot": evaluation_input.provenance_snapshot,
        "governance_snapshot": evaluation_input.governance_snapshot,
        "policy_registry_version": evaluation_input.policy_registry_version,
        "eligibility_matrix_version": evaluation_input.eligibility_matrix_version,
        "evaluation_contract_version": evaluation_input.evaluation_contract_version,
    }
    found, actual = _path_get(payload, rule.input_path)
    if not found:
        return ConditionResult(
            rule_id=rule.rule_id,
            policy_id=rule.policy_id,
            passed=False,
            blocking=rule.blocking,
            missing_inputs=(rule.input_path,),
            rejection_reason=rule.rejection_reason,
            actual_value=None,
        )
    passed = evaluate_operator(rule.operator, actual, rule.expected_value)
    return ConditionResult(
        rule_id=rule.rule_id,
        policy_id=rule.policy_id,
        passed=passed,
        blocking=rule.blocking,
        missing_inputs=tuple(),
        rejection_reason=None if passed else rule.rejection_reason,
        actual_value=actual,
    )


def evaluate_conditions(
    rules: Iterable[ConditionRule], evaluation_input: EvaluationInput
) -> Tuple[ConditionResult, ...]:
    return tuple(evaluate_condition_rule(rule, evaluation_input) for rule in rules)
