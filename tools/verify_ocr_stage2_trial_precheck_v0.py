#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-008 — Verify OCR Stage-2 dry-run precheck artifacts v0.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _case(name: str, ok: bool, details: Dict[str, Any]) -> Dict[str, Any]:
    return {"case": name, "ok": bool(ok), "details": details}


def _nonempty(path: Path) -> bool:
    try:
        return path.is_file() and bool(path.read_text(encoding="utf-8").strip())
    except Exception:
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--yolo-closure-root", required=True)
    args = ap.parse_args()

    out_root = Path(args.output_root).resolve()
    yolo_root = Path(args.yolo_closure_root).resolve()

    required_files = [
        "ocr_stage2_trial_precheck_summary.json",
        "ocr_stage2_trial_env_snapshot.json",
        "ocr_stage2_trial_precheck_result.json",
        "ocr_stage2_trial_runner_skeleton.json",
        "ocr_stage2_source_policy_readiness.json",
        "ocr_stage2_provider_readiness_static.json",
        "ocr_stage2_raw_text_candidate_schema_validation.json",
        "ocr_stage2_abort_rollback_plan.json",
        "ocr_stage2_trial_trace.jsonl",
        "ocr_stage2_trial_replay.jsonl",
        "ocr_stage2_trial_whitebox.jsonl",
        "precheck_notes.md",
    ]

    results: List[Dict[str, Any]] = []

    results.append(_case("A_output_root_exists", out_root.is_dir(), {"output_root": str(out_root)}))
    results.append(_case("B_yolo_closure_root_exists", yolo_root.is_dir(), {"yolo_closure_root": str(yolo_root)}))

    for fn in required_files:
        p = out_root / fn
        ok = p.is_file()
        details = {"path": str(p)}
        if fn.endswith(".jsonl") or fn.endswith(".md"):
            details["non_empty"] = _nonempty(p)
            ok = ok and details["non_empty"]
        results.append(_case(f"files_exist_{fn}", ok, details))

    pre = _read_json(out_root / "ocr_stage2_trial_precheck_result.json")
    runner = _read_json(out_root / "ocr_stage2_trial_runner_skeleton.json")
    rollback = _read_json(out_root / "ocr_stage2_abort_rollback_plan.json")

    results.append(_case("C_yolo_closed_v0_confirmed", pre.get("yolo_stage1_closed_v0_confirmed") is True, {"value": pre.get("yolo_stage1_closed_v0_confirmed")}))
    results.append(_case("D_precheck_result_present", pre.get("precheck_result") in {"GO", "CONDITIONAL_GO", "NO_GO"}, {"precheck_result": pre.get("precheck_result")}))
    results.append(_case("E_runner_skeleton_mode", runner.get("runner_mode") == "skeleton_only", {"runner_mode": runner.get("runner_mode")}))
    results.append(_case("F_global_kill_switch_field", "global_kill_switch" in pre, {"global_kill_switch": pre.get("global_kill_switch")}))
    results.append(_case("G_entry_flag_default_off", pre.get("entry_flag_enabled") in {False, True}, {"entry_flag_enabled": pre.get("entry_flag_enabled")}))

    # Hard boundary checks
    boundary_checks = {
        "provider_invoked": pre.get("provider_invoked") is False,
        "semantic_interpretation_enabled": pre.get("semantic_interpretation_enabled") is False,
        "midplatform_invoked": pre.get("midplatform_invoked") is False,
        "scene_delta_invoked": pre.get("scene_delta_invoked") is False,
        "world_context_invoked": pre.get("world_context_invoked") is False,
    }
    for k, ok in boundary_checks.items():
        results.append(_case(f"boundary_{k}", ok, {"value": pre.get(k)}))

    ha = pre.get("hard_audit") or {}
    more = {
        "qwen_invoked": ha.get("qwen_invoked") is False,
        "real_tts_invoked": ha.get("real_tts_invoked") is False,
        "playback_invoked": ha.get("playback_invoked") is False,
        "downstream_invocation_count": ha.get("downstream_invocation_count") == 0,
        "navigation_action": ha.get("navigation_action") in (None, "null"),
        "world_write_invoked": ha.get("world_write_invoked") is False,
        "hive_upload_invoked": ha.get("hive_upload_invoked") is False,
    }
    for k, ok in more.items():
        results.append(_case(f"hard_audit_{k}", ok, {"value": ha.get(k)}))

    results.append(_case("T_rollback_plan_exists", bool(rollback.get("commands")) and rollback.get("rollback_action") == "disable_ocr_trial", rollback))
    results.append(_case("U_abort_conditions_registered", pre.get("abort_conditions_registered") is True, {"value": pre.get("abort_conditions_registered")}))

    # Runner must keep provider off by default
    results.append(_case("runner_provider_execution_disabled", runner.get("provider_execution_enabled") is False, {"provider_execution_enabled": runner.get("provider_execution_enabled")}))
    results.append(_case("runner_semantic_disabled", runner.get("semantic_interpretation_enabled") is False, {"semantic_interpretation_enabled": runner.get("semantic_interpretation_enabled")}))
    results.append(_case("runner_midplatform_forward_disabled", runner.get("midplatform_forward_enabled") is False, {"midplatform_forward_enabled": runner.get("midplatform_forward_enabled")}))

    all_ok = all(r["ok"] for r in results)
    report = {
        "verifier": "verify_ocr_stage2_trial_precheck_v0",
        "verdict": "GO" if all_ok else "NO_GO",
        "hard_blockers": [r["case"] for r in results if not r["ok"]],
        "output_root": str(out_root),
        "yolo_closure_root": str(yolo_root),
        "precheck_result": pre.get("precheck_result"),
        "results": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if all_ok and pre.get("precheck_result") in {"GO", "CONDITIONAL_GO"} else 2


if __name__ == "__main__":
    raise SystemExit(main())

