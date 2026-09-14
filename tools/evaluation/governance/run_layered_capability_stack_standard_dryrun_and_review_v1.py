#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Layered Capability Stack Standard DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.layered_capability_stack_standard_dryrun_and_review_v1 import (
    run_layered_capability_stack_standard_dryrun_and_review_v1,
)

DEFAULT_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/layered_capability_stack_standard_planning"
)
DEFAULT_FP_DECISION_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_decision_chain_candidate_dryrun"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "layered_capability_stack_standard_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("layered_capability_stack_standard_dryrun_policy", "layered_capability_stack_standard_dryrun_policy_v1.json"),
    ("planning_input_review", "planning_input_review_v1.json"),
    (
        "sample_ocr_module_capability_stack_definition",
        "sample_ocr_module_capability_stack_definition_v1.json",
    ),
    ("standard_adoption_dryrun_review", "standard_adoption_dryrun_review_v1.json"),
    ("exemplar_alignment_review", "exemplar_alignment_review_v1.json"),
    ("layer_dependency_validation_review", "layer_dependency_validation_review_v1.json"),
    ("dryrun_blocked_path_result", "dryrun_blocked_path_result_v1.json"),
    ("dryrun_boundary_audit", "dryrun_boundary_audit_v1.json"),
    ("dryrun_closure_decision", "dryrun_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--planning-root", default=DEFAULT_PLAN)
    p.add_argument("--first-person-decision-chain-dryrun-root", default=DEFAULT_FP_DECISION_DR)
    args = p.parse_args()

    result = run_layered_capability_stack_standard_dryrun_and_review_v1(
        layered_capability_stack_standard_planning_root=args.planning_root,
        first_person_scene_understanding_decision_chain_candidate_dryrun_root=args.first_person_decision_chain_dryrun_root,
        output_root=args.output_root,
    )

    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])

    sm = result["summary"]
    print(
        json.dumps(
            {
                "dryrun_and_review_pass": sm.get("dryrun_and_review_pass"),
                "final_decision": sm.get("final_decision"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_and_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
