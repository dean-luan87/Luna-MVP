# -*- coding: utf-8 -*-
"""VisionDetectionEvidence v0 schema alignment (static; no Supervision mainline, no YOLO).

Phase-VisionDetectionEvidence-Schema-Alignment-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SCHEMA_VERSION = "vision_detection_evidence_v0"
SCHEMA_DOC_SCHEMA = "vision_detection_evidence_schema_v0"
MAPPING_MATRIX_SCHEMA = "vision_detection_evidence_supervision_mapping_matrix_v0"
BOUNDARY_REPORT_SCHEMA = "vision_detection_evidence_boundary_report_v0"
ALIGNMENT_AUDIT_SCHEMA = "vision_detection_evidence_schema_alignment_audit_v0"

REQUIRED_FIELD_NAMES = (
    "evidence_id",
    "source_frame_id",
    "roi_id",
    "unit_id",
    "provider",
    "label",
    "confidence",
    "bbox_in_frame",
    "fact_status",
)

OPTIONAL_FIELD_NAMES = (
    "stream_id",
    "frame_index",
    "timestamp_ms",
    "source_unit_ref",
    "provider_level",
    "provider_output_ref",
    "class_id",
    "class_name",
    "bbox_in_unit",
    "polygon_in_frame",
    "mask_ref",
    "tracker_id",
    "track_id_scope",
    "coordinate_space",
    "synthetic",
    "stub_provider",
    "evidence_role",
    "source_chain",
)


def build_vision_detection_evidence_schema_template_v0() -> Dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "description": "Luna visual detection candidate evidence (not_fact, not navigation input).",
        "required_fields": list(REQUIRED_FIELD_NAMES),
        "optional_fields": list(OPTIONAL_FIELD_NAMES),
        "field_definitions": {
            "evidence_id": "Stable id for this detection candidate row.",
            "source_frame_id": "Frame trace / stream frame id (required lineage).",
            "roi_id": "ROI proposal id within frame.",
            "unit_id": "Provider input unit id (crop / tile).",
            "provider": "e.g. vision_stub, supervision_adapter, yolo_gated (candidate only).",
            "provider_level": "stub | lightweight | heavy",
            "label": "Provider class label string; candidate_only, not confirmed object.",
            "confidence": "Provider score; not truthfulness.",
            "bbox_in_frame": "[x1,y1,x2,y2] in frame_pixel space.",
            "fact_status": "Must be not_fact for stub/synthetic phases.",
            "tracker_id": "Provider-local track id; not identity fact.",
            "track_id_scope": "provider_local | none",
            "evidence_role": "visual_detection_candidate",
        },
        "example_shape": {
            "schema_version": SCHEMA_VERSION,
            "evidence_id": "evidence_example",
            "source_frame_id": "stream_example_f000000",
            "stream_id": None,
            "frame_index": None,
            "timestamp_ms": None,
            "roi_id": "vision_roi_example",
            "unit_id": "unit_example",
            "source_unit_ref": "unit_example",
            "provider": "vision_stub",
            "provider_level": "stub",
            "provider_output_ref": "vision_provider_stub_result.json",
            "label": "stub_object",
            "class_id": None,
            "class_name": "stub_object",
            "confidence": 0.5,
            "bbox_in_unit": [0, 0, 100, 100],
            "bbox_in_frame": [10, 20, 110, 120],
            "polygon_in_frame": None,
            "mask_ref": None,
            "tracker_id": None,
            "track_id_scope": "none",
            "coordinate_space": "frame_pixel",
            "synthetic": True,
            "stub_provider": True,
            "fact_status": "not_fact",
            "evidence_role": "visual_detection_candidate",
            "source_chain": ["vision_provider_input_pack", "vision_stub_result"],
        },
    }


def build_supervision_mapping_matrix_v0(
    supervision_reference_mapping: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Supervision Detections → VisionDetectionEvidence v0 (derived from structure reference)."""
    rows: List[Dict[str, Any]] = [
        {
            "supervision_field": "xyxy",
            "luna_fields": ["bbox_in_frame", "bbox_in_unit"],
            "notes": "Lift bbox_in_unit to frame using ROI offset when applicable.",
        },
        {
            "supervision_field": "confidence",
            "luna_fields": ["confidence"],
            "notes": "Score only; not_fact.",
        },
        {
            "supervision_field": "class_id",
            "luna_fields": ["class_id"],
            "notes": "Optional numeric class id from detector.",
        },
        {
            "supervision_field": "class name / data",
            "luna_fields": ["class_name", "label"],
            "notes": "label is candidate string; never confirmed_object.",
        },
        {
            "supervision_field": "mask",
            "luna_fields": ["mask_ref"],
            "notes": "Reference or inline mask artifact; geometry candidate.",
        },
        {
            "supervision_field": "polygon",
            "luna_fields": ["polygon_in_frame"],
            "notes": "Optional polygon vertices in frame_pixel.",
        },
        {
            "supervision_field": "tracker_id",
            "luna_fields": ["tracker_id"],
            "notes": "track_id_scope=provider_local; not identity.",
        },
        {
            "supervision_field": "detections metadata",
            "luna_fields": ["provider_output_ref", "source_chain"],
            "notes": "Preserve adapter / probe lineage.",
        },
    ]
    gaps: List[str] = []
    if supervision_reference_mapping:
        ref_rows = supervision_reference_mapping.get("rows")
        if isinstance(ref_rows, list):
            det_row = next(
                (r for r in ref_rows if isinstance(r, dict) and "VisionDetectionEvidence" in str(r.get("luna_target"))),
                None,
            )
            if not det_row:
                gaps.append("structure_reference_missing_detections_row")
    else:
        gaps.append("structure_reference_mapping_not_loaded_optional")

    return {
        "schema": MAPPING_MATRIX_SCHEMA,
        "source": "supervision_structure_reference_analysis_v0",
        "rows": rows,
        "gaps": gaps,
    }


def pack_item_to_vision_detection_evidence_v0(
    item: Dict[str, Any],
    *,
    pack_meta: Dict[str, Any],
    provider_output_ref: str,
) -> Dict[str, Any]:
    """Map vision_recognition_evidence_pack_v0 item → vision_detection_evidence_v0."""
    bbox_frame = item.get("bbox_in_frame")
    bbox_unit = item.get("bbox_in_unit")
    if not isinstance(bbox_frame, list) or len(bbox_frame) != 4:
        bbox_frame = [0, 0, 0, 0]
    if not isinstance(bbox_unit, list) or len(bbox_unit) != 4:
        bbox_unit = list(bbox_frame)

    provider = str(pack_meta.get("provider") or "vision_stub")
    provider_level = "stub" if item.get("stub_provider") else "lightweight"

    chain = [
        str(pack_meta.get("evidence_pack_id") or "vision_recognition_evidence_pack"),
        f"source_frame_id:{item.get('source_frame_id')}",
        f"roi_id:{item.get('roi_id')}",
        f"unit_id:{item.get('unit_id')}",
    ]
    if item.get("crop_image_ref"):
        chain.append(f"crop_image_ref:{item.get('crop_image_ref')}")

    return {
        "schema_version": SCHEMA_VERSION,
        "evidence_id": str(item.get("evidence_id") or ""),
        "source_frame_id": str(item.get("source_frame_id") or ""),
        "stream_id": None,
        "frame_index": None,
        "timestamp_ms": None,
        "roi_id": str(item.get("roi_id") or ""),
        "unit_id": str(item.get("unit_id") or ""),
        "source_unit_ref": str(item.get("source_unit_ref") or item.get("unit_id") or ""),
        "provider": provider,
        "provider_level": provider_level,
        "provider_output_ref": provider_output_ref,
        "label": str(item.get("label") or "stub_object"),
        "class_id": None,
        "class_name": str(item.get("label") or "stub_object"),
        "confidence": float(item.get("confidence") or 0.0),
        "bbox_in_unit": [int(v) for v in bbox_unit],
        "bbox_in_frame": [int(v) for v in bbox_frame],
        "polygon_in_frame": None,
        "mask_ref": None,
        "tracker_id": None,
        "track_id_scope": "none",
        "coordinate_space": str(item.get("coordinate_space") or "frame_pixel"),
        "synthetic": bool(item.get("synthetic", True)),
        "stub_provider": bool(item.get("stub_provider", True)),
        "fact_status": str(item.get("fact_status") or "not_fact"),
        "evidence_role": "visual_detection_candidate",
        "source_chain": chain,
    }


def build_stub_compat_fixture_v0(
    pack: Dict[str, Any],
    *,
    provider_output_ref: str,
    max_items: int = 5,
) -> Dict[str, Any]:
    items = pack.get("items") if isinstance(pack.get("items"), list) else []
    meta = {
        "provider": pack.get("provider") or "vision_stub",
        "evidence_pack_id": pack.get("evidence_pack_id"),
    }
    converted: List[Dict[str, Any]] = []
    for it in items[: max(0, int(max_items))]:
        if isinstance(it, dict):
            converted.append(pack_item_to_vision_detection_evidence_v0(it, pack_meta=meta, provider_output_ref=provider_output_ref))
    return {
        "schema": "vision_detection_evidence_stub_compat_fixture_v0",
        "source_pack_schema": pack.get("schema_version"),
        "item_count": len(converted),
        "items": converted,
    }


def build_boundary_report_v0() -> Dict[str, Any]:
    return {
        "schema": BOUNDARY_REPORT_SCHEMA,
        "label_not_fact": True,
        "confidence_not_truth": True,
        "tracker_id_not_identity": True,
        "mask_bbox_not_traversable": True,
        "no_navigation_decision": True,
        "no_midplatform_fact_write": True,
        "no_scene_delta_write": True,
        "no_world_model_write": True,
        "no_ai_interpretation": True,
        "must_not": [
            "label_is_not_confirmed_object",
            "confidence_is_not_truthfulness",
            "tracker_id_is_not_identity_fact",
            "bbox_mask_polygon_are_geometry_candidates_only",
            "evidence_must_not_directly_trigger_navigation",
            "evidence_must_not_write_midplatform_fact",
            "evidence_must_not_write_scene_delta",
            "evidence_must_not_write_world_model",
        ],
        "narrative": [
            "VisionDetectionEvidence rows are visual_detection_candidate observations only.",
            "Supervision Detections xyxy maps to bbox fields but does not elevate to fact.",
            "tracker_id uses track_id_scope=provider_local when present; default none for stub.",
        ],
    }


def build_schema_alignment_audit_v0() -> Dict[str, Any]:
    return {
        "schema": ALIGNMENT_AUDIT_SCHEMA,
        "vision_detection_schema_alignment_executed": True,
        "supervision_mainline_invoked": False,
        "yolo_invoked": False,
        "real_detector_invoked": False,
        "navigation_decision_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "database_write_invoked": False,
    }


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def run_vision_detection_evidence_schema_alignment_v0(
    *,
    supervision_structure_reference_root: str,
    vision_recognition_evidence_pack_root: str,
    stub_fixture_max_items: int = 5,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], List[str]]:
    """Returns summary, schema_doc, example, stub_fixture, mapping, boundary, audit, errors."""
    errs: List[str] = []

    sup_root = Path(supervision_structure_reference_root).resolve()
    pack_root = Path(vision_recognition_evidence_pack_root).resolve()

    if not sup_root.is_dir():
        errs.append(f"supervision_reference_root_missing:{sup_root}")
    if not pack_root.is_dir():
        errs.append(f"evidence_pack_root_missing:{pack_root}")

    sup_mapping = None
    sup_map_p = sup_root / "supervision_to_luna_mapping_matrix.json"
    if sup_map_p.is_file():
        sup_mapping = _read_json(sup_map_p)
    else:
        errs.append("missing_supervision_to_luna_mapping_matrix")

    pack_p = pack_root / "vision_recognition_evidence_pack.json"
    pack: Dict[str, Any] = {}
    if pack_p.is_file():
        raw = _read_json(pack_p)
        if isinstance(raw, dict):
            pack = raw
        else:
            errs.append("evidence_pack_invalid")
    else:
        errs.append("missing_vision_recognition_evidence_pack")

    schema_doc = build_vision_detection_evidence_schema_template_v0()
    example = dict(schema_doc.get("example_shape") or {})
    example["schema_version"] = SCHEMA_VERSION

    provider_ref = str(pack_root / "vision_recognition_evidence_pack.json")
    stub_fixture = build_stub_compat_fixture_v0(
        pack, provider_output_ref=provider_ref, max_items=stub_fixture_max_items
    )
    mapping = build_supervision_mapping_matrix_v0(sup_mapping if isinstance(sup_mapping, dict) else None)
    boundary = build_boundary_report_v0()
    audit = build_schema_alignment_audit_v0()

    if mapping.get("gaps"):
        for g in mapping["gaps"]:
            if g != "structure_reference_mapping_not_loaded_optional":
                errs.append(f"mapping_gap:{g}")

    for it in stub_fixture.get("items") or []:
        if not isinstance(it, dict):
            continue
        if it.get("synthetic") is not True:
            errs.append(f"fixture_synthetic_not_true:{it.get('evidence_id')}")
        if str(it.get("fact_status") or "") != "not_fact":
            errs.append(f"fixture_fact_status_not_not_fact:{it.get('evidence_id')}")

    summary = {
        "schema_version": "vision_detection_evidence_schema_alignment_summary_v0",
        "phase": "Phase-VisionDetectionEvidence-Schema-Alignment-001",
        "supervision_structure_reference_root": str(sup_root),
        "vision_recognition_evidence_pack_root": str(pack_root),
        "vision_detection_evidence_schema_version": SCHEMA_VERSION,
        "stub_compat_item_count": stub_fixture.get("item_count"),
        "supervision_mapping_row_count": len(mapping.get("rows") or []),
        "errors": list(errs),
    }

    return summary, schema_doc, example, stub_fixture, mapping, boundary, audit, errs
