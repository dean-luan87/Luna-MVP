"""Candidate-only A3 Runtime Capability Admission DryRun Runner v1."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from capabilities.cognitive_flow.cognitive_analysis.runtime_registration.cognitive_analysis_runtime_registration_mapping_v1 import (
    MODEL_SKILL_ADMISSION_CONTRACT_REF_V1,
    OUTPUT_CANDIDATE_CONTRACT_REF_V1,
    PERMISSION_ADMISSION_CONTRACT_REF_V1,
    RUNTIME_BOUNDARY_CONTRACT_REF_V1,
    build_cognitive_analysis_runtime_registration_candidate_v1,
)
from capabilities.cognitive_flow.cognitive_analysis.runtime_registration.cognitive_analysis_runtime_registration_validator_v1 import (
    validate_cognitive_analysis_runtime_registration_candidate_v1,
)

from .cognitive_analysis_runtime_admission_dryrun_types_v1 import (
    ADMISSION_DRYRUN_PHASE_V1,
    ADMISSION_DRYRUN_RUN_ID_V1,
    CognitiveAnalysisRuntimeAdmissionAssessmentCandidateV1,
)


ADMISSION_DRYRUN_RESULT_FILENAME_V1 = (
    "cognitive_analysis_runtime_capability_admission_dryrun_result_v1.json"
)


def canonical_json_v1(value: Any) -> str:
    if hasattr(value, "__dataclass_fields__"):
        value = asdict(value)
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def run_cognitive_analysis_runtime_admission_dryrun_v1(
    project_root: Path,
    output_dir: Path,
) -> CognitiveAnalysisRuntimeAdmissionAssessmentCandidateV1:
    """Assess a candidate only; never write, activate, grant, or execute."""
    candidate = build_cognitive_analysis_runtime_registration_candidate_v1()
    candidate_validation = validate_cognitive_analysis_runtime_registration_candidate_v1(
        candidate, project_root
    )
    registry_reference_exists = (project_root / candidate.registry_ref).is_file()
    registry_record_exists = candidate_validation.duplicate_capability_detected
    required_contracts = {
        MODEL_SKILL_ADMISSION_CONTRACT_REF_V1,
        PERMISSION_ADMISSION_CONTRACT_REF_V1,
        RUNTIME_BOUNDARY_CONTRACT_REF_V1,
        OUTPUT_CANDIDATE_CONTRACT_REF_V1,
    }
    checks = {
        "registry_reference": registry_reference_exists,
        "candidate_not_pre_registered": not registry_record_exists,
        "lifecycle_consistency": candidate.lifecycle_state == "candidate",
        "contract_completeness": required_contracts.issubset(candidate.required_contracts),
        "permission_reference": PERMISSION_ADMISSION_CONTRACT_REF_V1 in candidate.required_contracts,
        "boundary_consistency": not any((
            candidate.registry_write_applied,
            candidate.capability_activation_applied,
            candidate.permission_grant_applied,
            candidate.runtime_authorized,
        )),
        "registration_candidate_valid": candidate_validation.valid,
    }
    blocker_codes = tuple(name for name, passed in checks.items() if not passed)
    assessment_ready = not blocker_codes
    result = CognitiveAnalysisRuntimeAdmissionAssessmentCandidateV1(
        phase=ADMISSION_DRYRUN_PHASE_V1,
        run_id=ADMISSION_DRYRUN_RUN_ID_V1,
        capability_id=candidate.capability_id,
        registry_ref=candidate.registry_ref,
        registry_reference_exists=registry_reference_exists,
        registry_record_exists=registry_record_exists,
        lifecycle_state=candidate.lifecycle_state,
        checks=checks,
        admission_status=(
            "admission_candidate_ready" if assessment_ready else "admission_candidate_blocked"
        ),
        admission_applied=False,
        registry_write_applied=False,
        capability_activation_applied=False,
        permission_grant_applied=False,
        runtime_executed=False,
        runtime_authorized=False,
        blocker_codes=blocker_codes,
        warning_codes=(
            "registry_record_not_written",
            "capability_not_activated",
            "runtime_not_authorized",
        ),
        blocker_count=len(blocker_codes),
        warning_count=3,
        deterministic_output=True,
        final_candidate_decision=(
            "CAPABILITY_ADMISSION_DRYRUN_READY_WITH_NOTES"
            if assessment_ready
            else "CAPABILITY_ADMISSION_DRYRUN_BLOCKED"
        ),
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / ADMISSION_DRYRUN_RESULT_FILENAME_V1).write_text(
        canonical_json_v1(result), encoding="utf-8"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = run_cognitive_analysis_runtime_admission_dryrun_v1(
        Path(args.project_root), Path(args.output_dir)
    )
    print(canonical_json_v1(result))


if __name__ == "__main__":
    main()
