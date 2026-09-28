"""Test-only C01 composite assertions; no provider, Gateway, or authority invocation."""

from __future__ import annotations

from copy import deepcopy
import math
from typing import Any

from grounding_dino_assertions_06_5_b01_v1 import validate_grounding_dino_native
from sam2_assertions_06_5_b02_v1 import validate_sam2_native


def materialize_case(collection: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(collection["defaults"])

    def merge(target: dict[str, Any], update: dict[str, Any]) -> None:
        for key, item in update.items():
            if isinstance(item, dict) and isinstance(target.get(key), dict):
                merge(target[key], item)
            else:
                target[key] = deepcopy(item)

    merge(value, case.get("overrides", {}))
    value["case_id"] = case["case_id"]
    value["case_kind"] = case["case_kind"]
    return value


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _box_valid(box: Any) -> bool:
    return (
        isinstance(box, list) and len(box) == 4 and all(_finite(value) for value in box)
        and 0 <= box[0] <= 1 and 0 <= box[1] <= 1
        and 0 < box[2] <= 1 and 0 < box[3] <= 1
        and box[0] - box[2] / 2 >= 0 and box[0] + box[2] / 2 <= 1
        and box[1] - box[3] / 2 >= 0 and box[1] + box[3] / 2 <= 1
    )


def _same_number(left: Any, right: Any) -> bool:
    return _finite(left) and _finite(right) and math.isclose(left, right, rel_tol=0.0, abs_tol=1e-12)


def _provider_envelopes(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    grounding = case["grounding"]
    prompt = case["original_text_prompt"]
    image = case["image_space"]["source"]
    detection = grounding["detections"][0]
    grounding_envelope = {
        "provider_model": "Grounding DINO", "provider_family": "grounding_dino",
        "source_kind": "SYNTHETIC", "simulation": True,
        "native_payload": {"image_ref": grounding["image_ref"], "prompt_ref": grounding["prompt_ref"], "caption": grounding["caption"], "detections": [{key: value for key, value in detection.items() if key != "detection_ref"}]},
        "input_refs": [grounding["image_ref"], grounding["prompt_ref"]],
        "configuration_snapshot": {"prompt_basis": "text_caption", "detection_threshold": 0.30, "box_encoding": "CXCYWH", "coordinate_basis": "IMAGE_NORMALIZED"},
        "coordinate_metadata": {"basis": "IMAGE_NORMALIZED", "box_encoding": "CXCYWH", "value_range": [0.0, 1.0], "reference_scope": grounding["image_ref"], "world_coordinate_claimed": False},
        "identity_metadata": [{"scope": "INVOCATION_LOCAL_ID", "native_field": "detections[0].detection_index"}, {"scope": "INVOCATION_LOCAL_ID", "native_field": "detections[0].query_index"}, {"scope": "INVOCATION_LOCAL_ID", "native_field": "detections[0].phrase_index"}],
        "score_metadata": [{"score_name": "provider_grounding_score", "score_value": detection["provider_score"], "score_domain": "GROUNDING_DINO_SYNTHETIC_PROVIDER_LOCAL", "score_semantics": "provider-local ranking", "score_range": [0.0, 1.0], "threshold": 0.30, "calibrated": False, "comparable_with": []}],
        "lineage_metadata": {"relations": case["relations"]["grounding"], "creates_authority": False},
        "invocation_ref": grounding["invocation_ref"],
        "expected_projection": {"candidate_only": True, "truth_declared": False, "admitted": False},
    }
    sam = case["sam2"]
    derived = case["derived_box_prompt"]
    sam_envelope = {
        "provider_model": "SAM2", "provider_family": "sam2", "source_kind": "SYNTHETIC", "simulation": True,
        "native_payload": {"mode": "IMAGE_SEGMENTATION", "image_ref": sam["image_ref"], "prompt_ref": sam["prompt_ref"], "prompt": {"type": "BOX", "box_xyxy": derived["box_xyxy"], "coordinate_basis": derived["coordinate_basis"], "box_encoding": derived["box_encoding"], "coordinate_type": derived["coordinate_type"]}, "invocation_ref": sam["invocation_ref"], "masks": sam["masks"]},
        "input_refs": [sam["image_ref"], sam["prompt_ref"]],
        "configuration_snapshot": {"mode": "IMAGE_SEGMENTATION", "prompt_coordinate_basis": "IMAGE_PIXEL", "mask_coordinate_basis": "IMAGE_PIXEL", "mask_encoding": "BINARY_MASK_DESCRIPTOR", "image_space": {"image_ref": image["image_ref"], "orientation": image["orientation"], "resize": image["resize"], "crop": image["crop"], "letterbox": image["letterbox"]}},
        "coordinate_metadata": {"basis": "IMAGE_PIXEL", "reference_scope": sam["image_ref"], "prompt_encoding": "XYXY", "box_encoding": "XYXY", "coordinate_type": "FINITE_FLOAT_PIXEL_COORDINATES", "mask_encoding": "BINARY_MASK_DESCRIPTOR", "image_ref": sam["image_ref"], "image_width": image["image_width"], "image_height": image["image_height"], "world_coordinate_claimed": False},
        "identity_metadata": [{"scope": "INVOCATION_LOCAL_ID", "native_field": "masks[0].mask_index"}],
        "score_metadata": [{"score_name": "provider_mask_quality", "score_value": sam["provider_quality_score"], "score_domain": "SAM2_SYNTHETIC_PROVIDER_LOCAL_MASK_QUALITY", "score_semantics": "provider-local mask quality", "score_range": [0.0, 1.0], "threshold": None, "calibrated": False, "comparable_with": []}],
        "temporal_metadata": [],
        "lineage_metadata": {"relations": case["relations"]["sam2"], "creates_authority": False},
        "invocation_ref": sam["invocation_ref"],
        "expected_projection": {"candidate_only": True, "truth_declared": False, "admitted": False},
    }
    return grounding_envelope, sam_envelope


def validate_composite_case(case: dict[str, Any]) -> tuple[str, ...]:
    errors: list[str] = []
    grounding = case.get("grounding")
    derived = case.get("derived_box_prompt")
    sam = case.get("sam2")
    image_space = case.get("image_space")
    mapping = case.get("handoff_mapping")
    order = case.get("processing_order")
    relations = case.get("relations")
    authority = case.get("authority")
    prompt = case.get("original_text_prompt")
    if case.get("source_kind") != "SYNTHETIC" or case.get("simulation") is not True:
        errors.append("synthetic_boundary_invalid")
    if not isinstance(prompt, dict) or not _nonempty(prompt.get("ref")) or not _nonempty(prompt.get("text")):
        errors.append("original_prompt_invalid")
    if not isinstance(image_space, dict) or not isinstance(image_space.get("source"), dict) or not isinstance(image_space.get("target"), dict):
        errors.append("image_space_declaration_invalid")
    else:
        source, target = image_space["source"], image_space["target"]
        fields = ("image_ref", "image_width", "image_height", "orientation", "resize", "crop", "letterbox")
        if any(field not in source or field not in target for field in fields):
            errors.append("image_space_declaration_invalid")
        elif source != target or source["image_width"] <= 0 or source["image_height"] <= 0:
            errors.append("image_space_mismatch")
    if not isinstance(grounding, dict) or not isinstance(grounding.get("detections"), list):
        errors.append("grounding_output_invalid")
    elif not grounding["detections"]:
        if any(value is not None for value in (derived, sam)):
            errors.append("empty_upstream_downstream_fabricated")
        return tuple(dict.fromkeys(errors))
    else:
        detection = grounding["detections"][0]
        if not _box_valid(detection.get("box_cxcywh")):
            errors.extend(("grounding_box_invalid", "handoff_source_detection_invalid"))
        if not _nonempty(detection.get("detection_ref")):
            errors.append("grounding_detection_identity_invalid")
    if not isinstance(derived, dict) or not isinstance(sam, dict) or not isinstance(mapping, dict):
        errors.append("handoff_artifact_invalid")
        return tuple(dict.fromkeys(errors))
    detection = grounding["detections"][0]
    if mapping.get("source_detection_ref") != detection.get("detection_ref"):
        errors.append("handoff_source_detection_missing")
    if mapping.get("derived_prompt_ref") != derived.get("ref") or derived.get("ref") == detection.get("detection_ref"):
        errors.append("identity_namespace_escalation" if derived.get("ref") == detection.get("detection_ref") else "handoff_prompt_identity_invalid")
    if derived.get("ref") == sam.get("invocation_ref") or sam.get("invocation_ref") == sam.get("mask_ref"):
        errors.append("identity_namespace_escalation")
    source = image_space["source"]
    box = detection.get("box_cxcywh")
    expected = [(box[0] - box[2] / 2) * source["image_width"], (box[1] - box[3] / 2) * source["image_height"], (box[0] + box[2] / 2) * source["image_width"], (box[1] + box[3] / 2) * source["image_height"]]
    actual = derived.get("box_xyxy")
    if (derived.get("image_ref") != source.get("image_ref") or derived.get("coordinate_basis") != "IMAGE_PIXEL" or derived.get("box_encoding") != "XYXY" or derived.get("coordinate_type") != "FINITE_FLOAT_PIXEL_COORDINATES" or not isinstance(actual, list) or len(actual) != 4 or any(not _same_number(left, right) for left, right in zip(actual, expected))):
        errors.append("mechanical_transform_invalid")
    if mapping.get("source_coordinate_basis") != "IMAGE_NORMALIZED" or mapping.get("source_box_encoding") != "CXCYWH" or mapping.get("target_coordinate_basis") != "IMAGE_PIXEL" or mapping.get("target_box_encoding") != "XYXY" or mapping.get("transform") != "NORMALIZED_CXCYWH_TO_PIXEL_XYXY" or mapping.get("transform_authority") != "NONE":
        errors.append("handoff_mapping_invalid")
    if sam.get("prompt_ref") != derived.get("ref") or sam.get("image_ref") != source.get("image_ref") or not _nonempty(sam.get("mask_ref")):
        errors.append("sam2_handoff_target_invalid")
    if not isinstance(relations, dict) or relations.get("creates_authority") is not False:
        errors.append("relation_authority_invalid")
    else:
        expected_grounding = {"CONDITIONED_BY", "PRODUCED_FROM"}
        expected_sam2 = {"CONDITIONED_BY", "PRODUCED_FROM"}
        if {item.get("kind") for item in relations.get("grounding", [])} != expected_grounding or {item.get("kind") for item in relations.get("sam2", [])} != expected_sam2:
            errors.append("provider_lineage_invalid")
        if not any(item.get("kind") == "CONDITIONED_BY" and item.get("source_ref") == prompt.get("ref") for item in relations.get("grounding", [])):
            errors.append("original_prompt_provenance_missing")
        if not any(item.get("kind") == "CONDITIONED_BY" and item.get("source_ref") == derived.get("ref") for item in relations.get("sam2", [])):
            errors.append("derived_prompt_provenance_missing")
    if not isinstance(authority, dict) or any(value is not False for key, value in authority.items() if key not in {"handoff_mapping_authority", "cross_provider_score_comparison_allowed", "composite_confidence_created", "luna_epistemic_confidence_created"}) or authority.get("handoff_mapping_authority") != "NONE":
        errors.append("composite_authority_claim_invalid")
    if not isinstance(authority, dict) or authority.get("cross_provider_score_comparison_allowed") is not False or authority.get("composite_confidence_created") is not False or authority.get("luna_epistemic_confidence_created") is not False:
        errors.append("cross_provider_score_boundary_invalid")
    if not isinstance(order, dict) or not (order.get("grounding") < order.get("handoff") < order.get("sam2")):
        errors.append("processing_order_invalid")
    if not isinstance(order, dict) or order.get("creates_currentness") is not False:
        errors.append("composite_currentness_claim_invalid")
    return tuple(dict.fromkeys(errors))


def validate_composite_collection(collection: dict[str, Any]) -> tuple[str, ...]:
    errors: list[str] = []
    if collection.get("composite_key") != "GROUNDING_DINO_TO_SAM2" or collection.get("composite_type") != "SYNTHETIC_CROSS_PROVIDER_HANDOFF":
        errors.append("composite_identity_invalid")
    if collection.get("model_count_increment") != 0 or collection.get("provider_contract_snapshot_increment") != 0:
        errors.append("composite_count_boundary_invalid")
    for case in collection.get("cases", []):
        actual = validate_composite_case(materialize_case(collection, case))
        if tuple(case.get("expected_errors", [])) != actual:
            errors.append(f"{case.get('case_id')}:expected_errors_mismatch:{actual}")
    return tuple(errors)
