#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision Module Model Profile + Governance Binding DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.vision_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    QUALIFICATION_FIELDS,
    QUALIFICATION_MODE,
    SCOPE,
)
from capabilities.governance.vision_module_model_profile_governance_binding_planning_v1 import (
    CLOSURE_CANNOT_SAY,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    QUALIFICATION_CHECK_CRITERIA,
)

MIN_CHECKS = 79

REQUIRED = (
    "vision_module_model_profile_governance_binding_dryrun_review_policy_v1.json",
    "planning_input_review_v1.json",
    "vision_module_model_profile_governance_binding_candidate_v1.json",
    "vision_module_registry_qualification_review_v1.json",
    "vision_module_local_standard_qualification_review_v1.json",
    "vision_midplatform_binding_qualification_review_v1.json",
    "vision_self_check_qualification_review_v1.json",
    "vision_interaction_check_qualification_review_v1.json",
    "vision_candidate_only_qualification_review_v1.json",
    "vision_no_bypass_qualification_review_v1.json",
    "vision_health_supervision_refs_qualification_review_v1.json",
    "vision_module_qualification_check_v1.json",
    "vision_module_qualification_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
    "non_claims_register_v1.json",
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
            "vision_module_model_profile_governance_binding_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "vision_module_model_profile_governance_binding_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(Path(args.planning_root) / "verifier_report.json")
    plan_sm = _load(Path(args.planning_root) / "summary.json")
    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == PLANNING_FINAL_GO)

    summary = _load(root / "summary.json")
    qual = _load(root / "vision_module_qualification_check_v1.json")
    closure = _load(root / "vision_module_qualification_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.qual_mode", summary.get("qualification_mode") == QUALIFICATION_MODE)
    ok("summary.qual_only", summary.get("qualification_check_only") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    for review in (
        "vision_module_registry_qualification_review_v1.json",
        "vision_module_local_standard_qualification_review_v1.json",
        "vision_midplatform_binding_qualification_review_v1.json",
        "vision_self_check_qualification_review_v1.json",
        "vision_interaction_check_qualification_review_v1.json",
        "vision_candidate_only_qualification_review_v1.json",
        "vision_no_bypass_qualification_review_v1.json",
        "vision_health_supervision_refs_qualification_review_v1.json",
    ):
        ok(f"review.{review[:24]}", _load(root / review).get("review_pass") is True)

    ok("qual.pass", qual.get("qualification_pass") is True)
    ok("qual.criteria8", qual.get("criteria_count") == len(QUALIFICATION_CHECK_CRITERIA) if qual.get("criteria_count") else len(qual.get("criteria") or []) == 8)
    for k, v in QUALIFICATION_FIELDS.items():
        ok(f"qual.{k[:18]}", (qual.get("qualification_fields") or {}).get(k) is v)

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.qual_mode", closure.get("qualification_mode") == QUALIFICATION_MODE)
    ok("closure.cannot_integrated", "module fully integrated with Constitution" in str(closure.get("closure_cannot_say")))

    ok("next.ocr", next_route.get("ready_for_ocr_module_model_profile_governance_binding_planning") is True)
    ok("next.phase", next_route.get("selected_next_phase") == NEXT_PHASE_GO)

    for claim in NON_CLAIMS:
        ok(f"non_claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("non_claims") or []))

    total = len(checks)
    passed = sum(1 for c in checks if c["passed"])
    min_checks = MIN_CHECKS if MIN_CHECKS else total
    verifier = "GO" if passed == total and passed >= min_checks else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verifier": verifier,
        "checks_passed": passed,
        "checks_total": total,
        "min_checks": min_checks,
        "dryrun_and_review_pass": summary.get("dryrun_and_review_pass"),
        "qualification_mode": QUALIFICATION_MODE,
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": verifier, "checks_passed": passed, "checks_total": total}))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
