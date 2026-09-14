#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Project Organization Work Manual and Existing Work Mapping v1."""

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

from capabilities.midplatform.luna_project_organization_work_manual_and_existing_work_mapping_v1 import (
    DEFAULT_RECALIBRATION_ROOT,
    DEFAULT_OUTPUT,
    run_luna_project_organization_work_manual_and_existing_work_mapping_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("project_work_mode_definition", "project_work_mode_definition_v1.json"),
    ("standard_work_manual_template", "standard_work_manual_template_v1.json"),
    ("midplatform_organization_manual", "midplatform_organization_manual_v1.json"),
    ("existing_work_mapping_matrix", "existing_work_mapping_matrix_v1.json"),
    ("completed_artifact_reclassification", "completed_artifact_reclassification_v1.json"),
    ("missing_work_manual_gap_register", "missing_work_manual_gap_register_v1.json"),
    ("peripheral_overbuild_risk_review", "peripheral_overbuild_risk_review_v1.json"),
    ("next_work_governance_rules", "next_work_governance_rules_v1.json"),
    ("next_route_recommendation", "next_route_recommendation_v1.json"),
    ("file_size_governance_review", "file_size_governance_review_v1.json"),
    ("summary", "summary.json"),
)

MD_FILES: Tuple[Tuple[str, str], ...] = (
    ("project_work_mode_definition_md", "project_work_mode_definition_v1.md"),
    ("midplatform_organization_manual_md", "midplatform_organization_manual_v1.md"),
    ("existing_work_mapping_matrix_md", "existing_work_mapping_matrix_v1.md"),
    ("next_work_governance_rules_md", "next_work_governance_rules_v1.md"),
    ("core_capability_peripheral_service_recalibration_report_md", "project_work_mode_definition_v1.md"),
)


def _default(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, tuple):
        return list(obj)
    return str(obj)


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--recalibration-root", default=DEFAULT_RECALIBRATION_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_luna_project_organization_work_manual_and_existing_work_mapping_v1(
        recalibration_root=args.recalibration_root, output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "project_work_mode_definition_v1.md").write_text(result["project_work_mode_definition_md"] + "\n", encoding="utf-8")
    (out / "midplatform_organization_manual_v1.md").write_text(result["midplatform_organization_manual_md"] + "\n", encoding="utf-8")
    (out / "existing_work_mapping_matrix_v1.md").write_text(result["existing_work_mapping_matrix_md"] + "\n", encoding="utf-8")
    (out / "next_work_governance_rules_v1.md").write_text(result["next_work_governance_rules_md"] + "\n", encoding="utf-8")
    report_md = result.get("core_capability_peripheral_service_recalibration_report_md", "")
    if report_md:
        (out / "luna_project_organization_work_manual_mapping_report_v1.md").write_text(report_md + "\n", encoding="utf-8")
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "luna_project_organization_work_manual_mapping_pass": s.get("luna_project_organization_work_manual_mapping_pass"),
        "selected_next_route": s.get("selected_next_route"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "final_decision": s.get("final_decision"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
