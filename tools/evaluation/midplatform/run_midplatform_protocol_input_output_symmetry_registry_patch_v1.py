#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Protocol Input-Output Symmetry Registry Patch v1."""

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

from capabilities.midplatform.protocol_canonical_standard_planning_v1 import DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT
from capabilities.midplatform.protocol_canonical_standard_shared_code_smoke_v1 import (
    DEFAULT_OUTPUT as DEFAULT_SMOKE_ROOT,
)
from capabilities.midplatform.protocol_input_output_symmetry_registry_patch_v1 import (
    DEFAULT_OUTPUT,
    run_protocol_input_output_symmetry_registry_patch_v1,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1 import (
    DEFAULT_OUTPUT as DEFAULT_POST_REVIEW_ROOT,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    (
        "protocol_input_output_symmetry_registry_patch_report",
        "protocol_input_output_symmetry_registry_patch_report_v1.json",
    ),
    (
        "input_candidate_governance_protocol_registration",
        "input_candidate_governance_protocol_registration_v1.json",
    ),
    (
        "output_candidate_governance_protocol_registration",
        "output_candidate_governance_protocol_registration_v1.json",
    ),
    (
        "input_output_symmetry_protocol_registration",
        "input_output_symmetry_protocol_registration_v1.json",
    ),
    (
        "protocol_traceability_governance_protocol_registration",
        "protocol_traceability_governance_protocol_registration_v1.json",
    ),
    (
        "input_candidate_required_field_contract",
        "input_candidate_required_field_contract_v1.json",
    ),
    (
        "output_candidate_required_field_contract",
        "output_candidate_required_field_contract_v1.json",
    ),
    (
        "input_output_traceability_contract",
        "input_output_traceability_contract_v1.json",
    ),
    (
        "input_output_error_namespace_mapping",
        "input_output_error_namespace_mapping_v1.json",
    ),
    (
        "input_output_whitebox_candidate_ref_mapping",
        "input_output_whitebox_candidate_ref_mapping_v1.json",
    ),
    (
        "input_output_protocol_reference_rule_patch",
        "input_output_protocol_reference_rule_patch_v1.json",
    ),
    (
        "input_output_existing_protocol_classification_patch",
        "input_output_existing_protocol_classification_patch_v1.json",
    ),
    (
        "input_output_governance_debt_patch",
        "input_output_governance_debt_patch_v1.json",
    ),
    (
        "input_output_protocol_dependency_graph",
        "input_output_protocol_dependency_graph_v1.json",
    ),
    (
        "legacy_input_protocol_consolidation_map",
        "legacy_input_protocol_consolidation_map_v1.json",
    ),
    (
        "legacy_output_protocol_consolidation_map",
        "legacy_output_protocol_consolidation_map_v1.json",
    ),
    (
        "legacy_candidate_role_dual_mapping",
        "legacy_candidate_role_dual_mapping_v1.json",
    ),
    (
        "protocol_traceability_rule_contract",
        "protocol_traceability_rule_contract_v1.json",
    ),
    (
        "protocol_traceability_query_path_contract",
        "protocol_traceability_query_path_contract_v1.json",
    ),
    (
        "protocol_traceability_error_to_source_mapping",
        "protocol_traceability_error_to_source_mapping_v1.json",
    ),
    (
        "protocol_traceability_candidate_lineage_mapping",
        "protocol_traceability_candidate_lineage_mapping_v1.json",
    ),
    (
        "protocol_traceability_whitebox_candidate_mapping",
        "protocol_traceability_whitebox_candidate_mapping_v1.json",
    ),
    (
        "protocol_traceability_cursor_query_rule",
        "protocol_traceability_cursor_query_rule_v1.json",
    ),
    (
        "input_output_non_runtime_constraints",
        "input_output_non_runtime_constraints_v1.json",
    ),
    (
        "input_output_next_phase_readiness",
        "input_output_next_phase_readiness_v1.json",
    ),
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
    parser.add_argument("--planning-root", default=DEFAULT_PLANNING_ROOT)
    parser.add_argument("--shared-code-smoke-root", default=DEFAULT_SMOKE_ROOT)
    parser.add_argument("--owner-approval-post-review-root", default=DEFAULT_POST_REVIEW_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_protocol_input_output_symmetry_registry_patch_v1(
        planning_root=args.planning_root,
        shared_code_smoke_root=args.shared_code_smoke_root,
        owner_approval_post_review_root=args.owner_approval_post_review_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "protocol_input_output_symmetry_registry_patch_report_v1.md").write_text(
        result["protocol_input_output_symmetry_registry_patch_report_md"] + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "registry_patch_pass": summary.get("registry_patch_pass"),
                "blocker_count": summary.get("blocker_count"),
                "input_candidate_protocol_registered": summary.get("input_candidate_protocol_registered"),
                "output_candidate_protocol_registered": summary.get("output_candidate_protocol_registered"),
                "input_output_symmetry_protocol_registered": summary.get("input_output_symmetry_protocol_registered"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("registry_patch_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
