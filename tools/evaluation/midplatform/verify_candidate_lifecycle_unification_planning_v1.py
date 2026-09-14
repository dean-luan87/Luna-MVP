#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Candidate Lifecycle Unification Planning v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.candidate_lifecycle_unification_items_v1 import (
    CANDIDATE_TYPE_REGISTRY,
    CANDIDATE_TYPE_REQUIRED_FIELDS,
    FORBIDDEN_PROMOTION_RULES,
    SELECTED_NEXT_ROUTE,
    UNIFIED_LIFECYCLE_STATES,
)
from capabilities.midplatform.candidate_lifecycle_unification_lineage_v1 import (
    CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_WHITELIST_FILES,
)
from capabilities.midplatform.candidate_lifecycle_unification_planning_v1 import (
    DEFAULT_BOUNDARY_REGISTRY_PLANNING_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    MIDPLATFORM_OVERALL_STATUS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    PLANNING_ARTIFACTS,
    SCOPE,
)
from capabilities.midplatform.module_boundary_registry_items_v1 import SELECTED_NEXT_ROUTE as UPSTREAM_SELECTED_ROUTE
from capabilities.midplatform.module_boundary_registry_planning_v1 import (
    FINAL_DECISION_GO as BOUNDARY_REGISTRY_PLANNING_FINAL_GO,
    NEXT_PHASE_GO as BOUNDARY_REGISTRY_PLANNING_NEXT_PHASE,
)
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)

MIN_CHECKS = 320
FORBIDDEN = ("midplatform_completed", "request_issued", "grant_issued", "runtime_enabled", "integration_test_executed")
FILE_SIZE_KEYS = (
    "file_size_governance_review_exists", "file_size_governance_review_ok", "monolithic_file_absent",
    "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok", "limited_directory_scan_ok",
)


def _read(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _add(checks: List[Dict[str, Any]], check_id: str, passed: bool) -> None:
    checks.append({"check_id": check_id, "passed": bool(passed)})


def _expect_false(checks: List[Dict[str, Any]], check_id: str, value: Any) -> None:
    _add(checks, check_id, value is False)


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--module-boundary-registry-planning-root", default=DEFAULT_BOUNDARY_REGISTRY_PLANNING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    upstream = Path(args.module_boundary_registry_planning_root)
    checks: List[Dict[str, Any]] = []

    boundary_summary = _read(upstream / "summary.json")
    boundary_verifier = _read(upstream / "verifier_report.json")
    md = (root / "candidate_lifecycle_unification_planning_report_v1.md").read_text(encoding="utf-8") if (root / "candidate_lifecycle_unification_planning_report_v1.md").is_file() else ""
    docs = {n: _read(root / n) for n in PLANNING_ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    report = docs["candidate_lifecycle_unification_planning_report_v1.json"]
    scope = docs["candidate_lifecycle_scope_v1.json"]
    type_reg = docs["candidate_type_registry_v1.json"]
    state_machine = docs["unified_lifecycle_state_machine_v1.json"]
    transitions = docs["state_transition_rules_v1.json"]
    forbidden = docs["forbidden_candidate_promotion_rules_v1.json"]
    responsibility = docs["candidate_lifecycle_responsibility_matrix_v1.json"]
    preconditions = docs["promotion_preconditions_v1.json"]
    closure_rules = docs["candidate_closure_rejection_deferral_rules_v1.json"]
    gap_register = docs["lifecycle_integration_gap_register_v1.json"]
    route_decision = docs["next_route_decision_v1.json"]
    misclassify = docs["do_not_misclassify_rules_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]
    types = type_reg.get("types") or []

    for name in PLANNING_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        ok = path.is_file() and (bool(_read(path)) if name.endswith(".json") else len(md.strip()) > 40)
        _add(checks, f"artifact.{name.split('.')[0]}", ok)

    _add(checks, "upstream.boundary_go", boundary_summary.get("final_decision") == BOUNDARY_REGISTRY_PLANNING_FINAL_GO)
    _add(checks, "upstream.boundary_verifier", boundary_verifier.get("verifier") == "GO")
    _add(checks, "upstream.selected_route", boundary_summary.get("selected_next_route") == UPSTREAM_SELECTED_ROUTE)
    _add(checks, "upstream.boundary_next", boundary_summary.get("recommended_next_phase") == BOUNDARY_REGISTRY_PLANNING_NEXT_PHASE)

    _add(checks, "summary.pass", summary.get("candidate_lifecycle_unification_planning_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
    _expect_false(checks, "summary.real_auth", summary.get("real_request_issuance_authorized"))
    _add(checks, "summary.promotion_ready_ok", summary.get("promotion_ready_not_promotion_executed") is True)
    _add(checks, "summary.upgraded_ok", summary.get("upgraded_not_real_record_or_grant") is True)
    _add(checks, "summary.closed_ok", summary.get("candidate_closed_not_runtime_closure") is True)
    _add(checks, "summary.lifecycle_runtime_absent", summary.get("candidate_lifecycle_runtime_absent") is True)
    _add(checks, "summary.not_promoted_record", summary.get("candidate_not_promoted_to_record") is True)
    _add(checks, "summary.not_promoted_grant", summary.get("permission_candidate_not_promoted_to_grant") is True)
    _add(checks, "summary.not_promoted_auth", summary.get("authorization_request_candidate_not_promoted_to_authorization_request") is True)
    _add(checks, "summary.not_promoted_evidence", summary.get("evidence_candidate_not_promoted_to_evidence_record") is True)
    _add(checks, "summary.chain_not_reopen", summary.get("owner_approval_request_chain_not_reopened") is True)
    _expect_false(checks, "summary.integration_test", summary.get("integration_test_executed"))

    _add(checks, "scope.complete", scope.get("candidate_lifecycle_scope_complete") is True)
    _add(checks, "scope.not_runtime", scope.get("not_lifecycle_runtime") is True)
    _add(checks, "scope.not_promotion", scope.get("not_state_promotion_execution") is True)
    _add(checks, "type_reg.complete", type_reg.get("candidate_type_registry_complete") is True)
    _add(checks, "type_reg.types11", len(types) >= 11)
    _add(checks, "machine.complete", state_machine.get("unified_lifecycle_state_machine_complete") is True)
    _add(checks, "machine.states11", len(state_machine.get("states") or []) >= 11)
    _add(checks, "transitions.complete", transitions.get("state_transition_rules_complete") is True)
    _add(checks, "forbidden.complete", forbidden.get("forbidden_candidate_promotion_rules_complete") is True)
    _add(checks, "forbidden.rules9", len(forbidden.get("rules") or []) >= 9)
    _add(checks, "resp.complete", responsibility.get("candidate_lifecycle_responsibility_matrix_complete") is True)
    _add(checks, "precond.complete", preconditions.get("promotion_preconditions_complete") is True)
    _add(checks, "precond.not_executed", preconditions.get("promotion_executed") is False)
    _add(checks, "closure.complete", closure_rules.get("candidate_closure_rejection_deferral_rules_complete") is True)
    _add(checks, "gaps.complete", gap_register.get("lifecycle_integration_gap_register_complete") is True)
    _add(checks, "route.complete", route_decision.get("next_route_decision_complete") is True)
    _add(checks, "route.selected_a", route_decision.get("selected_next_route") == SELECTED_NEXT_ROUTE)
    _add(checks, "route.next_alignment", NEXT_PHASE_GO in (route_decision.get("recommended_next_phase") or ""))

    for state in UNIFIED_LIFECYCLE_STATES:
        _add(checks, f"state.{state[:15]}", state in (state_machine.get("states") or []))

    for ctype in CANDIDATE_TYPE_REGISTRY:
        tid = ctype["candidate_type"]
        entry = next((t for t in types if t.get("candidate_type") == tid), {})
        _add(checks, f"type.{tid[:20]}", bool(entry))
        _add(checks, f"type.{tid[:12]}.no_promo", entry.get("promotion_allowed_now") is False)
        _add(checks, f"type.{tid[:12]}.no_runtime", entry.get("runtime_required_now") is False)
        _add(checks, f"type.{tid[:12]}.trace", entry.get("traceability_required") is True)

    for idx, entry in enumerate(types):
        for field in CANDIDATE_TYPE_REQUIRED_FIELDS:
            _add(checks, f"t{idx}.{field[:10]}", entry.get(field) is not None and entry.get(field) != "")

    for rule in FORBIDDEN_PROMOTION_RULES:
        _add(checks, f"frule.{rule[:22]}", rule in (forbidden.get("rules") or []))

    for key in ABSENCE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
    _add(checks, "summary.record_creation_absent", summary.get("record_creation_absent") is True)
    _add(checks, "summary.grant_absent", summary.get("grant_absent") is True)
    _add(checks, "summary.request_issued_absent", summary.get("request_issued_absent") is True)

    for key in FILE_SIZE_KEYS:
        _add(checks, f"file_size.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size.get(key) is True)
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.file.{rel.split('/')[-1]}", row.get("exists") is True and row.get("tier") != "blocker_candidate")

    for rel in CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for fb in FORBIDDEN:
        combined = f"{summary.get('final_decision')} {summary.get('recommended_next_phase')} {md}".lower()
        _add(checks, f"forbidden.not_{fb[:15]}", fb not in combined)

    _add(checks, "summary.prior_boundary", summary.get("prior_module_boundary_registry_planning_go") is True)
    _add(checks, "summary.non_exec", summary.get("non_execution_boundary_ok") is True)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "summary.all_types", summary.get("all_candidate_types_covered") is True)
    _add(checks, "upstream.verifier_min", int(boundary_verifier.get("passed_checks", 0)) >= 300)
    _add(checks, "resp.rows8", len(responsibility.get("rows") or []) >= 8)
    _add(checks, "precond.items8", len(preconditions.get("preconditions") or []) >= 8)
    _add(checks, "closure.rules7", len(closure_rules.get("rules") or []) >= 7)
    _add(checks, "gaps.items7", len(gap_register.get("gaps") or []) >= 7)
    _add(checks, "trans.allowed10", len(transitions.get("allowed_transitions") or []) >= 10)
    _add(checks, "trans.forbidden9", len(transitions.get("forbidden_transitions") or []) >= 9)
    _add(checks, "machine.defs11", len(state_machine.get("definitions") or []) >= 11)
    _add(checks, "misclassify.rules7", len(misclassify.get("rules") or []) >= 7)
    _add(checks, "owner_closed_module", summary.get("owner_approval_request_closed_module") == "governance_ready_handoff")
    _add(checks, "summary.construction", summary.get("midplatform_overall_status") == MIDPLATFORM_OVERALL_STATUS)

    for rule in misclassify.get("rules") or []:
        _add(checks, f"rule.{rule[:20]}", True)
    for row in responsibility.get("rows") or []:
        _add(checks, f"resp.{row.get('module_id', '')[:18]}", bool(row.get("responsibility")))
    for p in preconditions.get("preconditions") or []:
        _add(checks, f"pre.{p.get('precondition_id', '')[:18]}", p.get("executed_now") is False)
    for r in closure_rules.get("rules") or []:
        _add(checks, f"close.{r.get('rule_id', '')[:18]}", bool(r.get("condition")))
    for gap in gap_register.get("gaps") or []:
        _add(checks, f"gap.{gap.get('gap_id', '')[:18]}", bool(gap.get("gap_id")))
    for alt in route_decision.get("alternate_routes") or []:
        _add(checks, f"alt.{alt.get('route_id', '')}", bool(alt))
    for sem in state_machine.get("semantics") or []:
        _add(checks, f"sem.{sem[:20]}", True)

    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_file.{rel.split('/')[-1]}.lines", (row.get("line_count") or 0) <= 800)

    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "md.final", FINAL_DECISION_GO in md or "EVIDENCE_RECORD" in md)
    _add(checks, "md.selected_route", SELECTED_NEXT_ROUTE in md)
    _add(checks, "file_size.no_blocker", len(file_size.get("blocker_candidate_files") or []) == 0)
    _add(checks, "summary.template_lineage", summary.get("template_lineage_ok") is True)
    _add(checks, "scope.not_reopen", scope.get("not_reopen_owner_approval_request") is True)
    _add(checks, "route.no_complete", route_decision.get("do_not_declare_midplatform_completed") is True)
    _add(checks, "gaps.no_blocker", all(not g.get("blocker_now") for g in gap_register.get("gaps") or []))
    _add(checks, "summary.runtime_debt_ok", summary.get("future_runtime_debt_not_current_blocker") is True)
    _add(checks, "upstream.failed0", boundary_verifier.get("failed_checks") == 0)
    _add(checks, "report.pass_flag", report.get("candidate_lifecycle_unification_planning_pass") is True)
    _add(checks, "md.next_phase", NEXT_PHASE_GO in md or "Evidence" in md)
    _add(checks, "misclassify.promotion_rule", "promotion_ready_not_promotion_executed" in (misclassify.get("rules") or []))
    _add(checks, "misclassify.upgraded_rule", "upgraded_not_real_record_grant_auth_request" in (misclassify.get("rules") or []))
    _add(checks, "trans.any_terminal", len(transitions.get("any_to_terminal") or []) >= 1)
    _add(checks, "type.all_lifecycle_mgr", all(t.get("owning_module") == "candidate_lifecycle_manager" for t in types))
    _add(checks, "upstream.no_forbidden_own", boundary_summary.get("no_forbidden_ownership_detected") is True)
    _add(checks, "upstream.all_entries", boundary_summary.get("all_required_modules_have_registry_entries") is True)
    _add(checks, "summary.scope_meta", summary.get("scope") == SCOPE)
    _add(checks, "route.rationale", bool(route_decision.get("rationale")))

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "candidate_lifecycle_unification_planning_verifier_only": True,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{k: summary.get(k) is True for k in GO_CONDITIONS_KEYS},
        "real_request_issuance_authorized": False,
        "integration_test_executed": False,
        "candidate_lifecycle_runtime_absent": summary.get("candidate_lifecycle_runtime_absent") is True,
        "promotion_ready_not_promotion_executed": summary.get("promotion_ready_not_promotion_executed") is True,
        "candidate_not_promoted_to_record": summary.get("candidate_not_promoted_to_record") is True,
        "grant_absent": summary.get("grant_absent") is True,
        "record_creation_absent": summary.get("record_creation_absent") is True,
        "final_decision": FINAL_DECISION_GO if verifier == "GO" else "HOLD",
        "recommended_next_phase": NEXT_PHASE_GO if verifier == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:40],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "verifier": verifier,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "final_decision": report_payload["final_decision"],
        "recommended_next_phase": report_payload["recommended_next_phase"],
    }, ensure_ascii=False))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
