#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Voice Command Ownership Gate Policy v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


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
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    checks = 0

    def ok(c: bool, name: str) -> None:
        nonlocal checks
        if c:
            checks += 1
        else:
            blockers.append(name)

    files = {
        "summary": "voice_command_ownership_gate_policy_v1_summary.json",
        "policy_matrix": "voice_command_ownership_gate_policy_matrix_v1.json",
        "simulated_cases": "voice_command_ownership_simulated_voice_input_cases_v1.json",
        "decisions": "voice_command_ownership_gate_decision_candidates_v1.json",
        "speaker_matrix": "voice_command_ownership_speaker_ownership_matrix_v1.json",
        "addressing_matrix": "voice_command_ownership_addressing_matrix_v1.json",
        "context_matrix": "voice_command_ownership_conversation_context_matrix_v1.json",
        "entrypoint_matrix": "voice_command_ownership_entrypoint_decision_matrix_v1.json",
        "safety_keyword_matrix": "voice_command_ownership_safety_keyword_exception_matrix_v1.json",
        "voiceprint_schema": "voice_command_ownership_voiceprint_evidence_candidate_schema_v1.json",
        "emotion_schema": "voice_command_ownership_voice_emotion_evidence_candidate_schema_v1.json",
        "handoffs": "voice_command_ownership_handoff_contracts_v1.json",
        "boundary": "voice_command_ownership_gate_boundary_report_v1.json",
        "no_write": "voice_command_ownership_gate_no_write_boundary_report_v1.json",
        "final": "voice_command_ownership_gate_final_decision_v1.json",
        "audit": "voice_command_ownership_gate_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(
            root / "voice_command_ownership_gate_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(s.get("policy_scope") == "voice_command_ownership_gate_policy_only", "scope")
    ok(s.get("based_on_safety_task_arbitration") is True, "safety_arb")
    ok(s.get("voiceprint_schema_defined") is True, "vp_schema")
    ok(s.get("voice_emotion_schema_defined") is True, "emo_schema")
    ok(s.get("runtime_asr_invoked") is False, "no_asr")
    ok(s.get("runtime_voiceprint_invoked") is False, "no_vp")
    ok(s.get("runtime_diarization_invoked") is False, "no_diar")
    ok(s.get("runtime_audio_recorded") is False, "no_audio")
    ok(s.get("speech_gate_invoked") is False, "no_gate")
    ok(s.get("vop_invoked") is False, "no_vop")
    ok(s.get("task_state_committed_now") is False, "no_commit")
    ok(s.get("world_model_written") is False, "no_wm")

    pm = data["policy_matrix"]
    for state in (
        "OWNER_CONFIRMED",
        "OWNER_PROBABLE",
        "OWNER_UNCERTAIN",
        "NON_OWNER_PROBABLE",
        "NON_OWNER_CONFIRMED",
    ):
        ok(state in (pm.get("ownership_states") or []), f"own_{state}")

    cases = data["simulated_cases"].get("cases") or []
    ok(len(cases) >= 16, "cases_16")

    decs = data["decisions"].get("candidates") or []
    ok(len(decs) >= 16, "decs_16")
    for d in decs:
        ok(d.get("runtime_action_committed") is False, "dec_no_runtime")
        blocked = d.get("blocked_entrypoints") or []
        if d.get("ownership_state") in ("NON_OWNER_CONFIRMED", "NON_OWNER_PROBABLE"):
            ok("task_commit" in blocked, f"block_commit_{d.get('ownership_gate_decision_candidate_id')}")
            ok("navigation_action" in blocked, "block_nav")
            ok("memory_write" in blocked, "block_mem")
            ok("world_model_write" in blocked, "block_wm")

    case06 = next((d for d in decs if d.get("voice_input_candidate_id") == "voice_input_case_06"), None)
    ok(case06 and "task_control_candidate" not in (case06.get("allowed_entrypoints") or []), "non_owner_no_tc")

    case09 = next((d for d in decs if d.get("voice_input_candidate_id") == "voice_input_case_09"), None)
    ok(case09 and "interruption_classifier" not in (case09.get("allowed_entrypoints") or []), "phone_no_interrupt")

    case10 = next((d for d in decs if d.get("voice_input_candidate_id") == "voice_input_case_10"), None)
    ok(case10 and "interruption_classifier" not in (case10.get("allowed_entrypoints") or []), "human_conv_no_interrupt")

    case11 = next((d for d in decs if d.get("voice_input_candidate_id") == "voice_input_case_11"), None)
    ok(case11 and "task_control_candidate" not in (case11.get("allowed_entrypoints") or []), "media_no_control")

    case12 = next((d for d in decs if d.get("voice_input_candidate_id") == "voice_input_case_12"), None)
    ok(case12 and len(case12.get("allowed_entrypoints") or []) == 0, "announce_no_allow")

    case13 = next((d for d in decs if d.get("voice_input_candidate_id") == "voice_input_case_13"), None)
    ok(case13 and case13.get("safety_only_allowed") is True, "case13_safety_only")
    ok(
        case13
        and "safety_observation_candidate" in (case13.get("allowed_entrypoints") or [])
        and "task_control_candidate" not in (case13.get("allowed_entrypoints") or []),
        "case13_safety_path",
    )

    case08 = next((d for d in decs if d.get("voice_input_candidate_id") == "voice_input_case_08"), None)
    ok(case08 and case08.get("requires_confirmation") is True, "helper_confirm")

    vp = data["voiceprint_schema"]
    ok(vp.get("speaker_identity_fact") is False, "vp_not_fact")
    ok(vp.get("speaker_identity_write_allowed") is False, "vp_no_write")
    ok(vp.get("voiceprint_model_invoked") is False, "vp_no_model")

    em = data["emotion_schema"]
    ok(em.get("emotion_fact") is False, "emo_not_fact")
    ok(em.get("emotional_context_write_allowed") is False, "emo_no_write")

    hb = data["handoffs"]
    ok("to_voice_interruption_governance" in hb, "handoff_interrupt")

    bnd = data["boundary"]
    ok(bnd.get("boundary_ok") is True, "boundary_ok")
    ok(bnd.get("policy_only") is True, "policy_only")

    nw = data["no_write"]
    ok(nw.get("violations") == [], "violations")

    fin = data["final"]
    ok(
        fin.get("final_decision") == "VOICE_COMMAND_OWNERSHIP_GATE_POLICY_READY_FOR_INTERRUPTION_GOVERNANCE",
        "final_decision",
    )

    aud = data["audit"]
    ok(aud.get("runtime_routing_changed") is False if "runtime_routing_changed" in aud else True, "no_routing")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 64,
        "blockers": blockers,
        "final_decision": fin.get("final_decision"),
        "phase": "Voice-Command-Ownership-Gate-Policy-v1-001",
    }
    _write_json(root / "voice_command_ownership_gate_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
