#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run First Person Vision Navigation Candidate Flow DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.first_person_vision_navigation_candidate_flow_dryrun_and_review_v1 import (
    run_first_person_vision_navigation_candidate_flow_dryrun_and_review_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_vision_navigation_candidate_flow_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_vision_navigation_candidate_flow_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "first_person_vision_navigation_candidate_flow_dryrun_review_policy",
        "first_person_vision_navigation_candidate_flow_dryrun_review_policy_v1.json",
    ),
    ("candidate_flow_planning_input_review", "candidate_flow_planning_input_review_v1.json"),
    ("sample_visual_observation_candidate", "sample_visual_observation_candidate_v1.json"),
    ("sample_ocr_result_candidate", "sample_ocr_result_candidate_v1.json"),
    ("sample_map_location_context_candidate", "sample_map_location_context_candidate_v1.json"),
    ("sample_route_context_candidate", "sample_route_context_candidate_v1.json"),
    ("sample_navigation_task_candidate", "sample_navigation_task_candidate_v1.json"),
    ("perception_zone_candidate_flow_review", "perception_zone_candidate_flow_review_v1.json"),
    ("visual_ocr_map_binding_review", "visual_ocr_map_binding_review_v1.json"),
    ("drive_observation_priority_review", "drive_observation_priority_review_v1.json"),
    (
        "information_integration_handoff_review",
        "information_integration_handoff_review_v1.json",
    ),
    ("candidate_not_fact_review", "candidate_not_fact_review_v1.json"),
    ("candidate_flow_boundary_audit", "candidate_flow_boundary_audit_v1.json"),
    ("candidate_flow_blocked_path_result", "candidate_flow_blocked_path_result_v1.json"),
    ("candidate_flow_closure_decision", "candidate_flow_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--planning-root", default=DEFAULT_PLANNING)
    args = p.parse_args()

    result = run_first_person_vision_navigation_candidate_flow_dryrun_and_review_v1(
        first_person_vision_navigation_candidate_flow_planning_root=args.planning_root,
        output_root=args.output_root,
    )

    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])

    sm = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "dryrun_and_review_pass": sm.get("dryrun_and_review_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_and_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
