"""Independent verifier for serialized Concept Validation Closure output only."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable, List, Mapping

from .cognitive_concept_validation_types_v1 import (
    CONCEPT_VALIDATION_PHASE_V1,
    CONCEPT_VALIDATION_SCHEMA_VERSION_V1,
    REQUIRED_CASE_TYPES_V1,
)


_REQUIRED_CHECKS_V1 = (
    "source_dryrun_identity_valid", "six_concept_types_covered", "source_negative_flags_valid",
    "all_schema_valid", "all_semantic_mappings_valid", "all_primitive_references_valid",
    "all_context_references_valid", "all_provenance_closed", "all_candidate_lifecycles_valid",
    "all_provider_taxonomies_clean", "language_boundary_design_only",
)
_REQUIRED_GUARDS_V1 = (
    "concept_not_fact", "concept_not_decision", "concept_not_action", "no_field_state_mutation",
    "no_memory_write", "no_learning_admission", "no_language_to_concept_reverse_generation",
    "provider_identity_not_concept_taxonomy",
)


def verify_concept_validation_payload_v1(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    """Read only serialized closure evidence; do not import Runner, Skeleton, or generator."""

    issues: List[Mapping[str, str]] = []
    checks_performed = 0
    if payload.get("schema_version") != CONCEPT_VALIDATION_SCHEMA_VERSION_V1 or payload.get("phase") != CONCEPT_VALIDATION_PHASE_V1:
        issues.append({"check_id": "closure.identity", "message": "closure schema or phase mismatch"})
    checks_performed += 1
    for field in ("runtime_executed", "model_invoked", "provider_invoked", "external_call", "field_kernel_mutated", "reducer_invoked", "language_runtime_executed", "hive_integrated", "learning_integrated"):
        checks_performed += 1
        if payload.get(field) is not False:
            issues.append({"check_id": "boundary.{0}".format(field), "message": "{0} must be false".format(field)})
    checks = payload.get("checks")
    if not isinstance(checks, Mapping):
        issues.append({"check_id": "closure.checks", "message": "checks object required"})
        checks = {}
    for name in _REQUIRED_CHECKS_V1:
        checks_performed += 1
        if checks.get(name) is not True:
            issues.append({"check_id": "check.{0}".format(name), "message": "required closure check failed"})
    guards = payload.get("negative_guard_results")
    if not isinstance(guards, Mapping):
        issues.append({"check_id": "closure.guards", "message": "negative guard result object required"})
        guards = {}
    for name in _REQUIRED_GUARDS_V1:
        checks_performed += 1
        if guards.get(name) is not True:
            issues.append({"check_id": "guard.{0}".format(name), "message": "negative guard failed"})
    results = payload.get("case_results")
    if not isinstance(results, list) or len(results) != len(REQUIRED_CASE_TYPES_V1):
        issues.append({"check_id": "case.count", "message": "six validation case records required"})
        results = []
    observed = set()
    for result in results:
        checks_performed += 1
        if not isinstance(result, Mapping):
            issues.append({"check_id": "case.shape", "message": "case result must be an object"})
            continue
        case_id = result.get("case_id")
        observed.add(case_id)
        if result.get("actual_concept_type") != REQUIRED_CASE_TYPES_V1.get(case_id):
            issues.append({"check_id": "case.type", "message": "unexpected Concept type for {0}".format(case_id)})
        chain = result.get("provenance_chain")
        if not isinstance(chain, Mapping) or not all(chain.get(name) for name in ("concept_ref", "primitive_refs", "translation_refs", "evidence_refs_v1", "source_capability_refs")):
            issues.append({"check_id": "case.provenance", "message": "incomplete Concept-to-capability chain for {0}".format(case_id)})
    checks_performed += 1
    if observed != set(REQUIRED_CASE_TYPES_V1):
        issues.append({"check_id": "case.coverage", "message": "required six Concept categories missing"})
    return {
        "valid": not issues,
        "issues": issues,
        "checks_performed": checks_performed,
        "verifier_independence": "serialized_validation_output_only_no_runner_skeleton_or_generator_import",
    }


def verify_concept_validation_file_v1(input_path: Path, compare_path: Path | None = None) -> Mapping[str, Any]:
    raw = input_path.read_text(encoding="utf-8")
    payload = json.loads(raw)
    result = dict(verify_concept_validation_payload_v1(payload))
    canonical = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    result["canonical_serialization"] = raw == canonical
    if compare_path is not None:
        result["comparison_equal"] = raw == compare_path.read_text(encoding="utf-8")
        if not result["comparison_equal"]:
            result["valid"] = False
            result["issues"] = list(result["issues"]) + [{"check_id": "determinism.comparison", "message": "run1 and run2 differ"}]
    return result


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify serialized Concept Validation Closure v1.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--compare", type=Path)
    arguments = parser.parse_args(argv)
    result = verify_concept_validation_file_v1(arguments.input, arguments.compare)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
