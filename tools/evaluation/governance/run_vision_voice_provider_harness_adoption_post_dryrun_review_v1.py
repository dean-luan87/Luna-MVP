#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision / Voice Provider Harness Adoption Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_voice_provider_harness_adoption_post_dryrun_review_v1 import (
    run_vision_voice_provider_harness_adoption_post_dryrun_review_v1,
)

DEFAULT_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_voice_provider_harness_adoption_dryrun"
)
DEFAULT_HARNESS = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_provider_readiness_harness"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_voice_provider_harness_adoption_post_dryrun_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "vision_voice_harness_adoption_dryrun_input_review",
        "vision_voice_harness_adoption_dryrun_input_review_v1.json",
    ),
    (
        "vision_provider_readiness_candidate_review",
        "vision_provider_readiness_candidate_review_v1.json",
    ),
    (
        "voice_provider_readiness_candidate_review",
        "voice_provider_readiness_candidate_review_v1.json",
    ),
    (
        "vision_harness_contract_consumption_review",
        "vision_harness_contract_consumption_review_v1.json",
    ),
    (
        "voice_harness_contract_consumption_review",
        "voice_harness_contract_consumption_review_v1.json",
    ),
    ("vision_failure_route_review", "vision_failure_route_review_v1.json"),
    ("voice_failure_route_review", "voice_failure_route_review_v1.json"),
    (
        "vision_voice_boundary_guard_review",
        "vision_voice_boundary_guard_review_v1.json",
    ),
    ("harness_generalization_review", "harness_generalization_review_v1.json"),
    ("vision_voice_no_runtime_review", "vision_voice_no_runtime_review_v1.json"),
    (
        "vision_voice_harness_adoption_blocked_path_review",
        "vision_voice_harness_adoption_blocked_path_review_v1.json",
    ),
    (
        "vision_voice_harness_adoption_closure_decision",
        "vision_voice_harness_adoption_closure_decision_v1.json",
    ),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--vision-voice-provider-harness-adoption-dryrun-root",
        default=DEFAULT_DRYRUN,
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-root",
        default=DEFAULT_HARNESS,
    )
    args = p.parse_args()

    result = run_vision_voice_provider_harness_adoption_post_dryrun_review_v1(
        vision_voice_provider_harness_adoption_dryrun_root=(
            args.vision_voice_provider_harness_adoption_dryrun_root
        ),
        controlled_provider_readiness_harness_root=args.controlled_provider_readiness_harness_root,
        review_output_root=args.output_root,
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
                "harness_generalization_established": sm.get("harness_generalization_established"),
                "vision_voice_provider_harness_adoption_dryrun_closed": sm.get(
                    "vision_voice_provider_harness_adoption_dryrun_closed"
                ),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
