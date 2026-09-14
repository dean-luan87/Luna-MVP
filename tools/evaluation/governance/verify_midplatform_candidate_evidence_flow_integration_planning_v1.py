#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Candidate Evidence Flow Integration Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_candidate_evidence_flow_integration_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_MATRIX_FALSE,
    BOUNDARY_TRUE,
    CANDIDATE_REQUIRED_FIELDS,
    CANDIDATE_TYPES,
    DECISION_REQUEST_FIELDS,
    DOMAIN_CONFIG_DOMAINS,
    FINAL_DECISION_GO,
    FLOW_INTEGRITY_RULES,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    UPSTREAM_DC_DR_FINAL,
    UPSTREAM_DC_DR_NEXT,
    UPSTREAM_TEMPLATE_FINAL,
    VALIDATION_RESULT_STATES,
)
from capabilities.governance.midplatform_module_definition_template_v1 import (
    TEMPLATE_ID,
    TEMPLATE_SECTIONS,
    validate_module_definition,
)

MIN_CHECKS = 169

REQUIRED = (
    "candidate_evidence_flow_integration_planning_policy_v1.json",
    "upstream_decision_center_input_review_v1.json",
    "module_template_compliance_review_v1.json",
    "candidate_evidence_flow_module_definition_v1.json",
    "upstream_candidate_intake_contract_v1.json",
    "domain_config_intake_contract_v1.json",
    "evidence_pack_binding_contract_v1.json",
    "validation_result_binding_contract_v1.json",
    "health_signal_binding_contract_v1.json",
    "whitebox_visibility_binding_contract_v1.json",
    "issue_trace_violation_binding_contract_v1.json",
    "decision_request_assembly_contract_v1.json",
    "candidate_evidence_flow_integrity_policy_v1.json",
    "stale_missing_conflicting_evidence_policy_v1.json",
    "candidate_evidence_flow_boundary_matrix_v1.json",
    "candidate_evidence_flow_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "candidate_evidence_flow_integration_planning_decision_v1.json",
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
            "midplatform_candidate_evidence_flow_integration_planning"
        ),
    )
    p.add_argument(
        "--decision-center-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_decision_center_module_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--template-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_module_definition_template_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    dc_root = Path(args.decision_center_dryrun_root)
    template_root = Path(args.template_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    dc_vr = _load(dc_root / "verifier_report.json")
    dc_sm = _load(dc_root / "summary.json")
    template_vr = _load(template_root / "verifier_report.json")
    template_sm = _load(template_root / "summary.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "candidate_evidence_flow_integration_planning_policy_v1.json")
    dc_review = _load(root / "upstream_decision_center_input_review_v1.json")
    template_review = _load(root / "module_template_compliance_review_v1.json")
    flow_module = _load(root / "candidate_evidence_flow_module_definition_v1.json")
    candidate_intake = _load(root / "upstream_candidate_intake_contract_v1.json")
    domain_config = _load(root / "domain_config_intake_contract_v1.json")
    evidence = _load(root / "evidence_pack_binding_contract_v1.json")
    validation = _load(root / "validation_result_binding_contract_v1.json")
    health = _load(root / "health_signal_binding_contract_v1.json")
    whitebox = _load(root / "whitebox_visibility_binding_contract_v1.json")
    trace = _load(root / "issue_trace_violation_binding_contract_v1.json")
    assembly = _load(root / "decision_request_assembly_contract_v1.json")
    integrity = _load(root / "candidate_evidence_flow_integrity_policy_v1.json")
    stale = _load(root / "stale_missing_conflicting_evidence_policy_v1.json")
    boundary = _load(root / "candidate_evidence_flow_boundary_matrix_v1.json")
    dryrun = _load(root / "candidate_evidence_flow_dryrun_plan_v1.json")
    decision = _load(root / "candidate_evidence_flow_integration_planning_decision_v1.json")

    ok("upstream.dc_go", dc_vr.get("verifier") == "GO")
    ok("upstream.dc_final", dc_sm.get("final_decision") == UPSTREAM_DC_DR_FINAL)
    ok("upstream.dc_next", dc_sm.get("recommended_next_phase") == UPSTREAM_DC_DR_NEXT)
    ok("upstream.template_go", template_vr.get("verifier") == "GO")
    ok("upstream.template_final", template_sm.get("final_decision") == UPSTREAM_TEMPLATE_FINAL)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("candidate_evidence_flow_integration_planning_only") is True)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.not_decision", policy.get("flow_integration_not_decision") is True)
    ok("policy.assembly", policy.get("assembles_decision_request_not_decision_candidate") is True)

    ok("dc_review.pass", dc_review.get("review_pass") is True)
    ok("dc_review.not_task", dc_review.get("decision_candidate_not_task_response") is True)

    ok("template.compliance", template_review.get("compliance_pass") is True)
    ok("template.10sections", template_review.get("ten_section_structure_required") is True)

    identity = flow_module.get("module_identity") or {}
    processing = flow_module.get("processing_scope") or {}
    downstream = flow_module.get("downstream_targets") or {}
    valid, issues = validate_module_definition(flow_module)
    ok("module.valid", valid and len(issues) == 0)
    ok("module.id", identity.get("module_id") == "midplatform_candidate_evidence_flow_integration_v1")
    ok("module.type", identity.get("module_type") == "midplatform_flow_integration_module")
    ok("module.role", identity.get("role") == "candidate_evidence_binding_and_decision_request_assembly")
    ok("module.layer", identity.get("system_layer") == "Assembly")
    ok("module.no_arbitrate", processing.get("arbitration_allowed") is False)
    ok("module.no_write", processing.get("write_allowed") is False)
    ok("module.no_provider", processing.get("provider_invocation_allowed") is False)
    ok("module.downstream_dc", "midplatform_decision_center_v1" in (downstream.get("downstream_modules") or []))

    for section in TEMPLATE_SECTIONS:
        ok(f"section.{section[:12]}", section in flow_module)

    ok("candidate.types9", len(candidate_intake.get("supported_candidate_types") or []) == 9)
    for ct in CANDIDATE_TYPES:
        ok(f"candidate.{ct[:15]}", ct in (candidate_intake.get("supported_candidate_types") or []))
    for field in CANDIDATE_REQUIRED_FIELDS:
        ok(f"cand_field.{field[:12]}", field in (candidate_intake.get("required_fields_per_candidate") or []))
    ok("candidate.not_fact", candidate_intake.get("fact_status") == "not_fact")

    ok("domain.count7", len(domain_config.get("domains") or []) == 7)
    for d in DOMAIN_CONFIG_DOMAINS:
        ok(f"domain.{d}", d in (domain_config.get("domains") or []))
    ok("domain.constraints_only", domain_config.get("domain_config_provides_domain_constraints_only") is True)

    ok("evidence.validation_req", evidence.get("validation_required") is True)
    ok("evidence.whitebox_req", evidence.get("whitebox_visibility_required") is True)
    ok("evidence.not_fact", evidence.get("fact_status") == "not_fact")

    ok("validation.states6", len(validation.get("supported_states") or []) == 6)
    for state in VALIDATION_RESULT_STATES:
        ok(f"val.{state['state'][:12]}", any(
            s.get("state") == state["state"] for s in (validation.get("supported_states") or [])
        ))
    ok("validation.no_exec", validation.get("does_not_execute_validation") is True)

    ok("health.pressure", health.get("health_signal_is_pressure_context") is True)
    ok("health.reserved", health.get("health_metric_definition_status") == "reserved_not_defined")
    ok("health.no_auth", health.get("health_cannot_authorize_by_itself") is True)

    ok("wb.rationale", whitebox.get("whitebox_refs_provide_rationale_explainability") is True)
    ok("wb.no_decide", whitebox.get("whitebox_does_not_decide") is True)
    ok("wb.node_not_global", whitebox.get("node_level_cannot_define_global_status") is True)

    ok("trace.preserve", trace.get("issue_trace_refs_preserve_upstream_failure") is True)
    ok("trace.no_mutate", trace.get("trace_report_do_not_mutate_candidate") is True)

    ok("assembly.later", assembly.get("assembled_later_not_now") is True)
    ok("assembly.fields16", len(assembly.get("required_fields") or []) == 16)
    for field in DECISION_REQUEST_FIELDS:
        ok(f"assembly.{field[:15]}", field in (assembly.get("required_fields") or []))
    ok("assembly.consumer", assembly.get("downstream_consumer") == "midplatform_decision_center_v1")

    ok("integrity.rules8", len(integrity.get("rules") or []) == 8)
    for rule in FLOW_INTEGRITY_RULES:
        ok(f"integrity.{rule[:18]}", rule in (integrity.get("rules") or []))
    ok("integrity.no_fact", integrity.get("no_fact_write") is True)

    ok("stale.stale", stale.get("stale_evidence_action") == "request_more_evidence")
    ok("stale.missing_val", stale.get("missing_validation_action") == "request_validation")

    ok("boundary.all_false", boundary.get("all_runtime_actions_false") is True)
    for field in BOUNDARY_MATRIX_FALSE:
        ok(f"matrix.{field[:15]}", boundary.get("matrix", {}).get(field) is False)

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)

    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)

    ok("template_id", summary.get("template_id") == TEMPLATE_ID)
    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    pass_all = summary.get("planning_pass") is True
    go = passed >= MIN_CHECKS and pass_all and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "planning_pass": pass_all,
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
