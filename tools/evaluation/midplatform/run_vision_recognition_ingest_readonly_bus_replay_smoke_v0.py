#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-Ingest-to-Product-Bus-ReadOnly-Replay-001 — simulated Product Bus replay (Vision)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

WS_ROOT = Path(__file__).resolve().parents[3]
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default="")
    ap.add_argument("--output-root", required=True)
    ap.add_argument(
        "--ingest-root",
        required=True,
        help="Absolute path to midplatform_vision_recognition_evidence_readonly_ingest_candidate smoke output.",
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    ingest_root = _require_abs(args.ingest_root, "--ingest-root")

    cand_p = ingest_root / "midplatform_vision_recognition_ingest_candidate.json"
    mx_p = ingest_root / "midplatform_vision_recognition_ingest_matrix.json"
    chain_p = ingest_root / "midplatform_vision_recognition_ingest_source_chain_summary.json"
    ing_aud_p = ingest_root / "midplatform_vision_recognition_ingest_audit_report.json"

    for label, p in (
        ("ingest_candidate", cand_p),
        ("ingest_matrix", mx_p),
        ("source_chain_summary", chain_p),
        ("ingest_audit", ing_aud_p),
    ):
        if not p.is_file():
            raise SystemExit(f"ERROR: missing input {label}: {p}")

    ingest_candidate = _read_json(cand_p)
    _read_json(mx_p)
    _read_json(chain_p)
    _read_json(ing_aud_p)

    if args.repo_root.strip():
        repo = _require_abs(args.repo_root, "--repo-root")
        if str(repo) not in sys.path:
            sys.path.insert(0, str(repo))

    from capabilities.midplatform.vision_recognition_ingest_readonly_event_payload_v0 import (
        REPLAY_LOG_STAGES,
        build_replay_log_entries_v0,
        build_vision_recognition_ingest_readonly_event_payload_v0,
        build_vision_recognition_readonly_bus_replay_audit_v0,
    )
    from capabilities.midplatform.vision_recognition_ingest_readonly_replay_consumer_v0 import (
        consume_vision_recognition_ingest_readonly_event_payload_v0,
    )

    source_candidate_ref = str(cand_p.resolve())
    ingest_matrix_ref = str(mx_p.resolve())

    payload, p_errs = build_vision_recognition_ingest_readonly_event_payload_v0(
        ingest_candidate=ingest_candidate if isinstance(ingest_candidate, dict) else {},
        source_candidate_ref=source_candidate_ref,
        ingest_matrix_ref=ingest_matrix_ref,
    )

    payload_path = out / "vision_recognition_ingest_readonly_event_payload.json"
    _write_json(payload_path, payload)

    event_id = str(payload.get("event_id") or "")
    trace_id = str(payload.get("trace_id") or "")
    log_entries = build_replay_log_entries_v0(event_id=event_id, trace_id=trace_id)
    log_path = out / "vision_recognition_ingest_readonly_replay_log.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("w", encoding="utf-8") as fh:
        for row in log_entries:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    replay_view, c_errs = consume_vision_recognition_ingest_readonly_event_payload_v0(payload)
    _write_json(out / "vision_recognition_ingest_readonly_replay_consumer_view.json", replay_view)

    audit = build_vision_recognition_readonly_bus_replay_audit_v0()
    _write_json(out / "vision_recognition_ingest_readonly_replay_audit_report.json", audit)

    summary: Dict[str, Any] = {
        "schema": "vision_recognition_ingest_readonly_bus_replay_summary_v0",
        "phase": "Phase-Vision-Ingest-to-Product-Bus-ReadOnly-Replay-001",
        "input_ingest_candidate_root": str(ingest_root),
        "input_paths": {
            "midplatform_vision_recognition_ingest_candidate.json": source_candidate_ref,
            "midplatform_vision_recognition_ingest_matrix.json": ingest_matrix_ref,
            "midplatform_vision_recognition_ingest_source_chain_summary.json": str(chain_p.resolve()),
            "midplatform_vision_recognition_ingest_audit_report.json": str(ing_aud_p.resolve()),
        },
        "output_event_payload_path": str(payload_path.resolve()),
        "output_replay_log_path": str(log_path.resolve()),
        "replay_log_stage_count": len(REPLAY_LOG_STAGES),
        "payload_build_errors": list(p_errs),
        "consumer_validation_errors": list(c_errs),
        "event_id": event_id,
        "event_type": str(payload.get("event_type") or ""),
        "candidate_id": str(payload.get("candidate_id") or ""),
        "evidence_count": int(payload.get("evidence_count") or 0),
    }
    _write_json(out / "vision_recognition_ingest_readonly_bus_replay_summary.json", summary)

    (out / "vision_recognition_ingest_readonly_bus_replay_notes.md").write_text(
        "# Phase-Vision-Ingest-to-Product-Bus-ReadOnly-Replay-001\n\n"
        "Simulated **read-only** Product Bus for **Vision** ingest candidate: event payload, JSONL replay log, "
        "readonly replay consumer view. **No** real Kafka/Redis/NATS/gRPC/HTTP bus, **no** DB writes, "
        "**no** MidPlatform fact / Scene Delta / WorldModel, **no** AI interpretation / navigation / "
        "real vision / YOLO / Supervision mainline / VLM / OCR.\n",
        encoding="utf-8",
    )

    if p_errs or c_errs:
        _write_json(
            out / "vision_recognition_ingest_readonly_bus_replay_validation_errors.json",
            {"payload_errors": p_errs, "consumer_errors": c_errs},
        )

    ok = not p_errs and not c_errs
    print(
        json.dumps(
            {
                "vision_recognition_ingest_readonly_bus_replay_smoke_root": str(out),
                "event_payload": str(payload_path.resolve()),
                "status": "success" if ok else "validation_failed",
            },
            ensure_ascii=False,
        )
    )
    return 0 if ok else 3


if __name__ == "__main__":
    raise SystemExit(main())
