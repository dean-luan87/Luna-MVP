#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Protocol Canonical Standard Planning v1."""

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

from capabilities.midplatform.protocol_canonical_standard_planning_v1 import (
    DEFAULT_OUTPUT,
    run_protocol_canonical_standard_planning_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("protocol_canonical_standard_plan", "protocol_canonical_standard_plan_v1.json"),
    ("protocol_numbering_standard", "protocol_numbering_standard_v1.json"),
    ("protocol_error_code_standard", "protocol_error_code_standard_v1.json"),
    ("protocol_execution_result_schema", "protocol_execution_result_schema_v1.json"),
    (
        "constitution_process_interface_assimilation_error_taxonomy",
        "constitution_process_interface_assimilation_error_taxonomy_v1.json",
    ),
    ("whitebox_diagnostic_binding_contract", "whitebox_diagnostic_binding_contract_v1.json"),
    ("protocol_first_development_rule", "protocol_first_development_rule_v1.json"),
    (
        "module_internal_vs_cross_module_protocol_layering",
        "module_internal_vs_cross_module_protocol_layering_v1.json",
    ),
    ("protocol_assimilation_supervision_standard", "protocol_assimilation_supervision_standard_v1.json"),
    ("protocol_failure_handling_notification_standard", "protocol_failure_handling_notification_standard_v1.json"),
    ("protocol_shared_code_design", "protocol_shared_code_design_v1.json"),
    ("protocol_shared_checker_flow", "protocol_shared_checker_flow_v1.json"),
    ("protocol_standard_api_contract", "protocol_standard_api_contract_v1.json"),
    ("protocol_standard_verifier_contract", "protocol_standard_verifier_contract_v1.json"),
    ("protocol_error_object_schema", "protocol_error_object_schema_v1.json"),
    ("protocol_health_monitor_contract", "protocol_health_monitor_contract_v1.json"),
    ("protocol_template_reuse_contract", "protocol_template_reuse_contract_v1.json"),
    ("existing_protocol_classification_registry", "existing_protocol_classification_registry_v1.json"),
    ("existing_protocol_layer_mapping", "existing_protocol_layer_mapping_v1.json"),
    ("existing_protocol_error_namespace_mapping", "existing_protocol_error_namespace_mapping_v1.json"),
    (
        "existing_protocol_whitebox_binding_candidate_map",
        "existing_protocol_whitebox_binding_candidate_map_v1.json",
    ),
    ("existing_protocol_governance_debt_update", "existing_protocol_governance_debt_update_v1.json"),
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
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_protocol_canonical_standard_planning_v1(output_root=args.output_root)
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "protocol_canonical_standard_plan_v1.md").write_text(
        result["protocol_canonical_standard_plan_md"] + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "planning_pass": summary.get("planning_pass"),
                "blocker_count": summary.get("blocker_count"),
                "protocol_canonical_standard_plan_complete": summary.get(
                    "protocol_canonical_standard_plan_complete"
                ),
                "existing_protocol_classification_complete": summary.get(
                    "existing_protocol_classification_complete"
                ),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase_primary": summary.get("recommended_next_phase_primary"),
                "recommended_next_phase_alt": summary.get("recommended_next_phase_alt"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
