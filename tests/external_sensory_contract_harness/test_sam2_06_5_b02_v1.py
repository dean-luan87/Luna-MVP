"""Independent synthetic SAM2 image/mask-propagation contract; no real provider."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from sam2_assertions_06_5_b02_v1 import validate_sam2_native, validate_sam2_snapshots
from validator_v1 import (
    CASE_KINDS,
    NEGATIVE_AUTHORITY_KEYS,
    load_collection,
    materialize_case,
    validate_collection,
    validate_envelope,
    validate_provider_native,
)


COLLECTION = json.loads(Path(__file__).with_name("fixtures_sam2_06_5_b02_v1.json").read_text(encoding="utf-8"))
MODEL = COLLECTION["models"][0]
VIDEO_CASE = "TEMPORAL_OR_ORDER_EDGE_001"


def envelope_for(kind: str) -> dict:
    case = next(item for item in MODEL["cases"] if item["kind"] == kind)
    return materialize_case(COLLECTION, MODEL, case)


def test_sam2_is_model_seven_without_frozen_core_or_grounding_change() -> None:
    frozen = load_collection()
    grounding = json.loads(Path(__file__).with_name("fixtures_grounding_dino_06_5_b01_v1.json").read_text(encoding="utf-8"))
    combined = {"fixture_schema_version": frozen["fixture_schema_version"],
                "models": [*frozen["models"], *grounding["models"], *COLLECTION["models"]]}
    assert (len(frozen["models"]), len(grounding["models"]), len(COLLECTION["models"])) == (5, 1, 1)
    assert len(combined["models"]) == 7
    assert sum(len(model["cases"]) for model in combined["models"]) == 29
    assert sum(len(model["snapshots"]) for model in combined["models"]) == 14
    assert validate_collection(frozen) == ()
    assert validate_collection(grounding) == ()
    assert validate_collection(COLLECTION) == ()
    assert validate_collection(combined) == ()
    assert validate_provider_native(envelope_for("NORMAL_POSITIVE_001")) is None


@pytest.mark.parametrize("kind", [*CASE_KINDS, VIDEO_CASE])
def test_five_synthetic_cases_preserve_universal_and_native_boundaries(kind: str) -> None:
    envelope = envelope_for(kind)
    expected = ("authority_escalation_attempt",) if kind == "AUTHORITY_NEGATIVE_001" else ()
    assert envelope["source_kind"] == "SYNTHETIC"
    assert envelope["simulation"] is True
    assert envelope["provider_model"] == "SAM2"
    assert envelope["contract_requirements"] == {
        "coordinate": "REQUIRED", "temporal": "OPTIONAL", "identity": "OPTIONAL",
        "score": "OPTIONAL", "lineage": "REQUIRED",
    }
    assert validate_envelope(envelope) == expected
    assert validate_sam2_native(envelope) == expected
    assert validate_provider_native(envelope) is None  # Universal validity is not native proof.


def test_image_segmentation_preserves_prompt_mask_basis_and_lineage() -> None:
    envelope = envelope_for("NORMAL_POSITIVE_001")
    native = envelope["native_payload"]
    mask = native["masks"][0]
    relations = envelope["lineage_metadata"]["relations"]
    assert native["mode"] == "IMAGE_SEGMENTATION"
    assert native["prompt"]["type"] == "POINT"
    assert native["prompt"]["coordinate_basis"] == "IMAGE_PIXEL"
    assert envelope["coordinate_metadata"]["basis"] == "IMAGE_PIXEL"
    assert envelope["coordinate_metadata"]["reference_scope"] == native["image_ref"]
    assert mask["representation"] == "BINARY_MASK_DESCRIPTOR"
    assert mask["mask_ref"] and mask["foreground_pixel_count"] > 0
    assert mask["spatial_basis"] == "IMAGE_PIXEL"
    assert mask["reference_scope"] == native["image_ref"]
    assert relations == [
        {"kind": "CONDITIONED_BY", "source_ref": native["prompt_ref"], "subject_ref": envelope["invocation_ref"]},
        {"kind": "PRODUCED_FROM", "source_ref": envelope["invocation_ref"]},
    ]
    assert envelope["relation_declarations"]["CONDITIONED_BY"]["semantic_class"] == "CONDITIONING"
    assert envelope["relation_declarations"]["PRODUCED_FROM"]["semantic_class"] == "DERIVATION"
    assert {item["native_path"] for item in envelope["expected_projection"]["mappings"]} >= {
        "masks[0].mask_ref", "masks[0].representation", "masks[0].provider_quality_score",
    }


def test_video_propagation_has_sequence_local_time_identity_and_no_currentness() -> None:
    envelope = envelope_for(VIDEO_CASE)
    native = envelope["native_payload"]
    mask = native["masks"][0]
    assert native["mode"] == "VIDEO_PROPAGATION"
    assert native["prompt"]["type"] == "PRIOR_MASK_SEED"
    assert native["prompt_ref"] == native["prompt"]["mask_ref"]
    assert native["prompt"]["seed_frame_index"] < native["frame_index"]
    assert mask["frame_index"] == native["frame_index"]
    assert mask["reference_scope"] == native["frame_ref"]
    assert envelope["coordinate_metadata"]["reference_scope"] == native["frame_ref"]
    assert {item["role"]: item["value"] for item in envelope["temporal_metadata"]} == {
        "FRAME_INDEX_OR_ORDER": 1, "TRACKING_PROPAGATION_ORDER": 2,
    }
    assert all(item["creates_currentness"] is False for item in envelope["temporal_metadata"])
    assert {item["scope"] for item in envelope["identity_metadata"]} == {
        "INVOCATION_LOCAL_ID", "SESSION_LOCAL_TRACK_ID", "MEDIA_LOCAL_REGION_ID",
    }
    assert envelope["lineage_metadata"]["relations"] == [
        {"kind": "CONDITIONED_BY", "source_ref": native["prompt_ref"], "subject_ref": envelope["invocation_ref"]},
        {"kind": "PRODUCED_FROM", "source_ref": envelope["invocation_ref"]},
    ]
    assert envelope["expected_projection"]["candidate_only"] is True
    assert envelope["expected_projection"]["admitted"] is False


def test_empty_result_is_no_mask_candidate_not_world_truth_or_provider_failure() -> None:
    envelope = envelope_for("EMPTY_OR_NO_RESULT_001")
    assert envelope["native_payload"]["masks"] == []
    assert envelope["identity_metadata"] == []
    assert envelope["score_metadata"] == []
    assert envelope["expected_projection"]["mappings"] == []
    assert envelope["expected_projection"]["truth_declared"] is False
    assert validate_envelope(envelope) == ()
    assert validate_sam2_native(envelope) == ()


def test_high_provider_quality_and_authority_attempt_remain_non_authoritative() -> None:
    envelope = envelope_for("AUTHORITY_NEGATIVE_001")
    assert envelope["native_payload"]["masks"][0]["provider_quality_score"] == 0.99
    assert envelope["score_metadata"][0]["comparable_with"] == []
    assert envelope["score_metadata"][0]["calibrated"] is False
    assert envelope["expected_projection"]["truth_declared"] is False
    assert envelope["expected_projection"]["admitted"] is False
    assert envelope["lineage_metadata"]["creates_authority"] is False
    assert "authority_escalation_attempt" in validate_envelope(envelope)
    assert "authority_escalation_attempt" in validate_sam2_native(envelope)
    for key in NEGATIVE_AUTHORITY_KEYS:
        altered = envelope_for("NORMAL_POSITIVE_001")
        altered["expected_governance"][key] = True
        assert "governance_boundary_invalid" in validate_envelope(altered)
    for forbidden in ("luna_canonical_id", "world_truth_declared", "authority_granted", "currentness_granted"):
        altered = envelope_for("NORMAL_POSITIVE_001")
        altered["native_payload"][forbidden] = True
        assert "sam2_native_authority_claim_invalid" in validate_sam2_native(altered)


def test_baseline_and_simulated_variant_coexist_without_official_version_claim() -> None:
    assert validate_sam2_snapshots(MODEL) == ()
    old, variant = MODEL["snapshots"]["v1"], MODEL["snapshots"]["variant"]
    assert MODEL["snapshot_classification"] == {"v1": "SYNTHETIC_BASELINE", "variant": "SIMULATED_CONTRACT_VARIANT"}
    for key in ("model_contract_ref", "provider_model_revision", "provider_interface_version",
                "native_contract_version", "adapter_contract_version"):
        assert old[key] != variant[key]
    assert all(str(item[key]).startswith("synthetic-") for item in (old, variant)
               for key in ("provider_model_revision", "provider_interface_version",
                           "native_contract_version", "adapter_contract_version"))
    assert envelope_for("NORMAL_POSITIVE_001")["model_contract_ref"] == old["model_contract_ref"]
    assert envelope_for("VERSION_VARIANT_001")["model_contract_ref"] == variant["model_contract_ref"]
    altered = deepcopy(MODEL)
    altered["snapshots"]["variant"]["native_contract_version"] = old["native_contract_version"]
    assert "sam2_snapshot_dimension_invalid:native_contract_version" in validate_sam2_snapshots(altered)


@pytest.mark.parametrize("mutation,expected_error", [
    ("prompt", "sam2_point_prompt_invalid"),
    ("prompt_ref", "sam2_prompt_or_invocation_invalid"),
    ("invocation", "sam2_prompt_or_invocation_invalid"),
    ("masks", "sam2_masks_invalid"),
    ("mask_representation", "sam2_mask_representation_invalid"),
    ("mask_basis", "sam2_mask_representation_invalid"),
    ("mask_size", "sam2_mask_representation_invalid"),
    ("mask_score", "sam2_mask_score_invalid"),
    ("coordinate", "sam2_coordinate_contract_invalid"),
    ("score_domain", "sam2_score_contract_invalid"),
    ("prompt_lineage", "sam2_prompt_condition_invalid"),
    ("candidate_lineage", "sam2_mask_formation_invalid"),
    ("canonical_identity", "sam2_identity_scope_invalid"),
])
def test_malformed_image_native_contract_fails_closed(mutation: str, expected_error: str) -> None:
    envelope = envelope_for("NORMAL_POSITIVE_001")
    native = envelope["native_payload"]
    mask = native["masks"][0]
    if mutation == "prompt":
        native["prompt"]["coordinates_xy"] = [99, 4]
    elif mutation == "prompt_ref":
        native["prompt_ref"] = "synthetic:unlisted"
    elif mutation == "invocation":
        native["invocation_ref"] = "synthetic:wrong-invocation"
    elif mutation == "masks":
        native["masks"] = None
    elif mutation == "mask_representation":
        mask["representation"] = "BOX_ONLY"
    elif mutation == "mask_basis":
        mask["spatial_basis"] = "SLAM_MAP_FRAME"
    elif mutation == "mask_size":
        mask["foreground_pixel_count"] = 65
    elif mutation == "mask_score":
        mask["provider_quality_score"] = 1.2
    elif mutation == "coordinate":
        envelope["coordinate_metadata"]["basis"] = "IMAGE_NORMALIZED"
    elif mutation == "score_domain":
        envelope["score_metadata"][0]["score_domain"] = "GLOBAL_UNTYPED_CONFIDENCE"
    elif mutation == "prompt_lineage":
        envelope["lineage_metadata"]["relations"][0]["source_ref"] = native["image_ref"]
    elif mutation == "candidate_lineage":
        envelope["lineage_metadata"]["relations"][1]["source_ref"] = native["image_ref"]
    elif mutation == "canonical_identity":
        envelope["identity_metadata"][0]["scope"] = "LUNA_CANONICAL_ID"
    assert expected_error in validate_sam2_native(envelope)


@pytest.mark.parametrize("mutation", ["frame", "order", "seed", "sequence_local_id", "currentness"])
def test_malformed_video_propagation_fails_closed(mutation: str) -> None:
    envelope = envelope_for(VIDEO_CASE)
    native = envelope["native_payload"]
    if mutation == "frame":
        native["masks"][0]["frame_index"] = 2
    elif mutation == "order":
        envelope["temporal_metadata"][1]["value"] = 99
    elif mutation == "seed":
        native["prompt"]["seed_frame_index"] = 2
    elif mutation == "sequence_local_id":
        native["masks"][0]["object_index"] = "canonical-object-1"
    elif mutation == "currentness":
        envelope["temporal_metadata"][0]["creates_currentness"] = True
    errors = validate_sam2_native(envelope)
    assert "sam2_propagation_order_invalid" in errors or "sam2_sequence_local_identity_invalid" in errors


def test_no_real_golden_cross_model_input_or_composite_claim() -> None:
    assert len(MODEL["cases"]) == 5
    assert {case["kind"] for case in MODEL["cases"]} == {*CASE_KINDS, VIDEO_CASE}
    assert len({case["kind"] for case in MODEL["cases"]}) == len(MODEL["cases"])
    for case in MODEL["cases"]:
        envelope = materialize_case(COLLECTION, MODEL, case)
        assert envelope["source_kind"] == "SYNTHETIC"
        assert envelope["simulation"] is True
        assert all("grounding" not in ref.lower() for ref in envelope["input_refs"])
        assert all("grounding" not in str(relation).lower() for relation in envelope["lineage_metadata"]["relations"])
