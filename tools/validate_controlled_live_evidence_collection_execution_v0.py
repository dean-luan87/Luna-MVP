#!/usr/bin/env python3
"""
Phase-RealSceneTrial-002
Controlled Live Evidence Collection Execution v0 — validation wrapper.

This tool:
- Validates a given archive_root using Fix-001 validator.
- Produces a Trial-002 shaped structured JSON summary.

It does NOT run any live trial.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from typing import Any, Dict


def _now_ms() -> int:
    return int(time.time() * 1000)


def _run_fix001_validator(archive_root: str) -> Dict[str, Any]:
    cmd = [
        sys.executable,
        "tools/validate_controlled_live_run_evidence_capture_v0.py",
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
        return out.get("result", {})
    except Exception:
        return {
            "recommendation": "no_go",
            "hard_blockers": ["validator_output_unparseable"],
            "soft_followups": [],
            "details": {"stdout_tail": p.stdout[-4000:]},
        }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive_root", required=True, help="Archive root path to validate.")
    args = ap.parse_args()

    res = _run_fix001_validator(args.archive_root)
    report = {
        "tool": "validate_controlled_live_evidence_collection_execution_v0",
        "phase": "Phase-RealSceneTrial-002",
        "generated_at_ms": _now_ms(),
        "archive_root": args.archive_root,
        "summary": {
            "recommendation": res.get("recommendation", "no_go"),
            "hard_blockers": res.get("hard_blockers", []),
            "soft_followups": res.get("soft_followups", []),
            "details": res.get("details", {}),
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

