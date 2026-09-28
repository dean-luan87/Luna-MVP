"""Test-only validation of synthetic external-sensory contract fixtures.

This module never imports or invokes a provider, Gateway, or domain owner.
It checks declared native-to-candidate mappings, not runtime admission.
"""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any


FIXTURE_PATH = Path(__file__).with_name("fixtures_v1.json")
SCHEMA_VERSION = "external-sensory-simulation-fixture-v1"
CASE_KINDS = (
    "NORMAL_POSITIVE_001",
    "EMPTY_OR_NO_RESULT_001",
    "AUTHORITY_NEGATIVE_001",
    "VERSION_VARIANT_001",
)
IDENTITY_SCOPES = frozenset({
    "MODEL_LOCAL_INDEX", "INVOCATION_LOCAL_ID", "SESSION_LOCAL_TRACK_ID",
    "MEDIA_LOCAL_REGION_ID", "CLUSTER_LOCAL_ID", "EXTERNAL_STABLE_ID",
    "LUNA_CANONICAL_ID",
})
TEMPORAL_ROLES = frozenset({
    "MEDIA_CAPTURE_OR_EVENT_TIME", "MEDIA_RELATIVE_TIME", "FRAME_INDEX_OR_ORDER",
    "PROVIDER_PROCESSING_TIME", "ALIGNMENT_TIME", "TRACKING_PROPAGATION_ORDER",
})
COORDINATE_BASES = frozenset({
    "IMAGE_PIXEL", "IMAGE_NORMALIZED", "CAMERA_SENSOR_FRAME", "SLAM_MAP_FRAME",
    "TRAJECTORY_REFERENCE_FRAME", "RELATIVE_DEPTH", "METRIC_DEPTH",
})
COORDINATE_REQUIRED_MODELS = frozenset({"YOLO26", "ORB-SLAM3", "RelateAnything"})
RELATIONS = frozenset({
    "PRODUCED_FROM", "GROUNDED_FROM", "ALIGNED_WITH", "RELATION_ENDPOINT_FROM",
})
NEGATIVE_AUTHORITY_KEYS = (
    "provider_output_is_truth", "adapter_can_admit_evidence",
    "adapter_can_admit_field_truth", "provider_local_id_is_canonical_identity",
    "provider_score_is_luna_epistemic_confidence",
    "provider_timestamp_is_temporal_authority", "lineage_creates_authority",
    "simulation_can_create_production_truth",
)
REQUIRED_ENVELOPE_KEYS = frozenset({
    "fixture_schema_version", "source_kind", "simulation", "model_contract_ref",
    "provider_family", "provider_model", "provider_model_revision",
    "provider_interface_version", "capability_class", "case_id", "invocation_ref",
    "configuration_snapshot", "input_refs", "native_payload", "expected_projection",
    "temporal_metadata", "coordinate_metadata", "identity_metadata",
    "score_metadata", "lineage_metadata", "expected_governance",
    "migration_reference",
})


def load_collection(path: Path = FIXTURE_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def materialize_case(collection: dict[str, Any], model: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    """Expand file-local shared test metadata; never construct runtime objects."""
    snapshot = model["snapshots"][case["snapshot"]]
    envelope = {
        "fixture_schema_version": collection["fixture_schema_version"],
        "source_kind": "SYNTHETIC",
        "simulation": True,
        **copy.deepcopy(snapshot),
        "case_id": f"{model['model_key']}:{case['kind']}",
        "invocation_ref": f"synthetic-invocation:{model['model_key']}:{case['kind']}",
        "configuration_snapshot": copy.deepcopy(model["configuration_snapshot"]),
        "input_refs": copy.deepcopy(model["input_refs"]),
        "temporal_metadata": copy.deepcopy(model["temporal_metadata"]),
        "coordinate_metadata": copy.deepcopy(model["coordinate_metadata"]),
        "identity_metadata": copy.deepcopy(model["identity_metadata"]),
        "score_metadata": copy.deepcopy(model["score_metadata"]),
        "lineage_metadata": copy.deepcopy(model["lineage_metadata"]),
        "expected_governance": {key: False for key in NEGATIVE_AUTHORITY_KEYS},
        "migration_reference": None,
        "native_payload": copy.deepcopy(case["native_payload"]),
        "expected_projection": copy.deepcopy(case["expected_projection"]),
    }
    for key in ("configuration_snapshot", "temporal_metadata", "coordinate_metadata", "identity_metadata", "score_metadata", "lineage_metadata", "migration_reference"):
        if key in case:
            envelope[key] = copy.deepcopy(case[key])
    if "authority_attempt" in case:
        envelope["authority_attempt"] = copy.deepcopy(case["authority_attempt"])
    return envelope


def executable_cases(collection: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    """Enumerate identities and inherited metadata from the stored fixture tree."""
    return tuple(
        materialize_case(collection, model, case)
        for model in collection["models"]
        for case in model["cases"]
    )


def _native_at(payload: Any, path: str) -> Any:
    current = payload
    for part in re.findall(r"[^.\[\]]+|\[\d+\]", path):
        current = current[int(part[1:-1])] if part.startswith("[") else current[part]
    return current


def _model_specific_errors(envelope: dict[str, Any]) -> tuple[str, ...]:
    """Bounded structural checks only; no model inference or world adjudication."""
    native = envelope.get("native_payload")
    if not isinstance(native, dict):
        return ()
    model = envelope.get("provider_model")
    empty = str(envelope.get("case_id", "")).endswith("EMPTY_OR_NO_RESULT_001")
    errors: list[str] = []
    if model == "YOLO26":
        detections = native.get("detections")
        coordinates = envelope.get("coordinate_metadata")
        if not isinstance(detections, list) or not isinstance(coordinates, dict) or coordinates.get("basis") != "IMAGE_PIXEL" or not all(isinstance(native.get(key), int) and native[key] > 0 for key in ("image_width", "image_height")):
            errors.append("detection_basis_invalid")
        elif not empty and (not detections or any(not isinstance(item, dict) or not all(key in item for key in ("bbox_xyxy", "class_id", "label", "confidence", "detection_id", "track_id")) or not isinstance(item["bbox_xyxy"], list) or len(item["bbox_xyxy"]) != 4 for item in detections)):
            errors.append("detection_shape_invalid")
    elif model == "Qwen3-VL":
        if not all(key in native for key in ("media_ref", "messages", "processor_ref", "template_ref", "generation_config", "generated_text")) or not isinstance(native.get("messages"), list):
            errors.append("generated_payload_shape_invalid")
    elif model == "Qwen3-ASR":
        temporal = envelope.get("temporal_metadata")
        if not all(key in native for key in ("audio_ref", "transcript", "language", "aligner_revision", "segments")) or not isinstance(native.get("segments"), list) or not isinstance(temporal, list) or not any(isinstance(item, dict) and item.get("role") == "MEDIA_RELATIVE_TIME" for item in temporal):
            errors.append("asr_media_time_invalid")
    elif model == "ORB-SLAM3":
        coordinates = envelope.get("coordinate_metadata")
        if not isinstance(coordinates, dict) or coordinates.get("basis") != "SLAM_MAP_FRAME" or not coordinates.get("reference_scope") or coordinates.get("metric_scale_proven") is not False or not all(key in native for key in ("map_session_ref", "sensor_mode", "provider_timestamp", "translation", "quaternion_xyzw", "coordinate_frame", "tracking_state")) or native.get("coordinate_frame") != coordinates.get("reference_scope"):
            errors.append("slam_frame_or_scale_invalid")
        elif not empty and (not isinstance(native.get("translation"), list) or len(native["translation"]) != 3 or not isinstance(native.get("quaternion_xyzw"), list) or len(native["quaternion_xyzw"]) != 4):
            errors.append("slam_pose_invalid")
    elif model == "RelateAnything":
        relations = native.get("relations")
        if not native.get("predicate_vocabulary_version") or not isinstance(relations, list):
            errors.append("relation_vocabulary_invalid")
        elif not empty and (not relations or any(not isinstance(item, dict) or not all(key in item for key in ("subject_region", "predicate", "object_region", "rank")) for item in relations)):
            errors.append("relation_endpoint_invalid")
    else:
        errors.append("model_not_in_v1_set")
    return tuple(errors)


def validate_envelope(envelope: dict[str, Any]) -> tuple[str, ...]:
    errors: list[str] = []
    if not REQUIRED_ENVELOPE_KEYS.issubset(envelope):
        errors.append("required_envelope_field_missing")
    if envelope.get("fixture_schema_version") != SCHEMA_VERSION:
        errors.append("fixture_schema_version_invalid")
    if envelope.get("source_kind") not in {"SYNTHETIC", "REAL_GOLDEN"}:
        errors.append("source_kind_invalid")
    if envelope.get("source_kind") == "SYNTHETIC" and envelope.get("simulation") is not True:
        errors.append("synthetic_must_be_simulation")
    if envelope.get("source_kind") == "REAL_GOLDEN" and envelope.get("simulation") is not False:
        errors.append("golden_must_not_be_simulation")
    for key in ("model_contract_ref", "provider_family", "provider_model", "provider_model_revision", "provider_interface_version", "native_contract_version", "adapter_contract_version", "capability_class", "case_id", "invocation_ref"):
        if not isinstance(envelope.get(key), str) or not envelope[key].strip():
            errors.append(f"{key}_missing")
    if not isinstance(envelope.get("native_payload"), dict):
        errors.append("native_payload_invalid")
    governance = envelope.get("expected_governance")
    if not isinstance(governance, dict) or any(governance.get(key) is not False for key in NEGATIVE_AUTHORITY_KEYS):
        errors.append("governance_boundary_invalid")
    attempt = envelope.get("authority_attempt", {})
    if not isinstance(attempt, dict) or any(value is not False for value in attempt.values()):
        errors.append("authority_escalation_attempt")
    projection = envelope.get("expected_projection")
    if not isinstance(projection, dict) or projection.get("candidate_only") is not True or projection.get("truth_declared") is not False or projection.get("admitted") is not False:
        errors.append("projection_authority_invalid")
    else:
        if any(key in projection for key in ("canonical_id", "luna_epistemic_confidence", "currentness_proof", "authorization_proof")):
            errors.append("projection_authority_invalid")
        mappings = projection.get("mappings")
        if not isinstance(mappings, list):
            errors.append("projection_mappings_invalid")
        else:
            for mapping in mappings:
                if not isinstance(mapping, dict) or not all(isinstance(mapping.get(k), str) and mapping[k] for k in ("native_path", "candidate_path", "conversion", "loss")):
                    errors.append("projection_mapping_shape_invalid")
                    continue
                try:
                    native_value = _native_at(envelope["native_payload"], mapping["native_path"])
                except (KeyError, IndexError, TypeError, ValueError):
                    errors.append("projection_native_path_missing")
                    continue
                if mapping.get("conversion") == "identity" and native_value != mapping.get("expected_value"):
                    errors.append("projection_value_mismatch")
    identities = envelope.get("identity_metadata")
    if not isinstance(identities, list) or any(not isinstance(item, dict) or item.get("scope") not in IDENTITY_SCOPES or item.get("scope") == "LUNA_CANONICAL_ID" for item in identities):
        errors.append("identity_scope_invalid")
    elif any(item.get("native_field") and not _native_path_exists(envelope.get("native_payload"), item["native_field"]) for item in identities):
        errors.append("identity_native_path_missing")
    temporal = envelope.get("temporal_metadata")
    if not isinstance(temporal, list) or any(not isinstance(item, dict) or item.get("role") not in TEMPORAL_ROLES or item.get("creates_currentness") is not False or item.get("clock_domain") is None for item in temporal):
        errors.append("temporal_role_invalid")
    coordinates = envelope.get("coordinate_metadata")
    if (coordinates is None and envelope.get("provider_model") in COORDINATE_REQUIRED_MODELS) or (coordinates is not None and (not isinstance(coordinates, dict) or coordinates.get("basis") not in COORDINATE_BASES or not coordinates.get("reference_scope"))):
        errors.append("coordinate_basis_invalid")
    scores = envelope.get("score_metadata")
    if scores is not None:
        if not isinstance(scores, list):
            errors.append("score_metadata_invalid")
        else:
            for score in scores:
                if not isinstance(score, dict) or not all(key in score for key in ("score_name", "score_value", "score_domain", "score_semantics", "score_range", "threshold", "calibrated", "comparable_with")) or not isinstance(score.get("score_name"), str) or not score.get("score_name") or not isinstance(score.get("score_domain"), str) or not score.get("score_domain") or not isinstance(score.get("score_semantics"), str) or not score.get("score_semantics") or not isinstance(score.get("score_value"), (int, float)) or isinstance(score.get("score_value"), bool) or not isinstance(score.get("score_range"), list) or len(score.get("score_range")) != 2 or not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in score.get("score_range", [])) or not isinstance(score.get("calibrated"), bool) or not isinstance(score.get("comparable_with"), list) or score.get("comparable_with"):
                    errors.append("score_semantics_invalid")
                elif not score["score_range"][0] <= score["score_value"] <= score["score_range"][1]:
                    errors.append("score_value_out_of_range")
    lineage = envelope.get("lineage_metadata")
    if not isinstance(lineage, dict) or lineage.get("creates_authority") is not False or not isinstance(lineage.get("relations"), list) or any(not isinstance(relation, dict) or relation.get("kind") not in RELATIONS or not relation.get("source_ref") for relation in lineage.get("relations", [])):
        errors.append("lineage_boundary_invalid")
    native = envelope.get("native_payload")
    if isinstance(native, dict) and any(native.get(key) for key in ("luna_canonical_id", "world_truth_declared", "authority_granted")):
        errors.append("native_authority_claim_invalid")
    errors.extend(_model_specific_errors(envelope))
    return tuple(dict.fromkeys(errors))


def _native_path_exists(payload: Any, path: str) -> bool:
    try:
        _native_at(payload, path)
        return True
    except (KeyError, IndexError, TypeError, ValueError):
        return False


def validate_collection(collection: dict[str, Any]) -> tuple[str, ...]:
    errors: list[str] = []
    models = collection.get("models")
    if collection.get("fixture_schema_version") != SCHEMA_VERSION or not isinstance(models, list) or len(models) != 5:
        return ("collection_shape_invalid",)
    if len({model.get("model_key") for model in models}) != 5:
        errors.append("duplicate_model_key")
    for model in models:
        snapshots = model.get("snapshots", {})
        cases = model.get("cases", [])
        if set(snapshots) != {"v1", "variant"} or {case.get("kind") for case in cases} != set(CASE_KINDS) or len(cases) != 4:
            errors.append(f"case_or_snapshot_set_invalid:{model.get('model_key')}")
            continue
        old, variant = snapshots["v1"], snapshots["variant"]
        if (old["model_contract_ref"] == variant["model_contract_ref"]
                or any(old[key] == variant[key] for key in ("provider_model_revision", "native_contract_version", "adapter_contract_version"))):
            errors.append(f"historical_version_overwrite:{model['model_key']}")
        if (not all(snapshot["provider_model_revision"].startswith("synthetic-") for snapshot in (old, variant))
                or model.get("snapshot_classification") != {
                    "v1": "SYNTHETIC_BASELINE",
                    "variant": "SIMULATED_CONTRACT_VARIANT",
                }):
            errors.append(f"simulated_variant_disguise:{model['model_key']}")
        for case in cases:
            envelope = materialize_case(collection, model, case)
            result = validate_envelope(envelope)
            if case["kind"] == "AUTHORITY_NEGATIVE_001":
                if result != ("authority_escalation_attempt",):
                    errors.append(f"negative_case_not_rejected:{model['model_key']}")
            elif result:
                errors.extend(f"{model['model_key']}:{case['kind']}:{error}" for error in result)
    return tuple(dict.fromkeys(errors))
