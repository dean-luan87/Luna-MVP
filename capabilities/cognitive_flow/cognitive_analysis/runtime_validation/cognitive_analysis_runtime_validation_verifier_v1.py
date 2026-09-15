"""Independent file-based verifier for A3 Runtime Validation Closure v1."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .cognitive_analysis_runtime_validation_types_v1 import (
    RUNTIME_VALIDATION_CLOSURE_PHASE_V1,
    RUNTIME_VALIDATION_RUN_ID_V1,
    RUNTIME_VALIDATION_VERIFIER_ID_V1,
    CognitiveAnalysisRuntimeValidationVerificationResultV1,
)
from capabilities.evaluation.common.side_effect_observation_v1 import (
    OBSERVED_NOT_EXECUTED,
    classify_side_effect_map,
)


RUNTIME_DRYRUN_RESULT_FILENAME_V1 = "cognitive_analysis_runtime_dryrun_run_result_v1.json"
VALIDATION_RESULT_FILENAME_V1 = "cognitive_analysis_runtime_validation_run_result_v1.json"
VERIFICATION_RESULT_FILENAME_V1 = "cognitive_analysis_runtime_validation_verification_result_v1.json"
_EXPECTED_FLAGS_V1 = {
    "runtime_executed": False,
    "simulation_only": True,
    "model_invoked": False,
    "network_invoked": False,
    "database_invoked": False,
    "state_writeback": False,
    "decision_executed": False,
}


def _canonical_json_v1(value: Any) -> str:
    if hasattr(value, "__dataclass_fields__"):
        value = asdict(value)
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def verify_runtime_validation_closure_v1(
    input_dir: Path,
    validation_dir: Path,
) -> CognitiveAnalysisRuntimeValidationVerificationResultV1:
    """Read DryRun and validation artifacts only; never invoke the validation Runner."""
    source_path = input_dir / RUNTIME_DRYRUN_RESULT_FILENAME_V1
    validation_path = validation_dir / VALIDATION_RESULT_FILENAME_V1
    source_present = source_path.is_file()
    validation_present = validation_path.is_file()
    source_raw = source_path.read_text(encoding="utf-8") if source_present else ""
    validation_raw = validation_path.read_text(encoding="utf-8") if validation_present else ""
    source = json.loads(source_raw) if source_present else {}
    validation = json.loads(validation_raw) if validation_present else {}
    nested_flags = source.get("skeleton_result", {}).get("runtime_flags", {})
    flag_consistency = source_present and all(source.get(name) is expected for name, expected in _EXPECTED_FLAGS_V1.items()) and all(
        nested_flags.get(name) is expected for name, expected in _EXPECTED_FLAGS_V1.items()
    )
    permission_ok = source_present and source.get("state_writeback") is False and source.get("decision_executed") is False
    output_contract_ok = source_present and source.get("skeleton_result", {}).get("schema_version") == "luna.cognitive_analysis.runtime_skeleton.v1" and source.get("skeleton_result", {}).get("analysis_result_candidate", {}).get("status") == "not_executed"
    forbidden_absent = source_present and source.get("external_invocation_observed") is False and all(
        source.get(name) is False for name in ("model_invoked", "network_invoked", "database_invoked")
    )
    validation_checks = validation.get("checks")
    validation_checks_ok = validation_present and isinstance(validation_checks, dict) and bool(validation_checks) and all(validation_checks.values())
    determinism_evidence = validation.get("determinism_evidence") or {}
    deterministic_ok = validation_present and validation.get("determinism_status") == "DETERMINISM_VERIFIED" and validation.get("deterministic_validation_result") is True and validation_raw == _canonical_json_v1(validation) and determinism_evidence.get("reconstruction_a") != determinism_evidence.get("reconstruction_b") and determinism_evidence.get("canonical_digest_a") == determinism_evidence.get("canonical_digest_b")
    side_effect_evidence = source.get("side_effect_evidence")
    side_effect_status = classify_side_effect_map(side_effect_evidence)
    side_effect_proof = side_effect_status == "OBSERVED_NOT_EXECUTED"
    checks = (
        source_present,
        validation_present,
        source_raw == _canonical_json_v1(source),
        validation.get("phase") == RUNTIME_VALIDATION_CLOSURE_PHASE_V1,
        validation.get("run_id") == RUNTIME_VALIDATION_RUN_ID_V1,
        validation.get("runtime_authorized") is False,
        validation.get("blocker_count") == 0,
        validation_checks_ok,
        flag_consistency,
        permission_ok,
        output_contract_ok,
        forbidden_absent,
        deterministic_ok,
        side_effect_proof,
    )
    failed = sum(not check for check in checks)
    result = CognitiveAnalysisRuntimeValidationVerificationResultV1(
        verifier_id=RUNTIME_VALIDATION_VERIFIER_ID_V1,
        source_runtime_dryrun_ref=RUNTIME_DRYRUN_RESULT_FILENAME_V1,
        source_validation_ref=VALIDATION_RESULT_FILENAME_V1,
        passed_checks=len(checks) - failed,
        failed_checks=failed,
        blocker_count=failed,
        warning_count=int(source.get("warning_count", 0)) if source_present else 0,
        runtime_flag_consistency_ok=flag_consistency,
        permission_boundary_ok=permission_ok,
        output_contract_ok=output_contract_ok,
        forbidden_capability_absent=forbidden_absent and side_effect_proof,
        deterministic_validation_result_ok=deterministic_ok,
        verifier_invoked_runner=False,
        runtime_authorized=False,
        final_candidate_decision=(
            "RUNTIME_VALIDATION_CLOSURE_VERIFICATION_CANDIDATE_PASS"
            if failed == 0
            else "RUNTIME_VALIDATION_CLOSURE_VERIFICATION_CANDIDATE_BLOCKED"
        ),
        determinism_status=validation.get("determinism_status", "DETERMINISM_UNVERIFIED"),
        actual_side_effect_observation_status=side_effect_status,
        controlled_scope_passed=all(checks[:12]),
    )
    validation_dir.mkdir(parents=True, exist_ok=True)
    (validation_dir / VERIFICATION_RESULT_FILENAME_V1).write_text(_canonical_json_v1(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--validation-dir", required=True)
    args = parser.parse_args()
    print(_canonical_json_v1(verify_runtime_validation_closure_v1(Path(args.input_dir), Path(args.validation_dir))))


if __name__ == "__main__":
    main()
