"""Synthetic controlled runner for Outcome Evaluation Governance v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise FileNotFoundError("repository root sentinel not found")


REPO_ROOT = find_repo_root(Path(__file__).resolve())
sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.outcome_evaluation_governance.outcome_evaluation_engine_v1 import (  # noqa: E402
    OutcomeEvaluationEngineV1,
)
from capabilities.midplatform.core.outcome_evaluation_governance.outcome_evaluation_fixture_v1 import (  # noqa: E402
    OutcomeEvaluationFixtureCaseV1,
    build_fixture_cases,
)


OUTPUT_DIR = REPO_ROOT / "_eval_out/outcome_evaluation_controlled_implementation_v1"


def _check_case(engine: OutcomeEvaluationEngineV1, case: OutcomeEvaluationFixtureCaseV1) -> dict[str, Any]:
    output = engine.run_case(case.request)
    actual_attributions = tuple(item.attribution_kind for item in output.attributions)
    triggered_guards = tuple(item.guard_kind for item in output.idempotency_guards if item.triggered)
    checks = {
        "comparability": output.comparability.state == case.expected_comparability,
        "deviation": output.deviation.status == case.expected_deviation,
        "recommendation": (output.reconsideration.recommendation if output.reconsideration else "NO_ACTION") == case.expected_recommendation,
        "attribution_kinds": actual_attributions == case.expected_attribution_kinds,
        "observation_need": (output.observation_need is not None) == case.expected_observation_need,
        "learning_signal": (output.learning_signal is not None) == case.expected_learning_signal,
        "expected_guards": all(kind in triggered_guards for kind in case.expected_guard_kinds),
        "candidate_boundaries": (
            output.evaluation.candidate_only is True
            and output.evaluation.truth_declared is False
            and output.evaluation.mutation_authority is False
            and (output.reconsideration is None or output.reconsideration.executes_reconsideration is False)
            and (output.learning_signal is None or output.learning_signal.learning_executed is False)
            and (output.observation_need is None or output.observation_need.provider_invocation is False)
        ),
        "trace_reverse_lookup": (
            output.trace.provenance_grants_authority is False
            and len(output.trace.reverse_lookup) >= 4
            and output.trace.evaluation_trace_id == output.evaluation.trace_ref
            and output.evaluation.evaluation_id in {key for key, _ in output.trace.reverse_lookup}
        ),
        "trace_lineage": bool(output.evaluation.root_cycle_trace_id and output.trace.root_cycle_trace_id),
        "revision_lineage": (output.evaluation.revision_parent_ref is not None) == case.expected_revision,
        "all_negative_guards_false": all(value is False for value in output.guards.values()),
    }
    actual = {
        "comparability": output.comparability.state,
        "deviation": output.deviation.status,
        "recommendation": output.reconsideration.recommendation if output.reconsideration else "NO_ACTION",
        "attribution_kinds": actual_attributions,
        "observation_need": output.observation_need is not None,
        "learning_signal": output.learning_signal is not None,
        "triggered_guards": triggered_guards,
        "evaluation_status": output.evaluation.evaluation_status,
        "candidate_only": output.evaluation.candidate_only,
        "truth_declared": output.evaluation.truth_declared,
        "mutation_authority": output.evaluation.mutation_authority,
    }
    expected = {
        "comparability": case.expected_comparability,
        "deviation": case.expected_deviation,
        "recommendation": case.expected_recommendation,
        "attribution_kinds": case.expected_attribution_kinds,
        "observation_need": case.expected_observation_need,
        "learning_signal": case.expected_learning_signal,
        "expected_guards": case.expected_guard_kinds,
        "revision_lineage": case.expected_revision,
    }
    return {
        "scenario_id": case.scenario_id,
        "title": case.title,
        "expected": expected,
        "actual": actual,
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "output": asdict(output),
    }


def build_runner_result() -> dict[str, Any]:
    engine = OutcomeEvaluationEngineV1()
    cases = [_check_case(engine, case) for case in build_fixture_cases()]
    passed = sum(1 for case in cases if case["all_checks_passed"])
    trace = [
        {
            "scenario_id": case["scenario_id"],
            "evaluation_trace": case["output"]["trace"]["evaluation_trace_id"],
            "comparison_trace": case["output"]["trace"]["comparison_trace_id"],
            "reverse_lookup": case["output"]["trace"]["reverse_lookup"],
            "attribution_trace_refs": case["output"]["trace"]["attribution_trace_refs"],
            "reconsideration_trace_refs": case["output"]["trace"]["reconsideration_trace_refs"],
            "learning_signal_trace_refs": case["output"]["trace"]["learning_signal_trace_refs"],
            "observation_need_trace_refs": case["output"]["trace"]["observation_need_trace_refs"],
            "provenance_grants_authority": case["output"]["trace"]["provenance_grants_authority"],
        }
        for case in cases
    ]
    return {
        "phase": "Phase-Luna-A-Route-Result-Comparison-And-Outcome-Evaluation-Controlled-Implementation-v1-001",
        "owner": "Outcome Evaluation Governance",
        "scenario_count": len(cases),
        "passed_case_count": passed,
        "failed_case_count": len(cases) - passed,
        "all_cases_passed": passed == len(cases),
        "candidate_only": True,
        "synthetic_only": True,
        "runtime_execution": False,
        "provider_invocation": False,
        "model_call": False,
        "database_write": False,
        "field_state_mutation": False,
        "context_mutation": False,
        "intent_mutation": False,
        "decision_mutation": False,
        "task_mutation": False,
        "action_execution": False,
        "memory_mutation": False,
        "learning_execution": False,
        "self_mutation": False,
        "personality_mutation": False,
        "emotion_engine_execution": False,
        "b_route_execution": False,
        "semantic_compression_execution": False,
        "real_side_effect": False,
        "case_results": cases,
        "trace": trace,
    }


def main() -> int:
    payload = build_runner_result()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "outcome_evaluation_result_v1.json").write_text(
        json.dumps({key: value for key, value in payload.items() if key not in {"case_results", "trace"}}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (OUTPUT_DIR / "outcome_evaluation_case_results_v1.json").write_text(
        json.dumps(payload["case_results"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (OUTPUT_DIR / "outcome_evaluation_trace_v1.json").write_text(
        json.dumps(payload["trace"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"scenario_count": payload["scenario_count"], "all_cases_passed": payload["all_cases_passed"], "output_dir": str(OUTPUT_DIR)}, indent=2, ensure_ascii=False))
    return 0 if payload["all_cases_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
