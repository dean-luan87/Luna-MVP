#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Information Integration Layer Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_candidate_evidence_flow_integration_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CEF_DR_FINAL,
)
from capabilities.governance.midplatform_cognitive_zoning_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CZ_DR_FINAL,
    NO_UNIVERSAL_BRAIN_REVIEW_RULES,
)
from capabilities.governance.midplatform_decision_center_module_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DC_DR_FINAL,
)
from capabilities.governance.midplatform_end_to_end_output_chain_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as E2E_DR_FINAL,
)
from capabilities.governance.midplatform_frontend_model_influence_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FMIS_DR_FINAL,
)
from capabilities.governance.midplatform_information_integration_layer_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CONTEXT_CONFLICT_FIELDS,
    CONTEXT_CONFLICT_TYPES,
    CONTEXT_GAP_FIELDS,
    CONTEXT_GAP_TYPES,
    DECISION_READINESS_FIELDS,
    DRIVE_SIGNAL_INTEGRATION_CONFIRMATIONS,
    FINAL_DECISION_GO,
    FRESHNESS_STATUS_FIELDS,
    HANDOFF_PLAN_ITEMS,
    HEALTH_VALIDATION_WHITEBOX_CONFIRMATIONS,
    INTEGRATED_CONTEXT_CANDIDATE_FIELDS,
    INTEGRATION_INPUT_CONFIRMATIONS,
    INTEGRATION_INPUT_SOURCES,
    LAYER_CORE_RESPONSIBILITIES,
    LAYER_NOT_RESPONSIBILITIES,
    MEMORY_WM_INTEGRATION_CONFIRMATIONS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    NO_UNIVERSAL_BRAIN_BOUNDARIES,
    PERCEPTION_INTEGRATION_CONFIRMATIONS,
    PHASE_ID,
    PRIORITY_MAP_FIELDS,
    PROVIDER_STATUS_CONFIRMATIONS,
    SCORING_CONFIRMATIONS,
    SCORING_POLICY_ITEMS,
    SCOPE,
    TASK_ROUTE_MAP_CONFIRMATIONS,
    TRACEABILITY_FIELDS,
    UPSTREAM_DS_DR_FINAL,
    UPSTREAM_DS_DR_NEXT,
)
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_DR_FINAL,
)
from capabilities.governance.seed_core_drive_signal_contract_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DS_DR_FINAL,
    NEXT_PHASE_GO as DS_DR_NEXT,
)
from capabilities.governance.seed_core_pluggable_layer_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SC_DR_FINAL,
)

MIN_CHECKS = 355

REQUIRED = (
    "information_integration_layer_planning_policy_v1.json",
    "upstream_drive_signal_input_review_v1.json",
    "information_integration_layer_definition_v1.json",
    "integration_input_source_taxonomy_v1.json",
    "integrated_context_candidate_contract_v1.json",
    "context_conflict_candidate_contract_v1.json",
    "context_gap_candidate_contract_v1.json",
    "context_freshness_status_contract_v1.json",
    "context_priority_map_contract_v1.json",
    "decision_readiness_candidate_contract_v1.json",
    "drive_signal_integration_policy_v1.json",
    "perception_context_integration_policy_v1.json",
    "memory_worldmodel_context_integration_policy_v1.json",
    "task_route_map_context_integration_policy_v1.json",
    "health_validation_whitebox_integration_policy_v1.json",
    "provider_status_integration_policy_v1.json",
    "conflict_gap_freshness_scoring_policy_v1.json",
    "information_integration_to_decision_center_handoff_plan_v1.json",
    "information_integration_no_universal_brain_boundary_v1.json",
    "information_integration_traceability_policy_v1.json",
    "information_integration_boundary_matrix_v1.json",
    "information_integration_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "information_integration_layer_planning_decision_v1.json",
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
            "midplatform_information_integration_layer_planning"
        ),
    )
    p.add_argument(
        "--drive-signal-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "seed_core_drive_signal_contract_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--cognitive-zoning-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_cognitive_zoning_architecture_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--provider-abstraction-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "provider_abstraction_standard_alignment_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--fmis-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_frontend_model_influence_simulation_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--e2e-simulation-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_end_to_end_output_chain_simulation_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--candidate-evidence-flow-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_candidate_evidence_flow_integration_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--decision-center-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_decision_center_module_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    ds_dr_root = Path(args.drive_signal_dryrun_root)
    cz_dr_root = Path(args.cognitive_zoning_dryrun_root)
    provider_dr_root = Path(args.provider_abstraction_dryrun_root)
    fmis_dr_root = Path(args.fmis_dryrun_root)
    e2e_dr_root = Path(args.e2e_simulation_dryrun_root)
    cef_dr_root = Path(args.candidate_evidence_flow_dryrun_root)
    dc_dr_root = Path(args.decision_center_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    ds_dr_vr = _load(ds_dr_root / "verifier_report.json")
    ds_dr_sm = _load(ds_dr_root / "summary.json")
    cz_dr_vr = _load(cz_dr_root / "verifier_report.json")
    provider_dr_vr = _load(provider_dr_root / "verifier_report.json")
    provider_dr_sm = _load(provider_dr_root / "summary.json")
    fmis_dr_vr = _load(fmis_dr_root / "verifier_report.json")
    fmis_dr_sm = _load(fmis_dr_root / "summary.json")
    e2e_dr_vr = _load(e2e_dr_root / "verifier_report.json")
    e2e_dr_sm = _load(e2e_dr_root / "summary.json")
    cef_dr_vr = _load(cef_dr_root / "verifier_report.json")
    dc_dr_vr = _load(dc_dr_root / "verifier_report.json")

    ok("upstream.ds_dr_go", ds_dr_vr.get("verifier") == "GO")
    ok("upstream.ds_dr_final", ds_dr_sm.get("final_decision") == UPSTREAM_DS_DR_FINAL)
    ok("upstream.ds_dr_final_expected", ds_dr_sm.get("final_decision") == DS_DR_FINAL)
    ok("upstream.ds_dr_next", ds_dr_sm.get("recommended_next_phase") == UPSTREAM_DS_DR_NEXT)
    ok("upstream.ds_dr_next_expected", ds_dr_sm.get("recommended_next_phase") == DS_DR_NEXT)
    cz_dr_sm = _load(cz_dr_root / "summary.json")
    cef_dr_sm = _load(cef_dr_root / "summary.json")
    dc_dr_sm = _load(dc_dr_root / "summary.json")

    ok("upstream.cz_dr_go", cz_dr_vr.get("verifier") == "GO")
    ok("upstream.cz_dr_final", cz_dr_sm.get("final_decision") == CZ_DR_FINAL)
    ok("upstream.provider_go", provider_dr_vr.get("verifier") == "GO")
    ok("upstream.provider_final", provider_dr_sm.get("final_decision") == PROVIDER_DR_FINAL)
    ok("upstream.fmis_go", fmis_dr_vr.get("verifier") == "GO")
    ok("upstream.fmis_final", fmis_dr_sm.get("final_decision") == FMIS_DR_FINAL)
    ok("upstream.e2e_go", e2e_dr_vr.get("verifier") == "GO")
    ok("upstream.e2e_final", e2e_dr_sm.get("final_decision") == E2E_DR_FINAL)
    ok("upstream.cef_go", cef_dr_vr.get("verifier") == "GO")
    ok("upstream.cef_final", cef_dr_sm.get("final_decision") == CEF_DR_FINAL)
    ok("upstream.dc_go", dc_dr_vr.get("verifier") == "GO")
    ok("upstream.dc_final", dc_dr_sm.get("final_decision") == DC_DR_FINAL)

    summary = _load(root / "summary.json")
    policy = _load(root / "information_integration_layer_planning_policy_v1.json")
    input_review = _load(root / "upstream_drive_signal_input_review_v1.json")
    layer_def = _load(root / "information_integration_layer_definition_v1.json")
    taxonomy = _load(root / "integration_input_source_taxonomy_v1.json")
    integrated = _load(root / "integrated_context_candidate_contract_v1.json")
    conflict = _load(root / "context_conflict_candidate_contract_v1.json")
    gap = _load(root / "context_gap_candidate_contract_v1.json")
    freshness = _load(root / "context_freshness_status_contract_v1.json")
    priority = _load(root / "context_priority_map_contract_v1.json")
    readiness = _load(root / "decision_readiness_candidate_contract_v1.json")
    drive_policy = _load(root / "drive_signal_integration_policy_v1.json")
    perception_policy = _load(root / "perception_context_integration_policy_v1.json")
    memory_policy = _load(root / "memory_worldmodel_context_integration_policy_v1.json")
    task_policy = _load(root / "task_route_map_context_integration_policy_v1.json")
    health_policy = _load(root / "health_validation_whitebox_integration_policy_v1.json")
    provider_policy = _load(root / "provider_status_integration_policy_v1.json")
    scoring_policy = _load(root / "conflict_gap_freshness_scoring_policy_v1.json")
    handoff = _load(root / "information_integration_to_decision_center_handoff_plan_v1.json")
    no_brain = _load(root / "information_integration_no_universal_brain_boundary_v1.json")
    traceability = _load(root / "information_integration_traceability_policy_v1.json")
    boundary = _load(root / "information_integration_boundary_matrix_v1.json")
    dryrun_plan = _load(root / "information_integration_dryrun_plan_v1.json")
    planning_decision = _load(root / "information_integration_layer_planning_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.not_runtime", policy.get("planning_not_runtime_not_decide") is True)
    ok("policy.module_id", policy.get("module_id") == "midplatform_information_integration_layer_v1")
    ok("policy.input18", policy.get("input_source_count") == 18)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.ds_go", input_review.get("drive_signal_dryrun_verifier") == "GO")
    ok("input.ds_final", input_review.get("drive_signal_dryrun_final_decision") == UPSTREAM_DS_DR_FINAL)
    ok("input.ii_zone", input_review.get("information_integration_zone_validated") is True)
    ok("input.no_brain", input_review.get("no_universal_brain_pass") is True)
    ok("input.provider", input_review.get("provider_abstraction_go") is True)
    ok("input.fmis", input_review.get("fmis_go") is True)
    ok("input.e2e", input_review.get("e2e_go") is True)
    ok("input.cef", input_review.get("candidate_evidence_flow_go") is True)
    ok("input.dc", input_review.get("decision_center_go") is True)
    ok("input.no_leakage", input_review.get("no_runtime_leakage_in_upstream") is True)

    ok("layer.module_id", layer_def.get("module_id") == "midplatform_information_integration_layer_v1")
    ok("layer.zone", layer_def.get("zone") == "Information Integration Zone")
    ok("layer.role", layer_def.get("role") == "multi_source_context_assembly_and_decision_readiness_preparation")
    ok("layer.arch", layer_def.get("architectural_layer") == "InformationIntegration")
    ok("layer.runtime_false", layer_def.get("runtime_enabled_now") is False)
    ok("layer.not_brain", layer_def.get("not_universal_brain") is True)
    ok("layer.not_dc", layer_def.get("not_decision_center") is True)
    ok("layer.not_mem", layer_def.get("not_memory_writer") is True)
    ok("layer.not_wm", layer_def.get("not_worldmodel_writer") is True)
    ok("layer.not_exec", layer_def.get("not_runtime_executor") is True)
    for resp in LAYER_CORE_RESPONSIBILITIES:
        ok(f"layer.core.{resp[:18]}", resp in (layer_def.get("core_responsibilities") or []))
    for resp in LAYER_NOT_RESPONSIBILITIES:
        ok(f"layer.not.{resp[:12]}", resp in (layer_def.get("not_responsibilities") or []))

    ok("tax.count18", taxonomy.get("source_count") == 18)
    for src in INTEGRATION_INPUT_SOURCES:
        ok(f"tax.{src[:18]}", src in (taxonomy.get("input_sources") or []))
    for conf in INTEGRATION_INPUT_CONFIRMATIONS:
        ok(f"tax.conf.{conf[:18]}", conf in (taxonomy.get("confirmations") or []))

    for field in INTEGRATED_CONTEXT_CANDIDATE_FIELDS:
        ok(f"integrated.field.{field[:18]}", field in (integrated.get("required_fields") or []))
    ok("integrated.candidate", integrated.get("defaults", {}).get("candidate_only") is True)
    ok("integrated.not_decision", integrated.get("defaults", {}).get("not_decision") is True)
    ok("integrated.not_fact", integrated.get("defaults", {}).get("not_fact") is True)
    ok("integrated.not_output", integrated.get("defaults", {}).get("not_user_output") is True)
    ok("integrated.runtime_false", integrated.get("defaults", {}).get("runtime_enable_allowed") is False)

    for field in CONTEXT_CONFLICT_FIELDS:
        ok(f"conflict.field.{field[:18]}", field in (conflict.get("required_fields") or []))
    ok("conflict.count10", conflict.get("conflict_type_count") == 10)
    for ct in CONTEXT_CONFLICT_TYPES:
        ok(f"conflict.type.{ct[:18]}", ct in (conflict.get("conflict_types") or []))
    ok("conflict.decision_req", conflict.get("defaults", {}).get("decision_required") is True)

    for field in CONTEXT_GAP_FIELDS:
        ok(f"gap.field.{field[:18]}", field in (gap.get("required_fields") or []))
    ok("gap.count10", gap.get("gap_type_count") == 10)
    for gt in CONTEXT_GAP_TYPES:
        ok(f"gap.type.{gt[:18]}", gt in (gap.get("gap_types") or []))

    for field in FRESHNESS_STATUS_FIELDS:
        ok(f"fresh.field.{field[:18]}", field in (freshness.get("required_fields") or []))
    ok("fresh.can_drive_false", freshness.get("defaults", {}).get("can_drive_decision") is False)

    for field in PRIORITY_MAP_FIELDS:
        ok(f"priority.field.{field[:18]}", field in (priority.get("required_fields") or []))

    for field in DECISION_READINESS_FIELDS:
        ok(f"ready.field.{field[:18]}", field in (readiness.get("required_fields") or []))
    ok("ready.sufficient_false", readiness.get("defaults", {}).get("sufficient_for_decision") is False)
    ok("ready.handoff_false", readiness.get("defaults", {}).get("decision_center_handoff_allowed") is False)

    for conf in DRIVE_SIGNAL_INTEGRATION_CONFIRMATIONS:
        ok(f"drive.{conf[:18]}", conf in (drive_policy.get("confirmations") or []))
    for conf in PERCEPTION_INTEGRATION_CONFIRMATIONS:
        ok(f"perception.{conf[:18]}", conf in (perception_policy.get("confirmations") or []))
    for conf in MEMORY_WM_INTEGRATION_CONFIRMATIONS:
        ok(f"memory.{conf[:18]}", conf in (memory_policy.get("confirmations") or []))
    for conf in TASK_ROUTE_MAP_CONFIRMATIONS:
        ok(f"task.{conf[:18]}", conf in (task_policy.get("confirmations") or []))
    for conf in HEALTH_VALIDATION_WHITEBOX_CONFIRMATIONS:
        ok(f"health.{conf[:18]}", conf in (health_policy.get("confirmations") or []))
    for conf in PROVIDER_STATUS_CONFIRMATIONS:
        ok(f"provider.{conf[:18]}", conf in (provider_policy.get("confirmations") or []))

    ok("scoring.count8", scoring_policy.get("item_count") == 8)
    for item in SCORING_POLICY_ITEMS:
        ok(f"scoring.item.{item[:18]}", item in (scoring_policy.get("scoring_items") or []))
    for conf in SCORING_CONFIRMATIONS:
        ok(f"scoring.conf.{conf[:18]}", conf in (scoring_policy.get("confirmations") or []))

    ok("handoff.count6", handoff.get("item_count") == 6)
    for item in HANDOFF_PLAN_ITEMS:
        ok(f"handoff.{item[:18]}", item in (handoff.get("handoff_items") or []))
    ok("handoff.dc_final", handoff.get("decision_center_final") is True)

    ok("no_brain.count9", no_brain.get("boundary_count") == 9)
    for b in NO_UNIVERSAL_BRAIN_BOUNDARIES:
        ok(f"no_brain.{b[:18]}", b in (no_brain.get("boundaries") or []))
    for rule in NO_UNIVERSAL_BRAIN_REVIEW_RULES:
        ok(f"no_brain.rule.{rule[:18]}", rule in (no_brain.get("no_universal_brain_rules") or []))

    ok("trace.preserve", traceability.get("all_transformations_must_preserve") is True)
    for field in TRACEABILITY_FIELDS:
        ok(f"trace.{field[:18]}", field in (traceability.get("required_fields") or []))

    ok("boundary.pass", boundary.get("boundary_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE_GO)

    ok("plan_decision.pass", planning_decision.get("planning_pass") is True)
    ok("plan_decision.final", planning_decision.get("final_decision") == FINAL_DECISION_GO)
    ok("plan_decision.next", planning_decision.get("recommended_next_phase") == NEXT_PHASE_GO)

    for claim in NON_CLAIMS:
        ok(f"non_claim.{claim[:18]}", claim in (non_claims.get("non_claims") or []))

    total = len(checks)
    passed = sum(1 for c in checks if c["passed"])
    min_checks = MIN_CHECKS if MIN_CHECKS else total
    verifier = "GO" if passed == total and passed >= min_checks else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verifier": verifier,
        "checks_passed": passed,
        "checks_total": total,
        "min_checks": min_checks,
        "planning_pass": summary.get("planning_pass"),
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": verifier, "checks_passed": passed, "checks_total": total}))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
