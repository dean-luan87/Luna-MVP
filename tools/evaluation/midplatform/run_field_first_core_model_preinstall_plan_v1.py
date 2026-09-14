#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Field-First Core Model Preinstall Plan v1."""

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

from capabilities.midplatform.field_first_core_ideal_operation_mechanism_and_model_requirement_mapping_v1 import (
    DEFAULT_OUTPUT as DEFAULT_IDEAL_OP_ROOT,
)
from capabilities.midplatform.field_first_core_recalibration_and_next_work_definition_v1 import (
    DEFAULT_OUTPUT as DEFAULT_RECAL_ROOT,
)
from capabilities.midplatform.field_first_core_role_function_redefinition_v1 import (
    DEFAULT_OUTPUT as DEFAULT_ROLE_REDEF_ROOT,
)
from capabilities.midplatform.field_first_core_model_preinstall_plan_v1 import (
    DEFAULT_OUTPUT,
    run_field_first_core_model_preinstall_plan_v1,
)

OUTPUT_FILES = (
    ("model_preinstall_plan_report", "model_preinstall_plan_report_v1.json"),
    ("model_room_registry", "model_room_registry_v1.json"),
    ("preinstall_manifest", "preinstall_manifest_v1.json"),
    ("model_download_authorization", "model_download_authorization_v1.json"),
    ("model_adapter_placeholder_registry", "model_adapter_placeholder_registry_v1.json"),
    ("model_capability_review_queue", "model_capability_review_queue_v1.json"),
    ("model_preinstall_status_matrix", "model_preinstall_status_matrix_v1.json"),
    ("prohibited_preinstall_actions", "prohibited_preinstall_actions_v1.json"),
    ("adapter_placeholder_contract", "adapter_placeholder_contract_v1.json"),
    ("next_document_review_targets", "next_document_review_targets_v1.json"),
    ("prior_asset_repositioning", "prior_asset_repositioning_v1.json"),
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
    parser.add_argument("--ideal-operation-root", default=DEFAULT_IDEAL_OP_ROOT)
    parser.add_argument("--role-redef-root", default=DEFAULT_ROLE_REDEF_ROOT)
    parser.add_argument("--recal-root", default=DEFAULT_RECAL_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_field_first_core_model_preinstall_plan_v1(
        ideal_operation_root=args.ideal_operation_root,
        role_redef_root=args.role_redef_root,
        recal_root=args.recal_root,
        output_root=args.output_root,
        repo_root=str(REPO_ROOT),
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "model_preinstall_plan_report_v1.md").write_text(result["model_preinstall_plan_report_md"] + "\n", encoding="utf-8")
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "field_first_core_model_preinstall_plan_pass": s.get("field_first_core_model_preinstall_plan_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
