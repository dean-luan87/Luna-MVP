#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Provider Selection / Dependency / Environment Planning v1."""

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
    FINAL_DECISION_GO as ROADMAP_FINAL,
    SELECTED_ROUTE,
)
from capabilities.governance.ocr_controlled_provider_dryrun_v1 import BLOCKED_PATHS
from capabilities.governance.ocr_provider_selection_dependency_environment_planning_v1 import (
    BOUNDARY_FALSE,
    DEPENDENCY_CHECKS_PLANNED,
    FINAL_DECISION_GO,
    HEALTH_BINDINGS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    PROVIDER_INVENTORY,
    SCOPE,
    SELECTION_CRITERIA,
    SECURITY_CONFIRMATIONS,
)

MIN_CHECKS = 137

REQUIRED = (
    "ocr_provider_selection_dependency_environment_planning_policy_v1.json",
    "authorization_roadmap_input_review_v1.json",
    "ocr_provider_candidate_inventory_v1.json",
    "ocr_provider_selection_criteria_v1.json",
    "paddleocr_dependency_readiness_plan_v1.json",
    "rapidocr_dependency_readiness_plan_v1.json",
    "external_ocr_dependency_readiness_plan_v1.json",
    "local_environment_readiness_plan_v1.json",
    "model_file_and_cache_readiness_plan_v1.json",
    "provider_capability_comparison_matrix_v1.json",
    "provider_cost_latency_resource_matrix_v1.json",
    "provider_health_binding_plan_v1.json",
    "provider_fallback_strategy_plan_v1.json",
    "provider_security_and_boundary_plan_v1.json",
    "provider_selection_dryrun_plan_v1.json",
    "ocr_provider_selection_non_claims_register_v1.json",
    "ocr_provider_selection_planning_decision_v1.json",
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
            "ocr_provider_selection_dependency_environment_planning"
        ),
    )
    p.add_argument(
        "--ocr-controlled-provider-authorization-roadmap-decision-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_controlled_provider_authorization_roadmap_decision"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    roadmap_root = Path(args.ocr_controlled_provider_authorization_roadmap_decision_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "authorization_roadmap_input_review_v1.json")
    inventory = _load(root / "ocr_provider_candidate_inventory_v1.json")
    criteria = _load(root / "ocr_provider_selection_criteria_v1.json")
    paddle = _load(root / "paddleocr_dependency_readiness_plan_v1.json")
    rapid = _load(root / "rapidocr_dependency_readiness_plan_v1.json")
    external = _load(root / "external_ocr_dependency_readiness_plan_v1.json")
    local_env = _load(root / "local_environment_readiness_plan_v1.json")
    health = _load(root / "provider_health_binding_plan_v1.json")
    fallback = _load(root / "provider_fallback_strategy_plan_v1.json")
    security = _load(root / "provider_security_and_boundary_plan_v1.json")
    dryrun_plan = _load(root / "provider_selection_dryrun_plan_v1.json")
    decision = _load(root / "ocr_provider_selection_planning_decision_v1.json")

    roadmap_vr = _load(roadmap_root / "verifier_report.json")
    roadmap_sm = _load(roadmap_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("ocr_provider_selection_dependency_environment_planning_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.roadmap_go", input_review.get("roadmap_verifier_go") is True)
    ok("input.selected_route", input_review.get("selected_route") == SELECTED_ROUTE)
    ok("input.trusted", input_review.get("ocr_candidate_chain_trusted") is True)
    ok("input.readiness4", input_review.get("readiness_count") == 4)
    ok("input.blocked15", input_review.get("blocked_paths_count") == len(BLOCKED_PATHS))

    ok("upstream.roadmap_go", roadmap_vr.get("verifier") == "GO")
    ok("upstream.roadmap_final", roadmap_sm.get("final_decision") == ROADMAP_FINAL)
    ok("upstream.selected", roadmap_sm.get("selected_route") == SELECTED_ROUTE)

    ok("inventory.count", inventory.get("candidate_count") == 4)
    families = {c.get("provider_family") for c in inventory.get("candidates") or []}
    for fam in ("mock_or_fixture", "paddleocr_later", "rapidocr_later", "external_ocr_later"):
        ok(f"inventory.family.{fam}", fam in families)

    for i, cand in enumerate(PROVIDER_INVENTORY):
        inv = (inventory.get("candidates") or [])[i] if i < len(inventory.get("candidates") or []) else {}
        ok(f"inventory.{cand['provider_family']}.invocation", inv.get("invocation_allowed") is False)
        ok(f"inventory.{cand['provider_family']}.status", inv.get("provider_status") == "planned_candidate")

    ok("criteria.count", criteria.get("dimension_count") == len(SELECTION_CRITERIA))
    for dim in SELECTION_CRITERIA:
        ok(f"criteria.dim.{dim}", dim in (criteria.get("dimensions") or []))

    for plan_name, plan in (("paddle", paddle), ("rapid", rapid), ("external", external)):
        ok(f"dep.{plan_name}.planned_only", plan.get("planning_only") is True)
        for chk in DEPENDENCY_CHECKS_PLANNED:
            ok(f"dep.{plan_name}.{chk}", chk in (plan.get("checks_planned") or []))
        ok(f"dep.{plan_name}.no_exec", plan.get("dependency_check_executed_now") is False)
        ok(f"dep.{plan_name}.no_import", plan.get("import_check_executed_now") is False)
        ok(f"dep.{plan_name}.no_invoke", plan.get("provider_invoked_now") is False)

    ok("env.no_network_default", local_env.get("no_network_dependency_by_default") is True)
    ok("env.sandbox", local_env.get("sandbox_boundary") == "evaluation_governance_only")
    ok("env.no_prod_write", local_env.get("no_production_path_write") is True)
    ok("env.check_not_executed", local_env.get("environment_readiness_check_executed_now") is False)

    ok("health.bindings", len(health.get("bindings") or []) == len(HEALTH_BINDINGS))
    ok("fallback.no_auto", fallback.get("no_automatic_switch_execution") is True)
    ok("fallback.mock", fallback.get("fallback_to_mock_or_fixture") is True)
    ok("fallback.visual", fallback.get("fallback_to_visual_candidate") is True)

    for key in SECURITY_CONFIRMATIONS:
        ok(f"security.{key}", security.get("confirmations", {}).get(key) is True)

    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE_GO)
    ok("decision.ready", decision.get("ready_for_dryrun") is True)

    ok("summary.no_paddle", summary.get("paddleocr_invoked_now") is False)
    ok("summary.no_install", summary.get("dependency_install_executed_now") is False)
    ok("summary.no_download", summary.get("model_download_executed_now") is False)
    ok("summary.no_finalize", summary.get("provider_selection_finalized_now") is False)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "ocr_provider_selection_non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

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
