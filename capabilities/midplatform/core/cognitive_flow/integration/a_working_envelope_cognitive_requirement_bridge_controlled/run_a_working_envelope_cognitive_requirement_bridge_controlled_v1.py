"""Compact terminal-owned Runner for the working-envelope bridge."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

RUNNER_PATH = Path(__file__).resolve()
for _candidate in (RUNNER_PATH, *RUNNER_PATH.parents):
    if (_candidate / "capabilities").is_dir() and (_candidate / "docs").is_dir():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break

from capabilities.midplatform.core.cognitive_flow.integration.a_working_envelope_cognitive_requirement_bridge_controlled.a_working_envelope_cognitive_requirement_adapter_v1 import build_runner_result  # noqa: E402
from capabilities.midplatform.core.cognitive_flow.integration.a_working_envelope_cognitive_requirement_bridge_controlled.a_working_envelope_cognitive_requirement_registry_v1 import (  # noqa: E402
    CAPABILITY_RESOLUTION_OWNER,
    CAPABILITY_SCOPE_OWNER,
    NEGATIVE_GUARDS,
    OBSERVATION_OWNER,
    ROLE_A,
)


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted((_jsonable(item) for item in value), key=lambda item: str(item))
    return value


def _passed_cases(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [case for case in cases if case["passed"]]


def main() -> int:
    result = build_runner_result()
    cases = list(result["cases"])
    passed = _passed_cases(cases)
    summary = {
        "phase": result["phase"],
        "scenario_count": result["scenario_count"],
        "all_cases_passed": result["all_cases_passed"],
        "failed_case_ids": result["failed_case_ids"],
        "working_envelope_count": sum(case["case_id"].startswith("WE-") for case in passed),
        "environment_impact_assessment_count": sum(case["case_id"].startswith("EI-") for case in passed),
        "cognitive_requirement_count": sum("cognitive_requirement" in case["details"] for case in passed),
        "capability_requirement_count": sum("formation" in case["details"] for case in passed),
        "scope_result_count": sum("scope" in case["details"] for case in passed),
        "resolution_candidate_count": sum("resolution" in case["details"] for case in passed),
        "observation_admission_count": sum("observation" in case["details"] for case in passed),
        "evidence_return_count": sum("evidence_return" in case["details"] for case in passed),
        "invalidation_candidate_count": sum(case["case_id"].startswith("IV-") for case in passed),
        "key_guards": {
            "working_envelope_ref_only": not NEGATIVE_GUARDS["working_envelope_authoritative_duplication"],
            "a_owns_environment_impact": all(
                case["details"].get("impact").decision_owner_ref == ROLE_A
                for case in passed if case["case_id"].startswith("EI-")
            ),
            "a_owns_cognitive_requirement": all(
                case["details"].get("cognitive_requirement").issuing_owner_ref == ROLE_A
                for case in passed if "cognitive_requirement" in case["details"]
            ),
            "capability_scope_owner_preserved": CAPABILITY_SCOPE_OWNER == "Capability Registry / Capability Governance",
            "capability_resolution_owner_preserved": CAPABILITY_RESOLUTION_OWNER.endswith("Universal Slot Resolution Surface"),
            "observation_owner_preserved": OBSERVATION_OWNER == "Observation Gateway Governance",
            "evidence_returns_to_a": all(
                case["details"].get("evidence_return").target_owner_ref == ROLE_A
                for case in passed if "evidence_return" in case["details"]
            ),
            "loop_mechanical_only": all(value is False for key, value in NEGATIVE_GUARDS.items() if key.startswith("loop_")),
            "no_provider": not NEGATIVE_GUARDS["provider_invocation"],
            "no_runtime": not NEGATIVE_GUARDS["brain_runtime"] and not NEGATIVE_GUARDS["camera"],
        },
    }
    print(json.dumps(_jsonable(summary), ensure_ascii=False, sort_keys=True))
    return 0 if result["all_cases_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
