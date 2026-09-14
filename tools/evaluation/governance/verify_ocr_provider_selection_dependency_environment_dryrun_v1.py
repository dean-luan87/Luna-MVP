#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Provider Selection / Dependency / Environment DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.ocr_controlled_provider_authorization_roadmap_decision_v1 import (
    SELECTED_ROUTE,
)
from capabilities.governance.ocr_provider_selection_dependency_environment_dryrun_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    FINAL_DECISION_GO,
    HEALTH_BINDINGS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    SELECTION_CRITERIA,
)
from capabilities.governance.ocr_provider_selection_dependency_environment_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL,
    NEXT_PHASE_GO as PLANNING_NEXT,
    PROVIDER_INVENTORY,
    SECURITY_CONFIRMATIONS,
)

MIN_CHECKS = 150

REQUIRED = (
    "ocr_provider_selection_dependency_environment_dryrun_policy_v1.json",
    "provider_selection_planning_input_review_v1.json",
    "provider_selection_candidate_v1.json",
    "dependency_readiness_candidate_matrix_v1.json",
    "environment_readiness_candidate_v1.json",
    "provider_comparison_matrix_sample_v1.json",
    "provider_cost_latency_resource_sample_v1.json",
    "provider_capability_fit_sample_v1.json",
    "provider_health_binding_dryrun_result_v1.json",
    "provider_fallback_strategy_dryrun_result_v1.json",
    "provider_security_boundary_dryrun_result_v1.json",
    "provider_no_import_no_install_audit_v1.json",
    "provider_selection_blocked_path_result_v1.json",
    "provider_selection_dryrun_readiness_decision_v1.json",
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
            "ocr_provider_selection_dependency_environment_dryrun"
        ),
    )
    p.add_argument(
        "--ocr-provider-selection-dependency-environment-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_provider_selection_dependency_environment_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    planning_root = Path(args.ocr_provider_selection_dependency_environment_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "provider_selection_planning_input_review_v1.json")
    selection = _load(root / "provider_selection_candidate_v1.json")
    dependency = _load(root / "dependency_readiness_candidate_matrix_v1.json")
    environment = _load(root / "environment_readiness_candidate_v1.json")
    comparison = _load(root / "provider_comparison_matrix_sample_v1.json")
    health = _load(root / "provider_health_binding_dryrun_result_v1.json")
    fallback = _load(root / "provider_fallback_strategy_dryrun_result_v1.json")
    security = _load(root / "provider_security_boundary_dryrun_result_v1.json")
    audit = _load(root / "provider_no_import_no_install_audit_v1.json")
    blocked = _load(root / "provider_selection_blocked_path_result_v1.json")
    readiness = _load(root / "provider_selection_dryrun_readiness_decision_v1.json")

    plan_sm = _load(planning_root / "summary.json")
    plan_vr = _load(planning_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("ocr_provider_selection_dependency_environment_dryrun_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.selection_gen", summary.get("provider_selection_candidate_generated_now") is True)
    ok("summary.dependency_gen", summary.get("dependency_readiness_candidate_generated_now") is True)
    ok("summary.environment_gen", summary.get("environment_readiness_candidate_generated_now") is True)
    ok("summary.comparison_gen", summary.get("provider_comparison_matrix_sample_generated_now") is True)

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("upstream.plan_next", plan_sm.get("recommended_next_phase") == PLANNING_NEXT)
    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.route_b", input_review.get("selected_route") == SELECTED_ROUTE)
    ok("input.count4", input_review.get("provider_candidate_count") == 4)

    ok("selection.count4", selection.get("candidate_count") == 4)
    ok("selection.not_finalized", selection.get("selected_provider_for_execution") is None)
    ok("selection.finalized_false", selection.get("provider_selection_finalized_now") is False)

    families = {c.get("provider_family") for c in selection.get("candidates") or []}
    for fam in ("mock_or_fixture", "paddleocr_later", "rapidocr_later", "external_ocr_later"):
        ok(f"selection.family.{fam}", fam in families)

    for p in PROVIDER_INVENTORY:
        fam = p["provider_family"]
        cand = next((c for c in selection.get("candidates") or [] if c.get("provider_family") == fam), {})
        ok(f"selection.{fam}.status", cand.get("provider_status") == "planned_candidate")
        ok(f"selection.{fam}.invocation", cand.get("invocation_allowed") is False)
        ok(f"selection.{fam}.auth_req", cand.get("authorization_required") is True)
        ok(f"selection.{fam}.dep_req", cand.get("dependency_check_required") is True)
        ok(f"selection.{fam}.env_req", cand.get("environment_check_required") is True)

    ok("dependency.rows4", dependency.get("row_count") == 4)
    for row in dependency.get("rows") or []:
        fam = row.get("provider_family", "unknown")
        ok(f"dep.{fam}.planned_pkg", row.get("python_package_check_planned") is True)
        ok(f"dep.{fam}.no_exec_pkg", row.get("python_package_check_executed_now") is False)
        ok(f"dep.{fam}.no_import", row.get("provider_import_check_executed_now") is False)

    ok("env.virtualenv", environment.get("virtualenv_isolation_required") is True)
    ok("env.no_network", environment.get("network_dependency_default") is False)
    ok("env.sandbox", environment.get("sandbox_boundary_required") is True)
    ok("env.no_prod", environment.get("production_path_write_allowed") is False)
    ok("env.not_executed", environment.get("environment_readiness_check_executed_now") is False)

    ok("comparison.dims17", comparison.get("dimension_count") == len(SELECTION_CRITERIA))
    ok("comparison.rows4", len(comparison.get("rows") or []) == 4)
    for dim in SELECTION_CRITERIA:
        ok(f"comparison.dim.{dim}", dim in (comparison.get("dimensions") or []))

    ok("health.bindings", len(health.get("bindings") or []) == len(HEALTH_BINDINGS))
    ok("fallback.no_auto", fallback.get("no_automatic_switch_execution") is True)
    ok("fallback.not_exec", fallback.get("fallback_executed_now") is False)

    for key in SECURITY_CONFIRMATIONS:
        ok(f"security.{key}", security.get("confirmations", {}).get(key) is True)

    ok("audit.pass", audit.get("audit_pass") is True)
    ok("audit.no_paddle_import", audit.get("paddleocr_imported_now") is False)
    ok("audit.no_rapid_import", audit.get("rapidocr_imported_now") is False)
    ok("audit.no_install", audit.get("dependency_install_executed_now") is False)
    ok("audit.no_sample_ocr", audit.get("sample_ocr_executed_now") is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count", blocked.get("path_count") == len(BLOCKED_PATHS))

    ok("readiness.all_pass", readiness.get("all_pass") is True)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION_GO)

    ok("summary.no_paddle", summary.get("paddleocr_imported_now") is False)
    ok("summary.no_invoke", summary.get("paddleocr_invoked_now") is False)

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
