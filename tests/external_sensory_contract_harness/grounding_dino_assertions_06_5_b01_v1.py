"""Test-only Grounding DINO synthetic native assertions; no provider invocation or admission."""

from __future__ import annotations

from typing import Any


def _number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_grounding_dino_snapshots(model: dict[str, Any]) -> tuple[str, ...]:
    """Distinguish two synthetic contract snapshots, never official releases."""
    errors: list[str] = []
    snapshots = model.get("snapshots")
    if not isinstance(snapshots, dict) or set(snapshots) != {"v1", "variant"}:
        return ("grounding_snapshot_set_invalid",)
    if model.get("snapshot_classification") != {
        "v1": "SYNTHETIC_BASELINE", "variant": "SIMULATED_CONTRACT_VARIANT",
    }:
        errors.append("grounding_snapshot_classification_invalid")
    old, variant = snapshots["v1"], snapshots["variant"]
    if not isinstance(old, dict) or not isinstance(variant, dict):
        return ("grounding_snapshot_shape_invalid",)
    for field in (
        "model_contract_ref", "provider_model_revision", "provider_interface_version",
        "native_contract_version", "adapter_contract_version",
    ):
        if not _nonempty(old.get(field)) or not _nonempty(variant.get(field)) or old[field] == variant[field]:
            errors.append(f"grounding_snapshot_dimension_invalid:{field}")
    if any(not str(snapshot.get("provider_model_revision", "")).startswith("synthetic-")
           or not str(snapshot.get("native_contract_version", "")).startswith("synthetic-")
           or not str(snapshot.get("adapter_contract_version", "")).startswith("synthetic-")
           for snapshot in (old, variant)):
        errors.append("grounding_official_version_claim_invalid")
    if any(snapshot.get("provider_model") != "Grounding DINO"
           or snapshot.get("provider_family") != "grounding_dino"
           or snapshot.get("capability_class") != "TEXT_CONDITIONED_OPEN_SET_DETECTION"
           for snapshot in (old, variant)):
        errors.append("grounding_model_identity_invalid")
    return tuple(dict.fromkeys(errors))


def validate_grounding_dino_native(envelope: dict[str, Any]) -> tuple[str, ...]:
    """Check one synthetic native/result relation; never create Luna truth or authority."""
    errors: list[str] = []
    if (envelope.get("provider_model") != "Grounding DINO"
            or envelope.get("provider_family") != "grounding_dino"
            or envelope.get("source_kind") != "SYNTHETIC"
            or envelope.get("simulation") is not True):
        errors.append("grounding_provider_identity_invalid")
    native = envelope.get("native_payload")
    if not isinstance(native, dict):
        return ("grounding_native_payload_invalid",)
    image_ref, prompt_ref, caption = (native.get("image_ref"), native.get("prompt_ref"), native.get("caption"))
    inputs = envelope.get("input_refs")
    if (not _nonempty(image_ref) or not _nonempty(prompt_ref) or not _nonempty(caption)
            or not isinstance(inputs, list) or image_ref not in inputs or prompt_ref not in inputs):
        errors.append("grounding_input_condition_invalid")
    if any(native.get(key) for key in ("luna_canonical_id", "world_truth_declared", "authority_granted")):
        errors.append("grounding_native_authority_claim_invalid")

    config, coordinate = envelope.get("configuration_snapshot"), envelope.get("coordinate_metadata")
    if not isinstance(config, dict) or not isinstance(coordinate, dict):
        errors.append("grounding_coordinate_contract_invalid")
        threshold = None
    else:
        threshold = config.get("detection_threshold")
        if (config.get("prompt_basis") != "text_caption"
                or config.get("box_encoding") != "CXCYWH"
                or config.get("coordinate_basis") != "IMAGE_NORMALIZED"
                or not _number(threshold) or not 0 <= threshold <= 1
                or coordinate.get("basis") != "IMAGE_NORMALIZED"
                or coordinate.get("box_encoding") != "CXCYWH"
                or coordinate.get("value_range") != [0.0, 1.0]
                or coordinate.get("reference_scope") != image_ref
                or coordinate.get("world_coordinate_claimed") is not False):
            errors.append("grounding_coordinate_contract_invalid")

    detections = native.get("detections")
    empty_case = str(envelope.get("case_id", "")).endswith("EMPTY_OR_NO_RESULT_001")
    if not isinstance(detections, list):
        errors.append("grounding_detections_invalid")
        detections = []
    elif empty_case and detections:
        errors.append("grounding_empty_result_invalid")
    elif not empty_case and not detections:
        errors.append("grounding_detections_invalid")
    seen_indexes: set[int] = set()
    for detection in detections:
        if not isinstance(detection, dict):
            errors.append("grounding_detection_shape_invalid")
            continue
        indexes = (detection.get("detection_index"), detection.get("query_index"), detection.get("phrase_index"))
        if any(not isinstance(index, int) or isinstance(index, bool) or index < 0 for index in indexes):
            errors.append("grounding_local_index_invalid")
        elif indexes[0] in seen_indexes:
            errors.append("grounding_local_index_invalid")
        else:
            seen_indexes.add(indexes[0])
        box = detection.get("box_cxcywh")
        if (not isinstance(box, list) or len(box) != 4 or not all(_number(value) and 0 <= value <= 1 for value in box)
                or (isinstance(box, list) and len(box) == 4 and all(_number(value) for value in box)
                    and (box[2] <= 0 or box[3] <= 0 or box[0] - box[2] / 2 < 0 or box[0] + box[2] / 2 > 1
                         or box[1] - box[3] / 2 < 0 or box[1] + box[3] / 2 > 1))):
            errors.append("grounding_box_invalid")
        score = detection.get("provider_score")
        if not _number(score) or not 0 <= score <= 1:
            errors.append("grounding_score_invalid")
        phrase = detection.get("phrase")
        if not _nonempty(phrase) or not isinstance(caption, str) or phrase not in caption:
            errors.append("grounding_phrase_invalid")

    identities = envelope.get("identity_metadata")
    if not isinstance(identities, list) or any(not isinstance(item, dict) or item.get("scope") != "INVOCATION_LOCAL_ID" for item in identities):
        errors.append("grounding_identity_scope_invalid")
    elif detections and not {"detections[0].detection_index", "detections[0].query_index", "detections[0].phrase_index"} <= {
        item.get("native_field") for item in identities
    }:
        errors.append("grounding_identity_scope_invalid")
    elif empty_case and identities:
        errors.append("grounding_empty_identity_invalid")

    scores = envelope.get("score_metadata")
    if not isinstance(scores, list) or len(scores) != 1 or not isinstance(scores[0], dict):
        errors.append("grounding_score_contract_invalid")
    else:
        score_contract = scores[0]
        expected_name = "configured_detection_threshold" if empty_case else "provider_grounding_score"
        if (score_contract.get("score_name") != expected_name
                or score_contract.get("score_domain") != "GROUNDING_DINO_SYNTHETIC_PROVIDER_LOCAL"
                or score_contract.get("score_range") != [0.0, 1.0]
                or score_contract.get("comparable_with") != []
                or score_contract.get("calibrated") is not False
                or not _nonempty(score_contract.get("score_semantics"))
                or score_contract.get("threshold") != threshold):
            errors.append("grounding_score_contract_invalid")
        if empty_case and score_contract.get("score_value") != threshold:
            errors.append("grounding_empty_score_claim_invalid")
        if detections and score_contract.get("score_value") != detections[0].get("provider_score"):
            errors.append("grounding_score_projection_invalid")

    lineage = envelope.get("lineage_metadata")
    relations = lineage.get("relations") if isinstance(lineage, dict) else None
    if not isinstance(relations, list) or lineage.get("creates_authority") is not False:
        errors.append("grounding_lineage_invalid")
    else:
        conditions = [item for item in relations if isinstance(item, dict) and item.get("kind") == "CONDITIONED_BY"]
        produced = [item for item in relations if isinstance(item, dict) and item.get("kind") == "PRODUCED_FROM"]
        if (len(conditions) != 1 or conditions[0].get("source_ref") != prompt_ref
                or conditions[0].get("subject_ref") != envelope.get("invocation_ref")):
            errors.append("grounding_prompt_condition_invalid")
        if detections and (len(produced) != 1 or produced[0].get("source_ref") != envelope.get("invocation_ref")):
            errors.append("grounding_candidate_formation_invalid")
        if empty_case and produced:
            errors.append("grounding_empty_candidate_lineage_invalid")

    projection = envelope.get("expected_projection")
    if (not isinstance(projection, dict) or projection.get("candidate_only") is not True
            or projection.get("truth_declared") is not False or projection.get("admitted") is not False
            or any(key in projection for key in ("canonical_id", "luna_epistemic_confidence", "currentness_proof", "authorization_proof"))):
        errors.append("grounding_projection_authority_invalid")
    if isinstance(envelope.get("authority_attempt"), dict) and any(
        value is not False for value in envelope["authority_attempt"].values()
    ):
        errors.append("authority_escalation_attempt")
    return tuple(dict.fromkeys(errors))
