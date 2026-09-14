"""Independent file-based verifier for A3 Controlled DryRun output v1."""
from __future__ import annotations

import argparse
from pathlib import Path

from .cognitive_analysis_dryrun_serialization_v1 import read_json_v1, write_json_v1
from .cognitive_analysis_dryrun_types_v1 import CONTRACT_REF_V1, DRYRUN_VERIFIER_ID_V1, FIXTURE_BASELINE_V1, CognitiveAnalysisDryRunVerificationResultV1


_FILES = ("cognitive_analysis_dryrun_run_result_v1.json", "cognitive_analysis_dryrun_case_results_v1.json", "cognitive_analysis_dryrun_negative_guard_report_v1.json", "cognitive_analysis_dryrun_reference_closure_v1.json")


def verify_controlled_dryrun_v1(input_dir: Path) -> CognitiveAnalysisDryRunVerificationResultV1:
    present = all((input_dir / name).is_file() for name in _FILES)
    run = read_json_v1(input_dir / _FILES[0]); cases = read_json_v1(input_dir / _FILES[1]); guards = read_json_v1(input_dir / _FILES[2]); refs = read_json_v1(input_dir / _FILES[3])
    case_ids = [case["case_id"] for case in cases]; passed = sum(bool(case["passed"]) for case in cases)
    failures = 0
    checks = [present, run["contract_ref"] == CONTRACT_REF_V1, run["fixture_baseline_ref"] == FIXTURE_BASELINE_V1, len(cases) == 8, len(set(case_ids)) == 8, run["case_count"] == 8, run["passed_case_count"] == passed, run["failed_case_count"] == 8-passed, run["blocker_count"] == 0, refs["dangling_reference_count"] == 0, refs["cross_case_reference_count"] == 0, run["runtime_executed"] is False, run["simulation_only"] is True, all(run[name] is False for name in ("real_analysis_executed", "model_invoked", "network_invoked", "database_invoked", "observation_executed", "decision_executed", "state_writeback")), len(guards["guards"]) >= 24, all(guards["guards"].values())]
    failures = len([value for value in checks if not value])
    result = CognitiveAnalysisDryRunVerificationResultV1(DRYRUN_VERIFIER_ID_V1, _FILES[0], 8, len(cases), len(checks)-failures, failures, 0 if failures == 0 else failures, run["warning_count"], refs["dangling_reference_count"], refs["cross_case_reference_count"], failures == 0, True, run["runtime_executed"], run["simulation_only"], "DRYRUN_VERIFICATION_CANDIDATE_PASS" if failures == 0 else "DRYRUN_VERIFICATION_CANDIDATE_BLOCKED")
    write_json_v1(input_dir / "cognitive_analysis_dryrun_verification_result_v1.json", result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--input-dir", required=True); args = parser.parse_args()
    print(verify_controlled_dryrun_v1(Path(args.input_dir)))


if __name__ == "__main__": main()
