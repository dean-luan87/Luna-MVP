#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Capability Factory Admission and Operation Standard DryRunAndReview v1."""

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
    BOUNDARY_FALSE,
    COMPRESSED_PATH,
    COVERAGE_MATRIX_ITEMS,
    DRYRUN_NON_CLAIMS,
    FINAL_DECISION_GO,
    MERGEABLE_OCR_AUTHORIZATION_PHASES,
    NEXT_PHASE_GO,
    PHASE_ID,
    SCOPE,
    STANDALONE_AUTHORIZATION_PHASES,
)
from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    BOUNDARY_STANDARD_BLOCKED,
    FINAL_DECISION_GO as PLANNING_FINAL,
    LIFECYCLE_STATES,
    NEXT_PHASE_GO as PLANNING_NEXT,
    STANDARD_ID,
)
from capabilities.governance.ocr_provider_authorization_formal_request_artifact_generation_planning_v1 import (
    CURRENT_LIFECYCLE_STATE as FORMAL_PLANNING_STATE,
    FINAL_DECISION_GO as FORMAL_PLANNING_FINAL,
)
from capabilities.governance.ocr_provider_authorization_request_dryrun_v1 import (
    CURRENT_REQUEST_DRYRUN_STATE,
)
from capabilities.governance.ocr_provider_authorization_request_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as REQUEST_POST_REVIEW_FINAL,
)

MIN_CHECKS = 100

REQUIRED = (
    "capability_factory_standard_dryrun_and_review_policy_v1.json",
    "factory_standard_planning_input_review_v1.json",
    "candidate_standard_dryrun_review_v1.json",
    "artifact_standard_dryrun_review_v1.json",
    "lifecycle_standard_dryrun_review_v1.json",
    "boundary_standard_dryrun_review_v1.json",
    "evidence_standard_dryrun_review_v1.json",
    "approval_grant_standard_dryrun_review_v1.json",
    "sandbox_rollback_standard_dryrun_review_v1.json",
    "provider_machine_standard_dryrun_review_v1.json",
    "upstream_downstream_transfer_standard_dryrun_review_v1.json",
    "factory_role_responsibility_standard_review_v1.json",
    "ocr_authorization_chain_coverage_matrix_v1.json",
    "compressed_authorization_lifecycle_dryrun_result_v1.json",
    "compression_impact_review_v1.json",
    "factory_standard_boundary_audit_v1.json",
    "factory_standard_adoption_readiness_decision_v1.json",
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
            "capability_factory_admission_and_operation_standard_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--capability-factory-admission-and-operation-standard-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "capability_factory_admission_and_operation_standard_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    planning_root = Path(args.capability_factory_admission_and_operation_standard_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "factory_standard_planning_input_review_v1.json")
    candidate_r = _load(root / "candidate_standard_dryrun_review_v1.json")
    artifact_r = _load(root / "artifact_standard_dryrun_review_v1.json")
    lifecycle_r = _load(root / "lifecycle_standard_dryrun_review_v1.json")
    boundary_r = _load(root / "boundary_standard_dryrun_review_v1.json")
    evidence_r = _load(root / "evidence_standard_dryrun_review_v1.json")
    approval_r = _load(root / "approval_grant_standard_dryrun_review_v1.json")
    sandbox_r = _load(root / "sandbox_rollback_standard_dryrun_review_v1.json")
    provider_r = _load(root / "provider_machine_standard_dryrun_review_v1.json")
    transfer_r = _load(root / "upstream_downstream_transfer_standard_dryrun_review_v1.json")
    roles_r = _load(root / "factory_role_responsibility_standard_review_v1.json")
    coverage = _load(root / "ocr_authorization_chain_coverage_matrix_v1.json")
    compressed = _load(root / "compressed_authorization_lifecycle_dryrun_result_v1.json")
    compression_r = _load(root / "compression_impact_review_v1.json")
    audit = _load(root / "factory_standard_boundary_audit_v1.json")
    readiness = _load(root / "factory_standard_adoption_readiness_decision_v1.json")

    plan_vr = _load(planning_root / "verifier_report.json")
    plan_sm = _load(planning_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_review", summary.get("capability_factory_standard_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.standard_id", summary.get("standard_id") == STANDARD_ID)
    ok("summary.nine", summary.get("nine_standards_validated") is True)
    ok("summary.coverage", summary.get("ocr_chain_coverage") is True)
    ok("summary.compression", summary.get("compression_validated") is True)

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("upstream.plan_next", plan_sm.get("recommended_next_phase") == PLANNING_NEXT)
    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.compression", input_review.get("compression_supersedes_long_chain") is True)

    ok("candidate.pass", candidate_r.get("dryrun_and_review_pass") is True)
    ok("artifact.pass", artifact_r.get("dryrun_and_review_pass") is True)
    ok("lifecycle.pass", lifecycle_r.get("dryrun_and_review_pass") is True)
    ok("lifecycle.count13", lifecycle_r.get("state_count") == len(LIFECYCLE_STATES))
    ok("lifecycle.req_state", CURRENT_REQUEST_DRYRUN_STATE in (lifecycle_r.get("allowed_current_states") or []))
    ok("lifecycle.formal_state", FORMAL_PLANNING_STATE in (lifecycle_r.get("allowed_current_states") or []))
    ok("boundary.pass", boundary_r.get("dryrun_and_review_pass") is True)
    ok("boundary.count11", boundary_r.get("path_count") == len(BOUNDARY_STANDARD_BLOCKED))
    ok("evidence.pass", evidence_r.get("dryrun_and_review_pass") is True)
    ok("approval.pass", approval_r.get("dryrun_and_review_pass") is True)
    ok("sandbox.pass", sandbox_r.get("dryrun_and_review_pass") is True)
    ok("provider.pass", provider_r.get("dryrun_and_review_pass") is True)
    ok("transfer.pass", transfer_r.get("dryrun_and_review_pass") is True)
    ok("roles.pass", roles_r.get("dryrun_and_review_pass") is True)
    ok("roles.count5", roles_r.get("role_count") >= 5)

    ok("coverage.all", coverage.get("all_covered") is True)
    ok("coverage.count13", coverage.get("items_total") == len(COVERAGE_MATRIX_ITEMS))

    ok("compressed.pass", compressed.get("dryrun_pass") is True)
    ok("compressed.path7", len(compressed.get("compressed_path") or []) == len(COMPRESSED_PATH))
    ok("compressed.no_formal", compressed.get("formal_request_artifact_generated_now") is False)
    ok("compressed.no_sent", compressed.get("request_sent_now") is False)
    ok("compressed.no_grant", compressed.get("grant_issued_now") is False)
    ok("compressed.no_window", compressed.get("execution_window_opened_now") is False)
    ok("compressed.no_invoke", compressed.get("provider_invoked_now") is False)

    ok("compression.pass", compression_r.get("dryrun_and_review_pass") is True)
    ok("compression.formal", compression_r.get("formal_artifact_triple_compressible") is True)
    ok("compression.send", compression_r.get("send_triple_compressible") is True)
    ok("compression.grant", compression_r.get("grant_triple_compressible") is True)
    ok("compression.merge9", len(compression_r.get("mergeable_phases") or []) == len(MERGEABLE_OCR_AUTHORIZATION_PHASES))
    ok("compression.standalone4", len(compression_r.get("standalone_still_required") or []) == len(STANDALONE_AUTHORIZATION_PHASES))

    ok("audit.pass", audit.get("audit_pass") is True)

    ok("readiness.all", readiness.get("all_pass") is True)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION_GO)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("readiness.no_resume", readiness.get("do_not_resume_formal_artifact_triple_chain") is True)

    ok("summary.no_runtime", summary.get("factory_standard_runtime_enforced_now") is False)
    ok("summary.no_formal", summary.get("formal_request_artifact_generated_now") is False)
    ok("summary.no_persist", summary.get("formal_request_artifact_persisted_now") is False)
    ok("summary.no_sent", summary.get("authorization_request_sent_now") is False)
    ok("summary.no_grant", summary.get("grant_issued_now") is False)
    ok("summary.no_window", summary.get("execution_window_opened_now") is False)
    ok("summary.no_invoke", summary.get("provider_invoked_now") is False)
    ok("summary.no_real_dep", summary.get("real_dependency_check_executed_now") is False)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("formal.planning_final", FORMAL_PLANNING_FINAL == "OCR_PROVIDER_AUTHORIZATION_FORMAL_REQUEST_ARTIFACT_GENERATION_PLANNING_READY_FOR_DRYRUN")
    ok("req.post_final", REQUEST_POST_REVIEW_FINAL is not None)
    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(DRYRUN_NON_CLAIMS))

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
