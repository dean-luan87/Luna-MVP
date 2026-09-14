"""Independent verifier for A3 Runtime Capability Assessment v1."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .cognitive_analysis_runtime_assessment_types_v1 import (
    CAPABILITY_IDS_V1,
    RUNTIME_CAPABILITY_ASSESSMENT_PHASE_V1,
    RUNTIME_CAPABILITY_ASSESSMENT_RUN_ID_V1,
    RUNTIME_CAPABILITY_ASSESSMENT_VERIFIER_ID_V1,
    CognitiveAnalysisRuntimeCapabilityAssessmentVerificationResultV1,
)


ASSESSMENT_REPORT_FILENAME_V1 = "cognitive_analysis_runtime_capability_assessment_report_v1.json"
VERIFICATION_RESULT_FILENAME_V1 = "cognitive_analysis_runtime_capability_assessment_verification_result_v1.json"


def _canonical_json_v1(value: Any) -> str:
    if hasattr(value, "__dataclass_fields__"):
        value = asdict(value)
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def verify_runtime_capability_assessment_v1(
    input_dir: Path,
) -> CognitiveAnalysisRuntimeCapabilityAssessmentVerificationResultV1:
    """Read the assessment report only; this verifier never invokes its Runner."""
    report_path = input_dir / ASSESSMENT_REPORT_FILENAME_V1
    present = report_path.is_file()
    raw = report_path.read_text(encoding="utf-8") if present else ""
    report = json.loads(raw) if present else {}
    entries = report.get("capabilities", [])
    inventory_complete = present and tuple(entry.get("capability") for entry in entries) == CAPABILITY_IDS_V1
    boundary_ok = present and all(
        entry.get("authority_boundary") == "candidate_only; no Fact, Decision, Action, State, or Memory authority"
        for entry in entries
    )
    dependencies_ok = present and all(
        isinstance(entry.get("input_dependency"), list)
        and bool(entry["input_dependency"])
        and all(isinstance(item, str) and item for item in entry["input_dependency"])
        and isinstance(entry.get("expected_output"), str)
        and entry["expected_output"]
        and isinstance(entry.get("blocker_condition"), str)
        and entry["blocker_condition"]
        for entry in entries
    )
    forbidden_absent = present and all(
        report.get(name) is False
        for name in ("runtime_executed", "model_invoked", "evidence_inferred", "hypothesis_generated", "state_writeback", "decision_generated", "action_planned", "memory_updated")
    )
    deterministic_ok = present and report.get("deterministic_output") is True and raw == _canonical_json_v1(report)
    checks = (
        present,
        report.get("phase") == RUNTIME_CAPABILITY_ASSESSMENT_PHASE_V1,
        report.get("run_id") == RUNTIME_CAPABILITY_ASSESSMENT_RUN_ID_V1,
        report.get("runtime_authorized") is False,
        report.get("blocker_count") == 0,
        inventory_complete,
        boundary_ok,
        dependencies_ok,
        forbidden_absent,
        deterministic_ok,
    )
    failed = sum(not check for check in checks)
    result = CognitiveAnalysisRuntimeCapabilityAssessmentVerificationResultV1(
        verifier_id=RUNTIME_CAPABILITY_ASSESSMENT_VERIFIER_ID_V1,
        source_report_ref=ASSESSMENT_REPORT_FILENAME_V1,
        passed_checks=len(checks) - failed,
        failed_checks=failed,
        blocker_count=failed,
        warning_count=len(report.get("warning_codes", ())) if present else 0,
        capability_inventory_complete=inventory_complete,
        authority_boundary_ok=boundary_ok,
        forbidden_capability_absent=forbidden_absent,
        dependency_declaration_ok=dependencies_ok,
        deterministic_output_ok=deterministic_ok,
        verifier_invoked_runner=False,
        runtime_authorized=False,
        final_candidate_decision=(
            "RUNTIME_CAPABILITY_ASSESSMENT_VERIFICATION_CANDIDATE_PASS"
            if failed == 0
            else "RUNTIME_CAPABILITY_ASSESSMENT_VERIFICATION_CANDIDATE_BLOCKED"
        ),
    )
    input_dir.mkdir(parents=True, exist_ok=True)
    (input_dir / VERIFICATION_RESULT_FILENAME_V1).write_text(_canonical_json_v1(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True)
    args = parser.parse_args()
    print(_canonical_json_v1(verify_runtime_capability_assessment_v1(Path(args.input_dir))))


if __name__ == "__main__":
    main()
