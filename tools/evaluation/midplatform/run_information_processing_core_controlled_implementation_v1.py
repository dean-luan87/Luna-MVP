#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Information Processing Core Controlled Implementation v1."""

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

from capabilities.midplatform.information_processing_core_controlled_implementation_v1 import (
    DEFAULT_OUTPUT,
    DEFAULT_WORK_MANUAL_ROOT,
    run_information_processing_core_controlled_implementation_v1,
)

OUTPUT_FILES = (
    ("information_processing_core_controlled_implementation_report", "information_processing_core_controlled_implementation_report_v1.json"),
    ("implemented_files_inventory", "implemented_files_inventory_v1.json"),
    ("implemented_types_summary", "implemented_types_summary_v1.json"),
    ("implemented_contracts_summary", "implemented_contracts_summary_v1.json"),
    ("implemented_classifiers_summary", "implemented_classifiers_summary_v1.json"),
    ("implemented_builders_summary", "implemented_builders_summary_v1.json"),
    ("implemented_validators_summary", "implemented_validators_summary_v1.json"),
    ("implemented_core_summary", "implemented_core_summary_v1.json"),
    ("information_type_registry", "information_type_registry_v1.json"),
    ("controlled_information_processing_smoke_result", "controlled_information_processing_smoke_result_v1.json"),
    ("core_capability_marking_result", "core_capability_marking_result_v1.json"),
    ("workload_control_validation", "workload_control_validation_v1.json"),
    ("non_execution_guard_validation", "non_execution_guard_validation_v1.json"),
    ("peripheral_constraint_review", "peripheral_constraint_review_v1.json"),
    ("strong_coupled_single_package_review", "strong_coupled_single_package_review_v1.json"),
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
    parser.add_argument("--work-manual-root", default=DEFAULT_WORK_MANUAL_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_information_processing_core_controlled_implementation_v1(
        work_manual_root=args.work_manual_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    md = result.get("information_processing_core_controlled_implementation_report_md", "")
    if md:
        (out / "information_processing_core_controlled_implementation_report_v1.md").write_text(md + "\n", encoding="utf-8")
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "information_processing_core_controlled_implementation_pass": s.get("information_processing_core_controlled_implementation_pass"),
        "all_smoke_cases_passed": s.get("all_smoke_cases_passed"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
