#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Core Capability and Peripheral Service Recalibration v1."""

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

from capabilities.midplatform.core_capability_peripheral_service_recalibration_v1 import (
    DEFAULT_GAP_CONSOLIDATION_ROOT,
    DEFAULT_OUTPUT,
    run_core_capability_peripheral_service_recalibration_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("core_capability_peripheral_service_recalibration_report", "core_capability_peripheral_service_recalibration_report_v1.json"),
    ("recalibration_scope", "recalibration_scope_v1.json"),
    ("midplatform_capability_framework_definition", "midplatform_capability_framework_definition_v1.json"),
    ("midplatform_core_function_definition", "midplatform_core_function_definition_v1.json"),
    ("core_module_selection", "core_module_selection_v1.json"),
    ("peripheral_service_principle_matrix", "peripheral_service_principle_matrix_v1.json"),
    ("core_capability_marking_baseline", "core_capability_marking_baseline_v1.json"),
    ("conflict_resolution_rule", "conflict_resolution_rule_v1.json"),
    ("route_reassessment", "route_reassessment_v1.json"),
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
    parser.add_argument("--gap-consolidation-root", default=DEFAULT_GAP_CONSOLIDATION_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_core_capability_peripheral_service_recalibration_v1(
        gap_consolidation_root=args.gap_consolidation_root, output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        path = out / fname
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "core_capability_peripheral_service_recalibration_report_v1.md").write_text(
        result["core_capability_peripheral_service_recalibration_report_md"] + "\n", encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "core_capability_peripheral_service_recalibration_pass": s.get("core_capability_peripheral_service_recalibration_pass"),
        "selected_next_route": s.get("selected_next_route"),
        "handoff_contract_not_auto_selected": s.get("handoff_contract_not_auto_selected"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
