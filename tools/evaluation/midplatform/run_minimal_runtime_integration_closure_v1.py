#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Runner for Minimal Runtime Integration Closure v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("summary.json", "summary"),
    ("input_root_matrix.json", "input_root_matrix"),
    ("minimal_runtime_integration_closure_report.json", "minimal_runtime_integration_closure_report"),
    ("completed_phase_matrix.json", "completed_phase_matrix"),
    ("validated_capability_summary.json", "validated_capability_summary"),
    ("output_baseline_summary.json", "output_baseline_summary"),
    ("remaining_runtime_disabled_summary.json", "remaining_runtime_disabled_summary"),
    ("non_claims_register.json", "non_claims_register"),
    ("deferred_capability_pool.json", "deferred_capability_pool"),
    ("vision_mainline_handoff_plan.json", "vision_mainline_handoff_plan"),
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
    ap.add_argument("--trial-definition-root", required=True)
    ap.add_argument("--controlled-shadow-trial-root", required=True)
    ap.add_argument("--post-shadow-review-root", required=True)
    ap.add_argument("--controlled-output-definition-root", required=True)
    ap.add_argument("--text-only-trial-root", required=True)
    ap.add_argument("--text-only-post-trial-review-root", required=True)
    ap.add_argument("--stabilization-root", required=True)
    ap.add_argument("--safety-task-arbitration-root", required=True)
    ap.add_argument("--ownership-gate-root", required=True)
    ap.add_argument("--interruption-governance-root", required=True)
    ap.add_argument("--workspace-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min")
    args = ap.parse_args()

    output_root = _require_abs(args.output_root, "--output-root")
    output_root.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.minimal_runtime_integration_closure_v1 import (
        run_minimal_runtime_integration_closure_v1,
    )

    result = run_minimal_runtime_integration_closure_v1(
        trial_definition_root=str(_require_abs(args.trial_definition_root, "trial_definition")),
        controlled_shadow_trial_root=str(
            _require_abs(args.controlled_shadow_trial_root, "controlled_shadow_trial")
        ),
        post_shadow_review_root=str(_require_abs(args.post_shadow_review_root, "post_shadow_review")),
        controlled_output_definition_root=str(
            _require_abs(args.controlled_output_definition_root, "controlled_output_definition")
        ),
        text_only_trial_root=str(_require_abs(args.text_only_trial_root, "text_only_trial")),
        text_only_post_trial_review_root=str(
            _require_abs(args.text_only_post_trial_review_root, "text_only_post_trial_review")
        ),
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
                "closure_scope": result["summary"]["closure_scope"],
                "primary_next_phase_recommendation": result["final"]["primary_next_phase_recommendation"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
