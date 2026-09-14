from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.core.field_state_reducer.behavior_policy.policy_selection import (  # noqa: E402
    PolicySelectionInput,
    result_to_dict,
    select_policy_v1,
)


def _evaluation_row(
    evaluation_id: str,
    policy_id: str,
    status: str,
    allowed: bool,
) -> Dict[str, Any]:
    return {
        "evaluation_id": evaluation_id,
        "policy_id": policy_id,
        "state_type": "presence_state",
        "evaluation_status": status,
        "selection_candidate_allowed": allowed,
        "policy_selection_executed": False,
        "policy_execution_executed": False,
        "state_mutation_executed": False,
        "fact_promotion_executed": False,
        "action_trigger_executed": False,
        "runtime_execution": False,
    }


def _selection_input(case_id: str, rows: List[Dict[str, Any]]) -> PolicySelectionInput:
    return PolicySelectionInput(
        selection_id=f"selection_{case_id}",
        reducer_run_id=f"run_{case_id}",
        field_id="field_001",
        state_type="presence_state",
        evaluation_results=tuple(rows),
        policy_registry_version="v1",
        eligibility_matrix_version="v1",
        precedence_matrix_version="v1",
        composition_contract_version="v1",
        replay_contract_version="v1",
    )


def run_field_state_reducer_policy_selection_integration_v1() -> Dict[str, Any]:
    cases: List[Tuple[str, str, List[str], List[Dict[str, Any]]]] = []

    cases.append(
        (
            "single_eligible_candidate",
            "selected_single",
            ["latest_valid_event"],
            [
                _evaluation_row("e1", "latest_valid_event", "eligible_candidate", True),
            ],
        )
    )

    cases.append(
        (
            "multiple_candidates_with_precedence",
            "selected_single",
            ["multi_event_consensus"],
            [
                _evaluation_row(
                    "e1", "multi_event_consensus", "eligible_candidate", True
                ),
                _evaluation_row(
                    "e2", "highest_confidence_valid_event", "eligible_candidate", True
                ),
            ],
        )
    )

    cases.append(
        (
            "revocation_override",
            "selected_single",
            ["revocation_override"],
            [
                _evaluation_row(
                    "e1", "revocation_override", "eligible_candidate", True
                ),
                _evaluation_row("e2", "latest_valid_event", "eligible_candidate", True),
            ],
        )
    )

    cases.append(
        (
            "conflict_preservation",
            "selected_single",
            ["conflict_preservation"],
            [
                _evaluation_row(
                    "e1", "conflict_preservation", "eligible_candidate", True
                ),
                _evaluation_row(
                    "e2", "highest_confidence_valid_event", "eligible_candidate", True
                ),
            ],
        )
    )

    cases.append(
        (
            "mutually_exclusive_candidates",
            "selected_single",
            ["revocation_override"],
            [
                _evaluation_row(
                    "e1", "revocation_override", "eligible_candidate", True
                ),
                _evaluation_row(
                    "e2", "highest_confidence_valid_event", "eligible_candidate", True
                ),
            ],
        )
    )

    cases.append(
        (
            "valid_composition",
            "selected_composition",
            ["multi_event_consensus", "explicit_owner_override_candidate"],
            [
                _evaluation_row(
                    "e1", "multi_event_consensus", "eligible_candidate", True
                ),
                _evaluation_row(
                    "e2",
                    "explicit_owner_override_candidate",
                    "eligible_candidate",
                    True,
                ),
            ],
        )
    )

    cases.append(
        (
            "composition_depth_overflow",
            "selected_single",
            ["revocation_override"],
            [
                _evaluation_row(
                    "e1", "revocation_override", "eligible_candidate", True
                ),
                _evaluation_row("e2", "no_state_change", "eligible_candidate", True),
                _evaluation_row(
                    "e3", "conflict_preservation", "eligible_candidate", True
                ),
                _evaluation_row(
                    "e4", "insufficient_evidence_unresolved", "eligible_candidate", True
                ),
            ],
        )
    )

    cases.append(
        (
            "deterministic_tie",
            "selected_single",
            ["highest_confidence_valid_event"],
            [
                _evaluation_row("e1", "latest_valid_event", "eligible_candidate", True),
                _evaluation_row(
                    "e2", "highest_confidence_valid_event", "eligible_candidate", True
                ),
            ],
        )
    )

    cases.append(
        (
            "no_eligible_candidate",
            "no_eligible_candidate",
            [],
            [
                _evaluation_row("e1", "latest_valid_event", "ineligible", False),
                _evaluation_row(
                    "e2", "highest_confidence_valid_event", "blocked", False
                ),
            ],
        )
    )

    cases.append(
        (
            "governance_review_candidate_excluded",
            "selected_single",
            ["latest_valid_event"],
            [
                _evaluation_row(
                    "e1",
                    "explicit_owner_override_candidate",
                    "governance_review_required",
                    False,
                ),
                _evaluation_row("e2", "latest_valid_event", "eligible_candidate", True),
            ],
        )
    )

    cases.append(
        (
            "unresolved_conflict_candidate_excluded",
            "selected_single",
            ["latest_valid_event"],
            [
                _evaluation_row(
                    "e1", "conflict_preservation", "unresolved_conflict", False
                ),
                _evaluation_row("e2", "latest_valid_event", "eligible_candidate", True),
            ],
        )
    )

    cases.append(
        (
            "no_state_change_fallback",
            "no_state_change",
            ["no_state_change"],
            [
                _evaluation_row("e1", "no_state_change", "eligible_candidate", True),
            ],
        )
    )

    results: List[Dict[str, Any]] = []
    failed_cases: List[str] = []

    for case_id, expected_status, expected_selected, rows in cases:
        selection_input = _selection_input(case_id, rows)
        result, trace = select_policy_v1(selection_input)
        row = result_to_dict(result)
        row["trace_present"] = bool(trace.trace_id)
        row["case_id"] = case_id
        row["expected_status"] = expected_status
        row["expected_selected_policy_ids"] = expected_selected
        row["status_matched"] = row["selection_status"] == expected_status
        row["selected_matched"] = row["selected_policy_ids"] == expected_selected
        row["matched"] = row["status_matched"] and row["selected_matched"]
        results.append(row)
        if not row["matched"]:
            failed_cases.append(case_id)

    boundary_ok = all(
        r["policy_execution_executed"] is False
        and r["state_mutation_executed"] is False
        and r["fact_promotion_executed"] is False
        and r["action_trigger_executed"] is False
        and r["runtime_execution"] is False
        for r in results
    )

    report = {
        "module": "Field State Reducer Policy Selection",
        "execution_mode": "Function Module Engineering Build",
        "total_cases": len(cases),
        "passed_cases": len(cases) - len(failed_cases),
        "failed_cases": failed_cases,
        "trace_present_all": all(bool(r.get("trace_present")) for r in results),
        "replay_present_all": all(bool(r.get("replay_key")) for r in results),
        "boundary_preserved": boundary_ok,
        "module_status": {
            "selection_types_implemented": True,
            "candidate_filter_implemented": True,
            "precedence_resolver_implemented": True,
            "exclusion_resolver_implemented": True,
            "composition_eligibility_implemented": True,
            "deterministic_tie_breaker_implemented": True,
            "selection_orchestrator_implemented": True,
            "trace_replay_implemented": True,
            "integration_runner_created": True,
            "policy_execution_implemented": False,
            "state_mutation_implemented": False,
            "runtime_implemented": False,
        },
        "results": results,
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


if __name__ == "__main__":
    out = run_field_state_reducer_policy_selection_integration_v1()
    raise SystemExit(0 if not out.get("failed_cases") else 1)
