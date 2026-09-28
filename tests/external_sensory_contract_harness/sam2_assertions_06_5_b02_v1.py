"""Test-only SAM2 synthetic native assertions; no model, Gateway, or owner invocation."""

from __future__ import annotations

from typing import Any


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _index(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _score(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and 0 <= value <= 1


def validate_sam2_snapshots(model: dict[str, Any]) -> tuple[str, ...]:
    """Keep synthetic baseline and simulated evolution distinct from official revisions."""
    errors: list[str] = []
    snapshots = model.get("snapshots")
    if not isinstance(snapshots, dict) or set(snapshots) != {"v1", "variant"}:
        return ("sam2_snapshot_set_invalid",)
    if model.get("snapshot_classification") != {
        "v1": "SYNTHETIC_BASELINE", "variant": "SIMULATED_CONTRACT_VARIANT",
    }:
        errors.append("sam2_snapshot_classification_invalid")
    old, variant = snapshots["v1"], snapshots["variant"]
    if not isinstance(old, dict) or not isinstance(variant, dict):
        return ("sam2_snapshot_shape_invalid",)
    for key in (
        "model_contract_ref", "provider_model_revision", "provider_interface_version",
        "native_contract_version", "adapter_contract_version",
    ):
        if not _nonempty(old.get(key)) or not _nonempty(variant.get(key)) or old[key] == variant[key]:
            errors.append(f"sam2_snapshot_dimension_invalid:{key}")
    if any(
        not str(snapshot.get(key, "")).startswith("synthetic-")
        for snapshot in (old, variant)
        for key in ("provider_model_revision", "provider_interface_version", "native_contract_version", "adapter_contract_version")
    ):
        errors.append("sam2_official_version_claim_invalid")
    if any(
        snapshot.get("provider_model") != "SAM2"
        or snapshot.get("provider_family") != "sam2"
        or snapshot.get("capability_class") != "PROMPT_CONDITIONED_SEGMENTATION_AND_MASK_PROPAGATION"
        for snapshot in (old, variant)
    ):
        errors.append("sam2_model_identity_invalid")
    return tuple(dict.fromkeys(errors))


def validate_sam2_native(envelope: dict[str, Any]) -> tuple[str, ...]:
    """Validate synthetic native semantics separately from Universal envelope checks."""
    errors: list[str] = []
    if (
        envelope.get("provider_model") != "SAM2"
        or envelope.get("provider_family") != "sam2"
        or envelope.get("source_kind") != "SYNTHETIC"
        or envelope.get("simulation") is not True
    ):
        errors.append("sam2_provider_identity_invalid")
    native = envelope.get("native_payload")
    if not isinstance(native, dict):
        return ("sam2_native_payload_invalid",)
    mode = native.get("mode")
    config = envelope.get("configuration_snapshot")
    coordinate = envelope.get("coordinate_metadata")
    inputs = envelope.get("input_refs")
    prompt = native.get("prompt")
    prompt_ref = native.get("prompt_ref")
    invocation_ref = envelope.get("invocation_ref")
    if mode not in {"IMAGE_SEGMENTATION", "VIDEO_PROPAGATION"} or not isinstance(config, dict) or config.get("mode") != mode:
        errors.append("sam2_mode_invalid")
    if (
        not _nonempty(prompt_ref) or not isinstance(inputs, list) or prompt_ref not in inputs
        or not _nonempty(invocation_ref) or native.get("invocation_ref") != invocation_ref
        or not isinstance(prompt, dict)
    ):
        errors.append("sam2_prompt_or_invocation_invalid")
    if any(native.get(key) for key in ("luna_canonical_id", "world_truth_declared", "authority_granted", "currentness_granted")):
        errors.append("sam2_native_authority_claim_invalid")

    reference_ref = native.get("image_ref") if mode == "IMAGE_SEGMENTATION" else native.get("frame_ref")
    if (
        not _nonempty(reference_ref) or not isinstance(inputs, list) or reference_ref not in inputs
        or not isinstance(config, dict) or config.get("prompt_coordinate_basis") != "IMAGE_PIXEL"
        or config.get("mask_coordinate_basis") != "IMAGE_PIXEL"
        or config.get("mask_encoding") != "BINARY_MASK_DESCRIPTOR"
        or not isinstance(coordinate, dict) or coordinate.get("basis") != "IMAGE_PIXEL"
        or coordinate.get("reference_scope") != reference_ref
        or coordinate.get("mask_encoding") != "BINARY_MASK_DESCRIPTOR"
        or coordinate.get("world_coordinate_claimed") is not False
        or not _index(coordinate.get("image_width")) or coordinate.get("image_width") == 0
        or not _index(coordinate.get("image_height")) or coordinate.get("image_height") == 0
    ):
        errors.append("sam2_coordinate_contract_invalid")

    if mode == "IMAGE_SEGMENTATION":
        point = prompt.get("coordinates_xy") if isinstance(prompt, dict) else None
        width = coordinate.get("image_width") if isinstance(coordinate, dict) else None
        height = coordinate.get("image_height") if isinstance(coordinate, dict) else None
        if (
            not isinstance(prompt, dict) or prompt.get("type") != "POINT"
            or prompt.get("coordinate_basis") != "IMAGE_PIXEL"
            or not isinstance(point, list) or len(point) != 2 or not all(_index(value) for value in point)
            or not _index(width) or not _index(height)
            or point[0] >= width or point[1] >= height
            or prompt.get("label") not in (0, 1)
            or not isinstance(coordinate, dict) or coordinate.get("prompt_encoding") != "XY_POINT"
        ):
            errors.append("sam2_point_prompt_invalid")
        if envelope.get("temporal_metadata") != []:
            errors.append("sam2_image_temporal_claim_invalid")
    elif mode == "VIDEO_PROPAGATION":
        temporal = envelope.get("temporal_metadata")
        frame_index = native.get("frame_index")
        propagation_order = native.get("propagation_order")
        if (
            not _nonempty(native.get("sequence_ref")) or not isinstance(inputs, list)
            or native["sequence_ref"] not in inputs or not _index(frame_index)
            or not _index(propagation_order) or not isinstance(prompt, dict)
            or prompt.get("type") != "PRIOR_MASK_SEED" or prompt.get("mask_ref") != prompt_ref
            or prompt.get("coordinate_basis") != "IMAGE_PIXEL"
            or not _index(prompt.get("seed_frame_index")) or prompt["seed_frame_index"] >= frame_index
            or not isinstance(coordinate, dict) or coordinate.get("prompt_encoding") != "PRIOR_MASK_SEED"
            or not isinstance(temporal, list) or len(temporal) != 2
            or {item.get("role"): item.get("value") for item in temporal if isinstance(item, dict)} != {
                "FRAME_INDEX_OR_ORDER": frame_index, "TRACKING_PROPAGATION_ORDER": propagation_order,
            }
            or any(not isinstance(item, dict) or item.get("creates_currentness") is not False
                   or item.get("clock_domain") != "SAM2_SYNTHETIC_SEQUENCE_LOCAL" for item in temporal)
        ):
            errors.append("sam2_propagation_order_invalid")

    masks = native.get("masks")
    empty = str(envelope.get("case_id", "")).endswith("EMPTY_OR_NO_RESULT_001")
    if not isinstance(masks, list):
        errors.append("sam2_masks_invalid")
        masks = []
    elif empty and masks:
        errors.append("sam2_empty_result_invalid")
    elif not empty and not masks:
        errors.append("sam2_masks_invalid")
    seen_indexes: set[int] = set()
    for mask in masks:
        if not isinstance(mask, dict):
            errors.append("sam2_mask_shape_invalid")
            continue
        index = mask.get("mask_index")
        if not _index(index) or index in seen_indexes:
            errors.append("sam2_local_mask_index_invalid")
        else:
            seen_indexes.add(index)
        width, height = mask.get("width"), mask.get("height")
        if (
            mask.get("representation") != "BINARY_MASK_DESCRIPTOR"
            or not _nonempty(mask.get("mask_ref"))
            or mask.get("spatial_basis") != "IMAGE_PIXEL"
            or mask.get("reference_scope") != reference_ref
            or not _index(width) or not _index(height) or width == 0 or height == 0
            or not isinstance(coordinate, dict) or width != coordinate.get("image_width")
            or height != coordinate.get("image_height")
            or not _index(mask.get("foreground_pixel_count"))
            or mask["foreground_pixel_count"] > width * height
        ):
            errors.append("sam2_mask_representation_invalid")
        if not _score(mask.get("provider_quality_score")):
            errors.append("sam2_mask_score_invalid")
        if mode == "VIDEO_PROPAGATION" and (
            not _index(mask.get("object_index")) or mask.get("frame_index") != native.get("frame_index")
        ):
            errors.append("sam2_sequence_local_identity_invalid")

    identities = envelope.get("identity_metadata")
    if not isinstance(identities, list) or any(
        not isinstance(item, dict) or item.get("scope") not in {
            "INVOCATION_LOCAL_ID", "SESSION_LOCAL_TRACK_ID", "MEDIA_LOCAL_REGION_ID",
        } for item in identities
    ):
        errors.append("sam2_identity_scope_invalid")
    elif empty and identities:
        errors.append("sam2_empty_identity_invalid")
    elif masks:
        expected = {("INVOCATION_LOCAL_ID", "masks[0].mask_index")}
        if mode == "VIDEO_PROPAGATION":
            expected |= {("SESSION_LOCAL_TRACK_ID", "masks[0].object_index"),
                         ("MEDIA_LOCAL_REGION_ID", "frame_index")}
        if not expected <= {(item.get("scope"), item.get("native_field")) for item in identities}:
            errors.append("sam2_identity_scope_invalid")

    scores = envelope.get("score_metadata")
    if empty and scores != []:
        errors.append("sam2_empty_score_claim_invalid")
    elif masks and (
        not isinstance(scores, list) or len(scores) != 1 or not isinstance(scores[0], dict)
        or scores[0].get("score_name") != "provider_mask_quality"
        or scores[0].get("score_domain") != "SAM2_SYNTHETIC_PROVIDER_LOCAL_MASK_QUALITY"
        or scores[0].get("score_range") != [0.0, 1.0]
        or scores[0].get("comparable_with") != [] or scores[0].get("calibrated") is not False
        or scores[0].get("score_value") != masks[0].get("provider_quality_score")
    ):
        errors.append("sam2_score_contract_invalid")

    lineage = envelope.get("lineage_metadata")
    relations = lineage.get("relations") if isinstance(lineage, dict) else None
    if not isinstance(relations, list) or lineage.get("creates_authority") is not False:
        errors.append("sam2_lineage_invalid")
    else:
        conditioned = [item for item in relations if isinstance(item, dict) and item.get("kind") == "CONDITIONED_BY"]
        produced = [item for item in relations if isinstance(item, dict) and item.get("kind") == "PRODUCED_FROM"]
        if (
            len(conditioned) != 1 or conditioned[0].get("source_ref") != prompt_ref
            or conditioned[0].get("subject_ref") != invocation_ref
        ):
            errors.append("sam2_prompt_condition_invalid")
        if masks and (len(produced) != 1 or produced[0].get("source_ref") != invocation_ref):
            errors.append("sam2_mask_formation_invalid")
        if empty and produced:
            errors.append("sam2_empty_mask_lineage_invalid")
        if len(relations) != len(conditioned) + len(produced):
            errors.append("sam2_unexpected_relation_invalid")

    projection = envelope.get("expected_projection")
    if (
        not isinstance(projection, dict) or projection.get("candidate_only") is not True
        or projection.get("truth_declared") is not False or projection.get("admitted") is not False
        or any(key in projection for key in (
            "canonical_id", "luna_epistemic_confidence", "currentness_proof", "authorization_proof",
        ))
    ):
        errors.append("sam2_projection_authority_invalid")
    if isinstance(envelope.get("authority_attempt"), dict) and any(
        value is not False for value in envelope["authority_attempt"].values()
    ):
        errors.append("authority_escalation_attempt")
    return tuple(dict.fromkeys(errors))
