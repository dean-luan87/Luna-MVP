# -*- coding: utf-8 -*-
"""Read-only replay consumer for OCR ingest event payload (simulated bus).

Phase-OCR-Ingest-to-Product-Bus-ReadOnly-Replay-001 — no writes, no AI, no OCR provider.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPLAY_CONSUMER_VIEW_SCHEMA = "ocr_ingest_readonly_replay_consumer_view_v0"


def consume_ocr_ingest_readonly_event_payload_v0(
    payload: Dict[str, Any],
) -> Tuple[Dict[str, Any], List[str]]:
    """
    Validate payload fields and ``geometry_matrix_ref`` file; emit ``replay_consumer_view``.

    Does not mutate external systems.
    """
    errs: List[str] = []

    if str(payload.get("schema_version") or "") != "ocr_ingest_readonly_event_payload_v0":
        errs.append("payload_schema_version_mismatch")

    cid = str(payload.get("candidate_id") or "").strip()
    if not cid:
        errs.append("payload_missing_candidate_id")

    evc = int(payload.get("evidence_count") or 0)
    if evc < 1:
        errs.append("payload_evidence_count_lt_1")

    tj = str(payload.get("text_joined") or "").strip()
    if not tj:
        errs.append("payload_text_joined_empty")

    gref = str(payload.get("geometry_matrix_ref") or "").strip()
    if not gref:
        errs.append("payload_missing_geometry_matrix_ref")
    else:
        gp = Path(gref)
        if not gp.is_file():
            errs.append("geometry_matrix_ref_not_readable_file")
        else:
            try:
                raw = json.loads(gp.read_text(encoding="utf-8"))
            except Exception:
                errs.append("geometry_matrix_ref_invalid_json")
                raw = None
            if raw is not None and not isinstance(raw, list):
                errs.append("geometry_matrix_not_array")

    ebr = payload.get("evidence_by_roi")
    if not isinstance(ebr, dict) or not ebr:
        errs.append("payload_evidence_by_roi_empty")

    geom_rows = 0
    if gref and Path(gref).is_file():
        try:
            raw = json.loads(Path(gref).read_text(encoding="utf-8"))
            if isinstance(raw, list):
                geom_rows = len(raw)
        except Exception:
            pass

    scs = payload.get("source_chain_summary") if isinstance(payload.get("source_chain_summary"), dict) else {}
    chain_n = int(scs.get("chain_item_count") or 0) if isinstance(scs.get("chain_item_count"), (int, float)) else None
    if chain_n is None and isinstance(scs.get("chain"), list):
        chain_n = len(scs["chain"])

    view: Dict[str, Any] = {
        "schema_version": REPLAY_CONSUMER_VIEW_SCHEMA,
        "consumer_id": "readonly_replay_consumer_v0",
        "candidate_id_observed": cid,
        "evidence_count_observed": evc,
        "text_joined_observed": tj,
        "geometry_matrix_ref_observed": gref,
        "geometry_row_count": geom_rows,
        "evidence_by_roi_keys": sorted(ebr.keys()) if isinstance(ebr, dict) else [],
        "provider_summary_present": isinstance(payload.get("provider_summary"), dict) and bool(payload.get("provider_summary")),
        "source_chain_chain_item_count": chain_n,
        "payload_scope_observed": str(payload.get("payload_scope") or ""),
        "event_id_observed": str(payload.get("event_id") or ""),
        "event_type_observed": str(payload.get("event_type") or ""),
        "validation_errors": list(errs),
    }
    return view, errs
