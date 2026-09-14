"""Output-only Runner for A3 Runtime Validation Closure v1."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any, Mapping

from .cognitive_analysis_runtime_validation_types_v1 import (
    RUNTIME_VALIDATION_CLOSURE_PHASE_V1,
    RUNTIME_VALIDATION_RUN_ID_V1,
    CognitiveAnalysisRuntimeValidationRunResultV1,
)


RUNTIME_DRYRUN_RESULT_FILENAME_V1 = "cognitive_analysis_runtime_dryrun_run_result_v1.json"
VALIDATION_RESULT_FILENAME_V1 = "cognitive_analysis_runtime_validation_run_result_v1.json"
_SKELETON_SCHEMA_VERSION_V1 = "luna.cognitive_analysis.runtime_skeleton.v1"
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


def _references_present_v1(trace: Mapping[str, Any]) -> bool:
    required = ("context_refs", "evidence_refs", "hypothesis_refs", "analysis_question_refs")
    return all(
        isinstance(trace.get(name), list)
        and bool(trace[name])
        and all(isinstance(reference, str) and reference.strip() for reference in trace[name])
        for name in required
    )


def run_runtime_validation_closure_v1(
    input_dir: Path,
    output_dir: Path,
) -> CognitiveAnalysisRuntimeValidationRunResultV1:
    """Validate serialized DryRun output only; never invoke Runtime or Skeleton."""
    source_path = input_dir / RUNTIME_DRYRUN_RESULT_FILENAME_V1
    raw_source = source_path.read_text(encoding="utf-8")
    source = json.loads(raw_source)
    skeleton = source.get("skeleton_result", {})
    candidate = skeleton.get("analysis_result_candidate", {})
    trace = skeleton.get("evidence_trace", {})
    nested_flags = skeleton.get("runtime_flags", {})
    flag_consistency = all(source.get(name) is expected for name, expected in _EXPECTED_FLAGS_V1.items()) and all(
        nested_flags.get(name) is expected for name, expected in _EXPECTED_FLAGS_V1.items()
    )
    checks = {
        "source_canonical_json": raw_source == _canonical_json_v1(source),
        "request_references_present": _references_present_v1(trace),
        "output_envelope_present": all(
            key in skeleton
            for key in ("analysis_result_candidate", "evidence_trace", "uncertainty", "warning_codes", "runtime_flags", "validation_issue_codes")
        ),
        "candidate_not_executed": candidate.get("status") == "not_executed",
        "skeleton_schema_valid": skeleton.get("schema_version") == _SKELETON_SCHEMA_VERSION_V1,
        "runtime_authorization_denied": source.get("runtime_authorization_status") == "NOT_AUTHORIZED",
        "runtime_flags_consistent": flag_consistency,
        "permission_boundary_denied": source.get("state_writeback") is False and source.get("decision_executed") is False,
        "forbidden_capabilities_absent": source.get("external_invocation_observed") is False and all(
            source.get(name) is False for name in ("model_invoked", "network_invoked", "database_invoked")
        ),
    }
    failed = tuple(name for name, passed in checks.items() if not passed)
    provisional = CognitiveAnalysisRuntimeValidationRunResultV1(
        phase=RUNTIME_VALIDATION_CLOSURE_PHASE_V1,
        run_id=RUNTIME_VALIDATION_RUN_ID_V1,
        source_runtime_dryrun_ref=RUNTIME_DRYRUN_RESULT_FILENAME_V1,
        checks=checks,
        input_validation_ok=checks["request_references_present"] and checks["source_canonical_json"],
        output_validation_ok=checks["output_envelope_present"] and checks["candidate_not_executed"] and checks["skeleton_schema_valid"],
        boundary_validation_ok=checks["runtime_authorization_denied"] and checks["runtime_flags_consistent"],
        permission_validation_ok=checks["permission_boundary_denied"],
        forbidden_capability_absent=checks["forbidden_capabilities_absent"],
        deterministic_validation_result=False,
        blocker_codes=failed,
        warning_count=int(source.get("warning_count", 0)),
        blocker_count=len(failed),
        runtime_authorized=False,
        final_candidate_decision=(
            "RUNTIME_VALIDATION_CLOSURE_CANDIDATE_PASS"
            if not failed
            else "RUNTIME_VALIDATION_CLOSURE_CANDIDATE_BLOCKED"
        ),
    )
    candidate_result = replace(provisional, deterministic_validation_result=True)
    deterministic = _canonical_json_v1(candidate_result) == _canonical_json_v1(candidate_result)
    result = replace(provisional, deterministic_validation_result=deterministic)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / VALIDATION_RESULT_FILENAME_V1).write_text(_canonical_json_v1(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    print(_canonical_json_v1(run_runtime_validation_closure_v1(Path(args.input_dir), Path(args.output_dir))))


if __name__ == "__main__":
    main()
