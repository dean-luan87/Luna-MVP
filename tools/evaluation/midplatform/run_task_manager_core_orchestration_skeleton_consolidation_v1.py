#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Task Manager Core Orchestration Skeleton Consolidation v1."""

from __future__ import annotations

import dataclasses
import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.candidate_lifecycle_unification_planning_v1 import DEFAULT_OUTPUT as DEFAULT_LIFECYCLE_ROOT
from capabilities.midplatform.evidence_record_approval_permission_alignment_planning_v1 import DEFAULT_OUTPUT as DEFAULT_ALIGNMENT_ROOT
from capabilities.midplatform.module_boundary_registry_planning_v1 import DEFAULT_OUTPUT as DEFAULT_BOUNDARY_ROOT
from capabilities.midplatform.task_manager_core_orchestration_skeleton_consolidation_v1 import (
    DEFAULT_OUTPUT,
    run_task_manager_core_orchestration_skeleton_consolidation_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("task_manager_core_orchestration_skeleton_consolidation_report", "task_manager_core_orchestration_skeleton_consolidation_report_v1.json"),
    ("orchestration_consolidation_scope", "orchestration_consolidation_scope_v1.json"),
    ("core_orchestration_skeleton_role_definition", "core_orchestration_skeleton_role_definition_v1.json"),
    ("orchestration_input_output_contract", "orchestration_input_output_contract_v1.json"),
    ("orchestration_flow_skeleton", "orchestration_flow_skeleton_v1.json"),
    ("orchestration_responsibility_matrix", "orchestration_responsibility_matrix_v1.json"),
    ("orchestration_non_execution_boundary", "orchestration_non_execution_boundary_v1.json"),
    ("orchestration_gap_register", "orchestration_gap_register_v1.json"),
    ("future_brain_interface_placeholder", "future_brain_interface_placeholder_v1.json"),
    ("next_route_decision", "next_route_decision_v1.json"),
    ("do_not_misclassify_rules", "do_not_misclassify_rules_v1.json"),
    ("file_size_governance_review", "file_size_governance_review_v1.json"),
    ("summary", "summary.json"),
)


def _default(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, tuple):
        return list(obj)
    return str(obj)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--module-boundary-registry-planning-root", default=DEFAULT_BOUNDARY_ROOT)
    parser.add_argument("--candidate-lifecycle-unification-planning-root", default=DEFAULT_LIFECYCLE_ROOT)
    parser.add_argument("--alignment-planning-root", default=DEFAULT_ALIGNMENT_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_core_orchestration_skeleton_consolidation_v1(
        module_boundary_registry_planning_root=args.module_boundary_registry_planning_root,
        candidate_lifecycle_unification_planning_root=args.candidate_lifecycle_unification_planning_root,
        alignment_planning_root=args.alignment_planning_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "task_manager_core_orchestration_skeleton_consolidation_report_v1.md").write_text(
        result["task_manager_core_orchestration_skeleton_consolidation_report_md"] + "\n", encoding="utf-8",
    )
    summary = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "orchestration_skeleton_consolidation_pass": summary.get("orchestration_skeleton_consolidation_pass"),
        "selected_next_route": summary.get("selected_next_route"),
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
