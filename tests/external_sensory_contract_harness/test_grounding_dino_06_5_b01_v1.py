"""Independent synthetic Grounding DINO contract; no real model or runtime invocation."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from grounding_dino_assertions_06_5_b01_v1 import (
    validate_grounding_dino_native,
    validate_grounding_dino_snapshots,
)
from validator_v1 import (
    CASE_KINDS,
    NEGATIVE_AUTHORITY_KEYS,
    load_collection,
    materialize_case,
    validate_collection,
    validate_envelope,
    validate_provider_native,
)


COLLECTION = json.loads(Path(__file__).with_name("fixtures_grounding_dino_06_5_b01_v1.json").read_text(encoding="utf-8"))
MODEL = COLLECTION["models"][0]


def envelope_for(kind: str) -> dict:
    case = next(item for item in MODEL["cases"] if item["kind"] == kind)
    return materialize_case(COLLECTION, MODEL, case)


def test_grounding_dino_is_model_six_without_frozen_core_change() -> None:
    frozen = load_collection()
    combined = {"fixture_schema_version": frozen["fixture_schema_version"], "models": [*frozen["models"], *COLLECTION["models"]]}
    assert len(frozen["models"]) == 5
    assert len(COLLECTION["models"]) == 1
    assert len(combined["models"]) == 6
    assert sum(len(model["cases"]) for model in combined["models"]) == 24
    assert sum(len(model["snapshots"]) for model in combined["models"]) == 12
    assert validate_collection(frozen) == ()
    assert validate_collection(COLLECTION) == ()
    assert validate_collection(combined) == ()
    assert validate_provider_native(envelope_for("NORMAL_POSITIVE_001")) is None


@pytest.mark.parametrize("kind", CASE_KINDS)
def test_four_synthetic_cases_preserve_universal_and_native_boundaries(kind: str) -> None:
    envelope = envelope_for(kind)
    expected = ("authority_escalation_attempt",) if kind == "AUTHORITY_NEGATIVE_001" else ()
    assert envelope["source_kind"] == "SYNTHETIC"
    assert envelope["simulation"] is True
    assert envelope["provider_model"] == "Grounding DINO"
    assert envelope["contract_requirements"]["coordinate"] == "REQUIRED"
    assert envelope["contract_requirements"]["score"] == "REQUIRED"
    assert envelope["contract_requirements"]["lineage"] == "REQUIRED"
    assert envelope["contract_requirements"]["temporal"] == "OPTIONAL"
    assert envelope["contract_requirements"]["identity"] == "OPTIONAL"
    assert validate_envelope(envelope) == expected
    assert validate_grounding_dino_native(envelope) == expected
    assert validate_provider_native(envelope) is None  # Central native proof is not auto-granted.


def test_prompt_condition_and_candidate_invocation_lineage_are_distinct() -> None:
    for kind in CASE_KINDS:
        envelope = envelope_for(kind)
        native = envelope["native_payload"]
        relations = envelope["lineage_metadata"]["relations"]
        conditioned = [relation for relation in relations if relation["kind"] == "CONDITIONED_BY"]
        produced = [relation for relation in relations if relation["kind"] == "PRODUCED_FROM"]
        assert native["prompt_ref"] in envelope["input_refs"]
        assert native["image_ref"] in envelope["input_refs"]
        assert native["caption"] == "red cup on a table"
        assert len(conditioned) == 1
        assert conditioned[0]["source_ref"] == native["prompt_ref"]
        assert conditioned[0]["subject_ref"] == envelope["invocation_ref"]
        assert envelope["relation_declarations"]["CONDITIONED_BY"]["semantic_class"] == "CONDITIONING"
        assert envelope["relation_declarations"]["PRODUCED_FROM"]["semantic_class"] == "DERIVATION"
        if native["detections"]:
            assert len(produced) == 1
            assert produced[0]["source_ref"] == envelope["invocation_ref"]
            assert produced[0]["source_ref"] != native["prompt_ref"]
        else:
            assert produced == []  # No detection candidate exists to be produced.


def test_normalized_box_score_phrase_and_local_indexes_remain_traceable() -> None:
    envelope = envelope_for("NORMAL_POSITIVE_001")
    detection = envelope["native_payload"]["detections"][0]
    assert envelope["coordinate_metadata"]["basis"] == "IMAGE_NORMALIZED"
    assert envelope["coordinate_metadata"]["box_encoding"] == "CXCYWH"
    assert envelope["coordinate_metadata"]["value_range"] == [0.0, 1.0]
    assert envelope["coordinate_metadata"]["world_coordinate_claimed"] is False
    assert envelope["configuration_snapshot"]["coordinate_basis"] == "IMAGE_NORMALIZED"
    assert envelope["configuration_snapshot"]["box_encoding"] == "CXCYWH"
    assert detection["box_cxcywh"] == [0.40, 0.45, 0.20, 0.30]
    assert detection["phrase"] == "red cup"
    assert envelope["score_metadata"][0]["score_value"] == detection["provider_score"]
    assert envelope["score_metadata"][0]["comparable_with"] == []
    assert envelope["score_metadata"][0]["calibrated"] is False
    assert all(item["scope"] == "INVOCATION_LOCAL_ID" for item in envelope["identity_metadata"])
    assert {item["native_field"] for item in envelope["identity_metadata"]} == {
        "detections[0].detection_index", "detections[0].query_index", "detections[0].phrase_index",
    }
    paths = {item["native_path"] for item in envelope["expected_projection"]["mappings"]}
    assert {"detections[0].box_cxcywh", "detections[0].provider_score", "detections[0].phrase", "detections[0].query_index"} <= paths
    assert envelope["expected_projection"]["candidate_only"] is True
    assert envelope["expected_projection"]["admitted"] is False


def test_empty_result_is_valid_absence_of_candidates_not_world_truth() -> None:
    envelope = envelope_for("EMPTY_OR_NO_RESULT_001")
    assert envelope["native_payload"]["detections"] == []
    assert envelope["identity_metadata"] == []
    assert envelope["expected_projection"]["mappings"] == []
    assert envelope["expected_projection"]["truth_declared"] is False
    assert envelope["score_metadata"][0]["score_name"] == "configured_detection_threshold"
    assert "no detection score exists" in envelope["score_metadata"][0]["score_semantics"]
    assert validate_envelope(envelope) == ()
    assert validate_grounding_dino_native(envelope) == ()


def test_high_score_and_authority_attempt_do_not_admit_or_create_truth() -> None:
    envelope = envelope_for("AUTHORITY_NEGATIVE_001")
    assert envelope["native_payload"]["detections"][0]["provider_score"] == 0.99
    assert envelope["expected_projection"]["truth_declared"] is False
    assert envelope["expected_projection"]["admitted"] is False
    assert envelope["lineage_metadata"]["creates_authority"] is False
    assert "authority_escalation_attempt" in validate_envelope(envelope)
    assert "authority_escalation_attempt" in validate_grounding_dino_native(envelope)
    for key in NEGATIVE_AUTHORITY_KEYS:
        mutated = envelope_for("NORMAL_POSITIVE_001")
        mutated["expected_governance"][key] = True
        assert "governance_boundary_invalid" in validate_envelope(mutated)
    for forbidden in ("luna_canonical_id", "world_truth_declared", "authority_granted"):
        mutated = envelope_for("NORMAL_POSITIVE_001")
        mutated["native_payload"][forbidden] = True
        assert "native_authority_claim_invalid" in validate_envelope(mutated)
        assert "grounding_native_authority_claim_invalid" in validate_grounding_dino_native(mutated)


def test_baseline_and_simulated_variant_coexist_without_official_revision_claim() -> None:
    assert validate_grounding_dino_snapshots(MODEL) == ()
    old, variant = MODEL["snapshots"]["v1"], MODEL["snapshots"]["variant"]
    assert MODEL["snapshot_classification"] == {"v1": "SYNTHETIC_BASELINE", "variant": "SIMULATED_CONTRACT_VARIANT"}
    for key in ("model_contract_ref", "provider_model_revision", "provider_interface_version", "native_contract_version", "adapter_contract_version"):
        assert old[key] != variant[key]
    assert old["provider_model_revision"].startswith("synthetic-")
    assert variant["provider_model_revision"].startswith("synthetic-")
    assert envelope_for("NORMAL_POSITIVE_001")["model_contract_ref"] == old["model_contract_ref"]
    assert envelope_for("VERSION_VARIANT_001")["model_contract_ref"] == variant["model_contract_ref"]
    altered = deepcopy(MODEL)
    altered["snapshots"]["variant"]["native_contract_version"] = old["native_contract_version"]
    assert "grounding_snapshot_dimension_invalid:native_contract_version" in validate_grounding_dino_snapshots(altered)
    altered = deepcopy(MODEL)
    altered["snapshot_classification"]["variant"] = "OFFICIAL_MODEL_REVISION"
    assert "grounding_snapshot_classification_invalid" in validate_grounding_dino_snapshots(altered)


@pytest.mark.parametrize("mutation,expected_error", [
    ("caption", "grounding_input_condition_invalid"),
    ("image_ref", "grounding_input_condition_invalid"),
    ("detections", "grounding_detections_invalid"),
    ("box", "grounding_box_invalid"),
    ("score", "grounding_score_invalid"),
    ("phrase", "grounding_phrase_invalid"),
    ("query_index", "grounding_local_index_invalid"),
    ("coordinate", "grounding_coordinate_contract_invalid"),
    ("score_domain", "grounding_score_contract_invalid"),
    ("prompt_lineage", "grounding_prompt_condition_invalid"),
    ("candidate_lineage", "grounding_candidate_formation_invalid"),
    ("canonical_identity", "grounding_identity_scope_invalid"),
])
def test_malformed_native_contract_fails_closed(mutation: str, expected_error: str) -> None:
    envelope = envelope_for("NORMAL_POSITIVE_001")
    native = envelope["native_payload"]
    detection = native["detections"][0]
    if mutation == "caption":
        native["caption"] = None
    elif mutation == "image_ref":
        native["image_ref"] = "synthetic:image:unlisted"
    elif mutation == "detections":
        native["detections"] = None
    elif mutation == "box":
        detection["box_cxcywh"] = [0.9, 0.5, 0.5]
    elif mutation == "score":
        detection["provider_score"] = 1.2
    elif mutation == "phrase":
        detection["phrase"] = ""
    elif mutation == "query_index":
        detection["query_index"] = True
    elif mutation == "coordinate":
        envelope["coordinate_metadata"]["basis"] = "IMAGE_PIXEL"
    elif mutation == "score_domain":
        envelope["score_metadata"][0]["score_domain"] = "GLOBAL_UNTYPED_CONFIDENCE"
    elif mutation == "prompt_lineage":
        envelope["lineage_metadata"]["relations"][0]["source_ref"] = native["image_ref"]
    elif mutation == "candidate_lineage":
        envelope["lineage_metadata"]["relations"][1]["source_ref"] = native["image_ref"]
    elif mutation == "canonical_identity":
        envelope["identity_metadata"][0]["scope"] = "LUNA_CANONICAL_ID"
    assert expected_error in validate_grounding_dino_native(envelope)


def test_no_real_golden_or_cross_model_fixture_claim() -> None:
    assert len(MODEL["cases"]) == 4
    assert {case["kind"] for case in MODEL["cases"]} == set(CASE_KINDS)
    assert len({case["kind"] for case in MODEL["cases"]}) == 4
    for case in MODEL["cases"]:
        envelope = materialize_case(COLLECTION, MODEL, case)
        assert envelope["source_kind"] == "SYNTHETIC"
        assert envelope["simulation"] is True
        assert all(relation["source_ref"] in envelope["input_refs"] + [envelope["invocation_ref"]]
                   for relation in envelope["lineage_metadata"]["relations"])
