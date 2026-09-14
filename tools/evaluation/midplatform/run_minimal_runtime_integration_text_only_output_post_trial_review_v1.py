#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Runner for Minimal Runtime Integration Text-Only Output Post-Trial Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("summary.json", "summary"),
    ("input_root_matrix.json", "input_root_matrix"),
    ("text_only_output_post_trial_review_report.json", "text_only_output_post_trial_review_report"),
    ("text_only_output_stability_review.json", "text_only_output_stability_review"),
    ("output_mode_boundary_review.json", "output_mode_boundary_review"),
    ("user_heard_assumption_review.json", "user_heard_assumption_review"),
    ("audio_runtime_boundary_review.json", "audio_runtime_boundary_review"),
    ("source_chain_review.json", "source_chain_review"),
    ("safety_priority_review.json", "safety_priority_review"),
    ("ownership_guard_review.json", "ownership_guard_review"),
    ("freshness_review.json", "freshness_review"),
    ("abort_coverage_review.json", "abort_coverage_review"),
    ("closure_readiness_decision.json", "closure_readiness_decision"),
    ("risk_register.json", "risk_register"),
    ("next_phase_recommendation.json", "next_phase_recommendation"),
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
    ap.add_argument("--text-only-trial-root", required=True)
    ap.add_argument("--controlled-output-definition-root", required=True)
    ap.add_argument("--post-shadow-review-root", required=True)
    ap.add_argument("--controlled-shadow-trial-root", required=True)
    ap.add_argument("--trial-definition-root", required=True)
    ap.add_argument("--stabilization-root", required=True)
    ap.add_argument("--safety-task-arbitration-root", required=True)
    ap.add_argument("--ownership-gate-root", required=True)
    ap.add_argument("--interruption-governance-root", required=True)
    ap.add_argument("--workspace-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min")
    args = ap.parse_args()

    output_root = _require_abs(args.output_root, "--output-root")
    output_root.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.minimal_runtime_integration_text_only_output_post_trial_review_v1 import (
        run_minimal_runtime_integration_text_only_output_post_trial_review_v1,
    )

    result = run_minimal_runtime_integration_text_only_output_post_trial_review_v1(
        text_only_trial_root=str(_require_abs(args.text_only_trial_root, "text_only_trial")),
        controlled_output_definition_root=str(
            _require_abs(args.controlled_output_definition_root, "controlled_output_definition")
        ),
        post_shadow_review_root=str(_require_abs(args.post_shadow_review_root, "post_shadow_review")),
        controlled_shadow_trial_root=str(
            _require_abs(args.controlled_shadow_trial_root, "controlled_shadow_trial")
        ),
        trial_definition_root=str(_require_abs(args.trial_definition_root, "trial_definition")),
        stabilization_root=str(_require_abs(args.stabilization_root, "stabilization")),
        safety_task_arbitration_root=str(
            _require_abs(args.safety_task_arbitration_root, "safety_task_arbitration")
        ),
        ownership_gate_root=str(_require_abs(args.ownership_gate_root, "ownership_gate")),
        interruption_governance_root=str(
            _require_abs(args.interruption_governance_root, "interruption_governance")
        ),
        workspace_root=str(_require_abs(args.workspace_root, "workspace")),
    )

    for filename, key in WRITES:
        _write_json(output_root / filename, result[key])

    print(
        json.dumps(
            {
                "output_root": str(output_root),
                "final_decision": result["summary"]["final_decision"],
                "review_scope": result["summary"]["review_scope"],
                "next_phase_recommendation": result["closure_readiness_decision"]["next_phase_recommendation"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
