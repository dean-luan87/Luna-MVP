"""Independent output-only verifier for A3 Runtime Skeleton DryRun v1."""

from __future__ import annotations

import argparse
from pathlib import Path

from .cognitive_analysis_runtime_dryrun_serializer_v1 import (
    read_json_v1,
    serialize_json_v1,
    write_json_v1,
)
from .cognitive_analysis_runtime_dryrun_types_v1 import (
    RUNTIME_SKELETON_DRYRUN_FIXTURE_REF_V1,
    RUNTIME_SKELETON_DRYRUN_PHASE_V1,
    RUNTIME_SKELETON_DRYRUN_RUN_ID_V1,
    RUNTIME_SKELETON_DRYRUN_VERIFIER_ID_V1,
    CognitiveAnalysisRuntimeDryRunVerificationResultV1,
)


RUN_RESULT_FILENAME_V1 = "cognitive_analysis_runtime_dryrun_run_result_v1.json"
VERIFICATION_RESULT_FILENAME_V1 = "cognitive_analysis_runtime_dryrun_verification_result_v1.json"


def verify_runtime_skeleton_dryrun_v1(
    input_dir: Path,
) -> CognitiveAnalysisRuntimeDryRunVerificationResultV1:
    """Read serialized output only; this verifier never invokes the Runner."""
    run_path = input_dir / RUN_RESULT_FILENAME_V1
    present = run_path.is_file()
    run = read_json_v1(run_path) if present else {}
    canonical_matches = present and run_path.read_text(encoding="utf-8") == serialize_json_v1(run)
    expected_flags = {
        "runtime_executed": False,
        "simulation_only": True,
        "model_invoked": False,
        "network_invoked": False,
        "database_invoked": False,
        "state_writeback": False,
        "decision_executed": False,
    }
    flag_consistency = present and all(run.get(name) is value for name, value in expected_flags.items())
    nested_flags = run.get("skeleton_result", {}).get("runtime_flags", {})
    boundary_ok = present and run.get("runtime_authorization_status") == "NOT_AUTHORIZED" and flag_consistency
    permission_ok = present and run.get("state_writeback") is False and run.get("decision_executed") is False
    external_absent = present and run.get("external_invocation_observed") is False and all(
        run.get(name) is False
        for name in ("model_invoked", "network_invoked", "database_invoked")
    )
    nested_consistency = present and all(nested_flags.get(name) is value for name, value in expected_flags.items())
    checks = (
        present,
        run.get("phase") == RUNTIME_SKELETON_DRYRUN_PHASE_V1,
        run.get("run_id") == RUNTIME_SKELETON_DRYRUN_RUN_ID_V1,
        run.get("request_fixture_ref") == RUNTIME_SKELETON_DRYRUN_FIXTURE_REF_V1,
        boundary_ok,
        permission_ok,
        flag_consistency,
        nested_consistency,
        run.get("deterministic_serialization") is True,
        canonical_matches,
        external_absent,
        run.get("blocker_count") == 0,
        run.get("skeleton_result", {}).get("analysis_result_candidate", {}).get("status") == "not_executed",
    )
    failed = sum(not check for check in checks)
    result = CognitiveAnalysisRuntimeDryRunVerificationResultV1(
        verifier_id=RUNTIME_SKELETON_DRYRUN_VERIFIER_ID_V1,
        source_run_ref=RUN_RESULT_FILENAME_V1,
        passed_checks=len(checks) - failed,
        failed_checks=failed,
        blocker_count=failed,
        warning_count=run.get("warning_count", 0) if present else 0,
        runtime_boundary_ok=boundary_ok,
        permission_boundary_ok=permission_ok,
        flag_consistency_ok=flag_consistency and nested_consistency,
        deterministic_serialization_ok=bool(canonical_matches),
        external_invocation_absent=external_absent,
        verifier_invoked_runner=False,
        final_candidate_decision=(
            "RUNTIME_SKELETON_DRYRUN_VERIFICATION_CANDIDATE_PASS"
            if failed == 0
            else "RUNTIME_SKELETON_DRYRUN_VERIFICATION_CANDIDATE_BLOCKED"
        ),
    )
    input_dir.mkdir(parents=True, exist_ok=True)
    write_json_v1(input_dir / VERIFICATION_RESULT_FILENAME_V1, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True)
    args = parser.parse_args()
    print(serialize_json_v1(verify_runtime_skeleton_dryrun_v1(Path(args.input_dir))))


if __name__ == "__main__":
    main()
