#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Provider Real Dependency Check DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.ocr_provider_real_dependency_check_dryrun_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    EVIDENCE_CANDIDATE_SLOTS,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
)
from capabilities.governance.ocr_provider_real_dependency_check_planning_v1 import (
    CHECK_SEQUENCE,
    FAILURE_HANDLING,
    FINAL_DECISION_GO as PLANNING_FINAL,
    NEXT_PHASE_GO as PLANNING_NEXT,
    ROLLBACK_RULES,
)

MIN_CHECKS = 116

REQUIRED = (
    "ocr_real_dependency_check_dryrun_policy_v1.json",
    "real_dependency_check_planning_input_review_v1.json",
    "dependency_check_sequence_dryrun_result_v1.json",
    "paddleocr_dependency_check_dryrun_result_v1.json",
    "rapidocr_dependency_check_dryrun_result_v1.json",
    "external_ocr_dependency_check_dryrun_result_v1.json",
    "evidence_package_candidate_v1.json",
    "failure_route_candidate_matrix_v1.json",
    "rollback_plan_candidate_result_v1.json",
    "environment_isolation_boundary_dryrun_result_v1.json",
    "future_execution_gate_dryrun_result_v1.json",
    "real_dependency_check_blocked_path_result_v1.json",
    "real_dependency_check_no_execution_audit_v1.json",
    "real_dependency_check_dryrun_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_provider_real_dependency_check_dryrun"
        ),
    )
    p.add_argument(
        "--ocr-provider-real-dependency-check-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_provider_real_dependency_check_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    planning_root = Path(args.ocr_provider_real_dependency_check_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    sequence = _load(root / "dependency_check_sequence_dryrun_result_v1.json")
    paddle = _load(root / "paddleocr_dependency_check_dryrun_result_v1.json")
    rapid = _load(root / "rapidocr_dependency_check_dryrun_result_v1.json")
    external = _load(root / "external_ocr_dependency_check_dryrun_result_v1.json")
    evidence = _load(root / "evidence_package_candidate_v1.json")
    failure = _load(root / "failure_route_candidate_matrix_v1.json")
    rollback = _load(root / "rollback_plan_candidate_result_v1.json")
    gate = _load(root / "future_execution_gate_dryrun_result_v1.json")
    blocked = _load(root / "real_dependency_check_blocked_path_result_v1.json")
    audit = _load(root / "real_dependency_check_no_execution_audit_v1.json")
    readiness = _load(root / "real_dependency_check_dryrun_readiness_decision_v1.json")

    plan_sm = _load(planning_root / "summary.json")
    plan_vr = _load(planning_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("ocr_provider_real_dependency_check_dryrun_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.flow_sim", summary.get("real_dependency_check_flow_simulated_now") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("upstream.plan_next", plan_sm.get("recommended_next_phase") == PLANNING_NEXT)

    ok("sequence.count9", sequence.get("step_count") == len(CHECK_SEQUENCE))
    for step in sequence.get("steps") or []:
        sid = step.get("step_id", "unknown")
        ok(f"seq.{sid}.not_exec", step.get("current_executed_now") is False)
        ok(f"seq.{sid}.evidence_gen", step.get("evidence_candidate_generated") is True)
        ok(f"seq.{sid}.blocked", step.get("blocked_now") is True)

    for plan_name, plan in (("paddle", paddle), ("rapid", rapid), ("external", external)):
        ok(f"{plan_name}.ref", bool(plan.get("provider_candidate_ref")))
        ok(f"{plan_name}.pkg", bool(plan.get("package_name_or_provider_ref")))
        ok(f"{plan_name}.cache", bool(plan.get("cache_path_requirement")))
        ok(f"{plan_name}.no_invoke", plan.get("current_invocation_allowed") is False)
        ok(f"{plan_name}.no_import", plan.get("current_import_executed_now") is False)

    ok("evidence.slots10", evidence.get("slot_count") == len(EVIDENCE_CANDIDATE_SLOTS))
    ok("evidence.not_collected", evidence.get("evidence_collected_now") is False)
    ok("evidence.only", evidence.get("evidence_only_output") is True)

    ok("failure.count", failure.get("route_count") == len(FAILURE_HANDLING))
    ok("rollback.rules", len(rollback.get("rule_keys") or []) >= len(ROLLBACK_RULES))
    ok("rollback.not_exec", rollback.get("rollback_executed_now") is False)

    ok("gate.closed", gate.get("gate_open_now") is False)
    ok("gate.no_exec", gate.get("execution_allowed_now") is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count13", blocked.get("path_count") == len(BLOCKED_PATHS))

    ok("audit.pass", audit.get("audit_pass") is True)
    ok("audit.no_import", audit.get("no_import") is True)
    ok("audit.no_install", audit.get("no_install") is True)

    ok("readiness.all", readiness.get("all_pass") is True)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "check_count": len(checks),
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
