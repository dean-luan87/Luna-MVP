#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Provider Real Dependency Check Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.ocr_provider_real_dependency_check_planning_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    CHECK_SEQUENCE,
    EVIDENCE_ARTIFACTS,
    FAILURE_HANDLING,
    FINAL_DECISION_GO,
    FUTURE_CHECK_SCOPE,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    ROLLBACK_RULES,
    SCOPE,
)
from capabilities.governance.ocr_provider_selection_dependency_environment_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL,
    NEXT_PHASE_GO as POST_REVIEW_NEXT,
)

MIN_CHECKS = 124

REQUIRED = (
    "ocr_real_dependency_check_planning_policy_v1.json",
    "provider_selection_post_review_input_review_v1.json",
    "real_dependency_check_scope_v1.json",
    "provider_dependency_check_sequence_plan_v1.json",
    "paddleocr_real_dependency_check_plan_v1.json",
    "rapidocr_real_dependency_check_plan_v1.json",
    "external_ocr_real_dependency_check_plan_v1.json",
    "model_cache_and_file_integrity_check_plan_v1.json",
    "import_check_authorization_boundary_plan_v1.json",
    "environment_isolation_and_sandbox_plan_v1.json",
    "evidence_package_plan_v1.json",
    "failure_handling_and_rollback_plan_v1.json",
    "real_dependency_check_blocked_path_matrix_v1.json",
    "real_dependency_check_future_execution_gate_v1.json",
    "real_dependency_check_non_claims_register_v1.json",
    "real_dependency_check_planning_decision_v1.json",
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
            "ocr_provider_real_dependency_check_planning"
        ),
    )
    p.add_argument(
        "--ocr-provider-selection-dependency-environment-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_provider_selection_dependency_environment_post_dryrun_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    post_root = Path(args.ocr_provider_selection_dependency_environment_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "provider_selection_post_review_input_review_v1.json")
    scope = _load(root / "real_dependency_check_scope_v1.json")
    sequence = _load(root / "provider_dependency_check_sequence_plan_v1.json")
    paddle = _load(root / "paddleocr_real_dependency_check_plan_v1.json")
    rapid = _load(root / "rapidocr_real_dependency_check_plan_v1.json")
    external = _load(root / "external_ocr_real_dependency_check_plan_v1.json")
    evidence = _load(root / "evidence_package_plan_v1.json")
    failure = _load(root / "failure_handling_and_rollback_plan_v1.json")
    blocked = _load(root / "real_dependency_check_blocked_path_matrix_v1.json")
    gate = _load(root / "real_dependency_check_future_execution_gate_v1.json")
    decision = _load(root / "real_dependency_check_planning_decision_v1.json")

    post_sm = _load(post_root / "summary.json")
    post_vr = _load(post_root / "verifier_report.json")
    next_route = _load(post_root / "next_route_readiness_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("ocr_provider_real_dependency_check_planning_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.no_exec", summary.get("real_dependency_check_executed_now") is False)
    ok("summary.null_provider", summary.get("selected_provider_for_execution") is None)

    ok("upstream.post_go", post_vr.get("verifier") == "GO")
    ok("upstream.post_final", post_sm.get("final_decision") == POST_REVIEW_FINAL)
    ok("upstream.post_next", post_sm.get("recommended_next_phase") == POST_REVIEW_NEXT)
    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.trusted", input_review.get("selection_candidate_trusted") is True)

    ok("next.no_import", next_route.get("do_not_import_provider_now") is True)
    ok("next.no_install", next_route.get("do_not_install_dependency_now") is True)
    ok("next.no_invoke", next_route.get("do_not_invoke_provider_now") is True)
    ok("next.no_finalize", next_route.get("do_not_finalize_provider_selection_now") is True)

    for chk in FUTURE_CHECK_SCOPE:
        ok(f"scope.future.{chk}", chk in (scope.get("future_checks_allowed_after_authorization") or []))
        ok(f"scope.forbidden.{chk}", chk in (scope.get("forbidden_now") or []))

    ok("sequence.count9", sequence.get("step_count") == len(CHECK_SEQUENCE))
    for step in sequence.get("steps") or []:
        sid = step.get("step_id", "unknown")
        ok(f"seq.{sid}.later", step.get("execution_allowed_later") is True)
        ok(f"seq.{sid}.evidence", step.get("evidence_required") is True)
        ok(f"seq.{sid}.not_exec", step.get("current_executed_now") is False)

    for plan_name, plan in (("paddle", paddle), ("rapid", rapid), ("external", external)):
        ok(f"{plan_name}.no_invoke", plan.get("current_invocation_allowed") is False)
        ok(f"{plan_name}.no_import", plan.get("current_import_executed_now") is False)
        ok(f"{plan_name}.import_later", plan.get("import_check_later") is True)
        ok(f"{plan_name}.smoke_later", plan.get("smoke_check_later") is True)

    ok("evidence.count", len(evidence.get("artifacts") or []) >= len(EVIDENCE_ARTIFACTS))
    ok("evidence.not_now", evidence.get("evidence_collected_now") is False)

    ok("failure.routes", len(failure.get("failure_routes") or []) == len(FAILURE_HANDLING))
    ok("failure.rollback", len(failure.get("rollback_rules") or []) >= len(ROLLBACK_RULES))

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count13", blocked.get("path_count") == len(BLOCKED_PATHS))

    ok("gate.auth", gate.get("real_dependency_check_authorization_required") is True)
    ok("gate.sandbox", gate.get("sandbox_path_confirmed") is True)
    ok("gate.evidence", gate.get("evidence_package_required") is True)
    ok("gate.closed", gate.get("gate_open_now") is False)

    ok("decision.ready", decision.get("ready_for_dryrun") is True)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "real_dependency_check_non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

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
