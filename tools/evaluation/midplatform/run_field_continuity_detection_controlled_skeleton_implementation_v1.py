#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Field Continuity Detection Controlled Skeleton Implementation v1."""

from __future__ import annotations

import dataclasses
import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.field_continuity_detection_controlled_skeleton_implementation_v1 import (
    DEFAULT_OUTPUT,
    run_field_continuity_detection_controlled_skeleton_implementation_v1,
)
from capabilities.midplatform.field_continuity_detection_planning_v1 import DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT

OUTPUT_FILES = (
    ("field_continuity_controlled_skeleton_report", "field_continuity_controlled_skeleton_report_v1.json"),
    ("continuity_signal_scoring_registry", "continuity_signal_scoring_registry_v1.json"),
    ("continuity_decision_rule_registry", "continuity_decision_rule_registry_v1.json"),
    ("field_session_state_transition_registry", "field_session_state_transition_registry_v1.json"),
    ("continuity_mock_case_results", "continuity_mock_case_results_v1.json"),
    ("continuity_signal_bundle_results", "continuity_signal_bundle_results_v1.json"),
    ("continuity_decision_candidate_registry", "continuity_decision_candidate_registry_v1.json"),
    ("field_session_transition_validation_results", "field_session_transition_validation_results_v1.json"),
    ("non_execution_boundary_review", "non_execution_boundary_review_v1.json"),
    ("next_stage_split_plan", "next_stage_split_plan_v1.json"),
    ("prohibited_scope", "prohibited_scope_v1.json"),
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


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--planning-root", default=DEFAULT_PLANNING_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_field_continuity_detection_controlled_skeleton_implementation_v1(
        planning_root=args.planning_root, output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "field_continuity_controlled_skeleton_report_v1.md").write_text(result["field_continuity_controlled_skeleton_report_md"] + "\n", encoding="utf-8")
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "field_continuity_detection_controlled_skeleton_pass": s.get("field_continuity_detection_controlled_skeleton_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "all_mock_cases_passed": s.get("all_mock_cases_passed"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
