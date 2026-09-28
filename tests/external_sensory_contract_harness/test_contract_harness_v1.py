"""Contract-only checks; no provider, Gateway, or runtime invocation."""

from __future__ import annotations

from copy import deepcopy

import pytest

from validator_v1 import (
    CASE_KINDS,
    NEGATIVE_AUTHORITY_KEYS,
    executable_cases,
    load_collection,
    materialize_case,
    validate_collection,
    validate_envelope,
)


COLLECTION = load_collection()


def envelope_for(model_key: str, kind: str) -> dict:
    model = next(item for item in COLLECTION["models"] if item["model_key"] == model_key)
    case = next(item for item in model["cases"] if item["kind"] == kind)
    return materialize_case(COLLECTION, model, case)


def test_five_models_and_twenty_cases_load_with_expected_partitions() -> None:
    assert len(COLLECTION["models"]) == 5
    assert sum(len(model["cases"]) for model in COLLECTION["models"]) == 20
    assert all({case["kind"] for case in model["cases"]} == set(CASE_KINDS) for model in COLLECTION["models"])
    assert validate_collection(COLLECTION) == ()


def test_stored_cases_have_unique_materialized_synthetic_identities() -> None:
    cases = executable_cases(COLLECTION)
    assert len(COLLECTION["models"]) == 5
    assert len(cases) >= 20
    assert len({case["case_id"] for case in cases}) == len(cases)
    assert all(case["source_kind"] == "SYNTHETIC" and case["simulation"] is True for case in cases)
    model_keys = {model["model_key"] for model in COLLECTION["models"]}
    assert all(case["case_id"].split(":", 1)[0] in model_keys for case in cases)
    assert all(case["case_id"].split(":", 1)[1] in CASE_KINDS for case in cases)
    assert all(case["model_contract_ref"] and case["native_contract_version"] and case["adapter_contract_version"] for case in cases)
    assert all(case["provider_model_revision"].startswith("synthetic-") for case in cases)


@pytest.mark.parametrize("model_key", [model["model_key"] for model in COLLECTION["models"]])
@pytest.mark.parametrize("kind", CASE_KINDS)
def test_each_model_case_is_accepted_or_rejected_as_declared(model_key: str, kind: str) -> None:
    envelope = envelope_for(model_key, kind)
    assert envelope["source_kind"] == "SYNTHETIC"
    assert envelope["simulation"] is True
    assert isinstance(envelope["native_payload"], dict)
    assert validate_envelope(envelope) == (("authority_escalation_attempt",) if kind == "AUTHORITY_NEGATIVE_001" else ())


def test_version_dimensions_coexist_without_overwriting_v1() -> None:
    for model in COLLECTION["models"]:
        old, variant = model["snapshots"]["v1"], model["snapshots"]["variant"]
        assert model["snapshot_classification"] == {
            "v1": "SYNTHETIC_BASELINE",
            "variant": "SIMULATED_CONTRACT_VARIANT",
        }
        for key in ("model_contract_ref", "provider_model_revision", "native_contract_version", "adapter_contract_version"):
            assert old[key] != variant[key]
        assert old["provider_model_revision"].startswith("synthetic-")
        assert variant["provider_model_revision"].startswith("synthetic-")
        assert envelope_for(model["model_key"], "NORMAL_POSITIVE_001")["model_contract_ref"] == old["model_contract_ref"]
        assert envelope_for(model["model_key"], "VERSION_VARIANT_001")["model_contract_ref"] == variant["model_contract_ref"]
    altered = deepcopy(COLLECTION)
    altered["models"][0]["snapshots"]["variant"]["native_contract_version"] = altered["models"][0]["snapshots"]["v1"]["native_contract_version"]
    assert any(error.startswith("historical_version_overwrite") for error in validate_collection(altered))
    altered = deepcopy(COLLECTION)
    altered["models"][0]["snapshot_classification"]["variant"] = "OFFICIAL_MODEL_REVISION"
    assert any(error.startswith("simulated_variant_disguise") for error in validate_collection(altered))


def test_yolo_two_native_detections_remain_individually_traceable() -> None:
    envelope = envelope_for("yolo26", "NORMAL_POSITIVE_001")
    native = envelope["native_payload"]["detections"]
    mappings = envelope["expected_projection"]["mappings"]
    assert len(native) == 2
    for index in range(2):
        for field in ("bbox_xyxy", "class_id", "confidence", "detection_id"):
            assert any(mapping["native_path"] == f"detections[{index}].{field}" for mapping in mappings)
    assert validate_envelope(envelope) == ()
    envelope["native_payload"]["detections"][1]["confidence"] = 0.01
    assert "projection_value_mismatch" in validate_envelope(envelope)


def test_scores_are_typed_not_globally_comparable_or_epistemic() -> None:
    yolo = envelope_for("yolo26", "NORMAL_POSITIVE_001")
    relation = envelope_for("relateanything", "NORMAL_POSITIVE_001")
    assert yolo["score_metadata"][0]["score_domain"] != relation["score_metadata"][0]["score_domain"]
    assert yolo["score_metadata"][0]["comparable_with"] == relation["score_metadata"][0]["comparable_with"] == []
    yolo["score_metadata"] = 0.91
    assert "score_metadata_invalid" in validate_envelope(yolo)
    relation["score_metadata"][0]["comparable_with"] = ["YOLO26_SYNTHETIC_DETECTION_V1"]
    assert "score_semantics_invalid" in validate_envelope(relation)


def test_provider_local_identity_cannot_be_luna_canonical_identity() -> None:
    envelope = envelope_for("yolo26", "NORMAL_POSITIVE_001")
    envelope["identity_metadata"][0]["scope"] = "LUNA_CANONICAL_ID"
    assert "identity_scope_invalid" in validate_envelope(envelope)
    envelope = envelope_for("relateanything", "NORMAL_POSITIVE_001")
    envelope["expected_projection"]["canonical_id"] = "synthetic:object:3"
    assert "projection_authority_invalid" in validate_envelope(envelope)


def test_temporal_roles_never_create_currentness_or_source_clock_authority() -> None:
    asr = envelope_for("qwen3_asr", "NORMAL_POSITIVE_001")
    assert any(item["role"] == "MEDIA_RELATIVE_TIME" for item in asr["temporal_metadata"])
    assert all(item["creates_currentness"] is False for item in asr["temporal_metadata"])
    asr["temporal_metadata"][0]["creates_currentness"] = True
    assert "temporal_role_invalid" in validate_envelope(asr)
    slam = envelope_for("orb_slam3", "NORMAL_POSITIVE_001")
    assert all(item["creates_currentness"] is False for item in slam["temporal_metadata"])


def test_coordinate_basis_is_explicit_and_monocular_pose_is_not_metric() -> None:
    yolo = envelope_for("yolo26", "NORMAL_POSITIVE_001")
    assert yolo["coordinate_metadata"]["basis"] == "IMAGE_PIXEL"
    yolo["coordinate_metadata"] = None
    assert "coordinate_basis_invalid" in validate_envelope(yolo)
    slam = envelope_for("orb_slam3", "NORMAL_POSITIVE_001")
    assert slam["coordinate_metadata"]["basis"] == "SLAM_MAP_FRAME"
    assert slam["coordinate_metadata"]["metric_scale_proven"] is False
    slam["coordinate_metadata"]["reference_scope"] = None
    assert "coordinate_basis_invalid" in validate_envelope(slam)


def test_lineage_and_relation_edges_cannot_create_authority() -> None:
    envelope = envelope_for("relateanything", "NORMAL_POSITIVE_001")
    assert envelope["lineage_metadata"]["creates_authority"] is False
    envelope["lineage_metadata"]["creates_authority"] = True
    assert "lineage_boundary_invalid" in validate_envelope(envelope)


@pytest.mark.parametrize("key", NEGATIVE_AUTHORITY_KEYS)
def test_all_governance_authority_escalations_fail(key: str) -> None:
    envelope = envelope_for("qwen3_vl", "NORMAL_POSITIVE_001")
    envelope["expected_governance"][key] = True
    assert "governance_boundary_invalid" in validate_envelope(envelope)


def test_provider_native_authority_claim_and_projection_admission_fail() -> None:
    envelope = envelope_for("qwen3_vl", "NORMAL_POSITIVE_001")
    envelope["native_payload"]["world_truth_declared"] = True
    assert "native_authority_claim_invalid" in validate_envelope(envelope)
    envelope = envelope_for("qwen3_vl", "NORMAL_POSITIVE_001")
    envelope["expected_projection"]["admitted"] = True
    assert "projection_authority_invalid" in validate_envelope(envelope)


def test_real_golden_source_kind_is_representable_without_golden_payload() -> None:
    envelope = envelope_for("yolo26", "NORMAL_POSITIVE_001")
    envelope["source_kind"] = "REAL_GOLDEN"
    envelope["simulation"] = False
    assert validate_envelope(envelope) == ()


def test_native_version_config_and_lineage_are_separate_from_admission() -> None:
    vl = envelope_for("qwen3_vl", "VERSION_VARIANT_001")
    assert vl["configuration_snapshot"]["processor_ref"] == vl["native_payload"]["processor_ref"]
    assert vl["configuration_snapshot"]["template_ref"] == vl["native_payload"]["template_ref"]
    assert vl["expected_projection"]["candidate_only"] is True
    assert vl["expected_projection"]["admitted"] is False
    assert vl["lineage_metadata"]["creates_authority"] is False
