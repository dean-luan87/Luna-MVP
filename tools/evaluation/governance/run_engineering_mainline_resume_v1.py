#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Engineering Mainline Resume v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.engineering_mainline_resume_v1 import run_engineering_mainline_resume_v1

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "engineering_mainline_resume_v1_smoke_v0"
DEFAULT_SYNC_ROOT = REPO_ROOT / "_eval_out" / "post_migration_engineering_state_sync_v1_smoke_v0"
DEFAULT_CLOSURE_ROOT = None

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("engineering_mainline_resume_policy", "engineering_mainline_resume_policy_v1.json"),
    ("post_migration_state_sync_input_review", "post_migration_state_sync_input_review_v1.json"),
    ("engineering_focus_module_matrix", "engineering_focus_module_matrix_v1.json"),
    ("capability_layering_matrix", "capability_layering_matrix_v1.json"),
    ("mainline_resume_guardrails", "mainline_resume_guardrails_v1.json"),
    ("deferred_registers_handoff", "deferred_registers_handoff_v1.json"),
    ("engineering_resume_test_handoff", "engineering_resume_test_handoff_v1.json"),
    ("engineering_mainline_resume_decision", "engineering_mainline_resume_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--post-migration-engineering-state-sync-root", default=str(DEFAULT_SYNC_ROOT))
    p.add_argument(
        "--main-project-structure-migration-final-closure-root",
        default=None,
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_engineering_mainline_resume_v1(
        post_migration_engineering_state_sync_root=args.post_migration_engineering_state_sync_root,
        main_project_structure_migration_final_closure_root=args.main_project_structure_migration_final_closure_root,
    )
    out_root = Path(args.output_root)
    for key, filename in OUTPUT_FILES:
        _write_json(out_root / filename, result[key])

    summary = result["summary"]
    print(
        json.dumps(
            {
                "phase": summary.get("phase"),
                "boundary_ok": summary.get("boundary_ok"),
                "state_sync_upstream_confirmed": summary.get("state_sync_upstream_confirmed"),
                "resume_resign_after_state_sync": summary.get("resume_resign_after_state_sync"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
