#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Closure Planning v1."""

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
from capabilities.midplatform.task_manager_foundation_handoff_closure_planning_v1 import (
    DEFAULT_HANDOFF_DRYRUN_ROOT,
    DEFAULT_OUTPUT,
    DEFAULT_PLANNING_ROOT,
    DEFAULT_POST_REVIEW_ROOT,
    DRYRUN_PACKAGE_FILES,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_EXECUTION_CONSTRAINTS,
    PHASE_ID,
    PLANNING_PACKAGE_FILES,
    POST_REVIEW_PACKAGE_FILES,
    SCOPE,
)
from capabilities.midplatform.task_manager_foundation_handoff_dryrun_v1 import FINAL_DECISION_GO as DRYRUN_FINAL_GO
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import FINAL_DECISION_GO as PLANNING_FINAL_GO
from capabilities.midplatform.task_manager_foundation_handoff_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_closure_plan_v1.json",
    "task_manager_foundation_handoff_closure_plan_v1.md",
    "task_manager_foundation_asset_inventory_v1.json",
    "task_manager_handoff_closure_evidence_chain_v1.json",
    "task_manager_handoff_freeze_candidate_boundary_v1.json",
    "task_manager_handoff_candidate_semantics_lock_plan_v1.json",
    "task_manager_handoff_downstream_planning_map_v1.json",
    "task_manager_handoff_future_l1_protocol_dependency_map_v1.json",
    "task_manager_handoff_closure_non_execution_constraints_v1.json",
    "summary.json",
)
TRUE_KEYS: Tuple[str, ...] = (
    "prior_chain_go",
    "closure_plan_complete",
    "asset_inventory_complete",
    "evidence_chain_complete",
    "freeze_candidate_only",
    "closure_planning_only",
    "candidate_semantics_preserved",
    "non_execution_boundary_ok",
    "downstream_scope_ok",
    "future_l1_dependencies_only",
)
FORBIDDEN_WORDS: Tuple[str, ...] = (
    "implementation-ready",
    "runtime-ready",
    "production-ready",
    "foundation_frozen",
    "foundation-frozen",
    "closed",
    "finalized",
)
RUNTIME_FORBIDDEN: Tuple[str, ...] = (
    "runtime_executor_created_now",
    "scheduler_binding_created_now",
    "task_execution_authority_granted_now",
    "output_authorization_granted_now",
    "module_adapter_integration_created_now",
    "information_channel_governance_implemented_now",
    "protocol_governance_implemented_now",
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
    parser.add_argument("--planning-root", default=DEFAULT_PLANNING_ROOT)
    parser.add_argument("--handoff-dryrun-root", default=DEFAULT_HANDOFF_DRYRUN_ROOT)
    parser.add_argument("--post-review-root", default=DEFAULT_POST_REVIEW_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    planning = Path(args.planning_root)
    dryrun = Path(args.handoff_dryrun_root)
    post = Path(args.post_review_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_closure_plan_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    for stage_name, stage_root, expected_final in (
        ("planning", planning, PLANNING_FINAL_GO),
        ("dryrun", dryrun, DRYRUN_FINAL_GO),
        ("post_review", post, POST_REVIEW_FINAL_GO),
    ):
        summary = _read(stage_root / "summary.json")
        verifier = _read(stage_root / "verifier_report.json")
        _add(checks, f"prior.{stage_name}.summary_exists", bool(summary))
        _add(checks, f"prior.{stage_name}.verifier_exists", bool(verifier))
        _add(checks, f"prior.{stage_name}.summary_go", summary.get("final_decision") == expected_final)
        _add(checks, f"prior.{stage_name}.verifier_go", verifier.get("verifier") == "GO")
        _add(checks, f"prior.{stage_name}.failed_zero", verifier.get("failed_checks") == 0)
        _add(checks, f"prior.{stage_name}.blocker_zero", verifier.get("blocker_count") == 0)

    plan = docs["task_manager_foundation_handoff_closure_plan_v1.json"]
    inventory = docs["task_manager_foundation_asset_inventory_v1.json"]
    evidence = docs["task_manager_handoff_closure_evidence_chain_v1.json"]
    freeze = docs["task_manager_handoff_freeze_candidate_boundary_v1.json"]
    semantics = docs["task_manager_handoff_candidate_semantics_lock_plan_v1.json"]
    downstream = docs["task_manager_handoff_downstream_planning_map_v1.json"]
    l1_map = docs["task_manager_handoff_future_l1_protocol_dependency_map_v1.json"]
    constraints = docs["task_manager_handoff_closure_non_execution_constraints_v1.json"]
    summary = docs["summary.json"]

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(checks, f"meta.closure_planning_only.{doc_name}", doc.get("closure_planning_only") in (None, True))
        _add(checks, f"meta.not_frozen.{doc_name}", doc.get("foundation_not_frozen") in (None, True))
        for key in RUNTIME_FORBIDDEN:
            _add(checks, f"meta.no_runtime.{doc_name}.{key}", doc.get(key) is not True)
        if doc_name not in ("summary.json", "task_manager_handoff_closure_evidence_chain_v1.json"):
            dumped = json.dumps(doc, ensure_ascii=False)
            for word in ("foundation_frozen", "foundation-frozen"):
                _add(checks, f"meta.no_status_word.{doc_name}.{word}", f'"{word}"' not in dumped or doc.get(word) is False)

    _add(checks, "summary.pass", summary.get("planning_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in TRUE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
        _add(checks, f"plan.{key}", plan.get(key) is True)

    _add(checks, "plan.closure_readiness", plan.get("closure_readiness") == "closure-dryrun-ready")
    _add(checks, "plan.closure_not_applied", plan.get("closure_applied") is False)
    _add(checks, "plan.not_frozen", plan.get("foundation_not_frozen") is True)

    assets = inventory.get("assets") or []
    for rel in SKELETON_FILES:
        row = next((a for a in assets if a.get("path") == rel), {})
        _add(checks, f"inventory.skeleton.{rel}", row.get("exists") is True)
    for package_name, files, pkg_root in (
        ("planning_package", PLANNING_PACKAGE_FILES, planning),
        ("dryrun_package", DRYRUN_PACKAGE_FILES, dryrun),
        ("post_review_package", POST_REVIEW_PACKAGE_FILES, post),
    ):
        for fname in files:
            row = next((a for a in assets if a.get("file") == fname and a.get("asset_type") == package_name), {})
            _add(checks, f"inventory.{package_name}.{fname}", row.get("exists") is True or (pkg_root / fname).is_file())
    _add(checks, "inventory.complete", inventory.get("asset_inventory_complete") is True)

    chain = evidence.get("chain") or []
    for stage in ("planning", "dryrun", "post_dryrun_review"):
        row = next((c for c in chain if c.get("stage") == stage), {})
        _add(checks, f"evidence.linked.{stage}", row.get("linked") is True)
    closure_row = next((c for c in chain if c.get("stage") == "closure_planning"), {})
    _add(checks, "evidence.closure_readiness", closure_row.get("readiness") == "closure-dryrun-ready")
    _add(checks, "evidence.closure_not_applied", closure_row.get("closure_applied") is False)
    _add(checks, "evidence.complete", evidence.get("evidence_chain_complete") is True)

    _add(checks, "freeze.status", freeze.get("freeze_status") == "freeze-candidate")
    _add(checks, "freeze.not_frozen", freeze.get("foundation_frozen") is False)
    _add(checks, "freeze.closure_not_applied", freeze.get("closure_applied") is False)
    _add(checks, "freeze.readiness", freeze.get("closure_readiness") == "closure-dryrun-ready")
    _add(checks, "freeze.candidate_only", freeze.get("freeze_candidate_only") is True)
    for rel in SKELETON_FILES:
        _add(checks, f"freeze.skeleton.{rel}", rel in (freeze.get("skeleton_files_to_freeze") or []))

    _add(checks, "semantics.lock_plan_only", semantics.get("lock_plan_only") is True)
    _add(checks, "semantics.not_executed", semantics.get("semantics_executed") is False)
    _add(checks, "semantics.task_not_execution", semantics.get("task_candidate_not_task_execution") is True)
    _add(checks, "semantics.step_not_executed", semantics.get("task_step_candidate_not_executed_step") is True)
    _add(checks, "semantics.handoff_not_mount", semantics.get("task_handoff_candidate_not_direct_mount") is True)
    for boundary in semantics.get("boundaries") or []:
        _add(checks, f"semantics.boundary.{boundary.get('payload_type')}", bool(boundary.get("boundary")))

    for row in downstream.get("consumers") or []:
        consumer = row.get("consumer")
        _add(checks, f"downstream.readiness.{consumer}", row.get("readiness") == "planning-handoff-ready")
        _add(checks, f"downstream.not_impl.{consumer}", row.get("readiness") != "implementation-ready")
        _add(checks, f"downstream.not_runtime.{consumer}", row.get("readiness") != "runtime-ready")
        _add(checks, f"downstream.not_prod.{consumer}", row.get("readiness") != "production-ready")
    _add(checks, "downstream.scope_ok", downstream.get("downstream_scope_ok") is True)

    for dep in l1_map.get("dependencies") or []:
        protocol = dep.get("protocol")
        _add(checks, f"l1.future.{protocol}", dep.get("status") == "future_l1_dependency")
        _add(checks, f"l1.not_implemented.{protocol}", dep.get("implemented") == "false")
    _add(checks, "l1.only_dependencies", l1_map.get("future_l1_dependencies_only") is True)

    for constraint in NON_EXECUTION_CONSTRAINTS:
        _add(checks, f"constraints.exists.{constraint}", constraint in (constraints.get("constraints") or []))
        _add(checks, f"constraints.true.{constraint}", constraints.get(constraint) is True)
    _add(checks, "constraints.boundary_ok", constraints.get("non_execution_boundary_ok") is True)

    _add(checks, "md.non_empty", len(md.strip()) > 200)
    _add(checks, "md.final", FINAL_DECISION_GO in md or "closure-dryrun-ready" in md)
    _add(checks, "md.next", NEXT_PHASE_GO in md)
    _add(checks, "md.freeze_candidate", "freeze-candidate" in md)
    _add(checks, "md.not_frozen", "not frozen" in md.lower())
    for token in ("task_candidate != task execution", "task_step_candidate != executed step"):
        _add(checks, f"md.token.{token[:30]}", token in md)

    for scope_item in plan.get("closure_scope") or []:
        _add(checks, f"plan.scope_item.{scope_item[:40]}", bool(scope_item))
    for ctype in ("task_candidate", "task_plan_candidate", "task_step_candidate", "task_handoff_candidate"):
        _add(checks, f"freeze.candidate_type.{ctype}", ctype in (freeze.get("candidate_types_to_freeze") or []))

    # Cross-artifact sweeps
    for doc_name, doc in docs.items():
        for key in TRUE_KEYS:
            if key in doc:
                _add(checks, f"sweep.true.{doc_name}.{key}", doc.get(key) is True)
        _add(checks, f"sweep.next_closure_dryrun.{doc_name}", doc.get("recommended_next_phase") in (None, NEXT_PHASE_GO))
        for required in ("phase", "scope", "source_chain", "foundation_id", "runtime_status"):
            _add(checks, f"sweep.meta.{doc_name}.{required}", required in doc)
        _add(checks, f"sweep.closure_planning_only.{doc_name}", doc.get("closure_planning_only") in (None, True))
        _add(checks, f"sweep.foundation_not_frozen.{doc_name}", doc.get("foundation_not_frozen") in (None, True))
        for key in RUNTIME_FORBIDDEN:
            _add(checks, f"sweep.runtime_absent.{doc_name}.{key}", doc.get(key) is not True)

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        "prior_chain_go": summary.get("prior_chain_go") is True,
        "closure_plan_complete": summary.get("closure_plan_complete") is True,
        "asset_inventory_complete": summary.get("asset_inventory_complete") is True,
        "evidence_chain_complete": summary.get("evidence_chain_complete") is True,
        "freeze_candidate_only": summary.get("freeze_candidate_only") is True,
        "closure_planning_only": summary.get("closure_planning_only") is True,
        "candidate_semantics_preserved": summary.get("candidate_semantics_preserved") is True,
        "non_execution_boundary_ok": summary.get("non_execution_boundary_ok") is True,
        "downstream_scope_ok": summary.get("downstream_scope_ok") is True,
        "future_l1_dependencies_only": summary.get("future_l1_dependencies_only") is True,
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
                "prior_chain_go": report["prior_chain_go"],
                "closure_plan_complete": report["closure_plan_complete"],
                "asset_inventory_complete": report["asset_inventory_complete"],
                "evidence_chain_complete": report["evidence_chain_complete"],
                "freeze_candidate_only": report["freeze_candidate_only"],
                "closure_planning_only": report["closure_planning_only"],
                "candidate_semantics_preserved": report["candidate_semantics_preserved"],
                "non_execution_boundary_ok": report["non_execution_boundary_ok"],
                "downstream_scope_ok": report["downstream_scope_ok"],
                "future_l1_dependencies_only": report["future_l1_dependencies_only"],
                "final_decision": report["final_decision"],
                "recommended_next_phase": report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
