# -*- coding: utf-8 -*-
"""
Phase-Voice-OutputGovernance-009
Offline query tool for Phase-008 enhanced voice request chains.

Filters:
- submit_shadow_result
- submit_gate_position
- submit_allowed
- request_id
- hard_audit_only (anomaly)

Exports JSON/JSONL/MD.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


STAGE_NAME = "request_trace.stage.output.voice.governed_submit_shadow_gate"
ALLOWED_RESULTS = {
    "submit_allowed_shadow",
    "submit_blocked_shadow",
    "submit_expired_shadow",
    "submit_cancelled_shadow",
    "submit_fallback_candidate_shadow",
    "all",
}
ALLOWED_POSITIONS = {
    "_maybe_submit_real_output_v1_pre",
    "VoiceOutputPlane.submit_entry",
    "all",
}
ALLOWED_BOOL = {"true", "false", "all"}


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _mk_out_root(p: Optional[str]) -> Path:
    out = Path(p) if p else (Path("logs") / f"voice_governed_submit_unified_query_009_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    if not out.is_absolute():
        out = Path.cwd() / out
    out.mkdir(parents=True, exist_ok=True)
    return out


def _hard_audit_ok(ha: Dict[str, Any]) -> bool:
    return (
        ha.get("real_submit_invoked") in (False, None)
        and ha.get("real_tts_invoked") is False
        and ha.get("playback_invoked") is False
        and ha.get("provider_invoked") is False
        and ha.get("navigation_action") in (None, "")
        and ha.get("downstream_invocation_count") in (0, None)
    )


def _iter_gate_records(enhanced_chains: List[Dict[str, Any]], *, source_root: str) -> Iterable[Dict[str, Any]]:
    for ch in enhanced_chains:
        if not isinstance(ch, dict):
            continue
        rid = ch.get("request_id")
        if not isinstance(rid, str) or not rid:
            continue
        stages = ch.get("stages")
        if not isinstance(stages, list):
            continue
        for st in stages:
            if not isinstance(st, dict):
                continue
            if st.get("stage_name") != STAGE_NAME:
                continue
            kf = st.get("key_fields") if isinstance(st.get("key_fields"), dict) else {}
            ha = kf.get("hard_audit") if isinstance(kf.get("hard_audit"), dict) else {}
            wb = kf.get("whitebox_extension") if isinstance(kf.get("whitebox_extension"), dict) else {}
            yield {
                "source_root": source_root,
                "request_id": rid,
                "stage_name": STAGE_NAME,
                "submit_gate_position": kf.get("submit_gate_position"),
                "submit_shadow_result": kf.get("submit_shadow_result"),
                "submit_allowed": kf.get("submit_allowed"),
                "submit_block_reason": kf.get("submit_block_reason"),
                "source_submit_shadow_decision_id": kf.get("source_submit_shadow_decision_id"),
                "source_governance_decision_id": kf.get("source_governance_decision_id"),
                "hard_audit": ha,
                "hard_audit_ok": _hard_audit_ok(ha),
                "whitebox_extension": wb,
            }


def _matches(
    r: Dict[str, Any],
    *,
    submit_shadow_result: str,
    submit_gate_position: str,
    submit_allowed: str,
    request_id: Optional[str],
    hard_audit_only: bool,
) -> bool:
    if submit_shadow_result != "all" and r.get("submit_shadow_result") != submit_shadow_result:
        return False
    if submit_gate_position != "all" and r.get("submit_gate_position") != submit_gate_position:
        return False
    if request_id and r.get("request_id") != request_id:
        return False
    if submit_allowed != "all":
        want = submit_allowed == "true"
        if bool(r.get("submit_allowed")) != want:
            return False
    if hard_audit_only and r.get("hard_audit_ok") is True:
        return False
    return True


def _md_report(summary: Dict[str, Any], results: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Voice Governed Submit Unified Query Report (v0)")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(summary, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")
    lines.append("## Sample (first 10)")
    lines.append("")
    for i, r in enumerate(results[:10], start=1):
        lines.append(f"### Result {i}")
        lines.append("")
        compact = {k: r.get(k) for k in (
            "request_id",
            "submit_gate_position",
            "submit_shadow_result",
            "submit_allowed",
            "submit_block_reason",
            "hard_audit_ok",
            "source_submit_shadow_decision_id",
            "source_governance_decision_id",
        )}
        lines.append("```json")
        lines.append(json.dumps(compact, ensure_ascii=False, indent=2))
        lines.append("```")
        lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-root", required=True)
    ap.add_argument("--submit-shadow-result", default="all")
    ap.add_argument("--submit-gate-position", default="all")
    ap.add_argument("--submit-allowed", default="all")
    ap.add_argument("--request-id", default=None)
    ap.add_argument("--hard-audit-only", action="store_true")
    ap.add_argument("--export-format", default="json", choices=("json", "jsonl", "md"))
    ap.add_argument("--output-root", default=None)
    args = ap.parse_args()

    if args.submit_shadow_result not in ALLOWED_RESULTS:
        raise SystemExit(f"invalid --submit-shadow-result: {args.submit_shadow_result}")
    if args.submit_gate_position not in ALLOWED_POSITIONS:
        raise SystemExit(f"invalid --submit-gate-position: {args.submit_gate_position}")
    if args.submit_allowed not in ALLOWED_BOOL:
        raise SystemExit(f"invalid --submit-allowed: {args.submit_allowed}")

    input_root = Path(args.input_root)
    chains_path = input_root / "voice_governed_submit_enhanced_request_chains.json"
    if not chains_path.exists():
        raise SystemExit(f"missing enhanced chains: {chains_path}")

    enhanced = _read_json(chains_path)
    if not isinstance(enhanced, list):
        raise SystemExit("enhanced chains must be a list")

    rows = list(_iter_gate_records(enhanced, source_root=str(input_root)))
    filtered = [
        r
        for r in rows
        if _matches(
            r,
            submit_shadow_result=args.submit_shadow_result,
            submit_gate_position=args.submit_gate_position,
            submit_allowed=args.submit_allowed,
            request_id=args.request_id,
            hard_audit_only=bool(args.hard_audit_only),
        )
    ]

    out_root = _mk_out_root(args.output_root)
    summary = {
        "phase": "Phase-Voice-OutputGovernance-009",
        "tool": "query_voice_governed_submit_unified_view_v0.py",
        "input_root": str(input_root),
        "filters": {
            "submit_shadow_result": args.submit_shadow_result,
            "submit_gate_position": args.submit_gate_position,
            "submit_allowed": args.submit_allowed,
            "request_id": args.request_id,
            "hard_audit_only": bool(args.hard_audit_only),
        },
        "counts": {
            "total_gate_stage_records": len(rows),
            "matched_gate_stage_records": len(filtered),
        },
        "notes": ["offline/shadow only", "no real submit invoked"],
    }

    _write_json(out_root / "voice_governed_submit_unified_query_summary.json", summary)
    _write_json(out_root / "voice_governed_submit_unified_query_results.json", filtered)
    _write_jsonl(out_root / "voice_governed_submit_unified_query_results.jsonl", filtered)
    (out_root / "voice_governed_submit_unified_query_report.md").write_text(_md_report(summary, filtered), encoding="utf-8")

    print(str(out_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

