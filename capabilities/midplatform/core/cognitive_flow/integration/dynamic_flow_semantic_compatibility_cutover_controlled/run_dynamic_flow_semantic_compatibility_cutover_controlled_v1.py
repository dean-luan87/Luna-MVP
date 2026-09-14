"""Compact synthetic runner for the Dynamic Flow compatibility cutover."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path

RUNNER_PATH = Path(__file__).resolve()
for _candidate in (RUNNER_PATH, *RUNNER_PATH.parents):
    if (_candidate / "capabilities").is_dir() and (_candidate / "docs").is_dir():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break

from capabilities.midplatform.core.cognitive_flow.integration.dynamic_flow_semantic_compatibility_cutover_controlled.dynamic_flow_semantic_compatibility_fixture_v1 import build_compatibility_run_v1  # noqa: E402
from capabilities.midplatform.core.cognitive_flow.integration.dynamic_flow_semantic_compatibility_cutover_controlled.dynamic_flow_semantic_compatibility_registry_v1 import PHASE, negative_guards  # noqa: E402


def _jsonable(value):
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted(_jsonable(item) for item in value)
    return value


def build_runner_summary_v1() -> dict[str, object]:
    results = build_compatibility_run_v1()
    failed = [item.scenario_id for item in results if not item.passed]
    guards = negative_guards()
    return {
        "phase": PHASE,
        "scenario_count": len(results),
        "all_cases_passed": not failed,
        "failed_case_ids": failed,
        "compatibility_output_count": len(results),
        "a_need_decision_count": sum(item.interpretation.a_decisions.need_decision is not None for item in results),
        "a_sufficiency_decision_count": sum(item.interpretation.a_decisions.sufficiency_decision is not None for item in results),
        "a_reconsideration_decision_count": sum(item.interpretation.a_decisions.reconsideration_decision is not None for item in results),
        "a_next_step_decision_count": sum(item.interpretation.a_decisions.next_step_decision is not None for item in results),
        "migrated_caller_count": sum(item.migrated_caller for item in results),
        "legacy_compatibility_caller_count": 0,
        "key_guards": {
            "dynamic_flow_computation_retained": guards["dynamic_flow_computation_retained"],
            "dynamic_flow_semantic_authority_false": not guards["dynamic_flow_semantic_authority"],
            "direct_semantic_consumption_blocked": not guards["dynamic_flow_direct_semantic_consumption"],
            "a_semantic_authority_preserved": all(
                guards[key]
                for key in (
                    "a_need_authority",
                    "a_sufficiency_authority",
                    "a_reconsideration_authority",
                    "a_next_step_authority",
                )
            ),
            "loop_semantic_authority_false": guards["loop_semantic_authority"] is False,
            "legacy_fields_retained": guards["legacy_semantic_fields_removed"] is False,
            "no_provider": guards["provider_invocation"] is False,
            "no_runtime": guards["brain_runtime"] is False,
        },
    }


def main() -> int:
    summary = build_runner_summary_v1()
    print(json.dumps(_jsonable(summary), ensure_ascii=False, sort_keys=True))
    return 0 if summary["all_cases_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
