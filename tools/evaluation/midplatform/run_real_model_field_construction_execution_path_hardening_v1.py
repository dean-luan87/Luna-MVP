#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Real Model Field Construction Execution Path Hardening v1."""

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

from capabilities.midplatform.real_model_field_construction_execution_path_hardening_v1 import (
    DEFAULT_OUTPUT,
    run_real_model_field_construction_execution_path_hardening_v1,
)
from capabilities.midplatform.real_model_field_construction_success_path_hardening_v1 import (
    DEFAULT_OUTPUT as DEFAULT_HARDENING_ROOT,
)
from capabilities.midplatform.yolo_depth_controlled_real_model_dryrun_v1 import (
    DEFAULT_OUTPUT as DEFAULT_DRYRUN_ROOT,
)

OUTPUT_FILES = (
    ("real_model_field_construction_execution_path_hardening_report", "real_model_field_construction_execution_path_hardening_report_v1.json"),
    ("real_model_execution_authorization_resolved", "real_model_execution_authorization_resolved_v1.json"),
    ("real_frame_input_set_registry", "real_frame_input_set_registry_v1.json"),
    ("yolo_execution_path_result_registry", "yolo_execution_path_result_registry_v1.json"),
    ("depth_execution_path_result_registry", "depth_execution_path_result_registry_v1.json"),
    ("real_model_execution_path_result_registry", "real_model_execution_path_result_registry_v1.json"),
    ("real_field_construction_quality_report", "real_field_construction_quality_report_v1.json"),
    ("real_field_construction_baseline_registry", "real_field_construction_baseline_registry_v1.json"),
    ("real_model_execution_case_results", "real_model_execution_case_results_v1.json"),
    ("real_field_failure_localization_review", "real_field_failure_localization_review_v1.json"),
    ("real_field_traceability_review", "real_field_traceability_review_v1.json"),
    ("no_simulation_boundary_review", "no_simulation_boundary_review_v1.json"),
    ("readiness_for_real_field_quality_evaluation_review", "readiness_for_real_field_quality_evaluation_review_v1.json"),
    ("non_execution_boundary_review", "non_execution_boundary_review_v1.json"),
    ("file_size_governance_review", "file_size_governance_review_v1.json"),
    ("prohibited_scope", "prohibited_scope_v1.json"),
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
    parser.add_argument("--dryrun-root", default=DEFAULT_DRYRUN_ROOT)
    parser.add_argument("--hardening-root", default=DEFAULT_HARDENING_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_real_model_field_construction_execution_path_hardening_v1(
        dryrun_root=args.dryrun_root,
        hardening_root=args.hardening_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "real_model_field_construction_execution_path_hardening_report_v1.md").write_text(
        result["real_model_field_construction_execution_path_hardening_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "real_model_execution_path_hardening_pass": s.get("real_model_execution_path_hardening_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "execution_case_count": s.get("execution_case_count"),
        "enhanced_scene_count": s.get("execution_result_count"),
        "field_simulation_deferred": s.get("field_simulation_deferred"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
