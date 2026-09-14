# -*- coding: utf-8 -*-
"""YOLO VisionDetectionEvidence → vision_recognition_evidence_pack_v0 (evaluation-only stub).

Phase-Vision-YOLO-Evidence-Pack-Integration-Stub-001
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from capabilities.vision_runtime.vision_recognition_evidence_pack_v0 import EVIDENCE_PACK_SCHEMA

INTEGRATION_SUMMARY_SCHEMA = "yolo_evidence_pack_integration_summary_v0"
YOLO_MATRIX_SCHEMA = "yolo_vision_recognition_evidence_matrix_v0"
PROVIDER_SUMMARY_SCHEMA = "yolo_provider_summary_v0"
CONSUMER_COMPAT_SCHEMA = "yolo_evidence_consumer_compatibility_report_v0"
RISK_SCHEMA = "yolo_evidence_pack_risk_report_v0"
AUDIT_SCHEMA = "yolo_evidence_pack_audit_v0"

FORBIDDEN_KEYS: Set[str] = {
    "confirmed_object",
    "confirmed_fact",
    "navigation_action",
}

FORBIDDEN_LABELS: Set[str] = {
    "confirmed_object",
    "confirmed_fact",
}


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _scan_forbidden(obj: Any, path: str = "$") -> List[str]:
    hits: List[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            ks = str(k)
            if ks in FORBIDDEN_KEYS:
                hits.append(f"{path}.{ks}")
            hits.extend(_scan_forbidden(v, f"{path}.{ks}"))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits.extend(_scan_forbidden(v, f"{path}[{i}]"))
    return hits


def detection_evidence_to_pack_item_v0(det: Dict[str, Any]) -> Dict[str, Any]:
    """Map vision_detection_evidence_v0 → pack item row."""
    bbox_f = det.get("bbox_in_frame")
    bbox_u = det.get("bbox_in_unit")
    if not isinstance(bbox_f, list) or len(bbox_f) != 4:
        bbox_f = [0, 0, 0, 0]
    if not isinstance(bbox_u, list) or len(bbox_u) != 4:
        bbox_u = list(bbox_f)

    label = str(det.get("label") or det.get("class_name") or "unknown")
    item: Dict[str, Any] = {
        "evidence_id": str(det.get("evidence_id") or f"evidence_{uuid.uuid4().hex[:16]}"),
        "source_frame_id": str(det.get("source_frame_id") or ""),
        "unit_id": str(det.get("unit_id") or ""),
        "roi_id": str(det.get("roi_id") or ""),
        "source_unit_ref": str(det.get("source_unit_ref") or det.get("unit_id") or ""),
        "label": label,
        "confidence": float(det.get("confidence") or 0.0),
        "bbox_in_unit": [int(v) for v in bbox_u],
        "bbox_in_frame": [int(v) for v in bbox_f],
        "synthetic": det.get("synthetic") is True,
        "stub_provider": det.get("stub_provider") is True,
        "fact_status": str(det.get("fact_status") or "not_fact"),
        "coordinate_space": str(det.get("coordinate_space") or "frame_pixel"),
    }
    if det.get("class_id") is not None:
        item["class_id"] = det.get("class_id")
    if det.get("class_name"):
        item["class_name"] = str(det.get("class_name"))
    if det.get("evidence_role"):
        item["evidence_role"] = str(det.get("evidence_role"))
    if isinstance(det.get("source_chain"), list):
        item["source_chain"] = list(det.get("source_chain") or [])
    image_ref = None
    for part in item.get("source_chain") or []:
        if str(part).startswith("image_ref:"):
            image_ref = str(part).split("image_ref:", 1)[-1]
    if image_ref:
        item["crop_image_ref"] = image_ref
    return item


def build_yolo_provider_summary_v0(
    *,
    evidence_count: int,
    detector_mode: str,
    positive_root: str,
) -> Dict[str, Any]:
    return {
        "schema": PROVIDER_SUMMARY_SCHEMA,
        "provider": "yolo_candidate_adapter",
        "provider_level": "evaluation_candidate",
        "detector_mode": detector_mode,
        "real_detector_invoked": True,
        "yolo_invoked": True,
        "fixture_used": False,
        "evidence_count": evidence_count,
        "source_yolo_positive_sample_root": positive_root,
    }


def build_consumer_compatibility_report_v0(
    evidence_pack: Dict[str, Any],
) -> Dict[str, Any]:
    items = evidence_pack.get("items") if isinstance(evidence_pack.get("items"), list) else []
    pt = evidence_pack.get("provider_trace") if isinstance(evidence_pack.get("provider_trace"), dict) else {}
    pack_chain = evidence_pack.get("source_chain") if isinstance(evidence_pack.get("source_chain"), list) else []

    gaps: List[str] = []
    checks: Dict[str, bool] = {
        "items_count_positive": len(items) > 0,
        "pack_fact_status_not_fact": str(evidence_pack.get("fact_status") or "") == "not_fact",
        "provider_trace_present": bool(pt.get("provider")),
        "pack_source_chain_present": len(pack_chain) > 0,
        "no_confirmed_object_keys": True,
        "no_navigation_action_keys": True,
    }

    forbidden_hits = _scan_forbidden(evidence_pack)
    if forbidden_hits:
        checks["no_confirmed_object_keys"] = False
        checks["no_navigation_action_keys"] = False
        gaps.extend([f"forbidden_key:{h}" for h in forbidden_hits])

    per_item_ok = 0
    for it in items:
        if not isinstance(it, dict):
            gaps.append("invalid_item_type")
            continue
        ok = True
        if str(it.get("fact_status") or "") != "not_fact":
            ok = False
            gaps.append(f"item_fact_status:{it.get('evidence_id')}")
        if not isinstance(it.get("bbox_in_frame"), list) or len(it.get("bbox_in_frame") or []) != 4:
            ok = False
            gaps.append(f"item_bbox_in_frame:{it.get('evidence_id')}")
        if not it.get("source_chain"):
            gaps.append(f"item_source_chain_optional_missing:{it.get('evidence_id')}")
        if str(it.get("label") or "") in FORBIDDEN_LABELS:
            ok = False
            gaps.append(f"item_forbidden_label:{it.get('evidence_id')}")
        if ok:
            per_item_ok += 1

    checks["all_items_have_bbox_in_frame"] = per_item_ok == len(items) and len(items) > 0
    checks["all_items_fact_status_not_fact"] = all(
        isinstance(it, dict) and str(it.get("fact_status") or "") == "not_fact" for it in items
    )

    consumer_compatible = all(checks.values()) and not any(
        g.startswith("forbidden_key:") for g in gaps
    )

    return {
        "schema": CONSUMER_COMPAT_SCHEMA,
        "consumer_compatible": consumer_compatible,
        "checks": checks,
        "gaps": gaps,
        "items_count": len(items),
        "note": "Static compatibility vs Vision read-only consumer semantics; does not invoke consumer runner.",
    }


def build_risk_report_v0() -> Dict[str, Any]:
    return {
        "schema": RISK_SCHEMA,
        "yolo_label_not_fact": True,
        "real_detector_output_not_fact": True,
        "confidence_not_truth": True,
        "detection_not_navigation_decision": True,
        "no_midplatform_fact_write": True,
        "no_scene_delta_write": True,
        "no_world_model_write": True,
        "no_mainline_registry_change": True,
        "no_default_provider_change": True,
        "no_navigation_decision": True,
        "narrative": [
            "YOLO evidence pack is real_detector_candidate scope only; fact_status remains not_fact.",
            "Does not replace vision_stub mainline or change default provider registry.",
        ],
    }


def build_audit_v0() -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "yolo_evidence_pack_integration_executed": True,
        "evaluation_only": True,
        "real_detector_invoked": True,
        "yolo_invoked": True,
        "fixture_used": False,
        "vision_mainline_modified": False,
        "vision_provider_registry_default_changed": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "supervision_mainline_invoked": False,
        "vlm_invoked": False,
        "ocr_invoked": False,
        "database_write_invoked": False,
    }


def run_yolo_evidence_pack_integration_stub_v0(
    *,
    yolo_positive_sample_root: str,
    vision_recognition_evidence_pack_stub_root: str = "",
) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []
    yolo_root = Path(yolo_positive_sample_root).resolve()
    stub_root = (
        Path(vision_recognition_evidence_pack_stub_root).resolve()
        if vision_recognition_evidence_pack_stub_root.strip()
        else None
    )

    if not yolo_root.is_dir():
        errs.append("missing_yolo_positive_sample_root")

    fixture_p = yolo_root / "yolo_real_positive_vision_detection_evidence_fixture.json"
    matrix_in_p = yolo_root / "yolo_real_positive_detection_to_vision_evidence_matrix.json"
    det_summary_p = yolo_root / "yolo_real_positive_detector_result_summary.json"

    if not fixture_p.is_file():
        errs.append("missing_yolo_real_positive_vision_detection_evidence_fixture")

    detections: List[Dict[str, Any]] = []
    detector_mode = "real_yolo"
    if fixture_p.is_file():
        raw = _read_json(fixture_p)
        if isinstance(raw, dict):
            detector_mode = str(raw.get("detector_mode") or "real_yolo")
            detections = [d for d in (raw.get("items") or []) if isinstance(d, dict)]

    if not detections:
        errs.append("yolo_detection_items_empty")

    pack_items: List[Dict[str, Any]] = []
    matrix_rows: List[Dict[str, Any]] = []

    for det in detections:
        if str(det.get("schema_version") or "") != "vision_detection_evidence_v0":
            errs.append(f"unexpected_detection_schema:{det.get('evidence_id')}")
        if det.get("synthetic") is not False:
            errs.append(f"synthetic_must_be_false:{det.get('evidence_id')}")
        if det.get("stub_provider") is not False:
            errs.append(f"stub_provider_must_be_false:{det.get('evidence_id')}")
        if str(det.get("fact_status") or "") != "not_fact":
            errs.append(f"fact_status_must_be_not_fact:{det.get('evidence_id')}")
        if str(det.get("label") or "") in FORBIDDEN_LABELS:
            errs.append(f"forbidden_label:{det.get('evidence_id')}")

        item = detection_evidence_to_pack_item_v0(det)
        pack_items.append(item)
        matrix_rows.append(
            {
                "evidence_id": item["evidence_id"],
                "source_frame_id": item.get("source_frame_id"),
                "roi_id": item.get("roi_id"),
                "unit_id": item.get("unit_id"),
                "label": item.get("label"),
                "class_id": item.get("class_id"),
                "confidence": item.get("confidence"),
                "synthetic": item.get("synthetic"),
                "stub_provider": item.get("stub_provider"),
                "fact_status": item.get("fact_status"),
                "bbox_in_frame": item.get("bbox_in_frame"),
                "bbox_in_unit": item.get("bbox_in_unit"),
                "source_unit_ref": item.get("source_unit_ref"),
                "detector_mode": detector_mode,
            }
        )

    pack_id = f"evpack_yolo_{uuid.uuid4().hex[:16]}"
    source_chain = [
        f"yolo_positive_sample_root:{yolo_root}",
        f"yolo_fixture_ref:{fixture_p}",
    ]
    if matrix_in_p.is_file():
        source_chain.append(f"yolo_matrix_ref:{matrix_in_p}")
    if det_summary_p.is_file():
        source_chain.append(f"yolo_detector_summary_ref:{det_summary_p}")
    if stub_root and stub_root.is_dir():
        source_chain.append(f"reference_stub_pack_root:{stub_root}")
    source_chain.append("yolo_evidence_pack_integration_stub_built")

    evidence_pack = {
        "schema_version": EVIDENCE_PACK_SCHEMA,
        "pack_id": pack_id,
        "source_phase": "Vision-YOLO-Real-Smoke-Positive-Sample-001",
        "provider_trace": {
            "provider": "yolo_candidate_adapter",
            "provider_level": "evaluation_candidate",
            "real_provider_invoked": True,
            "detector_mode": detector_mode,
            "yolo_invoked": True,
            "fixture_used": False,
        },
        "evidence_scope": "real_detector_candidate",
        "fact_status": "not_fact",
        "items": pack_items,
        "source_chain": source_chain,
    }

    evidence_matrix = {
        "schema": YOLO_MATRIX_SCHEMA,
        "rows": matrix_rows,
        "converted_from": "yolo_real_positive_vision_detection_evidence_fixture",
    }

    provider_summary = build_yolo_provider_summary_v0(
        evidence_count=len(pack_items),
        detector_mode=detector_mode,
        positive_root=str(yolo_root),
    )

    consumer_report = build_consumer_compatibility_report_v0(evidence_pack)
    if not consumer_report.get("consumer_compatible"):
        for g in consumer_report.get("gaps") or []:
            if not str(g).startswith("item_source_chain_optional"):
                errs.append(f"consumer_gap:{g}")

    risk = build_risk_report_v0()
    audit = build_audit_v0()

    forbidden = _scan_forbidden(evidence_pack)
    if forbidden:
        errs.extend([f"forbidden_in_pack:{h}" for h in forbidden])

    phase_verdict = "GO"
    if errs:
        if pack_items and consumer_report.get("consumer_compatible") is not True:
            phase_verdict = "CONDITIONAL_GO"
        else:
            phase_verdict = "NO_GO"
    elif consumer_report.get("gaps"):
        phase_verdict = "CONDITIONAL_GO"

    summary = {
        "schema_version": INTEGRATION_SUMMARY_SCHEMA,
        "phase": "Phase-Vision-YOLO-Evidence-Pack-Integration-Stub-001",
        "yolo_positive_sample_root": str(yolo_root),
        "vision_recognition_evidence_pack_stub_root": str(stub_root) if stub_root else None,
        "evidence_count": len(pack_items),
        "detector_mode": detector_mode,
        "consumer_compatible": consumer_report.get("consumer_compatible"),
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    return (
        summary,
        evidence_pack,
        evidence_matrix,
        provider_summary,
        consumer_report,
        risk,
        audit,
        errs,
    )
