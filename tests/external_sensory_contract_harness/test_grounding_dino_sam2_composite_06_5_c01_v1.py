"""Synthetic C01 composite contract tests; no real providers or runtime pipeline."""

from __future__ import annotations

import json
from pathlib import Path

from grounding_dino_assertions_06_5_b01_v1 import validate_grounding_dino_native
from sam2_assertions_06_5_b02_v1 import validate_sam2_native
from grounding_dino_sam2_composite_assertions_06_5_c01_v1 import (
    materialize_case,
    validate_composite_case,
    validate_composite_collection,
    _provider_envelopes,
)


COLLECTION = json.loads(Path(__file__).with_name("fixtures_grounding_dino_sam2_composite_06_5_c01_v1.json").read_text(encoding="utf-8"))


def case_for(kind: str) -> dict:
    return materialize_case(COLLECTION, next(case for case in COLLECTION["cases"] if case["case_kind"] == kind))


def test_c01_is_composite_not_model_eight() -> None:
    assert "models" not in COLLECTION
    assert COLLECTION["model_count_increment"] == 0
    assert COLLECTION["provider_contract_snapshot_increment"] == 0
    assert len(COLLECTION["cases"]) == 9
    assert validate_composite_collection(COLLECTION) == ()


def test_normal_handoff_reuses_frozen_provider_native_assertions() -> None:
    case = case_for("NORMAL_HANDOFF")
    grounding, sam2 = _provider_envelopes(case)
    assert validate_grounding_dino_native(grounding) == ()
    assert validate_sam2_native(sam2) == ()
    assert validate_composite_case(case) == ()


def test_full_prompt_provenance_and_mechanical_mapping() -> None:
    case = case_for("NORMAL_HANDOFF")
    assert case["original_text_prompt"]["ref"] == case["grounding"]["prompt_ref"]
    assert case["grounding"]["detections"][0]["detection_ref"] == case["handoff_mapping"]["source_detection_ref"]
    assert case["handoff_mapping"]["derived_prompt_ref"] == case["derived_box_prompt"]["ref"]
    assert case["sam2"]["prompt_ref"] == case["derived_box_prompt"]["ref"]
    assert case["sam2"]["mask_ref"] != case["sam2"]["invocation_ref"]
    assert case["authority"]["handoff_mapping_authority"] == "NONE"


def test_empty_upstream_has_no_downstream_execution() -> None:
    case = case_for("EMPTY_UPSTREAM")
    assert case["grounding"]["detections"] == []
    assert case["derived_box_prompt"] is None
    assert case["sam2"] is None
    assert validate_composite_case(case) == ()


def test_negative_composite_cases_fail_closed() -> None:
    for case_record in COLLECTION["cases"]:
        if case_record["case_kind"] in {"NORMAL_HANDOFF", "EMPTY_UPSTREAM"}:
            continue
        case = materialize_case(COLLECTION, case_record)
        assert validate_composite_case(case) == tuple(case_record["expected_errors"])


def test_provider_scores_and_processing_order_are_non_authoritative() -> None:
    case = case_for("NORMAL_HANDOFF")
    assert case["grounding"]["detections"][0]["provider_score"] != case["sam2"]["provider_quality_score"]
    assert case["authority"]["cross_provider_score_comparison_allowed"] is False
    assert case["authority"]["composite_confidence_created"] is False
    assert case["processing_order"]["creates_currentness"] is False

