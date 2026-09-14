# -*- coding: utf-8 -*-
"""Supervision synthetic adapter vs rule_stub ROI A/B (evaluation-only).

Phase-Vision-Supervision-Adapter-AB-Test-001
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

VISION_DETECTION_SCHEMA = "vision_detection_evidence_v0"
ROI_CANDIDATE_SCHEMA = "vision_roi_proposal_candidate_v0"
AB_SUMMARY_SCHEMA = "supervision_adapter_ab_test_summary_v0"
AB_INPUT_SCHEMA = "supervision_adapter_ab_input_summary_v0"
FIXTURE_SCHEMA = "supervision_synthetic_to_vision_detection_fixture_v0"
COMPARISON_SCHEMA = "supervision_adapter_ab_comparison_matrix_v0"
SCORE_SCHEMA = "supervision_adapter_structure_score_report_v0"
RISK_SCHEMA = "supervision_adapter_ab_risk_report_v0"
AUDIT_SCHEMA = "supervision_adapter_ab_audit_v0"

REQUIRED_EVIDENCE_FIELDS = (
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


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _valid_bbox(bbox: Any) -> bool:
    if not isinstance(bbox, list) or len(bbox) != 4:
        return False
    try:
        x1, y1, x2, y2 = (float(v) for v in bbox)
    except (TypeError, ValueError):
        return False
    return x2 > x1 and y2 > y1


def _evidence_id_for_roi(roi_id: str, provider: str) -> str:
    h = hashlib.sha256(f"{provider}:{roi_id}".encode("utf-8")).hexdigest()[:16]
    return f"evidence_{h}"


def supervision_roi_to_vision_detection_evidence_v0(
    roi_item: Dict[str, Any],
    *,
    candidate: Dict[str, Any],
    experiment_root: str,
    index: int,
) -> Dict[str, Any]:
    """Convert supervision synthetic ROI row → vision_detection_evidence_v0 (not_fact)."""
    roi_id = str(roi_item.get("roi_id") or f"vision_roi_{index:03d}")
    bbox = roi_item.get("bbox_in_frame")
    if not isinstance(bbox, list) or len(bbox) != 4:
        bbox = [0, 0, 0, 0]
    label = str(roi_item.get("class_name") or roi_item.get("label") or "synthetic_unknown")
    conf = float(roi_item.get("confidence") if roi_item.get("confidence") is not None else 1.0)
    source_frame_id = str(
        roi_item.get("source_frame_id") or candidate.get("source_frame_id") or "unknown_frame"
    )
    chain = list(candidate.get("source_chain") or [])
    chain.extend(
        [
            "supervision_synthetic_adapter",
            f"roi_id:{roi_id}",
            "not_real_detector_output",
        ]
    )
    unit_id = f"unit_{roi_id}"
    return {
        "schema_version": VISION_DETECTION_SCHEMA,
        "evidence_id": _evidence_id_for_roi(roi_id, "supervision_synthetic_adapter"),
        "source_frame_id": source_frame_id,
        "stream_id": None,
        "frame_index": None,
        "timestamp_ms": None,
        "roi_id": roi_id,
        "unit_id": unit_id,
        "source_unit_ref": unit_id,
        "provider": "supervision_synthetic_adapter",
        "provider_level": "external_experiment",
        "provider_output_ref": str(Path(experiment_root) / "external_supervision_synthetic_detections.json"),
        "label": label,
        "class_id": None,
        "class_name": label,
        "confidence": conf,
        "bbox_in_unit": [int(v) for v in bbox],
        "bbox_in_frame": [int(v) for v in bbox],
        "polygon_in_frame": None,
        "mask_ref": roi_item.get("mask_ref"),
        "tracker_id": roi_item.get("tracker_id"),
        "track_id_scope": "provider_local" if roi_item.get("tracker_id") is not None else "none",
        "coordinate_space": str(roi_item.get("coordinate_space") or "frame_pixel"),
        "synthetic": True,
        "stub_provider": True,
        "fact_status": "not_fact",
        "evidence_role": "visual_detection_candidate",
        "source_chain": chain,
    }


def rule_stub_roi_to_vision_detection_evidence_v0(
    roi_item: Dict[str, Any],
    *,
    candidate: Dict[str, Any],
    stub_root: str,
    index: int,
) -> Dict[str, Any]:
    """Dry-run conversion for A/B metrics (rule_stub arm)."""
    roi_id = str(roi_item.get("roi_id") or f"rule_stub_roi_{index}")
    bbox = roi_item.get("bbox_in_frame")
    if not isinstance(bbox, list) or len(bbox) != 4:
        bbox = [0, 0, 0, 0]
    label = str(roi_item.get("roi_type") or roi_item.get("class_name") or "rule_stub_roi")
    source_frame_id = str(
        roi_item.get("source_frame_id") or candidate.get("source_frame_id") or "unknown_frame"
    )
    chain = [
        str(candidate.get("frame_input_governance_root_ref") or stub_root),
        "proposal_source:rule_stub",
        f"roi_id:{roi_id}",
    ]
    if roi_item.get("source_image_ref"):
        chain.append(f"source_image_ref:{roi_item.get('source_image_ref')}")
    unit_id = f"unit_{roi_id}"
    return {
        "schema_version": VISION_DETECTION_SCHEMA,
        "evidence_id": _evidence_id_for_roi(roi_id, "rule_stub"),
        "source_frame_id": source_frame_id,
        "stream_id": None,
        "frame_index": None,
        "timestamp_ms": None,
        "roi_id": roi_id,
        "unit_id": unit_id,
        "source_unit_ref": unit_id,
        "provider": "rule_stub",
        "provider_level": "stub",
        "provider_output_ref": str(Path(stub_root) / "vision_roi_proposal_candidate.json"),
        "label": label,
        "class_id": None,
        "class_name": label,
        "confidence": float(roi_item.get("confidence") if roi_item.get("confidence") is not None else 1.0),
        "bbox_in_unit": [int(v) for v in bbox],
        "bbox_in_frame": [int(v) for v in bbox],
        "polygon_in_frame": roi_item.get("polygon_in_frame"),
        "mask_ref": (roi_item.get("segmentation_stub") or {}).get("mask_ref")
        if isinstance(roi_item.get("segmentation_stub"), dict)
        else None,
        "tracker_id": None,
        "track_id_scope": "none",
        "coordinate_space": str(roi_item.get("coordinate_space") or "frame_pixel"),
        "synthetic": True,
        "stub_provider": True,
        "fact_status": "not_fact",
        "evidence_role": "visual_detection_candidate",
        "source_chain": chain,
    }


def _schema_fit_score(rows: List[Dict[str, Any]]) -> float:
    if not rows:
        return 0.0
    ok = 0
    for row in rows:
        if all(row.get(f) is not None and row.get(f) != "" for f in REQUIRED_EVIDENCE_FIELDS):
            ok += 1
    return round(ok / len(rows), 4)


def _coordinate_fit_score(rows: List[Dict[str, Any]]) -> float:
    if not rows:
        return 0.0
    ok = 0
    for row in rows:
        if str(row.get("coordinate_space") or "") == "frame_pixel" and _valid_bbox(row.get("bbox_in_frame")):
            ok += 1
    return round(ok / len(rows), 4)


def _lineage_fit_score(rows: List[Dict[str, Any]]) -> float:
    if not rows:
        return 0.0
    ok = 0
    for row in rows:
        if (
            row.get("source_frame_id")
            and row.get("roi_id")
            and isinstance(row.get("source_chain"), list)
            and len(row.get("source_chain") or []) > 0
        ):
            ok += 1
    return round(ok / len(rows), 4)


def _governance_fit_score(rows: List[Dict[str, Any]]) -> float:
    if not rows:
        return 0.0
    ok = 0
    for row in rows:
        if (
            row.get("synthetic") is True
            and row.get("stub_provider") is True
            and str(row.get("fact_status") or "") == "not_fact"
            and str(row.get("evidence_role") or "") == "visual_detection_candidate"
        ):
            ok += 1
    return round(ok / len(rows), 4)


def analyze_arm_v0(
    *,
    arm: str,
    roi_candidate: Dict[str, Any],
    converted_rows: List[Dict[str, Any]],
) -> Dict[str, Any]:
    roi_items = roi_candidate.get("roi_items") if isinstance(roi_candidate.get("roi_items"), list) else []
    bbox_valid = sum(1 for it in roi_items if isinstance(it, dict) and _valid_bbox(it.get("bbox_in_frame")))
    coord_spaces = sorted(
        {str(it.get("coordinate_space") or "") for it in roi_items if isinstance(it, dict) and it.get("coordinate_space")}
    )
    source_frame_ok = bool(roi_candidate.get("source_frame_id")) or all(
        isinstance(it, dict) and it.get("source_frame_id") for it in roi_items
    )
    roi_id_ok = all(isinstance(it, dict) and it.get("roi_id") for it in roi_items) if roi_items else False
    proposal_source = str(roi_candidate.get("proposal_source") or "")
    provider_trace = bool(proposal_source) or all(
        isinstance(it, dict) and it.get("proposal_source") for it in roi_items[:3]
    )
    back_ref = bool(roi_candidate.get("source_image_ref")) or bool(
        roi_candidate.get("frame_input_governance_root_ref")
    )
    conversion_ok = len(converted_rows) == len(roi_items) and len(converted_rows) > 0
    if conversion_ok:
        for row in converted_rows:
            if str(row.get("schema_version") or "") != VISION_DETECTION_SCHEMA:
                conversion_ok = False
                break
            if str(row.get("fact_status") or "") != "not_fact":
                conversion_ok = False
                break
    synthetic_ok = all(
        r.get("synthetic") is True and str(r.get("fact_status") or "") == "not_fact" for r in converted_rows
    )
    return {
        "arm": arm,
        "roi_count": len(roi_items),
        "bbox_valid_count": bbox_valid,
        "bbox_coordinate_space": coord_spaces[0] if len(coord_spaces) == 1 else coord_spaces,
        "source_frame_id_present": source_frame_ok,
        "roi_id_present": roi_id_ok,
        "provider_trace_present": provider_trace,
        "coordinate_back_reference_present": back_ref,
        "conversion_to_vision_detection_evidence_ok": conversion_ok,
        "synthetic_not_fact_preserved": synthetic_ok,
        "audit_complete": True,
        "schema_fit_score": _schema_fit_score(converted_rows),
        "coordinate_fit_score": _coordinate_fit_score(converted_rows),
        "lineage_fit_score": _lineage_fit_score(converted_rows),
        "governance_fit_score": _governance_fit_score(converted_rows),
    }


def build_ab_comparison_matrix_v0(
    rule_stub_arm: Dict[str, Any],
    supervision_arm: Dict[str, Any],
) -> Dict[str, Any]:
    dimensions = [
        "roi_count",
        "bbox_valid_count",
        "bbox_coordinate_space",
        "source_frame_id_present",
        "roi_id_present",
        "provider_trace_present",
        "coordinate_back_reference_present",
        "conversion_to_vision_detection_evidence_ok",
        "synthetic_not_fact_preserved",
        "audit_complete",
    ]
    rows = []
    for dim in dimensions:
        rows.append(
            {
                "dimension": dim,
                "rule_stub": rule_stub_arm.get(dim),
                "supervision_synthetic": supervision_arm.get(dim),
                "notes": "",
            }
        )
    winner = "tie"
    rs_gov = float(rule_stub_arm.get("governance_fit_score") or 0)
    sv_gov = float(supervision_arm.get("governance_fit_score") or 0)
    rs_line = float(rule_stub_arm.get("lineage_fit_score") or 0)
    sv_line = float(supervision_arm.get("lineage_fit_score") or 0)
    if sv_gov >= rs_gov and sv_line >= rs_line and supervision_arm.get("conversion_to_vision_detection_evidence_ok"):
        winner = "supervision_synthetic_adapter_structural_fit"
    elif rs_gov > sv_gov and rs_line > sv_line:
        winner = "rule_stub_lineage_preferred"
    return {
        "schema": COMPARISON_SCHEMA,
        "dimensions": dimensions,
        "rows": rows,
        "rule_stub_arm": rule_stub_arm,
        "supervision_synthetic_arm": supervision_arm,
        "structural_winner_hint": winner,
    }


def build_structure_score_report_v0(
    rule_stub_arm: Dict[str, Any],
    supervision_arm: Dict[str, Any],
) -> Dict[str, Any]:
    def avg_score(arm: Dict[str, Any]) -> float:
        parts = [
            float(arm.get("schema_fit_score") or 0),
            float(arm.get("coordinate_fit_score") or 0),
            float(arm.get("lineage_fit_score") or 0),
            float(arm.get("governance_fit_score") or 0),
        ]
        return round(sum(parts) / len(parts), 4) if parts else 0.0

    rs_avg = avg_score(rule_stub_arm)
    sv_avg = avg_score(supervision_arm)
    risk_score = round(max(0.0, 1.0 - min(rs_avg, sv_avg)), 4)
    if sv_avg >= rs_avg and supervision_arm.get("conversion_to_vision_detection_evidence_ok"):
        recommendation = (
            "supervision_synthetic_adapter is a viable evaluation-only adapter candidate for "
            "VisionDetectionEvidence v0; keep gated — no mainline, no real YOLO."
        )
    else:
        recommendation = (
            "rule_stub remains default for ROI lineage in Luna; Supervision adapter useful as "
            "reference-only until gated real-detector phase."
        )
    return {
        "schema": SCORE_SCHEMA,
        "note": "Scores measure structural fit to Luna evidence schema, not detection quality.",
        "rule_stub": {
            "schema_fit_score": rule_stub_arm.get("schema_fit_score"),
            "coordinate_fit_score": rule_stub_arm.get("coordinate_fit_score"),
            "lineage_fit_score": rule_stub_arm.get("lineage_fit_score"),
            "governance_fit_score": rule_stub_arm.get("governance_fit_score"),
            "aggregate_fit_score": rs_avg,
        },
        "supervision_synthetic": {
            "schema_fit_score": supervision_arm.get("schema_fit_score"),
            "coordinate_fit_score": supervision_arm.get("coordinate_fit_score"),
            "lineage_fit_score": supervision_arm.get("lineage_fit_score"),
            "governance_fit_score": supervision_arm.get("governance_fit_score"),
            "aggregate_fit_score": sv_avg,
        },
        "risk_score": risk_score,
        "recommendation": recommendation,
    }


def build_risk_report_v0() -> Dict[str, Any]:
    return {
        "schema": RISK_SCHEMA,
        "supervision_adapter_candidate_only": True,
        "not_luna_core": True,
        "must_not_bypass_frame_input_governance": True,
        "must_not_bypass_vision_provider_input_pack": True,
        "no_midplatform_fact_write": True,
        "no_scene_delta_write": True,
        "no_world_model_write": True,
        "no_navigation_decision": True,
        "no_ai_interpretation": True,
        "synthetic_detections_not_fact": True,
        "real_yolo_supervision_requires_gated_phase": True,
        "narrative": [
            "Supervision synthetic adapter output is geometry/label candidate only.",
            "Do not treat supervision_synthetic_adapter as real detector output.",
            "Real YOLO + Supervision integration must open a separate gated evaluation phase.",
        ],
    }


def build_ab_audit_v0() -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "supervision_ab_test_executed": True,
        "supervision_mainline_invoked": False,
        "yolo_invoked": False,
        "real_detector_invoked": False,
        "vlm_invoked": False,
        "ocr_invoked": False,
        "navigation_decision_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "database_write_invoked": False,
    }


def _load_supervision_probe(experiment_root: Path) -> Dict[str, Any]:
    probe_p = experiment_root / "external_supervision_availability_probe.json"
    if probe_p.is_file():
        raw = _read_json(probe_p)
        if isinstance(raw, dict):
            return raw
    ref_p = experiment_root.parent / "supervision_structure_reference_analysis_smoke_v0"
    summary_p = ref_p / "supervision_structure_reference_summary.json"
    if summary_p.is_file():
        s = _read_json(summary_p)
        if isinstance(s, dict):
            return {
                "supervision_installed": s.get("supervision_installed"),
                "supervision_version": s.get("supervision_version"),
            }
    return {"supervision_installed": False, "supervision_version": None}


def run_supervision_adapter_ab_test_v0(
    *,
    supervision_structure_reference_root: str,
    vision_detection_schema_alignment_root: str,
    rule_stub_roi_root: str,
    external_supervision_experiment_root: str,
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

    sup_ref = Path(supervision_structure_reference_root).resolve()
    schema_root = Path(vision_detection_schema_alignment_root).resolve()
    stub_root = Path(rule_stub_roi_root).resolve()
    exp_root = Path(external_supervision_experiment_root).resolve()

    for label, p in (
        ("supervision_structure_reference_root", sup_ref),
        ("vision_detection_schema_alignment_root", schema_root),
        ("rule_stub_roi_root", stub_root),
        ("external_supervision_experiment_root", exp_root),
    ):
        if not p.is_dir():
            errs.append(f"missing_root:{label}")

    schema_p = schema_root / "vision_detection_evidence_schema_v0.json"
    vision_detection_schema_version = VISION_DETECTION_SCHEMA
    if schema_p.is_file():
        doc = _read_json(schema_p)
        if isinstance(doc, dict) and doc.get("schema_version"):
            vision_detection_schema_version = str(doc.get("schema_version"))
    else:
        errs.append("missing_vision_detection_evidence_schema_v0")

    probe = _load_supervision_probe(exp_root)
    if probe.get("supervision_installed") is not True:
        errs.append("supervision_not_installed")

    stub_summary_p = stub_root / "vision_roi_proposal_stub_summary.json"
    input_units_count = 0
    rule_stub_roi_count = 0
    if stub_summary_p.is_file():
        ss = _read_json(stub_summary_p)
        if isinstance(ss, dict):
            input_units_count = int(ss.get("input_units_count") or 0)
            rule_stub_roi_count = int(ss.get("roi_items_count") or 0)

    stub_candidate_p = stub_root / "vision_roi_proposal_candidate.json"
    rule_candidate: Dict[str, Any] = {}
    if stub_candidate_p.is_file():
        raw = _read_json(stub_candidate_p)
        if isinstance(raw, dict):
            rule_candidate = raw
            items = raw.get("roi_items") if isinstance(raw.get("roi_items"), list) else []
            if not rule_stub_roi_count:
                rule_stub_roi_count = len(items)
        else:
            errs.append("rule_stub_candidate_invalid")
    else:
        errs.append("missing_rule_stub_vision_roi_proposal_candidate")

    sup_candidate_p = exp_root / "vision_roi_proposal_candidate.json"
    sup_candidate: Dict[str, Any] = {}
    if sup_candidate_p.is_file():
        raw = _read_json(sup_candidate_p)
        if isinstance(raw, dict):
            sup_candidate = raw
        else:
            errs.append("supervision_candidate_invalid")
    else:
        errs.append("missing_supervision_vision_roi_proposal_candidate")

    sup_roi_items = sup_candidate.get("roi_items") if isinstance(sup_candidate.get("roi_items"), list) else []
    supervision_roi_count = len(sup_roi_items)
    if supervision_roi_count <= 0:
        errs.append("supervision_roi_count_zero")
    if rule_stub_roi_count <= 0:
        errs.append("rule_stub_roi_count_zero")

    rule_converted: List[Dict[str, Any]] = []
    rule_items = rule_candidate.get("roi_items") if isinstance(rule_candidate.get("roi_items"), list) else []
    for i, it in enumerate(rule_items, start=1):
        if isinstance(it, dict):
            rule_converted.append(
                rule_stub_roi_to_vision_detection_evidence_v0(
                    it, candidate=rule_candidate, stub_root=str(stub_root), index=i
                )
            )

    sup_converted: List[Dict[str, Any]] = []
    for i, it in enumerate(sup_roi_items, start=1):
        if isinstance(it, dict):
            sup_converted.append(
                supervision_roi_to_vision_detection_evidence_v0(
                    it, candidate=sup_candidate, experiment_root=str(exp_root), index=i
                )
            )

    fixture = {
        "schema": FIXTURE_SCHEMA,
        "vision_detection_schema_version": vision_detection_schema_version,
        "provider": "supervision_synthetic_adapter",
        "not_real_detector_output": True,
        "item_count": len(sup_converted),
        "items": sup_converted,
    }

    rule_arm = analyze_arm_v0(arm="rule_stub", roi_candidate=rule_candidate, converted_rows=rule_converted)
    sup_arm = analyze_arm_v0(
        arm="supervision_synthetic_adapter", roi_candidate=sup_candidate, converted_rows=sup_converted
    )
    comparison = build_ab_comparison_matrix_v0(rule_arm, sup_arm)
    score_report = build_structure_score_report_v0(rule_arm, sup_arm)
    risk = build_risk_report_v0()
    audit = build_ab_audit_v0()

    for it in sup_converted:
        if str(it.get("provider") or "") != "supervision_synthetic_adapter":
            errs.append("fixture_provider_must_be_supervision_synthetic_adapter")
        if it.get("synthetic") is not True:
            errs.append("fixture_synthetic_must_be_true")
        if str(it.get("fact_status") or "") != "not_fact":
            errs.append("fixture_fact_status_must_be_not_fact")

    input_summary = {
        "schema": AB_INPUT_SCHEMA,
        "supervision_structure_reference_root": str(sup_ref),
        "vision_detection_schema_alignment_root": str(schema_root),
        "rule_stub_roi_root": str(stub_root),
        "external_supervision_experiment_root": str(exp_root),
        "rule_stub_roi_items_count": rule_stub_roi_count,
        "rule_stub_input_units_count": input_units_count,
        "supervision_roi_items_count": supervision_roi_count,
        "supervision_installed": bool(probe.get("supervision_installed")),
        "supervision_version": probe.get("supervision_version"),
        "vision_detection_schema_version": vision_detection_schema_version,
        "rule_stub_proposal_source": rule_candidate.get("proposal_source"),
        "supervision_proposal_source": sup_candidate.get("proposal_source"),
    }

    summary = {
        "schema_version": AB_SUMMARY_SCHEMA,
        "phase": "Phase-Vision-Supervision-Adapter-AB-Test-001",
        "supervision_structure_reference_root": str(sup_ref),
        "vision_detection_schema_alignment_root": str(schema_root),
        "rule_stub_roi_root": str(stub_root),
        "external_supervision_experiment_root": str(exp_root),
        "rule_stub_roi_count": rule_stub_roi_count,
        "rule_stub_input_units_count": input_units_count,
        "supervision_roi_count": supervision_roi_count,
        "supervision_installed": bool(probe.get("supervision_installed")),
        "supervision_version": probe.get("supervision_version"),
        "vision_detection_schema_version": vision_detection_schema_version,
        "supervision_fixture_item_count": len(sup_converted),
        "structural_winner_hint": comparison.get("structural_winner_hint"),
        "recommendation": score_report.get("recommendation"),
        "errors": list(errs),
    }

    return summary, input_summary, fixture, comparison, score_report, risk, audit, errs
