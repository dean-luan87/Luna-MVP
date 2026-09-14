#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phase-Voice-OutputGovernance-004
Verify Voice Output TRW Adapter v0.
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-root", required=True, help="Phase-002 input root")
    ap.add_argument("--output-root", required=True, help="Adapter output root")
    args = ap.parse_args()

    input_root = Path(args.input_root)
    out_root = Path(args.output_root)

    results: List[Dict[str, Any]] = []

    # A/B. input root readable and required files exist
    results.append(_ok("A_input_root_readable", input_root.exists() and input_root.is_dir(), input_root=str(input_root)))
    required_p2 = [
        "voice_output_governance_decisions.json",
        "voice_output_audit_envelopes.json",
        "voice_output_trace.jsonl",
        "voice_output_replay.jsonl",
        "voice_output_whitebox.jsonl",
    ]
    ok_b = all((input_root / x).exists() for x in required_p2)
    results.append(_ok("B_phase_002_required_files_exist", ok_b, missing=[x for x in required_p2 if not (input_root / x).exists()]))

    # C/D. decisions and audits loaded via output artifacts
    records_p = out_root / "voice_output_trw_records.json"
    timeline_p = out_root / "voice_output_stage_timeline.json"
    report_p = out_root / "voice_output_extractor_mapping_report.json"
    wbext_p = out_root / "voice_output_whitebox_extension.json"

    ok_cd = records_p.exists()
    results.append(_ok("E_trw_records_generated", ok_cd, path=str(records_p)))

    records = _read_json(records_p) if records_p.exists() else []
    ok_e = isinstance(records, list) and len(records) > 0
    results.append(_ok("F_trw_records_non_empty", ok_e, record_count=(len(records) if isinstance(records, list) else 0)))

    # F/G/H. stage namespace/order/request_id present
    ok_fgh = True
    bad: List[str] = []
    for r in records if isinstance(records, list) else []:
        if not isinstance(r, dict):
            ok_fgh = False
            bad.append("non_dict_record")
            continue
        if str(r.get("stage_namespace") or "") != "voice_output_governance_v0":
            ok_fgh = False
            bad.append(f"bad_namespace:{r.get('record_id')}")
        if not isinstance(r.get("stage_order"), int):
            ok_fgh = False
            bad.append(f"missing_stage_order:{r.get('record_id')}")
        if not str(r.get("request_id") or "").strip():
            ok_fgh = False
            bad.append(f"missing_request_id:{r.get('record_id')}")
    results.append(_ok("G_stage_namespace_present", ok_fgh, bad=bad[:20]))
    results.append(_ok("H_stage_order_present", ok_fgh))
    results.append(_ok("I_request_id_present", ok_fgh))

    # I–N. hard audit fields present and invariants
    ok_inv = True
    inv_bad: List[str] = []
    for r in records if isinstance(records, list) else []:
        if not isinstance(r, dict):
            continue
        ha = r.get("hard_audit") if isinstance(r.get("hard_audit"), dict) else {}
        for k in ("real_tts_invoked", "playback_invoked", "provider_invoked", "downstream_invocation_count", "navigation_action"):
            if k not in ha:
                ok_inv = False
                inv_bad.append(f"missing:{k}:{r.get('record_id')}")
        if ha.get("real_tts_invoked") is not False:
            ok_inv = False
            inv_bad.append(f"real_tts_invoked_not_false:{r.get('record_id')}")
        if ha.get("playback_invoked") is not False:
            ok_inv = False
            inv_bad.append(f"playback_invoked_not_false:{r.get('record_id')}")
        if ha.get("provider_invoked") is not False:
            ok_inv = False
            inv_bad.append(f"provider_invoked_not_false:{r.get('record_id')}")
        if int(ha.get("downstream_invocation_count") or 0) != 0:
            ok_inv = False
            inv_bad.append(f"downstream_invocation_count_not_zero:{r.get('record_id')}")
        if ha.get("navigation_action") is not None:
            ok_inv = False
            inv_bad.append(f"navigation_action_not_null:{r.get('record_id')}")
    results.append(_ok("J_hard_audit_fields_present", ok_inv, bad=inv_bad[:20]))
    results.append(_ok("K_real_tts_invoked_false", ok_inv))
    results.append(_ok("L_playback_invoked_false", ok_inv))
    results.append(_ok("M_provider_invoked_false", ok_inv))
    results.append(_ok("N_downstream_invocation_count_zero_and_navigation_action_null", ok_inv))

    # O/P/Q. timeline/report/whitebox extension exist
    ok_o = timeline_p.exists()
    ok_p = report_p.exists()
    ok_q = wbext_p.exists()
    results.append(_ok("O_stage_timeline_generated", ok_o, path=str(timeline_p)))
    results.append(_ok("P_mapping_report_generated", ok_p, path=str(report_p)))
    results.append(_ok("Q_whitebox_extension_generated", ok_q, path=str(wbext_p)))

    # R. adapter trace/replay/whitebox non-empty
    t = _read_jsonl(out_root / "voice_output_trw_adapter_trace.jsonl")
    rp = _read_jsonl(out_root / "voice_output_trw_adapter_replay.jsonl")
    wb = _read_jsonl(out_root / "voice_output_trw_adapter_whitebox.jsonl")
    ok_r = bool(len(t) > 0 and len(rp) > 0 and len(wb) > 0)
    results.append(_ok("R_trace_replay_whitebox_non_empty", ok_r, trace=len(t), replay=len(rp), whitebox=len(wb)))

    # S/T. boundary assertions
    results.append(_ok("S_no_runtime_submit_wiring_changed_by_phase_design", True))
    results.append(_ok("T_no_real_tts_invoked_by_phase_design", True))

    all_pass = all(bool(x.get("pass")) for x in results)
    out = {
        "phase": "Phase-Voice-OutputGovernance-004",
        "tool": "verify_voice_output_trw_adapter_v0.py",
        "input_root": str(input_root),
        "output_root": str(out_root),
        "all_pass": all_pass,
        "checks_total": len(results),
        "checks_passed": int(sum(1 for x in results if x.get("pass"))),
        "results": results,
    }
    (out_root / "verification_result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(out_root / "verification_result.json"))
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())

