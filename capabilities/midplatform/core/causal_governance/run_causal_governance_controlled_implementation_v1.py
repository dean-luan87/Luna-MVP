"""Controlled runner for Causal Governance implementation v1.

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
        sentinel = candidate / "capabilities/midplatform/core/causal_governance"
        if sentinel.is_dir():
            return candidate

    # Fallback 1: current working directory when launched from repository root.
    cwd = Path.cwd().resolve()
    if (cwd / "capabilities/midplatform/core/causal_governance").is_dir():
        return cwd

    # Fallback 2: historical repository layout used in this workspace.
    return Path(__file__).resolve().parents[4]


REPO_ROOT = _resolve_repo_root()

if __package__ in {None, ""}:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.causal_governance.causal_governance_engine_v1 import (
    CausalGovernanceEngineV1,
)
from capabilities.midplatform.core.causal_governance.causal_governance_fixture_v1 import (
    get_causal_synthetic_fixtures_v1,
)
from capabilities.midplatform.core.causal_governance.causal_static_validators_v1 import (
    validate_counterfactual_candidates,
    validate_handoff,
    validate_hypothesis_candidates,
    validate_input_refs_read_only,
    validate_negative_guard_flags,
    validate_no_runtime_side_effects,
    validate_trace_completeness,
)


OUTPUT_DIR = REPO_ROOT / "_eval_out/causal_governance_controlled_implementation_v1"


def run_controlled() -> Dict[str, Any]:
    engine = CausalGovernanceEngineV1()
    fixtures = get_causal_synthetic_fixtures_v1()

    case_results: List[Dict[str, Any]] = []
    traces: List[Dict[str, Any]] = []

    for case in fixtures:
        output = engine.run_case(case.request)
        all_refs = (
            case.request.target_event_refs
            + case.request.cause_candidate_refs
            + case.request.supporting_evidence_refs
            + case.request.opposing_evidence_refs
            + case.request.confounder_refs
            + case.request.temporal_order_refs
            + case.request.context_refs
            + case.request.prior_refs
            + case.request.intent_refs
            + case.request.influence_refs
            + case.request.correlation_signal_refs
        )

        checks = {
            "input_refs_read_only": validate_input_refs_read_only(all_refs),
            "hypothesis_candidates_valid": validate_hypothesis_candidates(
                output.hypothesis_candidates
            ),
            "counterfactual_candidates_valid": validate_counterfactual_candidates(
                output.counterfactual_candidates
            ),
            "trace_completeness": validate_trace_completeness(output),
            "handoff_valid": validate_handoff(output.handoff_candidate),
            "negative_guard_flags": validate_negative_guard_flags(),
            "no_runtime_side_effects": validate_no_runtime_side_effects(output),
            "state_expected": output.hypothesis_candidates[0].state_candidate
            == case.expected_state,
            "hypothesis_count_expected": len(output.hypothesis_candidates)
            == case.expected_hypothesis_count,
            "handoff_eligibility_expected": output.handoff_candidate.candidate_only
            is case.expected_handoff_eligible,
            "synthetic_only": case.synthetic_only is True
            and case.request.synthetic_only is True,
        }

        case_results.append(
            {
                "case_id": case.case_id,
                "description": case.description,
                "state": output.hypothesis_candidates[0].state_candidate,
                "hypothesis_count": len(output.hypothesis_candidates),
                "supporting_evidence_refs": list(
                    output.handoff_candidate.supporting_evidence_refs
                ),
                "opposing_evidence_refs": list(
                    output.handoff_candidate.opposing_evidence_refs
                ),
                "uncertainty": list(output.handoff_candidate.uncertainty),
                "provenance": list(output.handoff_candidate.provenance),
                "expected_guard_tokens": list(case.expected_guard_tokens),
                "checks": checks,
                "all_checks_passed": all(checks.values()),
            }
        )

        traces.append(
            {
                "case_id": case.case_id,
                "trace_id": output.trace_candidate.trace_id,
                "hypothesis_refs": list(output.trace_candidate.hypothesis_refs),
                "revision_chain_refs": list(output.trace_candidate.revision_chain_refs),
                "counterfactual_refs": list(output.trace_candidate.counterfactual_refs),
                "handoff_refs": list(output.trace_candidate.handoff_refs),
            }
        )

    passed = sum(1 for item in case_results if item["all_checks_passed"])
    summary = {
        "phase": "Phase-Luna-Causal-Governance-Controlled-Implementation-v1-001",
        "case_count": len(case_results),
        "passed_case_count": passed,
        "failed_case_count": len(case_results) - passed,
        "candidate_only": True,
        "runtime_executed": False,
        "source_mutation_executed": False,
        "decision_output": False,
        "action_output": False,
        "task_output": False,
        "status": "CAUSAL_GOVERNANCE_CONTROLLED_IMPLEMENTATION_RESULT_CANDIDATE_READY",
    }

    return {
        "summary": summary,
        "case_results": case_results,
        "trace": {
            "trace_id": "causal-governance-controlled-implementation-trace-v1",
            "case_traces": traces,
            "candidate_only": True,
        },
    }


def write_outputs(payload: Dict[str, Any]) -> Dict[str, str]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    result_path = OUTPUT_DIR / "causal_governance_result_v1.json"
    case_path = OUTPUT_DIR / "causal_governance_case_results_v1.json"
    trace_path = OUTPUT_DIR / "causal_governance_trace_v1.json"

    result_path.write_text(
        json.dumps(payload["summary"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    case_path.write_text(
        json.dumps(payload["case_results"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    if not case_path.exists():
        raise RuntimeError(
            f"CAUSAL_RUNNER_CASE_ARTIFACT_NOT_CREATED: {case_path.resolve()}"
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
