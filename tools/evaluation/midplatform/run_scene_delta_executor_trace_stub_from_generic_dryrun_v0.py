#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-MidPlatform-Scene-Delta-Executor-Trace-Stub-From-Generic-DryRun-001 — trace stub only."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument(
        "--dry-run-root",
        default="",
        help="OCR or Vision dry-run smoke directory (auto-detect by summary schema)",
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    default_dr = Path(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_write_candidate_dryrun_from_vision_smoke_v0"
    )
    dr = Path(args.dry_run_root).expanduser() if args.dry_run_root.strip() else default_dr
    if not dr.is_absolute():
        dr = (WS_ROOT / dr).resolve()
    in_root = _require_abs(str(dr), "--dry-run-root (resolved)")

    from capabilities.midplatform.scene_delta_executor_trace_stub_generic_v0 import (
        load_write_candidate_and_gate,
        resolve_dry_run_bundle,
        run_executor_trace_stub_from_generic_dryrun_v0,
    )

    try:
        flavor, dry_summary, mapping, risk, nw, map_p, risk_p, nw_p = resolve_dry_run_bundle(in_root)
    except (FileNotFoundError, ValueError) as e:
        raise SystemExit(f"ERROR: {e}") from e

    write_candidate, gate_stub = load_write_candidate_and_gate(dry_summary)

    summary, trace, matrix, compat, audit, errs = run_executor_trace_stub_from_generic_dryrun_v0(
        dry_run_root=str(in_root),
        dry_summary=dry_summary if isinstance(dry_summary, dict) else {},
        flavor=flavor,
        mapping_matrix=mapping if isinstance(mapping, dict) else {},
        risk_report=risk if isinstance(risk, dict) else {},
        no_write_audit=nw if isinstance(nw, dict) else {},
        mapping_matrix_path=str(map_p.resolve()),
        risk_report_path=str(risk_p.resolve()),
        no_write_audit_path=str(nw_p.resolve()),
        write_candidate=write_candidate if isinstance(write_candidate, dict) else {},
        gate_stub=gate_stub if isinstance(gate_stub, dict) else {},
    )

    paths = dry_summary.get("paths") if isinstance(dry_summary.get("paths"), dict) else {}
    summary["input_paths"] = {
        "dry_run_root": str(in_root),
        "dryrun_summary": str((in_root / (
            "scene_delta_write_candidate_dryrun_from_vision_summary.json"
            if flavor == "vision"
            else "scene_delta_write_candidate_dryrun_summary.json"
        )).resolve()),
        "mapping_matrix": str(map_p.resolve()),
        "risk_report": str(risk_p.resolve()),
        "no_write_audit": str(nw_p.resolve()),
        "write_candidate": str(paths.get("write_candidate_json") or ""),
        "gate_stub": str(paths.get("gate_stub_json") or ""),
    }
    summary["output_trace_stub_path"] = str((out / "scene_delta_executor_trace_stub_generic.json").resolve())

    _write_json(out / "scene_delta_executor_trace_stub_generic_summary.json", summary)
    _write_json(out / "scene_delta_executor_trace_stub_generic.json", trace)
    _write_json(out / "scene_delta_executor_planned_step_matrix_generic.json", matrix)
    _write_json(out / "scene_delta_executor_input_compatibility_report_generic.json", compat)
    _write_json(out / "scene_delta_executor_trace_stub_generic_audit_report.json", audit)

    (out / "scene_delta_executor_trace_stub_generic_notes.md").write_text(
        "# Phase-MidPlatform-Scene-Delta-Executor-Trace-Stub-From-Generic-DryRun-001\n\n"
        "Generates **`scene_delta_executor_trace_stub_generic_v0`** from **OCR or Vision** dry-run outputs "
        "(auto-detected summary schema). **Trace stub only** — no real executor, no DB, no fact writes, no AI, "
        "no navigation.\n",
        encoding="utf-8",
    )

    if errs:
        _write_json(out / "scene_delta_executor_trace_stub_generic_validation_errors.json", {"errors": errs})

    print(
        json.dumps(
            {
                "scene_delta_executor_trace_stub_generic_smoke_root": str(out),
                "trace_id": trace.get("trace_id"),
                "dry_run_flavor": flavor,
                "source_type": trace.get("source_type"),
                "status": "success" if not errs else "validation_failed",
            },
            ensure_ascii=False,
        )
    )
    return 0 if not errs else 3


if __name__ == "__main__":
    raise SystemExit(main())
