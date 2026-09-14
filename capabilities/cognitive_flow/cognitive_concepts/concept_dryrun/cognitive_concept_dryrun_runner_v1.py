"""Fixture-only controlled DryRun runner for Cognitive Concept Layer v1."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

from ..controlled_skeleton.cognitive_concept_skeleton_v1 import (
    CognitiveConceptControlledSkeletonV1,
)
from .cognitive_concept_dryrun_serializer_v1 import serialize_canonical_json_v1
from .cognitive_concept_dryrun_types_v1 import (
    CONCEPT_DRYRUN_PHASE_V1,
    CONCEPT_DRYRUN_RESULT_FILENAME_V1,
    CONCEPT_DRYRUN_SCHEMA_VERSION_V1,
    ConceptDryRunCaseV1,
)


_FIXTURE_CONTEXT_REF_V1 = "context:fixture:concept-dryrun:v1"


def fixed_concept_fixture_cases_v1() -> Tuple[ConceptDryRunCaseV1, ...]:
    """Return the six frozen inputs; no rule evaluation or inference occurs."""

    return (
        ConceptDryRunCaseV1(
            "case_1_pattern", "pattern_concept_candidate",
            ("primitive:fixture:entity:person:v1", "primitive:fixture:state:moving:v1"),
            ("pattern:fixture:movement-cluster:v1",), (_FIXTURE_CONTEXT_REF_V1,),
            "pattern_candidate_fixture_only",
        ),
        ConceptDryRunCaseV1(
            "case_2_situation", "situation_concept_candidate",
            ("primitive:fixture:situation:entry-area:v1",),
            ("pattern:fixture:situation-cluster:v1",), (_FIXTURE_CONTEXT_REF_V1,),
            "situation_candidate_fixture_only",
        ),
        ConceptDryRunCaseV1(
            "case_3_relationship", "relationship_concept_candidate",
            ("primitive:fixture:relation:near:v1",),
            ("pattern:fixture:relation-cluster:v1",), (_FIXTURE_CONTEXT_REF_V1,),
            "relationship_candidate_fixture_only",
        ),
        ConceptDryRunCaseV1(
            "case_4_risk", "risk_candidate_concept",
            ("primitive:fixture:entity:unknown-person:v1", "primitive:fixture:event:approaching:v1"),
            ("pattern:fixture:risk-cluster:v1",), (_FIXTURE_CONTEXT_REF_V1,),
            "risk_candidate_fixture_only",
        ),
        ConceptDryRunCaseV1(
            "case_5_context", "context_concept_candidate",
            ("primitive:fixture:context:night:v1", "primitive:fixture:state:low-visibility:v1"),
            ("pattern:fixture:context-cluster:v1",), (_FIXTURE_CONTEXT_REF_V1,),
            "context_candidate_fixture_only",
        ),
        ConceptDryRunCaseV1(
            "case_6_goal", "goal_candidate_concept",
            ("primitive:fixture:event:navigation:v1", "primitive:fixture:entity:entrance:v1"),
            ("pattern:fixture:goal-cluster:v1",), (_FIXTURE_CONTEXT_REF_V1,),
            "goal_candidate_fixture_only",
        ),
    )


def _candidate_input_v1(case: ConceptDryRunCaseV1) -> Dict[str, Any]:
    trace_ref = "trace:fixture:concept-dryrun:{0}:v1".format(case.case_id)
    return {
        "concept_id": "concept:fixture:{0}:v1".format(case.case_id),
        "concept_type": case.expected_concept_type,
        "primitive_refs": case.primitive_refs,
        "pattern_refs": case.pattern_refs,
        "context_refs": case.context_refs,
        "semantic_description": case.semantic_description,
        "confidence": 0.5,
        "uncertainty": {"status": "fixture_only", "reason": "no_inference"},
        "provenance": {
            "source_refs": ("provenance:fixture:{0}:v1".format(case.case_id),),
            "translation_refs": ("translation:fixture:{0}:v1".format(case.case_id),),
            "source_capability_refs": ("capability:fixture:translation-layer:v1",),
            "trace_ref": trace_ref,
        },
        "trace_ref": trace_ref,
        "candidate_status": "concept_fixture_candidate",
        "candidate_only": True,
        "fact_status": "not_fact",
    }


def run_concept_dryrun_v1() -> Dict[str, Any]:
    """Build deterministic candidate-only envelopes from the six fixed inputs."""

    cases = []
    for case in fixed_concept_fixture_cases_v1():
        candidate = CognitiveConceptControlledSkeletonV1.create_concept_candidate(
            _candidate_input_v1(case)
        )
        validation = CognitiveConceptControlledSkeletonV1.validate_concept_candidate(candidate)
        if not validation.valid:
            raise ValueError("controlled skeleton rejected fixed fixture: {0}".format(case.case_id))
        cases.append({
            "case_id": case.case_id,
            "fixture_type": "fixed_primitive_reference_fixture",
            "expected_concept_type": case.expected_concept_type,
            "candidate": asdict(candidate),
            "skeleton_validation": {"valid": validation.valid, "issues": []},
        })
    return {
        "schema_version": CONCEPT_DRYRUN_SCHEMA_VERSION_V1,
        "phase": CONCEPT_DRYRUN_PHASE_V1,
        "execution_mode": "controlled_dryrun",
        "runtime_executed": False,
        "simulation_only": True,
        "fixture_only": True,
        "model_invoked": False,
        "provider_invoked": False,
        "external_call": False,
        "database_written": False,
        "field_kernel_mutated": False,
        "reducer_invoked": False,
        "fact_created": False,
        "decision_created": False,
        "action_created": False,
        "state_writeback": False,
        "memory_updated": False,
        "learning_integrated": False,
        "language_encoding_executed": False,
        "case_count": len(cases),
        "cases": cases,
    }


def write_concept_dryrun_output_v1(output_directory: Path) -> Path:
    output_directory.mkdir(parents=True, exist_ok=True)
    target = output_directory / CONCEPT_DRYRUN_RESULT_FILENAME_V1
    target.write_text(serialize_canonical_json_v1(run_concept_dryrun_v1()), encoding="utf-8")
    return target


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Concept Layer fixture-only DryRun v1.")
    parser.add_argument("--output-dir", required=True, type=Path)
    arguments = parser.parse_args(argv)
    print(write_concept_dryrun_output_v1(arguments.output_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
