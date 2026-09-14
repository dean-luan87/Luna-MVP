from __future__ import annotations

import json
from pathlib import Path

from .archive_v1 import DEFAULT_ARCHIVE_ROOT, write_evaluation_run_record_v1
from .fixture_v1 import build_synthetic_evaluation_fixture_v1
from .run_boundary_v1 import new_evaluation_run_execution_id_v1
from .types_v1 import validate_evaluation_run_record_v1


OUTPUT_DIR = Path("_eval_out/level1_cognitive_evaluation_run_boundary_v1")


def build_synthetic_runner_summary_v1() -> dict:
    execution_instance_id = new_evaluation_run_execution_id_v1()
    fixture = build_synthetic_evaluation_fixture_v1(
        evaluation_run_id=(
            "evaluation-run:synthetic:level1:decision-governance-handoff:"
            + execution_instance_id
        )
    )
    archive_path, created = write_evaluation_run_record_v1(fixture.record)
    record_errors = validate_evaluation_run_record_v1(fixture.record)
    return {
        "phase": "Phase-P1-Luna-Level1-Cognitive-Evaluation-Run-Boundary-And-Durable-Archive-Bridge-v1-001",
        "execution_instance_id": execution_instance_id,
        "evaluation_run_id": fixture.record.evaluation_run.evaluation_run_id,
        "dataset_registry_ref": fixture.boundary.dataset_registry_ref,
        "dataset_ref": fixture.sample.dataset_ref,
        "sample_ref": fixture.sample.sample_id,
        "case_ref": fixture.case.cognitive_test_case_ref,
        "run_boundary_valid": fixture.boundary.valid,
        "run_boundary_errors": list(fixture.boundary.errors),
        "a_route_bridge_status": fixture.bridge.status,
        "a_route_bridge_missing_refs": list(fixture.bridge.missing_refs),
        "whitebox_attachment_status": fixture.whitebox.status,
        "whitebox_trace_ref": fixture.whitebox.trace_ref,
        "whitebox_profile_ref": fixture.whitebox.execution_profile_ref,
        "archive_record_created": created or archive_path.is_file(),
        "archive_record_immutable": fixture.record.immutable_by_identity,
        "archive_location": str(archive_path),
        "archive_root": str(DEFAULT_ARCHIVE_ROOT),
        "record_validation_errors": list(record_errors),
        "result_status": fixture.record.evaluation_run.result_status,
        "synthetic": True,
        "cognition_execution": False,
        "model_invocation": False,
        "provider_invocation": False,
        "observation_execution": False,
        "action_execution": False,
        "world_truth_declared": False,
        "field_mutation": False,
        "memory_promotion": False,
        "experience_promotion": False,
        "knowledge_promotion": False,
        "runtime_metrics_availability": "not_observed",
        "comparison_eligibility": "planned",
    }


def main() -> None:
    summary = build_synthetic_runner_summary_v1()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
