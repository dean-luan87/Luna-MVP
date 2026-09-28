"""Contract-only checks; no provider, Gateway, or runtime invocation."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json

import pytest

from validator_v1 import (
    CASE_KINDS,
    NEGATIVE_AUTHORITY_KEYS,
    executable_cases,
    load_collection,
    materialize_case,
    validate_collection,
    validate_envelope,
    validate_provider_native,
)


COLLECTION = load_collection()
HISTORICAL_MODEL_DIGESTS = {
    "yolo26": "7efdb492b97351f06fbc67468ae931450f3ac3d2ebd45884dd1cce55e5a9b0ab",
    "qwen3_vl": "6d2d974f3019b7262ad3df08e22a07214ac94867845be1c2fb2c329cb20dac4f",
    "qwen3_asr": "fdf659c33e08d0f2e569d14f3c850f96f3cc508c9e6c1998d64667c3b01d3b2b",
    "orb_slam3": "1aa8b545097f1fd60e8dfc98c3b1cf544c60ee6eb1c2352aee4032f4c06c4138",
    "relateanything": "f94e5f8d8ce9eb49996bbe4ca330a375eee7f0425400e8d10e79f51533754ed3",
}


def envelope_for(model_key: str, kind: str) -> dict:
    model = next(item for item in COLLECTION["models"] if item["model_key"] == model_key)
    case = next(item for item in model["cases"] if item["kind"] == kind)
    return materialize_case(COLLECTION, model, case)


def future_provider_probe() -> dict:
    """GENERALIZATION_PROBE_ONLY: in-memory, never a model fixture record."""
    model = deepcopy(next(item for item in COLLECTION["models"] if item["model_key"] == "qwen3_vl"))
    model["model_key"] = "future_provider_probe"
    for snapshot_name, snapshot in model["snapshots"].items():
        snapshot.update({
            "model_contract_ref": f"test-contract:anonymous-probe:{snapshot_name}",
            "provider_family": "synthetic_probe",
            "provider_model": "Anonymous Future Provider Probe",
            "provider_model_revision": f"synthetic-probe-revision-{snapshot_name}",
        })
    model["configuration_snapshot"] = {}
    model["input_refs"] = ["synthetic:probe:input"]
    model["lineage_metadata"] = {
        "relations": [{"kind": "PRODUCED_FROM", "source_ref": "synthetic:probe:input"}],
        "creates_authority": False,
    }
    for case in model["cases"]:
        case["native_payload"] = {"opaque_result": None if case["kind"] == "EMPTY_OR_NO_RESULT_001" else "probe"}
        case["expected_projection"] = {
            "candidate_only": True, "truth_declared": False, "admitted": False,
            "candidate_kind": "opaque_candidate", "mappings": [],
        }
        case.pop("configuration_snapshot", None)
    return model


def test_frozen_five_models_twenty_cases_and_ten_snapshots_remain_intact() -> None:
    historical = [model for model in COLLECTION["models"] if model["model_key"] in HISTORICAL_MODEL_DIGESTS]
    assert len(historical) == len(HISTORICAL_MODEL_DIGESTS) == 5
    assert sum(len(model["cases"]) for model in historical) == 20
    assert sum(len(model["snapshots"]) for model in historical) == 10
    assert all({case["kind"] for case in model["cases"]} == set(CASE_KINDS) for model in historical)
    for model in historical:
        original = {key: value for key, value in model.items() if key != "contract_requirements"}
        encoded = json.dumps(original, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        assert hashlib.sha256(encoded.encode("utf-8")).hexdigest() == HISTORICAL_MODEL_DIGESTS[model["model_key"]]
    assert validate_collection(COLLECTION) == ()


def test_stored_cases_have_unique_materialized_synthetic_identities() -> None:
    cases = executable_cases(COLLECTION)
    assert len(COLLECTION["models"]) >= 5
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
    assert validate_provider_native(envelope) == ()


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


def test_sixth_anonymous_provider_passes_universal_but_not_native_proof() -> None:
    expanded = deepcopy(COLLECTION)
    probe = future_provider_probe()
    expanded["models"].append(probe)
    assert validate_collection(expanded) == ()
    assert len(expanded["models"]) == 6
    for case in probe["cases"]:
        envelope = materialize_case(expanded, probe, case)
        assert validate_envelope(envelope) == (("authority_escalation_attempt",) if case["kind"] == "AUTHORITY_NEGATIVE_001" else ())
        assert validate_provider_native(envelope) is None


def test_duplicate_model_and_fixture_identity_still_fail() -> None:
    duplicated = deepcopy(COLLECTION)
    duplicated["models"].append(deepcopy(duplicated["models"][0]))
    assert "duplicate_model_key" in validate_collection(duplicated)
    assert any(error.startswith("duplicate_case_id:") for error in validate_collection(duplicated))
    duplicated = deepcopy(COLLECTION)
    duplicated["models"][0]["cases"].append(deepcopy(duplicated["models"][0]["cases"][0]))
    assert any(error.startswith("duplicate_case_id:") for error in validate_collection(duplicated))


def test_declared_coordinate_applicability_is_bounded_and_enforced() -> None:
    required = envelope_for("yolo26", "NORMAL_POSITIVE_001")
    required["coordinate_metadata"] = None
    assert "coordinate_required_missing" in validate_envelope(required)
    assert "coordinate_basis_invalid" in validate_envelope(required)
    optional = envelope_for("yolo26", "NORMAL_POSITIVE_001")
    optional["contract_requirements"]["coordinate"] = "OPTIONAL"
    optional["coordinate_metadata"] = {"basis": "NOT_A_BASIS"}
    assert "coordinate_basis_invalid" in validate_envelope(optional)
    not_applicable = envelope_for("qwen3_vl", "NORMAL_POSITIVE_001")
    assert not_applicable["contract_requirements"]["coordinate"] == "NOT_APPLICABLE"
    assert not_applicable["coordinate_metadata"] is None
    assert validate_envelope(not_applicable) == ()
    not_applicable["coordinate_metadata"] = {"basis": "IMAGE_PIXEL", "reference_scope": "synthetic:image:desk-001"}
    assert "coordinate_not_applicable_conflict" in validate_envelope(not_applicable)
    malformed = envelope_for("yolo26", "NORMAL_POSITIVE_001")
    malformed["contract_requirements"]["coordinate"] = "IGNORE"
    assert "contract_requirements_invalid" in validate_envelope(malformed)


@pytest.mark.parametrize("kind", ["temporal", "identity", "score", "lineage"])
def test_declared_noncoordinate_requirements_are_enforced(kind: str) -> None:
    envelope = envelope_for("yolo26", "NORMAL_POSITIVE_001")
    envelope["contract_requirements"][kind] = "REQUIRED"
    envelope[f"{kind}_metadata"] = None
    assert f"{kind}_required_missing" in validate_envelope(envelope)


@pytest.mark.parametrize("model_key,expected_error", [
    ("yolo26", "detection_basis_invalid"),
    ("orb_slam3", "slam_frame_or_scale_invalid"),
])
def test_false_declaration_cannot_bypass_frozen_native_coordinate_contract(model_key: str, expected_error: str) -> None:
    envelope = envelope_for(model_key, "NORMAL_POSITIVE_001")
    envelope["contract_requirements"]["coordinate"] = "NOT_APPLICABLE"
    envelope["coordinate_metadata"] = None
    assert expected_error in validate_provider_native(envelope)
    altered = deepcopy(COLLECTION)
    model = next(item for item in altered["models"] if item["model_key"] == model_key)
    model["contract_requirements"]["coordinate"] = "NOT_APPLICABLE"
    model["coordinate_metadata"] = None
    assert any(expected_error in error for error in validate_collection(altered))


@pytest.mark.parametrize("model_key,mutation,expected_error", [
    ("yolo26", "detections", "detection_basis_invalid"),
    ("qwen3_vl", "messages", "generated_payload_shape_invalid"),
    ("qwen3_asr", "segments", "asr_media_time_invalid"),
    ("orb_slam3", "coordinate_frame", "slam_frame_or_scale_invalid"),
    ("relateanything", "predicate_vocabulary_version", "relation_vocabulary_invalid"),
])
def test_frozen_provider_native_assertions_remain_active(model_key: str, mutation: str, expected_error: str) -> None:
    envelope = envelope_for(model_key, "NORMAL_POSITIVE_001")
    envelope["native_payload"].pop(mutation)
    assert expected_error in validate_provider_native(envelope)


def test_synthetic_and_golden_source_boundaries_remain_distinct() -> None:
    envelope = envelope_for("yolo26", "NORMAL_POSITIVE_001")
    envelope["simulation"] = False
    assert "synthetic_must_be_simulation" in validate_envelope(envelope)
    envelope["source_kind"] = "REAL_GOLDEN"
    envelope["simulation"] = True
    assert "golden_must_not_be_simulation" in validate_envelope(envelope)
