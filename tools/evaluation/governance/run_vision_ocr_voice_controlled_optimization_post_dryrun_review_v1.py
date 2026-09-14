#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision / OCR / Voice Controlled Optimization Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_ocr_voice_controlled_optimization_post_dryrun_review_v1 import (
    run_vision_ocr_voice_controlled_optimization_post_dryrun_review_v1,
)

DEFAULT_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_ocr_voice_controlled_optimization_dryrun"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_ocr_voice_controlled_optimization_post_dryrun_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "controlled_optimization_dryrun_input_review",
        "controlled_optimization_dryrun_input_review_v1.json",
    ),
    ("vision_readiness_candidate_review", "vision_readiness_candidate_review_v1.json"),
    ("ocr_readiness_candidate_review", "ocr_readiness_candidate_review_v1.json"),
    ("voice_readiness_candidate_review", "voice_readiness_candidate_review_v1.json"),
    ("cross_chain_dependency_review", "cross_chain_dependency_review_v1.json"),
    ("model_registry_binding_review", "model_registry_binding_review_v1.json"),
    ("health_management_binding_review", "health_management_binding_review_v1.json"),
    ("constitution_boundary_review", "constitution_boundary_review_v1.json"),
    ("no_runtime_boundary_review", "no_runtime_boundary_review_v1.json"),
    ("blocked_path_review", "blocked_path_review_v1.json"),
    ("controlled_optimization_closure_decision", "controlled_optimization_closure_decision_v1.json"),
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
        "--vision-ocr-voice-controlled-optimization-dryrun-root",
        default=DEFAULT_DRYRUN,
    )
    args = p.parse_args()

    result = run_vision_ocr_voice_controlled_optimization_post_dryrun_review_v1(
        vision_ocr_voice_controlled_optimization_dryrun_root=(
            args.vision_ocr_voice_controlled_optimization_dryrun_root
        ),
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
                "controlled_optimization_dryrun_closed": sm.get("controlled_optimization_dryrun_closed"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
