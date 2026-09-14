#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Field-First Core Role Function Redefinition v1."""

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

from capabilities.midplatform.field_first_core_role_function_redefinition_v1 import (
    DEFAULT_FIELD_FIRST_RECAL_ROOT,
    DEFAULT_OUTPUT,
    run_field_first_core_role_function_redefinition_v1,
)

OUTPUT_FILES = (
    ("field_first_core_role_function_redefinition_report", "field_first_core_role_function_redefinition_report_v1.json"),
    ("role_principles", "role_principles_v1.json"),
    ("role_separation_rules", "role_separation_rules_v1.json"),
    ("core_roles_register", "core_roles_register_v1.json"),
    ("drive_layer_roles_register", "drive_layer_roles_register_v1.json"),
    ("support_roles_register", "support_roles_register_v1.json"),
    ("role_main_chain", "role_main_chain_v1.json"),
    ("role_priority_register", "role_priority_register_v1.json"),
    ("prior_work_repositioning", "prior_work_repositioning_v1.json"),
    ("work_manual_outputs_definition", "work_manual_outputs_definition_v1.json"),
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
    parser.add_argument("--field-first-recal-root", default=DEFAULT_FIELD_FIRST_RECAL_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_field_first_core_role_function_redefinition_v1(
        field_first_recal_root=args.field_first_recal_root, output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "field_first_core_role_function_redefinition_report_v1.md").write_text(result["field_first_core_role_function_redefinition_report_md"] + "\n", encoding="utf-8")
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "field_first_core_role_function_redefinition_pass": s.get("field_first_core_role_function_redefinition_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
