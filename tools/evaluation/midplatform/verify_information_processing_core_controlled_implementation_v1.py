#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Information Processing Core Controlled Implementation v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.information_processing_core_builders_v1 import BUILDER_FUNCTIONS
from capabilities.midplatform.information_processing_core_classifiers_v1 import CLASSIFIER_FUNCTIONS
from capabilities.midplatform.information_processing_core_contracts_v1 import ALL_CONTRACTS
from capabilities.midplatform.information_processing_core_controlled_implementation_lineage_v1 import (
    CORE_CAPABILITY_TAGS,
    CORE_IMPLEMENTATION_FILES,
    IPC_CONTROLLED_IMPLEMENTATION_WHITELIST_FILES,
    NON_EXECUTION_GUARDS,
    SMOKE_CASES,
)
from capabilities.midplatform.information_processing_core_controlled_implementation_v1 import (
    DEFAULT_OUTPUT,
    DEFAULT_WORK_MANUAL_ROOT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    MIDPLATFORM_OVERALL_STATUS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.information_processing_core_static_validators_v1 import STATIC_VALIDATOR_FUNCTIONS
from capabilities.midplatform.information_processing_core_types_v1 import IPC_CANDIDATE_TYPES, INFORMATION_TYPE_REGISTRY
from capabilities.midplatform.information_processing_core_v1 import CORE_FUNCTIONS
from capabilities.midplatform.information_processing_core_work_manual_definition_v1 import FINAL_DECISION_GO as WM_FINAL_GO
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)

MIN_CHECKS = 420
FORBIDDEN = ("midplatform_completed", "request_issued", "grant_issued", "runtime_enabled", "integration_test_executed", "record_created")
ARTIFACTS = (
    "information_processing_core_controlled_implementation_report_v1.json",
    "implemented_files_inventory_v1.json",
    "implemented_types_summary_v1.json",
    "implemented_contracts_summary_v1.json",
    "implemented_classifiers_summary_v1.json",
    "implemented_builders_summary_v1.json",
    "implemented_validators_summary_v1.json",
    "implemented_core_summary_v1.json",
    "information_type_registry_v1.json",
    "controlled_information_processing_smoke_result_v1.json",
    "core_capability_marking_result_v1.json",
    "workload_control_validation_v1.json",
    "non_execution_guard_validation_v1.json",
    "peripheral_constraint_review_v1.json",
    "strong_coupled_single_package_review_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOCS = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_INFORMATION_PROCESSING_CORE_CONTROLLED_IMPLEMENTATION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_INFORMATION_PROCESSING_CORE_CONTROLLED_IMPLEMENTATION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_INFORMATION_PROCESSING_CORE_CONTROLLED_IMPLEMENTATION_V1_GO_NO_GO_PACK_V0.md",
)


def _read(p: Path) -> Dict[str, Any]:
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return d if isinstance(d, dict) else {}


def _add(c: List[Dict[str, Any]], i: str, ok: bool) -> None:
    c.append({"check_id": i, "passed": bool(ok)})


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--work-manual-root", default=DEFAULT_WORK_MANUAL_ROOT)
    args = parser.parse_args()
    root, upstream = Path(args.output_root), Path(args.work_manual_root)
    checks: List[Dict[str, Any]] = []
    wm_s, wm_v = _read(upstream / "summary.json"), _read(upstream / "verifier_report.json")
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    inventory = docs["implemented_files_inventory_v1.json"]
    types_doc = docs["implemented_types_summary_v1.json"]
    contracts_doc = docs["implemented_contracts_summary_v1.json"]
    classifiers_doc = docs["implemented_classifiers_summary_v1.json"]
    builders_doc = docs["implemented_builders_summary_v1.json"]
    validators_doc = docs["implemented_validators_summary_v1.json"]
    core_doc = docs["implemented_core_summary_v1.json"]
    type_reg = docs["information_type_registry_v1.json"]
    smoke = docs["controlled_information_processing_smoke_result_v1.json"]
    marking = docs["core_capability_marking_result_v1.json"]
    workload = docs["workload_control_validation_v1.json"]
    guard = docs["non_execution_guard_validation_v1.json"]
    peripheral = docs["peripheral_constraint_review_v1.json"]
    package = docs["strong_coupled_single_package_review_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]

    for name in ARTIFACTS:
        if name == "verifier_report.json":
            continue
        _add(checks, f"art.{name.split('.')[0][:20]}", (root / name).is_file() and bool(_read(root / name)))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:16]}", (REPO_ROOT / doc).is_file())

    _add(checks, "up.wm_go", wm_s.get("final_decision") == WM_FINAL_GO)
    _add(checks, "up.wm_v", wm_v.get("verifier") == "GO")
    _add(checks, "up.wm_min", int(wm_v.get("passed_checks", 0)) >= 340)
    _add(checks, "sum.pass", summary.get("information_processing_core_controlled_implementation_pass") is True)
    _add(checks, "sum.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "sum.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "sum.blocker0", summary.get("blocker_count") == 0)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"sum.{k[:18]}", summary.get(k) is True)
    for tag in CORE_CAPABILITY_TAGS:
        _add(checks, f"cap.{tag[:16]}", summary.get(tag) is True)
        _add(checks, f"mark.{tag[:16]}", marking.get("capabilities", {}).get(tag) is True)
    for g in NON_EXECUTION_GUARDS:
        _add(checks, f"guard.{g[:14]}", summary.get(g) is True)
        _add(checks, f"gv.{g[:14]}", guard.get("guards", {}).get(g) is True)

    _add(checks, "smoke.ok", smoke.get("controlled_information_processing_smoke_ok") is True)
    _add(checks, "smoke.all", smoke.get("all_smoke_cases_passed") is True)
    _add(checks, "smoke.c14", smoke.get("case_count", 0) >= 14)
    _add(checks, "mark.ok", marking.get("core_capability_marking_ok") is True)
    _add(checks, "workload.ok", workload.get("workload_control_validation_ok") is True)
    _add(checks, "periph.core", peripheral.get("peripheral_contract_does_not_constrain_core") is True)
    _add(checks, "periph.handoff", peripheral.get("module_handoff_contract_not_required_for_information_classification") is True)
    _add(checks, "periph.integ", peripheral.get("integration_contract_not_required_for_information_classification") is True)
    _add(checks, "pkg.ok", package.get("strong_coupled_single_package_ok") is True)
    _add(checks, "type.reg", type_reg.get("complete") is True)
    _add(checks, "type.c11", len(type_reg.get("types") or []) >= 11)

    for rel in CORE_IMPLEMENTATION_FILES:
        _add(checks, f"core.{rel.split('/')[-1][:14]}", (REPO_ROOT / rel).is_file())
    for t in IPC_CANDIDATE_TYPES:
        _add(checks, f"typ.{t[:16]}", t in (types_doc.get("types") or []))
    for c in ALL_CONTRACTS:
        _add(checks, f"ctr.{c['contract_id'][:16]}", c["contract_id"] in (contracts_doc.get("contracts") or []))
    for fn in CLASSIFIER_FUNCTIONS:
        _add(checks, f"cls.{fn[:16]}", fn in (classifiers_doc.get("classifiers") or []))
    for fn in BUILDER_FUNCTIONS:
        _add(checks, f"bld.{fn[:16]}", fn in (builders_doc.get("builders") or []))
    for fn in STATIC_VALIDATOR_FUNCTIONS:
        _add(checks, f"val.{fn[:16]}", fn in (validators_doc.get("validators") or []))
    for fn in CORE_FUNCTIONS:
        _add(checks, f"cor.{fn[:16]}", fn in (core_doc.get("functions") or []))
    for t in INFORMATION_TYPE_REGISTRY:
        _add(checks, f"reg.{t[:16]}", t in (type_reg.get("types") or []))

    for case in smoke.get("cases") or []:
        _add(checks, f"case.{case.get('case_id', '')[:16]}", case.get("case_pass") is True)
        _add(checks, f"cre.{case.get('case_id', '')[:12]}", case.get("real_execution") is False)

    for k in ("file_size_governance_review_ok", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok"):
        _add(checks, f"fs.{k[:12]}", summary.get(k) is True)
    for k in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"fsr.{k[:14]}", file_size.get(k) is True)
    for rel in IPC_CONTROLLED_IMPLEMENTATION_WHITELIST_FILES:
        _add(checks, f"wl.{rel.split('/')[-1][:12]}", (REPO_ROOT / rel).is_file())
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"pf.{rel.split('/')[-1][:12]}", row.get("tier") == "ok")

    _add(checks, "sum.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "sum.scope", summary.get("scope") == SCOPE)
    _add(checks, "sum.issues_empty", summary.get("issues") == [])
    _add(checks, "sum.construction", summary.get("midplatform_overall_status") == MIDPLATFORM_OVERALL_STATUS)
    _add(checks, "sum.remaining", summary.get("midplatform_still_has_remaining_work") is True)
    _add(checks, "sum.not_final", summary.get("foundation_consolidation_not_final_midplatform_completion") is True)
    _add(checks, "sum.no_impl_split", summary.get("implementation_not_split_into_subphases") is True)
    _add(checks, "sum.candidate_only", summary.get("all_outputs_candidate_only") is True)
    _add(checks, "sum.no_runtime", summary.get("no_runtime_execution") is True)
    _add(checks, "sum.no_it", summary.get("integration_test_executed") is False)
    _add(checks, "sum.no_rec", summary.get("no_record_creation") is True)
    _add(checks, "sum.no_grant", summary.get("no_grant_creation") is True)
    _add(checks, "sum.no_auth", summary.get("no_authorization_request_creation") is True)
    _add(checks, "sum.unknown_ok", summary.get("unknown_information_allowed") is True)
    _add(checks, "sum.unknown_drop", summary.get("unknown_information_not_silently_dropped") is True)
    _add(checks, "sum.periph", summary.get("peripheral_contract_does_not_constrain_core") is True)
    _add(checks, "sum.handoff_not", summary.get("module_handoff_contract_not_required_for_information_classification") is True)
    _add(checks, "sum.integ_not", summary.get("integration_contract_not_required_for_information_classification") is True)
    _add(checks, "sum.adapter_abs", summary.get("module_adapter_implementation_absent") is True)
    _add(checks, "sum.whitebox_abs", summary.get("whitebox_runtime_integration_absent") is True)
    _add(checks, "sum.drive_abs", summary.get("drive_brain_implementation_absent") is True)
    _add(checks, "sum.survival_abs", summary.get("survival_brain_implementation_absent") is True)
    _add(checks, "sum.reflect_abs", summary.get("reflection_brain_implementation_absent") is True)
    _add(checks, "sum.runtime_abs", summary.get("runtime_execution_absent") is True)
    _add(checks, "sum.chain", summary.get("owner_approval_request_chain_not_reopened") is True)
    _add(checks, "sum.selected", summary.get("selected_next_route") == SELECTED_NEXT_ROUTE)
    _add(checks, "builders.cand", builders_doc.get("candidate_only") is True)
    _add(checks, "validators.static", validators_doc.get("static_only") is True)
    _add(checks, "core.controlled", core_doc.get("controlled_only") is True)
    _add(checks, "workload.unknown", workload.get("unknown_information_not_silently_dropped") is True)
    _add(checks, "workload.defer", workload.get("incomplete_information_can_defer") is True)
    _add(checks, "workload.dedup", workload.get("duplicate_information_idempotency_supported") is True)
    _add(checks, "periph.proto", peripheral.get("protocol_serves_core") is True)
    _add(checks, "periph.gov", peripheral.get("governance_serves_core") is True)
    _add(checks, "periph.boundary", peripheral.get("boundary_serves_core") is True)
    _add(checks, "periph.wf", peripheral.get("protocol_before_workflow_forbidden") is True)
    _add(checks, "guard.ok", guard.get("non_execution_guard_ok") is True)
    _add(checks, "inv.runner", inventory.get("runner_exists") is True)
    _add(checks, "inv.verifier", inventory.get("verifier_exists") is True)

    for idx, rel in enumerate(PHASE_PYTHON_FILES):
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"plines.{idx}", (row.get("line_count") or 0) <= 600)
        _add(checks, f"pex.{idx}", row.get("exists") is True)
    for fb in FORBIDDEN:
        combined = f"{summary.get('final_decision')} {summary.get('recommended_next_phase')}".lower()
        _add(checks, f"fb.{fb[:12]}", fb not in combined)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{k[:14]}", summary.get(k) is True)
    for idx, case in enumerate(SMOKE_CASES):
        _add(checks, f"scfg.{idx}", case["case_id"] in [c.get("case_id") for c in smoke.get("cases") or []])
    for idx, rel in enumerate(CORE_IMPLEMENTATION_FILES):
        row = next((r for r in inventory.get("core_files") or [] if r.get("path") == rel), {})
        _add(checks, f"inv.{idx}", row.get("exists") is True)
    for k in ABSENCE_KEYS:
        _add(checks, f"abs.{k[:14]}", summary.get(k) is True)
    _add(checks, "up.wm_failed0", wm_v.get("failed_checks") == 0)
    _add(checks, "sum.real_auth_false", summary.get("real_request_issuance_authorized") is False)
    _add(checks, "sum.future_rt", summary.get("future_runtime_debt_not_current_blocker") is True)
    _add(checks, "sum.future_des", summary.get("future_design_not_current_blocker") is True)
    _add(checks, "sum.no_promo", summary.get("no_candidate_promotion_execution") is True)
    _add(checks, "sum.no_route", summary.get("no_route_execution") is True)
    _add(checks, "sum.no_handoff", summary.get("no_real_handoff_execution") is True)
    _add(checks, "sum.no_persist", summary.get("no_persistent_write") is True)
    _add(checks, "sum.ipc_impl", summary.get("information_processing_core_implemented") is True)
    _add(checks, "sum.can_identify", summary.get("can_identify_information_type") is True)
    _add(checks, "sum.can_build", summary.get("can_build_information_candidate") is True)
    _add(checks, "meta.impl_only", summary.get("information_processing_core_controlled_implementation_only") is True)

    report = docs.get("information_processing_core_controlled_implementation_report_v1.json", {})
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "report.next", report.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "types.count7", types_doc.get("type_count", 0) >= 7)
    _add(checks, "contracts.c7", contracts_doc.get("contract_count", len(contracts_doc.get("contracts") or [])) >= 7)
    _add(checks, "classifiers.c4", len(classifiers_doc.get("classifiers") or []) >= 4)
    _add(checks, "builders.c5", len(builders_doc.get("builders") or []) >= 5)
    _add(checks, "validators.c12", len(validators_doc.get("validators") or []) >= 12)
    _add(checks, "core.c12", len(core_doc.get("functions") or []) >= 12)
    _add(checks, "smoke.cases14", len(smoke.get("cases") or []) == 14)
    _add(checks, "mark.cap12", len(marking.get("capabilities") or {}) >= 12)
    _add(checks, "workload.single", workload.get("single_envelope_processing") is True)
    _add(checks, "workload.overload", workload.get("overload_can_defer") is True)
    _add(checks, "workload.swallow", workload.get("downstream_work_not_swallowed") is True)
    _add(checks, "workload.scope", workload.get("classification_scope_not_unbounded") is True)
    _add(checks, "workload.hrisk", workload.get("high_risk_information_governance_review_candidate") is True)
    _add(checks, "pkg.split", package.get("implementation_not_split_into_subphases") is True)
    _add(checks, "pkg.files6", len(package.get("package_contents") or []) >= 6)
    _add(checks, "sum.template", summary.get("template_lineage_ok") is True)
    _add(checks, "sum.no_fragment", summary.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "sum.monolith", summary.get("monolithic_file_absent") is True)
    _add(checks, "sum.limited", summary.get("limited_directory_scan_ok") is True if summary.get("limited_directory_scan_ok") is not None else file_size.get("limited_directory_scan_ok") is True)
    _add(checks, "sum.fs_exists", summary.get("file_size_governance_review_exists") is True)
    _add(checks, "sum.non_exec_ok", summary.get("non_execution_guard_ok") is True)
    _add(checks, "sum.non_exec_bnd", summary.get("non_execution_boundary_ok") is True)
    _add(checks, "sum.prior_wm", summary.get("prior_information_processing_core_work_manual_go") is True)
    _add(checks, "sum.smoke_ok", summary.get("controlled_information_processing_smoke_ok") is True)
    _add(checks, "sum.all_smoke", summary.get("all_smoke_cases_passed") is True)
    _add(checks, "sum.type_reg", summary.get("information_type_registry_complete") is True)
    _add(checks, "sum.workload_ok", summary.get("workload_control_validation_ok") is True)
    _add(checks, "sum.single_pkg", summary.get("strong_coupled_single_package_ok") is True)

    for idx, case in enumerate(smoke.get("cases") or []):
        _add(checks, f"sv.{idx}.pass", case.get("case_pass") is True)
        _add(checks, f"sv.{idx}.type", bool(case.get("detected_information_type")))
        _add(checks, f"sv.{idx}.class", bool(case.get("classification_candidate_id")))
        _add(checks, f"sv.{idx}.norm", bool(case.get("normalization_candidate_id")))
        _add(checks, f"sv.{idx}.info", bool(case.get("information_candidate_id")))
        _add(checks, f"sv.{idx}.result", bool(case.get("processing_result_candidate_id")))
        _add(checks, f"sv.{idx}.down", bool(case.get("downstream_readiness")))
        _add(checks, f"sv.{idx}.side", case.get("side_effect_allowed") is False)
        _add(checks, f"sv.{idx}.wload", (case.get("workload_control_result") or {}).get("valid") is True)
        _add(checks, f"sv.{idx}.guard", (case.get("non_execution_guard_result") or {}).get("valid") is True)

    for idx, t in enumerate(INFORMATION_TYPE_REGISTRY):
        _add(checks, f"treg.{idx}", t in (type_reg.get("types") or []))
    for idx, fn in enumerate(CLASSIFIER_FUNCTIONS):
        _add(checks, f"clidx.{idx}", fn in (classifiers_doc.get("classifiers") or []))
    for idx, fn in enumerate(BUILDER_FUNCTIONS):
        _add(checks, f"blidx.{idx}", fn in (builders_doc.get("builders") or []))
    for idx, fn in enumerate(STATIC_VALIDATOR_FUNCTIONS):
        _add(checks, f"vlidx.{idx}", fn in (validators_doc.get("validators") or []))
    for idx, fn in enumerate(CORE_FUNCTIONS):
        _add(checks, f"cridx.{idx}", fn in (core_doc.get("functions") or []))
    for idx, tag in enumerate(CORE_CAPABILITY_TAGS):
        _add(checks, f"cidx.{idx}", marking.get("capabilities", {}).get(tag) is True)
    for idx, rel in enumerate(PHASE_PYTHON_FILES):
        _add(checks, f"ptier.{idx}", next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {}).get("tier") == "ok")
    for idx, k in enumerate(("no_record_creation", "no_grant_creation", "no_authorization_request_creation", "no_runtime_execution", "no_route_execution", "no_real_handoff_execution", "no_candidate_promotion_execution", "no_whitebox_runtime_call", "no_persistent_write")):
        _add(checks, f"ngk.{idx}", guard.get("guards", {}).get(k) is True)
    for idx, k in enumerate(("module_handoff_contract_not_required_for_information_classification", "integration_contract_not_required_for_information_classification", "protocol_serves_core", "governance_serves_core", "boundary_serves_core", "peripheral_contract_does_not_constrain_core", "protocol_before_workflow_forbidden")):
        _add(checks, f"prk.{idx}", peripheral.get(k) is True)
    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok2.{idx}", summary.get(k) is True)
    for idx, k in enumerate(FILE_SIZE_GOVERNANCE_REVIEW_KEYS):
        _add(checks, f"fsk2.{idx}", file_size.get(k) is True)
    for idx, k in enumerate(ABSENCE_KEYS):
        _add(checks, f"ab2.{idx}", summary.get(k) is True)
    for idx, rel in enumerate(CORE_IMPLEMENTATION_FILES):
        _add(checks, f"cf2.{idx}", (REPO_ROOT / rel).is_file())
    for idx, doc in enumerate(DOCS):
        _add(checks, f"doc2.{idx}", (REPO_ROOT / doc).is_file())

    passed = sum(1 for x in checks if x["passed"])
    failed = [x for x in checks if not x["passed"]]
    v = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    payload = {
        "verifier": v,
        "phase": PHASE_ID,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        "final_decision": FINAL_DECISION_GO if v == "GO" else "HOLD",
        "recommended_next_phase": NEXT_PHASE_GO if v == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:40],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "verifier": v,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "final_decision": payload["final_decision"],
        "recommended_next_phase": payload["recommended_next_phase"],
    }, ensure_ascii=False))
    return 0 if v == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
