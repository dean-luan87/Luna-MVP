#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Capability Factory Authorization Standard Extension Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.capability_factory_authorization_standard_extension_planning_v1 import (
    AUTHORIZATION_STANDARD_ID,
    AUTHORIZATION_SUBCOMPONENTS,
    BOUNDARY_FALSE,
    FACTORY_AUTH_RESPONSIBILITIES,
    FINAL_DECISION_GO,
    NEXT_OCR_PHASE_AFTER_EXTENSION,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    PLANNING_DRYRUN_NEVER_AUTO_TRIGGER,
    SCOPE,
    TEN_STANDARDS,
)
from capabilities.governance.factory_standard_historical_redundancy_cleanup_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CLEANUP_DR_FINAL,
)
from capabilities.governance.ocr_authorization_next_route_decision_v1 import (
    FINAL_DECISION_GO as NEXT_ROUTE_FINAL,
)

MIN_CHECKS = 70

REQUIRED = (
    "factory_authorization_standard_extension_planning_policy_v1.json",
    "factory_standard_upstream_input_review_v1.json",
    "authorization_standard_contract_outline_v1.json",
    "authorization_scope_standard_plan_v1.json",
    "authorization_request_contract_standard_plan_v1.json",
    "authorization_grant_contract_standard_plan_v1.json",
    "authorization_execution_window_contract_standard_plan_v1.json",
    "authorization_action_matrix_standard_plan_v1.json",
    "authorization_owner_operator_approval_standard_plan_v1.json",
    "authorization_post_execution_review_standard_plan_v1.json",
    "authorization_revocation_rollback_standard_plan_v1.json",
    "authorization_standard_absorption_inventory_v1.json",
    "ocr_real_dependency_check_domain_config_template_v1.json",
    "ten_standards_contract_outline_v1.json",
    "route_adjustment_decision_v1.json",
    "authorization_standard_extension_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "authorization_standard_extension_planning_decision_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "capability_factory_authorization_standard_extension_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    upstream = _load(root / "factory_standard_upstream_input_review_v1.json")
    outline = _load(root / "authorization_standard_contract_outline_v1.json")
    scope = _load(root / "authorization_scope_standard_plan_v1.json")
    request = _load(root / "authorization_request_contract_standard_plan_v1.json")
    grant = _load(root / "authorization_grant_contract_standard_plan_v1.json")
    window = _load(root / "authorization_execution_window_contract_standard_plan_v1.json")
    matrix = _load(root / "authorization_action_matrix_standard_plan_v1.json")
    approval = _load(root / "authorization_owner_operator_approval_standard_plan_v1.json")
    post_review = _load(root / "authorization_post_execution_review_standard_plan_v1.json")
    rollback = _load(root / "authorization_revocation_rollback_standard_plan_v1.json")
    absorption = _load(root / "authorization_standard_absorption_inventory_v1.json")
    ocr_template = _load(root / "ocr_real_dependency_check_domain_config_template_v1.json")
    ten_outline = _load(root / "ten_standards_contract_outline_v1.json")
    route_adj = _load(root / "route_adjustment_decision_v1.json")
    dryrun = _load(root / "authorization_standard_extension_dryrun_plan_v1.json")
    decision = _load(root / "authorization_standard_extension_planning_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.ten", summary.get("ten_standard_count") == len(TEN_STANDARDS))
    ok("summary.route_adj", summary.get("route_adjustment_applied") is True)

    ok("upstream.pass", upstream.get("review_pass") is True)

    ok("outline.sub8", len(outline.get("subcomponents") or []) == len(AUTHORIZATION_SUBCOMPONENTS))
    ok("outline.resp6", len(outline.get("responsibilities") or []) == len(FACTORY_AUTH_RESPONSIBILITIES))
    ok("outline.std_id", outline.get("authorization_standard_id") == AUTHORIZATION_STANDARD_ID)

    ok("request.no_gen", request.get("request_generated_now") is False)
    ok("grant.not_issued", grant.get("grant_issued_now") is False)
    ok("window.not_open", window.get("current_window_opened_now") is False)
    ok("matrix.never_auto", len(matrix.get("planning_dryrun_never_auto_trigger") or []) >= len(PLANNING_DRYRUN_NEVER_AUTO_TRIGGER))
    ok("approval.not_now", approval.get("approval_collected_now") is False)
    ok("rollback.not_now", rollback.get("rollback_executed_now") is False)

    ok("absorption.superseded", absorption.get("ocr_auth_planning_superseded_for_auth_logic") is True)
    ok("absorption.preserved", absorption.get("ocr_auth_planning_preserved_as_evidence") is True)

    ok("ocr.domain", ocr_template.get("provider_domain") == "ocr")
    ok("ocr.target", ocr_template.get("authorization_target") == "real_dependency_check")
    ok("ocr.ref_std", ocr_template.get("references") == AUTHORIZATION_STANDARD_ID)
    ok("ocr.allowed5", len(ocr_template.get("allowed_checks") or []) == 5)
    ok("ocr.forbidden", "install" in (ocr_template.get("forbidden_actions") or []))

    ok("ten.count", len(ten_outline.get("ten_standards") or []) == 10)
    ok("ten.auth", ten_outline.get("tenth_standard") == "Authorization Standard")

    ok("route.superseded", route_adj.get("superseded_for_auth_logic_by") == AUTHORIZATION_STANDARD_ID)
    ok("route.no_delete", route_adj.get("physical_delete") is False)
    ok("route.next_ocr", route_adj.get("next_ocr_phase_after_extension") == NEXT_OCR_PHASE_AFTER_EXTENSION)

    ok("dryrun.merged", dryrun.get("dryrun_and_review_merged") is True)
    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)

    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.ten", decision.get("ten_standards_defined") is True)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))
    ok("cleanup.final", CLEANUP_DR_FINAL is not None)
    ok("route.final", NEXT_ROUTE_FINAL is not None)

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
