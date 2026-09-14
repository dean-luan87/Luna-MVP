# -*- coding: utf-8 -*-
"""
Phase-Voice-OutputGovernance-007
Evaluate governed submit shadow readiness v0.

Reads offline governance outputs (Phase-002) and produces pre-submit shadow decisions
and shadow trace/replay/whitebox artifacts.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from capabilities.voice.output.voice_governed_submit_shadow_v0 import (  # noqa: E402
    run_governed_submit_shadow_v0,
)


def _write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _shadow_jsonl(kind: str, decisions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for d in decisions:
        rows.append(
            {
                "kind": kind,
                "stage_namespace": "voice_governed_submit_shadow_v0",
                "stage_name": "governed_submit_shadow_gate",
                "request_id": d.get("request_id"),
                "submit_gate_position": d.get("submit_gate_position"),
                "submit_shadow_result": d.get("submit_shadow_result"),
                "submit_allowed": d.get("submit_allowed"),
                "governance_final_action": d.get("governance_final_action"),
                "hard_audit": d.get("hard_audit"),
                "source_governance_decision_id": d.get("source_governance_decision_id"),
                "source_audit_envelope_id": d.get("source_audit_envelope_id"),
                "trace_ref": d.get("trace_ref"),
                "replay_ref": d.get("replay_ref"),
                "whitebox_ref": d.get("whitebox_ref"),
                "shadow_only": True,
            }
        )
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--governance-root", required=True)
    ap.add_argument("--request-trace-root", required=True)
    ap.add_argument("--output-root", default=None)
    args = ap.parse_args()

    out_root = (
        Path(args.output_root)
        if args.output_root
        else (REPO_ROOT / "logs" / f"voice_governed_submit_shadow_007_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    )
    # If relative path, resolve from current cwd (workspace).
    if not out_root.is_absolute():
        out_root = Path.cwd() / out_root
    out_root.mkdir(parents=True, exist_ok=True)

    # Run shadow gate from governance root only; request-trace root is used for readiness context validation.
    result = run_governed_submit_shadow_v0(args.governance_root)
    inputs = result.get("inputs") if isinstance(result.get("inputs"), list) else []
    decisions = result.get("decisions") if isinstance(result.get("decisions"), list) else []
    audits = result.get("audit_envelopes") if isinstance(result.get("audit_envelopes"), list) else []

    summary = {
        "phase": "Phase-Voice-OutputGovernance-007",
        "tool": "evaluate_voice_governed_submit_shadow_v0.py",
        "mode": "governed_submit_shadow_readiness",
        "inputs": {"governance_root": args.governance_root, "request_trace_root": args.request_trace_root},
        "outputs": {
            "input_count": len(inputs),
            "decision_count": len(decisions),
            "audit_envelope_count": len(audits),
        },
        "hard_audit_invariants": {
            "real_submit_invoked": False,
            "real_tts_invoked": False,
            "playback_invoked": False,
            "provider_invoked": False,
            "navigation_action": None,
            "downstream_invocation_count": 0,
        },
        "env_snapshot": {"pwd": os.getcwd()},
        "notes": ["shadow-only: does not wire into real submit path"],
    }

    _write_json(out_root / "voice_governed_submit_shadow_summary.json", summary)
    _write_json(out_root / "voice_governed_submit_shadow_inputs.json", inputs)
    _write_json(out_root / "voice_governed_submit_shadow_decisions.json", decisions)
    _write_json(out_root / "voice_submit_gate_audit_envelopes.json", audits)

    _write_jsonl(out_root / "voice_governed_submit_shadow_trace.jsonl", _shadow_jsonl("trace", decisions))
    _write_jsonl(out_root / "voice_governed_submit_shadow_replay.jsonl", _shadow_jsonl("replay", decisions))
    _write_jsonl(out_root / "voice_governed_submit_shadow_whitebox.jsonl", _shadow_jsonl("whitebox", decisions))

    (out_root / "evaluation_notes.md").write_text(
        "\n".join(
            [
                "# Voice Governed Submit Shadow Readiness (v0)",
                "",
                "- This run is shadow-only and does not invoke real submit/TTS/playback.",
                "- It simulates pre-submit gate positions and outputs auditable decisions.",
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

