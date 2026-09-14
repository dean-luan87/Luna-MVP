"""cwd-independent synthetic runner for Context / Field / World integration."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

VERIFIER_PATH = Path(__file__).resolve()


def _resolve_repo_root() -> Path:
    for candidate in (VERIFIER_PATH, *VERIFIER_PATH.parents):
        if (
            (candidate / "capabilities").is_dir()
            and (candidate / "docs").is_dir()
            and (candidate / "README.md").is_file()
        ):
            return candidate
    raise RuntimeError("repository root sentinel not found")


REPO_ROOT = _resolve_repo_root()
sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.context_foundation.integration.context_world_state_controlled_integration_engine_v1 import (  # noqa: E402
    ContextWorldStateControlledIntegrationEngineV1,
)
from capabilities.midplatform.core.context_foundation.integration.context_world_state_controlled_integration_fixture_v1 import (  # noqa: E402
    build_context_world_state_cases_v1,
)


OUTPUT_DIR = REPO_ROOT / "_eval_out/context_world_state_controlled_integration_v1"


def _json_value(value):
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    return value


def build_runner_result() -> dict:
    engine = ContextWorldStateControlledIntegrationEngineV1()
    case_results = []
    traces = []
    for case in build_context_world_state_cases_v1():
        result = engine.run_case(case["request"])
        expected = dict(case["expected"])
        actual = _json_value(result.behavior)
        checks = [
            {
                "field": field,
                "expected": _json_value(expected_value),
                "actual": actual.get(field),
                "passed": actual.get(field) == _json_value(expected_value),
            }
            for field, expected_value in expected.items()
        ]
        case_results.append(
            {
                "case_id": case["case_id"],
                "title": case["title"],
                "expected": _json_value(expected),
                "actual": actual,
                "checks": checks,
                "all_checks_passed": all(item["passed"] for item in checks),
                "result": _json_value(asdict(result)),
            }
        )
        traces.append(_json_value(asdict(result.trace)))
    all_passed = all(item["all_checks_passed"] for item in case_results)
    summary = {
        "phase": "Phase-Luna-A-Route-Context-World-State-Controlled-Integration-v1-001",
        "scenario_count": len(case_results),
        "all_cases_passed": all_passed,
        "failed_case_ids": [item["case_id"] for item in case_results if not item["all_checks_passed"]],
        "candidate_only": True,
        "synthetic_only": True,
        "runtime_execution": False,
        "provider_invocation": False,
        "model_call": False,
        "database_write": False,
        "vector_store_write": False,
        "scheduler_execution": False,
        "device_control": False,
        "source_owner_mutation": False,
        "field_state_mutation": False,
        "emotion_engine_execution": False,
        "b_route_execution": False,
        "semantic_compression_execution": False,
        "runtime_handoff_ready": False,
        "mutation_authority": False,
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }
    return {"summary": summary, "case_results": case_results, "traces": traces}


def write_runner_artifacts(payload: dict) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "context_world_state_result_v1.json").write_text(
        json.dumps(payload["summary"], indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (OUTPUT_DIR / "context_world_state_case_results_v1.json").write_text(
        json.dumps(payload["case_results"], indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (OUTPUT_DIR / "context_world_state_trace_v1.json").write_text(
        json.dumps({"case_traces": payload["traces"]}, indent=2, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    result = build_runner_result()
    write_runner_artifacts(result)
    print(json.dumps(result["summary"], indent=2, ensure_ascii=False))
