#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-MidPlatform-Scene-Delta-Executor-Mock-Handshake-Generic-Trace-001 — in-memory mock only."""

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


def _read_json(p: Path) -> object:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument(
        "--generic-trace-root",
        default="",
        help="Directory with scene_delta_executor_trace_stub_generic.json",
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    default_tr = Path(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_trace_stub_from_generic_dryrun_vision_smoke_v0"
    )
    tr = Path(args.generic_trace_root).expanduser() if args.generic_trace_root.strip() else default_tr
    if not tr.is_absolute():
        tr = (WS_ROOT / tr).resolve()
    stub_root = _require_abs(str(tr), "--generic-trace-root (resolved)")

    stub_p = stub_root / "scene_delta_executor_trace_stub_generic.json"
    sum_p = stub_root / "scene_delta_executor_trace_stub_generic_summary.json"
    mat_p = stub_root / "scene_delta_executor_planned_step_matrix_generic.json"
    comp_p = stub_root / "scene_delta_executor_input_compatibility_report_generic.json"
    aud_p = stub_root / "scene_delta_executor_trace_stub_generic_audit_report.json"

    for label, p in (
        ("trace_stub_generic", stub_p),
        ("trace_stub_generic_summary", sum_p),
        ("planned_matrix_generic", mat_p),
        ("input_compatibility_generic", comp_p),
        ("trace_stub_generic_audit", aud_p),
    ):
        if not p.is_file():
            raise SystemExit(f"ERROR: missing {label}: {p}")

    trace_stub = _read_json(stub_p)
    stub_summary = _read_json(sum_p)
    matrix = _read_json(mat_p)
    compat_in = _read_json(comp_p)
    stub_audit = _read_json(aud_p)

    if not isinstance(trace_stub, dict):
        raise SystemExit("ERROR: trace stub generic must be object")
    if not isinstance(stub_summary, dict):
        raise SystemExit("ERROR: trace stub generic summary must be object")

    paths = stub_summary.get("input_paths") if isinstance(stub_summary.get("input_paths"), dict) else {}
    cand_ref = str(paths.get("write_candidate") or "").strip()
    if not cand_ref or not Path(cand_ref).is_file():
        raise SystemExit("ERROR: generic summary input_paths.write_candidate missing or not a file")

    from capabilities.midplatform.scene_delta_executor_mock_handshake_generic_v0 import run_mock_handshake_generic_v0

    summary, req, ack, trace_lines, compat, audit, blocking = run_mock_handshake_generic_v0(
        trace_stub=trace_stub,
        planned_matrix=matrix if isinstance(matrix, dict) else {},
        compatibility_input=compat_in if isinstance(compat_in, dict) else {},
        trace_stub_audit=stub_audit if isinstance(stub_audit, dict) else {},
        candidate_payload_ref=cand_ref,
        planned_matrix_path=str(mat_p.resolve()),
        compatibility_path=str(comp_p.resolve()),
        generic_trace_root=str(stub_root),
    )

    summary["paths"] = {
        "generic_trace_stub": str(stub_p.resolve()),
        "generic_trace_summary": str(sum_p.resolve()),
        "planned_step_matrix": str(mat_p.resolve()),
        "input_compatibility": str(comp_p.resolve()),
        "trace_stub_audit": str(aud_p.resolve()),
        "candidate_payload": cand_ref,
    }
    summary["mock_request_path"] = str((out / "scene_delta_mock_executor_request_generic.json").resolve())
    summary["mock_ack_path"] = str((out / "scene_delta_mock_executor_ack_generic.json").resolve())

    _write_json(out / "scene_delta_executor_mock_handshake_generic_summary.json", summary)
    _write_json(out / "scene_delta_mock_executor_request_generic.json", req)
    _write_json(out / "scene_delta_mock_executor_ack_generic.json", ack)
    trace_path = out / "scene_delta_mock_handshake_trace_generic.jsonl"
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    with trace_path.open("w", encoding="utf-8") as fh:
        for row in trace_lines:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    _write_json(out / "scene_delta_mock_handshake_compatibility_report_generic.json", compat)
    _write_json(out / "scene_delta_mock_handshake_audit_report_generic.json", audit)

    (out / "scene_delta_mock_handshake_generic_notes.md").write_text(
        "# Phase-MidPlatform-Scene-Delta-Executor-Mock-Handshake-Generic-Trace-001\n\n"
        "In-memory **mock executor** consumes **`scene_delta_executor_trace_stub_generic_v0`** "
        "(OCR or Vision `source_type`), emits **synthetic ACK**. "
        "**No** real executor, **no** Scene Delta write, **no** DB, **no** rehearsal log / WAL.\n",
        encoding="utf-8",
    )

    if blocking:
        _write_json(out / "scene_delta_mock_handshake_generic_blocking_errors.json", {"errors": blocking})

    ok = not blocking and bool(compat.get("overall_ok"))
    print(
        json.dumps(
            {
                "scene_delta_executor_mock_handshake_generic_smoke_root": str(out),
                "request_id": req.get("request_id") if isinstance(req, dict) else None,
                "ack_id": ack.get("ack_id") if isinstance(ack, dict) else None,
                "source_type": trace_stub.get("source_type") if isinstance(trace_stub, dict) else None,
                "status": "success" if ok else "validation_failed",
            },
            ensure_ascii=False,
        )
    )
    return 0 if ok else 3


if __name__ == "__main__":
    raise SystemExit(main())
