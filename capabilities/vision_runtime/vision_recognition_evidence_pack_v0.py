# -*- coding: utf-8 -*-
"""VisionRecognitionEvidencePack v0 — stub / synthetic candidates only, not fact."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Tuple


EVIDENCE_PACK_SCHEMA = "vision_recognition_evidence_pack_v0"


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _index_matrix_rows_by_unit(matrix: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for row in matrix.get("rows") or []:
        if not isinstance(row, dict):
            continue
        uid = str(row.get("unit_id") or "")
        if uid:
            out[uid] = row
    return out


def _index_pack_units_by_ids(packs: List[Dict[str, Any]]) -> Dict[Tuple[str, str], Dict[str, Any]]:
    """(pack_id, unit_id) -> unit dict with coordinate_transform etc."""
    out: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for pack in packs:
        pid = str(pack.get("pack_id") or "")
        for u in pack.get("input_units") or []:
            if not isinstance(u, dict):
                continue
            uid = str(u.get("unit_id") or "")
            if pid and uid:
                out[(pid, uid)] = u
    return out


def _collect_packs(bundle: Dict[str, Any]) -> List[Dict[str, Any]]:
    if isinstance(bundle.get("packs"), list):
        return [p for p in bundle["packs"] if isinstance(p, dict)]
    if bundle.get("schema_version") == "vision_provider_input_pack_v0" and isinstance(bundle.get("input_units"), list):
        return [bundle]
    return []


def build_vision_recognition_evidence_pack_from_adapter_selection_v0(
    adapter_selection_root: Path,
) -> Dict[str, Any]:
    """
    Load adapter selection artifacts + input pack (via summary.roi root).

    Returns keys: evidence_pack, evidence_matrix, provider_summary, audit, summary.
    """
    root = adapter_selection_root.resolve()
    stub_path = root / "vision_provider_stub_result.json"
    mx_path = root / "vision_recognition_candidate_matrix.json"
    sel_path = root / "vision_provider_selection_report.json"
    aud_sel_path = root / "vision_recognition_adapter_selection_audit_report.json"
    sum_path = root / "vision_recognition_adapter_selection_summary.json"

    for p in (stub_path, mx_path, sel_path, aud_sel_path, sum_path):
        if not p.is_file():
            raise FileNotFoundError(p)

    stub = _read_json(stub_path)
    matrix = _read_json(mx_path)
    selection = _read_json(sel_path)
    _read_json(aud_sel_path)
    adapter_summary = _read_json(sum_path)

    roi_root_raw = str(adapter_summary.get("vision_roi_proposal_root") or "").strip()
    if not roi_root_raw:
        raise ValueError("vision_recognition_adapter_selection_summary.json: missing vision_roi_proposal_root")
    roi_root = Path(roi_root_raw).resolve()
    pack_path = roi_root / "vision_provider_input_pack.json"
    if not pack_path.is_file():
        raise FileNotFoundError(pack_path)
    pack_bundle = _read_json(pack_path)
    packs = _collect_packs(pack_bundle)
    unit_by_pack_unit = _index_pack_units_by_ids(packs)
    row_by_unit = _index_matrix_rows_by_unit(matrix)

    provider_trace = {
        "provider": str(selection.get("selected_provider") or "vision_stub"),
        "provider_level": str(selection.get("selected_provider_level") or "stub"),
        "real_provider_invoked": bool(selection.get("real_provider_invoked")),
    }

    items_out: List[Dict[str, Any]] = []
    matrix_rows: List[Dict[str, Any]] = []

    for it in stub.get("items") or []:
        if not isinstance(it, dict):
            continue
        uid = str(it.get("unit_id") or "")
        pid = str(it.get("pack_id") or "")
        row = row_by_unit.get(uid) or {}
        sf = str(row.get("source_frame_id") or "")
        pack_unit = unit_by_pack_unit.get((pid, uid)) if pid and uid else None
        ct = (pack_unit or {}).get("coordinate_transform") if isinstance(pack_unit, dict) else None
        crop_ref = str(row.get("crop_image_ref") or "")

        eid = f"evidence_{uuid.uuid4().hex[:16]}"
        bbox_f = it.get("bbox_in_frame")
        bbox_u = it.get("bbox_in_unit")
        if not isinstance(bbox_f, list) or len(bbox_f) != 4:
            bbox_f = None
        if not isinstance(bbox_u, list) or len(bbox_u) != 4:
            bbox_u = None

        item = {
            "evidence_id": eid,
            "source_frame_id": sf,
            "unit_id": uid,
            "roi_id": str(it.get("roi_id") or ""),
            "source_unit_ref": str(it.get("source_unit_ref") or uid),
            "label": str(it.get("label") or "stub_object"),
            "confidence": float(it.get("confidence") or 0.0),
            "bbox_in_unit": bbox_u if bbox_u is not None else [0, 0, 1, 1],
            "bbox_in_frame": bbox_f if bbox_f is not None else [0, 0, 0, 0],
            "synthetic": True,
            "stub_provider": True,
            "fact_status": "not_fact",
            "coordinate_space": "frame_pixel",
        }
        if crop_ref:
            item["crop_image_ref"] = crop_ref
        if isinstance(ct, dict):
            item["coordinate_transform"] = ct
        items_out.append(item)

        matrix_rows.append(
            {
                "evidence_id": eid,
                "source_frame_id": sf,
                "roi_id": str(it.get("roi_id") or ""),
                "unit_id": uid,
                "label": item["label"],
                "confidence": item["confidence"],
                "synthetic": True,
                "stub_provider": True,
                "fact_status": "not_fact",
                "bbox_in_frame": item["bbox_in_frame"],
                "source_unit_ref": item["source_unit_ref"],
            }
        )

    pack_id = f"evpack_{uuid.uuid4().hex[:16]}"
    source_chain = [
        f"vision_provider_input_pack_ref:{pack_path}",
        f"vision_provider_selection_report_ref:{sel_path}",
        f"vision_stub_result_ref:{stub_path}",
        "vision_recognition_evidence_pack_built",
    ]

    evidence_pack = {
        "schema_version": EVIDENCE_PACK_SCHEMA,
        "pack_id": pack_id,
        "source_phase": "Vision-Lightweight-Recognition-Adapter-Selection-001",
        "provider_trace": provider_trace,
        "evidence_scope": "synthetic_stub_candidate",
        "fact_status": "not_fact",
        "items": items_out,
        "source_chain": source_chain,
    }

    provider_summary = {
        "schema": "vision_recognition_provider_summary_v0",
        "selected_provider": selection.get("selected_provider"),
        "selected_provider_level": selection.get("selected_provider_level"),
        "real_provider_invoked": selection.get("real_provider_invoked"),
        "provider_selection_reason_codes": list(selection.get("provider_selection_reason_codes") or []),
    }

    audit = {
        "schema": "vision_recognition_evidence_audit_v0",
        "vision_evidence_pack_generated": True,
        "real_provider_invoked": False,
        "yolo_invoked": False,
        "supervision_mainline_invoked": False,
        "vlm_invoked": False,
        "ocr_invoked": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
    }

    summary = {
        "phase": "Phase-Vision-Recognition-Evidence-Pack-Stub-001",
        "schema": "vision_recognition_evidence_pack_summary_v0",
        "vision_adapter_selection_root": str(root),
        "vision_roi_proposal_root": str(roi_root),
        "evidence_items_count": len(items_out),
        "fact_status_global": "not_fact",
        "evidence_scope": "synthetic_stub_candidate",
    }

    evidence_matrix = {"schema": "vision_recognition_evidence_matrix_v0", "rows": matrix_rows}

    return {
        "evidence_pack": evidence_pack,
        "evidence_matrix": evidence_matrix,
        "provider_summary": provider_summary,
        "audit": audit,
        "summary": summary,
    }
