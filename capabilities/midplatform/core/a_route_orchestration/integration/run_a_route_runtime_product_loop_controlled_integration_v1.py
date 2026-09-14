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

from capabilities.midplatform.core.a_route_orchestration.integration.a_route_product_loop_integration_engine_v1 import (  # noqa: E402
    ARouteProductLoopIntegrationEngineV1,
)
from capabilities.midplatform.core.a_route_orchestration.integration.a_route_product_loop_integration_fixture_v1 import (  # noqa: E402
    ProductLoopFixtureCaseV1,
    build_fixture_cases,
)


OUTPUT_DIR = REPO_ROOT / "_eval_out/a_route_runtime_product_loop_controlled_integration_v1"


def _check_case(engine: ARouteProductLoopIntegrationEngineV1, case: ProductLoopFixtureCaseV1) -> dict[str, Any]:
    result = engine.run_case(case.request)
    output_kind = result.output.output_kind if result.output else "NONE"
    feedback_route = result.feedback.route if result.feedback else "NO_ROUTE"
    stage_ids = tuple(stage.stage_id for stage in result.stages)
    expected_full_chain = (
        "INPUT", "OBSERVATION_REQUIRED", "OBSERVING", "OBSERVATION_READY", "WORLD_CONTEXT_READY",
        "COGNITION_READY", "DECISION_READY", "TASK_READY", "ACTION_READY", "EXECUTION_PENDING",
        "EXECUTING", "RESULT_READY", "EVALUATING", "FEEDBACK", "COMPLETED",
    )
    actual_errors = tuple(result.error_refs)
    checks = {
        "state": result.state == case.expected_state,
        "output_kind": output_kind == case.expected_output_kind,
        "feedback_route": feedback_route == case.expected_feedback_route,
        "runtime_admission": (result.runtime_admission is not None) == case.expect_runtime_admission,
        "execution_result": (result.execution_result is not None) == case.expect_execution_result,
        "observation_reentry": (result.observation_reentry is not None) == case.expect_observation_reentry,
        "reconsideration": (result.reconsideration is not None) == case.expect_reconsideration,
        "next_cycle": (result.next_cycle is not None) == case.expect_next_cycle,
        "expected_error": (case.expected_error_code == "" or case.expected_error_code in actual_errors),
        "candidate_boundaries": (
            result.candidate_only is True
            and result.synthetic_only is True
            and all(stage.candidate_only and not stage.mutation_authority and not stage.runtime_handoff_ready for stage in result.stages)
            and (result.runtime_admission is None or (result.runtime_admission.runtime_authorized is False and result.runtime_admission.provider_invocation is False))
            and (result.execution_request is None or result.execution_request.real_execution is False)
            and (result.execution_result is None or result.execution_result.real_runtime_execution is False)
            and (result.output is None or result.output.user_delivery_executed is False)
        ),
        "trace_reverse_lookup": (
            result.trace.provenance_grants_authority is False
            and result.trace.root_cycle_trace_id == result.cycle.trace_ref
            and len(result.trace.reverse_lookup) >= 2
            and (result.output is None or result.output.output_id in {key for key, _ in result.trace.reverse_lookup})
        ),
        "negative_guards": all(value is False for value in result.guards.values()),
        "no_hidden_retry": len([stage for stage in result.stages if stage.stage_id == "EXECUTING"]) <= 1,
        "full_chain": (not case.expected_full_chain) or all(stage_id in stage_ids for stage_id in expected_full_chain),
        "resume_linkage": (not case.request.previous_cycle_id) or result.cycle.previous_cycle_id == case.request.previous_cycle_id,
    }
    actual = {
        "state": result.state,
        "output_kind": output_kind,
        "feedback_route": feedback_route,
        "runtime_admission": result.runtime_admission is not None,
        "execution_result": result.execution_result is not None,
        "observation_reentry": result.observation_reentry is not None,
        "reconsideration": result.reconsideration is not None,
        "next_cycle": result.next_cycle is not None,
        "error_refs": actual_errors,
        "stage_ids": stage_ids,
        "candidate_only": result.candidate_only,
        "synthetic_only": result.synthetic_only,
    }
    expected = {
        "state": case.expected_state,
        "output_kind": case.expected_output_kind,
        "feedback_route": case.expected_feedback_route,
        "runtime_admission": case.expect_runtime_admission,
        "execution_result": case.expect_execution_result,
        "observation_reentry": case.expect_observation_reentry,
        "reconsideration": case.expect_reconsideration,
        "next_cycle": case.expect_next_cycle,
        "error_code": case.expected_error_code,
        "full_chain": case.expected_full_chain,
    }
    return {
        "scenario_id": case.scenario_id,
        "title": case.title,
        "expected": expected,
        "actual": actual,
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "result": asdict(result),
    }


def build_runner_payload() -> dict[str, Any]:
    engine = ARouteProductLoopIntegrationEngineV1()
    cases = [_check_case(engine, case) for case in build_fixture_cases()]
    failed = [case["scenario_id"] for case in cases if not case["all_checks_passed"]]
    return {
        "phase": "Phase-Luna-A-Route-Runtime-Product-Loop-Controlled-Integration-v1-001",
        "owner": "A Route Orchestration Governance",
        "scenario_count": len(cases),
        "all_cases_passed": not failed,
        "failed_case_ids": failed,
        "synthetic_only": True,
        "controlled_integration_only": True,
        "real_runtime_execution": False,
        "provider_invocation": False,
        "model_call": False,
        "database_write": False,
        "scheduler_execution": False,
        "device_control": False,
        "source_owner_mutation": False,
        "learning_execution": False,
        "emotion_engine_execution": False,
        "b_route_execution": False,
        "semantic_compression_execution": False,
        "real_side_effect": False,
        "case_results": cases,
        "trace": [
            {
                "scenario_id": case["scenario_id"],
                "root_cycle_trace_id": case["result"]["trace"]["root_cycle_trace_id"],
                "reverse_lookup": case["result"]["trace"]["reverse_lookup"],
                "provenance_grants_authority": case["result"]["trace"]["provenance_grants_authority"],
            }
            for case in cases
        ],
    }


def main() -> int:
    payload = build_runner_payload()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = {key: value for key, value in payload.items() if key not in {"case_results", "trace"}}
    (OUTPUT_DIR / "a_route_runtime_product_loop_result_v1.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "a_route_runtime_product_loop_case_results_v1.json").write_text(json.dumps(payload["case_results"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "a_route_runtime_product_loop_trace_v1.json").write_text(json.dumps(payload["trace"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"scenario_count": payload["scenario_count"], "all_cases_passed": payload["all_cases_passed"], "failed_case_ids": payload["failed_case_ids"], "output_dir": str(OUTPUT_DIR)}, indent=2, ensure_ascii=False))
    return 0 if payload["all_cases_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
