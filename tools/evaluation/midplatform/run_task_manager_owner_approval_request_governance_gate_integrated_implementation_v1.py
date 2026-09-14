#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Owner Approval Request Governance Gate Integrated Implementation v1."""

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

from capabilities.midplatform.task_manager_owner_approval_request_governance_gate_integrated_implementation_v1 import (
    DEFAULT_FINAL_GATE_PLANNING_ROOT,
    DEFAULT_OUTPUT,
    DEFAULT_POST_REVIEW_ROOT,
    run_task_manager_owner_approval_request_governance_gate_integrated_implementation_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("task_manager_owner_approval_request_governance_gate_integrated_plan", "task_manager_owner_approval_request_governance_gate_integrated_plan_v1.json"),
    ("integrated_roadmap_decision", "integrated_roadmap_decision_v1.json"),
    ("issuance_authorization_preparation_package", "issuance_authorization_preparation_package_v1.json"),
    ("missing_conditions_routing", "missing_conditions_routing_v1.json"),
    ("real_issuance_precondition_checklist", "real_issuance_precondition_checklist_v1.json"),
    ("record_approval_ack_evidence_closure_boundary", "record_approval_ack_evidence_closure_boundary_v1.json"),
    ("module_level_functional_slice_test_plan", "module_level_functional_slice_test_plan_v1.json"),
    ("governance_rule_reference", "governance_rule_reference_v1.json"),
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
    parser.add_argument("--post-review-root", default=DEFAULT_POST_REVIEW_ROOT)
    parser.add_argument("--final-gate-planning-root", default=DEFAULT_FINAL_GATE_PLANNING_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_owner_approval_request_governance_gate_integrated_implementation_v1(
        post_review_root=args.post_review_root,
        final_gate_planning_root=args.final_gate_planning_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "task_manager_owner_approval_request_governance_gate_integrated_plan_v1.md").write_text(
        result["task_manager_owner_approval_request_governance_gate_integrated_plan_md"] + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "integrated_implementation_pass": summary.get("integrated_implementation_pass"),
                "selected_route": summary.get("selected_route"),
                "integrated_plan_complete": summary.get("integrated_plan_complete"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("integrated_implementation_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
