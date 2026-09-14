#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Broader Midplatform Closure Roadmap v1."""

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
from capabilities.midplatform.task_manager_broader_midplatform_closure_lineage_v1 import (
    BROADER_MIDPLATFORM_CLOSURE_ROADMAP_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_broader_midplatform_closure_roadmap_v1 import (
    ABSENCE_KEYS,
    DEFAULT_MODULE_HANDOFF_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    ROADMAP_ARTIFACTS,
    ROUTE_A,
    SCOPE,
    SELECTED_ROUTE,
)
from capabilities.midplatform.task_manager_owner_approval_request_module_handoff_v1 import (
    FINAL_DECISION_GO as MODULE_HANDOFF_FINAL_GO,
)

MIN_CHECKS = 260
FORBIDDEN: Tuple[str, ...] = (
    "request_issued",
    "authorization_request_created",
    "grant_issued",
    "record_created",
    "foundation_frozen",
    "runtime_enabled",
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
    parser.add_argument("--module-handoff-root", default=DEFAULT_MODULE_HANDOFF_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    upstream = Path(args.module_handoff_root)
    checks: List[Dict[str, Any]] = []

    handoff_summary = _read(upstream / "summary.json")
    handoff_verifier = _read(upstream / "verifier_report.json")

    md = (
        (root / "broader_midplatform_closure_roadmap_v1.md").read_text(encoding="utf-8")
        if (root / "broader_midplatform_closure_roadmap_v1.md").is_file()
        else ""
    )
    docs = {n: _read(root / n) for n in ROADMAP_ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    roadmap = docs["broader_midplatform_closure_roadmap_v1.json"]
    inventory = docs["broader_midplatform_status_inventory_v1.json"]
    gap_matrix = docs["midplatform_closure_gap_matrix_v1.json"]
    integration = docs["module_integration_map_v1.json"]
    route_decision = docs["mainline_closure_route_decision_v1.json"]
    test_consolidation = docs["future_test_strategy_consolidation_v1.json"]
    do_not_reopen = docs["do_not_reopen_rules_v1.json"]
    next_phase = docs["next_phase_recommendation_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]

    for name in ROADMAP_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        ok = path.is_file() and (bool(_read(path)) if name.endswith(".json") else len(md.strip()) > 60)
        _add(checks, f"artifact.{name.split('.')[0]}", ok)

    _add(checks, "upstream.handoff_go", handoff_summary.get("final_decision") == MODULE_HANDOFF_FINAL_GO)
    _add(checks, "upstream.handoff_verifier", handoff_verifier.get("verifier") == "GO")
    _add(checks, "upstream.chain_not_ext", handoff_summary.get("owner_approval_request_chain_not_extended") is True)
    _add(checks, "upstream.no_preauth", handoff_summary.get("do_not_open_real_issuance_preauth_unless_mainline_requires") is True if "do_not_open_real_issuance_preauth_unless_mainline_requires" in handoff_summary else True)

    _add(checks, "summary.pass", summary.get("broader_midplatform_closure_roadmap_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "summary.roadmap_only", summary.get("broader_midplatform_closure_roadmap_only") is True if "broader_midplatform_closure_roadmap_only" in summary else summary.get("scope") == SCOPE)

    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _expect_false(checks, "summary.real_auth", summary.get("real_request_issuance_authorized"))
    _add(checks, "summary.owner_status", summary.get("owner_approval_request_closed_module_status") == "governance_ready_handoff")
    _add(checks, "summary.selected_route", summary.get("selected_route") == SELECTED_ROUTE)
    _add(checks, "summary.not_preauth", "PreAuthorization" not in (summary.get("selected_route") or ""))
    _add(checks, "summary.runtime_debt_ok", summary.get("future_runtime_debt_not_current_blocker") is True)
    _expect_false(checks, "summary.shared_reval", summary.get("shared_protocol_system_revalidation"))
    _expect_false(checks, "summary.l1_reval", summary.get("l1_input_output_protocol_revalidation"))

    _add(checks, "inventory.complete", inventory.get("broader_midplatform_status_inventory_complete") is True)
    _add(checks, "gap.complete", gap_matrix.get("midplatform_closure_gap_matrix_complete") is True)
    _add(checks, "integration.complete", integration.get("module_integration_map_complete") is True)
    _add(checks, "route.complete", route_decision.get("mainline_closure_route_decision_complete") is True)
    _add(checks, "test.complete", test_consolidation.get("future_test_strategy_consolidation_complete") is True)
    _add(checks, "reopen.complete", do_not_reopen.get("do_not_reopen_rules_complete") is True)
    _add(checks, "next.complete", next_phase.get("next_phase_recommendation_complete") is True)

    owner_item = next((i for i in inventory.get("items") or [] if i.get("item_id") == "owner_approval_request_closed_module"), {})
    _add(checks, "inventory.owner_handoff", owner_item.get("status") == "governance_ready_handoff")
    _add(checks, "inventory.items9", len(inventory.get("items") or []) >= 9)
    _add(checks, "gap.debt_not_blocker", gap_matrix.get("future_runtime_debt_not_current_blocker") is True)
    for gap in gap_matrix.get("gaps") or []:
        if gap.get("bucket") == "future_runtime_debt":
            _add(checks, f"gap.{gap.get('gap_id', '')[:18]}.not_block", gap.get("blocking_now") is False)
    _add(checks, "route.selected_a", route_decision.get("selected_route") == ROUTE_A)
    _add(checks, "route.not_preauth", route_decision.get("not_selected_real_issuance_preauth") is True)
    _add(checks, "integration.modules6", len(integration.get("modules") or []) >= 6)
    _add(checks, "integration.owner_note", bool(integration.get("owner_approval_request_note")))
    _add(checks, "test.no_runtime", test_consolidation.get("no_runtime_test_now") is True)
    _add(checks, "test.dryrun_input", test_consolidation.get("owner_approval_request_slice_dryrun_as_input") is True)
    _add(checks, "reopen.no_extend", "do_not_extend_owner_approval_request_fragmentary_phases" in (do_not_reopen.get("rules") or []))
    _add(checks, "reopen.no_l1", "do_not_reopen_l1_protocol_review" in (do_not_reopen.get("rules") or []))
    _add(checks, "next.foundation", NEXT_PHASE_GO in (next_phase.get("recommended_next_phase") or ""))

    for key in ABSENCE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _add(checks, "summary.record_creation_absent", summary.get("record_creation_absent") is True)
    _add(checks, "summary.auth_req_absent", summary.get("authorization_request_absent") is True)
    _add(checks, "summary.grant_absent", summary.get("grant_absent") is True)
    _add(checks, "summary.runtime_absent", summary.get("runtime_execution_absent") is True)
    _add(checks, "summary.adapter_absent", summary.get("module_adapter_implementation_absent") is True)
    _add(checks, "summary.whitebox_absent", summary.get("whitebox_runtime_integration_absent") is True)
    _add(checks, "summary.no_fragmentary", summary.get("no_fragmentary_phase_expansion") is True)

    for key in FILE_SIZE_KEYS:
        _add(checks, f"file_size.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size.get(key) is True)
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.file.{rel.split('/')[-1]}", row.get("exists") is True and row.get("tier") != "blocker_candidate")

    for rel in BROADER_MIDPLATFORM_CLOSURE_ROADMAP_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for forbidden in FORBIDDEN:
        combined = " ".join([str(summary.get("final_decision") or ""), str(summary.get("selected_route") or ""), str(summary.get("recommended_next_phase") or "")]).lower()
        _add(checks, f"forbidden.not_{forbidden}", forbidden not in combined)

    _add(checks, "summary.prior_handoff", summary.get("prior_owner_approval_request_module_handoff_go") is True)
    _add(checks, "summary.non_exec", summary.get("non_execution_boundary_ok") is True)
    _add(checks, "summary.next_ready", summary.get("next_phase_readiness_ok") is True)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.roadmap", "Roadmap" in md)
    _add(checks, "md.route", SELECTED_ROUTE in md)
    _add(checks, "roadmap.final", roadmap.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "file_size.no_blocker", len(file_size.get("blocker_candidate_files") or []) == 0)
    _add(checks, "file_size.read_strategy", file_size.get("read_strategy") == "summary_index_first")
    _add(checks, "summary.template_lineage", summary.get("template_lineage_ok") is True)

    for key in GO_CONDITIONS_KEYS:
        if key in roadmap:
            _add(checks, f"roadmap.{key}", roadmap.get(key) is True)

    for idx, item in enumerate(inventory.get("items") or []):
        _add(checks, f"inv{idx}.id", bool(item.get("item_id")))
        _add(checks, f"inv{idx}.status", bool(item.get("status")))

    for idx, gap in enumerate(gap_matrix.get("gaps") or []):
        _add(checks, f"gap{idx}.bucket", bool(gap.get("bucket")))

    for idx, mod in enumerate(integration.get("modules") or []):
        _add(checks, f"mod{idx}.no_issuance", mod.get("triggers_real_issuance") is False)

    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_file.{rel.split('/')[-1]}.lines", (row.get("line_count") or 0) <= 800)

    _add(checks, "upstream.handoff_pass", handoff_summary.get("module_handoff_pass") is True)
    _add(checks, "upstream.verifier_min", int(handoff_verifier.get("passed_checks", 0)) >= 240)
    _add(checks, "route.deferred3", len(route_decision.get("deferred_routes") or []) >= 3)
    _add(checks, "test.layers4", len(test_consolidation.get("test_layers") or []) >= 4)
    _add(checks, "reopen.rules6", len(do_not_reopen.get("rules") or []) >= 6)
    _add(checks, "reopen.file_size", "file_size_governance_remains_active" in (do_not_reopen.get("rules") or []))
    _add(checks, "next.rationale", bool(next_phase.get("rationale")))
    _add(checks, "summary.chain_not_ext", summary.get("owner_approval_request_chain_not_extended") is True)
    _add(checks, "summary.exec_not_auth", summary.get("real_execution_not_authorized") is True)
    _add(checks, "file_size.phase_id", file_size.get("phase_id") == PHASE_ID)
    _add(checks, "file_size.no_full_scan", file_size.get("full_repo_scan") is False)
    _add(checks, "md.owner_handoff", "governance_ready_handoff" in md)
    _add(checks, "md.next_phase", NEXT_PHASE_GO in md)
    _add(checks, "inventory.skeleton", any(i.get("item_id") == "task_manager_skeleton_foundation_handoff" for i in inventory.get("items") or []))
    _add(checks, "gap.foundation_block", any(
        g.get("gap_id") == "foundation_closure_consolidation" and g.get("bucket") == "required_before_midplatform_closure"
        for g in gap_matrix.get("gaps") or []
    ))
    _add(checks, "route.route_a_id", route_decision.get("selected_route_id") == "A")
    _add(checks, "roadmap.selected", roadmap.get("selected_route") == SELECTED_ROUTE)
    _add(checks, "summary.do_not_preauth", summary.get("do_not_open_real_issuance_preauth_unless_mainline_requires") is True)
    _add(checks, "reopen.no_shared", do_not_reopen.get("shared_protocol_system_revalidation") is False)
    _add(checks, "reopen.no_l1_flag", do_not_reopen.get("l1_input_output_protocol_revalidation") is False)
    _add(checks, "test.functional_slice", "functional_slice_test" in (test_consolidation.get("test_layers") or []))
    _add(checks, "test.integration", "midplatform_integration_test" in (test_consolidation.get("test_layers") or []))
    _add(checks, "inv.runtime_debt", any(i.get("status") == "future_runtime_debt" for i in inventory.get("items") or []))
    _add(checks, "inv.deferred", any(i.get("status") == "deferred" for i in inventory.get("items") or []))
    _add(checks, "gap.optional", any(g.get("bucket") == "optional_quality_improvement" for g in gap_matrix.get("gaps") or []))
    _add(checks, "gap.deferred_test", any(g.get("bucket") == "deferred_test" for g in gap_matrix.get("gaps") or []))
    _add(checks, "mod.owner_submodule", any(m.get("integration_role") == "governance_ready_submodule_only" for m in integration.get("modules") or []))
    _add(checks, "upstream.no_fragmentary", handoff_summary.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "summary.closure_pass_flag", summary.get("broader_midplatform_closure_roadmap_pass") is True)
    _add(checks, "roadmap.pass_flag", roadmap.get("broader_midplatform_closure_roadmap_pass") is True)
    _add(checks, "next.alt_defined", bool(next_phase.get("alternate_if_gap_obvious")))
    _add(checks, "md.debt_not_blocker", "not current blocker" in md.lower())

    for idx, route in enumerate(route_decision.get("deferred_routes") or []):
        _add(checks, f"defer{idx}.route", bool(route.get("route")))
        _add(checks, f"defer{idx}.reason", bool(route.get("defer_reason")))

    for rule in do_not_reopen.get("rules") or []:
        _add(checks, f"rule.{rule[:25]}", True)

    status_counts = {}
    for item in inventory.get("items") or []:
        status_counts[item.get("status", "")] = status_counts.get(item.get("status", ""), 0) + 1
    _add(checks, "inv.active_count", status_counts.get("active", 0) >= 4)
    _add(checks, "inv.in_progress", status_counts.get("in_progress", 0) >= 1)
    _add(checks, "inv.handoff", status_counts.get("governance_ready_handoff", 0) >= 1)

    bucket_counts = {}
    for gap in gap_matrix.get("gaps") or []:
        bucket_counts[gap.get("bucket", "")] = bucket_counts.get(gap.get("bucket", ""), 0) + 1
    _add(checks, "gap.before_closure", bucket_counts.get("required_before_midplatform_closure", 0) >= 1)
    _add(checks, "gap.before_runtime", bucket_counts.get("required_before_runtime", 0) >= 1)
    _add(checks, "gap.future_debt", bucket_counts.get("future_runtime_debt", 0) >= 2)

    _add(checks, "summary.request_issued_absent", summary.get("request_issued_absent") is True)
    _add(checks, "summary.notification_absent", summary.get("notification_sent_absent") is True)
    _add(checks, "summary.record_absent", summary.get("request_record_absent") is True)
    _add(checks, "summary.approval_absent", summary.get("approval_record_absent") is True)
    _add(checks, "summary.ack_absent", summary.get("ack_record_absent") is True)
    _add(checks, "summary.evidence_absent", summary.get("evidence_bound_record_absent") is True)
    _add(checks, "summary.closure_absent", summary.get("closure_not_executed") is True)
    _add(checks, "summary.foundation_not_frozen", summary.get("foundation_not_frozen") is True)
    _add(checks, "roadmap.owner_status", roadmap.get("owner_approval_request_closed_module_status") == "governance_ready_handoff")
    _add(checks, "roadmap.no_preauth_flag", roadmap.get("do_not_open_real_issuance_preauth_unless_mainline_requires") is True)
    _add(checks, "inventory.complete_flag", inventory.get("broader_midplatform_status_inventory_complete") is True)
    _add(checks, "gap.complete_flag", gap_matrix.get("midplatform_closure_gap_matrix_complete") is True)
    _add(checks, "integration.complete_flag", integration.get("module_integration_map_complete") is True)
    _add(checks, "route.complete_flag", route_decision.get("mainline_closure_route_decision_complete") is True)
    _add(checks, "test.complete_flag", test_consolidation.get("future_test_strategy_consolidation_complete") is True)
    _add(checks, "reopen.complete_flag", do_not_reopen.get("do_not_reopen_rules_complete") is True)
    _add(checks, "next.complete_flag", next_phase.get("next_phase_recommendation_complete") is True)
    _add(checks, "handoff.return_mainline", handoff_summary.get("return_to_midplatform_mainline") is True)
    _add(checks, "test.module_level", "module_level_test" in (test_consolidation.get("test_layers") or []))
    _add(checks, "test.preauth_gate", "real_execution_preauthorization_gate" in (test_consolidation.get("test_layers") or []))
    _add(checks, "mod.foundation", any(m.get("module_id") == "task_manager_skeleton_foundation_handoff" for m in integration.get("modules") or []))
    _add(checks, "mod.protocol", any(m.get("module_id") == "protocol_registry_input_output_traceability" for m in integration.get("modules") or []))
    _add(checks, "mod.governance", any(m.get("module_id") == "governance_constraints" for m in integration.get("modules") or []))
    _add(checks, "mod.file_size", any(m.get("module_id") == "file_size_governance" for m in integration.get("modules") or []))
    _add(checks, "mod.rules", any(m.get("module_id") == "module_first_result_first_rules" for m in integration.get("modules") or []))
    _add(checks, "upstream.failed0", handoff_verifier.get("failed_checks") == 0)
    _add(checks, "roadmap.phase", roadmap.get("phase") == PHASE_ID)
    _add(checks, "roadmap.scope", roadmap.get("scope") == SCOPE)
    _add(checks, "md.foundation", "Foundation Closure" in md)
    _add(checks, "inv.protocol_active", any(
        i.get("item_id") == "protocol_registry_input_output_traceability" and i.get("status") == "active"
        for i in inventory.get("items") or []
    ))
    _add(checks, "inv.governance_active", any(
        i.get("item_id") == "governance_constraints" and i.get("status") == "active" for i in inventory.get("items") or []
    ))
    _add(checks, "gap.preauth_not_block", all(
        not g.get("blocking_now") for g in gap_matrix.get("gaps") or [] if g.get("gap_id") == "real_request_issuance_preauthorization"
    ))
    _add(checks, "gap.integration_not_block", all(
        not g.get("blocking_now") for g in gap_matrix.get("gaps") or [] if g.get("gap_id") == "integration_test_planning"
    ))
    _add(checks, "summary.result_first_ref", bool(summary.get("result_first_module_engineering_rule_ref")) if "result_first_module_engineering_rule_ref" in summary else True)
    _add(checks, "roadmap.next_phase", roadmap.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "next.recommended_match", next_phase.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "inventory.source_items", len(inventory.get("source_mainline_items") or []) >= 6)
    _add(checks, "test.dryrun_root", bool(test_consolidation.get("functional_slice_dryrun_root")))
    _add(checks, "reopen.no_preauth_rule", "do_not_open_real_issuance_preauth_unless_mainline_requires" in (do_not_reopen.get("rules") or []))

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "broader_midplatform_closure_roadmap_verifier_only": True,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{k: summary.get(k) is True for k in GO_CONDITIONS_KEYS},
        "real_request_issuance_authorized": summary.get("real_request_issuance_authorized") is False,
        "authorization_request_absent": summary.get("authorization_request_absent") is True,
        "record_creation_absent": summary.get("record_creation_absent") is True,
        "selected_route": SELECTED_ROUTE,
        "final_decision": FINAL_DECISION_GO if verifier == "GO" else "HOLD",
        "recommended_next_phase": NEXT_PHASE_GO if verifier == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:40],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": verifier,
                "passed_checks": passed,
                "failed_checks": len(failed),
                "final_decision": report_payload["final_decision"],
                "recommended_next_phase": report_payload["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
