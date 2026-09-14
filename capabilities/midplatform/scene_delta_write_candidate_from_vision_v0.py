# -*- coding: utf-8 -*-
"""Scene Delta write candidate from Vision read-only ingest / event payload (stub).

Phase-MidPlatform-Scene-Delta-Write-Candidate-From-Vision-Ingest-Stub-001 — candidate JSON only;
no Scene Delta write, no fact layer, no WorldModel, no AI interpretation, no navigation.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Tuple

WRITE_CANDIDATE_SCHEMA = "scene_delta_write_candidate_from_vision_v0"
WRITE_AUDIT_SCHEMA = "scene_delta_write_candidate_from_vision_audit_v0"

FORBIDDEN_KEY_FRAGMENTS: Tuple[str, ...] = (
    "semantic_summary",
    "inferred_meaning",
    "object_meaning",
    "obstacle_decision",
    "navigation_action",
    "risk_level",
    "user_facing_explanation",
    "confirmed_object",
    "confirmed_fact",
    "navigation_obstacle",
    "world_model_fact",
    "scene_delta_written",
    "risk_decision",
)


def collect_forbidden_keys_in_object_vision_v0(obj: Any, prefix: str = "$") -> List[str]:
    hits: List[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            ks = str(k)
            if ks in FORBIDDEN_KEY_FRAGMENTS:
                hits.append(f"{prefix}.{ks}")
            hits.extend(collect_forbidden_keys_in_object_vision_v0(v, f"{prefix}.{ks}"))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits.extend(collect_forbidden_keys_in_object_vision_v0(v, f"{prefix}[{i}]"))
    return hits


def build_scene_delta_write_candidate_gate_stub_vision_v0() -> Dict[str, Any]:
    return {
        "schema": "scene_delta_write_candidate_vision_gate_stub_v0",
        "gate_required": True,
        "gate_status": "not_evaluated",
        "gate_reason_codes": [
            "vision_evidence_requires_scene_delta_gate",
            "stub_evidence_is_not_fact",
            "no_ai_interpretation",
            "no_navigation_decision",
            "no_world_fact_write",
        ],
    }


def build_scene_delta_write_candidate_vision_audit_v0() -> Dict[str, Any]:
    return {
        "schema": WRITE_AUDIT_SCHEMA,
        "scene_delta_write_candidate_generated": True,
        "scene_delta_written": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "database_write_invoked": False,
        "external_bus_invoked": False,
        "real_vision_provider_invoked": False,
        "yolo_invoked": False,
        "supervision_mainline_invoked": False,
        "vlm_invoked": False,
        "ocr_invoked": False,
        "external_bus_invoked": False,
    }


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build_evidence_items_from_vision_ingest_matrix_v0(
    rows: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[str]]:
    errs: List[str] = []
    items: List[Dict[str, Any]] = []
    for idx, row in enumerate(rows):
        if not isinstance(row, dict):
            errs.append(f"row_not_object_at_{idx}")
            continue
        eid = str(row.get("evidence_id") or "").strip()
        if not eid:
            errs.append(f"missing_evidence_id_at_{idx}")
        sf = str(row.get("source_frame_id") or "").strip()
        if not sf:
            errs.append(f"missing_source_frame_id_at_{idx}")
        rid = str(row.get("roi_id") or "").strip()
        rtype = str(row.get("roi_type") or "").strip()
        uid = str(row.get("unit_id") or "").strip()
        if not uid:
            uid = f"vision_stub_synthetic_unit::{eid}" if eid else f"vision_stub_synthetic_unit::idx_{idx}"
        sur = str(row.get("source_unit_ref") or "").strip() or uid
        bb = row.get("bbox_in_frame")
        if not isinstance(bb, list) or len(bb) != 4:
            errs.append(f"missing_bbox_in_frame_at_{idx}")
        if row.get("synthetic") is not True:
            errs.append(f"synthetic_not_true_at_{idx}")
        if row.get("stub_provider") is not True:
            errs.append(f"stub_provider_not_true_at_{idx}")
        if str(row.get("fact_status") or "") != "not_fact":
            errs.append(f"fact_status_not_not_fact_at_{idx}")
        items.append(
            {
                "evidence_id": eid,
                "source_frame_id": sf,
                "roi_id": rid,
                "roi_type": rtype or "unknown_roi_type",
                "unit_id": uid,
                "source_unit_ref": sur,
                "label": str(row.get("label") or "stub_object"),
                "confidence": float(row.get("confidence") or 0.0),
                "bbox_in_frame": bb if isinstance(bb, list) and len(bb) == 4 else [0, 0, 0, 0],
                "provider": "vision_stub",
                "synthetic": True,
                "stub_provider": True,
                "evidence_role": "observed_visual_candidate",
                "fact_status": "not_fact",
                "scene_delta_disposition": "scene_delta_candidate_later",
            }
        )
    return items, errs


def build_scene_delta_write_candidate_vision_evidence_matrix_v0(
    items: List[Dict[str, Any]],
) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for it in items:
        rows.append(
            {
                "evidence_id": it.get("evidence_id"),
                "source_frame_id": it.get("source_frame_id"),
                "roi_id": it.get("roi_id"),
                "roi_type": it.get("roi_type"),
                "unit_id": it.get("unit_id"),
                "label": it.get("label"),
                "confidence": it.get("confidence"),
                "synthetic": it.get("synthetic"),
                "stub_provider": it.get("stub_provider"),
                "fact_status": it.get("fact_status"),
                "bbox_in_frame": it.get("bbox_in_frame"),
                "scene_delta_disposition": it.get("scene_delta_disposition"),
            }
        )
    return {"schema": "scene_delta_write_candidate_vision_evidence_matrix_v0", "rows": rows}


def build_scene_delta_write_candidate_from_vision_v0(
    *,
    event_payload: Dict[str, Any],
    ingest_matrix_rows: List[Dict[str, Any]],
    replay_consumer_view: Dict[str, Any],
) -> Tuple[Dict[str, Any], List[str]]:
    errs: List[str] = []

    eid_evt = str(event_payload.get("event_id") or "").strip()
    cid = str(event_payload.get("candidate_id") or "").strip()
    if not eid_evt:
        errs.append("payload_missing_event_id")
    if not cid:
        errs.append("payload_missing_candidate_id")

    if str(replay_consumer_view.get("candidate_id") or "") != cid:
        errs.append("replay_view_candidate_id_mismatch")

    val_errs = replay_consumer_view.get("validation_errors")
    if not isinstance(val_errs, list) or len(val_errs) != 0:
        errs.append("replay_consumer_validation_errors_non_empty")

    evc_payload = int(event_payload.get("evidence_count") or 0)
    items, i_errs = build_evidence_items_from_vision_ingest_matrix_v0(ingest_matrix_rows)
    errs.extend(i_errs)

    if len(items) != evc_payload:
        errs.append("evidence_items_count_mismatch_payload_evidence_count")

    fs = event_payload.get("fact_status_summary") or {}
    syn = event_payload.get("synthetic_summary") or {}
    if int(fs.get("not_fact") or 0) != evc_payload:
        errs.append("payload_fact_status_mismatch")
    if int(syn.get("synthetic_count") or 0) != evc_payload:
        errs.append("payload_synthetic_mismatch")

    scs = event_payload.get("source_chain_summary")
    if not isinstance(scs, dict):
        errs.append("payload_source_chain_summary_missing")

    candidate: Dict[str, Any] = {
        "schema_version": WRITE_CANDIDATE_SCHEMA,
        "candidate_id": f"sd_vision_candidate_{uuid.uuid4().hex}",
        "source_event_id": eid_evt,
        "source_ingest_candidate_id": cid,
        "source_type": "vision_recognition_evidence",
        "candidate_scope": "write_candidate_only",
        "write_allowed": False,
        "requires_gate_approval": True,
        "evidence_count": evc_payload,
        "provider": "vision_stub",
        "provider_level": "stub",
        "fact_status_summary": dict(fs) if isinstance(fs, dict) else {},
        "synthetic_summary": dict(syn) if isinstance(syn, dict) else {},
        "evidence_items": items,
        "spatial_reference": {
            "geometry_source": "vision_bbox_in_frame",
            "coordinate_space": "frame_pixel",
        },
        "source_chain_summary": scs if isinstance(scs, dict) else {},
        "forbidden_actions": {
            "write_scene_delta": True,
            "write_midplatform_fact": True,
            "write_world_model": True,
            "invoke_ai_interpretation": True,
            "invoke_navigation_decision": True,
            "invoke_real_vision_provider": True,
        },
    }
    bad = collect_forbidden_keys_in_object_vision_v0(candidate)
    if bad:
        errs.extend([f"forbidden_key_in_candidate:{b}" for b in bad])

    return candidate, errs


def load_vision_ingest_matrix_rows_v0(ingest_matrix_ref: str) -> List[Dict[str, Any]]:
    p = Path(ingest_matrix_ref)
    if not p.is_file():
        raise FileNotFoundError(p)
    data = _read_json(p)
    rows = data.get("rows") if isinstance(data.get("rows"), list) else []
    return [r for r in rows if isinstance(r, dict)]
