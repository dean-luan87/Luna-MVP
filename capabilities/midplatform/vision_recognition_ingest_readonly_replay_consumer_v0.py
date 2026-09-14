# -*- coding: utf-8 -*-
"""Read-only replay consumer for Vision ingest event payload (simulated bus).

Phase-Vision-Ingest-to-Product-Bus-ReadOnly-Replay-001 — no writes, no AI, no real vision.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPLAY_CONSUMER_VIEW_SCHEMA = "vision_recognition_readonly_replay_consumer_view_v0"


def consume_vision_recognition_ingest_readonly_event_payload_v0(
    payload: Dict[str, Any],
) -> Tuple[Dict[str, Any], List[str]]:
    """Validate payload; optionally validate ``ingest_matrix_ref`` JSON; emit replay consumer view."""
    errs: List[str] = []

    if str(payload.get("schema_version") or "") != "vision_recognition_ingest_readonly_event_payload_v0":
        errs.append("payload_schema_version_mismatch")

    if str(payload.get("payload_scope") or "") != "read_only_replay":
        errs.append("payload_scope_not_read_only_replay")

    cid = str(payload.get("candidate_id") or "").strip()
    if not cid:
        errs.append("payload_missing_candidate_id")

    src_ref = str(payload.get("source_candidate_ref") or "").strip()
    if not src_ref:
        errs.append("payload_missing_source_candidate_ref")

    evc = int(payload.get("evidence_count") or 0)
    if evc < 1:
        errs.append("payload_evidence_count_lt_1")

    prov = str(payload.get("provider") or "")
    pl = str(payload.get("provider_level") or "")
    if prov != "vision_stub":
        errs.append("payload_provider_not_vision_stub")
    if pl != "stub":
        errs.append("payload_provider_level_not_stub")

    fs = payload.get("fact_status_summary") or {}
    if int(fs.get("not_fact") or 0) != evc:
        errs.append("payload_fact_status_not_fact_mismatch")

    syn = payload.get("synthetic_summary") or {}
    if int(syn.get("synthetic_count") or 0) != evc:
        errs.append("payload_synthetic_count_mismatch")
    if int(syn.get("stub_provider_count") or 0) != evc:
        errs.append("payload_stub_provider_count_mismatch")

    by_f = payload.get("evidence_by_frame")
    if not isinstance(by_f, dict) or not by_f:
        errs.append("payload_evidence_by_frame_empty")

    by_r = payload.get("evidence_by_roi_type")
    if not isinstance(by_r, dict) or not by_r:
        errs.append("payload_evidence_by_roi_type_empty")

    geom = payload.get("geometry_summary")
    if not isinstance(geom, dict) or not geom:
        errs.append("payload_geometry_summary_empty")

    mref = str(payload.get("ingest_matrix_ref") or "").strip()
    matrix_rows = 0
    if not mref:
        errs.append("payload_missing_ingest_matrix_ref")
    else:
        mp = Path(mref)
        if not mp.is_file():
            errs.append("ingest_matrix_ref_not_readable_file")
        else:
            try:
                raw = json.loads(mp.read_text(encoding="utf-8"))
            except Exception:
                errs.append("ingest_matrix_ref_invalid_json")
                raw = None
            if raw is not None:
                rows = raw.get("rows") if isinstance(raw.get("rows"), list) else []
                matrix_rows = len(rows)
                if matrix_rows != evc:
                    errs.append("ingest_matrix_row_count_mismatch_evidence_count")

    frame_keys = sorted(by_f.keys()) if isinstance(by_f, dict) else []
    roi_keys = sorted(by_r.keys()) if isinstance(by_r, dict) else []

    view: Dict[str, Any] = {
        "schema_version": REPLAY_CONSUMER_VIEW_SCHEMA,
        "consumer_id": "vision_readonly_replay_consumer_v0",
        "source_event_id": str(payload.get("event_id") or ""),
        "candidate_id": cid,
        "evidence_count_observed": evc,
        "provider_observed": prov,
        "provider_level_observed": pl,
        "fact_status_summary_observed": dict(fs) if isinstance(fs, dict) else {},
        "synthetic_summary_observed": dict(syn) if isinstance(syn, dict) else {},
        "evidence_by_frame_keys": frame_keys,
        "evidence_by_roi_type_keys": roi_keys,
        "ingest_matrix_row_count": matrix_rows,
        "validation_errors": list(errs),
    }
    return view, errs
