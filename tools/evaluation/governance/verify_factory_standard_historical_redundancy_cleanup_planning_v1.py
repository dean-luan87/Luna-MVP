#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Factory Standard Historical Redundancy Cleanup Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    MERGEABLE_OCR_AUTHORIZATION_PHASES,
    STANDARD_ID,
)
from capabilities.governance.compressed_ocr_authorization_lifecycle_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as LIFECYCLE_DR_FINAL,
    NEXT_PHASE_GO as LIFECYCLE_DR_NEXT,
)
from capabilities.governance.factory_standard_historical_redundancy_cleanup_planning_v1 import (
    BOUNDARY_FALSE,
    CLEANUP_SCOPES,
    FINAL_DECISION_GO,
    FORBIDDEN_ACTIONS,
    FUTURE_REFERENCE_RULES,
    MARKER_STATUSES,
    METADATA_SCHEMA_FIELDS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
)

MIN_CHECKS = 70

REQUIRED = (
    "factory_standard_historical_cleanup_planning_policy_v1.json",
    "compressed_lifecycle_input_review_v1.json",
    "historical_redundancy_scope_v1.json",
    "superseded_phase_inventory_plan_v1.json",
    "absorbed_rule_inventory_plan_v1.json",
    "deprecated_for_new_phase_inventory_plan_v1.json",
    "read_only_evidence_source_register_plan_v1.json",
    "no_physical_delete_policy_v1.json",
    "historical_chain_preservation_policy_v1.json",
    "future_phase_reference_policy_v1.json",
    "cleanup_metadata_schema_v1.json",
    "cleanup_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "cleanup_planning_decision_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _item_schema_ok(item: Dict[str, Any]) -> bool:
    for field in METADATA_SCHEMA_FIELDS:
        if field not in item:
            return False
    return (
        item.get("keep_for_audit") is True
        and item.get("physical_delete_allowed") is False
        and item.get("migration_required") is False
    )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "factory_standard_historical_redundancy_cleanup_planning"
        ),
    )
    p.add_argument(
        "--compressed-ocr-authorization-lifecycle-dryrun-and-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "compressed_ocr_authorization_lifecycle_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    lifecycle_root = Path(args.compressed_ocr_authorization_lifecycle_dryrun_and_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    lifecycle_review = _load(root / "compressed_lifecycle_input_review_v1.json")
    scope = _load(root / "historical_redundancy_scope_v1.json")
    superseded = _load(root / "superseded_phase_inventory_plan_v1.json")
    absorbed = _load(root / "absorbed_rule_inventory_plan_v1.json")
    deprecated = _load(root / "deprecated_for_new_phase_inventory_plan_v1.json")
    read_only = _load(root / "read_only_evidence_source_register_plan_v1.json")
    no_delete = _load(root / "no_physical_delete_policy_v1.json")
    preservation = _load(root / "historical_chain_preservation_policy_v1.json")
    future_ref = _load(root / "future_phase_reference_policy_v1.json")
    schema = _load(root / "cleanup_metadata_schema_v1.json")
    dryrun_plan = _load(root / "cleanup_dryrun_plan_v1.json")
    decision = _load(root / "cleanup_planning_decision_v1.json")

    lifecycle_vr = _load(lifecycle_root / "verifier_report.json")
    lifecycle_sm = _load(lifecycle_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("factory_standard_historical_redundancy_cleanup_planning_only") is True)
    ok("summary.marking_only", summary.get("marking_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.standard_id", summary.get("standard_id") == STANDARD_ID)

    ok("upstream.lifecycle_go", lifecycle_vr.get("verifier") == "GO")
    ok("upstream.lifecycle_final", lifecycle_sm.get("final_decision") == LIFECYCLE_DR_FINAL)
    ok("upstream.lifecycle_next", lifecycle_sm.get("recommended_next_phase") == LIFECYCLE_DR_NEXT)
    ok("lifecycle_review.pass", lifecycle_review.get("review_pass") is True)

    ok("scope.count6", scope.get("scope_count") == len(CLEANUP_SCOPES))
    ok("scope.marking", scope.get("marking_only") is True)
    ok("scope.no_delete", scope.get("physical_delete_allowed") is False)

    ok("superseded.count", superseded.get("item_count") == len(MERGEABLE_OCR_AUTHORIZATION_PHASES) + 1)
    ok("superseded.merge9", len(superseded.get("items") or []) >= len(MERGEABLE_OCR_AUTHORIZATION_PHASES))
    for item in superseded.get("items") or []:
        if not _item_schema_ok(item):
            ok(f"superseded.schema.{item.get('object_id')}", False)
            break
    else:
        ok("superseded.schema_all", all(_item_schema_ok(i) for i in (superseded.get("items") or [])))

    ok("absorbed.nonempty", (absorbed.get("item_count") or 0) > 0)
    ok("absorbed.schema_all", all(_item_schema_ok(i) for i in (absorbed.get("items") or [])))
    ok("deprecated.nonempty", (deprecated.get("item_count") or 0) > 0)
    ok("deprecated.schema_all", all(_item_schema_ok(i) for i in (deprecated.get("items") or [])))

    ok("readonly.count7", read_only.get("item_count") == 7)
    ok("readonly.schema_all", all(_item_schema_ok(i) for i in (read_only.get("items") or [])))
    ok(
        "readonly.all_flag",
        all(i.get("read_only_evidence_source") is True for i in (read_only.get("items") or [])),
    )

    ok("no_delete.forbidden7", len(no_delete.get("forbidden_actions") or []) >= len(FORBIDDEN_ACTIONS))
    ok("no_delete.physical_false", no_delete.get("physical_delete_allowed") is False)
    ok("preservation.no_modify", preservation.get("evidence_chain_modified_now") is False)
    ok("preservation.no_destructive", preservation.get("phase_table_destructive_update_now") is False)
    ok("preservation.preserve_verifier", preservation.get("preserve_verifier_reports") is True)

    ok("future.rules6", len(future_ref.get("rules") or []) >= len(FUTURE_REFERENCE_RULES))
    ok("future.no_triple", future_ref.get("do_not_resume_formal_artifact_triple_chain") is True)
    ok("future.prefer_factory", future_ref.get("prefer_factory_standard") is True)
    ok("future.prefer_harness", future_ref.get("prefer_controlled_provider_readiness_harness") is True)

    ok("schema.fields", schema.get("field_count") == len(METADATA_SCHEMA_FIELDS))
    ok("schema.statuses", len(schema.get("allowed_statuses") or []) == len(MARKER_STATUSES))
    ok("schema.no_delete_default", schema.get("physical_delete_allowed_default") is False)

    ok("dryrun.merged", dryrun_plan.get("dryrun_and_review_merged") is True)
    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE_GO)
    ok("dryrun.no_delete", dryrun_plan.get("historical_file_delete_executed_now") is False)

    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.marking", decision.get("marking_only") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "check_count": len(checks),
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
