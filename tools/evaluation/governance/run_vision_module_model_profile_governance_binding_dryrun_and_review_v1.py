#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision Module Model Profile + Governance Binding DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    run_vision_module_model_profile_governance_binding_dryrun_and_review_v1,
)

DEFAULT_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_module_model_profile_governance_binding_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_module_model_profile_governance_binding_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "vision_module_model_profile_governance_binding_dryrun_review_policy",
        "vision_module_model_profile_governance_binding_dryrun_review_policy_v1.json",
    ),
    ("planning_input_review", "planning_input_review_v1.json"),
    (
        "vision_module_model_profile_governance_binding_candidate",
        "vision_module_model_profile_governance_binding_candidate_v1.json",
    ),
    (
        "vision_module_registry_qualification_review",
        "vision_module_registry_qualification_review_v1.json",
    ),
    (
        "vision_module_local_standard_qualification_review",
        "vision_module_local_standard_qualification_review_v1.json",
    ),
    (
        "vision_midplatform_binding_qualification_review",
        "vision_midplatform_binding_qualification_review_v1.json",
    ),
    ("vision_self_check_qualification_review", "vision_self_check_qualification_review_v1.json"),
    (
        "vision_interaction_check_qualification_review",
        "vision_interaction_check_qualification_review_v1.json",
    ),
    (
        "vision_candidate_only_qualification_review",
        "vision_candidate_only_qualification_review_v1.json",
    ),
    ("vision_no_bypass_qualification_review", "vision_no_bypass_qualification_review_v1.json"),
    (
        "vision_health_supervision_refs_qualification_review",
        "vision_health_supervision_refs_qualification_review_v1.json",
    ),
    ("vision_module_qualification_check", "vision_module_qualification_check_v1.json"),
    ("vision_module_qualification_closure_decision", "vision_module_qualification_closure_decision_v1.json"),
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
    args = p.parse_args()

    result = run_vision_module_model_profile_governance_binding_dryrun_and_review_v1(
        vision_module_model_profile_governance_binding_planning_root=args.planning_root,
        output_root=args.output_root,
    )

    out_root = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out_root / fname, result[key])

    sm = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out_root),
                "dryrun_and_review_pass": sm.get("dryrun_and_review_pass"),
                "qualification_mode": sm.get("qualification_mode"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
