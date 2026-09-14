# -*- coding: utf-8 -*-
"""Read-only Vision recognition ingest event payload for simulated Product Bus replay.

Phase-Vision-Ingest-to-Product-Bus-ReadOnly-Replay-001 — no real MQ, no DB, no fact writes.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Tuple

EVENT_PAYLOAD_SCHEMA = "vision_recognition_ingest_readonly_event_payload_v0"
EVENT_TYPE = "midplatform.vision_recognition.readonly_ingest_candidate"

REPLAY_LOG_STAGES: Tuple[str, ...] = (
    "event_payload_created",
    "event_replayed",
    "readonly_consumer_received",
    "readonly_consumer_view_generated",
    "no_write_action_confirmed",
)

BUS_REPLAY_AUDIT_SCHEMA = "vision_recognition_ingest_readonly_bus_replay_audit_v0"


def build_replay_log_entries_v0(*, event_id: str, trace_id: str) -> List[Dict[str, Any]]:
    from datetime import datetime, timezone

    ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return [{"stage": s, "ts": ts, "event_id": event_id, "trace_id": trace_id} for s in REPLAY_LOG_STAGES]


def build_vision_recognition_readonly_bus_replay_audit_v0() -> Dict[str, Any]:
    return {
        "schema": BUS_REPLAY_AUDIT_SCHEMA,
        "event_payload_created": True,
        "replay_executed": True,
        "readonly_consumer_received": True,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "real_vision_provider_invoked": False,
        "yolo_invoked": False,
        "supervision_mainline_invoked": False,
        "vlm_invoked": False,
        "ocr_invoked": False,
        "database_write_invoked": False,
        "external_bus_invoked": False,
    }


def build_vision_recognition_ingest_readonly_event_payload_v0(
    *,
    ingest_candidate: Dict[str, Any],
    source_candidate_ref: str,
    ingest_matrix_ref: str,
) -> Tuple[Dict[str, Any], List[str]]:
    errs: List[str] = []
    cid = str(ingest_candidate.get("candidate_id") or "").strip()
    if not cid:
        errs.append("ingest_candidate_missing_candidate_id")

    evc = int(ingest_candidate.get("evidence_count") or 0)
    if evc < 1:
        errs.append("evidence_count_lt_1")

    prov = str(ingest_candidate.get("provider") or "")
    pl = str(ingest_candidate.get("provider_level") or "")
    if prov != "vision_stub":
        errs.append("provider_must_be_vision_stub")
    if pl != "stub":
        errs.append("provider_level_must_be_stub")

    fs = ingest_candidate.get("fact_status_summary") or {}
    if int(fs.get("not_fact") or 0) != evc:
        errs.append("fact_status_summary_not_fact_mismatch")

    syn = ingest_candidate.get("synthetic_summary") or {}
    if int(syn.get("synthetic_count") or 0) != evc:
        errs.append("synthetic_count_mismatch")
    if int(syn.get("stub_provider_count") or 0) != evc:
        errs.append("stub_provider_count_mismatch")

    by_f = ingest_candidate.get("evidence_by_frame")
    if not isinstance(by_f, dict) or not by_f:
        errs.append("evidence_by_frame_empty")

    by_r = ingest_candidate.get("evidence_by_roi_type")
    if not isinstance(by_r, dict) or not by_r:
        errs.append("evidence_by_roi_type_empty")

    geom = ingest_candidate.get("geometry_summary")
    if not isinstance(geom, dict) or not geom:
        errs.append("geometry_summary_empty")

    scs = ingest_candidate.get("source_chain_summary")
    if not isinstance(scs, dict):
        errs.append("source_chain_summary_missing")

    if not str(source_candidate_ref or "").strip():
        errs.append("missing_source_candidate_ref")
    if not str(ingest_matrix_ref or "").strip():
        errs.append("missing_ingest_matrix_ref")

    payload: Dict[str, Any] = {
        "schema_version": EVENT_PAYLOAD_SCHEMA,
        "event_id": f"evt_vision_replay_{uuid.uuid4().hex}",
        "event_type": EVENT_TYPE,
        "trace_id": f"trace_{uuid.uuid4().hex}",
        "candidate_id": cid,
        "source_candidate_ref": str(source_candidate_ref),
        "ingest_matrix_ref": str(ingest_matrix_ref),
        "payload_scope": "read_only_replay",
        "evidence_count": evc,
        "provider": prov,
        "provider_level": pl,
        "fact_status_summary": dict(fs) if isinstance(fs, dict) else {},
        "synthetic_summary": dict(syn) if isinstance(syn, dict) else {},
        "evidence_by_frame": by_f if isinstance(by_f, dict) else {},
        "evidence_by_roi_type": by_r if isinstance(by_r, dict) else {},
        "geometry_summary": geom if isinstance(geom, dict) else {},
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
            "invoke_navigation_decision": True,
            "invoke_real_vision_provider": True,
        },
    }
    return payload, errs
