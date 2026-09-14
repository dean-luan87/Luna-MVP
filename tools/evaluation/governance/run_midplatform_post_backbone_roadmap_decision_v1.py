#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Post-Backbone Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_post_backbone_roadmap_decision_v1 import (
    run_midplatform_post_backbone_roadmap_decision_v1,
)

DEFAULT_REVIEW_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_minimal_backbone_post_dryrun_review"
)
DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_post_backbone_roadmap_decision"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("post_backbone_roadmap_decision_policy", "post_backbone_roadmap_decision_policy_v1.json"),
    ("minimal_backbone_post_review_input_review", "minimal_backbone_post_review_input_review_v1.json"),
    ("route_a_task_response_candidate_assessment", "route_a_task_response_candidate_assessment_v1.json"),
    ("route_b_model_management_recovery_assessment", "route_b_model_management_recovery_assessment_v1.json"),
    ("route_selection_matrix", "route_selection_matrix_v1.json"),
    ("route_a_execution_preconditions", "route_a_execution_preconditions_v1.json"),
    ("route_b_defer_reason", "route_b_defer_reason_v1.json"),
    ("next_phase_readiness_decision", "next_phase_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    p.add_argument(
        "--midplatform-minimal-backbone-post-dryrun-review-root",
        default=DEFAULT_REVIEW_ROOT,
    )
    args = p.parse_args()

    result = run_midplatform_post_backbone_roadmap_decision_v1(
        midplatform_minimal_backbone_post_dryrun_review_root=(
            args.midplatform_minimal_backbone_post_dryrun_review_root
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
                "selected_route": summary.get("selected_route"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
