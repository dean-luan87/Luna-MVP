#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Real Dependency Formal Execution Request Generation Planning v1."""

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
from capabilities.governance.ocr_real_dependency_execution_authorization_planning_v1 import (
    EVIDENCE_ARTIFACTS,
)
from capabilities.governance.ocr_real_dependency_execution_request_generation_roadmap_decision_v1 import (
    FINAL_DECISION_GO as ROADMAP_FINAL,
    NEXT_PHASE_GO as ROADMAP_NEXT,
    SELECTED_ROUTE,
)
from capabilities.governance.ocr_real_dependency_formal_execution_request_generation_planning_v1 import (
    ARTIFACT_SCHEMA_VERSION,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    FIELD_SOURCE_BINDINGS,
    FINAL_DECISION_GO,
    GATE_BINDINGS,
    GENERATION_POLICY_VERSION,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    SCOPE_ALLOWED_CHECKS,
    UPSTREAM_ROADMAP_FINAL,
    UPSTREAM_ROADMAP_NEXT,
    VALIDATION_RULES,
)

MIN_CHECKS = 100

REQUIRED = (
    "formal_execution_request_generation_planning_policy_v1.json",
    "execution_request_generation_roadmap_input_review_v1.json",
    "formal_execution_request_artifact_schema_v1.json",
    "formal_execution_request_generation_precondition_v1.json",
    "formal_execution_request_field_source_map_v1.json",
    "formal_execution_request_validation_rule_v1.json",
    "formal_execution_request_versioning_policy_v1.json",
    "formal_execution_request_signature_approval_placeholder_v1.json",
    "formal_execution_request_storage_boundary_plan_v1.json",
    "formal_execution_request_send_boundary_plan_v1.json",
    "formal_execution_request_evidence_binding_plan_v1.json",
    "formal_execution_request_validation_gate_binding_plan_v1.json",
    "formal_execution_request_blocked_path_matrix_v1.json",
    "formal_execution_request_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "formal_execution_request_generation_planning_decision_v1.json",
    "summary.json",
)

SCHEMA_REQUIRED = (
    "formal_execution_request_artifact_id",
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
    "generated_now",
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
            "ocr_real_dependency_formal_execution_request_generation_planning"
        ),
    )
    p.add_argument(
        "--ocr-real-dependency-execution-request-generation-roadmap-decision-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_execution_request_generation_roadmap_decision"
        ),
    )
    p.add_argument(
        "--ocr-real-dependency-execution-authorization-dryrun-and-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_execution_authorization_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    roadmap_root = Path(args.ocr_real_dependency_execution_request_generation_roadmap_decision_root)
    dryrun_root = Path(args.ocr_real_dependency_execution_authorization_dryrun_and_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    roadmap_vr = _load(roadmap_root / "verifier_report.json")
    roadmap_sm = _load(roadmap_root / "summary.json")
    request_cand = _load(dryrun_root / "execution_authorization_request_candidate_v1.json")
    gate = _load(dryrun_root / "validation_gate_path_dryrun_review_v1.json")

    ok("upstream.roadmap_go", roadmap_vr.get("verifier") == "GO")
    ok("upstream.roadmap_final", roadmap_sm.get("final_decision") == UPSTREAM_ROADMAP_FINAL)
    ok("upstream.roadmap_next", roadmap_sm.get("recommended_next_phase") == UPSTREAM_ROADMAP_NEXT)
    ok("upstream.route_a", roadmap_sm.get("selected_route") == SELECTED_ROUTE)
    ok("upstream.no_formal", request_cand.get("formal_request_generated_now") is False)
    ok("upstream.gate", gate.get("simulated_gate_path_pass") is True)

    summary = _load(root / "summary.json")
    schema = _load(root / "formal_execution_request_artifact_schema_v1.json")
    precond = _load(root / "formal_execution_request_generation_precondition_v1.json")
    field_map = _load(root / "formal_execution_request_field_source_map_v1.json")
    rules = _load(root / "formal_execution_request_validation_rule_v1.json")
    versioning = _load(root / "formal_execution_request_versioning_policy_v1.json")
    signature = _load(root / "formal_execution_request_signature_approval_placeholder_v1.json")
    storage = _load(root / "formal_execution_request_storage_boundary_plan_v1.json")
    send = _load(root / "formal_execution_request_send_boundary_plan_v1.json")
    evidence = _load(root / "formal_execution_request_evidence_binding_plan_v1.json")
    gate_bind = _load(root / "formal_execution_request_validation_gate_binding_plan_v1.json")
    blocked = _load(root / "formal_execution_request_blocked_path_matrix_v1.json")
    dryrun_plan = _load(root / "formal_execution_request_dryrun_plan_v1.json")
    decision = _load(root / "formal_execution_request_generation_planning_decision_v1.json")
    roadmap_in = _load(root / "execution_request_generation_roadmap_input_review_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("formal_execution_request_generation_planning_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("roadmap_in.pass", roadmap_in.get("review_pass") is True)
    ok("precond.pass", precond.get("preconditions_pass") is True)
    ok("precond.route_a", precond.get("route_a_selected") is True)
    ok("precond.gate", precond.get("validation_gate_path_simulated_pass") is True)

    ok("schema.type", schema.get("request_type") == "ocr_real_dependency_execution_authorization_request")
    ok("schema.lifecycle", schema.get("lifecycle_state") == "formal_execution_request_planned")
    ok("schema.std", schema.get("factory_authorization_standard_ref") == AUTHORIZATION_STANDARD_ID)
    for key in SCHEMA_REQUIRED:
        ok(f"schema.{key}", key in schema)
    ok("schema.not_generated", schema.get("generated_now") is False)
    ok("schema.not_persisted", schema.get("persisted_now") is False)

    ok("field_map.count11", field_map.get("binding_count") == 11)
    ok("rules.count17", rules.get("rule_count") == 17)
    for rule in VALIDATION_RULES:
        ok(f"rule.{rule[:30]}", rules.get("rules", {}).get(rule) is True)

    ok("version.schema", versioning.get("artifact_schema_version") == ARTIFACT_SCHEMA_VERSION)
    ok("version.compat", versioning.get("backward_compatibility_required") is True)

    ok("sig.not_now", signature.get("signature_generated_now") is False)
    ok("sig.approval_not", signature.get("approval_collected_now") is False)

    ok("storage.no_persist", storage.get("planning_does_not_persist_artifact") is True)
    ok("storage.persisted_false", storage.get("persisted_now") is False)

    ok("send.chain", len(send.get("chain") or []) >= 6)
    ok("evidence.formal_ref", "formal_execution_request_ref" in (
        evidence.get("future_execution_evidence") or []
    ))
    for art in EVIDENCE_ARTIFACTS:
        ok(f"evidence.{art[:20]}", art in (evidence.get("future_execution_evidence") or []))

    ok("gate_bind.count6", len(gate_bind.get("gates_required_later") or []) == 6)
    for g in GATE_BINDINGS:
        ok(f"gate.{g[:15]}", g in (gate_bind.get("gates_required_later") or []))
    ok("gate.runtime_false", gate_bind.get("gate_runtime_enabled_now") is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count24", blocked.get("blocked_count") == 24)
    blocked_ids = {b.get("blocked_path") for b in blocked.get("blocked_paths") or []}
    for bp in BLOCKED_PATHS:
        ok(f"blocked.{bp}", bp in blocked_ids)

    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE_GO)
    ok("decision.pass", decision.get("planning_pass") is True)

    for cid in SCOPE_ALLOWED_CHECKS:
        ok(f"schema.check.{cid}", cid in (schema.get("requested_allowed_checks") or []))

    for field in BOUNDARY_FALSE:
        ok(f"boundary_false.{field}", summary.get(field) is False)

    ok("non_claims", len(non_claims.get("non_claims") or []) >= len(NON_CLAIMS))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    boundary_ok = summary.get("boundary_ok") is True
    go = passed >= MIN_CHECKS and boundary_ok and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "boundary_ok": boundary_ok,
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
