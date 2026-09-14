#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Module Integration Gap Consolidation v1."""

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

from capabilities.midplatform.module_integration_gap_consolidation_v1 import (
    DEFAULT_MODULE_DRYRUN_ROOT,
    DEFAULT_OUTPUT,
    run_module_integration_gap_consolidation_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("module_integration_gap_consolidation_report", "module_integration_gap_consolidation_report_v1.json"),
    ("integration_gap_consolidation_scope", "integration_gap_consolidation_scope_v1.json"),
    ("completed_module_inventory", "completed_module_inventory_v1.json"),
    ("remaining_gap_inventory", "remaining_gap_inventory_v1.json"),
    ("gap_classification_matrix", "gap_classification_matrix_v1.json"),
    ("module_chain_readiness_map", "module_chain_readiness_map_v1.json"),
    ("next_module_candidate_selection", "next_module_candidate_selection_v1.json"),
    ("do_not_reopen_do_not_overbuild_rules", "do_not_reopen_do_not_overbuild_rules_v1.json"),
    ("next_route_decision", "next_route_decision_v1.json"),
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
    parser.add_argument("--module-dryrun-root", default=DEFAULT_MODULE_DRYRUN_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_module_integration_gap_consolidation_v1(
        module_dryrun_root=args.module_dryrun_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "module_integration_gap_consolidation_report_v1.md").write_text(
        result["module_integration_gap_consolidation_report_md"] + "\n", encoding="utf-8",
    )
    summary = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "module_integration_gap_consolidation_pass": summary.get("module_integration_gap_consolidation_pass"),
        "selected_next_module": summary.get("selected_next_module"),
        "module_handoff_contract_gap_identified": summary.get("module_handoff_contract_gap_identified"),
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
