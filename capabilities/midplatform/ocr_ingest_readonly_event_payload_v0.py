# -*- coding: utf-8 -*-
"""Read-only OCR ingest event payload for simulated Product Bus replay.

Phase-OCR-Ingest-to-Product-Bus-ReadOnly-Replay-001 — no real MQ, no DB, no fact writes.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Tuple

EVENT_PAYLOAD_SCHEMA = "ocr_ingest_readonly_event_payload_v0"
EVENT_TYPE = "midplatform.ocr_evidence.readonly_ingest_candidate"

REPLAY_LOG_STAGES: Tuple[str, ...] = (
    "event_payload_created",
    "event_replayed",
    "readonly_consumer_received",
    "readonly_consumer_view_generated",
    "no_write_action_confirmed",
)

BUS_REPLAY_AUDIT_SCHEMA = "ocr_ingest_readonly_bus_replay_audit_v0"


def build_replay_log_entries_v0(*, event_id: str, trace_id: str) -> List[Dict[str, Any]]:
    from datetime import datetime, timezone

    ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return [{"stage": s, "ts": ts, "event_id": event_id, "trace_id": trace_id} for s in REPLAY_LOG_STAGES]


def build_ocr_ingest_readonly_bus_replay_audit_v0() -> Dict[str, Any]:
    return {
        "schema": BUS_REPLAY_AUDIT_SCHEMA,
        "event_payload_created": True,
        "replay_executed": True,
        "readonly_consumer_received": True,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "ocr_provider_invoked": False,
        "ocr_routing_changed": False,
        "database_write_invoked": False,
        "external_bus_invoked": False,
    }


def build_ocr_ingest_readonly_event_payload_v0(
    *,
    ingest_candidate: Dict[str, Any],
    source_candidate_ref: str,
    geometry_matrix_ref: str,
) -> Tuple[Dict[str, Any], List[str]]:
    """Build event payload from an already-loaded ingest candidate dict."""
    errs: List[str] = []
    cid = str(ingest_candidate.get("candidate_id") or "").strip()
    if not cid:
        errs.append("ingest_candidate_missing_candidate_id")

    evc = int(ingest_candidate.get("evidence_count") or 0)
    tj = str(ingest_candidate.get("text_joined") or "").strip()
    if evc < 1:
        errs.append("evidence_count_lt_1")
    if not tj:
        errs.append("text_joined_empty")

    ebr = ingest_candidate.get("evidence_by_roi")
    if not isinstance(ebr, dict) or not ebr:
        errs.append("evidence_by_roi_empty")

    ps = ingest_candidate.get("provider_summary")
    if not isinstance(ps, dict):
        errs.append("provider_summary_missing")

    scs = ingest_candidate.get("source_chain_summary")
    if not isinstance(scs, dict):
        errs.append("source_chain_summary_missing")

    if not str(source_candidate_ref or "").strip():
        errs.append("missing_source_candidate_ref")
    if not str(geometry_matrix_ref or "").strip():
        errs.append("missing_geometry_matrix_ref")

    payload: Dict[str, Any] = {
        "schema_version": EVENT_PAYLOAD_SCHEMA,
        "event_id": f"evt_ocr_replay_{uuid.uuid4().hex}",
        "event_type": EVENT_TYPE,
        "trace_id": f"trace_{uuid.uuid4().hex}",
        "candidate_id": cid,
        "source_candidate_ref": str(source_candidate_ref),
        "payload_scope": "read_only_replay",
        "evidence_count": evc,
        "text_joined": tj,
        "evidence_by_roi": ebr if isinstance(ebr, dict) else {},
        "geometry_matrix_ref": str(geometry_matrix_ref),
        "provider_summary": ps if isinstance(ps, dict) else {},
        "source_chain_summary": scs if isinstance(scs, dict) else {},
        "allowed_consumers": [
            "readonly_replay_consumer",
            "manual_review_later",
        ],
        "forbidden_actions": {
            "write_midplatform_fact": True,
            "write_scene_delta": True,
            "write_world_model": True,
            "invoke_ai_interpretation": True,
            "invoke_ocr_provider": True,
        },
    }
    return payload, errs
