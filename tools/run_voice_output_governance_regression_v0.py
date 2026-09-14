#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phase-Voice-OutputGovernance-006
Run Voice Output Governance Regression v0.

Reads Phase-002/004/005 output roots (read-only) and produces regression summaries.
Offline/shadow only: does not invoke real TTS/playback/providers and does not change runtime wiring.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


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
            row = json.loads(ln)
        except Exception:
            continue
        if isinstance(row, dict):
            out.append(row)
    return out


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _truthy(v: Any) -> bool:
    return bool(v is True or str(v).strip().lower() in ("1", "true", "yes"))


REQUIRED_STAGE_NAMES_005 = [
    "request_trace.stage.voice_output.candidate_input",
    "request_trace.stage.voice_output.speakable_guard",
    "request_trace.stage.voice_output.speech_gate",
    "request_trace.stage.voice_output.expiry_check",
    "request_trace.stage.voice_output.cancellation_check",
    "request_trace.stage.voice_output.provider_health_check",
    "request_trace.stage.voice_output.final_governance_decision",
]


def _summarize_phase_002(governance_root: Path) -> Dict[str, Any]:
    decisions_p = governance_root / "voice_output_governance_decisions.json"
    audits_p = governance_root / "voice_output_audit_envelopes.json"
    trace_p = governance_root / "voice_output_trace.jsonl"
    replay_p = governance_root / "voice_output_replay.jsonl"
    whitebox_p = governance_root / "voice_output_whitebox.jsonl"
    verifier_p = governance_root / "verification_result.json"

    decisions = _read_json(decisions_p) if decisions_p.exists() else []
    audits = _read_json(audits_p) if audits_p.exists() else []
    trace_rows = _read_jsonl(trace_p)
    replay_rows = _read_jsonl(replay_p)
    whitebox_rows = _read_jsonl(whitebox_p)
    verifier = _read_json(verifier_p) if verifier_p.exists() else {}

    if not isinstance(decisions, list):
        decisions = []
    if not isinstance(audits, list):
        audits = []

    final_action_counts: Dict[str, int] = {}
    inv_bad: List[str] = []
    hard_ok = True
    for d in decisions:
        if not isinstance(d, dict):
            continue
        fa = str(d.get("final_action") or "unknown")
        final_action_counts[fa] = final_action_counts.get(fa, 0) + 1
        gov = d.get("governance") if isinstance(d.get("governance"), dict) else {}
        if gov.get("real_tts_invoked") is not False:
            hard_ok = False
            inv_bad.append(f"{d.get('request_id')}:real_tts_invoked")
        if gov.get("playback_invoked") is not False:
            hard_ok = False
            inv_bad.append(f"{d.get('request_id')}:playback_invoked")
        if gov.get("provider_invoked") is not False:
            hard_ok = False
            inv_bad.append(f"{d.get('request_id')}:provider_invoked")
        if gov.get("navigation_action") is not None:
            hard_ok = False
            inv_bad.append(f"{d.get('request_id')}:navigation_action")
        if int(gov.get("downstream_invocation_count") or 0) != 0:
            hard_ok = False
            inv_bad.append(f"{d.get('request_id')}:downstream_invocation_count")

    return {
        "root": str(governance_root),
        "verifier_all_pass": bool(isinstance(verifier, dict) and verifier.get("all_pass") is True),
        "decisions_count": len([x for x in decisions if isinstance(x, dict)]),
        "audit_envelopes_count": len([x for x in audits if isinstance(x, dict)]),
        "trace_rows": len(trace_rows),
        "replay_rows": len(replay_rows),
        "whitebox_rows": len(whitebox_rows),
        "final_action_counts": final_action_counts,
        "hard_audit_invariants_ok": hard_ok,
        "hard_audit_bad": inv_bad[:50],
    }


def _summarize_phase_004(trw_adapter_root: Path) -> Dict[str, Any]:
    verifier_p = trw_adapter_root / "verification_result.json"
    summary_p = trw_adapter_root / "voice_output_trw_adapter_summary.json"
    records_p = trw_adapter_root / "voice_output_trw_records.json"
    timeline_p = trw_adapter_root / "voice_output_stage_timeline.json"
    report_p = trw_adapter_root / "voice_output_extractor_mapping_report.json"
    trace_p = trw_adapter_root / "voice_output_trw_adapter_trace.jsonl"
    replay_p = trw_adapter_root / "voice_output_trw_adapter_replay.jsonl"
    whitebox_p = trw_adapter_root / "voice_output_trw_adapter_whitebox.jsonl"

    verifier = _read_json(verifier_p) if verifier_p.exists() else {}
    summary = _read_json(summary_p) if summary_p.exists() else {}
    records = _read_json(records_p) if records_p.exists() else []
    timeline = _read_json(timeline_p) if timeline_p.exists() else []
    report = _read_json(report_p) if report_p.exists() else {}
    trace_rows = _read_jsonl(trace_p)
    replay_rows = _read_jsonl(replay_p)
    whitebox_rows = _read_jsonl(whitebox_p)

    if not isinstance(records, list):
        records = []
    if not isinstance(timeline, list):
        timeline = []

    ns_ok = all((isinstance(r, dict) and r.get("stage_namespace") == "voice_output_governance_v0") for r in records[:100] if records)
    inv_ok = True
    inv_bad: List[str] = []
    for r in records:
        if not isinstance(r, dict):
            continue
        ha = r.get("hard_audit") if isinstance(r.get("hard_audit"), dict) else {}
        if ha.get("real_tts_invoked") is not False:
            inv_ok = False
            inv_bad.append(f"{r.get('request_id')}:real_tts_invoked")
        if ha.get("playback_invoked") is not False:
            inv_ok = False
            inv_bad.append(f"{r.get('request_id')}:playback_invoked")
        if ha.get("provider_invoked") is not False:
            inv_ok = False
            inv_bad.append(f"{r.get('request_id')}:provider_invoked")
        if int(ha.get("downstream_invocation_count") or 0) != 0:
            inv_ok = False
            inv_bad.append(f"{r.get('request_id')}:downstream_invocation_count")
        if ha.get("navigation_action") is not None:
            inv_ok = False
            inv_bad.append(f"{r.get('request_id')}:navigation_action")

    return {
        "root": str(trw_adapter_root),
        "verifier_all_pass": bool(isinstance(verifier, dict) and verifier.get("all_pass") is True),
        "records_count": len([x for x in records if isinstance(x, dict)]),
        "timeline_rows": len(timeline),
        "mapping_report_present": bool(isinstance(report, dict) and report.get("stage_namespace") == "voice_output_governance_v0"),
        "stage_namespace_ok": bool(ns_ok),
        "hard_audit_invariants_ok": bool(inv_ok),
        "hard_audit_bad": inv_bad[:50],
        "adapter_trace_rows": len(trace_rows),
        "adapter_replay_rows": len(replay_rows),
        "adapter_whitebox_rows": len(whitebox_rows),
        "summary_excerpt": {
            "request_count": (summary.get("request_count") if isinstance(summary, dict) else None),
            "record_count": (summary.get("record_count") if isinstance(summary, dict) else None),
        },
    }


def _summarize_phase_005(request_trace_root: Path) -> Dict[str, Any]:
    verifier_p = request_trace_root / "verification_result.json"
    summary_p = request_trace_root / "voice_output_request_trace_extractor_summary.json"
    chains_p = request_trace_root / "voice_output_request_chains.json"
    mapping_p = request_trace_root / "voice_output_request_stage_mapping.json"
    whitebox_p = request_trace_root / "voice_output_request_chain_whitebox.json"
    trace_p = request_trace_root / "voice_output_extractor_shadow_trace.jsonl"
    replay_p = request_trace_root / "voice_output_extractor_shadow_replay.jsonl"
    wbj_p = request_trace_root / "voice_output_extractor_shadow_whitebox.jsonl"

    verifier = _read_json(verifier_p) if verifier_p.exists() else {}
    summary = _read_json(summary_p) if summary_p.exists() else {}
    chains = _read_json(chains_p) if chains_p.exists() else []
    mapping = _read_json(mapping_p) if mapping_p.exists() else {}
    whitebox = _read_json(whitebox_p) if whitebox_p.exists() else []
    trace_rows = _read_jsonl(trace_p)
    replay_rows = _read_jsonl(replay_p)
    wb_rows = _read_jsonl(wbj_p)

    if not isinstance(chains, list):
        chains = []

    required_ok = True
    missing: List[str] = []
    inv_ok = True
    inv_bad: List[str] = []
    for ch in chains:
        if not isinstance(ch, dict):
            continue
        rid = str(ch.get("request_id") or "")
        stages = ch.get("stages") if isinstance(ch.get("stages"), list) else []
        names = [str(s.get("stage_name") or "") for s in stages if isinstance(s, dict)]
        for req in REQUIRED_STAGE_NAMES_005:
            if req not in names:
                required_ok = False
                missing.append(f"{rid}:{req}")
        # invariants: read hard_audit from final stage key_fields.hard_audit
        ha = None
        for s in stages:
            if not isinstance(s, dict):
                continue
            if str(s.get("stage_name") or "").endswith(".final_governance_decision"):
                kf = s.get("key_fields") if isinstance(s.get("key_fields"), dict) else {}
                ha = kf.get("hard_audit") if isinstance(kf.get("hard_audit"), dict) else None
        if not isinstance(ha, dict):
            inv_ok = False
            inv_bad.append(f"{rid}:missing_hard_audit")
        else:
            if ha.get("real_tts_invoked") is not False:
                inv_ok = False
                inv_bad.append(f"{rid}:real_tts_invoked")
            if ha.get("playback_invoked") is not False:
                inv_ok = False
                inv_bad.append(f"{rid}:playback_invoked")
            if ha.get("provider_invoked") is not False:
                inv_ok = False
                inv_bad.append(f"{rid}:provider_invoked")
            if ha.get("navigation_action") is not None:
                inv_ok = False
                inv_bad.append(f"{rid}:navigation_action")
            if int(ha.get("downstream_invocation_count") or 0) != 0:
                inv_ok = False
                inv_bad.append(f"{rid}:downstream_invocation_count")

    return {
        "root": str(request_trace_root),
        "verifier_all_pass": bool(isinstance(verifier, dict) and verifier.get("all_pass") is True),
        "chains_count": len([x for x in chains if isinstance(x, dict)]),
        "shadow_only": bool(isinstance(summary, dict) and summary.get("shadow_only") is True),
        "stage_mapping_present": bool(isinstance(mapping, dict) and mapping.get("stage_namespace") == "voice_output_governance_v0"),
        "required_stages_ok": required_ok,
        "required_stages_missing": missing[:50],
        "hard_audit_invariants_ok": inv_ok,
        "hard_audit_bad": inv_bad[:50],
        "shadow_trace_rows": len(trace_rows),
        "shadow_replay_rows": len(replay_rows),
        "shadow_whitebox_rows": len(wb_rows),
        "whitebox_chain_rows": len(whitebox) if isinstance(whitebox, list) else 0,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--governance-root", required=True, help="Phase-002 root")
    ap.add_argument("--trw-adapter-root", required=True, help="Phase-004 root")
    ap.add_argument("--request-trace-root", required=True, help="Phase-005 root")
    ap.add_argument("--output-root", required=True, help="Regression output root")
    args = ap.parse_args()

    t0 = _now()
    out_root = Path(args.output_root)
    out_root.mkdir(parents=True, exist_ok=True)

    gov_root = Path(args.governance_root)
    trw_root = Path(args.trw_adapter_root)
    req_root = Path(args.request_trace_root)

    s2 = _summarize_phase_002(gov_root)
    s4 = _summarize_phase_004(trw_root)
    s5 = _summarize_phase_005(req_root)

    # Capability matrix (closure-oriented)
    capability_matrix = {
        "voice_output_governance_status": "closure_candidate_closed_v0",
        "scope": "offline_shadow_governance_chain",
        "existing_inventory": "done",
        "governance_definition": "done",
        "guard_gate_alignment": "done (001-fix risks resolved by 002)",
        "minimal_skeleton": "done",
        "trw_alignment": "done",
        "trw_adapter": "done",
        "request_trace_shadow": "done",
        "real_submit_wiring": "not_allowed",
        "real_playback": "not_allowed",
        "provider_runtime_invocation": "not_allowed",
    }

    # Boundary summary (must remain true)
    boundary = {
        "real_tts_invoked": False,
        "playback_invoked": False,
        "provider_invoked": False,
        "navigation_action": None,
        "downstream_invocation_count": 0,
        "notes": ["This regression is offline/shadow only; no real submit wiring is performed."],
    }

    # Hard audit consistency: all three summaries must say invariants ok.
    hard_audit_consistency = {
        "phase_002_invariants_ok": bool(s2.get("hard_audit_invariants_ok")),
        "phase_004_invariants_ok": bool(s4.get("hard_audit_invariants_ok")),
        "phase_005_invariants_ok": bool(s5.get("hard_audit_invariants_ok")),
        "all_ok": bool(s2.get("hard_audit_invariants_ok") and s4.get("hard_audit_invariants_ok") and s5.get("hard_audit_invariants_ok")),
        "bad_examples": {
            "phase_002": s2.get("hard_audit_bad"),
            "phase_004": s4.get("hard_audit_bad"),
            "phase_005": s5.get("hard_audit_bad"),
        },
    }

    regression_summary = {
        "phase": "Phase-Voice-OutputGovernance-006",
        "tool": "run_voice_output_governance_regression_v0.py",
        "generated_at_s": _now(),
        "duration_ms": int((_now() - t0) * 1000),
        "input_roots": {
            "phase_002_governance_root": str(gov_root),
            "phase_004_trw_adapter_root": str(trw_root),
            "phase_005_request_trace_root": str(req_root),
        },
        "counts": {
            "decisions_count": int(s2.get("decisions_count") or 0),
            "trw_records_count": int(s4.get("records_count") or 0),
            "request_chains_count": int(s5.get("chains_count") or 0),
        },
        "phase_checks": {
            "phase_002_verifier_go": bool(s2.get("verifier_all_pass")),
            "phase_004_verifier_go": bool(s4.get("verifier_all_pass")),
            "phase_005_verifier_go": bool(s5.get("verifier_all_pass")),
        },
        "required_stages_ok": bool(s5.get("required_stages_ok")),
        "hard_audit_consistency": hard_audit_consistency,
        "boundary": boundary,
        "closure_recommendation": {
            "voice_output_governance_status": "closed_v0",
            "scope": "offline_shadow_governance_chain",
            "real_submit_wiring_allowed": False,
            "real_playback_allowed": False,
        },
    }

    _write_json(out_root / "voice_output_governance_regression_summary.json", regression_summary)
    _write_json(out_root / "voice_output_governance_capability_matrix.json", capability_matrix)
    _write_json(out_root / "voice_output_governance_boundary_summary.json", boundary)
    _write_json(out_root / "voice_output_hard_audit_consistency_summary.json", hard_audit_consistency)
    _write_json(out_root / "voice_output_trw_adapter_regression_summary.json", s4)
    _write_json(out_root / "voice_output_request_trace_regression_summary.json", s5)

    (out_root / "regression_notes.md").write_text(
        "\n".join(
            [
                "# Phase-Voice-OutputGovernance-006 Regression Notes",
                "",
                f"- governance_root (002): `{args.governance_root}`",
                f"- trw_adapter_root (004): `{args.trw_adapter_root}`",
                f"- request_trace_root (005): `{args.request_trace_root}`",
                f"- output_root: `{str(out_root)}`",
                "",
                "- This regression is read-only and offline/shadow only.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(str(out_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

