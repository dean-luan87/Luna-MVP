#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Owner Approval Request Governance Gate Integrated Implementation v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.migration_governance_development_constraints_v1 import (
    TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_REF,
)
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import (
    FILE_SIZE_GOVERNANCE_REVIEW_KEYS,
)
from capabilities.midplatform.owner_approval_request_governance_gate_template_lineage_v1 import (
    OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1 import (
    FINAL_DECISION_GO as FINAL_GATE_PLANNING_FINAL_GO,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1 import (
    CORE_CANDIDATE_IDS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
)
from capabilities.midplatform.task_manager_owner_approval_request_governance_gate_integrated_implementation_v1 import (
    ABSENCE_KEYS,
    DEFAULT_FINAL_GATE_PLANNING_ROOT,
    DEFAULT_OUTPUT,
    DEFAULT_POST_REVIEW_ROOT,
    FINAL_DECISION_GO,
    FUNCTIONAL_SLICE_CHAINS,
    GO_CONDITIONS_KEYS,
    INTEGRATED_ARTIFACTS,
    NEXT_PHASE_A,
    NEXT_PHASE_B,
    NEXT_PHASE_C,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
    SELECTED_ROUTE,
)

MIN_CHECKS = 300
FORBIDDEN: Tuple[str, ...] = (
    "request_issued",
    "request_record_created",
    "approval_record_created",
    "grant_issued",
    "foundation_frozen",
    "closure_executed",
    "module_adapter_implementation",
)
FILE_SIZE_KEYS: Tuple[str, ...] = (
    "file_size_governance_review_exists",
    "file_size_governance_review_ok",
    "monolithic_file_absent",
    "full_repo_scan_absent",
    "tmp_eval_out_scan_absent",
    "summary_index_first_reading_ok",
    "limited_directory_scan_ok",
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
    parser.add_argument("--post-review-root", default=DEFAULT_POST_REVIEW_ROOT)
    parser.add_argument("--final-gate-planning-root", default=DEFAULT_FINAL_GATE_PLANNING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    post = Path(args.post_review_root)
    gate = Path(args.final_gate_planning_root)
    checks: List[Dict[str, Any]] = []

    post_summary = _read(post / "summary.json")
    post_verifier = _read(post / "verifier_report.json")
    gate_summary = _read(gate / "summary.json")
    gate_verifier = _read(gate / "verifier_report.json")

    md = (root / "task_manager_owner_approval_request_governance_gate_integrated_plan_v1.md").read_text(encoding="utf-8") if (root / "task_manager_owner_approval_request_governance_gate_integrated_plan_v1.md").is_file() else ""
    docs = {n: _read(root / n) for n in INTEGRATED_ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]

    for name in INTEGRATED_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        _add(checks, f"artifact.{name.split('.')[0]}", path.is_file() and (bool(_read(path)) if name.endswith(".json") else len(md.strip()) > 80))

    _add(checks, "upstream.post_go", post_summary.get("final_decision") == POST_REVIEW_FINAL_GO)
    _add(checks, "upstream.post_verifier", post_verifier.get("verifier") == "GO")
    _add(checks, "upstream.post_pass", post_summary.get("post_review_pass") is True)
    _add(checks, "upstream.closure_accepted", summary.get("closure_result_accepted") is True)
    _add(checks, "upstream.direct_linked", summary.get("direct_upstream_ref_linked") is True)
    _add(checks, "upstream.gate_declared", bool(gate_summary.get("final_decision")))
    _add(checks, "downstream.gate_readiness", "final_gate_planning_not_go" in (summary.get("downstream_readiness_gaps") or []) or gate_summary.get("final_decision") == FINAL_GATE_PLANNING_FINAL_GO)

    plan = docs["task_manager_owner_approval_request_governance_gate_integrated_plan_v1.json"]
    roadmap = docs["integrated_roadmap_decision_v1.json"]
    auth_prep = docs["issuance_authorization_preparation_package_v1.json"]
    routing = docs["missing_conditions_routing_v1.json"]
    checklist = docs["real_issuance_precondition_checklist_v1.json"]
    closure = docs["record_approval_ack_evidence_closure_boundary_v1.json"]
    slice_plan = docs["module_level_functional_slice_test_plan_v1.json"]
    governance = docs["governance_rule_reference_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]

    _add(checks, "summary.pass", summary.get("integrated_implementation_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "summary.route", summary.get("selected_route") == SELECTED_ROUTE)
    _add(checks, "summary.no_fragmentary", summary.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "summary.no_indep_roadmap", summary.get("no_independent_roadmap_verifier") is True)
    _add(checks, "summary.no_indep_auth", summary.get("no_independent_authorization_planning_phase") is True)

    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _expect_false(checks, "summary.no_real_auth", summary.get("real_request_issuance_authorized"))
    _add(checks, "summary.prior_post", summary.get("prior_post_review_go") is True)
    gate_readiness_gap = "final_gate_planning_not_go" in (summary.get("downstream_readiness_gaps") or [])
    _add(
        checks,
        "summary.prior_gate",
        summary.get("prior_final_gate_planning_go") is True or gate_readiness_gap,
    )

    _add(checks, "roadmap.complete", roadmap.get("integrated_roadmap_decision_complete") is True)
    _add(checks, "roadmap.route", roadmap.get("selected_route") == SELECTED_ROUTE)
    _expect_false(checks, "roadmap.no_exec", roadmap.get("executes_real_issuance"))

    _add(checks, "auth_prep.complete", auth_prep.get("issuance_authorization_preparation_package_complete") is True)
    _add(checks, "auth_prep.package_candidate", auth_prep.get("authorization_package_candidate") is True)
    _add(checks, "auth_prep.precond_candidate", auth_prep.get("authorization_precondition_candidate") is True)
    _expect_false(checks, "auth_prep.no_real_auth", auth_prep.get("executes_real_authorization"))
    _add(checks, "auth_prep.auth_req_absent", auth_prep.get("authorization_request_absent") is True)

    routes = {r.get("condition_id"): r for r in routing.get("routes") or []}
    _add(checks, "routing.complete", routing.get("missing_conditions_routing_complete") is True)
    _add(checks, "routing.real.blocker", routes.get("real_request_issuance", {}).get("routing_bucket") == "blocker_before_real_issuance")
    _add(checks, "routing.runtime.debt", routes.get("runtime_adapter_implementation", {}).get("routing_bucket") == "future_runtime_debt")
    _add(checks, "routing.whitebox.debt", routes.get("whitebox_runtime_integration", {}).get("routing_bucket") == "future_runtime_debt")
    _add(checks, "routing.slice.follow", routes.get("module_level_functional_slice_tests", {}).get("routing_bucket") == "non_blocking_follow_up")
    _add(checks, "routing.gov.debt", routes.get("governance_debt_closure", {}).get("routing_bucket") == "governance_debt")
    _add(checks, "routing.chain.resolved", routes.get("record_approval_closure_candidate_chain", {}).get("routing_bucket") == "resolved")

    _add(checks, "checklist.complete", checklist.get("real_issuance_precondition_checklist_complete") is True)
    _add(checks, "checklist.items", len(checklist.get("items") or []) >= 6)
    _expect_false(checks, "checklist.no_real_auth", checklist.get("real_request_issuance_authorized"))

    _add(checks, "closure.complete", closure.get("record_approval_ack_evidence_boundary_complete") is True)
    for cid in CORE_CANDIDATE_IDS:
        row = next((r for r in closure.get("rows") or [] if r.get("candidate_id") == cid), {})
        _add(checks, f"closure.{cid[:20]}", row.get("still_candidate") is True and row.get("record_created") is False)

    _add(checks, "slice.complete", slice_plan.get("module_level_functional_slice_test_plan_complete") is True)
    _add(checks, "slice.chains", len(slice_plan.get("chains") or []) == len(FUNCTIONAL_SLICE_CHAINS))
    for chain in FUNCTIONAL_SLICE_CHAINS:
        row = next((c for c in slice_plan.get("chains") or [] if c.get("chain_id") == chain), {})
        _add(checks, f"slice.{chain[:25]}", row.get("executed") is False)

    _add(checks, "gov.top_level", governance.get("top_level_objective_priority_rule_ref_ok") is True)
    _add(checks, "gov.module_first", governance.get("module_first_cadence_rule_ref_ok") is True)
    _add(checks, "gov.reuse", governance.get("reuse_first_rule_ref_ok") is True)
    _add(checks, "gov.validate_once", governance.get("validate_once_rule_ref_ok") is True)
    _add(checks, "gov.top_level_ref", governance.get("top_level_objective_priority_rule_ref") == TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_REF)
    _expect_false(checks, "gov.no_shared_reval", governance.get("shared_protocol_system_revalidation"))
    _expect_false(checks, "gov.no_l1_reval", governance.get("l1_input_output_protocol_revalidation"))

    for key in ABSENCE_KEYS:
        _add(checks, f"absence.{key}", summary.get(key) is True)

    for key in FILE_SIZE_KEYS:
        _add(checks, f"file_size.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size.get(key) is True)

    for rel in OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for flag in RUNTIME_FORBIDDEN_FLAGS:
        _add(checks, f"runtime.no_{flag[:25]}", summary.get(flag) is not True)

    next_phase = summary.get("recommended_next_phase") or ""
    _add(checks, "next_phase.candidate_a", NEXT_PHASE_A in next_phase or next_phase in (NEXT_PHASE_A, NEXT_PHASE_B, NEXT_PHASE_C))
    _add(checks, "next_phase.not_real_issuance", "request_issued" not in next_phase.lower())

    for forbidden in FORBIDDEN:
        combined = " ".join([str(summary.get("final_decision") or ""), next_phase]).lower()
        _add(checks, f"forbidden.not_{forbidden}", forbidden not in combined)

    for section in plan.get("integrated_sections") or []:
        _add(checks, f"plan.section.{section[:30]}", bool(section))

    for idx, item in enumerate(checklist.get("items") or []):
        _add(checks, f"checklist.item{idx}", bool(item.get("item_id")))

    for idx, route in enumerate(routing.get("routes") or []):
        _add(checks, f"route{idx}.bucket", bool(route.get("routing_bucket")))

    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.route", SELECTED_ROUTE in md)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "summary.integrated_only", summary.get("integrated_implementation_only") is True)
    _add(checks, "plan.complete", plan.get("integrated_plan_complete") is True)
    _add(checks, "next_phase.readiness", summary.get("next_phase_readiness_ok") is True)
    _add(checks, "next_phase.has_candidates", len(plan.get("next_phase_candidates") or []) >= 3)

    for idx, item in enumerate(checklist.get("items") or []):
        _add(checks, f"checklist.req.{item.get('item_id', '')[:25]}", item.get("required") is True)

    for bucket in (
        "blocker_before_real_issuance",
        "future_runtime_debt",
        "non_blocking_follow_up",
        "governance_debt",
        "resolved",
    ):
        _add(checks, f"routing.bucket.{bucket}", any(r.get("routing_bucket") == bucket for r in routing.get("routes") or []))

    _add(checks, "gov.file_size_ref", bool(governance.get("file_size_module_split_governance_rule_ref")))
    _add(checks, "gov.reuse_ref", bool(governance.get("reuse_first_protocol_engineering_rule_ref")))
    _add(checks, "gov.module_first_ref", bool(governance.get("module_first_development_verification_cadence_rule_ref")))
    _add(checks, "summary.integrated_complete", summary.get("integrated_plan_complete") is True)
    _add(checks, "summary.roadmap", summary.get("integrated_roadmap_decision_complete") is True)
    _add(checks, "summary.auth_prep", summary.get("issuance_authorization_preparation_package_complete") is True)
    _add(checks, "summary.routing", summary.get("missing_conditions_routing_complete") is True)
    _add(checks, "summary.checklist", summary.get("real_issuance_precondition_checklist_complete") is True)
    _add(checks, "summary.closure", summary.get("record_approval_ack_evidence_boundary_complete") is True)
    _add(checks, "summary.slice", summary.get("module_level_functional_slice_test_plan_complete") is True)
    _add(checks, "summary.top_level", summary.get("top_level_objective_priority_rule_ref_ok") is True)
    _add(checks, "summary.module_first", summary.get("module_first_cadence_rule_ref_ok") is True)
    _add(checks, "summary.reuse", summary.get("reuse_first_rule_ref_ok") is True)
    _add(checks, "summary.validate_once", summary.get("validate_once_rule_ref_ok") is True)
    _add(checks, "summary.next_ok", summary.get("next_phase_readiness_ok") is True)
    _add(checks, "plan.recommended", bool(plan.get("recommended_next_phase")))
    _add(checks, "next_phase.a", NEXT_PHASE_A in (summary.get("recommended_next_phase") or ""))
    _add(checks, "next_phase.b_in_candidates", NEXT_PHASE_B in (plan.get("next_phase_candidates") or []))
    _add(checks, "next_phase.c_in_candidates", NEXT_PHASE_C in (plan.get("next_phase_candidates") or []))
    _add(checks, "summary.governance_gate_pass", summary.get("governance_gate_pass") is True)
    _add(checks, "summary.evidence_chain_ok", summary.get("evidence_chain_ok") is True)
    _add(checks, "summary.gate_node_linked", summary.get("governance_gate_node_linked") is True)
    _add(checks, "summary.evidence_paths", summary.get("evidence_paths_declared") is True)
    _add(checks, "summary.candidate_only", summary.get("candidate_only") is True)
    _add(checks, "summary.no_execution_leakage", summary.get("no_execution_leakage") is True)
    _add(checks, "summary.no_protocol_change", summary.get("no_protocol_change") is True)
    _add(checks, "summary.downstream_refs", len(summary.get("downstream_readiness_refs") or []) >= 4)
    _add(checks, "roadmap.secondary", len(roadmap.get("secondary_routes") or []) >= 2)
    _add(checks, "auth_prep.owner_approval", auth_prep.get("owner_operator_explicit_approval_required") is True)
    _add(checks, "checklist.unsatisfied", any(not i.get("satisfied") for i in checklist.get("items") or []))
    _add(checks, "checklist.chain_satisfied", any(i.get("item_id") == "record_approval_closure_candidate_chain" and i.get("satisfied") for i in checklist.get("items") or []))

    for key in GO_CONDITIONS_KEYS:
        if key in plan:
            _add(checks, f"plan.{key}", plan.get(key) is True)
        if key in governance:
            _add(checks, f"gov.{key}", governance.get(key) is True)

    for idx, chain in enumerate(slice_plan.get("chains") or []):
        _add(checks, f"slice.chain{idx}.type", chain.get("test_type") == "functional_slice")

    gate_docs = (plan, roadmap, auth_prep, routing, checklist, closure, slice_plan, governance)
    for idx, doc in enumerate(gate_docs):
        _add(checks, f"doc{idx}.phase", doc.get("phase") == PHASE_ID)
        _add(checks, f"doc{idx}.scope", doc.get("scope") == SCOPE)
        _add(checks, f"doc{idx}.integrated", doc.get("integrated_implementation_only") is True)
        _add(checks, f"doc{idx}.runtime_off", doc.get("runtime_status") == "not_enabled")

    for idx, row in enumerate(closure.get("rows") or []):
        _add(checks, f"closure.row{idx}.forbidden", bool(row.get("forbidden_final_state")))
        _add(checks, f"closure.row{idx}.no_closure", row.get("closure_executed") is False)

    for idx, route in enumerate(routing.get("routes") or []):
        _add(checks, f"route{idx}.id", bool(route.get("condition_id")))
        _add(checks, f"route{idx}.bucket_ok", bool(route.get("routing_bucket")))

    for idx, section in enumerate(plan.get("integrated_sections") or []):
        _add(checks, f"section{idx}", bool(section))

    _add(checks, "file_size.phase_id", file_size.get("phase_id") == PHASE_ID)
    _add(checks, "file_size.read_strategy", file_size.get("read_strategy") == "summary_index_first")
    _add(checks, "file_size.no_full_scan", file_size.get("full_repo_scan") is False)
    _add(checks, "summary.no_indep_roadmap2", summary.get("no_independent_roadmap_verifier") is True)
    _add(checks, "summary.no_indep_auth2", summary.get("no_independent_authorization_planning_phase") is True)
    _add(checks, "summary.no_fragmentary2", summary.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "plan.no_fragmentary", plan.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "plan.prior_post", plan.get("prior_post_review_go") is True)
    _add(
        checks,
        "plan.prior_gate",
        plan.get("prior_final_gate_planning_go") is True or gate_readiness_gap,
    )
    _add(checks, "md.no_fragmentary", "fragmentary" in md.lower())
    _add(checks, "md.preparation", "Preparation" in md or "preparation" in md.lower())
    _add(checks, "summary.final_decision_go", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "plan.final_decision_go", plan.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "routing.real_unresolved", routes.get("real_request_issuance", {}).get("source_resolved") is False)
    _add(checks, "auth_prep.real_auth_false", auth_prep.get("real_request_issuance_authorized") is False if "real_request_issuance_authorized" in auth_prep else True)
    _add(checks, "checklist.real_auth_false", checklist.get("real_request_issuance_authorized") is False)
    _add(checks, "roadmap.real_auth_false", roadmap.get("real_request_issuance_authorized") is False if "real_request_issuance_authorized" in roadmap else True)
    _add(checks, "summary.runtime_absent", summary.get("runtime_execution_absent") is True)
    _add(checks, "summary.adapter_absent", summary.get("module_adapter_implementation_absent") is True)
    _add(checks, "summary.whitebox_absent", summary.get("whitebox_runtime_integration_absent") is True)
    _add(checks, "summary.grant_absent", summary.get("grant_absent") is True)
    _add(checks, "summary.auth_req_absent", summary.get("authorization_request_absent") is True)

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "integrated_implementation_verifier_only": True,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{k: summary.get(k) is True for k in GO_CONDITIONS_KEYS},
        "selected_route": SELECTED_ROUTE,
        "final_decision": FINAL_DECISION_GO if verifier == "GO" else "HOLD",
        "recommended_next_phase": summary.get("recommended_next_phase") if verifier == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:40],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": verifier, "passed_checks": passed, "failed_checks": len(failed), "selected_route": SELECTED_ROUTE, "final_decision": report["final_decision"], "recommended_next_phase": report["recommended_next_phase"]}, ensure_ascii=False))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
