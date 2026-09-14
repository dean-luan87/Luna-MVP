#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Phase-003 guarded trial wiring path artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _load(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def verify(output_root: Path, repo_root: Path) -> Tuple[bool, List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    req = [
        "mainline_guarded_trial_wiring_summary.json",
        "mainline_guarded_trial_gate_decisions.json",
        "mainline_guarded_trial_wiring_path_matrix.json",
        "mainline_guarded_trial_env_snapshot.json",
        "mainline_guarded_trial_trw_validation_matrix.json",
        "mainline_guarded_trial_abort_rollback_hook_matrix.json",
    ]
    for name in req:
        if not (output_root / name).is_file():
            errors.append(f"missing_file:{name}")

    if errors:
        return False, errors, warnings

    summary = _load(output_root / "mainline_guarded_trial_wiring_summary.json")
    gates = _load(output_root / "mainline_guarded_trial_gate_decisions.json")
    wiring = _load(output_root / "mainline_guarded_trial_wiring_path_matrix.json")
    trw_m = _load(output_root / "mainline_guarded_trial_trw_validation_matrix.json")
    hooks = _load(output_root / "mainline_guarded_trial_abort_rollback_hook_matrix.json")

    # B three trials in decisions
    dec = gates.get("decisions") or {}
    for tn in ("yolo_guarded_trial_v1", "ocr_guarded_trial_v1", "qwen_voice_governed_entry_trial_v1"):
        if tn not in dec:
            errors.append(f"missing_trial_decision:{tn}")

    # C global kill under default env must be false
    gk = (gates.get("decisions") or {}).get("global_kill_switch_engaged")
    if gk is not False:
        errors.append("global_kill_expected_false_under_default_env")

    # D default_enabled — field name is implicit false via decision disabled
    for tn, row in dec.items():
        if tn == "global_kill_switch_engaged":
            continue
        if isinstance(row, dict) and row.get("default_enabled") is not False:
            errors.append(f"default_enabled_not_false:{tn}")

    # E entry flags false under default env
    for tn, row in dec.items():
        if tn == "global_kill_switch_engaged":
            continue
        if isinstance(row, dict) and row.get("entry_flag_enabled") is not False:
            errors.append(f"entry_flag_not_false_default:{tn}")

    # F,G,H,I default booleans
    for tn, row in dec.items():
        if tn == "global_kill_switch_engaged" or not isinstance(row, dict):
            continue
        if row.get("provider_invocation_allowed"):
            errors.append(f"provider_true:{tn}")
        if row.get("playback_allowed"):
            errors.append(f"playback_true:{tn}")
        if row.get("downstream_allowed"):
            errors.append(f"downstream_true:{tn}")
        if row.get("world_write_allowed"):
            errors.append(f"world_write_true:{tn}")

    # J invalid mode blocked
    probe = gates.get("invalid_mode_probe") or {}
    pr = probe.get("decision") or {}
    if pr.get("decision") != "blocked_invalid_mode":
        errors.append("invalid_mode_probe_not_blocked")

    # K TRW matrix non-empty
    if not trw_m:
        errors.append("trw_validation_matrix_empty")

    # L hooks matrix
    if not hooks:
        errors.append("abort_rollback_hook_matrix_empty")

    # M wiring matrix
    if not wiring:
        errors.append("wiring_path_matrix_empty")
    caps = {row.get("capability") for row in wiring}
    if not {"yolo", "ocr", "qwen_voice"}.issubset(caps):
        errors.append("wiring_matrix_missing_capability")

    # N runtime activation
    c = summary.get("constraints") or {}
    if c.get("no_runtime_activation") is not True:
        errors.append("constraints_no_runtime_activation")
    if summary.get("verdict", {}).get("real_runtime_activation") != "NO_GO":
        errors.append("verdict_real_runtime_not_NO_GO")

    # O no default policy change claim
    if c.get("no_default_provider_policy_change") is not True:
        errors.append("constraints_no_default_policy_change")

    # Module files exist
    mods = summary.get("modules") or {}
    for k, rel in mods.items():
        if not (repo_root / rel).is_file():
            errors.append(f"missing_module_file:{k}:{rel}")

    ok = len(errors) == 0
    return ok, errors, warnings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--repo-root", default="")
    args = ap.parse_args()
    out = Path(args.output_root).expanduser().resolve()
    repo = Path(args.repo_root).expanduser().resolve() if args.repo_root else out.parents[1]
    ok, errors, warnings = verify(out, repo)
    print(
        json.dumps(
            {
                "ok": ok,
                "output_root_requested": args.output_root.strip(),
                "output_root_resolved": str(out),
                "repo_root": str(repo),
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
