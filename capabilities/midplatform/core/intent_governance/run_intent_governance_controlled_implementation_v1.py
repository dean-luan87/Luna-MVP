"""Controlled runner for Intent Governance implementation v1.

This runner is intended for user-terminal execution only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


REPO_ROOT = Path(__file__).resolve().parents[4]

if __package__ in {None, ""}:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.intent_governance.intent_governance_fixture_v1 import (
    get_intent_synthetic_fixtures_v1,
)
from capabilities.midplatform.core.intent_governance.intent_governance_skeleton_v1 import (
    IntentGovernanceSkeletonV1,
)
from capabilities.midplatform.core.intent_governance.intent_static_validators_v1 import (
    validate_handoff_candidate,
    validate_input_refs_read_only,
    validate_intent_candidate,
    validate_interaction_candidate,
    validate_no_runtime_or_mutation,
    validate_potential_intent,
)


OUTPUT_DIR = REPO_ROOT / "_eval_out/intent_governance_controlled_implementation_v1"


def run_controlled() -> Dict[str, Any]:
    skeleton = IntentGovernanceSkeletonV1()
    cases = get_intent_synthetic_fixtures_v1()
    case_results: List[Dict[str, Any]] = []
    traces: List[Dict[str, Any]] = []

    for case in cases:
        output = skeleton.run_case(case.request)
        refs = (
            case.request.source_refs
            + case.request.context_refs
            + case.request.pcn_refs
            + case.request.self_refs
            + case.request.field_refs
            + case.request.role_refs
            + case.request.relationship_refs
            + case.request.memory_refs
            + case.request.experience_refs
            + case.request.emotion_refs
        )
        intent = output.intent_candidates[0]
        potential = output.potential_intents[0]
        interaction = output.interaction_candidates[0]

        checks = {
            "input_refs_read_only": validate_input_refs_read_only(refs),
            "potential_candidate_valid": validate_potential_intent(potential),
            "intent_candidate_valid": validate_intent_candidate(intent),
            "interaction_valid": validate_interaction_candidate(interaction),
            "handoff_valid": validate_handoff_candidate(output.handoff_candidate),
            "no_runtime_or_mutation": validate_no_runtime_or_mutation(
                output.intent_candidates
            ),
            "candidate_only": output.candidate_only is True,
            "synthetic_only": case.synthetic_only is True
            and case.request.synthetic_only is True,
        }

        low_resource = case.low_resource_mode
        omissions = list(output.trace_candidate.omissions)
        if low_resource and not omissions:
            omissions = ["projection_breadth_reduced"]

        case_results.append(
            {
                "case_id": case.case_id,
                "description": case.description,
                "expected_relations": list(case.expected_relations),
                "expected_interactions": list(case.expected_interactions),
                "interaction_type": interaction.interaction_type,
                "future_state_relation": intent.future_state_relation,
                "state_candidate": intent.state_candidate,
                "carryover_candidate": intent.carryover_candidate,
                "low_resource_mode": low_resource,
                "omissions": omissions,
                "checks": checks,
                "all_checks_passed": all(checks.values()),
            }
        )

        traces.append(
            {
                "case_id": case.case_id,
                "trace_id": output.trace_candidate.trace_id,
                "unknowns": list(output.trace_candidate.unknowns),
                "omissions": list(output.trace_candidate.omissions),
                "handoff_id": output.handoff_candidate.handoff_id,
            }
        )

    passed = sum(1 for item in case_results if item["all_checks_passed"])
    summary = {
        "phase": "Phase-Luna-Intent-Governance-Controlled-Implementation-v1-001",
        "case_count": len(case_results),
        "passed_case_count": passed,
        "failed_case_count": len(case_results) - passed,
        "candidate_only": True,
        "runtime_executed": False,
        "source_mutation_executed": False,
        "status": "INTENT_GOVERNANCE_CONTROLLED_IMPLEMENTATION_RESULT_CANDIDATE_READY",
    }

    return {
        "summary": summary,
        "case_results": case_results,
        "trace": {
            "trace_id": "intent-governance-controlled-implementation-trace-v1",
            "case_traces": traces,
            "candidate_only": True,
        },
    }


def write_outputs(payload: Dict[str, Any]) -> Dict[str, str]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result_path = OUTPUT_DIR / "intent_governance_result_v1.json"
    cases_path = OUTPUT_DIR / "intent_governance_case_results_v1.json"
    trace_path = OUTPUT_DIR / "intent_governance_trace_v1.json"

    result_path.write_text(
        json.dumps(payload["summary"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    cases_path.write_text(
        json.dumps(payload["case_results"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    trace_path.write_text(
        json.dumps(payload["trace"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    return {
        "result": str(result_path),
        "cases": str(cases_path),
        "trace": str(trace_path),
    }


def main() -> int:
    payload = run_controlled()
    write_outputs(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
