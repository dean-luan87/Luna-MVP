#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify Phase-Mainline-RuntimeReadiness-002 guarded trial definition artifacts.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _load(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _needs_keyword(forbidden: List[str], keywords: Tuple[str, ...]) -> bool:
    blob = " ".join(forbidden).lower()
    return any(k.lower() in blob for k in keywords)


def verify(output_root: Path) -> Tuple[bool, List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    req = [
        "mainline_guarded_trial_summary.json",
        "mainline_guarded_trial_matrix.json",
        "mainline_guarded_trial_env_flag_matrix.json",
        "mainline_guarded_trial_acceptance_matrix.json",
        "mainline_guarded_trial_abort_rollback_matrix.json",
        "mainline_guarded_trial_trw_requirement_matrix.json",
    ]
    for name in req:
        if not (output_root / name).is_file():
            errors.append(f"missing_file:{name}")

    if errors:
        return False, errors, warnings

    summary = _load(output_root / "mainline_guarded_trial_summary.json")
    matrix: List[Dict[str, Any]] = _load(output_root / "mainline_guarded_trial_matrix.json")
    env_rows: List[Dict[str, Any]] = _load(output_root / "mainline_guarded_trial_env_flag_matrix.json")
    trw: Dict[str, Any] = _load(output_root / "mainline_guarded_trial_trw_requirement_matrix.json")

    # A
    if not isinstance(summary, dict):
        errors.append("summary_not_object")

    # B,C,D — three trials
    caps = {row.get("capability") for row in matrix}
    if "yolo" not in caps:
        errors.append("missing_yolo_trial")
    if "ocr" not in caps:
        errors.append("missing_ocr_trial")
    if "qwen_voice" not in caps:
        errors.append("missing_qwen_voice_trial")

    # E
    for row in matrix:
        if row.get("default_enabled") is not False:
            errors.append(f"trial_default_enabled_not_false:{row.get('trial_name')}")

    # F global kill switch
    gks = summary.get("global_kill_switch") or {}
    if gks.get("flag_name") != "LUNA_DISABLE_ALL_GUARDED_TRIALS":
        errors.append("global_kill_switch_flag_name_mismatch")

    # G env flags non-empty
    if not env_rows:
        errors.append("env_flag_matrix_empty")

    # H,I,J — non-empty lists per trial
    for row in matrix:
        tn = row.get("trial_name")
        for field in ("acceptance_checks", "abort_conditions", "rollback_actions"):
            v = row.get(field)
            if not v or not isinstance(v, list):
                errors.append(f"empty_or_missing_{field}:{tn}")
            elif len(v) == 0:
                errors.append(f"empty_list_{field}:{tn}")

    # K TRW
    req_fields = trw.get("required_fields_all_trials") or []
    if not req_fields:
        errors.append("trw_required_fields_empty")

    # L forbidden keywords by capability
    for row in matrix:
        cap = row.get("capability")
        forb = row.get("forbidden_actions") or []
        if cap == "yolo":
            if not _needs_keyword(forb, ("downstream", "navigation", "world", "playback", "tts", "scene")):
                warnings.append("yolo_forbidden_actions_may_be_incomplete")
        elif cap == "ocr":
            if not _needs_keyword(forb, ("downstream", "navigation", "tts", "semantic", "world", "scene")):
                warnings.append("ocr_forbidden_actions_may_be_incomplete")
        elif cap == "qwen_voice":
            if not _needs_keyword(forb, ("governance", "world", "navigation")):
                warnings.append("qwen_forbidden_actions_may_be_incomplete")

    # M max readiness
    for row in matrix:
        m = row.get("max_allowed_readiness_level_after_pass")
        if m != "R3_guarded_wiring_ready":
            errors.append(f"max_readiness_not_R3:{row.get('trial_name')}")

    # N no real runtime activation
    c = summary.get("constraints") or {}
    if c.get("no_runtime_wiring") is not True:
        errors.append("constraints_no_runtime_wiring_not_true")
    if summary.get("verdict", {}).get("real_runtime_activation") != "NO_GO":
        errors.append("verdict_real_runtime_not_NO_GO")

    ok = len(errors) == 0
    return ok, errors, warnings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True, help="Directory containing definition JSON")
    args = ap.parse_args()
    requested_raw = args.output_root.strip()
    root = Path(requested_raw).expanduser().resolve()
    ok, errors, warnings = verify(root)
    result = {
        "ok": ok,
        # User-visible path (as passed on CLI; may be relative to cwd).
        "output_root_requested": requested_raw,
        # Canonical path after symlink resolution (used for file checks).
        "output_root_resolved": str(root),
        # Back-compat: same as output_root_resolved.
        "output_root": str(root),
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
