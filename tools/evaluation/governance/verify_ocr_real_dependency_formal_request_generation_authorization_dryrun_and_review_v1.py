#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Formal Request Generation Authorization DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.capability_factory_authorization_standard_extension_planning_v1 import (
    AUTHORIZATION_STANDARD_ID,
)
from capabilities.governance.ocr_real_dependency_formal_execution_request_generation_post_route_decision_v1 import (
    FINAL_DECISION_GO as POST_ROUTE_FINAL,
    SELECTED_ROUTE,
)
from capabilities.governance.ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review_v1 import (
    ABSORBED_PHASE_LABELS,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    FINAL_DECISION_GO,
    FUTURE_EVIDENCE_ITEMS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    UPSTREAM_POST_ROUTE_FINAL,
    UPSTREAM_POST_ROUTE_NEXT,
    VALIDATION_GATES_PLANNED,
)

MIN_CHECKS = 110

REQUIRED = (
    "formal_request_generation_authorization_dryrun_review_policy_v1.json",
    "post_route_decision_input_review_v1.json",
    "formal_execution_request_candidate_input_review_v1.json",
    "formal_request_generation_authorization_candidate_v1.json",
    "owner_operator_approval_precheck_candidate_v1.json",
    "evidence_readiness_candidate_v1.json",
    "validation_gate_readiness_candidate_v1.json",
    "final_preflight_readiness_candidate_v1.json",
    "compressed_authorization_chain_integration_review_v1.json",
    "legacy_phase_absorption_marker_v1.json",
    "formal_request_generation_authorization_boundary_audit_v1.json",
    "formal_request_generation_authorization_blocked_path_result_v1.json",
    "formal_request_generation_authorization_closure_decision_v1.json",
    "next_phase_readiness_decision_v1.json",
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
            "ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--post-route-decision-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_formal_execution_request_generation_post_route_decision"
        ),
    )
    p.add_argument(
        "--formal-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_formal_execution_request_generation_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    post_root = Path(args.post_route_decision_root)
    formal_dr_root = Path(args.formal_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    post_vr = _load(post_root / "verifier_report.json")
    post_sm = _load(post_root / "summary.json")
    formal_cand = _load(formal_dr_root / "formal_execution_request_candidate_v1.json")

    ok("upstream.post_go", post_vr.get("verifier") == "GO")
    ok("upstream.post_final", post_sm.get("final_decision") == UPSTREAM_POST_ROUTE_FINAL)
    ok("upstream.post_next", post_sm.get("recommended_next_phase") == UPSTREAM_POST_ROUTE_NEXT)
    ok("upstream.route_a", post_sm.get("selected_route") == SELECTED_ROUTE)
    ok("upstream.formal_cand", bool(formal_cand.get("formal_execution_request_candidate_id")))
    ok("upstream.no_artifact", formal_cand.get("formal_artifact_generated_now") is False)

    summary = _load(root / "summary.json")
    policy = _load(root / "formal_request_generation_authorization_dryrun_review_policy_v1.json")
    auth_cand = _load(root / "formal_request_generation_authorization_candidate_v1.json")
    approval = _load(root / "owner_operator_approval_precheck_candidate_v1.json")
    evidence = _load(root / "evidence_readiness_candidate_v1.json")
    gate = _load(root / "validation_gate_readiness_candidate_v1.json")
    preflight = _load(root / "final_preflight_readiness_candidate_v1.json")
    integration = _load(root / "compressed_authorization_chain_integration_review_v1.json")
    legacy = _load(root / "legacy_phase_absorption_marker_v1.json")
    blocked = _load(root / "formal_request_generation_authorization_blocked_path_result_v1.json")
    closure = _load(root / "formal_request_generation_authorization_closure_decision_v1.json")
    next_route = _load(root / "next_phase_readiness_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.dryrun_only", summary.get("formal_request_generation_authorization_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.compressed", summary.get("compressed_merge") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("policy.no_split", policy.get("no_separate_authorization_planning_phase") is True)

    ok("auth.target", auth_cand.get("authorization_target") == "formal_execution_request_generation")
    ok("auth.std", auth_cand.get("factory_authorization_standard_ref") == AUTHORIZATION_STANDARD_ID)
    ok("auth.candidate_only", auth_cand.get("candidate_only") is True)
    ok("auth.no_artifact", auth_cand.get("formal_artifact_generation_allowed_now") is False)
    ok("auth.no_grant", auth_cand.get("grant_allowed_now") is False)

    ok("approval.not_collected", approval.get("approval_collected_now") is False)
    ok("approval.not_skipped", approval.get("approval_skipped_now") is False)
    ok("approval.scope", approval.get("approval_scope") == "formal_request_generation_only")

    ok("evidence.ready", evidence.get("evidence_ready_for_final_preflight") is True)
    ok("evidence.not_collected", evidence.get("evidence_collected_now") is False)
    for ref in (
        "formal_execution_request_candidate_ref",
        "execution_grant_candidate_ref",
        "execution_window_candidate_ref",
        "domain_config_ref",
        "validation_gate_path_ref",
        "allowed_check_plan_ref",
        "rollback_failure_route_ref",
        "evidence_collection_candidate_ref",
    ):
        ok(f"evidence.ref.{ref[:20]}", bool(evidence.get(ref)))

    for g in VALIDATION_GATES_PLANNED:
        ok(f"gate.{g[:15]}", gate.get(g) == "planned" or gate.get("gates_planned", {}).get(g) is True)
    ok("gate.runtime_false", gate.get("validator_runtime_enabled_now") is False)
    ok("gate.not_executed", gate.get("gate_executed_now") is False)

    ok("preflight.pass", preflight.get("readiness_pass") is True)
    ok("integration.pass", integration.get("dryrun_and_review_pass") is True)
    ok("integration.deprecated", integration.get("old_multi_step_request_generation_path_deprecated_for_new_phase") is True)
    ok("integration.read_only", integration.get("historical_evidence_remains_read_only_evidence_source") is True)
    for label in ABSORBED_PHASE_LABELS:
        ok(f"absorbed.{label[:15]}", any(
            a.get("phase_label") == label for a in (integration.get("absorbed_phases") or [])
        ))

    ok("legacy.absorbed_by", legacy.get("absorbed_by") == "FormalRequestGenerationAuthorizationDryRunAndReview")
    ok("legacy.deprecated", legacy.get("deprecated_for_new_phase") is True)
    ok("legacy.no_delete", legacy.get("physical_delete_allowed") is False)
    ok("legacy.verdict_preserved", legacy.get("historical_verdict_preserved") is True)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count24", blocked.get("blocked_count") == 24)
    blocked_ids = {b.get("blocked_path") for b in blocked.get("blocked_paths") or []}
    for bp in BLOCKED_PATHS:
        ok(f"blocked.{bp}", bp in blocked_ids)

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("next.preflight", next_route.get("ready_for_execution_final_preflight") is True)
    ok("next.no_exec", next_route.get("ready_for_minimal_controlled_execution") is False)

    for field in BOUNDARY_TRUE:
        ok(f"boundary_true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary_false.{field}", summary.get(field) is False)

    ok("evidence.items17", len(FUTURE_EVIDENCE_ITEMS) == 17)
    for item in FUTURE_EVIDENCE_ITEMS:
        ok(f"future.{item[:18]}", item in (evidence.get("future_evidence_items") or []))

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    pass_all = summary.get("dryrun_and_review_pass") is True
    go = passed >= MIN_CHECKS and pass_all and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "dryrun_and_review_pass": pass_all,
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "compressed_merge": True,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_total": total}, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
