"""Independent file-based verifier for A3 Translation Layer Controlled DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Tuple

from capabilities.cognitive_flow.cognitive_analysis.translation_layer.cognitive_translation_contract_v1 import (
    NEGATIVE_GUARD_IDS_V1,
)
from capabilities.cognitive_flow.cognitive_analysis.translation_layer.cognitive_translation_types_v1 import (
    CognitivePrimitiveCandidateV1,
    CognitiveTranslationCandidateEnvelopeV1,
    CognitiveTranslationFlagsV1,
    CognitiveTranslationRequestEnvelopeV1,
)
from capabilities.cognitive_flow.cognitive_analysis.translation_layer.cognitive_translation_validator_v1 import (
    validate_cognitive_translation_candidate_envelope_v1,
)

from .cognitive_translation_dryrun_serializer_v1 import (
    TRANSLATION_DRYRUN_RESULT_FILENAME_V1,
    canonical_json_v1,
    write_translation_dryrun_verification_v1,
)
from .cognitive_translation_dryrun_types_v1 import (
    TRANSLATION_DRYRUN_PHASE_V1,
    TRANSLATION_DRYRUN_RUN_ID_V1,
    TRANSLATION_DRYRUN_VERIFIER_ID_V1,
    CognitiveTranslationDryRunVerificationResultV1,
)


_EXPECTED_CASES_V1 = {
    "case_1_ocr_translation": ("ocr", "semantic_candidate", "exit_related_candidate"),
    "case_2_vision_translation": ("vision", "entity_candidate", "human_candidate"),
    "case_3_spatial_translation": ("spatial", "spatial_candidate", "location_related_candidate"),
    "case_4_audio_translation": ("audio", "semantic_candidate", "speaker_related_candidate"),
    "case_5_provenance_trace": ("provenance_trace", "temporal_candidate", "trace_preserving_candidate"),
}


def _request_from_dict_v1(raw: Dict[str, Any]) -> CognitiveTranslationRequestEnvelopeV1:
    return CognitiveTranslationRequestEnvelopeV1(
        translation_request_id=str(raw.get("translation_request_id") or ""),
        evidence_refs=tuple(raw.get("evidence_refs") or ()),
        context_refs=tuple(raw.get("context_refs") or ()),
        provenance_refs=tuple(raw.get("provenance_refs") or ()),
        source_capability_refs=tuple(raw.get("source_capability_refs") or ()),
        requested_primitive_type=str(raw.get("requested_primitive_type") or ""),
        trace_ref=str(raw.get("trace_ref") or ""),
        schema_version=str(raw.get("schema_version") or ""),
    )


def _envelope_from_dict_v1(raw: Dict[str, Any]) -> CognitiveTranslationCandidateEnvelopeV1:
    candidate_raw = dict(raw.get("cognitive_primitive_candidate") or {})
    flags_raw = dict(raw.get("translation_flags") or {})
    candidate = CognitivePrimitiveCandidateV1(
        candidate_id=str(candidate_raw.get("candidate_id") or ""),
        primitive_type=str(candidate_raw.get("primitive_type") or ""),
        source_refs=tuple(candidate_raw.get("source_refs") or ()),
        context_refs=tuple(candidate_raw.get("context_refs") or ()),
        confidence=candidate_raw.get("confidence"),
        uncertainty=dict(candidate_raw.get("uncertainty") or {}),
        provenance=dict(candidate_raw.get("provenance") or {}),
        trace_ref=str(candidate_raw.get("trace_ref") or ""),
        candidate_status=str(candidate_raw.get("candidate_status") or ""),
        candidate_only=candidate_raw.get("candidate_only") is True,
        fact_status=str(candidate_raw.get("fact_status") or ""),
        schema_version=str(candidate_raw.get("schema_version") or ""),
    )
    flags = CognitiveTranslationFlagsV1(
        translation_executed=flags_raw.get("translation_executed") is True,
        simulation_only=flags_raw.get("simulation_only") is True,
        model_invoked=flags_raw.get("model_invoked") is True,
        external_call=flags_raw.get("external_call") is True,
        fact_created=flags_raw.get("fact_created") is True,
        decision_created=flags_raw.get("decision_created") is True,
        action_created=flags_raw.get("action_created") is True,
        state_writeback=flags_raw.get("state_writeback") is True,
        context_mutated=flags_raw.get("context_mutated") is True,
        snapshot_mutated=flags_raw.get("snapshot_mutated") is True,
        memory_updated=flags_raw.get("memory_updated") is True,
        learning_candidate_admitted=flags_raw.get("learning_candidate_admitted") is True,
    )
    return CognitiveTranslationCandidateEnvelopeV1(
        request_ref=str(raw.get("request_ref") or ""),
        cognitive_primitive_candidate=candidate,
        translation_flags=flags,
        negative_guard_refs=tuple(raw.get("negative_guard_refs") or ()),
        schema_version=str(raw.get("schema_version") or ""),
    )


def verify_cognitive_translation_dryrun_v1(
    output_dir: Path,
) -> CognitiveTranslationDryRunVerificationResultV1:
    """Verify serialized output only; never import Runner or call Translation Skeleton."""
    source_path = output_dir / TRANSLATION_DRYRUN_RESULT_FILENAME_V1
    source_present = source_path.is_file()
    raw = source_path.read_text(encoding="utf-8") if source_present else ""
    source = json.loads(raw) if source_present else {}
    checks = [
        source_present,
        raw == canonical_json_v1(source),
        source.get("phase") == TRANSLATION_DRYRUN_PHASE_V1,
        source.get("run_id") == TRANSLATION_DRYRUN_RUN_ID_V1,
        source.get("translation_executed") is False,
        source.get("simulation_only") is True,
        all(source.get(name) is False for name in (
            "model_invoked", "external_call", "fact_created", "decision_created",
            "action_created", "state_writeback", "memory_updated",
        )),
        source.get("deterministic_output") is True,
    ]
    cases = source.get("case_results") if isinstance(source.get("case_results"), list) else []
    checks.append(len(cases) == len(_EXPECTED_CASES_V1))
    guard_checks = []
    observed_case_ids = set()
    for raw_case in cases:
        if not isinstance(raw_case, dict):
            checks.append(False)
            continue
        case_id = str(raw_case.get("case_id") or "")
        observed_case_ids.add(case_id)
        expected = _EXPECTED_CASES_V1.get(case_id)
        request = _request_from_dict_v1(dict(raw_case.get("request") or {}))
        envelope = _envelope_from_dict_v1(dict(raw_case.get("translation_candidate_envelope") or {}))
        validation = validate_cognitive_translation_candidate_envelope_v1(request, envelope)
        case_checks = (
            expected is not None,
            raw_case.get("fixture_kind") == (expected[0] if expected else None),
            raw_case.get("expected_primitive_type") == (expected[1] if expected else None),
            raw_case.get("expected_candidate_label") == (expected[2] if expected else None),
            raw_case.get("semantic_label_generated") is False,
            raw_case.get("case_passed") is True,
            validation.valid,
            envelope.negative_guard_refs == NEGATIVE_GUARD_IDS_V1,
            envelope.cognitive_primitive_candidate.candidate_status == "translation_not_executed",
            envelope.cognitive_primitive_candidate.candidate_id not in request.source_capability_refs,
        )
        checks.extend(case_checks)
        guard_checks.append(all(case_checks[6:]))
    checks.append(observed_case_ids == set(_EXPECTED_CASES_V1))
    checks.append(source.get("all_cases_passed") is True)
    checks.append(source.get("blocker_count") == 0)
    failed_checks = sum(not check for check in checks)
    result = CognitiveTranslationDryRunVerificationResultV1(
        verifier_id=TRANSLATION_DRYRUN_VERIFIER_ID_V1,
        source_result_ref=TRANSLATION_DRYRUN_RESULT_FILENAME_V1,
        passed_checks=len(checks) - failed_checks,
        failed_checks=failed_checks,
        case_count=len(cases),
        negative_guards_passed=bool(guard_checks) and all(guard_checks),
        deterministic_output_ok=source_present and raw == canonical_json_v1(source),
        verifier_invoked_runner=False,
        verifier_invoked_skeleton=False,
        blocker_count=failed_checks,
        warning_count=int(source.get("warning_count", 0)) if source_present else 0,
        final_candidate_decision=(
            "TRANSLATION_DRYRUN_VERIFICATION_CANDIDATE_PASS"
            if failed_checks == 0 else "TRANSLATION_DRYRUN_VERIFICATION_CANDIDATE_BLOCKED"
        ),
    )
    write_translation_dryrun_verification_v1(output_dir, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    print(canonical_json_v1(verify_cognitive_translation_dryrun_v1(Path(args.output_dir))))


if __name__ == "__main__":
    main()
