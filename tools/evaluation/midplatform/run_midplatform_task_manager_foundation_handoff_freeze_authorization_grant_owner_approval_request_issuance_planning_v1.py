#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Request Issuance Planning v1."""

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

from capabilities.midplatform.protocol_canonical_standard_shared_code_smoke_v1 import (
    DEFAULT_OUTPUT as DEFAULT_SMOKE_ROOT,
)
from capabilities.midplatform.protocol_input_output_symmetry_registry_patch_v1 import (
    DEFAULT_OUTPUT as DEFAULT_REGISTRY_PATCH_ROOT,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1 import (
    DEFAULT_OUTPUT as DEFAULT_REQUEST_DRYRUN_ROOT,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_REQUEST_PLANNING_ROOT,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1 import (
    DEFAULT_OUTPUT as DEFAULT_REQUEST_POST_REVIEW_ROOT,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_v1 import (
    DEFAULT_OUTPUT,
    run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    (
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_plan",
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_plan_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_candidate_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_candidate_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_input_candidate_contract",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_input_candidate_contract_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_output_candidate_contract",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_output_candidate_contract_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_input_output_traceability_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_input_output_traceability_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_protocol_reference_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_protocol_reference_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_protocol_traceability_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_protocol_traceability_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_error_namespace_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_error_namespace_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_whitebox_candidate_ref_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_whitebox_candidate_ref_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_owner_operator_notification_candidate_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_owner_operator_notification_candidate_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_rejection_reference_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_rejection_reference_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_expiry_reference_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_expiry_reference_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_revocation_reference_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_revocation_reference_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_absence_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_absence_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_validate_once_reference",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_validate_once_reference_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_precondition_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_precondition_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_boundary_contract",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_boundary_contract_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_non_execution_constraints",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_non_execution_constraints_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_governance_debt_carryover",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_governance_debt_carryover_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_template_lineage",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_template_lineage_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_next_phase_readiness",
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_next_phase_readiness_v1.json",
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
    parser.add_argument("--grant-owner-approval-request-post-dryrun-review-root", default=DEFAULT_REQUEST_POST_REVIEW_ROOT)
    parser.add_argument("--grant-owner-approval-request-planning-root", default=DEFAULT_REQUEST_PLANNING_ROOT)
    parser.add_argument("--grant-owner-approval-request-dryrun-root", default=DEFAULT_REQUEST_DRYRUN_ROOT)
    parser.add_argument("--input-output-registry-patch-root", default=DEFAULT_REGISTRY_PATCH_ROOT)
    parser.add_argument("--protocol-shared-code-smoke-root", default=DEFAULT_SMOKE_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_v1(
        grant_owner_approval_request_post_dryrun_review_root=args.grant_owner_approval_request_post_dryrun_review_root,
        grant_owner_approval_request_planning_root=args.grant_owner_approval_request_planning_root,
        grant_owner_approval_request_dryrun_root=args.grant_owner_approval_request_dryrun_root,
        input_output_registry_patch_root=args.input_output_registry_patch_root,
        protocol_shared_code_smoke_root=args.protocol_shared_code_smoke_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (
        out / "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_plan_v1.md"
    ).write_text(
        result["task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_plan_md"]
        + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "issuance_planning_pass": summary.get("issuance_planning_pass") or summary.get("planning_pass"),
                "blocker_count": summary.get("blocker_count"),
                "validate_once_per_module_rule_ref_ok": summary.get("validate_once_per_module_rule_ref_ok"),
                "issuance_input_output_traceability_contract_complete": summary.get(
                    "issuance_input_output_traceability_contract_complete"
                ),
                "owner_approval_request_issued_absent": summary.get("owner_approval_request_issued_absent"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if (summary.get("issuance_planning_pass") or summary.get("planning_pass")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
