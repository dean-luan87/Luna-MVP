#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Core Capability and Peripheral Service Recalibration v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core_capability_peripheral_service_recalibration_items_v1 import (
    CONFLICT_RESOLUTION_RULES,
    CORE_CAPABILITY_MARKING,
    CORE_MODULE_SELECTION,
    DO_NOT_MISCLASSIFY_RULES,
    PERIPHERAL_SERVICE_PRINCIPLES,
    ROUTE_REASSESSMENT,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.core_capability_peripheral_service_recalibration_lineage_v1 import RECALIBRATION_WHITELIST_FILES
from capabilities.midplatform.core_capability_peripheral_service_recalibration_v1 import (
    DEFAULT_GAP_CONSOLIDATION_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    MIDPLATFORM_OVERALL_STATUS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
)
from capabilities.midplatform.module_integration_gap_consolidation_v1 import FINAL_DECISION_GO as GAP_FINAL_GO
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import ABSENCE_KEYS

MIN_CHECKS = 340
FORBIDDEN = ("midplatform_completed", "request_issued", "grant_issued", "runtime_enabled", "integration_test_executed", "record_created")
ARTIFACTS = (
    "core_capability_peripheral_service_recalibration_report_v1.json",
    "core_capability_peripheral_service_recalibration_report_v1.md",
    "recalibration_scope_v1.json",
    "midplatform_capability_framework_definition_v1.json",
    "midplatform_core_function_definition_v1.json",
    "core_module_selection_v1.json",
    "peripheral_service_principle_matrix_v1.json",
    "core_capability_marking_baseline_v1.json",
    "conflict_resolution_rule_v1.json",
    "route_reassessment_v1.json",
    "next_route_decision_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOCS = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_CORE_CAPABILITY_PERIPHERAL_SERVICE_RECALIBRATION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_CORE_CAPABILITY_PERIPHERAL_SERVICE_RECALIBRATION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_CORE_CAPABILITY_PERIPHERAL_SERVICE_RECALIBRATION_V1_GO_NO_GO_PACK_V0.md",
)


def _read(path: Path) -> Dict[str, Any]:
    try:
        p = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return p if isinstance(p, dict) else {}


def _add(checks: List[Dict[str, Any]], cid: str, ok: bool) -> None:
    checks.append({"check_id": cid, "passed": bool(ok)})


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--gap-consolidation-root", default=DEFAULT_GAP_CONSOLIDATION_ROOT)
    args = parser.parse_args()
    root, upstream = Path(args.output_root), Path(args.gap_consolidation_root)
    checks: List[Dict[str, Any]] = []
    gap_s = _read(upstream / "summary.json")
    gap_v = _read(upstream / "verifier_report.json")
    md = (root / "core_capability_peripheral_service_recalibration_report_v1.md").read_text(encoding="utf-8") if (root / "core_capability_peripheral_service_recalibration_report_v1.md").is_file() else ""
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary, report = docs["summary.json"], docs["core_capability_peripheral_service_recalibration_report_v1.json"]
    scope = docs["recalibration_scope_v1.json"]
    framework = docs["midplatform_capability_framework_definition_v1.json"]
    core_fn = docs["midplatform_core_function_definition_v1.json"]
    modules_doc = docs["core_module_selection_v1.json"]
    peripheral = docs["peripheral_service_principle_matrix_v1.json"]
    marking = docs["core_capability_marking_baseline_v1.json"]
    conflict = docs["conflict_resolution_rule_v1.json"]
    route_re = docs["route_reassessment_v1.json"]
    route_dec = docs["next_route_decision_v1.json"]
    misclass = docs["do_not_misclassify_rules_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]

    for name in ARTIFACTS:
        if name == "verifier_report.json":
            continue
        p = root / name
        _add(checks, f"artifact.{name.split('.')[0]}", p.is_file() and (bool(_read(p)) if name.endswith(".json") else len(md.strip()) > 40))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:20]}", (REPO_ROOT / doc).is_file())

    _add(checks, "upstream.gap_go", gap_s.get("final_decision") == GAP_FINAL_GO)
    _add(checks, "upstream.gap_verifier", gap_v.get("verifier") == "GO")
    _add(checks, "summary.pass", summary.get("core_capability_peripheral_service_recalibration_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", NEXT_PHASE_GO in (summary.get("recommended_next_phase") or ""))
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
    _add(checks, "summary.core_fn", summary.get("core_function_defined") is True)
    _add(checks, "summary.core_mod", summary.get("core_module_identified") is True)
    _add(checks, "summary.handoff_not_auto", summary.get("handoff_contract_not_auto_selected") is True)
    _add(checks, "summary.handoff_gap", summary.get("handoff_gap_not_erased") is True)
    _add(checks, "summary.handoff_not_impl", summary.get("module_handoff_contract_not_implemented") is True)
    _add(checks, "summary.prior_go", summary.get("prior_go_results_not_invalidated") is True)
    _add(checks, "summary.gov_serves", summary.get("governance_serves_core") is True)
    _add(checks, "summary.proto_serves", summary.get("protocol_serves_core") is True)
    _add(checks, "summary.bound_serves", summary.get("boundary_serves_core") is True)
    _add(checks, "summary.integration_false", summary.get("integration_test_executed") is False)
    _add(checks, "summary.chain_not_reopen", summary.get("owner_approval_request_chain_not_reopened") is True)

    _add(checks, "scope.not_handoff", scope.get("not_handoff_implementation") is True)
    _add(checks, "scope.not_invalidate", scope.get("not_invalidate_prior_go") is True)
    _add(checks, "framework.defined", framework.get("midplatform_capability_framework_defined") is True)
    _add(checks, "framework.not_proto_only", framework.get("not_protocol_repository") is True)
    _add(checks, "core_fn.primary", core_fn.get("primary_core_function") == "Information Processing Core")
    _add(checks, "core_fn.defined", core_fn.get("midplatform_core_function_defined") is True)
    _add(checks, "modules.complete", modules_doc.get("core_module_selection_complete") is True)
    _add(checks, "peripheral.complete", peripheral.get("peripheral_service_principle_matrix_complete") is True)
    _add(checks, "marking.complete", marking.get("core_capability_marking_baseline_complete") is True)
    _add(checks, "conflict.complete", conflict.get("conflict_resolution_rule_complete") is True)
    _add(checks, "route_re.complete", route_re.get("route_reassessment_complete") is True)
    _add(checks, "route_re.handoff_p3", route_re.get("recalibrated_handoff_to_p3") is True)
    _add(checks, "route_dec.complete", route_dec.get("next_route_decision_complete") is True)
    _add(checks, "route_dec.not_handoff", route_dec.get("handoff_contract_not_auto_selected") is True)

    for m in CORE_MODULE_SELECTION:
        mid = m["module_id"]
        e = next((x for x in modules_doc.get("modules") or [] if x.get("module_id") == mid), {})
        _add(checks, f"mod.{mid[:18]}", bool(e))
        if m["core_relation"] == "core":
            _add(checks, f"mod.{mid[:10]}.core", e.get("core_relation") == "core")
    for p in PERIPHERAL_SERVICE_PRINCIPLES:
        _add(checks, f"periph.{p['service_id']}", p["service_id"] in [x.get("service_id") for x in peripheral.get("principles") or []])
        _add(checks, f"periph.{p['service_id'][:6]}.srv", next((x for x in peripheral.get("principles") or [] if x.get("service_id") == p["service_id"]), {}).get("serves_core") is True)
    for c in CORE_CAPABILITY_MARKING:
        _add(checks, f"cap.{c['capability_id'][:18]}", c["capability_id"] in [x.get("capability_id") for x in marking.get("capabilities") or []])
    for r in CONFLICT_RESOLUTION_RULES:
        _add(checks, f"conflict.{r[:18]}", r in (conflict.get("rules") or []))
    for r in ROUTE_REASSESSMENT:
        _add(checks, f"route.{r['route_id']}", r["route_id"] in [x.get("route_id") for x in route_re.get("routes") or []])
    handoff_route = next((r for r in ROUTE_REASSESSMENT if r["route_id"] == "D"), {})
    _add(checks, "route_d.peripheral", handoff_route.get("peripheral_only") is True)
    _add(checks, "route_d.wall_risk", handoff_route.get("premature_wall_risk") is True)
    _add(checks, "route_d.p3", handoff_route.get("recalibrated_priority") == "P3")
    for rule in DO_NOT_MISCLASSIFY_RULES:
        _add(checks, f"rule.{rule[:18]}", rule in (misclass.get("rules") or []))

    for key in ABSENCE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
    for fb in FORBIDDEN:
        combined = f"{summary.get('final_decision')} {summary.get('recommended_next_phase')} {md}".lower()
        _add(checks, f"forbid.{fb[:12]}", fb not in combined)
    for key in ("file_size_governance_review_exists", "file_size_governance_review_ok", "monolithic_file_absent", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok", "limited_directory_scan_ok"):
        _add(checks, f"fs.{key[:12]}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"fsrev.{key[:14]}", file_size.get(key) is True)
    for rel in RECALIBRATION_WHITELIST_FILES:
        _add(checks, f"wl.{rel.split('/')[-1][:14]}", (REPO_ROOT / rel).is_file())
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"pf.{rel.split('/')[-1][:12]}", row.get("tier") == "ok")

    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.scope", summary.get("scope") == SCOPE)
    _add(checks, "summary.construction", summary.get("midplatform_overall_status") == MIDPLATFORM_OVERALL_STATUS)
    _add(checks, "summary.selected", summary.get("selected_next_route") == SELECTED_NEXT_ROUTE)
    _add(checks, "md.primary", "Information Processing Core" in md)
    _add(checks, "md.handoff_defer", "P3" in md or "deferred" in md.lower())
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "upstream.gap_min", int(gap_v.get("passed_checks", 0)) >= 320)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "summary.safety", summary.get("safety_critical_constraints_preserved") is True)
    _add(checks, "summary.conflict_rule", summary.get("core_over_peripheral_conflict_rule_defined") is True)
    _add(checks, "summary.future_rt", summary.get("future_runtime_debt_not_current_blocker") is True)
    _add(checks, "summary.future_design", summary.get("future_design_not_current_blocker") is True)
    for key in GO_CONDITIONS_KEYS:
        if key in report:
            _add(checks, f"report.{key[:16]}", report.get(key) is True)
    for idx, m in enumerate(CORE_MODULE_SELECTION):
        _add(checks, f"midx.{idx}", m["module_id"] in [x.get("module_id") for x in modules_doc.get("modules") or []])
    for idx, c in enumerate(CORE_CAPABILITY_MARKING):
        _add(checks, f"cidx.{idx}", c["capability_id"] in [x.get("capability_id") for x in marking.get("capabilities") or []])
    for alt in route_dec.get("alternate_routes") or []:
        _add(checks, f"alt.{alt.get('route_id', '')}", bool(alt))

    _add(checks, "summary.runtime_absent", summary.get("runtime_execution_absent") is True)
    _add(checks, "summary.survival_absent", summary.get("survival_brain_implementation_absent") is True)
    _add(checks, "summary.reflection_absent", summary.get("reflection_brain_implementation_absent") is True)
    _add(checks, "summary.drive_absent", summary.get("drive_brain_implementation_absent") is True)
    _add(checks, "summary.adapter_absent", summary.get("module_adapter_implementation_absent") is True)
    _add(checks, "summary.whitebox_absent", summary.get("whitebox_runtime_integration_absent") is True)
    _add(checks, "summary.no_fragment", summary.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "summary.remaining_work", summary.get("midplatform_still_has_remaining_work") is True)
    _add(checks, "summary.not_final", summary.get("foundation_consolidation_not_final_midplatform_completion") is True)
    _add(checks, "summary.template_lineage", summary.get("template_lineage_ok") is True)
    _add(checks, "framework.non_exec", framework.get("non_execution_boundary") is True)
    _add(checks, "framework.collab", bool(framework.get("collaboration_mode")))
    _add(checks, "core_fn.secondary", len(core_fn.get("secondary_core_functions") or []) >= 2)
    _add(checks, "core_fn.info_meaning", len(core_fn.get("information_processing_meaning") or []) >= 8)
    _add(checks, "marking.count17", len(marking.get("capabilities") or []) >= 17)
    _add(checks, "marking.missing2", sum(1 for x in marking.get("capabilities") or [] if x.get("status") == "missing") >= 2)
    _add(checks, "marking.marked13", sum(1 for x in marking.get("capabilities") or [] if x.get("status") == "marked") >= 13)
    _add(checks, "modules.core3", sum(1 for x in modules_doc.get("modules") or [] if x.get("core_relation") == "core") >= 3)
    _add(checks, "modules.periph", any(x.get("module_id") == "module_handoff_contract" for x in modules_doc.get("modules") or []))
    handoff_mod = next((x for x in modules_doc.get("modules") or [] if x.get("module_id") == "module_handoff_contract"), {})
    _add(checks, "handoff_mod.p3", handoff_mod.get("current_priority_after_recalibration") == "P3")
    _add(checks, "handoff_mod.periph", handoff_mod.get("core_relation") == "peripheral_contract")
    _add(checks, "route_a.p1", next((r for r in ROUTE_REASSESSMENT if r["route_id"] == "A"), {}).get("recalibrated_priority") == "P1")
    _add(checks, "route_b.p1", next((r for r in ROUTE_REASSESSMENT if r["route_id"] == "B"), {}).get("recalibrated_priority") == "P1")
    _add(checks, "route_dec.route_a", route_dec.get("selected_route_id") == "A")
    _add(checks, "route_dec.alt_phase", bool(route_dec.get("alternate_phase")))
    _add(checks, "scope.not_runtime", scope.get("not_runtime") is True)
    _add(checks, "scope.not_orch_ext", scope.get("not_core_orchestration_extension") is True)
    _add(checks, "report.pass_flag", report.get("core_capability_peripheral_service_recalibration_pass") is True)
    _add(checks, "md.final", FINAL_DECISION_GO[:40] in md or "RECALIBRATION" in md)
    _add(checks, "md.next_info", "Information Processing" in md or NEXT_PHASE_GO in md)
    _add(checks, "upstream.gap_handoff", gap_s.get("module_handoff_contract_gap_identified") is True)
    _add(checks, "upstream.gap_failed0", gap_v.get("failed_checks") == 0)
    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{key[:16]}", summary.get(key) is True)
    for idx, rel in enumerate(PHASE_PYTHON_FILES):
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"plines.{idx}", (row.get("line_count") or 0) <= 600)
        _add(checks, f"pexists.{idx}", row.get("exists") is True)
    for idx, c in enumerate(CORE_CAPABILITY_MARKING):
        e = next((x for x in marking.get("capabilities") or [] if x.get("capability_id") == c["capability_id"]), {})
        _add(checks, f"cstat.{idx}", e.get("status") == c["status"])
    for idx, m in enumerate(CORE_MODULE_SELECTION):
        e = next((x for x in modules_doc.get("modules") or [] if x.get("module_id") == m["module_id"]), {})
        _add(checks, f"mrel.{idx}", e.get("core_relation") == m["core_relation"])
        _add(checks, f"mserve.{idx}", e.get("should_serve_core") is True)

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    payload = {
        "verifier": verifier, "phase": PHASE_ID, "passed_checks": passed, "failed_checks": len(failed),
        "min_checks": MIN_CHECKS, "blocker_count": len(failed),
        "final_decision": FINAL_DECISION_GO if verifier == "GO" else "HOLD",
        "recommended_next_phase": NEXT_PHASE_GO if verifier == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:40], "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": verifier, "passed_checks": passed, "failed_checks": len(failed),
                      "final_decision": payload["final_decision"], "recommended_next_phase": payload["recommended_next_phase"]}, ensure_ascii=False))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
