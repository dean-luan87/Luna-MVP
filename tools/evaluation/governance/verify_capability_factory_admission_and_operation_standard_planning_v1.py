#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Capability Factory Admission and Operation Standard Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_STANDARD_BLOCKED,
    COMPRESSED_PATH,
    FINAL_DECISION_GO,
    LIFECYCLE_STATES,
    MERGEABLE_OCR_AUTHORIZATION_PHASES,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    SOURCE_PHASE_INVENTORY,
    STANDALONE_AUTHORIZATION_PHASES,
    STANDARD_ID,
)
from capabilities.governance.ocr_provider_authorization_dryrun_v1 import (
    EVIDENCE_REQUIREMENTS as OCR_EVIDENCE,
)
from capabilities.governance.ocr_provider_authorization_request_dryrun_v1 import (
    CURRENT_REQUEST_DRYRUN_STATE,
)
from capabilities.governance.ocr_provider_authorization_request_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as REQUEST_POST_REVIEW_FINAL,
)

MIN_CHECKS = 95

REQUIRED = (
    "capability_factory_standard_planning_policy_v1.json",
    "source_phase_rule_inventory_v1.json",
    "candidate_standard_plan_v1.json",
    "artifact_standard_plan_v1.json",
    "lifecycle_standard_plan_v1.json",
    "boundary_standard_plan_v1.json",
    "evidence_standard_plan_v1.json",
    "approval_grant_standard_plan_v1.json",
    "sandbox_rollback_standard_plan_v1.json",
    "provider_machine_standard_plan_v1.json",
    "upstream_downstream_transfer_standard_plan_v1.json",
    "factory_role_responsibility_standard_plan_v1.json",
    "factory_standard_contract_outline_v1.json",
    "factory_standard_adoption_plan_v1.json",
    "compression_impact_assessment_v1.json",
    "non_claims_register_v1.json",
    "capability_factory_standard_planning_decision_v1.json",
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
            "capability_factory_admission_and_operation_standard_planning"
        ),
    )
    p.add_argument(
        "--ocr-provider-authorization-request-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_provider_authorization_request_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    req_post_root = Path(args.ocr_provider_authorization_request_post_dryrun_review_root)
    factory_post_root = Path(
        args.controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
    )
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    inventory = _load(root / "source_phase_rule_inventory_v1.json")
    candidate = _load(root / "candidate_standard_plan_v1.json")
    artifact = _load(root / "artifact_standard_plan_v1.json")
    lifecycle = _load(root / "lifecycle_standard_plan_v1.json")
    boundary = _load(root / "boundary_standard_plan_v1.json")
    evidence = _load(root / "evidence_standard_plan_v1.json")
    approval = _load(root / "approval_grant_standard_plan_v1.json")
    sandbox = _load(root / "sandbox_rollback_standard_plan_v1.json")
    provider = _load(root / "provider_machine_standard_plan_v1.json")
    transfer = _load(root / "upstream_downstream_transfer_standard_plan_v1.json")
    roles = _load(root / "factory_role_responsibility_standard_plan_v1.json")
    outline = _load(root / "factory_standard_contract_outline_v1.json")
    adoption = _load(root / "factory_standard_adoption_plan_v1.json")
    compression = _load(root / "compression_impact_assessment_v1.json")
    decision = _load(root / "capability_factory_standard_planning_decision_v1.json")

    req_post_vr = _load(req_post_root / "verifier_report.json")
    req_post_sm = _load(req_post_root / "summary.json")
    req_post_closure = _load(req_post_root / "authorization_request_closure_decision_v1.json")
    factory_post_vr = _load(factory_post_root / "verifier_report.json")
    factory_closure = _load(factory_post_root / "factory_registration_closure_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("capability_factory_standard_planning_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.standard_id", summary.get("standard_id") == STANDARD_ID)
    ok("summary.nine", summary.get("nine_standard_count") == 9)

    ok("upstream.req_post_go", req_post_vr.get("verifier") == "GO")
    ok("upstream.req_post_final", req_post_sm.get("final_decision") == REQUEST_POST_REVIEW_FINAL)
    ok("upstream.req_closed", req_post_closure.get("ocr_provider_authorization_request_dryrun_closed") is True)
    ok("upstream.candidate_trusted", req_post_closure.get("request_artifact_candidate_trusted") is True)
    ok("upstream.lifecycle", req_post_sm.get("current_lifecycle_state") == CURRENT_REQUEST_DRYRUN_STATE)
    ok("upstream.factory_go", factory_post_vr.get("verifier") == "GO")
    ok("upstream.seventh_module", factory_closure.get("controlled_provider_readiness_harness_seventh_module_candidate_trusted") is True)

    ok("inventory.count8", inventory.get("source_phase_count") == len(SOURCE_PHASE_INVENTORY))
    ok("inventory.categories9", len(inventory.get("rule_category_coverage") or []) >= 9)

    ok("candidate.only", candidate.get("candidate_only") is True)
    ok("candidate.not_fact", candidate.get("fact_status") == "not_fact")
    ok("candidate.no_write", candidate.get("write_allowed") is False)
    ok("candidate.no_user", candidate.get("user_facing_output_allowed") is False)
    ok("candidate.source_chain", candidate.get("source_chain_required") is True)
    ok("candidate.ttl", candidate.get("ttl_required") is True)
    ok("candidate.validation", candidate.get("validation_required_before_promotion") is True)

    ok("artifact.candidate_ne_formal", artifact.get("candidate_not_formal_artifact") is True)
    ok("artifact.explicit_phase", artifact.get("formal_artifact_generation_requires_explicit_phase") is True)
    ok("artifact.gen_ne_persist", artifact.get("generated_artifact_not_persisted") is True)
    ok("artifact.persist_ne_sent", artifact.get("persisted_artifact_not_sent") is True)
    ok("artifact.fields4", len(artifact.get("required_fields") or []) == 4)

    ok("lifecycle.count13", lifecycle.get("state_count") == len(LIFECYCLE_STATES))
    ok("lifecycle.states13", len(lifecycle.get("states") or []) == len(LIFECYCLE_STATES))
    ok("lifecycle.auth_state", lifecycle.get("current_authorization_state") == CURRENT_REQUEST_DRYRUN_STATE)

    ok("boundary.count11", boundary.get("path_count") == len(BOUNDARY_STANDARD_BLOCKED))
    ok("boundary.all", boundary.get("all_blocked_by_default") is True)
    ok("boundary.defaults8", len(boundary.get("factory_default_denials") or []) >= 8)

    ok("evidence.types8", len(evidence.get("required_artifact_types") or []) == 8)
    ok("evidence.ocr11", len(evidence.get("ocr_authorization_artifacts") or []) == len(OCR_EVIDENCE))

    ok("approval.later", approval.get("approval_required_later") is True)
    ok("approval.not_now", approval.get("approval_collected_now") is False)
    ok("approval.grant_chain", approval.get("grant_candidate_not_grant_issued") is True)
    ok("approval.revocation", approval.get("revocation_condition_required") is True)

    ok("sandbox.no_prod", sandbox.get("no_production_path_write") is True)
    ok("sandbox.workspace", sandbox.get("workspace_controlled_output_only") is True)
    ok("sandbox.no_env", sandbox.get("no_global_env_mutation") is True)
    ok("sandbox.rollback_req", sandbox.get("rollback_required_before_execution") is True)
    ok("sandbox.not_now", sandbox.get("rollback_executed_now") is False)

    ok("provider.status", provider.get("provider_status") == "planned_candidate")
    ok("provider.no_invoke", provider.get("invocation_allowed") is False)
    ok("provider.dep", provider.get("dependency_check_required") is True)
    ok("provider.constitution", provider.get("constitution_gate_required") is True)
    ok("provider.consumers3", len(provider.get("validated_consumers") or []) == 3)
    ok("provider.seventh", provider.get("seventh_module_candidate") == "controlled_provider_readiness_harness_v1")

    ok("transfer.upstream", transfer.get("upstream_input_contract_required") is True)
    ok("transfer.downstream", transfer.get("downstream_output_contract_required") is True)
    ok("transfer.no_user", transfer.get("no_direct_downstream_user_output") is True)
    ok("transfer.no_fact", transfer.get("no_direct_fact_write_path") is True)
    ok("transfer.market", transfer.get("market_validation_required") is True)
    ok("transfer.vf_pass", transfer.get("validation_factory_pass_required_before_midplatform_consumption") is True)

    ok("roles.count5", len(roles.get("roles") or []) == 5)
    ok("outline.nine", len(outline.get("nine_standards") or []) == 9)
    ok("outline.covers3", len(outline.get("covers") or []) == 3)

    ok("adoption.harness", adoption.get("adopt_via_lifecycle_harness") is True)
    ok("adoption.merged", adoption.get("dryrun_and_review_merged") is True)
    ok("adoption.next", adoption.get("next_phase") == NEXT_PHASE_GO)

    ok("compression.merge9", compression.get("mergeable_phase_count") == len(MERGEABLE_OCR_AUTHORIZATION_PHASES))
    ok("compression.defaults7", len(compression.get("factory_level_defaults") or []) >= 7)
    ok("compression.standalone4", len(compression.get("standalone_authorization_still_required") or []) == len(STANDALONE_AUTHORIZATION_PHASES))
    ok("compression.path7", len(compression.get("proposed_compressed_path") or []) == len(COMPRESSED_PATH))

    ok("decision.ready", decision.get("ready_for_dryrun_and_review") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)

    ok("summary.no_standard", summary.get("factory_standard_generated_now") is False)
    ok("summary.no_runtime", summary.get("factory_standard_runtime_enforced_now") is False)
    ok("summary.no_formal", summary.get("formal_request_artifact_generated_now") is False)
    ok("summary.no_sent", summary.get("authorization_request_sent_now") is False)
    ok("summary.no_grant", summary.get("grant_issued_now") is False)
    ok("summary.no_window", summary.get("execution_window_opened_now") is False)
    ok("summary.no_invoke", summary.get("provider_invoked_now") is False)
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
