#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Post-Migration Engineering State Sync v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.post_migration_engineering_state_sync_v1 import (
    run_post_migration_engineering_state_sync_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "post_migration_engineering_state_sync_v1_smoke_v0"
DEFAULT_CLOSURE_ROOT = REPO_ROOT / "_eval_out" / "main_project_structure_migration_final_closure_v1_smoke_v0"

JSON_OUTPUTS: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("current_project_structure_inventory", "current_project_structure_inventory_v1.json"),
    ("structure_documentation_sync_review", "structure_documentation_sync_review_v1.json"),
    ("reserved_but_not_implemented_module_register", "reserved_but_not_implemented_module_register_v1.json"),
    ("whitebox_test_backend_migration_status_review", "whitebox_test_backend_migration_status_review_v1.json"),
    ("midplatform_current_structure_sync", "midplatform_current_structure_sync_v1.json"),
    ("post_migration_engineering_test_plan", "post_migration_engineering_test_plan_v1.json"),
    ("engineering_state_sync_readiness_decision", "engineering_state_sync_readiness_decision_v1.json"),
)

MD_OUTPUTS: Tuple[Tuple[str, str], ...] = (
    ("current_project_structure_summary_md", "current_project_structure_summary_v1.md"),
    ("post_migration_work_summary_md", "post_migration_work_summary_v1.md"),
    ("post_migration_cursor_assistant_sync_pack_md", "post_migration_cursor_assistant_sync_pack_v1.md"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument(
        "--main-project-structure-migration-final-closure-root",
        default=str(DEFAULT_CLOSURE_ROOT),
    )
    p.add_argument("--repo-root", default=str(REPO_ROOT))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_post_migration_engineering_state_sync_v1(
        main_project_structure_migration_final_closure_root=args.main_project_structure_migration_final_closure_root,
        repo_root=args.repo_root,
    )
    out_root = Path(args.output_root)
    for key, filename in JSON_OUTPUTS:
        payload = result[key]
        if isinstance(payload, dict):
            _write_json(out_root / filename, payload)
        else:
            (out_root / filename).write_text(str(payload) + "\n", encoding="utf-8")

    for key, filename in MD_OUTPUTS:
        (out_root / filename).write_text(result[key] + "\n", encoding="utf-8")

    summary = result["summary"]
    print(
        json.dumps(
            {
                "phase": summary.get("phase"),
                "boundary_ok": summary.get("boundary_ok"),
                "hold_for_review": summary.get("hold_for_review"),
                "doc_high_risk_count": summary.get("doc_high_risk_count"),
                "reserved_module_count": summary.get("reserved_module_count"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
