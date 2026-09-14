from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .adapters_v1 import build_luna_cognitive_execution_profile_v1
from .fixtures_v1 import build_synthetic_cognitive_trace_cases_v1
from .types_v1 import validate_profile_contract_v1, validate_trace_contract_v1


OUTPUT_DIR = Path("_eval_out/a_route_cognitive_whitebox_trace_and_execution_profile_foundation_v1")


def build_synthetic_runner_payload_v1() -> dict[str, Any]:
    cases = []
    for scenario in build_synthetic_cognitive_trace_cases_v1():
        trace_errors = validate_trace_contract_v1(scenario.trace)
        profile = build_luna_cognitive_execution_profile_v1(
            scenario.trace,
            role_ref=f"role:{scenario.scenario_id}:candidate",
            environment_ref=f"environment:{scenario.scenario_id}:synthetic",
        )
        profile_errors = validate_profile_contract_v1(profile)
        cases.append(
            {
                "scenario_id": scenario.scenario_id,
                "title": scenario.title,
                "expected_process": dict(scenario.expected_process),
                "trace": asdict(scenario.trace),
                "execution_profile": asdict(profile),
                "fixture_contract_errors": [*trace_errors, *profile_errors],
            }
        )
    return {
        "phase": "Phase-P1-Luna-A-Route-Cognitive-Whitebox-Trace-And-Execution-Profile-Foundation-v1-001",
        "mode": "synthetic",
        "scenario_count": len(cases),
        "cases": cases,
        "candidate_only": True,
        "cognition_mutation": False,
        "field_mutation": False,
        "world_truth_declared": False,
        "model_invocation": False,
        "provider_invocation": False,
        "observation_execution": False,
        "action_execution": False,
        "dataset_download": False,
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


def write_synthetic_runner_payload_v1(payload: dict[str, Any]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "synthetic_cognitive_whitebox_runner_v1.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    payload = build_synthetic_runner_payload_v1()
    write_synthetic_runner_payload_v1(payload)
    print(json.dumps({key: payload[key] for key in ("phase", "mode", "scenario_count", "status")}, indent=2))

