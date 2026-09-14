#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Task Response Candidate Midplatform Integration Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.task_response_candidate_midplatform_integration_post_dryrun_review_v1 import (
    run_task_response_candidate_midplatform_integration_post_dryrun_review_v1,
)

DEFAULT_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "task_response_candidate_midplatform_integration_dryrun"
)
DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "task_response_candidate_midplatform_integration_post_dryrun_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("task_response_dryrun_input_review", "task_response_dryrun_input_review_v1.json"),
    ("task_response_flow_review", "task_response_flow_review_v1.json"),
    ("task_response_candidate_collection_review", "task_response_candidate_collection_review_v1.json"),
    ("task_response_candidate_contract_review", "task_response_candidate_contract_review_v1.json"),
    ("constitution_overlay_review", "constitution_overlay_review_v1.json"),
    ("output_arbitration_review", "output_arbitration_review_v1.json"),
    ("runtime_boundary_review", "runtime_boundary_review_v1.json"),
    ("blocked_path_review", "blocked_path_review_v1.json"),
    ("conflict_status_review", "conflict_status_review_v1.json"),
    ("post_dryrun_closure_decision", "post_dryrun_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    p.add_argument(
        "--task-response-candidate-midplatform-integration-dryrun-root",
        default=DEFAULT_DRYRUN_ROOT,
    )
    args = p.parse_args()

    result = run_task_response_candidate_midplatform_integration_post_dryrun_review_v1(
        task_response_candidate_midplatform_integration_dryrun_root=(
            args.task_response_candidate_midplatform_integration_dryrun_root
        ),
        review_output_root=args.output_root,
    )

    out_root = Path(args.output_root)
    for key, filename in OUTPUT_FILES:
        _write_json(out_root / filename, result[key])

    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out_root),
                "boundary_ok": summary.get("boundary_ok"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
