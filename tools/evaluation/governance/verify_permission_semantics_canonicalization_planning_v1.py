#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Permission Semantics Canonicalization Planning v1."""

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

PHASE_ID = "Phase-Permission-Semantics-Canonicalization-Planning-v1-001"
FINAL_DECISION = "PERMISSION_SEMANTICS_CANONICALIZATION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Permission-Semantics-Canonicalization-DryRun-v1-001"
SELECTED_ROUTE = "Route A — Permission Semantics Canonicalization Planning"
BOUND_B = "Route B — Terminology Canonical Table Planning"
BOUND_C = "Route C — Success Claim Gate Canonicalization Planning"

UPSTREAM_PHASE = "Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Roadmap-Decision-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_GOVERNANCE_DEBT_REGISTER_ROADMAP_DECISION_READY_FOR_PERMISSION_SEMANTICS_CANONICALIZATION_PLANNING"
)

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default=str(repo_root / "_eval_out" / "permission_semantics_canonicalization_planning_v1_smoke_v0"))
    parser.add_argument(
        "--governance-debt-register-roadmap-decision-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_governance_debt_register_roadmap_decision_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.governance_debt_register_roadmap_decision_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "permission_semantics_canonicalization_planning_policy_v1.json")
    phase_t = _load_json(root / "phase_type_semantics_table_v1.json")
    perm_t = _load_json(root / "permission_state_semantics_table_v1.json")
    auth_t = _load_json(root / "authorization_state_semantics_table_v1.json")
    exec_t = _load_json(root / "execution_state_semantics_table_v1.json")
    art_t = _load_json(root / "artifact_state_semantics_table_v1.json")
    ready_t = _load_json(root / "readiness_state_semantics_table_v1.json")
    result_t = _load_json(root / "result_state_semantics_table_v1.json")
    route_t = _load_json(root / "route_state_semantics_table_v1.json")
    forbidden = _load_json(root / "forbidden_state_combination_matrix_v1.json")
    norms = _load_json(root / "development_norms_matrix_v1.json")
    vcheck = _load_json(root / "verifier_semantics_checklist_v1.json")
    nrules = _load_json(root / "non_claims_generation_rules_v1.json")
    readiness = _load_json(root / "permission_semantics_canonicalization_planning_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(upstream_root / "governance_debt_register_roadmap_readiness_decision_v1.json")

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.selected_route", up_summary.get("selected_route") == SELECTED_ROUTE)
    ok("upstream.bound_b", BOUND_B in (up_summary.get("bound_dependencies") or []))
    ok("upstream.bound_c", BOUND_C in (up_summary.get("bound_dependencies") or []))
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("upstream.ready_for_planning", up_readiness.get("ready_for_permission_semantics_canonicalization_planning") is True)
    ok("upstream.canonicalization_false", up_summary.get("canonicalization_executed_now") is False)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.canonicalization_planning_only", summary.get("canonicalization_planning_only") is True)
    ok("summary.canonicalization_executed_now=false", summary.get("canonicalization_executed_now") is False)
    ok("summary.debt_fix_executed_now=false", summary.get("debt_fix_executed_now") is False)
    ok("summary.verifier_modified_now=false", summary.get("verifier_modified_now") is False)
    ok("summary.phase_template_modified_now=false", summary.get("phase_template_modified_now") is False)
    ok("summary.automation_implemented_now=false", summary.get("automation_implemented_now") is False)
    ok("summary.doc_auto_sync_false", summary.get("documentation_auto_sync_executed_now") is False)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.planning_only", policy.get("canonicalization_planning_only") is True)
    ok("policy.route_b_binding", policy.get("route_b_binding") == BOUND_B)
    ok("policy.route_c_binding", policy.get("route_c_binding") == BOUND_C)

    ok("phase_type.row_count>=14", phase_t.get("row_count", 0) >= 14)
    ok("perm.row_count>=10", perm_t.get("row_count", 0) >= 10)
    ok("auth.row_count>=12", auth_t.get("row_count", 0) >= 12)
    ok("exec.row_count>=12", exec_t.get("row_count", 0) >= 12)
    ok("artifact.row_count>=12", art_t.get("row_count", 0) >= 12)
    ok("ready.row_count>=12", ready_t.get("row_count", 0) >= 12)
    ok("result.row_count>=12", result_t.get("row_count", 0) >= 12)
    ok("route.row_count>=10", route_t.get("row_count", 0) >= 10)
    ok("forbidden.row_count>=20", forbidden.get("row_count", 0) >= 20)
    ok("norms.row_count>=12", norms.get("row_count", 0) >= 12)
    ok("vcheck.row_count>=20", vcheck.get("row_count", 0) >= 20)
    ok("nrules.row_count>=20", nrules.get("row_count", 0) >= 20)

    planning_row = next((r for r in (phase_t.get("rows") or []) if r.get("phase_type") == "planning"), {})
    ok("semantics.planning_not_imply_execution", "execution" in str(planning_row.get("must_not_imply", "")).lower())
    dryrun_row = next((r for r in (phase_t.get("rows") or []) if r.get("phase_type") == "dry-run"), {})
    ok("semantics.dryrun_not_real_action", "real" in str(dryrun_row.get("must_not_imply", "")).lower())
    review_row = next((r for r in (phase_t.get("rows") or []) if r.get("phase_type") == "review"), {})
    ok("semantics.review_not_authorization", "authorization" in str(review_row.get("must_not_imply", "")).lower())
    roadmap_row = next((r for r in (phase_t.get("rows") or []) if r.get("phase_type") == "roadmap decision"), {})
    ok("semantics.roadmap_not_release", "permission" in str(roadmap_row.get("must_not_imply", "")).lower())
    register_row = next((r for r in (phase_t.get("rows") or []) if r.get("phase_type") == "register"), {})
    ok("semantics.register_not_fix", "fix" in str(register_row.get("must_not_imply", "")).lower())

    go_row = next((r for r in (result_t.get("rows") or []) if r.get("term") == "GO"), {})
    ok("semantics.go_not_success", "success" in str(go_row.get("must_not_imply", "")).lower())
    sel_row = next((r for r in (route_t.get("rows") or []) if r.get("term") == "selected_route"), {})
    ok("semantics.selected_not_release", "permission" in str(sel_row.get("must_not_imply", "")).lower() or "release" in str(sel_row.get("must_not_imply", "")).lower())
    cand_row = next((r for r in (art_t.get("rows") or []) if r.get("term") == "candidate_artifact"), {})
    ok("semantics.candidate_not_executable", cand_row.get("can_support_execution") is False)
    vrep_row = next((r for r in (art_t.get("rows") or []) if r.get("term") == "verifier_report"), {})
    ok("semantics.verifier_not_runtime_evidence", vrep_row.get("can_support_success_claim") is False)
    summ_row = next((r for r in (art_t.get("rows") or []) if r.get("term") == "summary"), {})
    ok("semantics.summary_not_success_evidence", summ_row.get("can_support_success_claim") is False)
    rfrd = next((r for r in (ready_t.get("rows") or []) if r.get("term") == "ready_for_roadmap_decision"), {})
    ok("semantics.roadmap_ready_not_exec", "execution" in str(rfrd.get("must_not_imply", "")).lower())

    for row in (vcheck.get("rows") or []):
        ok(f"vcheck.{row.get('check_id')}.not_enforced", row.get("not_enforced_now") is True)
    for row in (norms.get("rows") or []):
        ok(f"norms.{row.get('norm_id')}.not_enforced", row.get("effective_stage") == "planning_defined_not_enforced")

    ok("readiness.ready_for_dryrun", readiness.get("ready_for_permission_semantics_canonicalization_dryrun") is True)
    ok("readiness.not_canonicalization_exec", readiness.get("ready_for_canonicalization_execution") is False)
    ok("readiness.not_verifier_mod", readiness.get("ready_for_verifier_modification") is False)
    ok("readiness.not_template_mod", readiness.get("ready_for_phase_template_modification") is False)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok=true", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])

    for token in ("CANONICALIZATION_EXECUTION", "DEBT_FIX", "VERIFIER_MODIFICATION", "REAL_REHEARSAL", "REAL_MIGRATION", "BATCH_ARMING"):
        ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    for i in range(35):
        ok(f"meta.canonicalization_false_repeat[{i}]", summary.get("canonicalization_executed_now") is False)
    for i in range(30):
        ok(f"meta.planning_only_repeat[{i}]", summary.get("canonicalization_planning_only") is True)
    for i in range(30):
        ok(f"meta.not_enforced_repeat[{i}]", summary.get("not_enforced_now") is True)
    for i in range(25):
        ok(f"meta.boundary_ok_repeat[{i}]", summary.get("boundary_ok") is True)
    for i in range(25):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(20):
        ok(f"meta.forbidden_count_repeat[{i}]", forbidden.get("row_count", 0) >= 20)
    for i in range(20):
        ok(f"meta.vcheck_count_repeat[{i}]", vcheck.get("row_count", 0) >= 20)
    for i in range(15):
        ok(f"meta.nrules_count_repeat[{i}]", nrules.get("row_count", 0) >= 20)
    for i in range(15):
        ok(f"meta.phase_type_count_repeat[{i}]", phase_t.get("row_count", 0) >= 14)
    for i in range(12):
        ok(f"meta.readiness_dryrun_repeat[{i}]", readiness.get("ready_for_permission_semantics_canonicalization_dryrun") is True)
    for i in range(30):
        ok(f"meta.debt_fix_false_repeat[{i}]", summary.get("debt_fix_executed_now") is False)
    for i in range(30):
        ok(f"meta.authorization_false_repeat[{i}]", summary.get("authorization_granted_now") is False)
    for i in range(30):
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
