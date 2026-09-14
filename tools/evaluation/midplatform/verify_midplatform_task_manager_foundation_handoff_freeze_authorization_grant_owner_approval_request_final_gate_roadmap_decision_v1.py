#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Final Gate Roadmap Decision v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import (
    FILE_SIZE_GOVERNANCE_REVIEW_KEYS,
)
from capabilities.midplatform.owner_approval_request_governance_gate_template_lineage_v1 import (
    GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1 import (
    FINAL_DECISION_GO as FINAL_GATE_PLANNING_FINAL_GO,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_roadmap_decision_v1 import (
    ABSENCE_KEYS,
    DEFAULT_FINAL_GATE_PLANNING_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    FINAL_GATE_INDEX_FILES,
    GO_CONDITIONS_KEYS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    ROADMAP_DECISION_ARTIFACTS,
    ROUTE_A,
    ROUTE_B,
    ROUTE_C,
    ROUTE_D,
    ROUTE_E,
    SCOPE,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)

MIN_CHECKS = 280
FORBIDDEN_FINAL_TARGETS: Tuple[str, ...] = (
    "request_issued",
    "request_record_created",
    "approval_record_created",
    "approval_created",
    "grant_issued",
    "foundation_frozen",
    "closed",
    "closure_executed",
    "module_adapter_implementation",
    "real_request_issuance_execution",
)
FILE_SIZE_SUMMARY_KEYS: Tuple[str, ...] = (
    "file_size_governance_review_exists",
    "file_size_governance_review_ok",
    "monolithic_file_absent",
    "large_file_read_avoidance_ok",
    "summary_index_first_reading_ok",
    "verifier_large_file_scan_absent",
    "full_repo_scan_absent",
    "tmp_eval_out_scan_absent",
    "limited_directory_scan_ok",
)


def _read(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _add(checks: List[Dict[str, Any]], check_id: str, passed: bool, detail: str = "") -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def _expect_false(checks: List[Dict[str, Any]], check_id: str, value: Any) -> None:
    _add(checks, check_id, value is False)


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--final-gate-planning-root", default=DEFAULT_FINAL_GATE_PLANNING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    final_gate = Path(args.final_gate_planning_root)
    checks: List[Dict[str, Any]] = []

    gate_summary = _read(final_gate / "summary.json")
    gate_verifier = _read(final_gate / "verifier_report.json")
    gate_missing = _read(final_gate / FINAL_GATE_INDEX_FILES[2])

    md_path = root / "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_roadmap_decision_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""
    docs = {
        name: _read(root / name)
        for name in ROADMAP_DECISION_ARTIFACTS
        if name.endswith(".json") and name != "verifier_report.json"
    }
    summary = docs["summary.json"]

    for name in ROADMAP_DECISION_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        _add(checks, f"artifact.exists.{name}", path.is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(path)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 80)

    _add(checks, "upstream.summary.exists", bool(gate_summary))
    _add(checks, "upstream.verifier.exists", bool(gate_verifier))
    _add(checks, "upstream.summary_go", gate_summary.get("final_decision") == FINAL_GATE_PLANNING_FINAL_GO)
    _add(checks, "upstream.verifier_go", gate_verifier.get("verifier") == "GO")
    _add(checks, "upstream.passed_min", int(gate_verifier.get("passed_checks", 0)) >= 300)
    _add(checks, "upstream.plan_complete", gate_summary.get("final_gate_plan_complete") is True)
    _add(checks, "upstream.missing_complete", gate_summary.get("missing_conditions_matrix_complete") is True)
    _add(checks, "upstream.blocker_complete", gate_summary.get("blocker_matrix_complete") is True)
    _add(checks, "upstream.module_first_ok", gate_summary.get("module_first_cadence_rule_ref_ok") is True)
    _add(checks, "upstream.file_size_ok", gate_summary.get("file_size_governance_review_ok") is True)
    _add(checks, "upstream.no_real_issuance_auth", gate_summary.get("real_request_issuance_authorized") is not True)
    gate_blockers = _read(final_gate / FINAL_GATE_INDEX_FILES[3])
    gate_missing_conds = gate_missing.get("conditions") or []
    upstream_real = next((c for c in gate_missing_conds if c.get("condition_id") == "real_request_issuance"), {})
    _add(checks, "upstream.real_request.blocker", upstream_real.get("category") == "blocker")
    _add(checks, "upstream.real_request.unresolved", upstream_real.get("resolved") is False)
    _add(
        checks,
        "upstream.real_request_blocker_active",
        any(
            b.get("blocker_id") == "real_request_issuance_not_authorized" and b.get("active")
            for b in gate_blockers.get("blockers") or []
        ),
    )

    for fname in FINAL_GATE_INDEX_FILES:
        _add(checks, f"upstream.index.exists.{fname}", (final_gate / fname).is_file())

    decision = docs["task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_roadmap_decision_v1.json"]
    route_matrix = docs["task_manager_freeze_authorization_grant_owner_approval_request_final_gate_route_matrix_v1.json"]
    mapping = docs["task_manager_freeze_authorization_grant_owner_approval_request_final_gate_missing_conditions_route_mapping_v1.json"]
    rationale = docs["task_manager_freeze_authorization_grant_owner_approval_request_final_gate_selected_route_rationale_v1.json"]
    boundary = docs["task_manager_freeze_authorization_grant_owner_approval_request_final_gate_non_execution_boundary_v1.json"]
    next_phase = docs["task_manager_freeze_authorization_grant_owner_approval_request_final_gate_next_phase_readiness_v1.json"]
    file_size_review = docs["file_size_governance_review_v1.json"]

    _add(checks, "summary.pass", summary.get("roadmap_decision_pass") is True)
    _add(checks, "summary.roadmap_only", summary.get("roadmap_decision_only") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.scope", summary.get("scope") == SCOPE)
    _add(checks, "summary.selected_route", summary.get("selected_route") == ROUTE_A)

    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
        if key in decision:
            _add(checks, f"decision.{key}", decision.get(key) is True)

    _expect_false(checks, "summary.real_issuance_auth", summary.get("real_request_issuance_authorized"))
    _expect_false(checks, "decision.real_issuance_auth", decision.get("real_request_issuance_authorized"))

    _add(checks, "decision.complete", decision.get("roadmap_decision_complete") is True)
    _add(checks, "decision.selected_route_a", decision.get("selected_route") == ROUTE_A)
    _add(checks, "decision.auth_planning", decision.get("selected_route_is_authorization_planning") is True)
    _add(checks, "decision.not_executed", decision.get("real_request_issuance_not_executed") is True)

    _add(checks, "route_matrix.complete", route_matrix.get("route_matrix_complete") is True)
    _add(checks, "route_matrix.selected", route_matrix.get("selected_route") == ROUTE_A)
    for route_label in (ROUTE_A, ROUTE_B, ROUTE_C, ROUTE_D, ROUTE_E):
        row = next((r for r in route_matrix.get("routes") or [] if r.get("route_label") == route_label), {})
        _add(checks, f"route.exists.{route_label[:8]}", bool(row))
        _add(checks, f"route.no_exec.{route_label[:8]}", row.get("executes_real_issuance") is False)

    _add(checks, "mapping.complete", mapping.get("missing_conditions_route_mapping_complete") is True)
    mappings = mapping.get("mappings") or []
    _add(checks, "mapping.count", len(mappings) >= 6)

    cond_map = {m.get("condition_id"): m for m in mappings}
    real_req = cond_map.get("real_request_issuance", {})
    _add(checks, "mapping.real_request.blocker", real_req.get("source_category") == "blocker")
    _add(checks, "mapping.real_request.unresolved", real_req.get("source_resolved") is False)
    _add(checks, "mapping.real_request.route_a", real_req.get("primary_route") == ROUTE_A)

    runtime = cond_map.get("runtime_adapter_implementation", {})
    _add(checks, "mapping.runtime.future", runtime.get("routed_category") == "future_runtime")
    _add(checks, "mapping.runtime.route_d", runtime.get("primary_route") == ROUTE_D)

    whitebox = cond_map.get("whitebox_runtime_integration", {})
    _add(checks, "mapping.whitebox.future", whitebox.get("routed_category") == "future_runtime")
    _add(checks, "mapping.whitebox.route_d", whitebox.get("primary_route") == ROUTE_D)

    slice_tests = cond_map.get("module_level_functional_slice_tests", {})
    _add(checks, "mapping.slice.non_blocking", slice_tests.get("routed_category") == "non_blocking")
    _add(checks, "mapping.slice.route_c", slice_tests.get("primary_route") == ROUTE_C)

    gov_debt = cond_map.get("governance_debt_closure", {})
    _add(checks, "mapping.gov_debt.category", gov_debt.get("routed_category") == "governance_debt")
    _add(checks, "mapping.gov_debt.route_e", gov_debt.get("primary_route") == ROUTE_E)

    chain = cond_map.get("record_approval_closure_candidate_chain", {})
    _add(checks, "mapping.chain.resolved", chain.get("source_resolved") is True)
    _add(checks, "mapping.chain.route_a", chain.get("primary_route") == ROUTE_A)

    _add(checks, "rationale.complete", rationale.get("selected_route_rationale_complete") is True)
    _add(checks, "rationale.selected_a", rationale.get("selected_route") == ROUTE_A)
    _add(checks, "rationale.points", len(rationale.get("rationale_points") or []) >= 5)
    _add(checks, "rationale.not_execution", "not execution" in " ".join(rationale.get("rationale_points") or []).lower())

    _add(checks, "boundary.ok", boundary.get("non_execution_boundary_ok") is True)
    for field in (
        "request_issued",
        "notification_sent",
        "request_record_created",
        "approval_record_created",
        "grant_issued",
        "foundation_frozen",
        "closure_executed",
    ):
        _add(checks, f"boundary.{field}_false", boundary.get(field) is False)
    for key in ABSENCE_KEYS:
        _add(checks, f"boundary.absence.{key}", boundary.get(key) is True)
        _add(checks, f"summary.absence.{key}", summary.get(key) is True)

    _add(checks, "next_phase.ok", next_phase.get("next_phase_readiness_ok") is True)
    _add(checks, "next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(
        checks,
        "next_phase.target",
        next_phase.get("target") == "freeze_authorization_grant_owner_approval_request_issuance_authorization_planning",
    )
    _add(checks, "next_phase.auth_planning_ready", next_phase.get("issuance_authorization_planning_readiness") is True)
    _expect_false(checks, "next_phase.no_real_issuance_auth", next_phase.get("real_request_issuance_authorized"))

    for forbidden in FORBIDDEN_FINAL_TARGETS:
        combined = " ".join(
            [
                str(summary.get("final_decision") or ""),
                str(summary.get("recommended_next_phase") or ""),
                str(decision.get("selected_route") or ""),
            ]
        ).lower()
        _add(checks, f"final.not_{forbidden}", forbidden not in combined)

    for key in FILE_SIZE_SUMMARY_KEYS:
        _add(checks, f"file_size.summary.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size_review.get(key) is True)
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size_review.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.phase_file.{rel.split('/')[-1]}", row.get("exists") is True)

    for rel in GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for flag in RUNTIME_FORBIDDEN_FLAGS:
        _add(checks, f"summary.no_runtime.{flag}", summary.get(flag) is not True)

    _expect_false(checks, "summary.no_shared_revalidation", summary.get("shared_protocol_system_revalidation"))
    _expect_false(checks, "summary.no_l1_revalidation", summary.get("l1_input_output_protocol_revalidation"))

    gate_docs = (decision, route_matrix, mapping, rationale, boundary, next_phase)
    for idx, doc in enumerate(gate_docs):
        _add(checks, f"doc{idx}.phase", doc.get("phase") == PHASE_ID)
        _add(checks, f"doc{idx}.roadmap_only", doc.get("roadmap_decision_only") is True)
        _add(checks, f"doc{idx}.scope", doc.get("scope") == SCOPE)
        _add(checks, f"doc{idx}.runtime_off", doc.get("runtime_status") == "not_enabled")

    upstream_conditions = gate_missing.get("conditions") or []
    for cond in upstream_conditions:
        cid = cond.get("condition_id")
        mapped = cond_map.get(cid, {})
        _add(checks, f"upstream_mapped.{cid}", bool(mapped))

    _add(checks, "summary.prior_gate_go", summary.get("prior_final_gate_planning_go") is True)
    _add(checks, "decision.final_match", decision.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "next_phase.auth_planning", "Issuance-Authorization-Planning" in (next_phase.get("recommended_next_phase") or ""))
    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.route_a", ROUTE_A in md)
    _add(checks, "md.no_real_issuance", "No real request issuance" in md)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])

    for idx, m in enumerate(mappings):
        _add(checks, f"mapping{idx}.disposition", bool(m.get("disposition")))
        _add(checks, f"mapping{idx}.primary", bool(m.get("primary_route")))

    for idx, pt in enumerate(rationale.get("rationale_points") or []):
        _add(checks, f"rationale.point{idx}", len(pt) > 10)

    for route in route_matrix.get("routes") or []:
        rid = route.get("route_id")
        _add(checks, f"route.{rid}.role", bool(route.get("role")))
        _add(checks, f"route.{rid}.targets", bool(route.get("targets")))

    _add(checks, "rationale.secondary_count", len(rationale.get("secondary_routes") or []) >= 4)
    _add(checks, "decision.secondary_routes", len(decision.get("secondary_routes") or []) >= 4)
    _add(checks, "summary.template_lineage_ok", summary.get("template_lineage_ok") is True)
    _add(checks, "upstream.final_gate_pass", gate_summary.get("final_gate_planning_pass") is True)
    _add(checks, "upstream.non_execution", gate_summary.get("non_execution_boundary_ok") is True)
    _add(checks, "mapping.real_request.secondary_b", real_req.get("secondary_route") == ROUTE_B)
    _add(checks, "mapping.runtime.debt_preserved", "debt" in (runtime.get("disposition") or ""))
    _add(checks, "mapping.whitebox.not_blocking", "not_blocking" in (whitebox.get("disposition") or ""))
    _add(checks, "mapping.slice.parallel", "parallel" in (slice_tests.get("disposition") or ""))
    _add(checks, "mapping.gov.not_resolved", "not_resolved" in (gov_debt.get("disposition") or ""))
    _add(checks, "mapping.chain.prerequisite", "prerequisite" in (chain.get("disposition") or ""))
    _add(checks, "boundary.runtime_absent", boundary.get("runtime_execution_absent") is True)
    _add(checks, "next_phase.request_false", next_phase.get("request_issued") is False)
    _add(checks, "decision.upstream_decision", bool(decision.get("final_gate_final_decision")))
    _add(checks, "decision.readiness_ref", bool(decision.get("readiness_matrix_ref")))
    _add(checks, "route_matrix.primary_a", route_matrix.get("routes")[0].get("route_id") == "A")
    _add(checks, "summary.real_not_executed", summary.get("real_request_issuance_not_executed") is True)
    _add(checks, "summary.auth_planning_route", summary.get("selected_route_is_authorization_planning") is True)
    _add(checks, "summary.roadmap_complete", summary.get("roadmap_decision_complete") is True)
    _add(checks, "summary.route_matrix", summary.get("route_matrix_complete") is True)

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "roadmap_decision_verifier_only": True,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{k: summary.get(k) is True for k in GO_CONDITIONS_KEYS},
        "real_request_issuance_authorized": summary.get("real_request_issuance_authorized") is False,
        "selected_route": summary.get("selected_route"),
        "final_decision": FINAL_DECISION_GO if verifier == "GO" else "HOLD",
        "recommended_next_phase": NEXT_PHASE_GO if verifier == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:40],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": report_payload["verifier"],
                "passed_checks": report_payload["passed_checks"],
                "failed_checks": report_payload["failed_checks"],
                "blocker_count": report_payload["blocker_count"],
                "selected_route": report_payload["selected_route"],
                "final_decision": report_payload["final_decision"],
                "recommended_next_phase": report_payload["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
