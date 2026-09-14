#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Request DryRun v1."""

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
    DEFAULT_OUTPUT as DEFAULT_PROTOCOL_SMOKE_ROOT,
)
from capabilities.midplatform.protocol_input_output_symmetry_registry_patch_v1 import (
    DEFAULT_OUTPUT as DEFAULT_REGISTRY_PATCH_ROOT,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1 import (
    DEFAULT_OUTPUT as DEFAULT_OWNER_APPROVAL_POST_REVIEW_ROOT,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1 import (
    DEFAULT_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_ROOT,
    DEFAULT_OUTPUT,
    run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    (
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_report",
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_report_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_plan_integrity_validation",
        "task_manager_freeze_authorization_grant_owner_approval_request_plan_integrity_validation_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_input_candidate_validation",
        "task_manager_freeze_authorization_grant_owner_approval_request_input_candidate_validation_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_output_candidate_validation",
        "task_manager_freeze_authorization_grant_owner_approval_request_output_candidate_validation_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_input_output_traceability_validation",
        "task_manager_freeze_authorization_grant_owner_approval_request_input_output_traceability_validation_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_protocol_reference_validation",
        "task_manager_freeze_authorization_grant_owner_approval_request_protocol_reference_validation_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_protocol_traceability_validation",
        "task_manager_freeze_authorization_grant_owner_approval_request_protocol_traceability_validation_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_error_namespace_validation",
        "task_manager_freeze_authorization_grant_owner_approval_request_error_namespace_validation_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_whitebox_candidate_ref_validation",
        "task_manager_freeze_authorization_grant_owner_approval_request_whitebox_candidate_ref_validation_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_owner_operator_notification_candidate_validation",
        "task_manager_freeze_authorization_grant_owner_approval_request_owner_operator_notification_candidate_validation_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_rejection_reference_validation",
        "task_manager_freeze_authorization_grant_owner_approval_request_rejection_reference_validation_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_expiry_reference_validation",
        "task_manager_freeze_authorization_grant_owner_approval_request_expiry_reference_validation_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_revocation_reference_validation",
        "task_manager_freeze_authorization_grant_owner_approval_request_revocation_reference_validation_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_absence_validation",
        "task_manager_freeze_authorization_grant_owner_approval_request_absence_validation_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_boundary_validation",
        "task_manager_freeze_authorization_grant_owner_approval_request_boundary_validation_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_evidence_traceability",
        "task_manager_freeze_authorization_grant_owner_approval_request_evidence_traceability_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_governance_debt_validation",
        "task_manager_freeze_authorization_grant_owner_approval_request_governance_debt_validation_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_template_lineage",
        "task_manager_freeze_authorization_grant_owner_approval_request_template_lineage_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_validate_once_per_module_rule",
        "task_manager_freeze_authorization_grant_owner_approval_request_validate_once_per_module_rule_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_post_review_readiness",
        "task_manager_freeze_authorization_grant_owner_approval_request_post_review_readiness_v1.json",
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
    parser.add_argument(
        "--grant-owner-approval-request-planning-root",
        default=DEFAULT_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_ROOT,
    )
    parser.add_argument(
        "--grant-owner-approval-post-dryrun-review-root",
        default=DEFAULT_OWNER_APPROVAL_POST_REVIEW_ROOT,
    )
    parser.add_argument(
        "--input-output-registry-patch-root",
        default=DEFAULT_REGISTRY_PATCH_ROOT,
    )
    parser.add_argument("--protocol-smoke-root", default=DEFAULT_PROTOCOL_SMOKE_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1(
        grant_owner_approval_request_planning_root=args.grant_owner_approval_request_planning_root,
        grant_owner_approval_post_dryrun_review_root=args.grant_owner_approval_post_dryrun_review_root,
        input_output_registry_patch_root=args.input_output_registry_patch_root,
        protocol_shared_code_smoke_root=args.protocol_smoke_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_report_v1.md").write_text(
        result["task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_report_md"] + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "dryrun_pass": summary.get("dryrun_pass"),
                "blocker_count": summary.get("blocker_count"),
                "approval_request_candidate_validation_ok": summary.get("approval_request_candidate_validation_ok"),
                "template_lineage_ok": summary.get("template_lineage_ok"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("dryrun_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
