"""Run fixed CWR integration DryRun fixtures and write JSON artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from capabilities.cognitive_flow.current_world_representation_integration.integration_dryrun_v1 import (
    run_controlled_integration_dryrun_v1,
)
from capabilities.cognitive_flow.current_world_representation_integration.integration_types_v1 import to_jsonable_v1
from capabilities.cognitive_flow.current_world_representation_integration.integration_validators_v1 import (
    static_negative_guard_results_v1,
    validate_all_results_v1,
)


DEFAULT_OUTPUT_DIR_V1 = Path("_eval_out/current_world_representation_integration_dryrun_v1_smoke_v0")


def run_and_write_v1(output_dir: Path = DEFAULT_OUTPUT_DIR_V1) -> Mapping[str, Any]:
    """Write deterministic fixture-only result and matrix artifacts."""

    results = run_controlled_integration_dryrun_v1()
    checks = validate_all_results_v1(results)
    source_root = Path(__file__).resolve().parents[1]
    negative_guards = static_negative_guard_results_v1(source_root)
    output_dir.mkdir(parents=True, exist_ok=True)
    result_payload = {"results": to_jsonable_v1(results), "runtime_executed": False, "simulation_only": True}
    matrix_payload = {"case_ids": [result.case_id for result in results], "case_checks": checks}
    verification_payload = {
        "component_scope": "fixture_only_controlled_dryrun",
        "case_checks": checks,
        "negative_guard_results": negative_guards,
        "component_ready": not any(checks.values()) and not negative_guards,
    }
    (output_dir / "current_world_representation_integration_dryrun_result_v1.json").write_text(json.dumps(result_payload, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "current_world_representation_integration_dryrun_case_matrix_v1.json").write_text(json.dumps(matrix_payload, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "current_world_representation_integration_dryrun_verification_v1.json").write_text(json.dumps(verification_payload, indent=2, sort_keys=True), encoding="utf-8")
    return verification_payload


if __name__ == "__main__":
    print(json.dumps(run_and_write_v1(), indent=2, sort_keys=True))
