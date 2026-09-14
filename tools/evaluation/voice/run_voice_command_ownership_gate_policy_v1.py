#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Voice-Command-Ownership-Gate-Policy-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("voice_command_ownership_gate_policy_v1_summary.json", "summary"),
    ("voice_command_ownership_gate_policy_matrix_v1.json", "policy_matrix"),
    ("voice_command_ownership_gate_input_intake_matrix_v1.json", "intake"),
    ("voice_command_ownership_simulated_voice_input_cases_v1.json", "simulated_cases"),
    ("voice_command_ownership_gate_decision_candidates_v1.json", "decisions"),
    ("voice_command_ownership_speaker_ownership_matrix_v1.json", "speaker_matrix"),
    ("voice_command_ownership_addressing_matrix_v1.json", "addressing_matrix"),
    ("voice_command_ownership_conversation_context_matrix_v1.json", "context_matrix"),
    ("voice_command_ownership_entrypoint_decision_matrix_v1.json", "entrypoint_matrix"),
    ("voice_command_ownership_safety_keyword_exception_matrix_v1.json", "safety_keyword_matrix"),
    ("voice_command_ownership_voiceprint_evidence_candidate_schema_v1.json", "voiceprint_schema"),
    ("voice_command_ownership_voiceprint_candidate_matrix_v1.json", "voiceprint_matrix"),
    ("voice_command_ownership_voice_emotion_evidence_candidate_schema_v1.json", "emotion_schema"),
    ("voice_command_ownership_voice_emotion_candidate_matrix_v1.json", "emotion_matrix"),
    ("voice_command_ownership_handoff_contracts_v1.json", "handoffs"),
    ("voice_command_ownership_gate_decision_trace_v1.json", "trace"),
    ("voice_command_ownership_gate_final_decision_v1.json", "final"),
    ("voice_command_ownership_gate_boundary_report_v1.json", "boundary"),
    ("voice_command_ownership_gate_metrics_candidate_report_v1.json", "metrics"),
    ("voice_command_ownership_gate_benchmark_link_report_v1.json", "benchmark_link"),
    ("voice_command_ownership_gate_system_health_report_v1.json", "health_report"),
    ("voice_command_ownership_gate_no_write_boundary_report_v1.json", "no_write"),
    ("voice_command_ownership_gate_simulation_context_report_v1.json", "sim_report"),
    ("voice_command_ownership_gate_non_claims_report_v1.json", "non_claims"),
    ("voice_command_ownership_gate_open_followups_v1.json", "followups"),
    ("voice_command_ownership_gate_audit_report_v1.json", "audit"),
]


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "voice").is_dir():
            return parent
    return here.parents[3]


WS_ROOT = _find_ws_root()
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--safety-task-arbitration-root", required=True)
    ap.add_argument("--basic-navigation-loop-root", required=True)
    ap.add_argument("--voice-dialogue-runtime-root", required=True)
    ap.add_argument("--vop-adapter-root", required=True)
    ap.add_argument("--navigation-speech-adapter-root", required=True)
    ap.add_argument("--task-manager-runtime-root", required=True)
    ap.add_argument("--midplatform-task-state-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--stc-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    ap.add_argument("--workspace-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.voice.voice_command_ownership_gate_policy_v1 import (
        run_voice_command_ownership_gate_policy_v1,
    )

    result = run_voice_command_ownership_gate_policy_v1(
        safety_task_arbitration_root=str(_require_abs(args.safety_task_arbitration_root, "safety_arb")),
        basic_navigation_loop_root=str(_require_abs(args.basic_navigation_loop_root, "nav_loop")),
        voice_dialogue_runtime_root=str(_require_abs(args.voice_dialogue_runtime_root, "voice_dialogue")),
        vop_adapter_root=str(_require_abs(args.vop_adapter_root, "vop")),
        navigation_speech_adapter_root=str(_require_abs(args.navigation_speech_adapter_root, "speech_adapter")),
        task_manager_runtime_root=str(_require_abs(args.task_manager_runtime_root, "tm_rt")),
        midplatform_task_state_root=str(_require_abs(args.midplatform_task_state_root, "mp_ts")),
        ocr_activation_root=str(_require_abs(args.ocr_activation_root, "ocr_act")),
        stc_root=str(_require_abs(args.stc_root, "stc")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        workspace_root=str(_require_abs(args.workspace_root, "workspace")),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "voice_command_ownership_gate_notes.md").write_text(
        "# Voice Command Ownership Gate Policy v1\n\n"
        f"Final: `{result['final']['final_decision']}`\n"
        f"Next: `{result['final']['recommended_next_phase']}`\n"
        f"Cases: {result['final']['simulated_case_count']}\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output_root": str(out),
                "final_decision": result["final"]["final_decision"],
                "case_count": result["final"]["simulated_case_count"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
