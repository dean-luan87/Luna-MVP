"""Fixed-reference-only runner for Cognitive Field Representation DryRun v1."""

from __future__ import annotations
import argparse
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Iterable

from ..controlled_skeleton.cognitive_field_representation_skeleton_v1 import CognitiveFieldRepresentationControlledSkeletonV1
from .cognitive_field_dryrun_serializer_v1 import serialize_canonical_json_v1
from .cognitive_field_dryrun_types_v1 import FIELD_DRYRUN_CASES_V1, FIELD_DRYRUN_PHASE_V1, FIELD_DRYRUN_RESULT_FILENAME_V1, FIELD_DRYRUN_SCHEMA_VERSION_V1


def _fixture_input_v1(case_id: str, field_kind: str) -> Dict[str, Any]:
    trace = "trace:fixture:field-dryrun:{0}:v1".format(case_id)
    return {
        "field_candidate_id": "field-candidate:fixture:{0}:v1".format(case_id),
        "context_refs": ("context:fixture:{0}:v1".format(case_id),),
        "snapshot_refs": ("snapshot:fixture:{0}:v1".format(case_id),),
        "primitive_refs": ("primitive:fixture:{0}:v1".format(case_id),),
        "concept_refs": ("concept:fixture:{0}:v1".format(case_id),),
        "temporal_scope": {"temporal_ref": "temporal:fixture:{0}:v1".format(case_id), "status": "fixture_unknown_preserved"},
        "spatial_scope": {"spatial_ref": "spatial:fixture:{0}:v1".format(case_id), "status": "fixture_reference_only"},
        "task_scope": {"task_ref": "task:fixture:{0}:v1".format(case_id)},
        "attention_scope": {"attention_ref": "attention:fixture:{0}:v1".format(case_id), "priority_status": "selection_only"},
        "relevance_partition": {"primary_now": ("primitive:fixture:{0}:v1".format(case_id),), "peripheral_now": ("concept:fixture:{0}:v1".format(case_id),), "deferred_candidate": (), "excluded_for_current_context_only": ()},
        "uncertainty": {"status": "fixture_only", "reason": "no_runtime_or_world_assertion"},
        "provenance": {"source_refs": ("evidence:fixture:{0}:v1".format(case_id),), "concept_binding_refs": ("binding:fixture:{0}:v1".format(case_id),), "source_capability_refs": ("capability:fixture:translation:v1",), "trace_ref": trace},
        "trace_ref": trace,
        "candidate_status": field_kind,
        "candidate_only": True, "field_state": False, "not_state": True, "not_fact": True,
    }


def run_cognitive_field_dryrun_v1() -> Dict[str, Any]:
    cases = []
    for case_id, kind in FIELD_DRYRUN_CASES_V1.items():
        candidate = CognitiveFieldRepresentationControlledSkeletonV1.create_field_representation_candidate(_fixture_input_v1(case_id, kind))
        validation = CognitiveFieldRepresentationControlledSkeletonV1.validate_field_representation_candidate(candidate)
        if not validation.valid:
            raise ValueError("skeleton rejected fixed Field fixture: " + case_id)
        cases.append({"case_id": case_id, "field_fixture_type": kind, "candidate": asdict(candidate), "skeleton_validation": {"valid": True, "issues": []}})
    return {"schema_version": FIELD_DRYRUN_SCHEMA_VERSION_V1, "phase": FIELD_DRYRUN_PHASE_V1, "execution_mode": "controlled_dryrun", "runtime_executed": False, "simulation_only": True, "fixture_only": True, "model_invoked": False, "provider_invoked": False, "external_call": False, "slam_invoked": False, "database_written": False, "field_kernel_mutated": False, "reducer_invoked": False, "state_mutation": False, "snapshot_updated": False, "temporal_history_modified": False, "fact_created": False, "decision_created": False, "action_created": False, "memory_updated": False, "learning_integrated": False, "case_count": len(cases), "cases": cases}


def write_cognitive_field_dryrun_v1(output_directory: Path) -> Path:
    output_directory.mkdir(parents=True, exist_ok=True)
    target = output_directory / FIELD_DRYRUN_RESULT_FILENAME_V1
    target.write_text(serialize_canonical_json_v1(run_cognitive_field_dryrun_v1()), encoding="utf-8")
    return target


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    print(write_cognitive_field_dryrun_v1(args.output_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
