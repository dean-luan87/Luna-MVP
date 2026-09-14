#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phase-Voice-OutputGovernance-002
Verify Voice Output Governance Minimal Skeleton v0.

Checks (A–S) per phase contract; offline-only.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _read_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _read_jsonl(path: str) -> List[Dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        return []
    out: List[Dict[str, Any]] = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append(json.loads(ln))
        except Exception:
            continue
    return out


def _ok(check: str, passed: bool, **detail: Any) -> Dict[str, Any]:
    return {"check": check, "pass": bool(passed), **detail}


def _find_by_sample(arr: List[Dict[str, Any]], sample_id: str) -> Optional[Dict[str, Any]]:
    for x in arr:
        if str(x.get("sample_id") or "") == str(sample_id):
            return x
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True, help="Evaluation output root")
    args = ap.parse_args()

    root = Path(args.output_root)
    summary_p = root / "voice_output_governance_summary.json"
    inputs_p = root / "voice_output_governance_inputs.json"
    decisions_p = root / "voice_output_governance_decisions.json"
    provider_p = root / "voice_provider_health_states.json"
    audit_p = root / "voice_output_audit_envelopes.json"
    trace_p = root / "voice_output_trace.jsonl"
    replay_p = root / "voice_output_replay.jsonl"
    whitebox_p = root / "voice_output_whitebox.jsonl"

    results: List[Dict[str, Any]] = []

    # A. sample input readable
    try:
        inputs = _read_json(str(inputs_p))
        ok_a = isinstance(inputs, list) and len(inputs) > 0
        results.append(_ok("A_sample_input_readable", ok_a, count=(len(inputs) if isinstance(inputs, list) else 0)))
    except Exception as e:
        results.append(_ok("A_sample_input_readable", False, error=repr(e)))
        out = {"phase": "Phase-Voice-OutputGovernance-002", "all_pass": False, "results": results}
        (root / "verification_result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return 2

    # B. guard_v1_speakable_text importable
    try:
        from capabilities.voice.output.voice_output_governance_v0 import guard_v1_speakable_text  # type: ignore

        gr = guard_v1_speakable_text("test")
        ok_b = bool(getattr(gr, "guard_name", "") == "guard_v1_speakable_text")
        results.append(_ok("B_guard_importable", ok_b))
    except Exception as e:
        results.append(_ok("B_guard_importable", False, error=repr(e)))

    # C. SpeechGate exists
    try:
        from core.speech_gate import SpeechGate  # type: ignore

        _ = SpeechGate()
        results.append(_ok("C_speech_gate_exists", True))
    except Exception as e:
        results.append(_ok("C_speech_gate_exists", False, error=repr(e)))

    # Load other outputs
    decisions = _read_json(str(decisions_p)) if decisions_p.exists() else []
    providers = _read_json(str(provider_p)) if provider_p.exists() else []
    audits = _read_json(str(audit_p)) if audit_p.exists() else []
    trace = _read_jsonl(str(trace_p))
    replay = _read_jsonl(str(replay_p))
    whitebox = _read_jsonl(str(whitebox_p))

    # D. SpeechGate invoked in skeleton
    ok_d = False
    if isinstance(decisions, list) and decisions:
        ok_d = all(bool(((d.get("speech_gate_result") or {}).get("gate_invoked")) is True) for d in decisions if isinstance(d, dict))
    results.append(_ok("D_speech_gate_invoked", ok_d, decision_count=(len(decisions) if isinstance(decisions, list) else 0)))

    # E. decisions generated
    ok_e = isinstance(decisions, list) and len(decisions) == len(inputs)
    results.append(_ok("E_decisions_generated", ok_e, decisions=(len(decisions) if isinstance(decisions, list) else 0)))

    # Helper checks for specific samples
    def _decision(sample_id: str) -> Optional[Dict[str, Any]]:
        return _find_by_sample(decisions if isinstance(decisions, list) else [], sample_id)

    # F. expired request suppressed
    d_exp = _decision("expired_request")
    ok_f = bool(d_exp and d_exp.get("final_action") == "suppressed" and "expired" in str(((d_exp.get("suppression_result") or {}).get("suppression_reason"))))
    results.append(_ok("F_expired_suppressed", ok_f))

    # G. low priority not allowed to interrupt high priority
    d_low_int = _decision("low_priority_interrupt_attempt")
    ok_g = bool(d_low_int and d_low_int.get("final_action") == "suppressed" and "interrupt_denied" in str(((d_low_int.get("suppression_result") or {}).get("suppression_reason"))))
    results.append(_ok("G_low_priority_interrupt_denied", ok_g))

    # H. high priority may interrupt low priority only if allowed by policy
    d_hi_int = _decision("high_priority_interrupt_allowed")
    ok_h = bool(d_hi_int and d_hi_int.get("final_action") == "accepted_dry_run" and ((d_hi_int.get("priority_result") or {}).get("interrupt_decision") in ("allowed", "not_applicable")))
    results.append(_ok("H_high_priority_interrupt_allowed", ok_h))

    # I. cancelled request not spoken
    d_can = _decision("cancelled_request")
    ok_i = bool(d_can and d_can.get("final_action") == "cancelled")
    results.append(_ok("I_cancelled_not_spoken", ok_i))

    # J. stale request not spoken
    d_stale = _decision("stale_navigation_instruction")
    ok_j = bool(d_stale and d_stale.get("final_action") == "suppressed" and "stale" in str(((d_stale.get("suppression_result") or {}).get("suppression_reason"))))
    results.append(_ok("J_stale_suppressed", ok_j))

    # K. provider health state generated
    ok_k = isinstance(providers, list) and len(providers) == len(inputs)
    results.append(_ok("K_provider_health_generated", ok_k, count=(len(providers) if isinstance(providers, list) else 0)))

    # L. provider unhealthy causes suppression or fallback decision
    d_ph = _decision("provider_unhealthy")
    ok_l = bool(d_ph and d_ph.get("final_action") in ("fallback_candidate", "suppressed"))
    results.append(_ok("L_provider_unhealthy_handled", ok_l))

    # M/N/O/P/Q. invariants
    inv_ok = True
    bad: List[str] = []
    if isinstance(decisions, list):
        for d in decisions:
            if not isinstance(d, dict):
                continue
            gov = d.get("governance") if isinstance(d.get("governance"), dict) else {}
            if gov.get("real_tts_invoked") is not False:
                inv_ok = False
                bad.append(f"{d.get('sample_id')}:real_tts_invoked")
            if gov.get("playback_invoked") is not False:
                inv_ok = False
                bad.append(f"{d.get('sample_id')}:playback_invoked")
            if gov.get("provider_invoked") is not False:
                inv_ok = False
                bad.append(f"{d.get('sample_id')}:provider_invoked")
            if gov.get("navigation_action") is not None:
                inv_ok = False
                bad.append(f"{d.get('sample_id')}:navigation_action")
            if int(gov.get("downstream_invocation_count") or 0) != 0:
                inv_ok = False
                bad.append(f"{d.get('sample_id')}:downstream_invocation_count")
    results.append(_ok("M_real_tts_invoked_false", inv_ok, bad=bad[:20]))
    results.append(_ok("N_playback_invoked_false", inv_ok))
    results.append(_ok("O_provider_invoked_false", inv_ok))
    results.append(_ok("P_navigation_action_null", inv_ok))
    results.append(_ok("Q_downstream_invocation_count_zero", inv_ok))

    # R. trace/replay/whitebox non-empty
    ok_r = bool(len(trace) > 0 and len(replay) > 0 and len(whitebox) > 0)
    results.append(_ok("R_trace_replay_whitebox_non_empty", ok_r, trace=len(trace), replay=len(replay), whitebox=len(whitebox)))

    # S. audit envelope present
    ok_s = isinstance(audits, list) and len(audits) == len(inputs) and all(isinstance(x, dict) and str(x.get("audit_id") or "").strip() for x in audits)
    results.append(_ok("S_audit_envelope_present", ok_s, count=(len(audits) if isinstance(audits, list) else 0)))

    all_pass = all(bool(x.get("pass")) for x in results)
    out = {
        "phase": "Phase-Voice-OutputGovernance-002",
        "tool": "verify_voice_output_governance_v0.py",
        "output_root": str(root),
        "all_pass": all_pass,
        "checks_total": len(results),
        "checks_passed": int(sum(1 for x in results if x.get("pass"))),
        "results": results,
        "artifacts": {
            "summary": str(summary_p.name),
            "inputs": str(inputs_p.name),
            "decisions": str(decisions_p.name),
            "provider_states": str(provider_p.name),
            "audit_envelopes": str(audit_p.name),
            "trace": str(trace_p.name),
            "replay": str(replay_p.name),
            "whitebox": str(whitebox_p.name),
        },
        "notes": [
            "This verifier is offline-only and asserts real_tts_invoked/playback_invoked/provider_invoked are all false.",
            "SpeechGate invocation is asserted by decision.speech_gate_result.gate_invoked==true for all samples.",
        ],
    }
    (root / "verification_result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(root / "verification_result.json"))
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())

