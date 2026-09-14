#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Field Continuity Detection Planning v1."""

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

from capabilities.midplatform.field_continuity_detection_planning_v1 import (
    DEFAULT_OUTPUT,
    run_field_continuity_detection_planning_v1,
)
from capabilities.midplatform.field_scene_small_range_construction_core_definition_v1 import (
    DEFAULT_OUTPUT as DEFAULT_FIELD_SCENE_ROOT,
)

OUTPUT_FILES = (
    ("field_continuity_detection_planning_report", "field_continuity_detection_planning_report_v1.json"),
    ("field_continuity_scope_definition", "field_continuity_scope_definition_v1.json"),
    ("field_continuity_signal_registry", "field_continuity_signal_registry_v1.json"),
    ("field_continuity_status_registry", "field_continuity_status_registry_v1.json"),
    ("field_continuity_decision_model", "field_continuity_decision_model_v1.json"),
    ("field_session_state_machine", "field_session_state_machine_v1.json"),
    ("field_continuity_abnormal_case_policy", "field_continuity_abnormal_case_policy_v1.json"),
    ("field_continuity_mock_case_registry", "field_continuity_mock_case_registry_v1.json"),
    ("field_continuity_mock_case_expected_results", "field_continuity_mock_case_expected_results_v1.json"),
    ("field_continuity_input_output_contract", "field_continuity_input_output_contract_v1.json"),
    ("field_continuity_next_implementation_plan", "field_continuity_next_implementation_plan_v1.json"),
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
    parser.add_argument("--field-scene-root", default=DEFAULT_FIELD_SCENE_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_field_continuity_detection_planning_v1(
        field_scene_root=args.field_scene_root, output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "field_continuity_detection_planning_report_v1.md").write_text(result["field_continuity_detection_planning_report_md"] + "\n", encoding="utf-8")
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "field_continuity_detection_planning_pass": s.get("field_continuity_detection_planning_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "mock_case_count": s.get("mock_case_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
