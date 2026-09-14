#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-011 — Run OCR Stage-2 controlled provider trial v0.

Absolute paths only.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.guarded_trial.ocr_stage2_controlled_provider_executor_v0 import (  # noqa: E402
    run_ocr_stage2_controlled_provider_invocation_v0,
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
    ap.add_argument("--approval-root", required=True)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--input-image", default=None, help="Optional override; must match approval snapshot")
    args = ap.parse_args()

    approval_root = Path(args.approval_root).expanduser()
    output_root = Path(args.output_root).expanduser()
    if not approval_root.is_absolute() or not output_root.is_absolute():
        raise SystemExit("ERROR: --approval-root and --output-root must be absolute paths")
    approval_root = approval_root.resolve()
    output_root = output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    input_override: Optional[str] = None
    if args.input_image is not None:
        p = Path(args.input_image).expanduser()
        if not p.is_absolute():
            raise SystemExit("ERROR: --input-image must be an absolute path when provided")
        input_override = str(p.resolve())

    trial = run_ocr_stage2_controlled_provider_invocation_v0(
        approval_root=str(approval_root),
        input_image_override=input_override,
    )

    details = trial.get("details") or {}
    input_match = details.get("input_snapshot_match") or {}
    provider_sel = details.get("provider_selection") or {}
    provider_payload = details.get("provider_payload") or {}
    candidate = details.get("raw_text_candidate") or {}
    candidate_val = details.get("raw_text_candidate_validation") or {}

    _write_json(output_root / "ocr_stage2_controlled_provider_summary.json", {"phase": "Phase-Mainline-GuardedTrial-011", "ts": _now_iso(), "output_root": str(output_root)})
    _write_json(output_root / "ocr_stage2_input_snapshot_match.json", input_match)
    _write_json(output_root / "ocr_stage2_provider_selection.json", provider_sel)
    _write_json(output_root / "ocr_stage2_provider_invocation_result.json", provider_payload)
    _write_json(output_root / "ocr_stage2_raw_text_candidate.json", candidate)
    _write_json(output_root / "ocr_stage2_raw_text_candidate_schema_validation.json", candidate_val)
    _write_json(
        output_root / "ocr_stage2_provider_latency_summary.json",
        {"latency_ms": (candidate.get("provider_metadata") or {}).get("latency_ms"), "provider": trial.get("provider_selected")},
    )
    _write_json(
        output_root / "ocr_stage2_abort_rollback_report.json",
        {
            "abort_triggered": trial.get("abort_triggered"),
            "abort_reason": trial.get("abort_reason"),
            "rollback_commands": [
                "unset LUNA_ENABLE_OCR_GUARDED_TRIAL_V1",
                "unset LUNA_OCR_TRIAL_ALLOW_PROVIDER_INVOCATION",
                "export LUNA_DISABLE_ALL_GUARDED_TRIALS=true",
            ],
        },
    )
    _write_json(output_root / "ocr_stage2_post_trial_report.json", trial.get("post_trial_report"))

    _append_jsonl(output_root / "ocr_stage2_controlled_provider_trace.jsonl", {"type": "ocr_s2_trace_v0", "ts": _now_iso(), "trial_id": trial.get("trial_id")})
    _append_jsonl(output_root / "ocr_stage2_controlled_provider_replay.jsonl", {"type": "ocr_s2_replay_v0", "ts": _now_iso(), "trial_id": trial.get("trial_id")})
    _append_jsonl(output_root / "ocr_stage2_controlled_provider_whitebox.jsonl", {"type": "ocr_s2_whitebox_v0", "ts": _now_iso(), "trial_id": trial.get("trial_id"), "hard_audit": trial.get("hard_audit")})

    notes = "\n".join(
        [
            "# OCR Stage-2 Controlled Provider Invocation v0 (Phase-011)",
            "",
            f"- **approval_root:** `{str(approval_root)}`",
            f"- **output_root:** `{str(output_root)}`",
            f"- **trial_id:** `{trial.get('trial_id')}`",
            f"- **provider_selected:** `{trial.get('provider_selected')}`",
            f"- **input_snapshot_match:** `{trial.get('input_snapshot_match')}`",
            f"- **post_trial_recommendation:** `{(trial.get('post_trial_report') or {}).get('post_trial_recommendation')}`",
            "",
            "## Hard boundary",
            "",
            "- raw_text only; no semantic interpretation",
            "- no MidPlatform / SceneDelta / WorldContext",
            "- no navigation / TTS / Qwen / world write / hive upload",
            "- no network request",
            "",
        ]
    )
    (output_root / "execution_notes.md").write_text(notes + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "ok": True,
                "output_root": str(output_root),
                "trial_id": trial.get("trial_id"),
                "input_snapshot_match": trial.get("input_snapshot_match"),
                "provider_selected": trial.get("provider_selected"),
                "post_trial_recommendation": (trial.get("post_trial_report") or {}).get("post_trial_recommendation"),
            },
            ensure_ascii=False,
        )
    )
    rec = (trial.get("post_trial_report") or {}).get("post_trial_recommendation")
    return 0 if rec in {"GO_next_window", "CONDITIONAL_GO_repeat"} else 2


if __name__ == "__main__":
    raise SystemExit(main())

