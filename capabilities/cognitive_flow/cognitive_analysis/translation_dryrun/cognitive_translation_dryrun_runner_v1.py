"""Fixture-only runner for A3 Translation Layer Controlled DryRun v1."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Tuple

from capabilities.cognitive_flow.cognitive_analysis.translation_layer.cognitive_translation_skeleton_v1 import (
    CognitiveTranslationSkeletonV1,
)
from capabilities.cognitive_flow.cognitive_analysis.translation_layer.cognitive_translation_types_v1 import (
    CognitiveTranslationRequestEnvelopeV1,
)
from capabilities.cognitive_flow.cognitive_analysis.translation_layer.cognitive_translation_validator_v1 import (
    validate_cognitive_translation_candidate_envelope_v1,
)

from .cognitive_translation_dryrun_serializer_v1 import (
    canonical_json_v1,
    write_translation_dryrun_result_v1,
)
from .cognitive_translation_dryrun_types_v1 import (
    TRANSLATION_DRYRUN_PHASE_V1,
    TRANSLATION_DRYRUN_RUN_ID_V1,
    CognitiveTranslationDryRunCaseResultV1,
    CognitiveTranslationDryRunFixtureCaseV1,
    CognitiveTranslationDryRunRunResultV1,
)


def _fixture_request_v1(
    *,
    case_id: str,
    primitive_type: str,
    evidence_ref: str,
    source_capability_ref: str,
) -> CognitiveTranslationRequestEnvelopeV1:
    return CognitiveTranslationRequestEnvelopeV1(
        translation_request_id=f"a3-translation-dryrun:{case_id}:v1",
        evidence_refs=(evidence_ref,),
        context_refs=("current_cognitive_context:fixture:translation-dryrun:v1",),
        provenance_refs=(f"provenance:fixture:{case_id}:v1",),
        source_capability_refs=(source_capability_ref,),
        requested_primitive_type=primitive_type,
        trace_ref=f"trace:a3-translation-dryrun:{case_id}:v1",
    )


def build_translation_dryrun_fixture_cases_v1() -> Tuple[CognitiveTranslationDryRunFixtureCaseV1, ...]:
    """Build the five immutable reference-only cases; no external Evidence is read."""
    return (
        CognitiveTranslationDryRunFixtureCaseV1(
            case_id="case_1_ocr_translation",
            fixture_kind="ocr",
            input_candidate_label="text_candidate:出口",
            expected_primitive_type="semantic_candidate",
            expected_candidate_label="exit_related_candidate",
            forbidden_claims=("fact:这里存在出口", "decision:用户应该向右走"),
            request=_fixture_request_v1(
                case_id="case_1_ocr_translation",
                primitive_type="semantic_candidate",
                evidence_ref="evidence:fixture:ocr:text-candidate:exit:v1",
                source_capability_ref="capability:fixture:ocr-provider:v1",
            ),
        ),
        CognitiveTranslationDryRunFixtureCaseV1(
            case_id="case_2_vision_translation",
            fixture_kind="vision",
            input_candidate_label="object_candidate:person",
            expected_primitive_type="entity_candidate",
            expected_candidate_label="human_candidate",
            forbidden_claims=("confirmed_person", "identity_inference"),
            request=_fixture_request_v1(
                case_id="case_2_vision_translation",
                primitive_type="entity_candidate",
                evidence_ref="evidence:fixture:vision:object-candidate:person:v1",
                source_capability_ref="capability:fixture:vision-provider:v1",
            ),
        ),
        CognitiveTranslationDryRunFixtureCaseV1(
            case_id="case_3_spatial_translation",
            fixture_kind="spatial",
            input_candidate_label="location_reference:indoor-zone-a",
            expected_primitive_type="spatial_candidate",
            expected_candidate_label="location_related_candidate",
            forbidden_claims=("navigation_decision", "route_action"),
            request=_fixture_request_v1(
                case_id="case_3_spatial_translation",
                primitive_type="spatial_candidate",
                evidence_ref="evidence:fixture:slam:location-reference:zone-a:v1",
                source_capability_ref="capability:fixture:slam-provider:v1",
            ),
        ),
        CognitiveTranslationDryRunFixtureCaseV1(
            case_id="case_4_audio_translation",
            fixture_kind="audio",
            input_candidate_label="speaker_candidate:unknown-speaker",
            expected_primitive_type="semantic_candidate",
            expected_candidate_label="speaker_related_candidate",
            forbidden_claims=("identity_confirmation", "relationship_judgment"),
            request=_fixture_request_v1(
                case_id="case_4_audio_translation",
                primitive_type="semantic_candidate",
                evidence_ref="evidence:fixture:audio:speaker-candidate:v1",
                source_capability_ref="capability:fixture:audio-provider:v1",
            ),
        ),
        CognitiveTranslationDryRunFixtureCaseV1(
            case_id="case_5_provenance_trace",
            fixture_kind="provenance_trace",
            input_candidate_label="evidence_reference:trace-required",
            expected_primitive_type="temporal_candidate",
            expected_candidate_label="trace_preserving_candidate",
            forbidden_claims=("missing_source_ref", "hidden_model_source"),
            request=_fixture_request_v1(
                case_id="case_5_provenance_trace",
                primitive_type="temporal_candidate",
                evidence_ref="evidence:fixture:provenance:trace-required:v1",
                source_capability_ref="capability:fixture:external-provider:v1",
            ),
        ),
    )


def run_cognitive_translation_dryrun_v1(
    output_dir: Path,
) -> CognitiveTranslationDryRunRunResultV1:
    """Call only the non-executing Skeleton against fixed fixtures and serialize the result."""
    skeleton = CognitiveTranslationSkeletonV1()
    case_results = []
    for fixture in build_translation_dryrun_fixture_cases_v1():
        envelope = skeleton.translate(fixture.request)
        validation = validate_cognitive_translation_candidate_envelope_v1(
            fixture.request, envelope
        )
        case_passed = (
            validation.valid
            and envelope.cognitive_primitive_candidate.primitive_type
            == fixture.expected_primitive_type
            and envelope.cognitive_primitive_candidate.candidate_status
            == "translation_not_executed"
        )
        case_results.append(CognitiveTranslationDryRunCaseResultV1(
            case_id=fixture.case_id,
            fixture_kind=fixture.fixture_kind,
            input_candidate_label=fixture.input_candidate_label,
            expected_primitive_type=fixture.expected_primitive_type,
            expected_candidate_label=fixture.expected_candidate_label,
            forbidden_claims=fixture.forbidden_claims,
            semantic_label_generated=False,
            request=fixture.request,
            translation_candidate_envelope=envelope,
            case_passed=case_passed,
        ))
    all_cases_passed = all(item.case_passed for item in case_results)
    result = CognitiveTranslationDryRunRunResultV1(
        phase=TRANSLATION_DRYRUN_PHASE_V1,
        run_id=TRANSLATION_DRYRUN_RUN_ID_V1,
        case_results=tuple(case_results),
        translation_executed=False,
        simulation_only=True,
        model_invoked=False,
        external_call=False,
        fact_created=False,
        decision_created=False,
        action_created=False,
        state_writeback=False,
        memory_updated=False,
        all_cases_passed=all_cases_passed,
        deterministic_output=True,
        blocker_count=0 if all_cases_passed else 1,
        warning_count=1,
        final_candidate_decision=(
            "TRANSLATION_DRYRUN_READY_WITH_NOTES"
            if all_cases_passed else "TRANSLATION_DRYRUN_BLOCKED"
        ),
    )
    write_translation_dryrun_result_v1(output_dir, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    print(canonical_json_v1(run_cognitive_translation_dryrun_v1(Path(args.output_dir))))


if __name__ == "__main__":
    main()
