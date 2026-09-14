#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-011 — Verify OCR Stage-2 controlled provider trial artifacts v0.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _nonempty(path: Path) -> bool:
    try:
        return path.is_file() and bool(path.read_text(encoding="utf-8").strip())
    except Exception:
        return False


def _case(name: str, ok: bool, details: Dict[str, Any]) -> Dict[str, Any]:
    return {"case": name, "ok": bool(ok), "details": details}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--approval-root", required=True)
    ap.add_argument("--output-root", required=True)
    ap.add_argument(
        "--strict-rapidocr-012",
        action="store_true",
        help="Phase-012: require RapidOCR mainline, non-empty raw_text, GO_next_window; forbid macOS Vision selection.",
    )
    args = ap.parse_args()

    approval_root = Path(args.approval_root).expanduser()
    out_root = Path(args.output_root).expanduser()
    if not approval_root.is_absolute() or not out_root.is_absolute():
        raise SystemExit("ERROR: --approval-root and --output-root must be absolute paths")
    approval_root = approval_root.resolve()
    out_root = out_root.resolve()

    required_files = [
        "ocr_stage2_controlled_provider_summary.json",
        "ocr_stage2_input_snapshot_match.json",
        "ocr_stage2_provider_selection.json",
        "ocr_stage2_provider_invocation_result.json",
        "ocr_stage2_raw_text_candidate.json",
        "ocr_stage2_raw_text_candidate_schema_validation.json",
        "ocr_stage2_provider_latency_summary.json",
        "ocr_stage2_abort_rollback_report.json",
        "ocr_stage2_post_trial_report.json",
        "ocr_stage2_controlled_provider_trace.jsonl",
        "ocr_stage2_controlled_provider_replay.jsonl",
        "ocr_stage2_controlled_provider_whitebox.jsonl",
        "execution_notes.md",
    ]

    results: List[Dict[str, Any]] = []
    results.append(_case("A_output_root_exists", out_root.is_dir(), {"output_root": str(out_root)}))
    results.append(_case("B_approval_root_readable", approval_root.is_dir(), {"approval_root": str(approval_root)}))

    for fn in required_files:
        p = out_root / fn
        ok = p.is_file()
        d: Dict[str, Any] = {"path": str(p)}
        if fn.endswith((".jsonl", ".md")):
            d["non_empty"] = _nonempty(p)
            ok = ok and d["non_empty"]
        results.append(_case(f"files_exist_{fn}", ok, d))

    match = _read_json(out_root / "ocr_stage2_input_snapshot_match.json")
    results.append(_case("D_input_snapshot_match_true", match.get("input_snapshot_match") is True, {"input_snapshot_match": match.get("input_snapshot_match")}))

    cand_val = _read_json(out_root / "ocr_stage2_raw_text_candidate_schema_validation.json")
    results.append(_case("H_candidate_schema_valid", cand_val.get("schema_valid") is True, {"schema_valid": cand_val.get("schema_valid"), "blockers": cand_val.get("blockers")}))

    whitebox = (out_root / "ocr_stage2_controlled_provider_whitebox.jsonl").read_text(encoding="utf-8").strip().splitlines()[-1]
    try:
        wb = json.loads(whitebox)
    except Exception:
        wb = {}
    ha = (wb.get("hard_audit") or {}) if isinstance(wb, dict) else {}

    checks = {
        "I_semantic_false": ha.get("semantic_interpretation_enabled") is False,
        "J_midplatform_false": ha.get("midplatform_invoked") is False,
        "K_scene_delta_false": ha.get("scene_delta_invoked") is False,
        "L_world_context_false": ha.get("world_context_invoked") is False,
        "M_qwen_false": ha.get("qwen_invoked") is False,
        "N_real_tts_false": ha.get("real_tts_invoked") is False,
        "O_playback_false": ha.get("playback_invoked") is False,
        "P_downstream_zero": ha.get("downstream_invocation_count") == 0,
        "Q_navigation_null": ha.get("navigation_action") in (None, "null"),
        "R_world_write_false": ha.get("world_write_invoked") is False,
        "S_hive_upload_false": ha.get("hive_upload_invoked") is False,
        "T_network_false": ha.get("network_request_invoked") is False,
    }
    for k, ok in checks.items():
        results.append(_case(k, ok, {"hard_audit": ha}))

    all_ok = all(r["ok"] for r in results)
    post = _read_json(out_root / "ocr_stage2_post_trial_report.json")
    rec = post.get("post_trial_recommendation")

    if args.strict_rapidocr_012:
        sel = _read_json(out_root / "ocr_stage2_provider_selection.json")
        ps = str(sel.get("provider_selected") or "")
        cand = _read_json(out_root / "ocr_stage2_raw_text_candidate.json")
        raw_txt = str(cand.get("raw_text") or "").strip()
        strict_cases = [
            _case(
                "S012_provider_is_rapidocr",
                "rapidocr" in ps.lower() and "macos_vision" not in ps.lower(),
                {"provider_selected": ps},
            ),
            _case("S012_raw_text_nonempty", bool(raw_txt), {"raw_text_len": len(raw_txt)}),
            _case("S012_post_trial_go_next", rec == "GO_next_window", {"post_trial_recommendation": rec}),
        ]
        results.extend(strict_cases)
        all_ok = all(r["ok"] for r in results)
        verdict = "GO" if all_ok else "NO_GO"
    else:
        verdict = "GO" if all_ok and rec in {"GO_next_window", "CONDITIONAL_GO_repeat"} else "NO_GO"
    report = {
        "verifier": "verify_ocr_stage2_controlled_provider_trial_v0",
        "verdict": verdict,
        "post_trial_recommendation": rec,
        "hard_blockers": [r["case"] for r in results if not r["ok"]],
        "approval_root": str(approval_root),
        "output_root": str(out_root),
        "results": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

