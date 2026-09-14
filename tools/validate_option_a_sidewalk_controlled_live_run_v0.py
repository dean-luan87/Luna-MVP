#!/usr/bin/env python3
"""
Phase-RealSceneRun-002A
Validate an Option A sidewalk controlled live run archive.

This tool:
- Performs Option A scope checks on run_evidence.json
- Calls Fix-001 validator wrapper (Trial-002 validation wrapper)

It does NOT run any live trial.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from typing import Any, Dict, List


def _now_ms() -> int:
    return int(time.time() * 1000)


def _load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _run_trial002_wrapper(archive_root: str) -> Dict[str, Any]:
    cmd = [
        sys.executable,
        "tools/validate_controlled_live_evidence_collection_execution_v0.py",
        "--archive_root",
        archive_root,
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        return {
            "recommendation": "no_go",
            "hard_blockers": ["validator_failed_to_run"],
            "soft_followups": [],
            "details": {"stderr": p.stderr[-4000:], "stdout": p.stdout[-4000:]},
        }
    try:
        out = json.loads(p.stdout)
        return out.get("summary", {})
    except Exception:
        return {
            "recommendation": "no_go",
            "hard_blockers": ["validator_output_unparseable"],
            "soft_followups": [],
            "details": {"stdout_tail": p.stdout[-4000:]},
        }


def _scope_checks(run_evidence: Dict[str, Any]) -> Dict[str, Any]:
    hard: List[str] = []
    soft: List[str] = []

    if run_evidence.get("selected_option") != "OptionA_sidewalk_short_walk_observe":
        hard.append("selected_option_not_optionA")
    if run_evidence.get("scenario_id") != "sidewalk_short_walk_observe_v0":
        hard.append("scenario_id_mismatch")
    if run_evidence.get("evidence_type") != "controlled_live":
        hard.append("evidence_type_not_controlled_live")
    if run_evidence.get("input_source") != "mac_camera":
        hard.append("input_source_not_mac_camera")

    # Safety assertions must be true (Fix-001 already checks but keep explicit here)
    if run_evidence.get("no_execute_leakage_assertion") is not True:
        hard.append("no_execute_leakage_assertion_not_true")
    if run_evidence.get("no_default_on_assertion") is not True:
        hard.append("no_default_on_assertion_not_true")
    if run_evidence.get("no_side_effect_expansion_assertion") is not True:
        hard.append("no_side_effect_expansion_assertion_not_true")

    # Optional quality guidance (soft)
    if int(run_evidence.get("frame_count") or 0) <= 0:
        hard.append("frame_count_not_positive")

    return {"hard_blockers": hard, "soft_followups": soft}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive_root", required=True)
    args = ap.parse_args()

    archive_root = args.archive_root
    run_evidence_path = os.path.join(archive_root, "run_evidence.json")
    if not os.path.exists(run_evidence_path):
        raise SystemExit("missing run_evidence.json")

    run_evidence = _load_json(run_evidence_path)
    scope = _scope_checks(run_evidence)
    fix = _run_trial002_wrapper(archive_root)

    hard = list(scope.get("hard_blockers", [])) + list(fix.get("hard_blockers", []))
    soft = list(scope.get("soft_followups", [])) + list(fix.get("soft_followups", []))

    rec = "no_go" if hard else ("conditional_go" if soft or fix.get("recommendation") == "conditional_go" else "go")

    report = {
        "tool": "validate_option_a_sidewalk_controlled_live_run_v0",
        "phase": "Phase-RealSceneRun-002A",
        "generated_at_ms": _now_ms(),
        "archive_root": archive_root,
        "scope_checks": scope,
        "fix001_wrapper_summary": fix,
        "summary": {
            "recommendation": rec,
            "hard_blockers": hard,
            "soft_followups": soft,
        },
        "assertions": {
            "default_path_enabled": False,
            "full_controlled_trial_entered": False,
            "real_side_effects_expanded": False,
            "open_user_testing": False,
            "scope_expanded": False,
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

