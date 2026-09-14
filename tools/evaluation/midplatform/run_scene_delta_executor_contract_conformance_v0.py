#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-MidPlatform-Scene-Delta-Executor-Contract-Conformance-001 — static contract vs local skeleton."""

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
        "--mock-handshake-root",
        default="",
        help="Directory with scene_delta_mock_executor_request.json",
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    default_h = Path(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/scene_delta_executor_mock_handshake_smoke_v0"
    )
    hr = Path(args.mock_handshake_root).expanduser() if args.mock_handshake_root.strip() else default_h
    if not hr.is_absolute():
        hr = (WS_ROOT / hr).resolve()
    in_root = _require_abs(str(hr), "--mock-handshake-root (resolved)")

    req_p = in_root / "scene_delta_mock_executor_request.json"
    ack_p = in_root / "scene_delta_mock_executor_ack.json"
    comp_p = in_root / "scene_delta_mock_handshake_compatibility_report.json"
    aud_p = in_root / "scene_delta_mock_handshake_audit_report.json"

    for label, p in (
        ("mock_request", req_p),
        ("mock_ack", ack_p),
        ("handshake_compatibility", comp_p),
        ("handshake_audit", aud_p),
    ):
        if not p.is_file():
            raise SystemExit(f"ERROR: missing {label}: {p}")

    request = _read_json(req_p)
    ack = _read_json(ack_p)
    compat = _read_json(comp_p)
    audit = _read_json(aud_p)

    from capabilities.midplatform.scene_delta_executor_contract_conformance_v0 import run_contract_conformance_v0

    skeleton, req_matrix, ack_matrix, gap, nw_rep, conf_audit, summary, blocking = run_contract_conformance_v0(
        request=request if isinstance(request, dict) else {},
        ack=ack if isinstance(ack, dict) else {},
        handshake_compat=compat if isinstance(compat, dict) else {},
        handshake_audit=audit if isinstance(audit, dict) else {},
    )

    summary["input_mock_handshake_root"] = str(in_root)
    summary["input_paths"] = {
        "mock_request": str(req_p.resolve()),
        "mock_ack": str(ack_p.resolve()),
        "handshake_compatibility": str(comp_p.resolve()),
        "handshake_audit": str(aud_p.resolve()),
    }

    _write_json(out / "scene_delta_executor_contract_skeleton_v0.json", skeleton)
    _write_json(out / "scene_delta_executor_contract_conformance_summary.json", summary)
    _write_json(out / "scene_delta_executor_request_conformance_matrix.json", req_matrix)
    _write_json(out / "scene_delta_executor_ack_conformance_matrix.json", ack_matrix)
    _write_json(out / "scene_delta_executor_contract_gap_report.json", gap)
    _write_json(out / "scene_delta_executor_no_write_contract_report.json", nw_rep)
    _write_json(out / "scene_delta_executor_contract_conformance_audit_report.json", conf_audit)

    (out / "scene_delta_executor_contract_conformance_notes.md").write_text(
        "# Phase-MidPlatform-Scene-Delta-Executor-Contract-Conformance-001\n\n"
        "Static conformance of mock **request/ACK** against **`scene_delta_executor_contract_skeleton_v0`** "
        "(**local_skeleton** — not production executor OpenAPI/proto). "
        "**No** real executor, **no** writes, **no** DB/WAL/rehearsal log.\n",
        encoding="utf-8",
    )

    if blocking:
        _write_json(out / "scene_delta_executor_contract_conformance_blocking_errors.json", {"errors": blocking})

    ok = not blocking
    print(
        json.dumps(
            {
                "scene_delta_executor_contract_conformance_smoke_root": str(out),
                "contract_reference_mode": summary.get("contract_reference_mode"),
                "status": "success" if ok else "blocking_failed",
            },
            ensure_ascii=False,
        )
    )
    return 0 if ok else 3


if __name__ == "__main__":
    raise SystemExit(main())
