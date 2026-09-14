#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-VoiceInteraction-Readiness-002 — Verifier for ASR boundary contract review outputs.
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
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    repo = Path(args.repo_root).expanduser().resolve()
    root = Path(args.output_root).expanduser().resolve()
    blockers: List[str] = []

    voice_readiness_root: Path | None = None
    summary_path = root / "voice_asr_boundary_contract_summary.json"
    if not summary_path.is_file():
        blockers.append("missing_summary")
    else:
        sm = _read_json(summary_path)
        voice_readiness_root_str = sm.get("voice_readiness_input_root")
        if isinstance(voice_readiness_root_str, str) and voice_readiness_root_str:
            voice_readiness_root = Path(voice_readiness_root_str).expanduser().resolve()
            if not voice_readiness_root.is_dir():
                blockers.append("A_readiness_root_not_dir")
            else:
                # readable: can list + optional summary
                try:
                    _ = list(voice_readiness_root.iterdir())
                except OSError:
                    blockers.append("A_readiness_root_unreadable")
        else:
            blockers.append("A_readiness_root_missing_in_summary")

    arch_voice = repo / "docs" / "architecture" / "voice"
    if not (arch_voice / "LUNA_VOICE_ASR_BOUNDARY_CONTRACT_V0.md").is_file():
        blockers.append("B_missing_asr_boundary_doc")
    if not (repo / "capabilities" / "voice" / "input" / "asr_final_text_event_contract_v0.py").is_file():
        blockers.append("C_missing_final_text_contract_py")
    if not (arch_voice / "LUNA_VOICE_ASR_STATE_MACHINE_V0.md").is_file():
        blockers.append("D_missing_state_machine_doc")
    if not (arch_voice / "LUNA_VOICE_ASR_TRACE_REPLAY_AUDIT_CONTRACT_V0.md").is_file():
        blockers.append("E_missing_trace_doc_repo")
    if not (root / "voice_asr_trace_replay_audit_matrix.json").is_file():
        blockers.append("E_missing_trace_matrix_output")

    required_out = [
        "voice_asr_boundary_contract_summary.json",
        "voice_asr_final_text_event_schema.json",
        "voice_asr_state_machine_matrix.json",
        "voice_asr_trace_replay_audit_matrix.json",
        "voice_asr_fallback_suppress_matrix.json",
        "voice_asr_runtime_flag_matrix.json",
        "voice_asr_boundary_contract_notes.md",
    ]
    for fn in required_out:
        if not (root / fn).is_file():
            blockers.append(f"missing_output:{fn}")

    if not (arch_voice / "LUNA_VOICE_ASR_FALLBACK_SUPPRESS_POLICY_V0.md").is_file():
        blockers.append("F_missing_fallback_doc")

    rf_path = root / "voice_asr_runtime_flag_matrix.json"
    if rf_path.is_file():
        rf = _read_json(rf_path)
        if not rf.get("defaults_all_conservative_closed"):
            blockers.append("G_flags_not_conservative")
        for fl in rf.get("flags") or []:
            name = fl.get("name", "")
            dv = fl.get("default_value")
            if name == "LUNA_DISABLE_VOICE_ASR_RUNTIME_V1" and dv is not True:
                blockers.append("G_disable_must_default_true")
            if name.startswith("LUNA_ENABLE_VOICE_ASR_") and dv is not False:
                blockers.append(f"G_enable_must_default_false:{name}")

    if summary_path.is_file():
        sm = _read_json(summary_path)
        c = sm.get("constraints") or {}
        if c.get("asr_provider_invoked") is not False:
            blockers.append("H_asr_provider_invoked")
        if c.get("qianwen_invoked") is not False:
            blockers.append("I_qianwen_invoked")
        if c.get("tts_invoked") is not False:
            blockers.append("J_tts_invoked")
        if c.get("playback_executed") is not False:
            blockers.append("K_playback")
        if c.get("runtime_mutation") is not False:
            blockers.append("L_runtime_mutation")

        stm_path = root / "voice_asr_state_machine_matrix.json"
        if stm_path.is_file():
            stm = _read_json(stm_path)
            if stm.get("only_final_text_ready_allows_semantic_downstream") is not True:
                blockers.append("M_downstream_entry_rule")

    verdict = "GO" if not blockers else "NO_GO"
    report: Dict[str, Any] = {
        "phase": "Phase-VoiceInteraction-Readiness-002",
        "verdict": verdict,
        "blockers": blockers,
        "repo_root": str(repo),
        "output_root": str(root),
    }
    (root / "voice_asr_boundary_contract_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
