#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Voice-Qianwen-002 — Evaluate governed voice provider entry skeleton (offline).
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from capabilities.voice.output.governed_voice_provider_entry_v0 import (
    append_jsonl,
    load_voice_governance_inputs_v0,
    run_governed_voice_provider_entry_skeleton_v0,
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _utc_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--governance-root", required=True)
    ap.add_argument("--provider-mode", choices=("online_prefer_qwen", "offline_only"), required=True)
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    repo = _repo_root()
    gov = Path(args.governance_root)
    if not gov.is_absolute():
        gov = repo / gov

    out = Path(args.output_root) if args.output_root else repo / "logs" / f"voice_qwen_governed_entry_002_{args.provider_mode}_{_utc_tag()}"
    out.mkdir(parents=True, exist_ok=True)

    entries, audits, sel_rows, trace_rows, replay_rows, white_rows = run_governed_voice_provider_entry_skeleton_v0(
        governance_root=str(gov),
        provider_mode=args.provider_mode,
    )

    inputs = load_voice_governance_inputs_v0(str(gov))
    shutil.copy2(gov / "voice_output_governance_decisions.json", out / "_source_voice_output_governance_decisions.json")

    summary: Dict[str, Any] = {
        "phase": "Phase-Voice-Qianwen-002",
        "provider_mode": args.provider_mode,
        "governance_root": str(gov),
        "output_root": str(out),
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "contract_defined": True,
        "static_verifier_passed": None,
        "runtime_wiring_done": False,
        "real_qwen_invoked": False,
        "real_tts_invoked": False,
        "default_policy_changed": False,
        "samples": len(entries),
        "entry_allowed_count": sum(1 for e in entries if e.get("entry_allowed")),
        "selected_qwen_count": sum(1 for e in entries if e.get("provider_selection", {}).get("selected_provider") == "qwen"),
        "selected_piper_count": sum(1 for e in entries if e.get("provider_selection", {}).get("selected_provider") == "piper"),
        "selected_none_count": sum(1 for e in entries if e.get("provider_selection", {}).get("selected_provider") == "none"),
    }

    (out / "voice_qwen_governed_entry_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "voice_qwen_governed_entry_inputs.json").write_text(
        json.dumps(
            {
                "governance_root": str(gov),
                "provider_mode": args.provider_mode,
                "inputs_manifest": inputs,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (out / "voice_qwen_governed_entry_decisions.json").write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "voice_speakability_audits.json").write_text(json.dumps(audits, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "voice_provider_selection_dry_run.json").write_text(json.dumps(sel_rows, ensure_ascii=False, indent=2), encoding="utf-8")

    append_jsonl(out / "voice_qwen_governed_entry_trace.jsonl", trace_rows)
    append_jsonl(out / "voice_qwen_governed_entry_replay.jsonl", replay_rows)
    append_jsonl(out / "voice_qwen_governed_entry_whitebox.jsonl", white_rows)

    notes = [
        "# Phase-Voice-Qianwen-002 evaluation notes",
        "",
        f"- governance_root: `{gov}`",
        f"- provider_mode: `{args.provider_mode}`",
        f"- output_root: `{out}`",
        "",
        "Dry-run only: no DashScope, no Piper executable, no playback.",
        "",
        "## Contract flags",
        "",
        "- `runtime_wiring_done=false` (skeleton only)",
        "- `real_qwen_invoked=false`, `real_tts_invoked=false`",
        "",
    ]
    (out / "evaluation_notes.md").write_text("\n".join(notes), encoding="utf-8")

    print(json.dumps({"ok": True, "output_root": str(out)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
