#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Provider Selection / Dependency / Environment Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.ocr_provider_selection_dependency_environment_dryrun_v1 import (
    BLOCKED_PATHS,
    FINAL_DECISION_GO as DRYRUN_FINAL,
    NEXT_PHASE_GO as DRYRUN_NEXT,
    SELECTION_CRITERIA,
)
from capabilities.governance.ocr_provider_selection_dependency_environment_post_dryrun_review_v1 import (
    BOUNDARY_FALSE_REVIEW,
    EXPECTED_PROVIDER_FAMILIES,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REVIEW_SCOPE,
)

MIN_CHECKS = 85

REQUIRED = (
    "provider_selection_dependency_environment_dryrun_input_review_v1.json",
    "provider_selection_candidate_review_v1.json",
    "dependency_readiness_candidate_review_v1.json",
    "environment_readiness_candidate_review_v1.json",
    "provider_comparison_matrix_review_v1.json",
    "provider_cost_latency_resource_review_v1.json",
    "provider_capability_fit_review_v1.json",
    "provider_health_binding_review_v1.json",
    "provider_fallback_strategy_review_v1.json",
    "provider_security_boundary_review_v1.json",
    "provider_no_import_no_install_review_v1.json",
    "provider_selection_blocked_path_review_v1.json",
    "provider_selection_dependency_environment_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
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
            "ocr_provider_selection_dependency_environment_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--ocr-provider-selection-dependency-environment-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_provider_selection_dependency_environment_dryrun"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    dryrun_root = Path(args.ocr_provider_selection_dependency_environment_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "provider_selection_dependency_environment_dryrun_input_review_v1.json")
    selection_r = _load(root / "provider_selection_candidate_review_v1.json")
    dependency_r = _load(root / "dependency_readiness_candidate_review_v1.json")
    environment_r = _load(root / "environment_readiness_candidate_review_v1.json")
    comparison_r = _load(root / "provider_comparison_matrix_review_v1.json")
    no_import_r = _load(root / "provider_no_import_no_install_review_v1.json")
    blocked_r = _load(root / "provider_selection_blocked_path_review_v1.json")
    closure = _load(root / "provider_selection_dependency_environment_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    dryrun_sm = _load(dryrun_root / "summary.json")
    dryrun_vr = _load(dryrun_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("review_scope") == REVIEW_SCOPE)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.dryrun_closed", summary.get("ocr_provider_selection_dependency_environment_dryrun_closed") is True)
    ok("summary.trusted", summary.get("provider_selection_candidate_trusted") is True)

    ok("upstream.dryrun_go", dryrun_vr.get("verifier") == "GO")
    ok("upstream.dryrun_final", dryrun_sm.get("final_decision") == DRYRUN_FINAL)
    ok("upstream.dryrun_next", dryrun_sm.get("recommended_next_phase") == DRYRUN_NEXT)
    ok("upstream.simulated", dryrun_sm.get("simulated") is True)
    ok("input.pass", input_review.get("review_pass") is True)

    ok("selection.review_pass", selection_r.get("review_pass") is True)
    ok("selection.null_exec", selection_r.get("selected_provider_for_execution") is None)
    ok("selection.not_finalized", selection_r.get("provider_selection_finalized_now") is False)
    ok("selection.count4", selection_r.get("candidate_count") == 4)

    ok("dependency.review_pass", dependency_r.get("review_pass") is True)
    ok("dependency.rows4", dependency_r.get("row_count") == 4)

    ok("environment.review_pass", environment_r.get("review_pass") is True)

    ok("comparison.review_pass", comparison_r.get("review_pass") is True)
    ok("comparison.dims17", comparison_r.get("dimension_count") == len(SELECTION_CRITERIA))
    ok("comparison.sample_only", comparison_r.get("comparison_is_sample_only") is True)
    ok("comparison.no_finalize", comparison_r.get("comparison_result_does_not_finalize_provider") is True)

    ok("no_import.review_pass", no_import_r.get("review_pass") is True)
    ok("no_import.no_install", no_import_r.get("no_dependency_install") is True)
    ok("no_import.no_download", no_import_r.get("no_model_download") is True)
    ok("no_import.no_import", no_import_r.get("no_provider_import") is True)

    ok("blocked.review_pass", blocked_r.get("review_pass") is True)
    ok("blocked.count15", blocked_r.get("paths_total") == len(BLOCKED_PATHS))
    ok("blocked.all", blocked_r.get("all_blocked") is True)

    ok("closure.closed", closure.get("ocr_provider_selection_dependency_environment_dryrun_closed") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)

    ok("next.ready", next_route.get("ready_for_real_dependency_check_planning") is True)
    ok("next.no_import", next_route.get("do_not_import_provider_now") is True)
    ok("next.no_install", next_route.get("do_not_install_dependency_now") is True)
    ok("next.no_invoke", next_route.get("do_not_invoke_provider_now") is True)

    for fam in EXPECTED_PROVIDER_FAMILIES:
        ok(f"families.{fam}", fam in EXPECTED_PROVIDER_FAMILIES)

    for field in BOUNDARY_FALSE_REVIEW:
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
