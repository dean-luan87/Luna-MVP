"""Fixture-isolated Validation Closure runner for A3 Translation Layer v1."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict

from capabilities.cognitive_flow.cognitive_analysis.translation_dryrun.cognitive_translation_dryrun_runner_v1 import (
    build_translation_dryrun_fixture_cases_v1,
)
from capabilities.cognitive_flow.cognitive_analysis.translation_layer.cognitive_translation_contract_v1 import (
    NEGATIVE_GUARD_IDS_V1,
    TRANSLATION_LAYER_CONTRACT_ID_V1,
)
from capabilities.cognitive_flow.cognitive_analysis.translation_layer.cognitive_translation_skeleton_v1 import (
    CognitiveTranslationSkeletonV1,
)
from capabilities.cognitive_flow.cognitive_analysis.translation_layer.cognitive_translation_validator_v1 import (
    validate_cognitive_translation_candidate_envelope_v1,
)


VALIDATION_PHASE_V1 = (
    "Phase-A3-Evidence-Context-Translation-Layer-Validation-Closure-Execution-v1-001"
)
VALIDATION_SCHEMA_VERSION_V1 = "luna.cognitive_analysis.translation_validation_closure.v1"
_JSON_FILENAMES_V1 = (
    "translation_validation_result_v1.json",
    "semantic_boundary_result_v1.json",
    "provenance_closure_result_v1.json",
    "negative_guard_result_v1.json",
    "deterministic_result_v1.json",
)


def canonical_json_v1(value: Any) -> str:
    """Serialize without timestamps, random values, or environment-specific paths."""
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _boundary_flags_v1() -> Dict[str, bool]:
    return {
        "validation_executed": True,
        "runtime_executed": False,
        "model_invoked": False,
        "external_call": False,
        "state_writeback": False,
        "fact_created": False,
        "decision_created": False,
        "action_created": False,
        "memory_updated": False,
    }


def _provenance_closed_v1(request: Any, envelope: Any) -> bool:
    candidate = envelope.cognitive_primitive_candidate
    provenance = candidate.provenance
    return (
        candidate.source_refs == request.evidence_refs
        and candidate.context_refs == request.context_refs
        and tuple(provenance.get("source_refs", ())) == request.provenance_refs
        and tuple(provenance.get("source_capability_refs", ()))
        == request.source_capability_refs
        and provenance.get("trace_ref") == request.trace_ref
        and candidate.trace_ref == request.trace_ref
        and candidate.candidate_id not in request.source_capability_refs
    )


def _guard_results_v1(envelope: Any, provenance_closed: bool) -> Dict[str, bool]:
    candidate = envelope.cognitive_primitive_candidate
    flags = envelope.translation_flags
    return {
        "Guard-1-evidence-to-fact-forbidden": (
            candidate.candidate_only is True
            and candidate.fact_status == "not_fact"
            and candidate.candidate_status == "translation_not_executed"
            and flags.fact_created is False
        ),
        "Guard-2-evidence-to-decision-forbidden": (
            candidate.primitive_type.endswith("_candidate")
            and flags.decision_created is False
            and flags.action_created is False
        ),
        "Guard-3-provenance-required": provenance_closed,
        "Guard-4-external-model-identity-not-cognitive-entity": (
            candidate.candidate_id not in candidate.provenance.get(
                "source_capability_refs", ()
            )
            and "external_model_entity_ref" not in candidate.provenance
        ),
        "Guard-5-context-snapshot-field-state-mutation-forbidden": (
            flags.context_mutated is False
            and flags.snapshot_mutated is False
            and flags.state_writeback is False
            and flags.memory_updated is False
        ),
    }


def _build_validation_payloads_v1() -> Dict[str, Any]:
    """Evaluate fixed fixture envelopes only; no external Evidence is resolved."""
    skeleton = CognitiveTranslationSkeletonV1()
    cases = []
    semantic_cases = []
    provenance_cases = []
    guard_cases = []
    for fixture in build_translation_dryrun_fixture_cases_v1():
        envelope = skeleton.translate(fixture.request)
        contract_validation = validate_cognitive_translation_candidate_envelope_v1(
            fixture.request, envelope
        )
        provenance_closed = _provenance_closed_v1(fixture.request, envelope)
        guard_results = _guard_results_v1(envelope, provenance_closed)
        semantic_passed = (
            envelope.cognitive_primitive_candidate.primitive_type
            == fixture.expected_primitive_type
            and envelope.cognitive_primitive_candidate.candidate_only is True
            and envelope.cognitive_primitive_candidate.fact_status == "not_fact"
            and envelope.cognitive_primitive_candidate.candidate_status
            == "translation_not_executed"
        )
        case_passed = (
            contract_validation.valid
            and semantic_passed
            and provenance_closed
            and all(guard_results.values())
        )
        cases.append({
            "case_id": fixture.case_id,
            "fixture_kind": fixture.fixture_kind,
            "expected_primitive_type": fixture.expected_primitive_type,
            "expected_candidate_label": fixture.expected_candidate_label,
            "semantic_label_generated": False,
            "request": asdict(fixture.request),
            "translation_candidate_envelope": asdict(envelope),
            "contract_valid": contract_validation.valid,
            "contract_issue_codes": [issue.code for issue in contract_validation.issues],
            "semantic_boundary_passed": semantic_passed,
            "provenance_closure_passed": provenance_closed,
            "negative_guard_results": guard_results,
            "case_passed": case_passed,
        })
        semantic_cases.append({
            "case_id": fixture.case_id,
            "fixture_kind": fixture.fixture_kind,
            "expected_primitive_type": fixture.expected_primitive_type,
            "fixture_vocabulary": fixture.expected_candidate_label,
            "candidate_only": envelope.cognitive_primitive_candidate.candidate_only,
            "fact_status": envelope.cognitive_primitive_candidate.fact_status,
            "candidate_status": envelope.cognitive_primitive_candidate.candidate_status,
            "semantic_label_generated": False,
            "passed": semantic_passed,
        })
        provenance_cases.append({
            "case_id": fixture.case_id,
            "candidate_source_refs_preserved": (
                envelope.cognitive_primitive_candidate.source_refs == fixture.request.evidence_refs
            ),
            "context_refs_preserved": (
                envelope.cognitive_primitive_candidate.context_refs == fixture.request.context_refs
            ),
            "provenance_refs_preserved": (
                tuple(envelope.cognitive_primitive_candidate.provenance.get("source_refs", ()))
                == fixture.request.provenance_refs
            ),
            "source_capability_refs_preserved": (
                tuple(envelope.cognitive_primitive_candidate.provenance.get("source_capability_refs", ()))
                == fixture.request.source_capability_refs
            ),
            "trace_ref_preserved": (
                envelope.cognitive_primitive_candidate.trace_ref == fixture.request.trace_ref
            ),
            "provider_identity_not_candidate_id": (
                envelope.cognitive_primitive_candidate.candidate_id
                not in fixture.request.source_capability_refs
            ),
            "passed": provenance_closed,
        })
        guard_cases.append({
            "case_id": fixture.case_id,
            "guard_results": guard_results,
            "passed": all(guard_results.values()),
        })

    all_cases_passed = all(case["case_passed"] for case in cases)
    flags = _boundary_flags_v1()
    base = {
        "phase": VALIDATION_PHASE_V1,
        "schema_version": VALIDATION_SCHEMA_VERSION_V1,
        "contract_ref": TRANSLATION_LAYER_CONTRACT_ID_V1,
        "validation_flags": flags,
        "case_count": len(cases),
        "case_results": cases,
        "all_cases_passed": all_cases_passed,
        "blocker_count": 0 if all_cases_passed else 1,
        "warning_count": 1,
        "final_candidate_decision": (
            "TRANSLATION_VALIDATION_CLOSURE_EXECUTION_CANDIDATE_PASS_WITH_NOTES"
            if all_cases_passed
            else "TRANSLATION_VALIDATION_CLOSURE_EXECUTION_CANDIDATE_BLOCKED"
        ),
    }
    return {
        "translation_validation_result_v1.json": base,
        "semantic_boundary_result_v1.json": {
            "phase": VALIDATION_PHASE_V1,
            "schema_version": VALIDATION_SCHEMA_VERSION_V1,
            "cases": semantic_cases,
            "passed": all(item["passed"] for item in semantic_cases),
        },
        "provenance_closure_result_v1.json": {
            "phase": VALIDATION_PHASE_V1,
            "schema_version": VALIDATION_SCHEMA_VERSION_V1,
            "cases": provenance_cases,
            "passed": all(item["passed"] for item in provenance_cases),
        },
        "negative_guard_result_v1.json": {
            "phase": VALIDATION_PHASE_V1,
            "schema_version": VALIDATION_SCHEMA_VERSION_V1,
            "required_guard_ids": list(NEGATIVE_GUARD_IDS_V1),
            "cases": guard_cases,
            "passed": all(item["passed"] for item in guard_cases),
        },
    }


def run_cognitive_translation_validation_closure_v1(output_dir: Path) -> Dict[str, Any]:
    """Run two deterministic fixture-isolated passes and write canonical closure evidence."""
    run1 = _build_validation_payloads_v1()
    run2 = _build_validation_payloads_v1()
    deterministic = all(
        canonical_json_v1(run1[name]) == canonical_json_v1(run2[name])
        for name in run1
    )
    run1["deterministic_result_v1.json"] = {
        "phase": VALIDATION_PHASE_V1,
        "schema_version": VALIDATION_SCHEMA_VERSION_V1,
        "run1_equals_run2": deterministic,
        "canonical_json": True,
        "random_id_present": False,
        "timestamp_drift_present": False,
        "environment_path_drift_present": False,
        "passed": deterministic,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename in _JSON_FILENAMES_V1:
        (output_dir / filename).write_text(
            canonical_json_v1(run1[filename]), encoding="utf-8"
        )
    summary = "\n".join((
        "# A3 Translation Layer Validation Closure v1",
        "",
        "- validation_executed: true",
        "- runtime_executed: false",
        "- model_invoked: false",
        "- external_call: false",
        f"- schema_validation: {'PASS' if run1['translation_validation_result_v1.json']['all_cases_passed'] else 'FAIL'}",
        f"- semantic_boundary: {'PASS' if run1['semantic_boundary_result_v1.json']['passed'] else 'FAIL'}",
        f"- provenance_closure: {'PASS' if run1['provenance_closure_result_v1.json']['passed'] else 'FAIL'}",
        f"- negative_guards: {'PASS' if run1['negative_guard_result_v1.json']['passed'] else 'FAIL'}",
        f"- deterministic: {'PASS' if deterministic else 'FAIL'}",
        "- independent_verifier: required; not invoked by this runner",
        "",
    ))
    (output_dir / "validation_summary_v1.md").write_text(summary, encoding="utf-8")
    return run1["translation_validation_result_v1.json"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    print(canonical_json_v1(run_cognitive_translation_validation_closure_v1(Path(args.output_dir))))


if __name__ == "__main__":
    main()

