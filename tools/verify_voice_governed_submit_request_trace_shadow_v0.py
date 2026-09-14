# -*- coding: utf-8 -*-
"""Phase-Voice-OutputGovernance-008 verifier for governed submit RequestTrace integration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Set

GOVERNED_SUBMIT_STAGE_FULL = "request_trace.stage.output.voice.governed_submit_shadow_gate"

GATE_POSITIONS = {
    "_maybe_submit_real_output_v1_pre",
    "VoiceOutputPlane.submit_entry",
}


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _non_empty_file(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def _require(cond: bool, msg: str, errors: List[str]) -> None:
    if not cond:
        errors.append(msg)


def verify(
    submit_shadow_root: Path,
    voice_request_trace_root: Path,
    output_root: Path,
) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []

    _require(submit_shadow_root.exists(), f"submit shadow root not readable: {submit_shadow_root}", errors)
    _require(voice_request_trace_root.exists(), f"voice request trace root not readable: {voice_request_trace_root}", errors)
    _require(output_root.exists(), f"output root not readable: {output_root}", errors)

    dec_path = submit_shadow_root / "voice_governed_submit_shadow_decisions.json"
    chains_path = voice_request_trace_root / "voice_output_request_chains.json"
    _require(dec_path.exists(), "submit decisions file missing", errors)
    _require(chains_path.exists(), "voice chains file missing", errors)

    enhanced_path = output_root / "voice_governed_submit_enhanced_request_chains.json"
    summary_path = output_root / "voice_governed_submit_request_trace_summary.json"
    matrix_path = output_root / "voice_governed_submit_gate_position_matrix.json"

    for p in (enhanced_path, summary_path, matrix_path):
        _require(p.exists(), f"missing output: {p.name}", errors)

    for p in (
        output_root / "voice_governed_submit_request_trace_trace.jsonl",
        output_root / "voice_governed_submit_request_trace_replay.jsonl",
        output_root / "voice_governed_submit_request_trace_whitebox.jsonl",
    ):
        _require(_non_empty_file(p), f"jsonl empty/missing: {p.name}", errors)

    if errors:
        return {"verdict": "NO_GO", "errors": errors, "warnings": warnings}

    decisions = _read_json(dec_path)
    enhanced = _read_json(enhanced_path)
    summary = _read_json(summary_path) if summary_path.exists() else {}

    _require(isinstance(decisions, list) and len(decisions) > 0, "submit decisions not loaded", errors)
    _require(isinstance(enhanced, list) and len(enhanced) > 0, "enhanced chains not generated", errors)

    # Stage presence + hard audit
    gate_seen = 0
    positions_seen: Set[str] = set()
    join_ok = 0
    if isinstance(summary, dict):
        st = summary.get("stats")
        if isinstance(st, dict) and st.get("join_matched_request_count") is not None:
            join_ok = int(st["join_matched_request_count"])
        elif isinstance(summary.get("outputs"), dict):
            join_ok = int(summary["outputs"].get("join_matched_request_count") or 0)

    for ch in enhanced:
        if not isinstance(ch, dict):
            continue
        stages = ch.get("stages")
        if not isinstance(stages, list):
            continue
        for st in stages:
            if not isinstance(st, dict):
                continue
            if st.get("stage_name") != GOVERNED_SUBMIT_STAGE_FULL:
                continue
            gate_seen += 1
            kf = st.get("key_fields")
            if isinstance(kf, dict):
                gp = kf.get("submit_gate_position")
                if isinstance(gp, str):
                    positions_seen.add(gp)
                ha = kf.get("hard_audit")
                if isinstance(ha, dict):
                    _require(ha.get("real_submit_invoked") in (False, None), "real_submit_invoked must be false", errors)
                    _require(ha.get("real_tts_invoked") is False, "real_tts_invoked must be false", errors)
                    _require(ha.get("playback_invoked") is False, "playback_invoked must be false", errors)
                    _require(ha.get("provider_invoked") is False, "provider_invoked must be false", errors)
                    _require(ha.get("navigation_action") in (None, ""), "navigation_action must be null", errors)
                    _require(ha.get("downstream_invocation_count") in (0, None), "downstream_invocation_count must be 0", errors)
                else:
                    errors.append("governed_submit gate missing hard_audit in key_fields")

    _require(gate_seen > 0, "governed_submit_shadow_gate stage not present", errors)
    _require(positions_seen == GATE_POSITIONS, f"expected both gate positions, got {positions_seen}", errors)
    _require(join_ok > 0, "request_id join success count must be > 0", errors)

    unmatched = 0
    if isinstance(summary, dict):
        stats = summary.get("stats") or summary.get("outputs")
        if isinstance(stats, dict):
            um = stats.get("unmatched_submit_decisions")
            if isinstance(um, list):
                unmatched = len(um)

    if unmatched > 0:
        warnings.append(f"unmatched submit decisions recorded: {unmatched}")

    verdict = "GO" if not errors else "NO_GO"
    return {"verdict": verdict, "errors": errors, "warnings": warnings, "gate_stage_count": gate_seen}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--submit-shadow-root", required=True)
    ap.add_argument("--voice-request-trace-root", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    report = verify(Path(args.submit_shadow_root), Path(args.voice_request_trace_root), Path(args.output_root))
    out_path = Path(args.output_root) / "voice_governed_submit_request_trace_verify_report.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["verdict"] == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
