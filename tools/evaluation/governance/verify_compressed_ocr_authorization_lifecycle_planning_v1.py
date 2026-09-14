#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Compressed OCR Authorization Lifecycle Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.capability_factory_admission_and_operation_standard_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FACTORY_DR_FINAL,
)
from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    COMPRESSED_PATH,
    STANDARD_ID,
)
from capabilities.governance.compressed_ocr_authorization_lifecycle_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_MATRIX_BLOCKED,
    CURRENT_STATE,
    EVIDENCE_FIELDS,
    FACTORY_STANDARDS_REQUIRED,
    FINAL_DECISION_GO,
    LIFECYCLE_STATES,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    SELECTED_ROUTE,
)
from capabilities.governance.compressed_ocr_authorization_roadmap_decision_v1 import (
    FINAL_DECISION_GO as ROADMAP_FINAL,
    NEXT_PHASE_GO as ROADMAP_NEXT,
)
from capabilities.governance.ocr_provider_authorization_formal_request_artifact_generation_planning_v1 import (
    FINAL_DECISION_GO as FORMAL_PLANNING_FINAL,
)
from capabilities.governance.ocr_provider_authorization_request_dryrun_v1 import (
    CURRENT_REQUEST_DRYRUN_STATE,
)
from capabilities.governance.ocr_provider_authorization_request_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as REQUEST_POST_REVIEW_FINAL,
)

MIN_CHECKS = 90

REQUIRED = (
    "compressed_ocr_authorization_lifecycle_planning_policy_v1.json",
    "compressed_ocr_authorization_roadmap_input_review_v1.json",
    "factory_standard_adoption_input_review_v1.json",
    "compressed_authorization_lifecycle_contract_v1.json",
    "compressed_authorization_state_machine_v1.json",
    "request_candidate_stage_contract_v1.json",
    "formal_artifact_candidate_stage_contract_v1.json",
    "send_candidate_stage_contract_v1.json",
    "grant_candidate_stage_contract_v1.json",
    "execution_window_candidate_stage_contract_v1.json",
    "review_stage_contract_v1.json",
    "compressed_lifecycle_boundary_matrix_v1.json",
    "compressed_lifecycle_evidence_requirement_v1.json",
    "compressed_lifecycle_approval_grant_policy_v1.json",
    "compressed_lifecycle_sandbox_rollback_policy_v1.json",
    "compressed_lifecycle_validation_factory_binding_v1.json",
    "compressed_lifecycle_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "compressed_lifecycle_planning_decision_v1.json",
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
            "compressed_ocr_authorization_lifecycle_planning"
        ),
    )
    p.add_argument(
        "--compressed-ocr-authorization-roadmap-decision-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "compressed_ocr_authorization_roadmap_decision"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    roadmap_root = Path(args.compressed_ocr_authorization_roadmap_decision_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    roadmap_review = _load(root / "compressed_ocr_authorization_roadmap_input_review_v1.json")
    factory_input = _load(root / "factory_standard_adoption_input_review_v1.json")
    lifecycle_contract = _load(root / "compressed_authorization_lifecycle_contract_v1.json")
    state_machine = _load(root / "compressed_authorization_state_machine_v1.json")
    req_stage = _load(root / "request_candidate_stage_contract_v1.json")
    formal_stage = _load(root / "formal_artifact_candidate_stage_contract_v1.json")
    send_stage = _load(root / "send_candidate_stage_contract_v1.json")
    grant_stage = _load(root / "grant_candidate_stage_contract_v1.json")
    window_stage = _load(root / "execution_window_candidate_stage_contract_v1.json")
    review_stage = _load(root / "review_stage_contract_v1.json")
    boundary_matrix = _load(root / "compressed_lifecycle_boundary_matrix_v1.json")
    evidence_req = _load(root / "compressed_lifecycle_evidence_requirement_v1.json")
    approval_policy = _load(root / "compressed_lifecycle_approval_grant_policy_v1.json")
    sandbox_policy = _load(root / "compressed_lifecycle_sandbox_rollback_policy_v1.json")
    vf_binding = _load(root / "compressed_lifecycle_validation_factory_binding_v1.json")
    dryrun_plan = _load(root / "compressed_lifecycle_dryrun_plan_v1.json")
    planning_decision = _load(root / "compressed_lifecycle_planning_decision_v1.json")

    roadmap_vr = _load(roadmap_root / "verifier_report.json")
    roadmap_sm = _load(roadmap_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("compressed_ocr_authorization_lifecycle_planning_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.current_state", summary.get("current_state") == CURRENT_STATE)
    ok("summary.route", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.standard_id", summary.get("standard_id") == STANDARD_ID)

    ok("upstream.roadmap_go", roadmap_vr.get("verifier") == "GO")
    ok("upstream.roadmap_final", roadmap_sm.get("final_decision") == ROADMAP_FINAL)
    ok("upstream.roadmap_next", roadmap_sm.get("recommended_next_phase") == ROADMAP_NEXT)
    ok("roadmap_review.pass", roadmap_review.get("review_pass") is True)
    ok("factory_input.pass", factory_input.get("review_pass") is True)
    ok("factory_input.superseded", factory_input.get("superseded_by_factory_standard") is True)

    ok("contract.steps7", lifecycle_contract.get("step_count") == len(COMPRESSED_PATH))
    ok("contract.all_future", lifecycle_contract.get("all_stages_promotion_requires_future_phase") is True)
    ok("contract.all_not_exec", lifecycle_contract.get("all_stages_executed_now_false") is True)
    stages = lifecycle_contract.get("stages") or []
    ok("contract.stage_count", len(stages) == len(COMPRESSED_PATH))
    for i, step in enumerate(COMPRESSED_PATH):
        ok(f"contract.stage.{i}", stages[i].get("stage_id") == step if i < len(stages) else False)

    ok("state_machine.current", state_machine.get("current_state") == CURRENT_STATE)
    ok("state_machine.states", state_machine.get("states") == list(LIFECYCLE_STATES))

    ok("req_stage.bind_auth", "authorization_request_candidate" in str(req_stage.get("input_contract")))
    ok("req_stage.bind_artifact", "request_artifact_candidate" in str(req_stage.get("input_contract")))
    ok("req_stage.no_new", req_stage.get("output_contract", {}).get("new_request_candidate_generated_now") is False)
    ok("req_stage.no_formal", req_stage.get("output_contract", {}).get("formal_artifact_generated_now") is False)
    ok("req_stage.no_sent", req_stage.get("output_contract", {}).get("request_sent_now") is False)

    ok("formal_stage.later", formal_stage.get("output_contract", {}).get("formal_artifact_candidate_later") is True)
    ok("formal_stage.schema", formal_stage.get("input_contract", {}).get("schema_version_required") is True)
    ok("formal_stage.no_gen", formal_stage.get("output_contract", {}).get("formal_request_artifact_generated_now") is False)
    ok("formal_stage.no_persist", formal_stage.get("output_contract", {}).get("artifact_persisted_now") is False)

    ok("send_stage.precheck", send_stage.get("input_contract", {}).get("send_precheck_required") is True)
    ok("send_stage.approval", send_stage.get("input_contract", {}).get("owner_operator_approval_required") is True)
    ok("send_stage.no_sent", send_stage.get("output_contract", {}).get("authorization_request_sent_now") is False)

    ok("grant_stage.conditions", grant_stage.get("input_contract", {}).get("grant_conditions_required") is True)
    ok("grant_stage.revoke", grant_stage.get("input_contract", {}).get("revocation_condition_required") is True)
    ok("grant_stage.no_grant", grant_stage.get("output_contract", {}).get("grant_issued_now") is False)

    ok("window_stage.sandbox", window_stage.get("input_contract", {}).get("sandbox_required") is True)
    ok("window_stage.rollback", window_stage.get("input_contract", {}).get("rollback_required") is True)
    ok("window_stage.no_open", window_stage.get("output_contract", {}).get("execution_window_opened_now") is False)
    ok("window_stage.no_real_dep", window_stage.get("output_contract", {}).get("real_dependency_check_executed_now") is False)

    ok("review_stage.verifier", review_stage.get("input_contract", {}).get("verifier_required") is True)
    ok("review_stage.closure", review_stage.get("input_contract", {}).get("closure_decision_required") is True)

    ok("boundary.path_count", boundary_matrix.get("path_count") == len(BOUNDARY_MATRIX_BLOCKED))
    ok("boundary.all_blocked", boundary_matrix.get("all_blocked") is True)
    for bp in BOUNDARY_MATRIX_BLOCKED:
        blocked = any(
            r.get("path_id") == bp and r.get("status") == "blocked"
            for r in (boundary_matrix.get("blocked_paths") or [])
        )
        ok(f"boundary.{bp}", blocked)

    ok("evidence.count", evidence_req.get("field_count") == len(EVIDENCE_FIELDS))
    ok("evidence.binding", evidence_req.get("factory_standard_evidence_binding") is True)

    ok("approval.grant_false", approval_policy.get("grant_issued_now") is False)
    ok("sandbox.window_false", sandbox_policy.get("execution_window_opened_now") is False)

    ok("vf.count9", vf_binding.get("standard_count") == len(FACTORY_STANDARDS_REQUIRED))
    ok("vf.harness", vf_binding.get("harness_factory_module_candidate") is True)
    ok("vf.midplatform_blocked", vf_binding.get("midplatform_consumption_blocked_until_validation_factory_pass") is True)

    ok("dryrun.merged", dryrun_plan.get("dryrun_and_review_merged") is True)
    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE_GO)
    ok("dryrun.no_formal", dryrun_plan.get("formal_request_artifact_generated_now") is False)
    ok("dryrun.no_grant", dryrun_plan.get("grant_issued_now") is False)

    ok("decision.pass", planning_decision.get("planning_pass") is True)
    ok("decision.no_triple", planning_decision.get("formal_artifact_triple_chain_resumed_now") is False)
    ok("decision.final", planning_decision.get("final_decision") == FINAL_DECISION_GO)
    ok("decision.next", planning_decision.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("summary.no_triple", summary.get("formal_artifact_triple_chain_resumed_now") is False)
    ok("summary.no_exec", summary.get("compressed_lifecycle_executed_now") is False)
    ok("summary.no_formal", summary.get("formal_request_artifact_generated_now") is False)
    ok("summary.no_sent", summary.get("authorization_request_sent_now") is False)
    ok("summary.no_grant", summary.get("grant_issued_now") is False)
    ok("summary.no_window", summary.get("execution_window_opened_now") is False)
    ok("summary.no_real_dep", summary.get("real_dependency_check_executed_now") is False)
    ok("summary.null_provider", summary.get("selected_provider_for_execution") is None)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))
    ok("formal.planning_final", FORMAL_PLANNING_FINAL is not None)
    ok("req.post_final", REQUEST_POST_REVIEW_FINAL is not None)
    ok("lifecycle.upstream", CURRENT_REQUEST_DRYRUN_STATE == "request_artifact_candidate_ready")

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
