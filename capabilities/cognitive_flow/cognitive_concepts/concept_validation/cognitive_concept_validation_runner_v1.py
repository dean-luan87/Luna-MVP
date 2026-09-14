"""Read-only Validation Closure runner over frozen Concept DryRun evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping

from .cognitive_concept_validation_serializer_v1 import serialize_canonical_json_v1
from .cognitive_concept_validation_types_v1 import (
    CONCEPT_VALIDATION_PHASE_V1,
    CONCEPT_VALIDATION_RESULT_FILENAME_V1,
    CONCEPT_VALIDATION_SCHEMA_VERSION_V1,
    REQUIRED_CASE_TYPES_V1,
    SOURCE_DRYRUN_PHASE_V1,
    SOURCE_DRYRUN_SCHEMA_VERSION_V1,
)


_FORBIDDEN_FIELDS_V1 = {
    "fact_id", "decision_id", "action_id", "state_write_target", "memory_target",
}
_FORBIDDEN_SOURCE_FLAGS_V1 = (
    "runtime_executed", "model_invoked", "provider_invoked", "external_call",
    "database_written", "field_kernel_mutated", "reducer_invoked", "fact_created",
    "decision_created", "action_created", "state_writeback", "memory_updated",
    "learning_integrated", "language_encoding_executed",
)


def _case_validation_v1(row: Mapping[str, Any]) -> Dict[str, Any]:
    candidate = row.get("candidate") if isinstance(row.get("candidate"), Mapping) else {}
    provenance = candidate.get("provenance") if isinstance(candidate.get("provenance"), Mapping) else {}
    trace_ref = candidate.get("trace_ref")
    concept_type = str(candidate.get("concept_type", "")).lower()
    primitive_refs = candidate.get("primitive_refs")
    context_refs = candidate.get("context_refs")
    source_refs = provenance.get("source_refs")
    translation_refs = provenance.get("translation_refs")
    capability_refs = provenance.get("source_capability_refs")
    case_id = row.get("case_id")
    expected_type = REQUIRED_CASE_TYPES_V1.get(case_id)
    schema_valid = all(candidate.get(name) not in (None, "", [], {}, ()) for name in (
        "concept_id", "concept_type", "primitive_refs", "pattern_refs", "context_refs",
        "confidence", "uncertainty", "provenance", "trace_ref",
    ))
    primitive_integrity = isinstance(primitive_refs, list) and bool(primitive_refs) and all(
        isinstance(item, str) and item.startswith("primitive:") for item in primitive_refs
    )
    context_integrity = isinstance(context_refs, list) and bool(context_refs) and all(
        isinstance(item, str) and item.startswith("context:") for item in context_refs
    )
    evidence_integrity = isinstance(source_refs, list) and bool(source_refs) and all(
        isinstance(item, str) and item.startswith("provenance:") for item in source_refs
    )
    provenance_closure = bool(translation_refs) and bool(capability_refs) and evidence_integrity and provenance.get("trace_ref") == trace_ref
    candidate_boundary = candidate.get("candidate_only") is True and candidate.get("fact_status") == "not_fact" and not _FORBIDDEN_FIELDS_V1.intersection(candidate)
    provider_taxonomy_free = not any(token in concept_type for token in ("gemma", "ocr", "vision", "provider", "model"))
    return {
        "case_id": case_id,
        "expected_concept_type": expected_type,
        "actual_concept_type": candidate.get("concept_type"),
        "schema_valid": schema_valid,
        "semantic_mapping_valid": expected_type == candidate.get("concept_type"),
        "primitive_reference_integrity": primitive_integrity,
        "context_reference_integrity": context_integrity,
        "provenance_closure": provenance_closure,
        "candidate_lifecycle_valid": candidate_boundary,
        "provider_taxonomy_free": provider_taxonomy_free,
        "trace_ref": trace_ref,
        "provenance_chain": {
            "concept_ref": candidate.get("concept_id"),
            "primitive_refs": primitive_refs,
            "translation_refs": translation_refs,
            "evidence_refs_v1": source_refs,
            "source_capability_refs": capability_refs,
        },
    }


def run_concept_validation_closure_v1(dryrun_path: Path) -> Dict[str, Any]:
    """Validate frozen DryRun evidence without calling Runner, Skeleton, or a generator."""

    source = json.loads(dryrun_path.read_text(encoding="utf-8"))
    rows = source.get("cases") if isinstance(source.get("cases"), list) else []
    case_results: List[Dict[str, Any]] = [_case_validation_v1(row) for row in rows if isinstance(row, Mapping)]
    flags_valid = all(source.get(flag) is False for flag in _FORBIDDEN_SOURCE_FLAGS_V1)
    case_ids = {item.get("case_id") for item in case_results}
    checks = {
        "source_dryrun_identity_valid": source.get("schema_version") == SOURCE_DRYRUN_SCHEMA_VERSION_V1 and source.get("phase") == SOURCE_DRYRUN_PHASE_V1,
        "six_concept_types_covered": case_ids == set(REQUIRED_CASE_TYPES_V1),
        "source_negative_flags_valid": flags_valid,
        "all_schema_valid": all(item["schema_valid"] for item in case_results),
        "all_semantic_mappings_valid": all(item["semantic_mapping_valid"] for item in case_results),
        "all_primitive_references_valid": all(item["primitive_reference_integrity"] for item in case_results),
        "all_context_references_valid": all(item["context_reference_integrity"] for item in case_results),
        "all_provenance_closed": all(item["provenance_closure"] for item in case_results),
        "all_candidate_lifecycles_valid": all(item["candidate_lifecycle_valid"] for item in case_results),
        "all_provider_taxonomies_clean": all(item["provider_taxonomy_free"] for item in case_results),
        "language_boundary_design_only": True,
    }
    negative_guards = {
        "concept_not_fact": checks["all_candidate_lifecycles_valid"],
        "concept_not_decision": source.get("decision_created") is False,
        "concept_not_action": source.get("action_created") is False,
        "no_field_state_mutation": source.get("field_kernel_mutated") is False and source.get("state_writeback") is False,
        "no_memory_write": source.get("memory_updated") is False,
        "no_learning_admission": source.get("learning_integrated") is False,
        "no_language_to_concept_reverse_generation": source.get("language_encoding_executed") is False,
        "provider_identity_not_concept_taxonomy": checks["all_provider_taxonomies_clean"],
    }
    return {
        "schema_version": CONCEPT_VALIDATION_SCHEMA_VERSION_V1,
        "phase": CONCEPT_VALIDATION_PHASE_V1,
        "validation_mode": "controlled_validation_closure",
        "source_dryrun": {
            "schema_version": source.get("schema_version"),
            "phase": source.get("phase"),
            "fixture_only": source.get("fixture_only"),
            "simulation_only": source.get("simulation_only"),
        },
        "validation_executed": True,
        "runtime_executed": False,
        "model_invoked": False,
        "provider_invoked": False,
        "external_call": False,
        "field_kernel_mutated": False,
        "reducer_invoked": False,
        "language_runtime_executed": False,
        "hive_integrated": False,
        "learning_integrated": False,
        "case_results": case_results,
        "checks": checks,
        "negative_guard_results": negative_guards,
        "source_output_ref": "cognitive_concept_dryrun_result_v1.json",
    }


def write_concept_validation_closure_v1(dryrun_path: Path, output_directory: Path) -> Path:
    output_directory.mkdir(parents=True, exist_ok=True)
    target = output_directory / CONCEPT_VALIDATION_RESULT_FILENAME_V1
    target.write_text(serialize_canonical_json_v1(run_concept_validation_closure_v1(dryrun_path)), encoding="utf-8")
    return target


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Concept Validation Closure v1 over frozen DryRun evidence.")
    parser.add_argument("--dryrun-input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    arguments = parser.parse_args(argv)
    print(write_concept_validation_closure_v1(arguments.dryrun_input, arguments.output_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
