#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Post-Migration Engineering Smoke Test v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.post_migration_engineering_smoke_test_v1 import (
    run_post_migration_engineering_smoke_test_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "post_migration_engineering_smoke_test_v1_smoke_v0"
DEFAULT_ROADMAP_ROOT = None
DEFAULT_EVAL_BASE = None

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("post_migration_smoke_test_policy", "post_migration_smoke_test_policy_v1.json"),
    ("roadmap_decision_input_review", "roadmap_decision_input_review_v1.json"),
    ("python_import_smoke_result", "python_import_smoke_result_v1.json"),
    ("capabilities_module_import_smoke_result", "capabilities_module_import_smoke_result_v1.json"),
    ("midplatform_module_import_smoke_result", "midplatform_module_import_smoke_result_v1.json"),
    ("runner_verifier_execution_smoke_result", "runner_verifier_execution_smoke_result_v1.json"),
    ("config_readability_smoke_result", "config_readability_smoke_result_v1.json"),
    ("docs_index_link_smoke_result", "docs_index_link_smoke_result_v1.json"),
    ("phase_verdict_table_smoke_result", "phase_verdict_table_smoke_result_v1.json"),
    ("protected_eval_out_mutation_guard_smoke_result", "protected_eval_out_mutation_guard_smoke_result_v1.json"),
    ("smoke_test_issue_register", "smoke_test_issue_register_v1.json"),
    ("smoke_test_readiness_decision", "smoke_test_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", default=str(REPO_ROOT))
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--engineering-mainline-roadmap-decision-root", default=None)
    p.add_argument("--eval-out-base", default=None)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    roadmap_root = args.engineering_mainline_roadmap_decision_root
    if not roadmap_root:
        print("error: --engineering-mainline-roadmap-decision-root is required", file=sys.stderr)
        return 2

    result = run_post_migration_engineering_smoke_test_v1(
        repo_root=args.repo_root,
        engineering_mainline_roadmap_decision_root=roadmap_root,
        eval_out_base=args.eval_out_base,
        output_root=args.output_root,
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
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
                "high_risk_count": summary.get("high_risk_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
