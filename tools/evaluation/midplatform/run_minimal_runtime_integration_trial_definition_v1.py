#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Runner for Minimal Runtime Integration Trial Definition v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("summary.json", "summary"),
    ("input_root_matrix.json", "input_root_matrix"),
    ("minimal_runtime_trial_definition.json", "minimal_runtime_trial_definition"),
    ("runtime_module_boundary_matrix.json", "runtime_module_boundary_matrix"),
    ("trial_input_plan.json", "trial_input_plan"),
    ("trial_output_plan.json", "trial_output_plan"),
    ("trial_safety_envelope.json", "trial_safety_envelope"),
    ("abort_conditions.json", "abort_conditions"),
    ("rollback_plan.json", "rollback_plan"),
    ("observability_requirements.json", "observability_requirements"),
    ("go_no_go_criteria.json", "go_no_go_criteria"),
    ("future_trial_execution_contract.json", "future_trial_execution_contract"),
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
    ap.add_argument("--stabilization-root", required=True)
    ap.add_argument("--basic-navigation-loop-root", required=True)
    ap.add_argument("--safety-task-arbitration-root", required=True)
    ap.add_argument("--ownership-gate-root", required=True)
    ap.add_argument("--interruption-governance-root", required=True)
    ap.add_argument("--workspace-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min")
    args = ap.parse_args()

    output_root = _require_abs(args.output_root, "--output-root")
    output_root.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.minimal_runtime_integration_trial_definition_v1 import (
        run_minimal_runtime_integration_trial_definition_v1,
    )

    result = run_minimal_runtime_integration_trial_definition_v1(
        stabilization_root=str(_require_abs(args.stabilization_root, "stabilization")),
        basic_navigation_loop_root=str(_require_abs(args.basic_navigation_loop_root, "basic_navigation_loop")),
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
                "trial_mode": result["minimal_runtime_trial_definition"]["trial_mode"],
                "allowed_module_count": len(
                    result["runtime_module_boundary_matrix"]["allowed_in_future_minimal_trial"]
                ),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
