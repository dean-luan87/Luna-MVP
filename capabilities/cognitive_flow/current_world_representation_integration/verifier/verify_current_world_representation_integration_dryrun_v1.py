"""Verify fixture-only CWR DryRun artifacts; this is not a Final Phase Verifier."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from capabilities.cognitive_flow.current_world_representation_integration.integration_dryrun_v1 import (
    run_controlled_integration_dryrun_v1,
)
from capabilities.cognitive_flow.current_world_representation_integration.integration_validators_v1 import (
    static_negative_guard_results_v1,
    validate_all_results_v1,
)
from capabilities.cognitive_flow.current_world_representation_integration.runner.run_current_world_representation_integration_dryrun_v1 import (
    DEFAULT_OUTPUT_DIR_V1,
)


def verify_dryrun_v1(output_dir: Path = DEFAULT_OUTPUT_DIR_V1) -> Mapping[str, Any]:
    """Return component-level validation only; it has no phase decision authority."""

    results = run_controlled_integration_dryrun_v1()
    case_checks = validate_all_results_v1(results)
    source_root = Path(__file__).resolve().parents[1]
    negative_guards = static_negative_guard_results_v1(source_root)
    failures = [f"{case_id}:{item}" for case_id, items in case_checks.items() for item in items]
    failures.extend(negative_guards)
    warnings = [warning for result in results for warning in result.warning_codes]
    passed = 18 - len(failures)
    payload = {
        "passed_checks": passed,
        "failed_checks": failures,
        "warning_checks": warnings,
        "blocker_count": len(failures),
        "case_results": {case_id: "passed" if not items else "failed" for case_id, items in case_checks.items()},
        "boundary_results": {"runtime_executed_false": all(not result.runtime_executed for result in results), "simulation_only_true": all(result.simulation_only for result in results), "cognitive_writeback_absent": all(result.cognitive_writeback_absent for result in results)},
        "reference_chain_results": {result.case_id: result.reference_chain_valid for result in results},
        "version_chain_results": {result.case_id: result.version_chain_valid for result in results},
        "negative_guard_results": negative_guards,
        "final_decision": "GO" if not failures else "NO_GO",
        "authority_note": "component-level result only; not Final Phase Verification and not a phase GO declaration",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "current_world_representation_integration_dryrun_verification_v1.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return payload


if __name__ == "__main__":
    print(json.dumps(verify_dryrun_v1(), indent=2, sort_keys=True))
