#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Return To Vision Mainline Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.vision.return_to_vision_mainline_planning_v1 import (
    run_return_to_vision_mainline_planning_v1,
)


DEFAULT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")
DEFAULT_OUTPUT_ROOT = DEFAULT_WORKSPACE_ROOT / "_eval_out" / "return_to_vision_mainline_planning_v1_smoke_v0"


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Return-To-Vision Mainline Planning v1")
    parser.add_argument("--workspace-root", default=str(DEFAULT_WORKSPACE_ROOT))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--preplan-input-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "return_to_vision_mainline_preplan_v1"),
    )
    parser.add_argument(
        "--ocr-final-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "ocr_mainline_final_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--minimal-runtime-integration-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "minimal_runtime_integration_closure_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_return_to_vision_mainline_planning_v1(
        preplan_input_root=args.preplan_input_root,
        ocr_final_closure_root=args.ocr_final_closure_root,
        minimal_runtime_integration_closure_root=args.minimal_runtime_integration_closure_root,
        workspace_root=args.workspace_root,
    )

    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    for name in (
        "summary",
        "input_root_matrix",
        "vision_mainline_planning_report",
        "vision_mainline_roadmap",
        "adopted_preplan_principles",
        "rejected_patterns_register",
        "midplatform_reuse_commitment",
        "duplicate_module_ban_list",
        "governance_boundary_matrix",
        "first_batch_phase_definitions",
        "deferred_capability_register",
        "deferred_worldmodel_memory_library_boundary",
        "worldmodel_memory_library_placeholder_plan",
        "vision_mainline_non_claims_register",
        "formal_readiness_gate",
        "next_phase_recommendation",
        "no_runtime_boundary_report",
        "no_write_boundary_report",
    ):
        _write_json(output_root / f"{name}.json", result[name])

    print(
        json.dumps(
            {
                "output_root": str(output_root),
                "formal_mainline_name": result["summary"]["formal_mainline_name"],
                "final_decision": result["summary"]["final_decision"],
                "recommended_next_phase": result["summary"]["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
