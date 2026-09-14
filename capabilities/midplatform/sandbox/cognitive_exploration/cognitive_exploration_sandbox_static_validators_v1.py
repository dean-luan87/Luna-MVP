"""Static contract validators for sandbox trace output."""

from __future__ import annotations

from typing import Any, Dict, Iterable, Tuple


REQUIRED_SCENARIO_IDS = {
    "SCENARIO_01_SINGLE_CLEAR_CUE",
    "SCENARIO_02_UNKNOWN_EXIT",
    "SCENARIO_03_SIGNAGE_AND_HUMAN_FLOW_AGREE",
    "SCENARIO_04_SIGNAGE_AND_HUMAN_FLOW_CONFLICT",
    "SCENARIO_05_SIGNAGE_NOT_VISIBLE",
    "SCENARIO_06_OCR_CONDITIONS_INSUFFICIENT",
    "SCENARIO_07_MULTIPLE_UNKNOWNS",
    "SCENARIO_08_DEFERRED_BRANCH",
    "SCENARIO_09_REJECTED_BRANCH",
    "SCENARIO_10_NO_ACQUISITION_STRATEGY_AVAILABLE",
    "SCENARIO_11_IRRELEVANT_ENVIRONMENTAL_CHANGE",
    "SCENARIO_12_EVIDENCE_CHANGES_COGNITIVE_BASIS",
}


def check_trace_contract(trace: Dict[str, Any]) -> Tuple[Dict[str, bool], list[str]]:
    checks: Dict[str, bool] = {}
    cases = trace.get("scenarios") or []
    case_map = {case.get("scenario_id"): case for case in cases}

    checks["scenario_count_at_least_12"] = trace.get("scenario_count", 0) >= 12
    checks["required_scenario_ids"] = REQUIRED_SCENARIO_IDS.issubset(case_map)
    checks["synthetic_only"] = trace.get("synthetic_only") is True

    guards = trace.get("negative_guard_summary") or {}
    for name, expected in (
        ("provider_execution", False),
        ("model_execution", False),
        ("ocr_execution", False),
        ("capability_execution", False),
        ("observation_demand_implementation", False),
        ("strategy_coordination_implementation", False),
        ("decision_execution", False),
        ("task_execution", False),
        ("action_execution", False),
        ("canonical_cognition_mutation", False),
        ("canonical_ownership_transfer", False),
        ("autonomous_infinite_loop", False),
        ("winner_selection", False),
        ("strategy_fabrication", False),
        ("hidden_fallback_strategy", False),
        ("synthetic_evidence_as_real", False),
    ):
        checks[f"guard:{name}"] = guards.get(name) is expected

    for case in cases:
        case_id = case.get("scenario_id", "missing")
        checks[f"{case_id}:round_0"] = isinstance(case.get("round_0"), dict)
        round_zero = case.get("round_0") or {}
        checks[f"{case_id}:trace_schema"] = all(
            key in round_zero
            for key in (
                "problem",
                "required_conditions",
                "required_condition_refs",
                "information_needs",
                "branches",
                "governance_result",
                "strategy_candidates",
                "cognitive_economy",
            )
        )
        simulated = case.get("simulated_return")
        round_one = case.get("round_1")
        checks[f"{case_id}:round_1_requires_return"] = round_one is None or simulated is not None
        if simulated is not None:
            checks[f"{case_id}:simulated_return_marked"] = (
                simulated.get("sandbox_only") is True
                and simulated.get("synthetic") is True
                and simulated.get("runtime_acquisition") is False
                and simulated.get("provider_executed") is False
                and simulated.get("capability_executed") is False
            )
        strategy_candidates = round_zero.get("strategy_candidates") or []
        governance = round_zero.get("governance_result") or {}
        admitted = set(governance.get("admitted_branch_refs") or [])
        checks[f"{case_id}:strategies_admitted_only"] = all(
            strategy.get("branch_ref") in admitted for strategy in strategy_candidates
        )
        checks[f"{case_id}:lineage_integrity"] = bool(
            (case.get("lineage_integrity") or {}).get("round_0", {}).get("valid") is True
        )
        checks[f"{case_id}:strategy_candidate_flags"] = all(
            strategy.get("candidate_only") is True
            and strategy.get("read_only") is True
            and strategy.get("truth_declared") is False
            and strategy.get("world_truth_declared") is False
            for strategy in strategy_candidates
        )
        nested_results = [
            round_zero.get("information_need_result") or {},
            round_zero.get("branch_formation_result") or {},
            round_zero.get("governance_result") or {},
            round_zero.get("strategy_formation_result") or {},
        ]
        mutation_or_execution_fields = (
            "goal_mutation",
            "intent_mutation",
            "concern_mutation",
            "role_mutation",
            "context_mutation",
            "field_mutation",
            "self_mutation",
            "current_world_mutation",
            "memory_mutation",
            "pcn_mutation",
            "provider_invocation",
            "model_invocation",
            "observation_execution",
            "observation_demand_formed",
            "capability_selection_executed",
            "decision_execution",
            "task_execution",
            "action_execution",
            "truth_declared",
            "world_truth_declared",
        )
        checks[f"{case_id}:canonical_outputs_non_mutating"] = all(
            result.get(field) is False
            for result in nested_results
            for field in mutation_or_execution_fields
            if field in result
        )
        if round_one is not None:
            checks[f"{case_id}:delta_schema"] = all(
                key in (case.get("cognitive_delta") or {})
                for key in (
                    "needs_added",
                    "needs_removed",
                    "needs_retained",
                    "branches_added",
                    "branches_removed",
                    "branches_retained",
                    "strategies_added",
                    "strategies_removed",
                    "strategies_retained",
                    "unresolved_gap_before",
                    "unresolved_gap_after",
                )
            )
            checks[f"{case_id}:round_1_lineage_integrity"] = bool(
                (case.get("lineage_integrity") or {}).get("round_1", {}).get("valid") is True
            )

    no_strategy = case_map.get("SCENARIO_10_NO_ACQUISITION_STRATEGY_AVAILABLE", {})
    checks["strategy_zero_case_allowed"] = not (
        (no_strategy.get("round_0") or {}).get("strategy_candidates") or []
    )
    deferred = case_map.get("SCENARIO_08_DEFERRED_BRANCH", {})
    deferred_result = (deferred.get("round_0") or {}).get("governance_result") or {}
    deferred_refs = set(deferred_result.get("deferred_branch_refs") or [])
    checks["deferred_branch_not_active_strategy"] = not any(
        strategy.get("branch_ref") in deferred_refs
        for strategy in ((deferred.get("round_0") or {}).get("strategy_candidates") or [])
    )
    rejected = case_map.get("SCENARIO_09_REJECTED_BRANCH", {})
    rejected_result = (rejected.get("round_0") or {}).get("governance_result") or {}
    rejected_refs = set(rejected_result.get("rejected_branch_refs") or [])
    checks["rejected_branch_not_active_strategy"] = not any(
        strategy.get("branch_ref") in rejected_refs
        for strategy in ((rejected.get("round_0") or {}).get("strategy_candidates") or [])
    )
    checks["irrelevant_change_scenario_present"] = "SCENARIO_11_IRRELEVANT_ENVIRONMENTAL_CHANGE" in case_map
    checks["evidence_update_scenario_present"] = "SCENARIO_12_EVIDENCE_CHANGES_COGNITIVE_BASIS" in case_map
    checks["economy_metrics_present"] = all(
        "cognitive_economy" in ((case.get("round_0") or {})) for case in cases
    )
    checks["deterministic_trace_version_present"] = bool(trace.get("sandbox_version"))

    failed = sorted(name for name, passed in checks.items() if not passed)
    return checks, failed


__all__ = ["REQUIRED_SCENARIO_IDS", "check_trace_contract"]
