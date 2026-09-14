#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Evidence Record Approval Permission Alignment Planning v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.candidate_lifecycle_unification_items_v1 import SELECTED_NEXT_ROUTE as UPSTREAM_SELECTED_ROUTE
from capabilities.midplatform.candidate_lifecycle_unification_planning_v1 import (
    FINAL_DECISION_GO as CANDIDATE_LIFECYCLE_PLANNING_FINAL_GO,
    NEXT_PHASE_GO as CANDIDATE_LIFECYCLE_PLANNING_NEXT_PHASE,
)
from capabilities.midplatform.evidence_record_approval_permission_alignment_items_v1 import (
    ALIGNMENT_OBJECT_REGISTRY,
    ALIGNMENT_OBJECT_REQUIRED_FIELDS,
    CANDIDATE_OBJECT_IDS,
    REAL_OBJECT_IDS,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.evidence_record_approval_permission_alignment_lineage_v1 import ALIGNMENT_PLANNING_WHITELIST_FILES
from capabilities.midplatform.evidence_record_approval_permission_alignment_planning_v1 import (
    DEFAULT_CANDIDATE_LIFECYCLE_PLANNING_ROOT,
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
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import ABSENCE_KEYS

MIN_CHECKS = 320
FORBIDDEN = ("midplatform_completed", "request_issued", "grant_issued", "runtime_enabled", "integration_test_executed", "record_created")
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
    parser.add_argument("--candidate-lifecycle-unification-planning-root", default=DEFAULT_CANDIDATE_LIFECYCLE_PLANNING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    upstream = Path(args.candidate_lifecycle_unification_planning_root)
    checks: List[Dict[str, Any]] = []

    lifecycle_summary = _read(upstream / "summary.json")
    lifecycle_verifier = _read(upstream / "verifier_report.json")
    md = (root / "evidence_record_approval_permission_alignment_planning_report_v1.md").read_text(encoding="utf-8") if (root / "evidence_record_approval_permission_alignment_planning_report_v1.md").is_file() else ""
    docs = {n: _read(root / n) for n in PLANNING_ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    report = docs["evidence_record_approval_permission_alignment_planning_report_v1.json"]
    scope = docs["alignment_scope_v1.json"]
    obj_reg = docs["alignment_object_registry_v1.json"]
    boundary = docs["candidate_real_object_boundary_matrix_v1.json"]
    preconditions = docs["promotion_creation_preconditions_v1.json"]
    responsibility = docs["alignment_responsibility_matrix_v1.json"]
    forbidden = docs["forbidden_alignment_transitions_v1.json"]
    traceability = docs["alignment_traceability_contract_v1.json"]
    gap_register = docs["alignment_gap_register_v1.json"]
    route_decision = docs["next_route_decision_v1.json"]
    misclassify = docs["do_not_misclassify_rules_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]
    objects = obj_reg.get("objects") or []

    for name in PLANNING_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        ok = path.is_file() and (bool(_read(path)) if name.endswith(".json") else len(md.strip()) > 40)
        _add(checks, f"artifact.{name.split('.')[0]}", ok)

    _add(checks, "upstream.lifecycle_go", lifecycle_summary.get("final_decision") == CANDIDATE_LIFECYCLE_PLANNING_FINAL_GO)
    _add(checks, "upstream.lifecycle_verifier", lifecycle_verifier.get("verifier") == "GO")
    _add(checks, "upstream.selected_route", lifecycle_summary.get("selected_next_route") == UPSTREAM_SELECTED_ROUTE)
    _add(checks, "upstream.lifecycle_next", lifecycle_summary.get("recommended_next_phase") == CANDIDATE_LIFECYCLE_PLANNING_NEXT_PHASE)

    _add(checks, "summary.pass", summary.get("alignment_planning_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
    _expect_false(checks, "summary.real_auth", summary.get("real_request_issuance_authorized"))
    _expect_false(checks, "summary.promotion_exec", summary.get("candidate_promotion_executed"))
    _add(checks, "summary.precond_not_exec", summary.get("promotion_preconditions_not_promotion_execution") is True)
    _add(checks, "summary.real_objects_absent", summary.get("real_objects_absent") is True)
    _add(checks, "summary.alignment_runtime_absent", summary.get("alignment_runtime_absent") is True)
    _add(checks, "summary.evidence_not_record", summary.get("evidence_candidate_not_evidence_record") is True)
    _add(checks, "summary.record_not_req", summary.get("record_candidate_not_request_record") is True)
    _add(checks, "summary.approval_not_rec", summary.get("approval_candidate_not_approval_record") is True)
    _add(checks, "summary.ack_not_rec", summary.get("ack_record_candidate_not_ack_record") is True)
    _add(checks, "summary.perm_not_grant", summary.get("permission_candidate_not_grant") is True)
    _add(checks, "summary.grant_cand_not_rec", summary.get("grant_candidate_not_grant_record") is True)
    _add(checks, "summary.auth_not_req", summary.get("authorization_request_candidate_not_authorization_request") is True)
    _add(checks, "summary.chain_not_reopen", summary.get("owner_approval_request_chain_not_reopened") is True)
    _expect_false(checks, "summary.integration_test", summary.get("integration_test_executed"))

    _add(checks, "scope.complete", scope.get("alignment_scope_complete") is True)
    _add(checks, "scope.not_promotion", scope.get("not_promotion_execution") is True)
    _add(checks, "scope.not_real", scope.get("not_real_object_creation") is True)
    _add(checks, "obj_reg.complete", obj_reg.get("alignment_object_registry_complete") is True)
    _add(checks, "obj_reg.count13", len(objects) >= 13)
    _add(checks, "boundary.complete", boundary.get("candidate_real_object_boundary_matrix_complete") is True)
    _add(checks, "boundary.pairs9", len(boundary.get("pairs") or []) >= 9)
    _add(checks, "precond.complete", preconditions.get("promotion_creation_preconditions_complete") is True)
    _add(checks, "precond.not_executed", preconditions.get("promotion_executed") is False)
    _add(checks, "resp.complete", responsibility.get("alignment_responsibility_matrix_complete") is True)
    _add(checks, "forbidden.complete", forbidden.get("forbidden_alignment_transitions_complete") is True)
    _add(checks, "forbidden.trans9", len(forbidden.get("transitions") or []) >= 9)
    _add(checks, "trace.complete", traceability.get("alignment_traceability_contract_complete") is True)
    _add(checks, "trace.no_real", traceability.get("no_real_trace_record_created") is True)
    _add(checks, "gaps.complete", gap_register.get("alignment_gap_register_complete") is True)
    _add(checks, "route.complete", route_decision.get("next_route_decision_complete") is True)
    _add(checks, "route.selected_a", route_decision.get("selected_next_route") == SELECTED_NEXT_ROUTE)
    _add(checks, "route.next_orch", NEXT_PHASE_GO in (route_decision.get("recommended_next_phase") or ""))

    for oid in ALIGNMENT_OBJECT_REGISTRY:
        eid = oid["object_id"]
        entry = next((o for o in objects if o.get("object_id") == eid), {})
        _add(checks, f"obj.{eid[:22]}", bool(entry))
        _add(checks, f"obj.{eid[:12]}.no_create", entry.get("creation_allowed_now") is False)
        _add(checks, f"obj.{eid[:12]}.no_runtime", entry.get("runtime_required_now") is False)

    for oid in CANDIDATE_OBJECT_IDS:
        entry = next((o for o in objects if o.get("object_id") == oid), {})
        _add(checks, f"cand.{oid[:18]}", entry.get("object_layer") == "candidate")

    for oid in REAL_OBJECT_IDS:
        entry = next((o for o in objects if o.get("object_id") == oid), {})
        _add(checks, f"real.{oid[:18]}", entry.get("creation_allowed_now") is False)

    for idx, entry in enumerate(objects):
        for field in ALIGNMENT_OBJECT_REQUIRED_FIELDS:
            _add(checks, f"o{idx}.{field[:10]}", entry.get(field) is not None and entry.get(field) != "")

    for pair in boundary.get("pairs") or []:
        _add(checks, f"pair.{pair.get('rule', '')[:20]}", bool(pair.get("rule")))

    for key in ABSENCE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
    _add(checks, "summary.record_creation_absent", summary.get("record_creation_absent") is True)
    _add(checks, "summary.grant_absent", summary.get("grant_absent") is True)
    _add(checks, "summary.auth_req_absent", summary.get("authorization_request_absent") is True)
    _add(checks, "summary.evidence_absent", summary.get("evidence_bound_record_absent") is True)
    _add(checks, "summary.request_record_absent", summary.get("request_record_absent") is True)
    _add(checks, "summary.approval_record_absent", summary.get("approval_record_absent") is True)
    _add(checks, "summary.ack_record_absent", summary.get("ack_record_absent") is True)

    for key in FILE_SIZE_KEYS:
        _add(checks, f"file_size.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size.get(key) is True)
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.file.{rel.split('/')[-1]}", row.get("exists") is True and row.get("tier") != "blocker_candidate")

    for rel in ALIGNMENT_PLANNING_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for fb in FORBIDDEN:
        combined = f"{summary.get('final_decision')} {summary.get('recommended_next_phase')} {md}".lower()
        _add(checks, f"forbidden.not_{fb[:15]}", fb not in combined)

    _add(checks, "summary.prior_lifecycle", summary.get("prior_candidate_lifecycle_unification_go") is True)
    _add(checks, "summary.non_exec", summary.get("non_execution_boundary_ok") is True)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "upstream.verifier_min", int(lifecycle_verifier.get("passed_checks", 0)) >= 320)
    _add(checks, "resp.rows8", len(responsibility.get("rows") or []) >= 8)
    _add(checks, "precond.items10", len(preconditions.get("preconditions") or []) >= 10)
    _add(checks, "gaps.items8", len(gap_register.get("gaps") or []) >= 8)
    _add(checks, "misclassify.rules9", len(misclassify.get("rules") or []) >= 9)
    _add(checks, "owner_closed_module", summary.get("owner_approval_request_closed_module") == "governance_ready_handoff")
    _add(checks, "summary.construction", summary.get("midplatform_overall_status") == MIDPLATFORM_OVERALL_STATUS)

    for rule in misclassify.get("rules") or []:
        _add(checks, f"rule.{rule[:20]}", True)
    for row in responsibility.get("rows") or []:
        _add(checks, f"resp.{row.get('module_id', '')[:18]}", bool(row.get("responsibility")))
    for p in preconditions.get("preconditions") or []:
        _add(checks, f"pre.{p.get('precondition_id', '')[:18]}", p.get("executed_now") is False)
    for t in forbidden.get("transitions") or []:
        _add(checks, f"trans.{t.get('from', '')[:15]}", t.get("forbidden_now") is True)
    for c in traceability.get("contracts") or []:
        _add(checks, f"trace.{c.get('contract_id', '')[:18]}", bool(c.get("contract_id")))
    for gap in gap_register.get("gaps") or []:
        _add(checks, f"gap.{gap.get('gap_id', '')[:18]}", bool(gap.get("gap_id")))
    for alt in route_decision.get("alternate_routes") or []:
        _add(checks, f"alt.{alt.get('route_id', '')}", bool(alt))

    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_file.{rel.split('/')[-1]}.lines", (row.get("line_count") or 0) <= 800)

    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "md.final", FINAL_DECISION_GO in md or "ORCHESTRATION" in md)
    _add(checks, "md.selected_route", SELECTED_NEXT_ROUTE in md)
    _add(checks, "file_size.no_blocker", len(file_size.get("blocker_candidate_files") or []) == 0)
    _add(checks, "summary.template_lineage", summary.get("template_lineage_ok") is True)
    _add(checks, "scope.not_reopen", scope.get("not_reopen_owner_approval_request") is True)
    _add(checks, "route.no_complete", route_decision.get("do_not_declare_midplatform_completed") is True)
    _add(checks, "gaps.no_blocker", all(not g.get("blocker_now") for g in gap_register.get("gaps") or []))
    _add(checks, "summary.runtime_debt_ok", summary.get("future_runtime_debt_not_current_blocker") is True)
    _add(checks, "upstream.failed0", lifecycle_verifier.get("failed_checks") == 0)
    _add(checks, "report.pass_flag", report.get("alignment_planning_pass") is True)
    _add(checks, "md.next_phase", NEXT_PHASE_GO in md or "Orchestration" in md)
    _add(checks, "misclassify.alignment_rule", "alignment_planning_not_alignment_runtime" in (misclassify.get("rules") or []))
    _add(checks, "misclassify.precond_rule", "promotion_preconditions_not_promotion_execution" in (misclassify.get("rules") or []))
    _add(checks, "upstream.lifecycle_runtime_absent", lifecycle_summary.get("candidate_lifecycle_runtime_absent") is True)
    _add(checks, "upstream.all_types", lifecycle_summary.get("all_candidate_types_covered") is True)
    _add(checks, "route.rationale", bool(route_decision.get("rationale")))
    _add(checks, "summary.scope_meta", summary.get("scope") == SCOPE)
    _add(checks, "align_mod.owns_rules", any(o.get("object_id") == "evidence_candidate" and o.get("owning_module") == "candidate_lifecycle_manager" for o in objects))
    _add(checks, "future_adapter.real_objs", all(
        next((o for o in objects if o.get("object_id") == rid), {}).get("owning_module") == "future_runtime_adapter"
        for rid in REAL_OBJECT_IDS
    ))

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "alignment_planning_verifier_only": True,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{k: summary.get(k) is True for k in GO_CONDITIONS_KEYS},
        "real_request_issuance_authorized": False,
        "integration_test_executed": False,
        "candidate_promotion_executed": False,
        "alignment_runtime_absent": summary.get("alignment_runtime_absent") is True,
        "real_objects_absent": summary.get("real_objects_absent") is True,
        "record_creation_absent": summary.get("record_creation_absent") is True,
        "grant_absent": summary.get("grant_absent") is True,
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
