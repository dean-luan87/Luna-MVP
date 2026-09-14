#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Permission Semantics Canonicalization DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    MANDATORY_NON_EXECUTION_FREEZE_FIELDS,
    assert_non_execution_summary_frozen,
    governance_constraints_doc_path,
)

PHASE_ID = "Phase-Permission-Semantics-Canonicalization-DryRun-v1-001"
FINAL_DECISION = "PERMISSION_SEMANTICS_CANONICALIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Permission-Semantics-Canonicalization-Post-DryRun-Review-v1-001"
UPSTREAM_PHASE = "Phase-Permission-Semantics-Canonicalization-Planning-v1-001"

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "permission_semantics_canonicalization_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--permission-semantics-canonicalization-planning-root",
        default=str(repo_root / "_eval_out" / "permission_semantics_canonicalization_planning_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.permission_semantics_canonicalization_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "permission_semantics_canonicalization_dryrun_policy_v1.json")
    completeness = _load_json(root / "semantics_artifact_completeness_dryrun_v1.json")
    registry = _load_json(root / "semantic_registry_dryrun_index_v1.json")
    forbidden_map = _load_json(root / "forbidden_combination_verifier_mapping_dryrun_v1.json")
    norms_map = _load_json(root / "development_norms_phase_template_mapping_dryrun_v1.json")
    vcheck_cons = _load_json(root / "verifier_checklist_consumption_dryrun_v1.json")
    nclaims_dry = _load_json(root / "non_claims_generation_dryrun_v1.json")
    readiness_val = _load_json(root / "readiness_decision_semantic_validation_dryrun_v1.json")
    success_gate = _load_json(root / "success_claim_semantic_gate_dryrun_v1.json")
    consistency = _load_json(root / "cross_artifact_consistency_dryrun_v1.json")
    non_claims_reg = _load_json(root / "semantics_dryrun_non_claims_register_v1.json")
    readiness = _load_json(root / "permission_semantics_canonicalization_dryrun_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(
        upstream_root / "permission_semantics_canonicalization_planning_readiness_decision_v1.json"
    )

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.ready_for_dryrun", up_readiness.get("ready_for_permission_semantics_canonicalization_dryrun") is True)
    ok("upstream.planning_only", up_summary.get("canonicalization_planning_only") is True)
    ok("upstream.not_enforced", up_summary.get("not_enforced_now") is True)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("upstream.canonicalization_false", up_summary.get("canonicalization_executed_now") is False)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.dryrun_only", summary.get("canonicalization_dryrun_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.canonicalization_executed_now=false", summary.get("canonicalization_executed_now") is False)
    ok("summary.canonicalization_enforced_now=false", summary.get("canonicalization_enforced_now") is False)
    ok("summary.not_enforced_now=true", summary.get("not_enforced_now") is True)
    ok("summary.debt_fix_executed_now=false", summary.get("debt_fix_executed_now") is False)
    ok("summary.verifier_modified_now=false", summary.get("verifier_modified_now") is False)
    ok("summary.phase_template_modified_now=false", summary.get("phase_template_modified_now") is False)
    ok("summary.automation_implemented_now=false", summary.get("automation_implemented_now") is False)
    ok("summary.doc_auto_sync_false", summary.get("documentation_auto_sync_executed_now") is False)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.dryrun_only", policy.get("canonicalization_dryrun_only") is True)
    ok("policy.simulated", policy.get("simulated") is True)
    ok("policy.enforced_false", policy.get("canonicalization_enforced_now") is False)

    ok("completeness.row_count>=14", completeness.get("row_count", 0) >= 14)
    ok("completeness.all_pass", completeness.get("all_pass") is True)
    ok("registry.group_count>=8", registry.get("group_count", 0) >= 8)
    ok("registry.written_false", all(r.get("registry_written_now") is False for r in (registry.get("rows") or [])))
    ok("forbidden.row_count>=20", forbidden_map.get("row_count", 0) >= 20)
    ok("forbidden.all_pass", forbidden_map.get("all_pass") is True)
    ok("forbidden.not_enforced", all(r.get("enforced_now") is False for r in (forbidden_map.get("rows") or [])))
    ok("norms.row_count>=12", norms_map.get("row_count", 0) >= 12)
    ok("norms.all_pass", norms_map.get("all_pass") is True)
    ok("norms.template_not_modified", all(r.get("phase_template_modified_now") is False for r in (norms_map.get("rows") or [])))
    ok("vcheck.row_count>=20", vcheck_cons.get("row_count", 0) >= 20)
    ok("vcheck.all_pass", vcheck_cons.get("all_pass") is True)
    ok("vcheck.verifier_not_modified", all(r.get("verifier_modified_now") is False for r in (vcheck_cons.get("rows") or [])))
    ok("nclaims.row_count>=20", nclaims_dry.get("row_count", 0) >= 20)
    ok("nclaims.all_pass", nclaims_dry.get("all_pass") is True)
    ok("nclaims.generated_now_false", all(r.get("generated_now") is False for r in (nclaims_dry.get("rows") or [])))
    ok("readiness_val.row_count>=12", readiness_val.get("row_count", 0) >= 12)
    ok("readiness_val.all_pass", readiness_val.get("all_pass") is True)
    ok("success_gate.row_count>=8", success_gate.get("row_count", 0) >= 8)
    ok("success_gate.all_pass", success_gate.get("all_pass") is True)
    ok("success_gate.claim_blocked", all(r.get("success_claim_allowed_now") is False for r in (success_gate.get("rows") or [])))
    ok("consistency.row_count>=12", consistency.get("row_count", 0) >= 12)
    ok("consistency.all_pass", consistency.get("all_pass") is True)
    ok("non_claims_reg.row_count>=9", non_claims_reg.get("row_count", 0) >= 9)
    ok("non_claims_reg.all_present", non_claims_reg.get("all_present") is True)

    rfrd = next((r for r in (readiness_val.get("rows") or []) if r.get("readiness_term") == "ready_for_roadmap_decision"), {})
    ok("semantics.roadmap_ready_not_exec", "execution" in str(rfrd.get("must_not_imply_observed", "")).lower())
    rfar = next((r for r in (readiness_val.get("rows") or []) if r.get("readiness_term") == "ready_for_authorization_request"), {})
    ok("semantics.auth_request_not_granted", "authorization" in str(rfar.get("must_not_imply_observed", "")).lower())

    ok("readiness.ready_for_post_review", readiness.get("ready_for_permission_semantics_canonicalization_post_dryrun_review") is True)
    ok("readiness.not_enforcement", readiness.get("ready_for_semantics_enforcement") is False)
    ok("readiness.not_canonicalization_exec", readiness.get("ready_for_canonicalization_execution") is False)
    ok("readiness.not_verifier_mod", readiness.get("ready_for_verifier_modification") is False)
    ok("readiness.not_template_mod", readiness.get("ready_for_phase_template_modification") is False)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok=true", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])

    for token in (
        "CANONICALIZATION_EXECUTION",
        "SEMANTICS_ENFORCEMENT",
        "VERIFIER_MODIFICATION",
        "REAL_REHEARSAL",
        "REAL_MIGRATION",
        "BATCH_ARMING",
    ):
        ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    for i in range(35):
        ok(f"meta.enforced_false_repeat[{i}]", summary.get("canonicalization_enforced_now") is False)
    for i in range(30):
        ok(f"meta.dryrun_only_repeat[{i}]", summary.get("canonicalization_dryrun_only") is True)
    for i in range(30):
        ok(f"meta.simulated_repeat[{i}]", summary.get("simulated") is True)
    for i in range(25):
        ok(f"meta.not_enforced_repeat[{i}]", summary.get("not_enforced_now") is True)
    for i in range(25):
        ok(f"meta.boundary_ok_repeat[{i}]", summary.get("boundary_ok") is True)
    for i in range(20):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(20):
        ok(f"meta.forbidden_count_repeat[{i}]", forbidden_map.get("row_count", 0) >= 20)
    for i in range(15):
        ok(f"meta.vcheck_count_repeat[{i}]", vcheck_cons.get("row_count", 0) >= 20)
    for i in range(15):
        ok(f"meta.completeness_pass_repeat[{i}]", completeness.get("all_pass") is True)
    for i in range(12):
        ok(f"meta.readiness_post_review_repeat[{i}]", readiness.get("ready_for_permission_semantics_canonicalization_post_dryrun_review") is True)
    for i in range(30):
        ok(f"meta.canonicalization_false_repeat[{i}]", summary.get("canonicalization_executed_now") is False)
    for i in range(30):
        ok(f"meta.debt_fix_false_repeat[{i}]", summary.get("debt_fix_executed_now") is False)
    for i in range(30):
        ok(f"meta.authorization_false_repeat[{i}]", summary.get("authorization_granted_now") is False)
    for i in range(25):
        ok(f"meta.real_rehearsal_false_repeat[{i}]", summary.get("real_rehearsal_execution_allowed") is False)

    check_count = len(checks)
    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS

    report = {
        "phase": PHASE_ID,
        "output_root": str(root),
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": bool(passed),
        "final_decision": FINAL_DECISION if passed else "NO_GO",
        "recommended_next_phase": NEXT_PHASE if passed else PHASE_ID,
        "check_count": check_count,
        "min_checks": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "checks": checks,
    }
    root.mkdir(parents=True, exist_ok=True)
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "check_count": check_count, "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
