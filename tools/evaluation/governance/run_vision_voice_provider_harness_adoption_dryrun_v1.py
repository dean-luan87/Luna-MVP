#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision / Voice Provider Harness Adoption DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_voice_provider_harness_adoption_dryrun_v1 import (
    run_vision_voice_provider_harness_adoption_dryrun_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/vision_voice_provider_harness_adoption_planning"
)
DEFAULT_HARNESS = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_provider_readiness_harness"
)
DEFAULT_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_next_roadmap_decision"
)
DEFAULT_VOV_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_ocr_voice_controlled_optimization_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/vision_voice_provider_harness_adoption_dryrun"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("vision_voice_harness_adoption_dryrun_policy", "vision_voice_harness_adoption_dryrun_policy_v1.json"),
    ("vision_voice_harness_adoption_planning_input_review", "vision_voice_harness_adoption_planning_input_review_v1.json"),
    ("vision_domain_config_consumption_result", "vision_domain_config_consumption_result_v1.json"),
    ("voice_domain_config_consumption_result", "voice_domain_config_consumption_result_v1.json"),
    ("vision_provider_readiness_candidate", "vision_provider_readiness_candidate_v1.json"),
    ("voice_provider_readiness_candidate", "voice_provider_readiness_candidate_v1.json"),
    ("vision_harness_contract_consumption_matrix", "vision_harness_contract_consumption_matrix_v1.json"),
    ("voice_harness_contract_consumption_matrix", "voice_harness_contract_consumption_matrix_v1.json"),
    ("vision_failure_route_dryrun_result", "vision_failure_route_dryrun_result_v1.json"),
    ("voice_failure_route_dryrun_result", "voice_failure_route_dryrun_result_v1.json"),
    ("vision_voice_boundary_guard_dryrun_result", "vision_voice_boundary_guard_dryrun_result_v1.json"),
    ("harness_generalization_dryrun_result", "harness_generalization_dryrun_result_v1.json"),
    ("vision_voice_no_runtime_audit", "vision_voice_no_runtime_audit_v1.json"),
    ("vision_voice_harness_adoption_blocked_path_result", "vision_voice_harness_adoption_blocked_path_result_v1.json"),
    ("vision_voice_harness_adoption_readiness_decision", "vision_voice_harness_adoption_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--vision-voice-provider-harness-adoption-planning-root", default=DEFAULT_PLANNING)
    p.add_argument("--controlled-provider-readiness-harness-root", default=DEFAULT_HARNESS)
    p.add_argument("--ocr-provider-next-roadmap-decision-root", default=DEFAULT_ROADMAP)
    p.add_argument(
        "--vision-ocr-voice-controlled-optimization-post-dryrun-review-root",
        default=DEFAULT_VOV_POST,
    )
    args = p.parse_args()

    result = run_vision_voice_provider_harness_adoption_dryrun_v1(
        vision_voice_provider_harness_adoption_planning_root=args.vision_voice_provider_harness_adoption_planning_root,
        controlled_provider_readiness_harness_root=args.controlled_provider_readiness_harness_root,
        ocr_provider_next_roadmap_decision_root=args.ocr_provider_next_roadmap_decision_root,
        vision_ocr_voice_controlled_optimization_post_dryrun_review_root=(
            args.vision_ocr_voice_controlled_optimization_post_dryrun_review_root
        ),
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
                "boundary_ok": sm.get("boundary_ok"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
