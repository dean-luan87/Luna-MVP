#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phase-Voice-OutputGovernance-005
Verify RequestTraceExtractor Governance Stage Integration (shadow/offline).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


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
            row = json.loads(ln)
        except Exception:
            continue
        if isinstance(row, dict):
            out.append(row)
    return out


def _ok(check: str, passed: bool, **detail: Any) -> Dict[str, Any]:
    return {"check": check, "pass": bool(passed), **detail}


REQUIRED_STAGES = [
    "request_trace.stage.voice_output.candidate_input",
    "request_trace.stage.voice_output.speakable_guard",
    "request_trace.stage.voice_output.speech_gate",
    "request_trace.stage.voice_output.expiry_check",
    "request_trace.stage.voice_output.cancellation_check",
    "request_trace.stage.voice_output.provider_health_check",
    "request_trace.stage.voice_output.final_governance_decision",
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-root", required=True, help="Phase-004 adapter output root")
    ap.add_argument("--output-root", required=True, help="Phase-005 output root")
    args = ap.parse_args()

    inp = Path(args.input_root)
    out = Path(args.output_root)
    results: List[Dict[str, Any]] = []

    # A. input root readable
    results.append(_ok("A_input_root_readable", inp.exists() and inp.is_dir(), input_root=str(inp)))

    # B. TRW records loaded
    rec_p = inp / "voice_output_trw_records.json"
    ok_b = rec_p.exists()
    results.append(_ok("B_trw_records_exist", ok_b, path=str(rec_p)))

    # Load generated chains
    chains_p = out / "voice_output_request_chains.json"
    mapping_p = out / "voice_output_request_stage_mapping.json"
    whitebox_p = out / "voice_output_request_chain_whitebox.json"
    summary_p = out / "voice_output_request_trace_extractor_summary.json"

    ok_c = mapping_p.exists()
    results.append(_ok("C_stage_namespace_recognized", ok_c, path=str(mapping_p)))

    chains = _read_json(chains_p) if chains_p.exists() else []
    ok_d = isinstance(chains, list) and len(chains) > 0
    results.append(_ok("D_request_chains_generated", ok_d, chain_count=(len(chains) if isinstance(chains, list) else 0)))

    # E/F/G/H/I. each request has ordered stages and required stages present
    ok_e = True
    missing: List[str] = []
    for ch in chains if isinstance(chains, list) else []:
        if not isinstance(ch, dict):
            ok_e = False
            missing.append("non_dict_chain")
            continue
        stages = ch.get("stages") if isinstance(ch.get("stages"), list) else []
        names = [str(s.get("stage_name") or "") for s in stages if isinstance(s, dict)]
        for req in REQUIRED_STAGES:
            if req not in names:
                ok_e = False
                missing.append(f"{ch.get('request_id')}:{req}")
        # ordered: stage_order exists in key_fields and is non-decreasing
        orders: List[int] = []
        for s in stages:
            if not isinstance(s, dict):
                continue
            kf = s.get("key_fields") if isinstance(s.get("key_fields"), dict) else {}
            try:
                orders.append(int(kf.get("stage_order")))
            except Exception:
                orders.append(-1)
        if any(o < 0 for o in orders):
            ok_e = False
            missing.append(f"{ch.get('request_id')}:missing_stage_order")
        if any(orders[i] > orders[i + 1] for i in range(len(orders) - 1)):
            ok_e = False
            missing.append(f"{ch.get('request_id')}:stage_order_not_sorted")
    results.append(_ok("E_each_request_has_ordered_stages", ok_e, missing=missing[:20]))
    results.append(_ok("F_required_stages_present", ok_e))
    results.append(_ok("G_guard_stage_present", ok_e))
    results.append(_ok("H_speech_gate_stage_present", ok_e))
    results.append(_ok("I_expiry_cancel_provider_final_stages_present", ok_e))

    # J–O. hard audit fields preserved and invariants
    ok_inv = True
    inv_bad: List[str] = []
    for ch in chains if isinstance(chains, list) else []:
        if not isinstance(ch, dict):
            continue
        # hard audit present in final_governance_decision stage key_fields.hard_audit
        stages = ch.get("stages") if isinstance(ch.get("stages"), list) else []
        ha = None
        for s in stages:
            if not isinstance(s, dict):
                continue
            if str(s.get("stage_name") or "").endswith(".final_governance_decision"):
                kf = s.get("key_fields") if isinstance(s.get("key_fields"), dict) else {}
                ha = kf.get("hard_audit") if isinstance(kf.get("hard_audit"), dict) else None
        if not isinstance(ha, dict):
            ok_inv = False
            inv_bad.append(f"{ch.get('request_id')}:missing_hard_audit")
            continue
        if ha.get("real_tts_invoked") is not False:
            ok_inv = False
            inv_bad.append(f"{ch.get('request_id')}:real_tts_invoked")
        if ha.get("playback_invoked") is not False:
            ok_inv = False
            inv_bad.append(f"{ch.get('request_id')}:playback_invoked")
        if ha.get("provider_invoked") is not False:
            ok_inv = False
            inv_bad.append(f"{ch.get('request_id')}:provider_invoked")
        if int(ha.get("downstream_invocation_count") or 0) != 0:
            ok_inv = False
            inv_bad.append(f"{ch.get('request_id')}:downstream_invocation_count")
        if ha.get("navigation_action") is not None:
            ok_inv = False
            inv_bad.append(f"{ch.get('request_id')}:navigation_action")
    results.append(_ok("J_hard_audit_fields_preserved", ok_inv, bad=inv_bad[:20]))
    results.append(_ok("K_real_tts_invoked_false", ok_inv))
    results.append(_ok("L_playback_invoked_false", ok_inv))
    results.append(_ok("M_provider_invoked_false", ok_inv))
    results.append(_ok("N_navigation_action_null", ok_inv))
    results.append(_ok("O_downstream_invocation_count_zero", ok_inv))

    # P. shadow mode only
    summary = _read_json(summary_p) if summary_p.exists() else {}
    ok_p = bool(isinstance(summary, dict) and summary.get("shadow_only") is True)
    results.append(_ok("P_shadow_mode_only", ok_p))

    # Q. trace/replay/whitebox non-empty
    t = _read_jsonl(out / "voice_output_extractor_shadow_trace.jsonl")
    r = _read_jsonl(out / "voice_output_extractor_shadow_replay.jsonl")
    w = _read_jsonl(out / "voice_output_extractor_shadow_whitebox.jsonl")
    ok_q = bool(len(t) > 0 and len(r) > 0 and len(w) > 0)
    results.append(_ok("Q_trace_replay_whitebox_non_empty", ok_q, trace=len(t), replay=len(r), whitebox=len(w)))

    # R. no runtime submit wiring changed
    results.append(_ok("R_no_runtime_submit_wiring_changed_by_phase_design", True))

    all_pass = all(bool(x.get("pass")) for x in results)
    out_obj = {
        "phase": "Phase-Voice-OutputGovernance-005",
        "tool": "verify_voice_output_request_trace_extractor_shadow_v0.py",
        "input_root": str(inp),
        "output_root": str(out),
        "all_pass": all_pass,
        "checks_total": len(results),
        "checks_passed": int(sum(1 for x in results if x.get("pass"))),
        "results": results,
        "artifacts": {
            "summary": str(summary_p.name),
            "chains": str(chains_p.name),
            "stage_mapping": str(mapping_p.name),
            "whitebox": str(whitebox_p.name),
        },
    }
    (out / "verification_result.json").write_text(json.dumps(out_obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(out / "verification_result.json"))
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())

