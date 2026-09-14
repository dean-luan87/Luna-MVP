"""Fixture-only runner; invokes only the in-memory Primitive Skeleton."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path

from capabilities.cognitive_flow.cognitive_primitives.controlled_skeleton.cognitive_primitive_skeleton_v1 import CognitivePrimitiveControlledSkeletonV1

from .cognitive_primitive_dryrun_serializer_v1 import canonical_json_v1, write_result_v1
from .cognitive_primitive_dryrun_types_v1 import PRIMITIVE_DRYRUN_PHASE_V1, PRIMITIVE_DRYRUN_SCHEMA_V1


def _fixture_cases_v1():
    base = {
        "context_refs": ("context:fixture:primitive-dryrun:v1",),
        "confidence": None,
        "uncertainty": {"status": "not_evaluated"},
        "candidate_status": "primitive_not_admitted",
    }
    return (
        ("case_1_vision_entity", "vision", "entity_primitive_candidate", "evidence:fixture:vision:object:v1", "capability:fixture:vision:v1", {"entity_kind": "person_candidate"}),
        ("case_2_ocr_entity", "ocr", "entity_primitive_candidate", "evidence:fixture:ocr:text:v1", "capability:fixture:ocr:v1", {"entity_kind": "text_bearing_object_candidate"}),
        ("case_3_spatial_relation", "spatial", "relation_primitive_candidate", "evidence:fixture:spatial:location:v1", "capability:fixture:spatial:v1", {"subject_ref": "entity:fixture:a", "predicate": "near_candidate", "object_ref": "entity:fixture:b"}),
        ("case_4_temporal_event", "temporal", "event_primitive_candidate", "evidence:fixture:temporal:change:v1", "capability:fixture:temporal:v1", {"event_kind": "change_candidate", "temporal_context": {"status": "unknown_start"}}),
        ("case_5_context_situation", "situation", "situation_primitive_candidate", "evidence:fixture:context:situation:v1", "capability:fixture:context:v1", {"situation_kind": "scene_candidate", "member_refs": ("entity:fixture:a",)}),
    ), base


def run_cognitive_primitive_dryrun_v1(output_dir: Path):
    skeleton = CognitivePrimitiveControlledSkeletonV1()
    fixture_cases, base = _fixture_cases_v1()
    results = []
    for case_id, kind, primitive_type, evidence_ref, source_capability, extra in fixture_cases:
        trace_ref = f"trace:primitive-dryrun:{case_id}:v1"
        request = {
            **base, **extra,
            "primitive_id": f"primitive:{case_id}:v1",
            "primitive_type": primitive_type,
            "source_refs": (evidence_ref,),
            "provenance": {"source_refs": (f"provenance:{case_id}:v1",), "source_capability_refs": (source_capability,), "trace_ref": trace_ref},
            "trace_ref": trace_ref,
        }
        candidate = skeleton.create_candidate(request)
        validation = skeleton.validate_candidate(candidate)
        flags = asdict(skeleton.flags())
        semantic_ok = candidate.candidate_only and candidate.fact_status == "not_fact" and candidate.primitive_type == primitive_type
        provenance_ok = candidate.source_refs == (evidence_ref,) and candidate.provenance.get("trace_ref") == trace_ref and source_capability in candidate.provenance.get("source_capability_refs", ())
        guards_ok = all(value is False for value in flags.values())
        results.append({"case_id": case_id, "fixture_kind": kind, "expected_primitive_type": primitive_type, "candidate": asdict(candidate), "schema_valid": validation.valid, "issues": [asdict(issue) for issue in validation.issues], "semantic_boundary_valid": semantic_ok, "provenance_valid": provenance_ok, "negative_guards_valid": guards_ok, "case_passed": validation.valid and semantic_ok and provenance_ok and guards_ok})
    passed = all(item["case_passed"] for item in results)
    result = {"phase": PRIMITIVE_DRYRUN_PHASE_V1, "schema_version": PRIMITIVE_DRYRUN_SCHEMA_V1, "case_results": results, "runtime_flags": asdict(skeleton.flags()), "runtime_executed": False, "simulation_only": True, "model_invoked": False, "external_call": False, "field_kernel_mutated": False, "reducer_invoked": False, "all_cases_passed": passed, "deterministic_output": True, "blocker_count": 0 if passed else 1, "warning_count": 1, "final_candidate_decision": "COGNITIVE_PRIMITIVE_LAYER_DRYRUN_READY_WITH_NOTES" if passed else "COGNITIVE_PRIMITIVE_LAYER_DRYRUN_BLOCKED"}
    write_result_v1(output_dir, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--output-dir", required=True)
    print(canonical_json_v1(run_cognitive_primitive_dryrun_v1(Path(parser.parse_args().output_dir))))


if __name__ == "__main__":
    main()

