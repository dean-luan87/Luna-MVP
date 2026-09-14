#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR ingest read-only bus replay smoke."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

EXPECTED_EVENT_SCHEMA = "ocr_ingest_readonly_event_payload_v0"
EXPECTED_EVENT_TYPE = "midplatform.ocr_evidence.readonly_ingest_candidate"
EXPECTED_STAGES = {
    "event_payload_created",
    "event_replayed",
    "readonly_consumer_received",
    "readonly_consumer_view_generated",
    "no_write_action_confirmed",
}
FORBIDDEN_KEYS = (
    "write_midplatform_fact",
    "write_scene_delta",
    "write_world_model",
    "invoke_ai_interpretation",
    "invoke_ocr_provider",
)


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    pay_p = root / "ocr_ingest_readonly_event_payload.json"
    log_p = root / "ocr_ingest_readonly_replay_log.jsonl"
    view_p = root / "ocr_ingest_readonly_replay_consumer_view.json"
    aud_p = root / "ocr_ingest_readonly_replay_audit_report.json"

    for label, p in (
        ("event_payload", pay_p),
        ("replay_log", log_p),
        ("replay_consumer_view", view_p),
        ("replay_audit", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"
    if blockers:
        rep = {
            "schema": "ocr_ingest_readonly_bus_replay_verifier_report_v0",
            "phase": "Phase-OCR-Ingest-to-Product-Bus-ReadOnly-Replay-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
        }
        _write_json(root / "ocr_ingest_readonly_bus_replay_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    payload: Dict[str, Any] = _read_json(pay_p)
    aud: Dict[str, Any] = _read_json(aud_p)
    view: Dict[str, Any] = _read_json(view_p)

    if str(payload.get("schema_version") or "") != EXPECTED_EVENT_SCHEMA:
        blockers.append("event_payload_schema_mismatch")
    if str(payload.get("event_type") or "") != EXPECTED_EVENT_TYPE:
        blockers.append("event_type_mismatch")
    if not str(payload.get("candidate_id") or "").strip():
        blockers.append("candidate_id_missing")
    if not str(payload.get("source_candidate_ref") or "").strip():
        blockers.append("source_candidate_ref_missing")
    if str(payload.get("payload_scope") or "") != "read_only_replay":
        blockers.append("payload_scope_must_be_read_only_replay")
    if int(payload.get("evidence_count") or 0) < 1:
        blockers.append("evidence_count_ge_1")
    if not str(payload.get("text_joined") or "").strip():
        blockers.append("text_joined_non_empty")
    ebr = payload.get("evidence_by_roi")
    if not isinstance(ebr, dict) or not ebr:
        blockers.append("evidence_by_roi_present")
    if not str(payload.get("geometry_matrix_ref") or "").strip():
        blockers.append("geometry_matrix_ref_present")

    fa = payload.get("forbidden_actions")
    if not isinstance(fa, dict):
        blockers.append("forbidden_actions_must_be_object")
    else:
        for k in FORBIDDEN_KEYS:
            if k not in fa or fa.get(k) is not True:
                blockers.append(f"forbidden_actions_missing_or_not_true:{k}")

    stages_seen: set[str] = set()
    try:
        for line in log_p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            st = str(row.get("stage") or "")
            if st:
                stages_seen.add(st)
    except Exception:
        blockers.append("replay_log_invalid")

    if not EXPECTED_STAGES.issubset(stages_seen):
        blockers.append("replay_log_missing_required_stages")

    for k, must in (
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("ai_interpretation_invoked", False),
        ("ocr_provider_invoked", False),
        ("ocr_routing_changed", False),
        ("database_write_invoked", False),
        ("external_bus_invoked", False),
    ):
        if aud.get(k) is not must:
            blockers.append(f"audit_gate:{k}")

    for k, must in (
        ("event_payload_created", True),
        ("replay_executed", True),
        ("readonly_consumer_received", True),
    ):
        if aud.get(k) is not must:
            blockers.append(f"audit_positive_gate:{k}")

    soft: List[str] = []
    if not blockers:
        verdict = "GO"
        ve = view.get("validation_errors")
        if isinstance(ve, list) and ve:
            verdict = "CONDITIONAL_GO"
            soft.append("consumer_validation_errors_non_empty")
        if view.get("provider_summary_present") is not True:
            verdict = "CONDITIONAL_GO"
            soft.append("provider_summary_absent_in_view")
    else:
        verdict = "NO_GO"

    rep = {
        "schema": "ocr_ingest_readonly_bus_replay_verifier_report_v0",
        "phase": "Phase-OCR-Ingest-to-Product-Bus-ReadOnly-Replay-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
        "event_payload_path": str(pay_p.resolve()),
    }
    _write_json(root / "ocr_ingest_readonly_bus_replay_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
