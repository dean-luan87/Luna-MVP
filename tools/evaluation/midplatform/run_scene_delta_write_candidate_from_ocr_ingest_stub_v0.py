#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-MidPlatform-Scene-Delta-Write-Candidate-From-OCR-Ingest-Stub-001 — stub write candidate only."""

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
    ap.add_argument("--output-root", required=True)
    ap.add_argument(
        "--bus-replay-root",
        default="",
        help="Directory containing ocr_ingest_readonly_event_payload.json",
    )
    ap.add_argument(
        "--event-payload",
        default="",
        help="Optional absolute path to ocr_ingest_readonly_event_payload.json (overrides bus-replay-root default)",
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    default_bus = Path(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_ingest_readonly_bus_replay_smoke_v0"
    )
    br = Path(args.bus_replay_root).expanduser() if args.bus_replay_root.strip() else default_bus
    if not br.is_absolute():
        br = (WS_ROOT / br).resolve()
    bus_root = _require_abs(str(br), "--bus-replay-root (resolved)")

    if args.event_payload.strip():
        pay_p = Path(args.event_payload).expanduser()
        if not pay_p.is_absolute():
            pay_p = (WS_ROOT / pay_p).resolve()
        pay_p = _require_abs(str(pay_p), "--event-payload")
    else:
        pay_p = bus_root / "ocr_ingest_readonly_event_payload.json"

    if not pay_p.is_file():
        raise SystemExit(f"ERROR: event payload not found: {pay_p}")

    payload = _read_json(pay_p)
    if not isinstance(payload, dict):
        raise SystemExit("ERROR: event payload must be a JSON object")

    gref = str(payload.get("geometry_matrix_ref") or "").strip()
    if not gref:
        raise SystemExit("ERROR: payload missing geometry_matrix_ref")
    geom_p = Path(gref)
    if not geom_p.is_file():
        raise SystemExit(f"ERROR: geometry_matrix_ref not found: {geom_p}")
    geometry_matrix = _read_json(geom_p)

    from capabilities.midplatform.scene_delta_write_candidate_from_ocr_v0 import (
        build_scene_delta_write_candidate_audit_v0,
        build_scene_delta_write_candidate_from_ocr_v0,
        build_scene_delta_write_candidate_gate_stub_v0,
        collect_forbidden_keys_in_object_v0,
    )

    candidate, build_errs = build_scene_delta_write_candidate_from_ocr_v0(
        event_payload=payload,
        geometry_matrix=geometry_matrix,
    )
    key_hits = collect_forbidden_keys_in_object_v0(candidate)
    if key_hits:
        build_errs = list(build_errs) + [f"forbidden_key_in_candidate:{h}" for h in key_hits]

    gate = build_scene_delta_write_candidate_gate_stub_v0()
    audit = build_scene_delta_write_candidate_audit_v0()

    cand_path = out / "scene_delta_write_candidate_from_ocr.json"
    _write_json(cand_path, candidate)
    _write_json(out / "scene_delta_write_candidate_evidence_matrix.json", candidate.get("evidence_items") or [])
    _write_json(out / "scene_delta_write_candidate_gate_stub.json", gate)
    _write_json(out / "scene_delta_write_candidate_audit_report.json", audit)

    summary: Dict[str, Any] = {
        "schema": "scene_delta_write_candidate_from_ocr_summary_v0",
        "phase": "Phase-MidPlatform-Scene-Delta-Write-Candidate-From-OCR-Ingest-Stub-001",
        "input_bus_replay_root": str(bus_root),
        "input_event_payload_path": str(pay_p.resolve()),
        "input_geometry_matrix_path": str(geom_p.resolve()),
        "output_write_candidate_path": str(cand_path.resolve()),
        "source_event_id": str(payload.get("event_id") or ""),
        "source_ingest_candidate_id": str(payload.get("candidate_id") or ""),
        "write_candidate_candidate_id": candidate.get("candidate_id"),
        "build_errors": list(build_errs),
        "validation_ok": len(build_errs) == 0,
    }
    _write_json(out / "scene_delta_write_candidate_from_ocr_summary.json", summary)

    (out / "scene_delta_write_candidate_notes.md").write_text(
        "# Phase-MidPlatform-Scene-Delta-Write-Candidate-From-OCR-Ingest-Stub-001\n\n"
        "Builds **`scene_delta_write_candidate_from_ocr_v0`** from read-only OCR event payload + geometry matrix. "
        "**Write candidate only** — no Scene Delta execution, no DB, no MidPlatform fact, no WorldModel, no AI.\n",
        encoding="utf-8",
    )

    if build_errs:
        _write_json(out / "scene_delta_write_candidate_validation_errors.json", {"errors": build_errs})

    print(
        json.dumps(
            {
                "scene_delta_write_candidate_from_ocr_smoke_root": str(out),
                "write_candidate": str(cand_path.resolve()),
                "status": "success" if not build_errs else "validation_failed",
            },
            ensure_ascii=False,
        )
    )
    return 0 if not build_errs else 3


if __name__ == "__main__":
    raise SystemExit(main())
