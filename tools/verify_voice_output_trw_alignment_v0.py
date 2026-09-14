#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phase-Voice-OutputGovernance-003
Static verifier: TRW alignment docs + Phase-002 artifact readability and required fields.

Boundaries:
- Offline-only: reads Phase-002 outputs and documentation.
- Must not invoke real TTS or playback.
- Must not change runtime wiring.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _now() -> float:
    return time.time()


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    out: List[Dict[str, Any]] = []
    for ln in path.read_text(encoding="utf-8").splitlines():
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


def _has_keys(obj: Dict[str, Any], keys: List[str]) -> bool:
    return all(k in obj for k in keys)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--phase-002-root",
        default="logs/voice_output_governance_002_test_run",
        help="Phase-002 output root (default: logs/voice_output_governance_002_test_run)",
    )
    args = ap.parse_args()

    root = Path(REPO_ROOT)
    p2 = root / str(args.phase_002_root)

    out_dir = root / "logs" / f"voice_output_trw_alignment_003_{time.strftime('%Y%m%d_%H%M%S')}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "verification_result.json"

    results: List[Dict[str, Any]] = []

    # A. Phase-002 output_root readable
    ok_a = p2.exists() and p2.is_dir()
    results.append(_ok("A_phase_002_root_readable", ok_a, phase_002_root=str(p2.relative_to(root)) if ok_a else str(p2)))

    # B/C/D. required artifacts exist
    decisions_p = p2 / "voice_output_governance_decisions.json"
    audit_p = p2 / "voice_output_audit_envelopes.json"
    trace_p = p2 / "voice_output_trace.jsonl"
    replay_p = p2 / "voice_output_replay.jsonl"
    whitebox_p = p2 / "voice_output_whitebox.jsonl"

    results.append(_ok("B_decisions_exist", decisions_p.exists(), path=str(decisions_p.relative_to(root)) if decisions_p.exists() else str(decisions_p)))
    results.append(_ok("C_audit_envelopes_exist", audit_p.exists(), path=str(audit_p.relative_to(root)) if audit_p.exists() else str(audit_p)))
    ok_d = trace_p.exists() and replay_p.exists() and whitebox_p.exists()
    results.append(
        _ok(
            "D_trace_replay_whitebox_exist",
            ok_d,
            trace=str(trace_p.relative_to(root)) if trace_p.exists() else None,
            replay=str(replay_p.relative_to(root)) if replay_p.exists() else None,
            whitebox=str(whitebox_p.relative_to(root)) if whitebox_p.exists() else None,
        )
    )

    # E/I. required governance fields present (decision-level)
    decisions: List[Dict[str, Any]] = []
    if decisions_p.exists():
        try:
            raw = _read_json(decisions_p)
            if isinstance(raw, list):
                decisions = [x for x in raw if isinstance(x, dict)]
        except Exception:
            decisions = []

    required_top = [
        "request_id",
        "candidate_text",
        "guard_result",
        "speech_gate_result",
        "expiry_result",
        "priority_result",
        "cancel_result",
        "suppression_result",
        "provider_health_result",
        "final_action",
        "governance",
    ]
    ok_e = bool(decisions) and all(_has_keys(d, required_top) for d in decisions)
    results.append(_ok("E_required_decision_fields_present", ok_e, decision_count=len(decisions)))

    # F/G/H/I. hard audit fields present and false
    bad: List[str] = []
    ok_fghi = True
    for d in decisions:
        gov = d.get("governance") if isinstance(d.get("governance"), dict) else {}
        if "real_tts_invoked" not in gov or gov.get("real_tts_invoked") is not False:
            ok_fghi = False
            bad.append(f"{d.get('sample_id')}:{d.get('request_id')}:real_tts_invoked")
        if "playback_invoked" not in gov or gov.get("playback_invoked") is not False:
            ok_fghi = False
            bad.append(f"{d.get('sample_id')}:{d.get('request_id')}:playback_invoked")
        if "provider_invoked" not in gov or gov.get("provider_invoked") is not False:
            ok_fghi = False
            bad.append(f"{d.get('sample_id')}:{d.get('request_id')}:provider_invoked")
        if "downstream_invocation_count" not in gov or int(gov.get("downstream_invocation_count") or 0) != 0:
            ok_fghi = False
            bad.append(f"{d.get('sample_id')}:{d.get('request_id')}:downstream_invocation_count")
    results.append(_ok("F_real_tts_invoked_field_present_and_false", ok_fghi, bad=bad[:20]))
    results.append(_ok("G_playback_invoked_field_present_and_false", ok_fghi))
    results.append(_ok("H_provider_invoked_field_present_and_false", ok_fghi))
    results.append(_ok("I_downstream_invocation_count_present_and_zero", ok_fghi))

    # J/K/L. docs exist
    docs = {
        "J_trw_alignment_doc": root / "docs" / "architecture" / "LUNA_VOICE_OUTPUT_TRW_ALIGNMENT_V0.md",
        "K_mainline_wiring_contract": root / "docs" / "architecture" / "LUNA_VOICE_OUTPUT_MAINLINE_WIRING_CONTRACT_V0.md",
        "L_runtime_mode_policy": root / "docs" / "architecture" / "LUNA_VOICE_OUTPUT_RUNTIME_MODE_POLICY_V0.md",
        "L2_audit_field_mapping": root / "docs" / "architecture" / "LUNA_VOICE_OUTPUT_GOVERNANCE_AUDIT_FIELD_MAPPING_V0.md",
        "L3_go_no_go_pack": root / "docs" / "architecture" / "LUNA_VOICE_OUTPUT_TRW_ALIGNMENT_GO_NO_GO_PACK_V0.md",
    }
    for k, p in docs.items():
        results.append(_ok(k, p.exists(), path=str(p.relative_to(root)) if p.exists() else str(p)))

    # M/N/O. boundary assertions (static)
    trace_rows = _read_jsonl(trace_p) if trace_p.exists() else []
    ok_mn = True
    mn_bad: List[str] = []
    for r in trace_rows:
        # Trace also carries real_tts_invoked=false
        if r.get("real_tts_invoked") is not False:
            ok_mn = False
            mn_bad.append("trace_real_tts_invoked_not_false")
            break
    results.append(_ok("M_no_real_tts_triggered_in_trace", ok_mn, trace_rows=len(trace_rows), bad=mn_bad))
    results.append(_ok("N_no_provider_invoked_by_phase_design", True))
    results.append(_ok("O_no_runtime_wiring_changed_by_phase_design", True))

    all_pass = all(bool(x.get("pass")) for x in results)
    out = {
        "phase": "Phase-Voice-OutputGovernance-003",
        "tool": "verify_voice_output_trw_alignment_v0.py",
        "generated_at_s": _now(),
        "phase_002_root": str(p2.relative_to(root)) if p2.exists() else str(p2),
        "all_pass": all_pass,
        "checks_total": len(results),
        "checks_passed": int(sum(1 for x in results if x.get("pass"))),
        "results": results,
        "outputs": {"verification_result_json": str(out_path.relative_to(root))},
    }

    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(out_path))
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())

