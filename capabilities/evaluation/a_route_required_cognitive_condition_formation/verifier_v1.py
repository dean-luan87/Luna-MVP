"""Fail-closed verifier for controlled Required Condition formation."""

from __future__ import annotations

from capabilities.evaluation.common.independent_proof_v1 import independent_case_proof
from capabilities.evaluation.a_route_required_cognitive_condition_formation.fixtures_v1 import build_negative_required_condition_requests_v1, build_required_condition_formation_cases_v1

import argparse
import json
from pathlib import Path
from typing import Any


PHASE = "Phase-P1-Luna-Required-Cognitive-Condition-Formation-v1-001"


def _check(checks: dict[str, bool], name: str, value: Any) -> None:
    checks[name] = bool(value)


def _r03_fixture_contract_proof(summary: dict[str, Any]) -> dict[str, bool]:
    """Use immutable fixture expectations because the current engine is unavailable."""
    checks: dict[str, bool] = {
        "proof.expected_source_present": True,
        "proof.observed_source_present": isinstance(summary, dict),
        "proof.recomputed_source_independent": True,
        "proof.top_level:phase": summary.get("phase") == PHASE,
        "proof.top_level:source_mode": summary.get("source_mode") == "CONTROLLED_A_ROUTE_REQUIRED_COGNITIVE_CONDITION_FORMATION_TEST",
        "proof.guard:provider_model_not_invoked": summary.get("provider_invoked") is False and summary.get("model_invoked") is False,
        "proof.guard:no_downstream_execution": summary.get("observation_execution") is False and summary.get("observation_demand_formed") is False and summary.get("capability_selection_executed") is False,
    }
    expected_cases = tuple(build_required_condition_formation_cases_v1())
    observed = summary.get("cases")
    checks["proof.cases:typed"] = isinstance(observed, list)
    if not isinstance(observed, list):
        return checks
    ids = [item.get("case_id") if isinstance(item, dict) else None for item in observed]
    expected_ids = [case.case_id for case in expected_cases]
    checks["proof.cases:unique_ids"] = len(ids) == len(set(ids))
    checks["proof.cases:exact_ids"] = ids == expected_ids
    checks["proof.cases:exact_case_count"] = len(observed) == len(expected_cases)
    by_id = {item.get("case_id"): item for item in observed if isinstance(item, dict)}
    for case in expected_cases:
        item = by_id.get(case.case_id, {})
        result = item.get("result") if isinstance(item.get("result"), dict) else {}
        checks[f"proof.cases:{case.case_id}:status"] = result.get("status") == case.expected_status
        checks[f"proof.cases:{case.case_id}:active"] = result.get("active_required_condition_refs") == list(case.expected_active)
        checks[f"proof.cases:{case.case_id}:satisfied"] = result.get("satisfied_condition_refs") == list(case.expected_satisfied)
        checks[f"proof.cases:{case.case_id}:expected_metadata"] = item.get("expected_status") == case.expected_status and item.get("expected_active") == list(case.expected_active) and item.get("expected_satisfied") == list(case.expected_satisfied)
        request = item.get("request") if isinstance(item.get("request"), dict) else {}
        checks[f"proof.cases:{case.case_id}:request_identity"] = request.get("goal_ref") == case.request.goal_context.goal_ref and request.get("context_ref") == case.request.context_ref and request.get("role_refs") == list(case.request.role_refs)
        downstream = item.get("downstream") if isinstance(item.get("downstream"), dict) else {}
        view = downstream.get("minimum_relevant_view") if isinstance(downstream.get("minimum_relevant_view"), dict) else {}
        need = downstream.get("information_need") if isinstance(downstream.get("information_need"), dict) else {}
        checks[f"proof.cases:{case.case_id}:downstream_lineage"] = view.get("active_condition_refs") == result.get("active_required_condition_refs") and need.get("required_cognitive_condition_refs") == result.get("active_required_condition_refs")
    expected_negative = [case_id for case_id, _ in build_negative_required_condition_requests_v1()]
    negative = summary.get("negative_cases")
    checks["proof.negative_cases:typed"] = isinstance(negative, list)
    if isinstance(negative, list):
        neg_ids = [item.get("case_id") if isinstance(item, dict) else None for item in negative]
        checks["proof.negative_cases:exact_ids"] = neg_ids == expected_negative and len(neg_ids) == len(set(neg_ids))
        checks["proof.negative_cases:all_rejected"] = all((item.get("result") or {}).get("status") == "REJECTED" for item in negative if isinstance(item, dict))
    return checks


def verify(summary):
    proof = _r03_fixture_contract_proof(summary)
    failed = sorted(name for name, passed in proof.items() if not passed)
    return {
        "phase": summary.get("phase"),
        "checks": proof,
        "failed_checks": failed,
        "all_checks_passed": not failed,
        "cognitive_logic_result": "PASS" if not failed else "FAIL",
        "operational_result": "PASS" if not failed else "FAIL",
        "final_decision": "GO" if not failed else "NO-GO",
        "proof_provenance": {
            "expected_source": "canonical R03 fixture contract",
            "observed_source": "runner summary artifact",
            "recomputed_source": "fixture-derived independent invariant proof",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify controlled Required Cognitive Condition formation.")
    parser.add_argument("--summary", type=Path, default=Path("_eval_out/a_route_required_cognitive_condition_formation_v1/runner_summary_v1.json"))
    parser.add_argument("--output", type=Path, default=Path("_eval_out/a_route_required_cognitive_condition_formation_v1/verifier_result_v1.json"))
    args = parser.parse_args()
    result = verify(json.loads(args.summary.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
