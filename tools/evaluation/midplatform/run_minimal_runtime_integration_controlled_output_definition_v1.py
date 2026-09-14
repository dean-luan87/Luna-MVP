#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Runner for Minimal Runtime Integration Controlled Output Definition v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("summary.json", "summary"),
    ("input_root_matrix.json", "input_root_matrix"),
    ("controlled_output_definition.json", "controlled_output_definition"),
    ("speech_gate_controlled_output_contract.json", "speech_gate_controlled_output_contract"),
    ("vop_controlled_output_contract.json", "vop_controlled_output_contract"),
    ("tts_placeholder_policy.json", "tts_placeholder_policy"),
    ("user_visible_output_boundary.json", "user_visible_output_boundary"),
    ("output_abort_conditions.json", "output_abort_conditions"),
    ("output_recovery_policy.json", "output_recovery_policy"),
    ("controlled_output_observability.json", "controlled_output_observability"),
    ("go_no_go_criteria.json", "go_no_go_criteria"),
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

    from capabilities.midplatform.minimal_runtime_integration_controlled_output_definition_v1 import (
        run_minimal_runtime_integration_controlled_output_definition_v1,
    )

    result = run_minimal_runtime_integration_controlled_output_definition_v1(
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
                "definition_scope": result["summary"]["definition_scope"],
                "next_phase_recommendation": result["final"]["next_phase_recommendation"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
