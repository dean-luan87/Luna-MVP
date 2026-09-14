#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Field-First Core Model Room and Interface Logic Definition v1."""

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

from capabilities.midplatform.field_first_core_model_room_interface_logic_definition_v1 import (
    DEFAULT_OUTPUT,
    DEFAULT_ROLE_REDEF_ROOT,
    run_field_first_core_model_room_interface_logic_definition_v1,
)

OUTPUT_FILES = (
    ("model_room_interface_logic_report", "model_room_interface_logic_report_v1.json"),
    ("model_room_registry", "model_room_registry_v1.json"),
    ("open_source_reference_inventory", "open_source_reference_inventory_v1.json"),
    ("model_capability_mapping", "model_capability_mapping_v1.json"),
    ("model_adapter_interface", "model_adapter_interface_v1.json"),
    ("model_candidate_output_registry", "model_candidate_output_registry_v1.json"),
    ("field_model_input_contract_from_models", "field_model_input_contract_from_models_v1.json"),
    ("field_simulation_input_output_contract", "field_simulation_input_output_contract_v1.json"),
    ("midplatform_reasoning_model_input_output_contract", "midplatform_reasoning_model_input_output_contract_v1.json"),
    ("prohibited_model_outputs", "prohibited_model_outputs_v1.json"),
    ("deferred_model_integration_register", "deferred_model_integration_register_v1.json"),
    ("prior_asset_repositioning", "prior_asset_repositioning_v1.json"),
    ("interface_logic_flows", "interface_logic_flows_v1.json"),
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
    parser.add_argument("--role-redef-root", default=DEFAULT_ROLE_REDEF_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_field_first_core_model_room_interface_logic_definition_v1(
        role_redef_root=args.role_redef_root, output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "model_room_interface_logic_report_v1.md").write_text(result["model_room_interface_logic_report_md"] + "\n", encoding="utf-8")
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "field_first_core_model_room_interface_logic_definition_pass": s.get("field_first_core_model_room_interface_logic_definition_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
