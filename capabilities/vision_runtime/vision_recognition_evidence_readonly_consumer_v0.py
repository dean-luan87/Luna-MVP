# -*- coding: utf-8 -*-
"""Read-only consumer for vision_recognition_evidence_pack_v0 (no writes, no facts)."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple


CONSUMER_VIEW_SCHEMA = "vision_recognition_evidence_readonly_consumer_view_v0"

KNOWN_ROI_TYPE_SUFFIXES: Tuple[str, ...] = (
    "center_roi",
    "ground_roi",
    "upper_sign_roi",
    "left_roi",
    "right_roi",
)

FORBIDDEN_OUTPUT_KEYS: Set[str] = {
    "confirmed_object",
    "confirmed_fact",
    "navigation_action",
    "scene_delta_candidate",
    "world_model_candidate",
    "ai_interpretation",
}


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def roi_type_from_roi_id_v0(roi_id: str) -> str:
    rid = str(roi_id or "")
    for suf in KNOWN_ROI_TYPE_SUFFIXES:
        if rid.endswith("_" + suf):
            return suf
    return "unknown_roi_type"


def _assert_no_forbidden_keys(obj: Any, path: str = "$") -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            ks = str(k)
            if ks in FORBIDDEN_OUTPUT_KEYS:
                raise ValueError(f"forbidden_output_key:{path}.{ks}")
            _assert_no_forbidden_keys(v, f"{path}.{ks}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            _assert_no_forbidden_keys(v, f"{path}[{i}]")


def run_vision_recognition_evidence_readonly_consumer_v0(
    evidence_pack_root: Path,
    *,
    pack_basename: str = "vision_recognition_evidence_pack.json",
    matrix_basename: str = "vision_recognition_evidence_matrix.json",
    provider_basename: str = "vision_recognition_provider_summary.json",
    audit_basename: str = "vision_recognition_evidence_audit_report.json",
    consumer_id: str = "vision_recognition_readonly_consumer_v0",
    phase_label: str = "Phase-Vision-Recognition-Evidence-ReadOnly-Consumer-001",
    summary_schema: str = "vision_recognition_evidence_readonly_consumer_summary_v0",
) -> Dict[str, Any]:
    root = evidence_pack_root.resolve()
    pack_path = root / pack_basename
    mx_path = root / matrix_basename
    prov_path = root / provider_basename
    aud_in_path = root / audit_basename

    for p in (pack_path, mx_path, prov_path, aud_in_path):
        if not p.is_file():
            raise FileNotFoundError(p)

    pack = _read_json(pack_path)
    matrix = _read_json(mx_path)
    provider = _read_json(prov_path)
    _ = _read_json(aud_in_path)

    if pack.get("schema_version") != "vision_recognition_evidence_pack_v0":
        raise ValueError("unexpected evidence pack schema_version")

    items = pack.get("items") or []
    if not isinstance(items, list):
        raise ValueError("evidence pack items must be a list")

    n = len(items)
    pt = pack.get("provider_trace") or {}
    prov_name = str(pt.get("provider") or "")
    prov_level = str(pt.get("provider_level") or "")

    fact_status_counter: Counter = Counter()
    label_counter: Counter = Counter()
    synthetic_count = 0
    stub_provider_count = 0
    real_detector_count = 0
    bbox_ok = 0

    by_frame: Dict[str, Dict[str, Any]] = {}
    by_roi_type: Counter = Counter()

    for it in items:
        if not isinstance(it, dict):
            continue
        fs = str(it.get("fact_status") or "unknown")
        fact_status_counter[fs] += 1
        label_counter[str(it.get("label") or "")] += 1
        if it.get("synthetic") is True:
            synthetic_count += 1
        if it.get("stub_provider") is True:
            stub_provider_count += 1
        if it.get("synthetic") is not True and it.get("stub_provider") is not True:
            real_detector_count += 1
        bb = it.get("bbox_in_frame")
        if isinstance(bb, list) and len(bb) == 4:
            bbox_ok += 1

        fid = str(it.get("source_frame_id") or "")
        if fid:
            slot = by_frame.setdefault(fid, {"evidence_count": 0, "evidence_ids": []})
            slot["evidence_count"] += 1
            eid = str(it.get("evidence_id") or "")
            if eid:
                slot["evidence_ids"].append(eid)

        rt = roi_type_from_roi_id_v0(str(it.get("roi_id") or ""))
        by_roi_type[rt] += 1

    source_chain = pack.get("source_chain")
    if not isinstance(source_chain, list):
        source_chain = []

    source_chain_summary = {
        "schema": "vision_recognition_source_chain_summary_consumer_v0",
        "evidence_pack_id": str(pack.get("pack_id") or ""),
        "steps": list(source_chain),
        "step_count": len(source_chain),
    }

    geometry_summary_obj = {
        "schema": "vision_recognition_evidence_geometry_summary_v0",
        "bbox_in_frame_count": bbox_ok,
        "evidence_items_total": n,
    }

    detector_mode = str(pt.get("detector_mode") or provider.get("detector_mode") or "")

    consumer_view = {
        "schema_version": CONSUMER_VIEW_SCHEMA,
        "consumer_id": consumer_id,
        "source_pack_id": str(pack.get("pack_id") or ""),
        "evidence_count_observed": n,
        "provider": prov_name,
        "provider_level": prov_level,
        "fact_status_summary": dict(fact_status_counter),
        "synthetic_summary": {
            "synthetic_count": synthetic_count,
            "stub_provider_count": stub_provider_count,
        },
        "real_detector_summary": {
            "real_detector_count": real_detector_count,
            "detector_mode": detector_mode,
        },
        "evidence_by_frame": by_frame,
        "evidence_by_roi_type": dict(by_roi_type),
        "label_summary": dict(label_counter),
        "geometry_summary": {"bbox_in_frame_count": bbox_ok},
        "source_chain_summary": source_chain_summary,
    }

    _assert_no_forbidden_keys(consumer_view)

    frame_rows: List[Dict[str, Any]] = []
    for fid, data in sorted(by_frame.items()):
        frame_rows.append(
            {
                "source_frame_id": fid,
                "evidence_count": int(data.get("evidence_count") or 0),
                "evidence_ids": list(data.get("evidence_ids") or []),
            }
        )

    roi_rows: List[Dict[str, Any]] = []
    for rt, c in sorted(by_roi_type.items()):
        roi_rows.append({"roi_type": rt, "evidence_count": int(c)})

    matrix_readonly = {
        "schema": "vision_recognition_evidence_matrix_readonly_pass_v0",
        "row_count": len(matrix.get("rows") or []),
        "columns_observed": [
            "evidence_id",
            "source_frame_id",
            "roi_id",
            "unit_id",
            "label",
            "confidence",
            "bbox_in_frame",
            "source_unit_ref",
            "synthetic",
            "stub_provider",
            "fact_status",
        ],
    }

    audit = {
        "schema": "vision_recognition_evidence_readonly_consumer_audit_v0",
        "vision_evidence_readonly_consumer_executed": True,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "yolo_invoked": False,
        "supervision_mainline_invoked": False,
        "vlm_invoked": False,
        "ocr_invoked": False,
    }

    summary = {
        "phase": phase_label,
        "schema": summary_schema,
        "vision_recognition_evidence_pack_root": str(root),
        "evidence_count_observed": n,
        "consumer_id": consumer_id,
        "matrix_rows_read": int(matrix_readonly["row_count"]),
    }

    _assert_no_forbidden_keys(
        {
            "summary": summary,
            "consumer_view": consumer_view,
            "by_frame_matrix": frame_rows,
            "by_roi_matrix": roi_rows,
            "geometry_summary": geometry_summary_obj,
            "audit": audit,
        }
    )

    return {
        "summary": summary,
        "consumer_view": consumer_view,
        "by_frame_matrix": {"schema": "vision_recognition_evidence_by_frame_matrix_v0", "rows": frame_rows},
        "by_roi_matrix": {"schema": "vision_recognition_evidence_by_roi_matrix_v0", "rows": roi_rows},
        "geometry_summary": geometry_summary_obj,
        "matrix_read_meta": matrix_readonly,
        "provider_summary_echo": provider,
        "audit": audit,
    }
