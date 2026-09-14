#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-MidPlatform-Scene-Delta-Write-Candidate-From-Vision-Ingest-Stub-001 — stub candidate only."""

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
    ap.add_argument(
        "--bus-replay-root",
        required=True,
        help="Absolute path to vision_recognition_ingest_readonly_bus_replay smoke output.",
    )
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    bus = _require_abs(args.bus_replay_root, "--bus-replay-root")
    out = _require_abs(args.output_root, "--output-root")

    pay_p = bus / "vision_recognition_ingest_readonly_event_payload.json"
    view_p = bus / "vision_recognition_ingest_readonly_replay_consumer_view.json"
    aud_p = bus / "vision_recognition_ingest_readonly_replay_audit_report.json"

    for label, p in (("event_payload", pay_p), ("replay_consumer_view", view_p), ("replay_audit", aud_p)):
        if not p.is_file():
            raise SystemExit(f"ERROR: missing {label}: {p}")

    payload = _read_json(pay_p)
    view = _read_json(view_p)
    _read_json(aud_p)

    if not isinstance(payload, dict):
        raise SystemExit("ERROR: event payload must be a JSON object")

    mref = str(payload.get("ingest_matrix_ref") or "").strip()
    if not mref:
        raise SystemExit("ERROR: payload missing ingest_matrix_ref")

    if args.repo_root.strip():
        repo = _require_abs(args.repo_root, "--repo-root")
        if str(repo) not in sys.path:
            sys.path.insert(0, str(repo))

    from capabilities.midplatform.scene_delta_write_candidate_from_vision_v0 import (
        build_scene_delta_write_candidate_from_vision_v0,
        build_scene_delta_write_candidate_gate_stub_vision_v0,
        build_scene_delta_write_candidate_vision_audit_v0,
        build_scene_delta_write_candidate_vision_evidence_matrix_v0,
        load_vision_ingest_matrix_rows_v0,
    )

    matrix_rows = load_vision_ingest_matrix_rows_v0(mref)
    candidate, build_errs = build_scene_delta_write_candidate_from_vision_v0(
        event_payload=payload,
        ingest_matrix_rows=matrix_rows,
        replay_consumer_view=view if isinstance(view, dict) else {},
    )

    gate = build_scene_delta_write_candidate_gate_stub_vision_v0()
    audit = build_scene_delta_write_candidate_vision_audit_v0()
    ev_mx = build_scene_delta_write_candidate_vision_evidence_matrix_v0(candidate.get("evidence_items") or [])

    cand_path = out / "scene_delta_write_candidate_from_vision.json"
    _write_json(cand_path, candidate)
    _write_json(out / "scene_delta_write_candidate_vision_gate_stub.json", gate)
    _write_json(out / "scene_delta_write_candidate_vision_evidence_matrix.json", ev_mx)
    _write_json(out / "scene_delta_write_candidate_vision_audit_report.json", audit)

    summary: Dict[str, Any] = {
        "schema": "scene_delta_write_candidate_from_vision_summary_v0",
        "phase": "Phase-MidPlatform-Scene-Delta-Write-Candidate-From-Vision-Ingest-Stub-001",
        "input_vision_bus_replay_root": str(bus),
        "ingest_matrix_ref": mref,
        "write_candidate_path": str(cand_path.resolve()),
        "source_event_id": str(candidate.get("source_event_id") or ""),
        "source_ingest_candidate_id": str(candidate.get("source_ingest_candidate_id") or ""),
        "candidate_scope": str(candidate.get("candidate_scope") or ""),
        "write_allowed": bool(candidate.get("write_allowed")),
        "requires_gate_approval": bool(candidate.get("requires_gate_approval")),
        "evidence_count": int(candidate.get("evidence_count") or 0),
        "build_errors": list(build_errs),
    }
    _write_json(out / "scene_delta_write_candidate_from_vision_summary.json", summary)

    (out / "scene_delta_write_candidate_from_vision_notes.md").write_text(
        "# Phase-MidPlatform-Scene-Delta-Write-Candidate-From-Vision-Ingest-Stub-001\n\n"
        "Builds **`scene_delta_write_candidate_from_vision_v0`** from Vision read-only **event payload** "
        "and **ingest matrix**. **Candidate only** — no Scene Delta write, no MidPlatform fact, no WorldModel, "
        "no AI interpretation, no navigation, no real vision providers.\n",
        encoding="utf-8",
    )

    if build_errs:
        _write_json(out / "scene_delta_write_candidate_from_vision_validation_errors.json", {"errors": build_errs})

    ok = not build_errs
    print(
        json.dumps(
            {
                "scene_delta_write_candidate_from_vision_smoke_root": str(out),
                "write_candidate": str(cand_path.resolve()),
                "status": "success" if ok else "validation_failed",
            },
            ensure_ascii=False,
        )
    )
    return 0 if ok else 3


if __name__ == "__main__":
    raise SystemExit(main())
