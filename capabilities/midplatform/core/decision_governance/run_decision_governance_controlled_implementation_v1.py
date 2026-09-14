"""Controlled runner for Decision Governance implementation v1.

This runner is intended for user-terminal execution only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def _resolve_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in current.parents:
        if (candidate / "capabilities/midplatform/core/decision_governance").is_dir():
            return candidate

    cwd = Path.cwd().resolve()
    if (cwd / "capabilities/midplatform/core/decision_governance").is_dir():
        return cwd

    return Path(__file__).resolve().parents[4]


REPO_ROOT = _resolve_repo_root()

if __package__ in {None, ""}:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.decision_governance.decision_governance_engine_v1 import (
    DecisionGovernanceEngineV1,
)
from capabilities.midplatform.core.decision_governance.decision_governance_fixture_v1 import (
    get_decision_synthetic_fixtures_v1,
)
from capabilities.midplatform.core.decision_governance.decision_static_validators_v1 import (
    validate_candidates,
    validate_handoff,
    validate_input_refs_read_only,
    validate_negative_guard_flags,
    validate_no_runtime_side_effects,
    validate_option,
    validate_trace_completeness,
)


OUTPUT_DIR = REPO_ROOT / "_eval_out/decision_governance_controlled_implementation_v1"


def run_controlled() -> Dict[str, Any]:
    engine = DecisionGovernanceEngineV1()
    fixtures = get_decision_synthetic_fixtures_v1()

    case_results: List[Dict[str, Any]] = []
    traces: List[Dict[str, Any]] = []

    for case in fixtures:
        output = engine.run_case(case.request)
        all_refs = (
            case.request.intent_refs
            + case.request.causal_refs
            + case.request.context_refs
            + case.request.field_refs
            + case.request.role_refs
            + case.request.permission_refs
            + case.request.safety_refs
            + case.request.resource_refs
            + case.request.constraint_refs
            + case.request.evidence_refs
        )

        checks = {
            "input_refs_read_only": validate_input_refs_read_only(all_refs),
            "options_valid": all(
                validate_option(item) for item in case.request.options
            ),
            "decision_candidates_valid": validate_candidates(
                output.decision_candidates
            ),
            "trace_complete": validate_trace_completeness(output),
            "handoff_valid": validate_handoff(output.handoff_candidate),
            "negative_guard_flags": validate_negative_guard_flags(),
            "no_runtime_side_effects": validate_no_runtime_side_effects(output),
            "state_expected": output.state == case.expected_state,
            "outcome_expected": output.outcome_kind == case.expected_outcome_kind,
            "selection_expected": (
                output.selection_candidate.selected_candidate_ref is None
                if case.expected_selected_option is None
                else any(
                    c.option_id == case.expected_selected_option
                    and c.decision_candidate_id
                    == output.selection_candidate.selected_candidate_ref
                    for c in output.decision_candidates
                )
            ),
            "handoff_eligibility_expected": (
                output.handoff_candidate.execution_eligibility_candidate
                is case.expected_handoff_eligible
            ),
            "synthetic_only": case.synthetic_only is True
            and case.request.synthetic_only is True,
        }

        selected_option_id = None
        for candidate in output.decision_candidates:
            if (
                candidate.decision_candidate_id
                == output.selection_candidate.selected_candidate_ref
            ):
                selected_option_id = candidate.option_id
                break

        case_results.append(
            {
                "case_id": case.case_id,
                "description": case.description,
                "input_refs": {
                    "intent_refs": [r.ref_id for r in case.request.intent_refs],
                    "causal_refs": [r.ref_id for r in case.request.causal_refs],
                    "context_refs": [r.ref_id for r in case.request.context_refs],
                    "field_refs": [r.ref_id for r in case.request.field_refs],
                    "role_refs": [r.ref_id for r in case.request.role_refs],
                    "permission_refs": [r.ref_id for r in case.request.permission_refs],
                    "safety_refs": [r.ref_id for r in case.request.safety_refs],
                    "resource_refs": [r.ref_id for r in case.request.resource_refs],
                    "constraint_refs": [r.ref_id for r in case.request.constraint_refs],
                    "evidence_refs": [r.ref_id for r in case.request.evidence_refs],
                },
                "option_result": [
                    {
                        "option_id": c.option_id,
                        "eligible": c.eligibility_candidate,
                        "veto_reasons": list(c.veto_reasons),
                    }
                    for c in output.decision_candidates
                ],
                "state": output.state,
                "outcome_kind": output.outcome_kind,
                "selected_option_id": selected_option_id,
                "risk_utility_constraints": {
                    "utility_scores": {
                        c.option_id: c.utility_score_candidate
                        for c in output.decision_candidates
                    },
                    "risk_scores": {
                        c.option_id: c.risk_score_candidate
                        for c in output.decision_candidates
                    },
                    "constraint_refs": [r.ref_id for r in case.request.constraint_refs],
                },
                "permission_safety": {
                    "permission_refs": [r.ref_id for r in case.request.permission_refs],
                    "safety_refs": [r.ref_id for r in case.request.safety_refs],
                },
                "reversibility": {
                    c.option_id: c.reversibility for c in output.decision_candidates
                },
                "confirmation_requirement": output.selection_candidate.confirmation_requirement,
                "provenance": list(output.trace_candidate.provenance),
                "expected_negative_guards": list(case.expected_negative_guards),
                "handoff_eligibility": output.handoff_candidate.execution_eligibility_candidate,
                "checks": checks,
                "all_checks_passed": all(checks.values()),
            }
        )

        traces.append(
            {
                "case_id": case.case_id,
                "trace_id": output.trace_candidate.trace_id,
                "decision_candidate_refs": list(
                    output.trace_candidate.decision_candidate_refs
                ),
                "selection_reason_refs": list(
                    output.trace_candidate.selection_or_nonselection_reason_refs
                ),
                "state_transition_refs": list(
                    output.trace_candidate.state_transition_refs
                ),
                "handoff_id": output.handoff_candidate.handoff_id,
            }
        )

    passed = sum(1 for item in case_results if item["all_checks_passed"])
    summary = {
        "phase": "Phase-Luna-Decision-Governance-Controlled-Implementation-v1-001",
        "case_count": len(case_results),
        "passed_case_count": passed,
        "failed_case_count": len(case_results) - passed,
        "candidate_only": True,
        "runtime_executed": False,
        "database_write_executed": False,
        "source_mutation_executed": False,
        "decision_output": False,
        "action_output": False,
        "task_output": False,
        "status": "DECISION_GOVERNANCE_CONTROLLED_IMPLEMENTATION_RESULT_CANDIDATE_READY",
    }

    return {
        "summary": summary,
        "case_results": case_results,
        "trace": {
            "trace_id": "decision-governance-controlled-implementation-trace-v1",
            "case_traces": traces,
            "candidate_only": True,
        },
    }


def write_outputs(payload: Dict[str, Any]) -> Dict[str, str]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    result_path = OUTPUT_DIR / "decision_governance_result_v1.json"
    case_path = OUTPUT_DIR / "decision_governance_case_results_v1.json"
    trace_path = OUTPUT_DIR / "decision_governance_trace_v1.json"

    result_path.write_text(
        json.dumps(payload["summary"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    case_path.write_text(
        json.dumps(payload["case_results"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    trace_path.write_text(
        json.dumps(payload["trace"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    return {
        "result": str(result_path),
        "cases": str(case_path),
        "trace": str(trace_path),
    }


def main() -> int:
    payload = run_controlled()
    write_outputs(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
