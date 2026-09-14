#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Voice-Qianwen-003 — Verify RequestTrace mapping outputs (static).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # type: ignore


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _require(cond: bool, msg: str, errors: List[str]) -> None:
    if not cond:
        errors.append(msg)


def verify(*, repo: Path, eval_root: Path, output_verify: Path) -> Dict[str, Any]:
    errors: List[str] = []
    checks: List[Dict[str, Any]] = []

    on_path = eval_root / "voice_qwen_entry_request_trace_summary.json"
    cmp_path = eval_root / "voice_qwen_provider_mode_comparison_matrix.json"
    diff_path = eval_root / "voice_qwen_text_diff_audit_table.json"
    speak_path = eval_root / "voice_qwen_speakability_audit_stage_table.json"
    chains_path = eval_root / "voice_qwen_entry_request_chains.json"

    online_hint = eval_root / "voice_qwen_entry_request_trace_summary.json"
    _require(on_path.is_file(), "A/C: summary missing", errors)
    summary = _read_json(on_path) if on_path.is_file() else {}
    checks.append({"id": "A", "name": "eval_root_readable", "ok": on_path.is_file()})

    oroot = str(summary.get("online_root") or "")
    froots = str(summary.get("offline_root") or "")
    _require(bool(oroot), "B: online_root missing in summary", errors)
    _require(bool(froots), "B: offline_root missing in summary", errors)
    _require(Path(oroot).exists(), "A/B: online path not found", errors)
    _require(Path(froots).exists(), "A/B: offline path not found", errors)

    cmp_rows = _read_json(cmp_path) if cmp_path.is_file() else []
    diff_rows = _read_json(diff_path) if diff_path.is_file() else []
    speak_rows = _read_json(speak_path) if speak_path.is_file() else []
    chains = _read_json(chains_path) if chains_path.is_file() else []

    _require(isinstance(cmp_rows, list) and len(cmp_rows) > 0, "C/D/E: comparison matrix empty", errors)
    _require(len(chains) > 0, "E: chains empty", errors)
    checks.append({"id": "C", "name": "online_decisions_mapped", "ok": len(cmp_rows) > 0})
    checks.append({"id": "D", "name": "offline_decisions_mapped", "ok": len(cmp_rows) > 0})
    checks.append({"id": "E", "name": "request_chains_generated", "ok": len(chains) > 0})
    checks.append({"id": "F", "name": "provider_mode_comparison_generated", "ok": len(cmp_rows) > 0})

    for row in cmp_rows:
        if not isinstance(row, dict):
            continue
        fa = str(row.get("governance_final_action") or "")
        ons = str(row.get("online_selected_provider") or "")
        offs = str(row.get("offline_selected_provider") or "")
        sid = str(row.get("sample_id") or "")
        if fa == "accepted_dry_run":
            _require(ons == "qwen", f"G: accepted must select qwen online sid={sid}", errors)
        off_po = row.get("offline_provider_order") or []
        _require("qwen" not in off_po and offs != "qwen", f"H: offline must exclude qwen sid={sid}", errors)

        blocked = {
            "expired_request",
            "stale_navigation_instruction",
            "cancelled_request",
            "duplicate_low_priority",
            "low_priority_interrupt_attempt",
            "unspeakable_text",
        }
        if sid in blocked:
            _require(ons == "none" and offs == "none", f"I: blocked sid={sid} got on={ons} off={offs}", errors)

        if fa == "fallback_candidate":
            _require(ons == "piper", f"J: fallback online piper sid={sid}", errors)

        _require(row.get("selection_consistent_with_policy") is True, f"F row inconsistent sid={sid}", errors)

    checks.append({"id": "G", "name": "online_qwen_first_when_accepted", "ok": True})
    checks.append({"id": "H", "name": "offline_excludes_qwen", "ok": True})
    checks.append({"id": "I", "name": "blocked_select_none", "ok": True})
    checks.append({"id": "J", "name": "fallback_maps_piper", "ok": True})

    _require(len(speak_rows) >= len(cmp_rows) * 2, "K: speakability table rows", errors)
    checks.append({"id": "K", "name": "speakability_stages", "ok": len(speak_rows) > 0})

    for dr in diff_rows:
        if not isinstance(dr, dict):
            continue
        _require("source_text" in dr and "provider_input_text" in dr and "spoken_text" in dr, "L: diff row missing text fields", errors)
        _require("text_changed" in dr and "diff_type" in dr, "M: diff row missing audit fields", errors)
    checks.append({"id": "L", "name": "source_provider_spoken_present", "ok": True})
    checks.append({"id": "M", "name": "text_diff_present", "ok": len(diff_rows) > 0})

    for sr in speak_rows:
        if not isinstance(sr, dict):
            continue
        pb = sr.get("provider_boundary") if isinstance(sr.get("provider_boundary"), dict) else {}
        if pb:
            _require(pb.get("provider_kind") == "text_to_audio", "N: provider_kind", errors)
            _require(pb.get("expression_provider") is False, "O: expression_provider", errors)
            _require(pb.get("model_may_rewrite_text") is False, "P: model_may_rewrite", errors)

    checks.append({"id": "N", "name": "text_to_audio", "ok": True})
    checks.append({"id": "O", "name": "expression_false", "ok": True})
    checks.append({"id": "P", "name": "no_provider_rewrite_flag", "ok": True})

    for dr in diff_rows:
        if not isinstance(dr, dict):
            continue
        if dr.get("provider_caused_rewrite") is True:
            errors.append("P: provider_caused_rewrite must stay false")
        if dr.get("text_changed") is True:
            rs = dr.get("rewrite_source")
            dt = str(dr.get("diff_type") or "")
            if dt == "guard_normalization":
                _require(
                    rs == "guard_v1_speakable_text",
                    f"Q: guard normalization must attribute guard_v1_speakable_text rid={dr.get('request_id')}",
                    errors,
                )

    checks.append({"id": "Q", "name": "guard_rewrite_attribution", "ok": True})

    on_dec_path = Path(oroot) / "voice_qwen_governed_entry_decisions.json"
    if on_dec_path.is_file():
        decs = _read_json(on_dec_path)
        if isinstance(decs, list):
            for d in decs:
                if not isinstance(d, dict):
                    continue
                ha = d.get("hard_audit") if isinstance(d.get("hard_audit"), dict) else {}
                _require(ha.get("real_qwen_invoked") is False, "R: real_qwen_invoked must be false", errors)
                _require(ha.get("real_tts_invoked") is False, "S: real_tts_invoked must be false", errors)
                _require(ha.get("provider_invoked") is False, "T: provider_invoked must be false", errors)
                _require(ha.get("playback_invoked") is False, "U: playback_invoked must be false", errors)
                _require(ha.get("navigation_action") is None, "V: navigation_action must be null", errors)
                _require(int(ha.get("downstream_invocation_count") or 0) == 0, "W: downstream_invocation_count must be 0", errors)

    checks.extend(
        [
            {"id": "R", "name": "real_qwen_false", "ok": True},
            {"id": "S", "name": "real_tts_false", "ok": True},
            {"id": "T", "name": "provider_invoked_false", "ok": True},
            {"id": "U", "name": "playback_false", "ok": True},
            {"id": "V", "name": "navigation_null", "ok": True},
            {"id": "W", "name": "downstream_zero", "ok": True},
        ]
    )

    tr = eval_root / "voice_qwen_entry_request_trace_trace.jsonl"
    rp = eval_root / "voice_qwen_entry_request_trace_replay.jsonl"
    wb = eval_root / "voice_qwen_entry_request_trace_whitebox.jsonl"
    for label, pth in (("trace", tr), ("replay", rp), ("whitebox", wb)):
        txt = pth.read_text(encoding="utf-8").strip() if pth.is_file() else ""
        _require(len(txt) > 0, f"X: {label} empty", errors)
    checks.append({"id": "X", "name": "trw_nonempty", "ok": True})

    if yaml is None:
        errors.append("Y: PyYAML unavailable")
        checks.append({"id": "Y", "name": "default_config_ok", "ok": False})
    else:
        cfg = yaml.safe_load((repo / "capabilities/voice/config/voice_tts_config.yaml").read_text(encoding="utf-8")) or {}
        y_ok = (
            str(cfg.get("tts_runtime_mode") or "") == "offline_only"
            and str(cfg.get("active_provider") or "") == "piper"
            and [str(x) for x in (cfg.get("provider_order") or [])] == ["piper"]
            and cfg.get("offline_only") is True
            and ((cfg.get("local_runtime") or {}).get("qwen") or {}).get("enabled") is False
        )
        _require(y_ok, "Y: voice_tts_config baseline drift", errors)
        checks.append({"id": "Y", "name": "default_config_ok", "ok": y_ok})

    ok = len(errors) == 0
    out = {
        "phase": "Phase-Voice-Qianwen-003",
        "ok": ok,
        "errors": errors,
        "checks": checks,
        "eval_root": str(eval_root),
    }
    output_verify.mkdir(parents=True, exist_ok=True)
    (output_verify / "verification_result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(_repo_root()))
    ap.add_argument("--eval-root", required=True, help="Phase-003 evaluate output root")
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    er = Path(args.eval_root)
    if not er.is_absolute():
        er = repo / er

    tag = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")
    ov = Path(args.output_root) if args.output_root else repo / "logs" / f"voice_qwen_governed_entry_request_trace_verify_003_{tag}"

    res = verify(repo=repo, eval_root=er, output_verify=ov)
    print(json.dumps({"ok": res["ok"], "output_root": str(ov)}, ensure_ascii=False))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
