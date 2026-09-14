#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Provider Authorization Formal Request Artifact Generation Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.ocr_provider_authorization_planning_v1 import (
    AUTHORIZATION_SCOPE_COVERED,
)
from capabilities.governance.ocr_provider_authorization_request_dryrun_v1 import (
    CURRENT_REQUEST_DRYRUN_STATE,
)
from capabilities.governance.ocr_provider_authorization_request_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as REQUEST_POST_REVIEW_FINAL,
    NEXT_PHASE_GO as REQUEST_POST_REVIEW_NEXT,
)
from capabilities.governance.ocr_provider_authorization_formal_request_artifact_generation_planning_v1 import (
    ARTIFACT_SCHEMA_VERSION,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    CURRENT_LIFECYCLE_STATE,
    FINAL_DECISION_GO,
    FORMAL_SCHEMA_STATE,
    GENERATION_POLICY_VERSION,
    GENERATION_RULES,
    LIFECYCLE_STATES,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    SEND_PRECHECK_REQUIREMENTS,
    VALIDATION_RULES,
)

MIN_CHECKS = 90

REQUIRED = (
    "formal_request_artifact_generation_planning_policy_v1.json",
    "request_post_dryrun_review_input_review_v1.json",
    "formal_request_artifact_schema_v1.json",
    "formal_request_artifact_generation_rule_v1.json",
    "formal_request_artifact_field_source_map_v1.json",
    "formal_request_artifact_validation_rule_v1.json",
    "formal_request_artifact_versioning_policy_v1.json",
    "formal_request_artifact_signature_placeholder_policy_v1.json",
    "formal_request_artifact_storage_boundary_plan_v1.json",
    "formal_request_artifact_lifecycle_plan_v1.json",
    "formal_request_artifact_send_precheck_plan_v1.json",
    "formal_request_artifact_blocked_path_matrix_v1.json",
    "formal_request_artifact_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "formal_request_artifact_generation_planning_decision_v1.json",
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
            "ocr_provider_authorization_formal_request_artifact_generation_planning"
        ),
    )
    p.add_argument(
        "--ocr-provider-authorization-request-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_provider_authorization_request_post_dryrun_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    post_root = Path(args.ocr_provider_authorization_request_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "request_post_dryrun_review_input_review_v1.json")
    schema = _load(root / "formal_request_artifact_schema_v1.json")
    gen_rules = _load(root / "formal_request_artifact_generation_rule_v1.json")
    field_map = _load(root / "formal_request_artifact_field_source_map_v1.json")
    validation = _load(root / "formal_request_artifact_validation_rule_v1.json")
    versioning = _load(root / "formal_request_artifact_versioning_policy_v1.json")
    signature = _load(root / "formal_request_artifact_signature_placeholder_policy_v1.json")
    storage = _load(root / "formal_request_artifact_storage_boundary_plan_v1.json")
    lifecycle = _load(root / "formal_request_artifact_lifecycle_plan_v1.json")
    send_precheck = _load(root / "formal_request_artifact_send_precheck_plan_v1.json")
    blocked = _load(root / "formal_request_artifact_blocked_path_matrix_v1.json")
    dryrun_plan = _load(root / "formal_request_artifact_dryrun_plan_v1.json")
    decision = _load(root / "formal_request_artifact_generation_planning_decision_v1.json")

    post_vr = _load(post_root / "verifier_report.json")
    post_sm = _load(post_root / "summary.json")
    post_closure = _load(post_root / "authorization_request_closure_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok(
        "summary.planning_only",
        summary.get("ocr_provider_authorization_formal_request_artifact_generation_planning_only") is True,
    )
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.state", summary.get("current_lifecycle_state") == CURRENT_LIFECYCLE_STATE)
    ok("summary.null_provider", summary.get("selected_provider_for_execution") is None)

    ok("upstream.post_go", post_vr.get("verifier") == "GO")
    ok("upstream.post_final", post_sm.get("final_decision") == REQUEST_POST_REVIEW_FINAL)
    ok("upstream.post_next", post_sm.get("recommended_next_phase") == REQUEST_POST_REVIEW_NEXT)
    ok("upstream.closed", post_closure.get("ocr_provider_authorization_request_dryrun_closed") is True)
    ok("upstream.candidate_trusted", post_closure.get("request_artifact_candidate_trusted") is True)
    ok("upstream.prior_state", post_sm.get("current_lifecycle_state") == CURRENT_REQUEST_DRYRUN_STATE)
    ok("input.pass", input_review.get("review_pass") is True)

    ok("schema.type", schema.get("request_type") == "ocr_provider_authorization_request")
    ok("schema.version", schema.get("artifact_version") == ARTIFACT_SCHEMA_VERSION)
    ok("schema.lifecycle", schema.get("lifecycle_state") == FORMAL_SCHEMA_STATE)
    ok("schema.candidate_ref", bool(schema.get("source_request_artifact_candidate_ref")))
    ok("schema.request_ref", bool(schema.get("source_authorization_request_candidate_ref")))
    ok("schema.scope5", len(schema.get("target_scope") or []) == len(AUTHORIZATION_SCOPE_COVERED))
    ok("schema.window_ref", bool(schema.get("requested_execution_window_ref")))
    ok("schema.sandbox_ref", bool(schema.get("sandbox_boundary_ref")))
    ok("schema.rollback_ref", bool(schema.get("rollback_plan_ref")))
    ok("schema.evidence_ref", bool(schema.get("evidence_requirement_ref")))
    ok("schema.owner", schema.get("owner_operator_approval_required") is True)
    ok("schema.verifier", schema.get("verifier_required") is True)
    ok("schema.post_review", schema.get("post_execution_review_required") is True)
    ok("schema.no_gen", schema.get("generated_now") is False)
    ok("schema.no_persist", schema.get("persisted_now") is False)
    ok("schema.no_sent", schema.get("sent_now") is False)
    ok("schema.no_approved", schema.get("approved_now") is False)

    ok("gen_rules.count10", gen_rules.get("rule_count") == len(GENERATION_RULES))
    ok("gen_rules.trusted", gen_rules.get("source_request_artifact_candidate_trusted") is True)
    ok("gen_rules.post_go", gen_rules.get("post_dryrun_review_go") is True)
    ok("gen_rules.no_gen_now", gen_rules.get("artifact_generation_allowed_now") is False)
    ok("gen_rules.future_phase", gen_rules.get("requires_explicit_future_generation_phase") is True)

    ok("field_map.count8", field_map.get("binding_count") == 8)
    ok("field_map.bindings8", len(field_map.get("bindings") or []) == 8)

    ok("validation.count10", validation.get("rule_count") == len(VALIDATION_RULES))
    ok("validation.blocked", validation.get("formal_artifact_generation_blocked_in_planning") is True)

    ok("versioning.schema", versioning.get("artifact_schema_version") == ARTIFACT_SCHEMA_VERSION)
    ok("versioning.policy", versioning.get("generation_policy_version") == GENERATION_POLICY_VERSION)
    ok("versioning.backward", versioning.get("backward_compatibility_required") is True)
    ok("versioning.bump", versioning.get("version_bump_required_on_schema_change") is True)

    ok("signature.required_later", signature.get("signature_required_later") is True)
    ok("signature.not_now", signature.get("signature_generated_now") is False)
    ok("signature.no_approval", signature.get("approval_collected_now") is False)

    ok("storage.no_persist", storage.get("planning_does_not_persist_artifact") is True)
    ok("storage.no_prod", storage.get("no_production_path_write") is True)
    ok("storage.no_registry", storage.get("no_global_registry_write") is True)
    ok("storage.no_external", storage.get("no_external_transmission") is True)
    ok("storage.persisted_false", storage.get("persisted_now") is False)

    ok("lifecycle.current", lifecycle.get("current_state") == CURRENT_LIFECYCLE_STATE)
    ok("lifecycle.count12", len(lifecycle.get("states") or []) == len(LIFECYCLE_STATES))
    ok("lifecycle.prior", lifecycle.get("prior_request_state") == CURRENT_REQUEST_DRYRUN_STATE)

    ok("precheck.count8", send_precheck.get("requirement_count") == len(SEND_PRECHECK_REQUIREMENTS))
    ok("precheck.no_send", send_precheck.get("send_allowed_now") is False)

    ok("blocked.count17", blocked.get("path_count") == len(BLOCKED_PATHS))
    ok("blocked.all", blocked.get("all_blocked") is True)

    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE_GO)
    ok("decision.ready", decision.get("ready_for_dryrun") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)

    ok("summary.no_formal", summary.get("formal_request_artifact_generated_now") is False)
    ok("summary.no_persist", summary.get("formal_request_artifact_persisted_now") is False)
    ok("summary.no_sent", summary.get("authorization_request_sent_now") is False)
    ok("summary.no_approved", summary.get("authorization_request_approved_now") is False)
    ok("summary.no_grant", summary.get("grant_issued_now") is False)
    ok("summary.no_window", summary.get("execution_window_opened_now") is False)
    ok("summary.no_real_dep", summary.get("real_dependency_check_executed_now") is False)

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
