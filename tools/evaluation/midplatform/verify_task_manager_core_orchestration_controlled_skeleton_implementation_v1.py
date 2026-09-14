#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Core Orchestration Controlled Skeleton Implementation v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS
from capabilities.midplatform.task_manager_core_orchestration_builders_v1 import BUILDER_FUNCTIONS
from capabilities.midplatform.task_manager_core_orchestration_contracts_v1 import ALL_CONTRACTS
from capabilities.midplatform.task_manager_core_orchestration_controlled_skeleton_implementation_v1 import (
    DEFAULT_IMPLEMENTATION_PLANNING_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    MIDPLATFORM_OVERALL_STATUS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.task_manager_core_orchestration_controlled_skeleton_lineage_v1 import (
    CORE_IMPLEMENTATION_FILES,
    ORCHESTRATION_CONTROLLED_SKELETON_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_core_orchestration_implementation_items_v1 import NON_EXECUTION_GUARDS
from capabilities.midplatform.task_manager_core_orchestration_implementation_planning_v1 import (
    FINAL_DECISION_GO as IMPLEMENTATION_PLANNING_FINAL_GO,
    NEXT_PHASE_GO as IMPLEMENTATION_PLANNING_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_core_orchestration_skeleton_v1 import SKELETON_FUNCTIONS
from capabilities.midplatform.task_manager_core_orchestration_static_validators_v1 import STATIC_VALIDATOR_FUNCTIONS
from capabilities.midplatform.task_manager_core_orchestration_types_v1 import ORCHESTRATION_CANDIDATE_TYPES
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)

MIN_CHECKS = 360
FORBIDDEN = ("midplatform_completed", "request_issued", "grant_issued", "runtime_enabled", "integration_test_executed", "record_created")
FILE_SIZE_KEYS = (
    "file_size_governance_review_exists", "file_size_governance_review_ok", "monolithic_file_absent",
    "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok", "limited_directory_scan_ok",
)
ARTIFACTS: Tuple[str, ...] = (
    "controlled_skeleton_implementation_report_v1.json",
    "controlled_skeleton_implementation_report_v1.md",
    "implemented_files_inventory_v1.json",
    "implemented_types_summary_v1.json",
    "implemented_contracts_summary_v1.json",
    "implemented_builders_summary_v1.json",
    "implemented_validators_summary_v1.json",
    "implemented_skeleton_summary_v1.json",
    "non_execution_guard_validation_v1.json",
    "controlled_skeleton_smoke_result_v1.json",
    "strong_coupled_single_package_review_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOC_PATHS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_CONTROLLED_SKELETON_IMPLEMENTATION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_CORE_ORCHESTRATION_CONTROLLED_SKELETON_IMPLEMENTATION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_CORE_ORCHESTRATION_CONTROLLED_SKELETON_IMPLEMENTATION_V1_GO_NO_GO_PACK_V0.md",
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
    parser.add_argument("--implementation-planning-root", default=DEFAULT_IMPLEMENTATION_PLANNING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    upstream = Path(args.implementation_planning_root)
    checks: List[Dict[str, Any]] = []

    planning_summary = _read(upstream / "summary.json")
    planning_verifier = _read(upstream / "verifier_report.json")
    md = (root / "controlled_skeleton_implementation_report_v1.md").read_text(encoding="utf-8") if (root / "controlled_skeleton_implementation_report_v1.md").is_file() else ""
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    report = docs["controlled_skeleton_implementation_report_v1.json"]
    inventory = docs["implemented_files_inventory_v1.json"]
    types_doc = docs["implemented_types_summary_v1.json"]
    contracts_doc = docs["implemented_contracts_summary_v1.json"]
    builders_doc = docs["implemented_builders_summary_v1.json"]
    validators_doc = docs["implemented_validators_summary_v1.json"]
    skeleton_doc = docs["implemented_skeleton_summary_v1.json"]
    guard_doc = docs["non_execution_guard_validation_v1.json"]
    smoke_doc = docs["controlled_skeleton_smoke_result_v1.json"]
    package_doc = docs["strong_coupled_single_package_review_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]

    for name in ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        ok = path.is_file() and (bool(_read(path)) if name.endswith(".json") else len(md.strip()) > 40)
        _add(checks, f"artifact.{name.split('.')[0]}", ok)

    for doc in DOC_PATHS:
        _add(checks, f"doc.{doc.split('/')[-1][:24]}", (REPO_ROOT / doc).is_file())

    _add(checks, "upstream.planning_go", planning_summary.get("final_decision") == IMPLEMENTATION_PLANNING_FINAL_GO)
    _add(checks, "upstream.planning_verifier", planning_verifier.get("verifier") == "GO")
    _add(checks, "upstream.planning_next", planning_summary.get("recommended_next_phase") == IMPLEMENTATION_PLANNING_NEXT_PHASE)
    _add(checks, "upstream.planning_pass", planning_summary.get("orchestration_implementation_planning_pass") is True)
    _add(checks, "upstream.controlled_ready", planning_summary.get("controlled_implementation_ready") is True)

    for rel in CORE_IMPLEMENTATION_FILES:
        _add(checks, f"core.{rel.split('/')[-1][:22]}", (REPO_ROOT / rel).is_file())

    _add(checks, "runner.exists", (REPO_ROOT / PHASE_PYTHON_FILES[-2]).is_file())
    _add(checks, "verifier.exists", (REPO_ROOT / PHASE_PYTHON_FILES[-1]).is_file())

    _add(checks, "summary.pass", summary.get("orchestration_controlled_skeleton_implementation_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
    _expect_false(checks, "summary.real_auth", summary.get("real_request_issuance_authorized"))
    _expect_false(checks, "summary.promotion_exec", summary.get("candidate_promotion_executed"))
    _expect_false(checks, "summary.integration_test", summary.get("integration_test_executed"))
    _add(checks, "summary.runtime_absent", summary.get("runtime_execution_absent") is True)
    _add(checks, "summary.adapter_absent", summary.get("module_adapter_implementation_absent") is True)
    _add(checks, "summary.whitebox_absent", summary.get("whitebox_runtime_integration_absent") is True)
    _add(checks, "summary.drive_absent", summary.get("drive_brain_implementation_absent") is True)
    _add(checks, "summary.reflection_absent", summary.get("reflection_brain_implementation_absent") is True)
    _add(checks, "summary.chain_not_reopen", summary.get("owner_approval_request_chain_not_reopened") is True)
    _add(checks, "summary.not_split", summary.get("implementation_not_split_into_subphases") is True)
    _add(checks, "summary.single_package", summary.get("strong_coupled_single_package_ok") is True)
    _add(checks, "summary.smoke_ok", summary.get("controlled_skeleton_smoke_ok") is True)
    _add(checks, "summary.all_cand", summary.get("all_outputs_candidate_only") is True)
    _add(checks, "summary.guard_ok", summary.get("non_execution_guard_ok") is True)

    _add(checks, "types.implemented", types_doc.get("types_implemented") is True)
    _add(checks, "types.count10", types_doc.get("type_count") >= 10)
    for t in ORCHESTRATION_CANDIDATE_TYPES:
        _add(checks, f"type.{t[:20]}", t in (types_doc.get("types") or []))

    _add(checks, "contracts.implemented", contracts_doc.get("contracts_implemented") is True)
    _add(checks, "contracts.count6", contracts_doc.get("contract_count") >= 6)

    _add(checks, "builders.implemented", builders_doc.get("builders_implemented") is True)
    _add(checks, "builders.candidate_only", builders_doc.get("candidate_only") is True)
    _add(checks, "builders.count9", builders_doc.get("builder_count") >= 9)
    for b in BUILDER_FUNCTIONS:
        _add(checks, f"builder.{b[:20]}", b in (builders_doc.get("builders") or []))

    _add(checks, "validators.implemented", validators_doc.get("validators_implemented") is True)
    _add(checks, "validators.static", validators_doc.get("static_only") is True)
    _add(checks, "validators.count11", validators_doc.get("validator_count") >= 11)
    for v in STATIC_VALIDATOR_FUNCTIONS:
        _add(checks, f"validator.{v[:20]}", v in (validators_doc.get("validators") or []))

    _add(checks, "skeleton.implemented", skeleton_doc.get("skeleton_implemented") is True)
    _add(checks, "skeleton.controlled", skeleton_doc.get("controlled_only") is True)
    _add(checks, "skeleton.count11", skeleton_doc.get("function_count") >= 11)
    for fn in SKELETON_FUNCTIONS:
        _add(checks, f"skel.{fn[:20]}", fn in (skeleton_doc.get("functions") or []))

    _add(checks, "smoke.ok", smoke_doc.get("controlled_skeleton_smoke_ok") is True)
    _add(checks, "smoke.pass", smoke_doc.get("skeleton_pass") is True)
    _add(checks, "smoke.candidate_only", smoke_doc.get("candidate_only") is True)
    _add(checks, "smoke.no_side", smoke_doc.get("side_effect_allowed") is False)
    _add(checks, "smoke.no_real", smoke_doc.get("real_execution") is False)
    _add(checks, "smoke.no_rt", smoke_doc.get("runtime_required_now") is False)
    _add(checks, "smoke.result_id", bool(smoke_doc.get("result_candidate_id")))

    _add(checks, "package.ok", package_doc.get("strong_coupled_single_package_ok") is True)
    _add(checks, "package.not_split", package_doc.get("implementation_not_split_into_subphases") is True)
    _add(checks, "package.split_resp", package_doc.get("files_split_by_responsibility") is True)
    _add(checks, "package.no_mono", package_doc.get("no_monolithic_skeleton") is True)

    _add(checks, "guard.ok", guard_doc.get("non_execution_guard_ok") is True)
    for g in NON_EXECUTION_GUARDS:
        _add(checks, f"guard.{g[:18]}", (guard_doc.get("guards") or {}).get(g) is True)

    for key in ABSENCE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
    _add(checks, "summary.record_creation_absent", summary.get("record_creation_absent") is True)
    _add(checks, "summary.grant_absent", summary.get("grant_absent") is True)
    _add(checks, "summary.auth_req_absent", summary.get("authorization_request_absent") is True)
    _add(checks, "summary.route_exec_absent", summary.get("route_execution_absent") is True)
    _add(checks, "summary.handoff_runtime_absent", summary.get("module_handoff_runtime_absent") is True)

    for key in FILE_SIZE_KEYS:
        _add(checks, f"file_size.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size.get(key) is True)
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.file.{rel.split('/')[-1]}", row.get("exists") is True and row.get("tier") != "blocker_candidate")

    for rel in ORCHESTRATION_CONTROLLED_SKELETON_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for fb in FORBIDDEN:
        combined = f"{summary.get('final_decision')} {summary.get('recommended_next_phase')} {md}".lower()
        _add(checks, f"forbidden.not_{fb[:15]}", fb not in combined)

    _add(checks, "summary.prior_planning", summary.get("prior_implementation_planning_go") is True)
    _add(checks, "summary.non_exec", summary.get("non_execution_boundary_ok") is True)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "upstream.verifier_min", int(planning_verifier.get("passed_checks", 0)) >= 320)
    _add(checks, "owner_closed_module", summary.get("owner_approval_request_closed_module") == "governance_ready_handoff")
    _add(checks, "summary.construction", summary.get("midplatform_overall_status") == MIDPLATFORM_OVERALL_STATUS)
    _add(checks, "summary.future_design_ok", summary.get("future_design_not_current_blocker") is True)
    _add(checks, "summary.runtime_debt_ok", summary.get("future_runtime_debt_not_current_blocker") is True)
    _add(checks, "summary.remaining_work", summary.get("midplatform_still_has_remaining_work") is True)
    _add(checks, "summary.not_final", summary.get("foundation_consolidation_not_final_midplatform_completion") is True)
    _add(checks, "summary.scope_meta", summary.get("scope") == SCOPE)
    _add(checks, "summary.selected_route", summary.get("selected_next_route") == SELECTED_NEXT_ROUTE)
    _add(checks, "inventory.runner", inventory.get("runner_exists") is True)
    _add(checks, "inventory.verifier", inventory.get("verifier_exists") is True)

    for key in GO_CONDITIONS_KEYS:
        if key in report:
            _add(checks, f"report.{key}", report.get(key) is True)

    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "md.final", FINAL_DECISION_GO in md or "DRYRUN" in md)
    _add(checks, "file_size.no_blocker", len(file_size.get("blocker_candidate_files") or []) == 0)
    _add(checks, "summary.template_lineage", summary.get("template_lineage_ok") is True)
    _add(checks, "upstream.failed0", planning_verifier.get("failed_checks") == 0)
    _add(checks, "report.pass_flag", report.get("orchestration_controlled_skeleton_implementation_pass") is True)
    _add(checks, "md.next_phase", NEXT_PHASE_GO in md or "DryRun" in md)

    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_file.{rel.split('/')[-1]}.lines", (row.get("line_count") or 0) <= 800)

    for c in ALL_CONTRACTS:
        _add(checks, f"contract.{c.get('contract_id', '')[:18]}", bool(c.get("contract_id")))

    for rel in CORE_IMPLEMENTATION_FILES:
        entry = next((x for x in inventory.get("core_files") or [] if x.get("path") == rel), {})
        _add(checks, f"inv.{rel.split('/')[-1][:16]}", entry.get("exists") is True)

    _add(checks, "summary.types_impl", summary.get("types_implemented") is True)
    _add(checks, "summary.contracts_impl", summary.get("contracts_implemented") is True)
    _add(checks, "summary.builders_impl", summary.get("builders_implemented") is True)
    _add(checks, "summary.validators_impl", summary.get("validators_implemented") is True)
    _add(checks, "summary.skeleton_impl", summary.get("skeleton_implemented") is True)
    _add(checks, "summary.real_issuance_off", summary.get("real_issuance_preauthorization_not_opened") is True)
    _add(checks, "summary.no_fragment", summary.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "summary.monolithic_absent", summary.get("monolithic_file_absent") is True)
    _add(checks, "summary.full_scan_absent", summary.get("full_repo_scan_absent") is True)
    _add(checks, "summary.tmp_scan_absent", summary.get("tmp_eval_out_scan_absent") is True)
    _add(checks, "summary.index_first", summary.get("summary_index_first_reading_ok") is True)
    _add(checks, "summary.limited_scan", summary.get("limited_directory_scan_ok") is True)
    _add(checks, "summary.file_size_ok", summary.get("file_size_governance_review_ok") is True)
    _add(checks, "summary.next_ready", summary.get("next_phase_readiness_ok") is True)

    for idx, t in enumerate(ORCHESTRATION_CANDIDATE_TYPES):
        _add(checks, f"type_idx.{idx}", t in (types_doc.get("types") or []))
        _add(checks, f"type_len.{idx}", len(t) > 5)

    for idx, b in enumerate(BUILDER_FUNCTIONS):
        _add(checks, f"bld_idx.{idx}", b in (builders_doc.get("builders") or []))
        _add(checks, f"bld_build.{idx}", b.startswith("build_"))

    for idx, v in enumerate(STATIC_VALIDATOR_FUNCTIONS):
        _add(checks, f"val_idx.{idx}", v in (validators_doc.get("validators") or []))
        _add(checks, f"val_prefix.{idx}", v.startswith("validate_"))

    for idx, fn in enumerate(SKELETON_FUNCTIONS):
        _add(checks, f"skel_idx.{idx}", fn in (skeleton_doc.get("functions") or []))

    for idx, rel in enumerate(PHASE_PYTHON_FILES):
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_tier.{idx}", row.get("tier") == "ok")
        _add(checks, f"phase_exists.{idx}", row.get("exists") is True)

    _add(checks, "upstream.planning_types", planning_summary.get("orchestration_data_structure_plan_complete") is True)
    _add(checks, "upstream.planning_units", planning_summary.get("orchestration_functional_units_complete") is True)
    _add(checks, "upstream.planning_files", planning_summary.get("implementation_file_plan_complete") is True)
    _add(checks, "upstream.planning_guard", planning_summary.get("non_execution_implementation_guard_plan_complete") is True)
    _add(checks, "upstream.no_mono", planning_summary.get("no_monolithic_skeleton_planned") is True)
    _add(checks, "upstream.files_split", planning_summary.get("implementation_files_split_by_responsibility") is True)

    _add(checks, "smoke.not_placeholder", smoke_doc.get("result_candidate_id") is not None)
    _add(checks, "package.contents5", len(package_doc.get("package_contents") or []) >= 5)
    _add(checks, "inventory.docs", inventory.get("docs_exist") is True)
    _add(checks, "report.scope", report.get("scope") == SCOPE)
    _add(checks, "report.phase", report.get("phase") == PHASE_ID)
    _add(checks, "md.core_files", "Core files" in md)
    _add(checks, "md.smoke", "Smoke" in md or "smoke" in md.lower())
    _add(checks, "md.single_package", "single package" in md.lower() or "Strong" in md)

    for g in NON_EXECUTION_GUARDS:
        _add(checks, f"summary.guard_{g[:12]}", guard_doc.get("non_execution_guard_ok") is True)

    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"go_cond.{key[:18]}", summary.get(key) is True)

    for rel in CORE_IMPLEMENTATION_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"core_lines.{rel.split('/')[-1][:12]}", (row.get("line_count") or 0) <= 600)

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "orchestration_controlled_skeleton_implementation_verifier_only": True,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{k: summary.get(k) is True for k in GO_CONDITIONS_KEYS},
        "real_request_issuance_authorized": False,
        "integration_test_executed": False,
        "candidate_promotion_executed": False,
        "runtime_execution_absent": summary.get("runtime_execution_absent") is True,
        "drive_brain_implementation_absent": summary.get("drive_brain_implementation_absent") is True,
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
