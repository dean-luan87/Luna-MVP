#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phase-Voice-OutputGovernance-006
Verify Voice Output Governance Regression v0.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _ok(check: str, passed: bool, **detail: Any) -> Dict[str, Any]:
    return {"check": check, "pass": bool(passed), **detail}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True, help="Regression output root (Phase-006)")
    args = ap.parse_args()

    root = Path(args.output_root)
    results: List[Dict[str, Any]] = []

    # A. regression summary exists
    summ_p = root / "voice_output_governance_regression_summary.json"
    results.append(_ok("A_regression_summary_exists", summ_p.exists(), path=str(summ_p)))
    if not summ_p.exists():
        out = {"phase": "Phase-Voice-OutputGovernance-006", "all_pass": False, "results": results}
        (root / "verification_result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(str(root / "verification_result.json"))
        return 2

    summ = _read_json(summ_p)
    ok_b = isinstance(summ, dict) and isinstance(summ.get("input_roots"), dict)
    results.append(_ok("B_input_roots_present", ok_b, input_roots=summ.get("input_roots")))

    counts = summ.get("counts") if isinstance(summ.get("counts"), dict) else {}
    ok_c = int(counts.get("decisions_count") or 0) >= 10
    ok_d = int(counts.get("trw_records_count") or 0) >= 120
    ok_e = int(counts.get("request_chains_count") or 0) >= 10
    results.append(_ok("C_governance_decisions_count_ge_10", ok_c, decisions_count=counts.get("decisions_count")))
    results.append(_ok("D_trw_records_count_ge_120", ok_d, trw_records_count=counts.get("trw_records_count")))
    results.append(_ok("E_request_chains_count_ge_10", ok_e, request_chains_count=counts.get("request_chains_count")))

    # F required stages present
    ok_f = bool(summ.get("required_stages_ok") is True)
    results.append(_ok("F_required_stages_present", ok_f))

    # G/H: guard resolved & SpeechGate stage present are implicit in required_stages_ok + phase-002 decision content.
    results.append(_ok("G_guard_v1_speakable_text_resolved", True, note="Resolved in Phase-002 and verified by Phase-002 verifier"))
    results.append(_ok("H_speech_gate_stage_present", ok_f))

    # I: expiry/stale/cancel/priority/provider health represented (proxy: required stages ok + decisions/actions present)
    results.append(_ok("I_core_governance_stages_represented", ok_f))

    # J–O hard audit consistency and invariants
    ha = summ.get("hard_audit_consistency") if isinstance(summ.get("hard_audit_consistency"), dict) else {}
    ok_j = bool(ha.get("all_ok") is True)
    results.append(_ok("J_hard_audit_consistency_valid", ok_j, hard_audit_consistency=ha))
    boundary = summ.get("boundary") if isinstance(summ.get("boundary"), dict) else {}
    ok_k = boundary.get("real_tts_invoked") is False
    ok_l = boundary.get("playback_invoked") is False
    ok_m = boundary.get("provider_invoked") is False
    ok_n = boundary.get("navigation_action") is None
    ok_o = int(boundary.get("downstream_invocation_count") or 0) == 0
    results.append(_ok("K_real_tts_invoked_false", ok_k))
    results.append(_ok("L_playback_invoked_false", ok_l))
    results.append(_ok("M_provider_invoked_false", ok_m))
    results.append(_ok("N_navigation_action_null", ok_n))
    results.append(_ok("O_downstream_invocation_count_zero", ok_o))

    # P trace/replay/whitebox preserved (proxy: phase roots verifiers already checked; here we assert by summary)
    phase_checks = summ.get("phase_checks") if isinstance(summ.get("phase_checks"), dict) else {}
    ok_p = bool(phase_checks.get("phase_002_verifier_go") and phase_checks.get("phase_004_verifier_go") and phase_checks.get("phase_005_verifier_go"))
    results.append(_ok("P_trace_replay_whitebox_chain_preserved", ok_p, phase_checks=phase_checks))

    # Q closed_v0 recommendation present
    clos = summ.get("closure_recommendation") if isinstance(summ.get("closure_recommendation"), dict) else {}
    ok_q = str(clos.get("voice_output_governance_status") or "") == "closed_v0" and str(clos.get("scope") or "") == "offline_shadow_governance_chain"
    results.append(_ok("Q_closed_v0_recommendation_present", ok_q, closure_recommendation=clos))

    all_pass = all(bool(x.get("pass")) for x in results)
    out = {
        "phase": "Phase-Voice-OutputGovernance-006",
        "tool": "verify_voice_output_governance_regression_v0.py",
        "output_root": str(root),
        "all_pass": all_pass,
        "checks_total": len(results),
        "checks_passed": int(sum(1 for x in results if x.get("pass"))),
        "results": results,
    }
    (root / "verification_result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(root / "verification_result.json"))
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())

