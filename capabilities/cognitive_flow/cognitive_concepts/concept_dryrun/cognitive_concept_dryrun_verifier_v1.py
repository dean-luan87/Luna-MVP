"""Independent, serialized-output verifier for Cognitive Concept DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable, List, Mapping, Tuple


_PHASE_V1 = "Phase-A3-Cognitive-Concept-Layer-DryRun-v1-001"
_SCHEMA_V1 = "luna.cognitive_concept.dryrun.v1"
_EXPECTED_TYPES_V1 = {
    "case_1_pattern": "pattern_concept_candidate",
    "case_2_situation": "situation_concept_candidate",
    "case_3_relationship": "relationship_concept_candidate",
    "case_4_risk": "risk_candidate_concept",
    "case_5_context": "context_concept_candidate",
    "case_6_goal": "goal_candidate_concept",
}
_FORBIDDEN_FIELDS_V1 = {
    "fact_id", "decision_id", "action_id", "state_write_target", "memory_target",
}
_NEGATIVE_FLAG_FIELDS_V1 = (
    "runtime_executed", "model_invoked", "provider_invoked", "external_call",
    "database_written", "field_kernel_mutated", "reducer_invoked", "fact_created",
    "decision_created", "action_created", "state_writeback", "memory_updated",
    "learning_integrated", "language_encoding_executed",
)


def _issue(issues: List[Mapping[str, str]], check_id: str, message: str) -> None:
    issues.append({"check_id": check_id, "message": message})


def verify_concept_dryrun_payload_v1(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    """Validate only serialized output; this module imports no Runner or Skeleton."""

    issues: List[Mapping[str, str]] = []
    check_count = 0
    check_count += 1
    if payload.get("schema_version") != _SCHEMA_V1 or payload.get("phase") != _PHASE_V1:
        _issue(issues, "root.schema", "schema_version or phase does not match the frozen DryRun contract")
    check_count += 1
    if payload.get("execution_mode") != "controlled_dryrun" or payload.get("simulation_only") is not True or payload.get("fixture_only") is not True:
        _issue(issues, "root.mode", "output is not marked as fixture-only controlled DryRun")
    for field in _NEGATIVE_FLAG_FIELDS_V1:
        check_count += 1
        if payload.get(field) is not False:
            _issue(issues, "negative_guard.{0}".format(field), "{0} must be false".format(field))
    cases = payload.get("cases")
    check_count += 1
    if not isinstance(cases, list) or len(cases) != len(_EXPECTED_TYPES_V1):
        _issue(issues, "case.count", "exactly six fixed Concept DryRun cases are required")
        cases = []
    received_case_ids = set()
    for row in cases:
        check_count += 1
        if not isinstance(row, Mapping):
            _issue(issues, "case.shape", "every case row must be an object")
            continue
        case_id = row.get("case_id")
        received_case_ids.add(case_id)
        candidate = row.get("candidate")
        expected_type = _EXPECTED_TYPES_V1.get(case_id)
        if expected_type is None:
            _issue(issues, "case.id", "unexpected case identifier: {0}".format(case_id))
            continue
        if not isinstance(candidate, Mapping):
            _issue(issues, "candidate.shape", "candidate envelope is absent for {0}".format(case_id))
            continue
        for field in ("concept_id", "concept_type", "primitive_refs", "context_refs", "pattern_refs", "confidence", "uncertainty", "provenance", "trace_ref"):
            check_count += 1
            if candidate.get(field) in (None, "", (), [], {}):
                _issue(issues, "candidate.{0}".format(field), "{0} is required for {1}".format(field, case_id))
        check_count += 1
        if candidate.get("concept_type") != expected_type:
            _issue(issues, "semantic.type", "concept type mismatch for {0}".format(case_id))
        check_count += 1
        if candidate.get("candidate_only") is not True or candidate.get("fact_status") != "not_fact":
            _issue(issues, "boundary.candidate_only", "candidate-only / not-fact boundary failed for {0}".format(case_id))
        check_count += 1
        if _FORBIDDEN_FIELDS_V1.intersection(candidate):
            _issue(issues, "boundary.forbidden_fields", "authority-bearing field present for {0}".format(case_id))
        provenance = candidate.get("provenance")
        check_count += 1
        if not isinstance(provenance, Mapping) or not provenance.get("source_refs") or not provenance.get("translation_refs") or not provenance.get("source_capability_refs") or provenance.get("trace_ref") != candidate.get("trace_ref"):
            _issue(issues, "provenance.closure", "provenance chain is incomplete for {0}".format(case_id))
        check_count += 1
        concept_type = str(candidate.get("concept_type", "")).lower()
        if any(provider in concept_type for provider in ("gemma", "ocr", "vision", "provider", "model")):
            _issue(issues, "guard.provider_taxonomy", "provider identity entered Concept taxonomy for {0}".format(case_id))
    check_count += 1
    if received_case_ids != set(_EXPECTED_TYPES_V1):
        _issue(issues, "case.coverage", "six required fixture mappings are not all represented")
    return {
        "valid": not issues,
        "issues": issues,
        "checks_performed": check_count,
        "verifier_independence": "serialized_output_only_no_runner_or_skeleton_import",
        "deterministic_validation": True,
    }


def verify_concept_dryrun_file_v1(input_path: Path, compare_path: Path | None = None) -> Mapping[str, Any]:
    raw = input_path.read_text(encoding="utf-8")
    payload = json.loads(raw)
    result = dict(verify_concept_dryrun_payload_v1(payload))
    canonical = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    result["canonical_serialization"] = raw == canonical
    if compare_path is not None:
        result["deterministic_rerun_equal"] = raw == compare_path.read_text(encoding="utf-8")
        if not result["deterministic_rerun_equal"]:
            result["valid"] = False
            result["issues"] = list(result["issues"]) + [{"check_id": "determinism.rerun", "message": "run outputs differ"}]
    return result


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify serialized Concept Layer DryRun evidence v1.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--compare", type=Path)
    arguments = parser.parse_args(argv)
    result = verify_concept_dryrun_file_v1(arguments.input, arguments.compare)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
