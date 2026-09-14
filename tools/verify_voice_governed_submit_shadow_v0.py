# -*- coding: utf-8 -*-
"""
Phase-Voice-OutputGovernance-007
Verifier for governed submit shadow readiness v0.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _non_empty_file(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def _require(cond: bool, msg: str, errors: List[str]) -> None:
    if not cond:
        errors.append(msg)


def _index_governance_decisions(decisions: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    idx: Dict[str, Dict[str, Any]] = {}
    for d in decisions:
        if not isinstance(d, dict):
            continue
        rid = d.get("request_id")
        if isinstance(rid, str) and rid:
            idx[rid] = d
    return idx


def _expected_shadow_result(final_action: str, d: Dict[str, Any]) -> str:
    # Mirror logic in shadow gate module (must remain conservative).
    cancel_requested = (d.get("cancel_result") or {}).get("cancel_requested") if isinstance(d.get("cancel_result"), dict) else None
    is_expired = (d.get("expiry_result") or {}).get("is_expired") if isinstance(d.get("expiry_result"), dict) else None
    speech_allowed = (d.get("speech_gate_result") or {}).get("allowed") if isinstance(d.get("speech_gate_result"), dict) else None

    if cancel_requested:
        return "submit_cancelled_shadow"
    if is_expired:
        return "submit_expired_shadow"
    if speech_allowed is False:
        return "submit_blocked_shadow"
    if final_action == "fallback_candidate":
        return "submit_fallback_candidate_shadow"
    if final_action == "accepted_dry_run":
        return "submit_allowed_shadow"
    if final_action in ("suppressed", "rejected", "cancelled", "expired"):
        # map cancelled/expired already handled by checks; default to blocked/expired/cancelled as appropriate
        if final_action == "cancelled":
            return "submit_cancelled_shadow"
        if final_action == "expired":
            return "submit_expired_shadow"
        return "submit_blocked_shadow"
    return "submit_blocked_shadow"


def verify(governance_root: Path, request_trace_root: Path, output_root: Path) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []

    _require(governance_root.exists() and governance_root.is_dir(), f"governance root not readable: {governance_root}", errors)
    _require(request_trace_root.exists() and request_trace_root.is_dir(), f"request trace root not readable: {request_trace_root}", errors)
    _require(output_root.exists() and output_root.is_dir(), f"output root not readable: {output_root}", errors)

    # input existence
    gov_decisions_p = governance_root / "voice_output_governance_decisions.json"
    _require(gov_decisions_p.exists(), "governance decisions missing", errors)

    # output existence
    dec_p = output_root / "voice_governed_submit_shadow_decisions.json"
    _require(dec_p.exists(), "submit shadow decisions missing", errors)
    _require((output_root / "voice_governed_submit_shadow_summary.json").exists(), "summary missing", errors)
    _require((output_root / "voice_submit_gate_audit_envelopes.json").exists(), "audit envelopes missing", errors)

    # jsonl non-empty
    for p in (
        output_root / "voice_governed_submit_shadow_trace.jsonl",
        output_root / "voice_governed_submit_shadow_replay.jsonl",
        output_root / "voice_governed_submit_shadow_whitebox.jsonl",
    ):
        _require(_non_empty_file(p), f"jsonl output missing/empty: {p.name}", errors)

    if errors:
        return {"verdict": "NO_GO", "errors": errors, "warnings": warnings}

    gov_decisions = _read_json(gov_decisions_p)
    shadow_decisions = _read_json(dec_p)
    _require(isinstance(gov_decisions, list) and len(gov_decisions) > 0, "governance decisions not loaded", errors)
    _require(isinstance(shadow_decisions, list) and len(shadow_decisions) > 0, "shadow decisions not generated", errors)
    if errors:
        return {"verdict": "NO_GO", "errors": errors, "warnings": warnings}

    gov_idx = _index_governance_decisions(gov_decisions)

    # mapping checks + invariants
    for sd in shadow_decisions:
        if not isinstance(sd, dict):
            continue
        rid = sd.get("request_id")
        _require(isinstance(rid, str) and rid, "shadow decision missing request_id", errors)
        pos = sd.get("submit_gate_position")
        _require(pos in ("_maybe_submit_real_output_v1_pre", "VoiceOutputPlane.submit_entry"), "invalid submit_gate_position", errors)
        ha = sd.get("hard_audit")
        _require(isinstance(ha, dict), "hard_audit missing", errors)
        if isinstance(ha, dict):
            _require(ha.get("real_submit_invoked") is False, "real_submit_invoked must be false", errors)
            _require(ha.get("real_tts_invoked") is False, "real_tts_invoked must be false", errors)
            _require(ha.get("playback_invoked") is False, "playback_invoked must be false", errors)
            _require(ha.get("provider_invoked") is False, "provider_invoked must be false", errors)
            _require(ha.get("navigation_action") in (None, ""), "navigation_action must be null", errors)
            _require(ha.get("downstream_invocation_count") in (0, None), "downstream_invocation_count must be 0", errors)

        # Check mapping from final_action
        gd = gov_idx.get(rid or "", {})
        fa = gd.get("final_action") if isinstance(gd, dict) else None
        if isinstance(fa, str) and gd:
            expected = _expected_shadow_result(fa, gd)
            got = sd.get("submit_shadow_result")
            if expected != got:
                errors.append(f"mapping mismatch for request_id={rid}: expected {expected} got {got}")

        # Check key checks preserved
        _require(sd.get("expiry_checked") is True, "expiry_checked must be true", errors)
        _require(sd.get("cancel_checked") is True, "cancel_checked must be true", errors)
        _require(sd.get("speech_gate_checked") is True, "speech_gate_checked must be true", errors)
        _require(sd.get("provider_health_checked") is True, "provider_health_checked must be true", errors)

    verdict = "GO" if not errors else "NO_GO"
    return {"verdict": verdict, "errors": errors, "warnings": warnings}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--governance-root", required=True)
    ap.add_argument("--request-trace-root", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    report = verify(Path(args.governance_root), Path(args.request_trace_root), Path(args.output_root))
    out_path = Path(args.output_root) / "voice_governed_submit_shadow_verify_report.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["verdict"] == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

