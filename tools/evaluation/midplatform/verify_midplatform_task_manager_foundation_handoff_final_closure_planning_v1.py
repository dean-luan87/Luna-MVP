#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Final Closure Planning v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_task_manager_controlled_skeleton_implementation_dryrun_v1 import (
    SKELETON_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_closure_dryrun_v1 import (
    CLOSURE_PLANNING_PACKAGE_FILES,
    FINAL_DECISION_GO as CLOSURE_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.task_manager_foundation_handoff_closure_planning_v1 import (
    DRYRUN_PACKAGE_FILES,
    FINAL_DECISION_GO as CLOSURE_PLANNING_FINAL_GO,
    PLANNING_PACKAGE_FILES,
    POST_REVIEW_PACKAGE_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_closure_post_dryrun_review_v1 import (
    CLOSURE_DRYRUN_ARTIFACTS,
    FINAL_DECISION_GO as CLOSURE_POST_REVIEW_FINAL_GO,
)
from capabilities.midplatform.task_manager_foundation_handoff_dryrun_v1 import FINAL_DECISION_GO as HANDOFF_DRYRUN_FINAL_GO
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import (
    BOUNDARY_CONTRACT_STATEMENTS,
    CLOSURE_POST_REVIEW_PACKAGE_FILES,
    DEFAULT_CLOSURE_DRYRUN_ROOT,
    DEFAULT_CLOSURE_PLANNING_ROOT,
    DEFAULT_CLOSURE_POST_REVIEW_ROOT,
    DEFAULT_HANDOFF_DRYRUN_ROOT,
    DEFAULT_HANDOFF_PLANNING_ROOT,
    DEFAULT_HANDOFF_POST_REVIEW_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GOVERNANCE_DEBTS,
    NEXT_PHASE_GO,
    NON_EXECUTION_CONSTRAINTS,
    PHASE_ID,
    SCOPE,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import FINAL_DECISION_GO as HANDOFF_PLANNING_FINAL_GO
from capabilities.midplatform.task_manager_foundation_handoff_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as HANDOFF_POST_REVIEW_FINAL_GO,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_final_closure_plan_v1.json",
    "task_manager_foundation_handoff_final_closure_plan_v1.md",
    "task_manager_final_closure_chain_evidence_map_v1.json",
    "task_manager_final_freeze_candidate_asset_map_v1.json",
    "task_manager_final_closure_boundary_contract_v1.json",
    "task_manager_final_candidate_semantics_lock_plan_v1.json",
    "task_manager_final_downstream_reference_contract_v1.json",
    "task_manager_final_governance_debt_carryover_v1.json",
    "task_manager_final_non_execution_constraints_v1.json",
    "task_manager_final_closure_next_phase_readiness_v1.json",
    "summary.json",
)
TRUE_KEYS: Tuple[str, ...] = (
    "prior_full_chain_go",
    "final_closure_plan_complete",
    "chain_evidence_complete",
    "freeze_candidate_asset_map_complete",
    "freeze_candidate_only",
    "closure_planning_only",
    "candidate_semantics_preserved",
    "non_execution_boundary_ok",
    "downstream_reference_scope_ok",
    "governance_debt_carryover_complete",
    "l1_protocols_not_implemented",
    "system_protocols_integration_not_implemented",
)
FORBIDDEN_DOWNSTREAM: Tuple[str, ...] = ("implementation-ready", "runtime-ready", "production-ready")
RUNTIME_FORBIDDEN: Tuple[str, ...] = (
    "runtime_executor_created_now",
    "scheduler_binding_created_now",
    "task_execution_authority_granted_now",
    "output_authorization_granted_now",
    "module_adapter_integration_created_now",
    "information_channel_governance_implemented_now",
    "protocol_governance_implemented_now",
    "closure_channel_governance_implemented_now",
    "system_protocols_integration_implemented_now",
)


def _read(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _add(checks: List[Dict[str, Any]], check_id: str, passed: bool, detail: str = "") -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--handoff-planning-root", default=DEFAULT_HANDOFF_PLANNING_ROOT)
    parser.add_argument("--handoff-dryrun-root", default=DEFAULT_HANDOFF_DRYRUN_ROOT)
    parser.add_argument("--handoff-post-review-root", default=DEFAULT_HANDOFF_POST_REVIEW_ROOT)
    parser.add_argument("--closure-planning-root", default=DEFAULT_CLOSURE_PLANNING_ROOT)
    parser.add_argument("--closure-dryrun-root", default=DEFAULT_CLOSURE_DRYRUN_ROOT)
    parser.add_argument("--closure-post-review-root", default=DEFAULT_CLOSURE_POST_REVIEW_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_final_closure_plan_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    chain_stages = (
        ("handoff_planning", Path(args.handoff_planning_root), HANDOFF_PLANNING_FINAL_GO, PLANNING_PACKAGE_FILES),
        ("handoff_dryrun", Path(args.handoff_dryrun_root), HANDOFF_DRYRUN_FINAL_GO, DRYRUN_PACKAGE_FILES),
        ("handoff_post_review", Path(args.handoff_post_review_root), HANDOFF_POST_REVIEW_FINAL_GO, POST_REVIEW_PACKAGE_FILES),
        ("closure_planning", Path(args.closure_planning_root), CLOSURE_PLANNING_FINAL_GO, CLOSURE_PLANNING_PACKAGE_FILES),
        ("closure_dryrun", Path(args.closure_dryrun_root), CLOSURE_DRYRUN_FINAL_GO, CLOSURE_DRYRUN_ARTIFACTS),
        ("closure_post_review", Path(args.closure_post_review_root), CLOSURE_POST_REVIEW_FINAL_GO, CLOSURE_POST_REVIEW_PACKAGE_FILES),
    )
    for stage_name, stage_root, expected_final, _files in chain_stages:
        summary = _read(stage_root / "summary.json")
        verifier = _read(stage_root / "verifier_report.json")
        _add(checks, f"prior.{stage_name}.summary_exists", (stage_root / "summary.json").is_file())
        _add(checks, f"prior.{stage_name}.verifier_exists", (stage_root / "verifier_report.json").is_file())
        _add(checks, f"prior.{stage_name}.summary_go", summary.get("final_decision") == expected_final)
        _add(checks, f"prior.{stage_name}.verifier_go", verifier.get("verifier") == "GO")
        _add(checks, f"prior.{stage_name}.failed_zero", verifier.get("failed_checks") == 0)
        _add(checks, f"prior.{stage_name}.blocker_zero", verifier.get("blocker_count") == 0)

    plan = docs["task_manager_foundation_handoff_final_closure_plan_v1.json"]
    chain_map = docs["task_manager_final_closure_chain_evidence_map_v1.json"]
    freeze_map = docs["task_manager_final_freeze_candidate_asset_map_v1.json"]
    boundary = docs["task_manager_final_closure_boundary_contract_v1.json"]
    semantics = docs["task_manager_final_candidate_semantics_lock_plan_v1.json"]
    downstream = docs["task_manager_final_downstream_reference_contract_v1.json"]
    debt_carryover = docs["task_manager_final_governance_debt_carryover_v1.json"]
    constraints = docs["task_manager_final_non_execution_constraints_v1.json"]
    next_phase = docs["task_manager_final_closure_next_phase_readiness_v1.json"]
    summary = docs["summary.json"]

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(checks, f"meta.closure_planning_only.{doc_name}", doc.get("closure_planning_only") in (None, True))
        _add(checks, f"meta.foundation_not_frozen.{doc_name}", doc.get("foundation_not_frozen") in (None, True))
        _add(checks, f"meta.l1_not_impl.{doc_name}", doc.get("l1_protocols_not_implemented") in (None, True))
        _add(checks, f"meta.sys_proto_not_impl.{doc_name}", doc.get("system_protocols_integration_not_implemented") in (None, True))
        for key in RUNTIME_FORBIDDEN:
            _add(checks, f"meta.no_runtime.{doc_name}.{key}", doc.get(key) is not True)

    _add(checks, "summary.pass", summary.get("planning_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in TRUE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
        _add(checks, f"plan.{key}", plan.get(key) is True)

    expected_stages = (
        "planning",
        "dryrun",
        "post_dryrun_review",
        "closure_planning",
        "closure_dryrun",
        "closure_post_dryrun_review",
    )
    _add(checks, "chain.complete", chain_map.get("chain_evidence_complete") is True)
    for stage in expected_stages:
        row = next((r for r in chain_map.get("chain") or [] if r.get("stage") == stage), {})
        _add(checks, f"chain.linked.{stage}", row.get("linked") is True)

    _add(checks, "freeze_map.complete", freeze_map.get("freeze_candidate_asset_map_complete") is True)
    _add(checks, "freeze_map.candidate_only", freeze_map.get("freeze_candidate_only") is True)
    _add(checks, "freeze_map.status", freeze_map.get("freeze_status") == "freeze-candidate")
    _add(checks, "freeze_map.not_frozen", freeze_map.get("foundation_frozen") is False)
    for rel in SKELETON_FILES:
        row = next((a for a in freeze_map.get("assets") or [] if a.get("path") == rel), {})
        _add(checks, f"freeze_map.skeleton.{rel.split('/')[-1]}", row.get("exists") is True)
        _add(checks, f"freeze_map.skeleton_status.{rel.split('/')[-1]}", row.get("freeze_status") == "freeze-candidate")
    for pkg in (
        "planning_package",
        "dryrun_package",
        "post_review_package",
        "closure_planning_package",
        "closure_dryrun_package",
        "closure_post_review_package",
    ):
        pkg_rows = [a for a in freeze_map.get("assets") or [] if a.get("asset_type") == pkg]
        _add(checks, f"freeze_map.pkg.{pkg}.exists", len(pkg_rows) > 0)
        _add(checks, f"freeze_map.pkg.{pkg}.all_candidate", all(r.get("freeze_status") == "freeze-candidate" for r in pkg_rows))

    _add(checks, "boundary.readiness", boundary.get("closure_readiness") == "final-closure-planning-ready")
    _add(checks, "boundary.not_closed", boundary.get("closure_applied") is False)
    _add(checks, "boundary.freeze_status", boundary.get("freeze_status") == "freeze-candidate")
    for stmt in BOUNDARY_CONTRACT_STATEMENTS:
        _add(checks, f"boundary.stmt.{stmt[:30]}", stmt in (boundary.get("statements") or []))
        _add(checks, f"md.boundary.{stmt[:30]}", stmt in md)

    _add(checks, "semantics.lock_plan_only", semantics.get("lock_plan_only") is True)
    _add(checks, "semantics.not_executed", semantics.get("semantics_executed") is False)
    _add(checks, "semantics.lock_not_executed", semantics.get("lock_executed") is False)
    _add(checks, "semantics.preserved", semantics.get("candidate_semantics_preserved") is True)

    _add(checks, "downstream.ok", downstream.get("downstream_reference_scope_ok") is True)
    for row in downstream.get("consumers") or []:
        consumer = row.get("consumer")
        readiness = row.get("readiness")
        _add(checks, f"downstream.ref_ok.{consumer}", readiness in ("reference-ready", "planning-reference-ready"))
        for forbidden in FORBIDDEN_DOWNSTREAM:
            _add(checks, f"downstream.not_{forbidden}.{consumer}", readiness != forbidden)

    debts = debt_carryover.get("debts") or []
    _add(checks, "debt.count", len(debts) >= 2)
    debt0 = debts[0] if debts else {}
    debt1 = debts[1] if len(debts) > 1 else {}
    _add(checks, "debt0.title", debt0.get("debt_title") == GOVERNANCE_DEBTS[0]["debt_title"])
    _add(checks, "debt0.priority", debt0.get("priority") == "P1")
    _add(checks, "debt0.classification", debt0.get("classification") == "L1 Midplatform System Protocols")
    _add(checks, "debt0.must_not_impl", debt0.get("must_not_implement_now") is True)
    _add(checks, "debt0.future_phase", debt0.get("recommended_future_phase") == GOVERNANCE_DEBTS[0]["recommended_future_phase"])
    _add(checks, "debt1.title", debt1.get("debt_title") == GOVERNANCE_DEBTS[1]["debt_title"])
    _add(checks, "debt1.priority", debt1.get("priority") == "P1")
    _add(checks, "debt1.classification", debt1.get("classification") == "L1 Midplatform System Protocols")
    _add(checks, "debt1.must_not_impl", debt1.get("must_not_implement_now") is True)
    _add(checks, "debt1.future_phase", debt1.get("recommended_future_phase") == GOVERNANCE_DEBTS[1]["recommended_future_phase"])
    _add(checks, "debt.carryover_complete", debt_carryover.get("governance_debt_carryover_complete") is True)

    for key in NON_EXECUTION_CONSTRAINTS:
        _add(checks, f"constraints.{key}", constraints.get(key) is True)
    _add(checks, "constraints.ok", constraints.get("non_execution_boundary_ok") is True)

    _add(checks, "next_phase.not_module_adapter", next_phase.get("module_adapter_implementation_ready") is False)
    _add(checks, "next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE_GO)
    for candidate in next_phase.get("candidates") or []:
        phase = candidate.get("phase", "")
        _add(checks, f"next_phase.candidate.{phase[:40]}.no_adapter", candidate.get("module_adapter_implementation") is False)

    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.next", NEXT_PHASE_GO in md)
    _add(checks, "md.not_execute", "does not execute closure" in md or "不执行 closure" in md)
    _add(checks, "md.debt0", GOVERNANCE_DEBTS[0]["debt_title"] in md)
    _add(checks, "md.debt1", GOVERNANCE_DEBTS[1]["debt_title"] in md)

    for doc_name, doc in docs.items():
        for key in TRUE_KEYS:
            if key in doc:
                _add(checks, f"sweep.true.{doc_name}.{key}", doc.get(key) is True)
        _add(checks, f"sweep.next.{doc_name}", doc.get("recommended_next_phase") in (None, NEXT_PHASE_GO))
        for required in ("phase", "scope", "source_chain", "foundation_id", "runtime_status"):
            _add(checks, f"sweep.meta.{doc_name}.{required}", required in doc)
        for key in RUNTIME_FORBIDDEN:
            _add(checks, f"sweep.runtime.{doc_name}.{key}", doc.get(key) is not True)
        _add(checks, f"sweep.boundary_en.{doc_name}", bool(doc.get("boundary_statement_en")))
        _add(checks, f"sweep.boundary_zh.{doc_name}", bool(doc.get("boundary_statement_zh")))

    for phrase in ("final-closure-planning-ready", "freeze-candidate", "Governance Debt Carryover"):
        _add(checks, f"md.phrase.{phrase[:30]}", phrase in md)

    passed = sum(1 for check in checks if check["passed"])
    failed = [check for check in checks if not check["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        "prior_full_chain_go": summary.get("prior_full_chain_go") is True,
        "final_closure_plan_complete": summary.get("final_closure_plan_complete") is True,
        "chain_evidence_complete": summary.get("chain_evidence_complete") is True,
        "freeze_candidate_asset_map_complete": summary.get("freeze_candidate_asset_map_complete") is True,
        "freeze_candidate_only": summary.get("freeze_candidate_only") is True,
        "closure_planning_only": summary.get("closure_planning_only") is True,
        "candidate_semantics_preserved": summary.get("candidate_semantics_preserved") is True,
        "non_execution_boundary_ok": summary.get("non_execution_boundary_ok") is True,
        "downstream_reference_scope_ok": summary.get("downstream_reference_scope_ok") is True,
        "governance_debt_carryover_complete": summary.get("governance_debt_carryover_complete") is True,
        "l1_protocols_not_implemented": summary.get("l1_protocols_not_implemented") is True,
        "system_protocols_integration_not_implemented": summary.get("system_protocols_integration_not_implemented") is True,
        "final_decision": FINAL_DECISION_GO if verifier == "GO" else "HOLD",
        "recommended_next_phase": NEXT_PHASE_GO if verifier == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:80],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": report["verifier"],
                "passed_checks": report["passed_checks"],
                "failed_checks": report["failed_checks"],
                "blocker_count": report["blocker_count"],
                "prior_full_chain_go": report["prior_full_chain_go"],
                "final_closure_plan_complete": report["final_closure_plan_complete"],
                "chain_evidence_complete": report["chain_evidence_complete"],
                "freeze_candidate_asset_map_complete": report["freeze_candidate_asset_map_complete"],
                "freeze_candidate_only": report["freeze_candidate_only"],
                "closure_planning_only": report["closure_planning_only"],
                "candidate_semantics_preserved": report["candidate_semantics_preserved"],
                "non_execution_boundary_ok": report["non_execution_boundary_ok"],
                "downstream_reference_scope_ok": report["downstream_reference_scope_ok"],
                "governance_debt_carryover_complete": report["governance_debt_carryover_complete"],
                "l1_protocols_not_implemented": report["l1_protocols_not_implemented"],
                "system_protocols_integration_not_implemented": report["system_protocols_integration_not_implemented"],
                "final_decision": report["final_decision"],
                "recommended_next_phase": report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
