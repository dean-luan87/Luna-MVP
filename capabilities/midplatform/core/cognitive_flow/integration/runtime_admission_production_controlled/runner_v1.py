"""Controlled Runner for repository-backed Runtime Admission records."""

from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
from typing import Any, Dict, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.governed_capability_execution_record_production_controlled.yolo11n_producer_entry_v1 import (
    produce_yolo11n_governed_execution_records_v1,
)

from .producer_v1 import assess_runtime_admission_production_v1
from .repository_source_v1 import build_repository_runtime_admission_input_v1


def _cases(repo_root: Path) -> Tuple[Tuple[str, Any, bool], ...]:
    source = build_repository_runtime_admission_input_v1(
        repo_root,
        model_asset_id="model-asset:yolo11n:weights-v1",
        capability_id="object_detection",
        provider_family="yolo",
    )
    if source is None:
        return (("repository_input_missing", None, True),)
    return (
        ("repository_backed_positive", source, False),
        ("missing_capability_resolution", replace(source, capability_resolution=None), True),
        ("stale_capability_model_binding", replace(source, capability_model_binding=replace(source.capability_model_binding, lifecycle_status="STALE")), True),
        ("missing_model_provider_binding", replace(source, model_provider_binding=None), True),
        ("model_version_mismatch", replace(source, model_version_status_ref="MODEL_VERSION_MISMATCH"), True),
        ("grant_revoked", replace(source, grant_status_ref="GRANT_REVOKED"), True),
        ("permission_blocked", replace(source, permission_status_ref="PERMISSION_DENIED"), True),
        ("safety_blocked", replace(source, safety_status_ref="SAFETY_BLOCKED"), True),
        ("resource_unavailable", replace(source, resource_status_ref="RESOURCE_UNAVAILABLE"), True),
        ("working_envelope_incompatible", replace(source, working_envelope_status_ref="ENVELOPE_STALE"), True),
        ("input_invalidated", replace(source, invalidation_refs=("invalidation:runtime-admission:test",)), True),
        ("missing_provenance", replace(source, provenance_refs=()), True),
    )


def run_runtime_admission_production_v1(repo_root: Path) -> Dict[str, Any]:
    cases = []
    for case_id, source, expect_blocked in _cases(repo_root):
        if source is None:
            passed = expect_blocked
            failure = "RUNTIME_ADMISSION_REPOSITORY_INPUT_MISSING"
            executable = False
        else:
            result = assess_runtime_admission_production_v1(source)
            failure = result.failure.classification if result.failure else None
            executable = result.executable is not None
            passed = (not expect_blocked and result.failure is None and executable) or (expect_blocked and result.failure is not None and not executable)
        cases.append({
            "case_id": case_id,
            "passed": passed,
            "blocked": bool(failure),
            "failure": failure,
            "executable_candidate_produced": executable,
            "candidate_only": True,
            "runtime_execution": False,
            "model_loading": False,
            "provider_admission": False,
            "provider_invocation": False,
            "observation_execution": False,
            "action_execution": False,
            "source_mutation": False,
            "world_truth_declared": False,
        })
    governed = produce_yolo11n_governed_execution_records_v1(repo_root)
    return {
        "phase": "Phase-P1-Midplatform-Runtime-Admission-Production-Source-v1-001",
        "scenario_count": len(cases),
        "all_cases_passed": all(case["passed"] for case in cases),
        "failed_case_ids": [case["case_id"] for case in cases if not case["passed"]],
        "cases": cases,
        "record_bundle_produced": governed.bundle is not None,
        "governed_record_status": governed.status,
        "missing_declarations": list(governed.missing_declarations),
        "runtime_execution_count": 0,
        "model_loading_count": 0,
        "provider_admission_count": 0,
        "provider_invocation_count": 0,
        "observation_execution_count": 0,
        "action_execution_count": 0,
        "source_mutation_count": 0,
        "world_truth_count": 0,
        "key_guards": {
            "runtime_admission_owner": "Runtime Admission",
            "no_success_synthesis": governed.no_success_synthesized,
            "no_global_version": True,
            "candidate_only": True,
        },
    }


def main() -> None:
    root = Path(__file__).resolve().parents[6]
    print(json.dumps(run_runtime_admission_production_v1(root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
