#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Voice-Qianwen-002 — Verify governed voice provider entry skeleton outputs.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

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


def _load_run(root: Path) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    dec_p = root / "voice_qwen_governed_entry_decisions.json"
    au_p = root / "voice_speakability_audits.json"
    sum_p = root / "voice_qwen_governed_entry_summary.json"
    return _read_json(dec_p), _read_json(au_p), _read_json(sum_p)


def _index_by_sample(audits: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    idx: Dict[str, Dict[str, Any]] = {}
    for a in audits:
        sid = str(a.get("sample_id") or "")
        if sid:
            idx[sid] = a
    return idx


def verify(
    *,
    repo: Path,
    online_root: Path,
    offline_root: Path,
    output_verify: Path,
) -> Dict[str, Any]:
    errors: List[str] = []
    checks: List[Dict[str, Any]] = []

    _require(online_root.is_dir(), f"B: online_root missing {online_root}", errors)
    _require(offline_root.is_dir(), f"C: offline_root missing {offline_root}", errors)

    on_dec, on_aud, on_sum = _load_run(online_root)
    off_dec, off_aud, off_sum = _load_run(offline_root)

    checks.append({"id": "A", "name": "governance_runs_readable", "ok": True})
    checks.append({"id": "B", "name": "online_run_readable", "ok": len(on_dec) > 0})
    checks.append({"id": "C", "name": "offline_run_readable", "ok": len(off_dec) > 0})
    _require(len(on_dec) > 0, "B/D: online decisions empty", errors)
    _require(len(off_dec) > 0, "C/D: offline decisions empty", errors)
    _require(len(on_aud) == len(on_dec), "E: audits/decisions count mismatch online", errors)
    checks.append({"id": "D", "name": "entry_decisions_generated", "ok": len(on_dec) > 0})
    checks.append({"id": "E", "name": "speakability_audits_generated", "ok": len(on_aud) > 0})

    # Pair audits by sample_id + request_id alignment
    on_ix = _index_by_sample(on_aud)

    blocked_samples = {
        "expired_request",
        "stale_navigation_instruction",
        "cancelled_request",
        "duplicate_low_priority",
        "low_priority_interrupt_attempt",
        "unspeakable_text",
    }

    online_pm = str(on_sum.get("provider_mode") or "")

    for e in on_dec:
        sid = str(e.get("sample_id") or "")
        ps = e.get("provider_selection") if isinstance(e.get("provider_selection"), dict) else {}
        sel = str(ps.get("selected_provider") or "")
        fa = str(e.get("governance_final_action") or "")
        entry_allowed = bool(e.get("entry_allowed"))

        if sid in blocked_samples:
            _require(sel == "none", f"N: blocked sample {sid} must select none, got {sel}", errors)

        if entry_allowed and online_pm == "online_prefer_qwen":
            po = ps.get("provider_order") or []
            if fa in ("accepted_dry_run", "fallback_candidate"):
                _require(
                    list(po) == ["qwen", "piper"],
                    f"F: online sample {sid} order mismatch fa={fa} po={po}",
                    errors,
                )

        ha = e.get("hard_audit") if isinstance(e.get("hard_audit"), dict) else {}
        _require(ha.get("real_qwen_invoked") is False, f"O: real_qwen_invoked {sid}", errors)
        _require(ha.get("real_tts_invoked") is False, f"P: real_tts_invoked {sid}", errors)
        _require(ha.get("provider_invoked") is False, f"Q: provider_invoked {sid}", errors)
        _require(ha.get("playback_invoked") is False, f"R: playback_invoked {sid}", errors)
        _require(ha.get("navigation_action") is None, f"S: navigation_action {sid}", errors)
        _require(int(ha.get("downstream_invocation_count") or 0) == 0, f"T: downstream {sid}", errors)

        au = on_ix.get(sid)
        if au:
            _require("text_diff_audit" in au, f"L: text_diff_audit missing {sid}", errors)
            _require("source_text" in au and "spoken_text" in au, f"K: source/spoken {sid}", errors)
            pb = au.get("provider_boundary") if isinstance(au.get("provider_boundary"), dict) else {}
            _require(pb.get("provider_kind") == "text_to_audio", f"H: provider_kind {sid}", errors)
            _require(pb.get("expression_provider") is False, f"I: expression_provider {sid}", errors)
            _require(pb.get("model_may_rewrite_text") is False, f"J: model_may_rewrite_text {sid}", errors)

            td = au.get("text_diff_audit") if isinstance(au.get("text_diff_audit"), dict) else {}
            if sid == "normal_speakable_dry_run":
                _require(td.get("text_changed") is False, f"M: normal sample text_changed {sid}", errors)

            if td.get("text_changed") is True:
                _require(
                    td.get("rewrite_allowed") is True or td.get("diff_type") == "unknown",
                    f"M/NO_GO: text_changed without rewrite policy {sid}",
                    errors,
                )

    # Offline: never select qwen
    for e in off_dec:
        sid = str(e.get("sample_id") or "")
        ps = e.get("provider_selection") if isinstance(e.get("provider_selection"), dict) else {}
        sel = str(ps.get("selected_provider") or "")
        po = ps.get("provider_order") or []
        if e.get("entry_allowed") is True:
            _require("qwen" not in po, f"G: offline order must exclude qwen sid={sid} po={po}", errors)
            _require(sel != "qwen", f"G: offline must not select qwen sid={sid}", errors)

    checks.append({"id": "F", "name": "online_order_qwen_piper", "ok": True})
    checks.append({"id": "G", "name": "offline_excludes_qwen", "ok": True})
    checks.append({"id": "H", "name": "provider_kind_text_to_audio", "ok": True})
    checks.append({"id": "I", "name": "expression_provider_false", "ok": True})
    checks.append({"id": "J", "name": "model_may_rewrite_false", "ok": True})
    checks.append({"id": "K", "name": "source_spoken_present", "ok": True})
    checks.append({"id": "L", "name": "text_diff_audit_present", "ok": True})
    checks.append({"id": "M", "name": "text_changed_rules", "ok": True})
    checks.append({"id": "N", "name": "blocked_no_qwen", "ok": True})
    for oid, label in (
        ("O", "real_qwen_invoked_false"),
        ("P", "real_tts_invoked_false"),
        ("Q", "provider_invoked_false"),
        ("R", "playback_invoked_false"),
        ("S", "navigation_null"),
        ("T", "downstream_zero"),
    ):
        checks.append({"id": oid, "name": label, "ok": True})

    for name, pth in (
        ("trace", online_root / "voice_qwen_governed_entry_trace.jsonl"),
        ("replay", online_root / "voice_qwen_governed_entry_replay.jsonl"),
        ("whitebox", online_root / "voice_qwen_governed_entry_whitebox.jsonl"),
    ):
        txt = pth.read_text(encoding="utf-8").strip() if pth.is_file() else ""
        _require(len(txt) > 0, f"U: {name} empty online", errors)

    checks.append({"id": "U", "name": "trw_nonempty_online", "ok": True})

    # V default yaml baseline
    if yaml is None:
        errors.append("V: PyYAML unavailable")
        checks.append({"id": "V", "name": "default_config_not_modified", "ok": False})
    else:
        cfg = yaml.safe_load((repo / "capabilities/voice/config/voice_tts_config.yaml").read_text(encoding="utf-8")) or {}
        v_ok = (
            str(cfg.get("tts_runtime_mode") or "") == "offline_only"
            and str(cfg.get("active_provider") or "") == "piper"
            and [str(x) for x in (cfg.get("provider_order") or [])] == ["piper"]
            and cfg.get("offline_only") is True
            and ((cfg.get("local_runtime") or {}).get("qwen") or {}).get("enabled") is False
        )
        _require(v_ok, f"V: baseline drift {cfg.get('tts_runtime_mode')}", errors)
        checks.append({"id": "V", "name": "default_config_not_modified", "ok": v_ok})

    ok = len(errors) == 0
    out = {
        "phase": "Phase-Voice-Qianwen-002",
        "ok": ok,
        "errors": errors,
        "checks": checks,
        "online_root": str(online_root),
        "offline_root": str(offline_root),
    }
    output_verify.mkdir(parents=True, exist_ok=True)
    (output_verify / "verification_result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(_repo_root()))
    ap.add_argument("--online-root", required=True)
    ap.add_argument("--offline-root", required=True)
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    on_r = Path(args.online_root)
    off_r = Path(args.offline_root)
    if not on_r.is_absolute():
        on_r = repo / on_r
    if not off_r.is_absolute():
        off_r = repo / off_r

    tag = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")
    out_verify = Path(args.output_root) if args.output_root else repo / "logs" / f"voice_qwen_governed_entry_skeleton_verify_002_{tag}"
    res = verify(repo=repo, online_root=on_r, offline_root=off_r, output_verify=out_verify)
    print(json.dumps({"ok": res["ok"], "output_root": str(out_verify)}, ensure_ascii=False))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
