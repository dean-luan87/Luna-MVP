#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Real Dependency Formal Execution Request Generation DryRunAndReview v1."""

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
from capabilities.governance.ocr_real_dependency_formal_execution_request_generation_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    DRYRUN_VALIDATION_RULE_LABELS,
    FINAL_DECISION_GO,
    FUTURE_EVIDENCE_ITEMS,
    GATE_BINDINGS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    SCOPE_ALLOWED_CHECKS,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
)

MIN_CHECKS = 120

REQUIRED = (
    "formal_execution_request_generation_dryrun_review_policy_v1.json",
    "formal_execution_request_generation_planning_input_review_v1.json",
    "formal_execution_request_candidate_v1.json",
    "formal_execution_request_schema_validation_result_v1.json",
    "formal_execution_request_precondition_dryrun_result_v1.json",
    "formal_execution_request_field_source_map_dryrun_result_v1.json",
    "formal_execution_request_validation_rule_dryrun_result_v1.json",
    "formal_execution_request_versioning_review_v1.json",
    "formal_execution_request_signature_approval_review_v1.json",
    "formal_execution_request_storage_boundary_review_v1.json",
    "formal_execution_request_send_boundary_review_v1.json",
    "formal_execution_request_evidence_binding_review_v1.json",
    "formal_execution_request_validation_gate_binding_review_v1.json",
    "formal_execution_request_boundary_audit_v1.json",
    "formal_execution_request_blocked_path_result_v1.json",
    "formal_execution_request_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)

CANDIDATE_REQUIRED = (
    "formal_execution_request_candidate_id",
    "request_type",
    "artifact_version",
    "lifecycle_state",
    "provider_domain",
    "authorization_target",
    "source_execution_authorization_request_candidate_ref",
    "source_domain_config_ref",
    "factory_authorization_standard_ref",
    "validation_engineering_ref",
    "requested_allowed_checks",
    "forbidden_actions_ref",
    "evidence_collection_ref",
    "rollback_failure_route_ref",
    "execution_window_candidate_ref",
    "execution_grant_candidate_ref",
    "validation_gate_path_ref",
    "owner_operator_approval_required",
    "verifier_required",
    "post_execution_review_required",
    "candidate_only",
    "formal_artifact_generated_now",
    "persisted_now",
    "sent_now",
    "approved_now",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_formal_execution_request_generation_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--ocr-real-dependency-formal-execution-request-generation-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_formal_execution_request_generation_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.ocr_real_dependency_formal_execution_request_generation_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.plan_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)

    summary = _load(root / "summary.json")
    candidate = _load(root / "formal_execution_request_candidate_v1.json")
    schema_val = _load(root / "formal_execution_request_schema_validation_result_v1.json")
    precond = _load(root / "formal_execution_request_precondition_dryrun_result_v1.json")
    field_map = _load(root / "formal_execution_request_field_source_map_dryrun_result_v1.json")
    rules = _load(root / "formal_execution_request_validation_rule_dryrun_result_v1.json")
    storage = _load(root / "formal_execution_request_storage_boundary_review_v1.json")
    send = _load(root / "formal_execution_request_send_boundary_review_v1.json")
    evidence = _load(root / "formal_execution_request_evidence_binding_review_v1.json")
    gate = _load(root / "formal_execution_request_validation_gate_binding_review_v1.json")
    sig = _load(root / "formal_execution_request_signature_approval_review_v1.json")
    blocked = _load(root / "formal_execution_request_blocked_path_result_v1.json")
    closure = _load(root / "formal_execution_request_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    plan_in = _load(root / "formal_execution_request_generation_planning_input_review_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.dryrun_only", summary.get("formal_execution_request_generation_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.candidate_gen", summary.get("formal_execution_request_candidate_generated_now") is True)
    ok("summary.no_artifact", summary.get("formal_execution_request_artifact_generated_now") is False)

    ok("plan_in.pass", plan_in.get("review_pass") is True)

    ok("cand.lifecycle", candidate.get("lifecycle_state") == "formal_execution_request_candidate_ready")
    ok("cand.std", candidate.get("factory_authorization_standard_ref") == AUTHORIZATION_STANDARD_ID)
    for key in CANDIDATE_REQUIRED:
        ok(f"cand.{key}", key in candidate)
    ok("cand.candidate_only", candidate.get("candidate_only") is True)
    ok("cand.no_artifact", candidate.get("formal_artifact_generated_now") is False)

    ok("schema.pass", schema_val.get("dryrun_and_review_pass") is True)
    ok("precond.pass", precond.get("preconditions_pass") is True)
    ok("precond.dryrun_pass", precond.get("dryrun_and_review_pass") is True)
    ok("field_map.pass", field_map.get("dryrun_and_review_pass") is True)
    ok("field_map.count11", field_map.get("binding_count") == 11)
    ok("rules.pass", rules.get("dryrun_and_review_pass") is True)
    ok("rules.count17", rules.get("rule_count") == 17)
    for label in DRYRUN_VALIDATION_RULE_LABELS:
        ok(f"rule.{label[:25]}", rules.get("rules", {}).get(label) is True)

    ok("storage.pass", storage.get("dryrun_and_review_pass") is True)
    ok("storage.no_persist", storage.get("dryrun_does_not_persist_artifact") is True)
    ok("send.pass", send.get("dryrun_and_review_pass") is True)
    ok("evidence.pass", evidence.get("dryrun_and_review_pass") is True)
    ok("evidence.count17", evidence.get("evidence_count") == 17)
    for item in FUTURE_EVIDENCE_ITEMS:
        ok(f"evidence.item.{item[:20]}", item in (evidence.get("future_evidence_items") or []))

    ok("gate.pass", gate.get("dryrun_and_review_pass") is True)
    ok("gate.runtime_false", gate.get("gate_runtime_enabled_now") is False)
    for g in GATE_BINDINGS:
        ok(f"gate.{g[:15]}", g in (gate.get("gates_required_later") or []))

    ok("sig.not_generated", sig.get("signature_generated_now") is False)
    ok("sig.not_approved", sig.get("approval_collected_now") is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count24", blocked.get("blocked_count") == 24)
    blocked_ids = {b.get("blocked_path") for b in blocked.get("blocked_paths") or []}
    for bp in BLOCKED_PATHS:
        ok(f"blocked.{bp}", bp in blocked_ids)

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("next.ready", next_route.get("ready_for_formal_execution_request_generation_post_route_decision") is True)
    ok("next.no_artifact", next_route.get("ready_for_formal_request_artifact_generation") is False)

    for cid in SCOPE_ALLOWED_CHECKS:
        ok(f"cand.check.{cid}", cid in (candidate.get("requested_allowed_checks") or []))

    for field in BOUNDARY_TRUE:
        ok(f"boundary_true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary_false.{field}", summary.get(field) is False)

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
