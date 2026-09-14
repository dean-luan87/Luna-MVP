#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Field-First Core Recalibration and Next Work Definition v1."""

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

from capabilities.midplatform.field_first_core_recalibration_and_next_work_definition_v1 import (
    DEFAULT_IPC_DESIGN_ROOT,
    DEFAULT_OUTPUT,
    run_field_first_core_recalibration_and_next_work_definition_v1,
)

OUTPUT_FILES = (
    ("field_first_core_recalibration_report", "field_first_core_recalibration_report_v1.json"),
    ("core_route_adjustment", "core_route_adjustment_v1.json"),
    ("field_first_core_concept_definition", "field_first_core_concept_definition_v1.json"),
    ("field_model_architecture_sketch", "field_model_architecture_sketch_v1.json"),
    ("source_mounting_model", "source_mounting_model_v1.json"),
    ("field_boundary_model", "field_boundary_model_v1.json"),
    ("field_continuity_model", "field_continuity_model_v1.json"),
    ("field_simulation_model", "field_simulation_model_v1.json"),
    ("midplatform_reasoning_input_model", "midplatform_reasoning_input_model_v1.json"),
    ("drive_layer_field_relationship", "drive_layer_field_relationship_v1.json"),
    ("perception_request_loop_model", "perception_request_loop_model_v1.json"),
    ("ipc_repositioning_review", "ipc_repositioning_review_v1.json"),
    ("deferred_route_register", "deferred_route_register_v1.json"),
    ("next_work_definition", "next_work_definition_v1.json"),
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


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--ipc-design-root", default=DEFAULT_IPC_DESIGN_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_field_first_core_recalibration_and_next_work_definition_v1(
        ipc_design_root=args.ipc_design_root, output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "field_first_core_recalibration_report_v1.md").write_text(result["field_first_core_recalibration_report_md"] + "\n", encoding="utf-8")
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "field_first_core_recalibration_pass": s.get("field_first_core_recalibration_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
