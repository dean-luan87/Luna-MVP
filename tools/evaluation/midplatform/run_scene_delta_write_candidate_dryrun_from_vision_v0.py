#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-From-Vision-001 — dry-run only."""

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
        "--write-candidate-root",
        default="",
        help="Directory with scene_delta_write_candidate_from_vision.json (Vision stub smoke output)",
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    default_in = Path(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_write_candidate_from_vision_ingest_stub_smoke_v0"
    )
    wr = Path(args.write_candidate_root).expanduser() if args.write_candidate_root.strip() else default_in
    if not wr.is_absolute():
        wr = (WS_ROOT / wr).resolve()
    in_root = _require_abs(str(wr), "--write-candidate-root (resolved)")

    cand_p = in_root / "scene_delta_write_candidate_from_vision.json"
    mat_p = in_root / "scene_delta_write_candidate_vision_evidence_matrix.json"
    gate_p = in_root / "scene_delta_write_candidate_vision_gate_stub.json"
    aud_p = in_root / "scene_delta_write_candidate_vision_audit_report.json"

    for label, p in (
        ("write_candidate", cand_p),
        ("evidence_matrix", mat_p),
        ("gate_stub", gate_p),
        ("vision_audit", aud_p),
    ):
        if not p.is_file():
            raise SystemExit(f"ERROR: missing input {label}: {p}")

    candidate = _read_json(cand_p)
    matrix = _read_json(mat_p)
    gate = _read_json(gate_p)
    vision_audit = _read_json(aud_p)

    if not isinstance(candidate, dict):
        raise SystemExit("ERROR: write candidate must be object")

    from capabilities.midplatform.scene_delta_write_candidate_dryrun_from_vision_v0 import (
        run_scene_delta_write_candidate_dryrun_from_vision_v0,
    )

    summary, comp, mapping, risks, no_write, blocking = run_scene_delta_write_candidate_dryrun_from_vision_v0(
        input_write_candidate_root=str(in_root),
        candidate=candidate,
        evidence_matrix=matrix,
        gate=gate if isinstance(gate, dict) else {},
        vision_audit=vision_audit if isinstance(vision_audit, dict) else {},
    )

    summary["paths"] = {
        "write_candidate_json": str(cand_p.resolve()),
        "evidence_matrix_json": str(mat_p.resolve()),
        "gate_stub_json": str(gate_p.resolve()),
        "vision_audit_json": str(aud_p.resolve()),
    }
    summary["phase"] = "Phase-MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-From-Vision-001"

    _write_json(out / "scene_delta_write_candidate_dryrun_from_vision_summary.json", summary)
    _write_json(out / "scene_delta_write_candidate_from_vision_field_completeness_report.json", comp)
    _write_json(out / "scene_delta_write_candidate_from_vision_mapping_matrix.json", mapping)
    _write_json(out / "scene_delta_write_candidate_from_vision_risk_report.json", risks)
    _write_json(out / "scene_delta_write_candidate_from_vision_no_write_audit_report.json", no_write)

    (out / "scene_delta_write_candidate_dryrun_from_vision_notes.md").write_text(
        "# Phase-MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-From-Vision-001\n\n"
        "Dry-run verification of **`scene_delta_write_candidate_from_vision`** — field completeness, "
        "Vision → Scene Delta **mapping matrix** (conceptual only), **risk report**, **no-write audit**. "
        "**No** Scene Delta executor, **no** DB, **no** fact / WorldModel / AI / navigation / real vision.\n",
        encoding="utf-8",
    )

    if blocking:
        _write_json(out / "scene_delta_write_candidate_dryrun_from_vision_blocking_errors.json", {"errors": blocking})

    ok = not blocking
    print(
        json.dumps(
            {
                "scene_delta_write_candidate_dryrun_from_vision_smoke_root": str(out),
                "dry_run_id": summary.get("dry_run_id"),
                "status": "success" if ok else "blocking_failed",
            },
            ensure_ascii=False,
        )
    )
    return 0 if ok else 3


if __name__ == "__main__":
    raise SystemExit(main())
