#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Engineering Mainline Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.engineering_mainline_roadmap_decision_v1 import (
    run_engineering_mainline_roadmap_decision_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "engineering_mainline_roadmap_decision_v1_smoke_v0"
DEFAULT_RESUME_ROOT = None

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("engineering_mainline_roadmap_decision_policy", "engineering_mainline_roadmap_decision_policy_v1.json"),
    ("engineering_mainline_resume_input_review", "engineering_mainline_resume_input_review_v1.json"),
    ("feature_module_priority_matrix", "feature_module_priority_matrix_v1.json"),
    ("capability_layer_priority_matrix", "capability_layer_priority_matrix_v1.json"),
    ("midplatform_focus_readiness_review", "midplatform_focus_readiness_review_v1.json"),
    ("post_migration_smoke_test_route_review", "post_migration_smoke_test_route_review_v1.json"),
    ("roadmap_route_matrix", "roadmap_route_matrix_v1.json"),
    ("selected_route_decision", "selected_route_decision_v1.json"),
    ("roadmap_non_claims_register", "roadmap_non_claims_register_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--engineering-mainline-resume-root", default=str(DEFAULT_RESUME_ROOT))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_engineering_mainline_roadmap_decision_v1(
        engineering_mainline_resume_root=args.engineering_mainline_resume_root,
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
                "selected_route_id": summary.get("selected_route_id"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
                "recommended_parallel_or_next_test_phase": summary.get("recommended_parallel_or_next_test_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
