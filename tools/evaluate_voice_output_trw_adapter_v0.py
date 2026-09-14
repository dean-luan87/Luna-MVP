#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phase-Voice-OutputGovernance-004
Evaluate Voice Output TRW Adapter v0 (offline).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _now() -> float:
    return time.time()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-root", required=True, help="Phase-002 output root")
    ap.add_argument("--output-root", required=True, help="Output root")
    args = ap.parse_args()

    from capabilities.voice.output.voice_output_trw_adapter_v0 import (  # type: ignore
        run_voice_output_trw_adapter_v0,
    )

    t0 = _now()
    records, summary, timeline, mapping_report = run_voice_output_trw_adapter_v0(input_root=args.input_root)

    out_root = Path(args.output_root)
    out_root.mkdir(parents=True, exist_ok=True)

    # Main JSON outputs
    _write_json(out_root / "voice_output_trw_adapter_summary.json", summary)
    _write_json(out_root / "voice_output_trw_records.json", [r.__dict__ for r in records])
    _write_json(out_root / "voice_output_stage_timeline.json", timeline)
    _write_json(out_root / "voice_output_extractor_mapping_report.json", mapping_report)

    # Whitebox extension as separate view
    wb_ext = [
        {
            "record_id": r.record_id,
            "request_id": r.request_id,
            "stage_name": r.stage_name,
            "stage_order": r.stage_order,
            "whitebox_extension": r.whitebox_extension,
        }
        for r in records
        if r.whitebox_extension
    ]
    _write_json(out_root / "voice_output_whitebox_extension.json", wb_ext)

    # Adapter trace/replay/whitebox JSONL
    trace_p = out_root / "voice_output_trw_adapter_trace.jsonl"
    replay_p = out_root / "voice_output_trw_adapter_replay.jsonl"
    whitebox_p = out_root / "voice_output_trw_adapter_whitebox.jsonl"
    for p in (trace_p, replay_p, whitebox_p):
        try:
            p.unlink()
        except Exception:
            pass

    for r in records:
        _append_jsonl(
            trace_p,
            {
                "type": "voice_output_trw_adapter_trace_v0",
                "timestamp": _now(),
                "request_id": r.request_id,
                "stage_namespace": r.stage_namespace,
                "stage_name": r.stage_name,
                "stage_order": r.stage_order,
                "status": r.status,
                "reason": r.reason,
                "hard_audit": r.hard_audit,
            },
        )
        _append_jsonl(
            replay_p,
            {
                "type": "voice_output_trw_adapter_replay_v0",
                "timestamp": _now(),
                "request_id": r.request_id,
                "decision_ref": r.decision_ref,
                "audit_envelope_ref": r.audit_envelope_ref,
                "input_ref": r.input_ref,
                "output_ref": r.output_ref,
            },
        )
        _append_jsonl(
            whitebox_p,
            {
                "type": "voice_output_trw_adapter_whitebox_v0",
                "timestamp": _now(),
                "request_id": r.request_id,
                "stage_name": r.stage_name,
                "whitebox_extension": r.whitebox_extension,
            },
        )

    (out_root / "evaluation_notes.md").write_text(
        "\n".join(
            [
                "# Phase-Voice-OutputGovernance-004 Evaluation Notes",
                "",
                f"- input_root: `{args.input_root}`",
                f"- output_root: `{str(out_root)}`",
                f"- record_count: {len(records)}",
                f"- duration_ms: {int((_now()-t0)*1000)}",
                "",
                "- boundary: offline adapter only; no runtime wiring; no TTS/playback.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(str(out_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

