#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-VoiceInteraction-Readiness-001 — Verifier for voice interaction readiness outputs.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    root = Path(args.output_root).expanduser().resolve()
    blockers: List[str] = []

    required = [
        "voice_interaction_readiness_summary.json",
        "voice_asr_readiness_matrix.json",
        "voice_session_readiness_matrix.json",
        "voice_semantic_context_readiness_matrix.json",
        "voice_qianwen_interaction_readiness_matrix.json",
        "voice_output_governance_readiness_matrix.json",
        "voice_playback_audio_readiness_matrix.json",
        "voice_trace_replay_audit_readiness_matrix.json",
        "voice_interaction_gap_register.json",
        "voice_interaction_next_step_recommendation.json",
        "voice_interaction_readiness_notes.md",
    ]
    for fn in required:
        if not (root / fn).is_file():
            blockers.append(f"A_missing:{fn}")

    if not blockers:
        sm = _read_json(root / "voice_interaction_readiness_summary.json")
        if sm.get("full_voice_interaction_connected") is True:
            blockers.append("J_full_voice_must_not_be_true")
        c = sm.get("constraints") or {}
        if c.get("provider_invoked_by_tool") is not False:
            blockers.append("K_provider_invoked")
        if c.get("real_tts_invoked") is not False:
            blockers.append("L_real_tts")
        if c.get("playback_executed") is not False:
            blockers.append("M_playback_executed")
        if c.get("runtime_mutation") is not False:
            blockers.append("N_runtime_mutation")
        if sm.get("qianwen_first_policy_preserved") is not True:
            blockers.append("O_qianwen_first_not_preserved")
        if sm.get("tts_fallback_preserved") is not True:
            blockers.append("O_tts_fallback_not_preserved")

        nx = _read_json(root / "voice_interaction_next_step_recommendation.json")
        if not isinstance(nx, dict) or not nx.get("recommended_phases"):
            blockers.append("P_missing_next_step")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "phase": "Phase-VoiceInteraction-Readiness-001",
        "verdict": verdict,
        "blockers": blockers,
        "output_root": str(root),
    }
    (root / "voice_interaction_readiness_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
