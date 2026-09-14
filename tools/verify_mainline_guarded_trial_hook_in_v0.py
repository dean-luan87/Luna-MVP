#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Phase-004 guarded trial hook-in artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _load(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _load_jsonl(p: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if isinstance(obj, dict):
            rows.append(obj)
    return rows


def verify(output_root: Path) -> Tuple[bool, List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    req = [
        "mainline_guarded_trial_hook_in_summary.json",
        "mainline_guarded_trial_hook_results.json",
        "mainline_guarded_trial_gate_decisions.json",
        "mainline_guarded_trial_noop_matrix.json",
        "mainline_guarded_trial_side_effect_audit.json",
        "mainline_guarded_trial_hook_trace.jsonl",
        "mainline_guarded_trial_hook_replay.jsonl",
        "mainline_guarded_trial_hook_whitebox.jsonl",
        "evaluation_notes.md",
    ]
    for name in req:
        if not (output_root / name).is_file():
            errors.append(f"missing_file:{name}")

    if errors:
        return False, errors, warnings

    summary = _load(output_root / "mainline_guarded_trial_hook_in_summary.json")
    results = _load(output_root / "mainline_guarded_trial_hook_results.json")
    noop = _load(output_root / "mainline_guarded_trial_noop_matrix.json")
    side = _load(output_root / "mainline_guarded_trial_side_effect_audit.json")
    gates = _load(output_root / "mainline_guarded_trial_gate_decisions.json")
    trace = _load_jsonl(output_root / "mainline_guarded_trial_hook_trace.jsonl")
    replay = _load_jsonl(output_root / "mainline_guarded_trial_hook_replay.jsonl")
    white = _load_jsonl(output_root / "mainline_guarded_trial_hook_whitebox.jsonl")

    # A files exist already
    # B,C,D hook results exist for all three capabilities under default_env
    default_rows = [r for r in results if r.get("scenario") == "default_env"]
    caps = {r.get("hook_result", {}).get("capability") for r in default_rows if isinstance(r, dict)}
    if "yolo" not in caps:
        errors.append("missing_yolo_hook_result_default_env")
    if "ocr" not in caps:
        errors.append("missing_ocr_hook_result_default_env")
    if "qwen_voice" not in caps:
        errors.append("missing_qwen_voice_hook_result_default_env")

    # E,F,G,H,I,J,K,L,M from noop / side_effect audit
    for row in noop:
        if row.get("enabled") is not False:
            errors.append("enabled_not_false_default")
        if row.get("no_op") is not True:
            errors.append("noop_not_true_default")
    if side.get("runtime_invoked_any") is not False:
        errors.append("runtime_invoked_any_true")
    if side.get("provider_invoked_any") is not False:
        errors.append("provider_invoked_any_true")
    if side.get("playback_invoked_any") is not False:
        errors.append("playback_invoked_any_true")
    if int(side.get("downstream_invocation_count_sum") or 0) != 0:
        errors.append("downstream_invocation_count_nonzero")
    if side.get("world_write_invoked_any") is not False:
        errors.append("world_write_invoked_any_true")
    if side.get("navigation_action_any") is not False:
        errors.append("navigation_action_any_true")
    if side.get("default_behavior_changed_any") is not False:
        errors.append("default_behavior_changed_any_true")

    # N global kill honored: scenario must exist and gates show kill switch engaged
    kill_rows = [r for r in gates if r.get("scenario") == "global_kill_switch_true"]
    if not kill_rows:
        errors.append("missing_global_kill_scenario")
    else:
        gk = (kill_rows[0].get("gate_decisions") or {}).get("global_kill_switch_engaged")
        if gk is not True:
            errors.append("global_kill_not_engaged_in_gate_decisions")

    # O trace/replay/whitebox non-empty
    if len(trace) == 0:
        errors.append("trace_jsonl_empty")
    if len(replay) == 0:
        errors.append("replay_jsonl_empty")
    if len(white) == 0:
        errors.append("whitebox_jsonl_empty")

    # P no default provider policy changed: asserted by constraints
    c = summary.get("constraints") or {}
    if c.get("no_default_provider_policy_change") is not True:
        errors.append("constraints_no_default_provider_policy_change_not_true")

    ok = len(errors) == 0
    return ok, errors, warnings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()
    out = Path(args.output_root).expanduser().resolve()
    ok, errors, warnings = verify(out)
    print(
        json.dumps(
            {
                "ok": ok,
                "output_root_requested": args.output_root.strip(),
                "output_root_resolved": str(out),
                "errors": errors,
                "warnings": warnings,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

