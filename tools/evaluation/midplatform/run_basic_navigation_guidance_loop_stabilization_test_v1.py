#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Runner for Basic Navigation Guidance Loop Stabilization Test v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("summary.json", "summary"),
    ("input_root_matrix.json", "input_root_matrix"),
    ("stabilization_policy.json", "stabilization_policy"),
    ("stabilization_scenarios.json", "stabilization_scenarios"),
    ("stabilization_decision_candidates.json", "stabilization_decision_candidates"),
    ("baseline_vs_task_matrix.json", "baseline_vs_task_matrix"),
    ("safety_vs_navigation_matrix.json", "safety_vs_navigation_matrix"),
    ("safety_vs_ocr_matrix.json", "safety_vs_ocr_matrix"),
    ("voice_ownership_vs_interruption_matrix.json", "voice_ownership_vs_interruption_matrix"),
    ("speech_priority_vs_interruption_matrix.json", "speech_priority_vs_interruption_matrix"),
    ("freshness_repeat_resume_matrix.json", "freshness_repeat_resume_matrix"),
    ("context_preservation_matrix.json", "context_preservation_matrix"),
    ("handoff_boundary_matrix.json", "handoff_boundary_matrix"),
    ("no_runtime_boundary_report.json", "no_runtime_boundary_report"),
    ("no_write_boundary_report.json", "no_write_boundary_report"),
]


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            return parent
    return here.parents[3]


WS_ROOT = _find_ws_root()
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))


def _require_abs(path_str: str, label: str) -> Path:
    p = Path(path_str).expanduser()
    if not p.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {path_str}")
    return p.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--basic-navigation-loop-root", required=True)
    ap.add_argument("--safety-task-arbitration-root", required=True)
    ap.add_argument("--voice-command-ownership-gate-root", required=True)
    ap.add_argument("--voice-interruption-governance-root", required=True)
    ap.add_argument("--workspace-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min")
    args = ap.parse_args()

    output_root = _require_abs(args.output_root, "--output-root")
    output_root.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.basic_navigation_guidance_loop_stabilization_test_v1 import (
        run_basic_navigation_guidance_loop_stabilization_test_v1,
    )

    result = run_basic_navigation_guidance_loop_stabilization_test_v1(
        basic_navigation_loop_root=str(_require_abs(args.basic_navigation_loop_root, "basic_navigation_loop")),
        safety_task_arbitration_root=str(_require_abs(args.safety_task_arbitration_root, "safety_task_arbitration")),
        voice_command_ownership_gate_root=str(
            _require_abs(args.voice_command_ownership_gate_root, "voice_command_ownership_gate")
        ),
        voice_interruption_governance_root=str(
            _require_abs(args.voice_interruption_governance_root, "voice_interruption_governance")
        ),
        workspace_root=str(_require_abs(args.workspace_root, "workspace")),
    )

    for filename, key in WRITES:
        _write_json(output_root / filename, result[key])

    print(
        json.dumps(
            {
                "output_root": str(output_root),
                "final_decision": result["final"]["final_decision"],
                "scenario_count": result["stabilization_scenarios"]["stabilization_scenario_count"],
                "decision_count": result["stabilization_decision_candidates"][
                    "stabilization_decision_candidate_count"
                ],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
