#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-010 — Prepare OCR Stage-2 provider approval gate artifacts.

All paths must be ABSOLUTE (--static-config-root, --input-image, --output-root).
Does not invoke OCR providers/models or network.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.guarded_trial.ocr_stage2_provider_approval_gate_v0 import (  # noqa: E402
    run_ocr_stage2_provider_approval_gate_v0,
    validate_ocr_provider_dependency_snapshot_v0,
    validate_ocr_provider_credentials_snapshot_v0,
    validate_ocr_input_sample_snapshot_v0,
    validate_ocr_fallback_snapshot_v0,
    validate_ocr_controlled_provider_runbook_snapshot_v0,
)


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--static-config-root", required=True)
    ap.add_argument("--input-image", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    for label, pth in (
        ("--static-config-root", args.static_config_root),
        ("--input-image", args.input_image),
        ("--output-root", args.output_root),
    ):
        pp = Path(pth).expanduser()
        if not pp.is_absolute():
            raise SystemExit(f"ERROR: {label} must be an absolute path, got: {pth}")

    out_root = Path(args.output_root).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    scr = Path(args.static_config_root).expanduser().resolve()
    gate = run_ocr_stage2_provider_approval_gate_v0(
        static_config_root=str(scr),
        input_image_path=str(Path(args.input_image).expanduser()),
    )

    dep = validate_ocr_provider_dependency_snapshot_v0()
    cred = validate_ocr_provider_credentials_snapshot_v0()
    inp_full = validate_ocr_input_sample_snapshot_v0(str(Path(args.input_image).expanduser()))
    fb = validate_ocr_fallback_snapshot_v0()
    rb = validate_ocr_controlled_provider_runbook_snapshot_v0(scr)

    _write_json(
        out_root / "ocr_stage2_provider_approval_summary.json",
        {
            "phase": "Phase-Mainline-GuardedTrial-010",
            "ts": _now_iso(),
            "output_root": str(out_root),
            "static_config_root": str(scr),
            "input_image": str(Path(args.input_image).expanduser().resolve()),
            "approval_gate_result": gate.get("approval_gate_result"),
        },
    )
    _write_json(out_root / "ocr_stage2_provider_dependency_snapshot.json", dep)
    _write_json(out_root / "ocr_stage2_provider_credentials_snapshot.json", cred)
    _write_json(out_root / "ocr_stage2_input_sample_snapshot.json", {k: v for k, v in inp_full.items() if k != "blockers"})
    _write_json(out_root / "ocr_stage2_fallback_snapshot.json", fb)
    _write_json(
        out_root / "ocr_stage2_controlled_provider_runbook_snapshot.json",
        {"runbook_path": rb.get("path"), "runbook": rb.get("runbook"), "found": rb.get("found")},
    )
    _write_json(out_root / "ocr_stage2_provider_approval_gate_report.json", gate)

    aid = gate.get("approval_id") or "unknown"
    _append_jsonl(out_root / "ocr_stage2_provider_approval_trace.jsonl", {"type": "ocr_stage2_approval_trace_v0", "ts": _now_iso(), "approval_id": aid})
    _append_jsonl(out_root / "ocr_stage2_provider_approval_replay.jsonl", {"type": "ocr_stage2_approval_replay_v0", "ts": _now_iso(), "approval_id": aid})
    _append_jsonl(out_root / "ocr_stage2_provider_approval_whitebox.jsonl", {"type": "ocr_stage2_approval_whitebox_v0", "ts": _now_iso(), "approval_id": aid, "provider_invoked": False})

    notes = "\n".join(
        [
            "# OCR Stage-2 Provider Approval Gate v0 (Phase-010)",
            "",
            f"- **static_config_root:** `{str(scr)}`",
            f"- **input_image:** `{str(Path(args.input_image).expanduser().resolve())}`",
            f"- **output_root:** `{str(out_root)}`",
            f"- **approval_gate_result:** `{gate.get('approval_gate_result')}`",
            "",
            "## Scope",
            "",
            "- Pre-execution approval only; **no** OCR provider/model/network/camera/video.",
            "- Voice interaction main chain is **not** wired; voice governance artifacts are not full ASR/dialog runtime.",
            "",
        ]
    )
    (out_root / "approval_notes.md").write_text(notes + "\n", encoding="utf-8")

    print(
        json.dumps(
            {"ok": True, "output_root": str(out_root), "approval_gate_result": gate.get("approval_gate_result")},
            ensure_ascii=False,
        )
    )
    return 0 if gate.get("approval_gate_result") in {"GO", "CONDITIONAL_GO"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
