#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Static/Dynamic Target Locking & Tracking Planning v1."""

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
    DEFAULT_OUTPUT as DEFAULT_CONTINUITY_SKELETON_ROOT,
)
from capabilities.midplatform.field_scene_small_range_construction_core_definition_v1 import (
    DEFAULT_OUTPUT as DEFAULT_FIELD_SCENE_ROOT,
)
from capabilities.midplatform.static_dynamic_target_locking_tracking_planning_v1 import (
    DEFAULT_OUTPUT,
    run_static_dynamic_target_locking_tracking_planning_v1,
)

OUTPUT_FILES = (
    ("static_dynamic_target_locking_tracking_planning_report", "static_dynamic_target_locking_tracking_planning_report_v1.json"),
    ("target_classification_registry", "target_classification_registry_v1.json"),
    ("target_status_registry", "target_status_registry_v1.json"),
    ("static_target_lock_model", "static_target_lock_model_v1.json"),
    ("dynamic_target_track_model", "dynamic_target_track_model_v1.json"),
    ("target_task_impact_hint_policy", "target_task_impact_hint_policy_v1.json"),
    ("target_abnormal_case_policy", "target_abnormal_case_policy_v1.json"),
    ("target_mock_case_registry", "target_mock_case_registry_v1.json"),
    ("target_mock_case_expected_results", "target_mock_case_expected_results_v1.json"),
    ("target_input_output_contract", "target_input_output_contract_v1.json"),
    ("target_next_implementation_plan", "target_next_implementation_plan_v1.json"),
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
    parser.add_argument("--continuity-skeleton-root", default=DEFAULT_CONTINUITY_SKELETON_ROOT)
    parser.add_argument("--field-scene-root", default=DEFAULT_FIELD_SCENE_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_static_dynamic_target_locking_tracking_planning_v1(
        continuity_skeleton_root=args.continuity_skeleton_root,
        field_scene_root=args.field_scene_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "static_dynamic_target_locking_tracking_planning_report_v1.md").write_text(
        result["static_dynamic_target_locking_tracking_planning_report_md"] + "\n", encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "static_dynamic_target_locking_tracking_planning_pass": s.get("static_dynamic_target_locking_tracking_planning_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "mock_case_count": s.get("mock_case_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
