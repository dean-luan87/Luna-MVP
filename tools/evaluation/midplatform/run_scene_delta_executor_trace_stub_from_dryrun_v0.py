#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-MidPlatform-Scene-Delta-Executor-Trace-Stub-From-DryRun-001 — trace stub only."""

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
        "--dry-run-root",
        default="",
        help="Directory with scene_delta_write_candidate_dryrun_summary.json",
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    default_dr = Path(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_write_candidate_dryrun_verifier_smoke_v0"
    )
    dr = Path(args.dry_run_root).expanduser() if args.dry_run_root.strip() else default_dr
    if not dr.is_absolute():
        dr = (WS_ROOT / dr).resolve()
    in_root = _require_abs(str(dr), "--dry-run-root (resolved)")

    sum_p = in_root / "scene_delta_write_candidate_dryrun_summary.json"
    map_p = in_root / "scene_delta_write_candidate_mapping_matrix.json"
    risk_p = in_root / "scene_delta_write_candidate_risk_report.json"
    nw_p = in_root / "scene_delta_write_candidate_no_write_audit_report.json"

    for label, p in (
        ("dryrun_summary", sum_p),
        ("mapping_matrix", map_p),
        ("risk_report", risk_p),
        ("no_write_audit", nw_p),
    ):
        if not p.is_file():
            raise SystemExit(f"ERROR: missing dry-run input {label}: {p}")

    dry_summary = _read_json(sum_p)
    mapping = _read_json(map_p)
    risk = _read_json(risk_p)
    nw = _read_json(nw_p)

    if not isinstance(dry_summary, dict):
        raise SystemExit("ERROR: dryrun summary must be object")

    paths = dry_summary.get("paths") if isinstance(dry_summary.get("paths"), dict) else {}
    cand_path_s = str(paths.get("write_candidate_json") or "").strip()
    gate_path_s = str(paths.get("gate_stub_json") or "").strip()
    if not cand_path_s or not Path(cand_path_s).is_file():
        raise SystemExit("ERROR: dryrun summary missing write_candidate_json path")
    if not gate_path_s or not Path(gate_path_s).is_file():
        raise SystemExit("ERROR: dryrun summary missing gate_stub_json path")

    write_candidate = _read_json(Path(cand_path_s))
    gate_stub = _read_json(Path(gate_path_s))

    from capabilities.midplatform.scene_delta_executor_trace_stub_v0 import run_executor_trace_stub_from_dryrun_v0

    summary, trace, matrix, compat, audit, errs = run_executor_trace_stub_from_dryrun_v0(
        dry_run_summary=dry_summary,
        mapping_matrix=mapping if isinstance(mapping, dict) else {},
        risk_report=risk if isinstance(risk, dict) else {},
        write_candidate=write_candidate if isinstance(write_candidate, dict) else {},
        gate_stub=gate_stub if isinstance(gate_stub, dict) else {},
    )

    summary["input_dry_run_root"] = str(in_root)
    summary["input_paths"] = {
        "dryrun_summary": str(sum_p.resolve()),
        "mapping_matrix": str(map_p.resolve()),
        "risk_report": str(risk_p.resolve()),
        "no_write_audit": str(nw_p.resolve()),
        "write_candidate": cand_path_s,
        "gate_stub": gate_path_s,
    }
    summary["output_trace_stub_path"] = str((out / "scene_delta_executor_trace_stub.json").resolve())

    _write_json(out / "scene_delta_executor_trace_stub_summary.json", summary)
    _write_json(out / "scene_delta_executor_trace_stub.json", trace)
    _write_json(out / "scene_delta_executor_planned_step_matrix.json", matrix)
    _write_json(out / "scene_delta_executor_input_compatibility_report.json", compat)
    _write_json(out / "scene_delta_executor_trace_stub_audit_report.json", audit)

    (out / "scene_delta_executor_trace_stub_notes.md").write_text(
        "# Phase-MidPlatform-Scene-Delta-Executor-Trace-Stub-From-DryRun-001\n\n"
        "Generates **`scene_delta_executor_trace_stub_v0`** and planned step matrix from **dry-run** outputs. "
        "**Trace stub only** — no real Scene Delta executor, no DB, no fact writes, no AI.\n",
        encoding="utf-8",
    )

    if errs:
        _write_json(out / "scene_delta_executor_trace_stub_validation_errors.json", {"errors": errs})

    print(
        json.dumps(
            {
                "scene_delta_executor_trace_stub_smoke_root": str(out),
                "trace_id": trace.get("trace_id"),
                "status": "success" if not errs else "validation_failed",
            },
            ensure_ascii=False,
        )
    )
    return 0 if not errs else 3


if __name__ == "__main__":
    raise SystemExit(main())
