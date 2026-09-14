"""Independent verifier for the A3 Runtime Capability Admission DryRun v1."""

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

from .cognitive_analysis_runtime_admission_dryrun_runner_v1 import (
    ADMISSION_DRYRUN_RESULT_FILENAME_V1,
    canonical_json_v1,
)
from .cognitive_analysis_runtime_admission_dryrun_types_v1 import (
    ADMISSION_DRYRUN_PHASE_V1,
    ADMISSION_DRYRUN_RUN_ID_V1,
    ADMISSION_DRYRUN_VERIFIER_ID_V1,
    CognitiveAnalysisRuntimeAdmissionDryRunVerificationResultV1,
)


ADMISSION_DRYRUN_VERIFICATION_FILENAME_V1 = (
    "cognitive_analysis_runtime_capability_admission_dryrun_verification_v1.json"
)


def verify_cognitive_analysis_runtime_admission_dryrun_v1(
    project_root: Path,
    output_dir: Path,
) -> CognitiveAnalysisRuntimeAdmissionDryRunVerificationResultV1:
    """Read candidate output and L1 references; never invoke the Runner."""
    source_path = output_dir / ADMISSION_DRYRUN_RESULT_FILENAME_V1
    source_present = source_path.is_file()
    source_raw = source_path.read_text(encoding="utf-8") if source_present else ""
    source = json.loads(source_raw) if source_present else {}
    candidate = build_cognitive_analysis_runtime_registration_candidate_v1()
    candidate_validation = validate_cognitive_analysis_runtime_registration_candidate_v1(
        candidate, project_root
    )
    required_contracts = {
        MODEL_SKILL_ADMISSION_CONTRACT_REF_V1,
        PERMISSION_ADMISSION_CONTRACT_REF_V1,
        RUNTIME_BOUNDARY_CONTRACT_REF_V1,
        OUTPUT_CANDIDATE_CONTRACT_REF_V1,
    }
    registry_reference_ok = (
        source_present
        and source.get("registry_ref") == candidate.registry_ref
        and (project_root / candidate.registry_ref).is_file()
        and source.get("registry_record_exists") is False
    )
    lifecycle_consistent = source_present and source.get("lifecycle_state") == "candidate"
    contract_complete = required_contracts.issubset(candidate.required_contracts)
    permission_reference_ok = PERMISSION_ADMISSION_CONTRACT_REF_V1 in candidate.required_contracts
    boundary_consistent = source_present and all(source.get(name) is False for name in (
        "admission_applied",
        "registry_write_applied",
        "capability_activation_applied",
        "permission_grant_applied",
        "runtime_executed",
        "runtime_authorized",
    ))
    deterministic_output_ok = (
        source_present
        and source_raw == canonical_json_v1(source)
        and source.get("deterministic_output") is True
    )
    checks = (
        source_present,
        source.get("phase") == ADMISSION_DRYRUN_PHASE_V1,
        source.get("run_id") == ADMISSION_DRYRUN_RUN_ID_V1,
        registry_reference_ok,
        lifecycle_consistent,
        contract_complete,
        permission_reference_ok,
        boundary_consistent,
        candidate_validation.valid,
        source.get("admission_status") == "admission_candidate_ready",
        source.get("blocker_count") == 0,
        deterministic_output_ok,
    )
    failed_checks = sum(not check for check in checks)
    result = CognitiveAnalysisRuntimeAdmissionDryRunVerificationResultV1(
        verifier_id=ADMISSION_DRYRUN_VERIFIER_ID_V1,
        source_result_ref=ADMISSION_DRYRUN_RESULT_FILENAME_V1,
        passed_checks=len(checks) - failed_checks,
        failed_checks=failed_checks,
        blocker_count=failed_checks,
        warning_count=int(source.get("warning_count", 0)) if source_present else 0,
        registry_reference_ok=registry_reference_ok,
        lifecycle_consistent=lifecycle_consistent,
        contract_complete=contract_complete,
        permission_reference_ok=permission_reference_ok,
        boundary_consistent=boundary_consistent,
        deterministic_output_ok=deterministic_output_ok,
        verifier_invoked_runner=False,
        runtime_authorized=False,
        final_candidate_decision=(
            "CAPABILITY_ADMISSION_DRYRUN_VERIFICATION_CANDIDATE_PASS"
            if failed_checks == 0
            else "CAPABILITY_ADMISSION_DRYRUN_VERIFICATION_CANDIDATE_BLOCKED"
        ),
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / ADMISSION_DRYRUN_VERIFICATION_FILENAME_V1).write_text(
        canonical_json_v1(result), encoding="utf-8"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = verify_cognitive_analysis_runtime_admission_dryrun_v1(
        Path(args.project_root), Path(args.output_dir)
    )
    print(canonical_json_v1(result))


if __name__ == "__main__":
    main()
