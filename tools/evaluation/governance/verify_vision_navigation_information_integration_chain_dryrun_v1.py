#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision Navigation Information Integration Chain DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.first_person_vision_navigation_candidate_flow_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CF_DR_FINAL_GO,
    NEXT_PHASE_GO as CF_DR_NEXT_PHASE,
)
from capabilities.governance.midplatform_information_integration_layer_planning_v1 import (
    DECISION_READINESS_FIELDS,
    FRESHNESS_STATUS_FIELDS,
    INTEGRATED_CONTEXT_CANDIDATE_FIELDS,
    PRIORITY_MAP_FIELDS,
)
from capabilities.governance.vision_navigation_information_integration_chain_dryrun_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CONFLICT_GAP_FRESHNESS_REVIEW_ITEMS,
    DC_HANDOFF_REVIEW_ITEMS,
    DRIVE_PRIORITY_REVIEW_ITEMS,
    EVIDENCE_TRACEABILITY_REVIEW_ITEMS,
    FINAL_DECISION_GO,
    INTAKE_SAMPLE_IDS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    RISK_INTEGRATION_REVIEW_ITEMS,
    SCOPE,
    VISUAL_OCR_MAP_ROUTE_REVIEW_ITEMS,
)

MIN_CHECKS = 258

REQUIRED = (
    "vision_navigation_information_integration_chain_dryrun_policy_v1.json",
    "candidate_flow_input_review_v1.json",
    "sample_candidate_intake_set_v1.json",
    "information_integration_chain_model_candidate_v1.json",
    "sample_integrated_context_candidate_v1.json",
    "sample_context_conflict_candidate_v1.json",
    "sample_context_gap_candidate_v1.json",
    "sample_context_freshness_status_v1.json",
    "sample_context_priority_map_v1.json",
    "sample_decision_readiness_candidate_v1.json",
    "visual_ocr_map_route_integration_review_v1.json",
    "drive_signal_priority_integration_review_v1.json",
    "risk_context_integration_review_v1.json",
    "evidence_traceability_integration_review_v1.json",
    "conflict_gap_freshness_integration_review_v1.json",
    "decision_center_handoff_readiness_review_v1.json",
    "chain_boundary_audit_v1.json",
    "chain_blocked_path_result_v1.json",
    "chain_closure_decision_v1.json",
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
            "vision_navigation_information_integration_chain_dryrun"
        ),
    )
    p.add_argument(
        "--candidate-flow-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "first_person_vision_navigation_candidate_flow_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--information-integration-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_information_integration_layer_dryrun_and_review"
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
        "--constitution-bus-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "luna_constitution_capability_bus_governance_baseline_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--provider-abstraction-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "provider_abstraction_standard_alignment_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    cf_dr_vr = _load(Path(args.candidate_flow_dryrun_root) / "verifier_report.json")
    cf_dr_sm = _load(Path(args.candidate_flow_dryrun_root) / "summary.json")
    ii_dr_vr = _load(Path(args.information_integration_dryrun_root) / "verifier_report.json")
    ds_dr_vr = _load(Path(args.drive_signal_dryrun_root) / "verifier_report.json")
    cb_dr_vr = _load(Path(args.constitution_bus_dryrun_root) / "verifier_report.json")
    provider_dr_vr = _load(Path(args.provider_abstraction_dryrun_root) / "verifier_report.json")

    ok("upstream.cf_dr_go", cf_dr_vr.get("verifier") == "GO")
    ok("upstream.cf_dr_final", cf_dr_sm.get("final_decision") == CF_DR_FINAL_GO)
    ok("upstream.cf_dr_next", cf_dr_sm.get("recommended_next_phase") == CF_DR_NEXT_PHASE)
    ok("upstream.ii_dr_go", ii_dr_vr.get("verifier") == "GO")
    ok("upstream.ds_dr_go", ds_dr_vr.get("verifier") == "GO")
    ok("upstream.cb_dr_go", cb_dr_vr.get("verifier") == "GO")
    ok("upstream.provider_go", provider_dr_vr.get("verifier") == "GO")

    summary = _load(root / "summary.json")
    policy = _load(root / "vision_navigation_information_integration_chain_dryrun_policy_v1.json")
    input_review = _load(root / "candidate_flow_input_review_v1.json")
    intake = _load(root / "sample_candidate_intake_set_v1.json")
    chain_model = _load(root / "information_integration_chain_model_candidate_v1.json")
    integrated = _load(root / "sample_integrated_context_candidate_v1.json")
    conflict = _load(root / "sample_context_conflict_candidate_v1.json")
    gap = _load(root / "sample_context_gap_candidate_v1.json")
    freshness = _load(root / "sample_context_freshness_status_v1.json")
    priority = _load(root / "sample_context_priority_map_v1.json")
    readiness = _load(root / "sample_decision_readiness_candidate_v1.json")
    visual_review = _load(root / "visual_ocr_map_route_integration_review_v1.json")
    drive_review = _load(root / "drive_signal_priority_integration_review_v1.json")
    risk_review = _load(root / "risk_context_integration_review_v1.json")
    trace_review = _load(root / "evidence_traceability_integration_review_v1.json")
    cgf_review = _load(root / "conflict_gap_freshness_integration_review_v1.json")
    dc_handoff = _load(root / "decision_center_handoff_readiness_review_v1.json")
    boundary = _load(root / "chain_boundary_audit_v1.json")
    blocked = _load(root / "chain_blocked_path_result_v1.json")
    closure = _load(root / "chain_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.fixture_chain", summary.get("fixture_chain_integrated") is True)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.chain_dryrun", policy.get("chain_dryrun_not_runtime_not_decide") is True)
    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.fixture_only", input_review.get("fixture_metadata_only") is True)
    ok("input.cf_go", input_review.get("candidate_flow_dryrun_verifier") == "GO")
    ok("input.ii_go", input_review.get("information_integration_verifier") == "GO")

    for sid in INTAKE_SAMPLE_IDS:
        ok(f"intake.{sid[:18]}", sid in (intake.get("sample_ids") or []))
    ok("intake.fixture", intake.get("fixture_metadata_only") is True)
    ok("intake.candidate", intake.get("candidate_only") is True)
    ok("intake.not_fact", intake.get("not_fact") is True)

    ok("model.id", chain_model.get("model_id") == "vision_navigation_information_integration_chain_v1")
    ok("model.chain_type", chain_model.get("chain_type") == "fixture_based_information_integration_chain")
    ok("model.consumes_perception", chain_model.get("consumes_perception_candidates") is True)
    ok("model.consumes_drive", chain_model.get("consumes_drive_signal_candidate") is True)
    ok("model.emits_integrated", chain_model.get("emits_integrated_context_candidate") is True)
    ok("model.emits_conflict", chain_model.get("emits_context_conflict_candidate") is True)
    ok("model.emits_gap", chain_model.get("emits_context_gap_candidate") is True)
    ok("model.emits_readiness", chain_model.get("emits_decision_readiness_candidate") is True)
    ok("model.not_decide", chain_model.get("does_not_decide") is True)
    ok("model.not_provider", chain_model.get("does_not_invoke_provider") is True)
    ok("model.not_runtime", chain_model.get("does_not_enable_runtime") is True)
    ok("model.candidate", chain_model.get("candidate_only") is True)

    for field in INTEGRATED_CONTEXT_CANDIDATE_FIELDS:
        ok(f"integrated.{field[:18]}", field in integrated)
    ok("integrated.candidate", integrated.get("candidate_only") is True)
    ok("integrated.not_decision", integrated.get("not_decision") is True)
    ok("integrated.not_fact", integrated.get("not_fact") is True)
    ok("integrated.no_runtime", integrated.get("runtime_enable_allowed") is False)
    ok("integrated.scene", integrated.get("current_scene_context", {}).get("scene_type") == "street_crossing")
    ok("integrated.hint", integrated.get("recommended_next_step_hint") == "observe_more_or_hold_for_safety")
    ok(
        "integrated.forbidden",
        "direct_navigation_action_without_decision" in (integrated.get("forbidden_actions") or []),
    )

    ok("conflict.type", conflict.get("conflict_type") in ("map_vs_vision", "visual_vs_ocr"))
    ok("conflict.decision_req", conflict.get("decision_required") is True)
    ok("conflict.candidate", conflict.get("candidate_only") is True)

    ok("gap.missing", "missing_real_time_frame_validation" in str(gap.get("missing_source_type", "")))
    ok("gap.observe", gap.get("required_observation") == "observe_crossing_status_later")
    ok("gap.candidate", gap.get("candidate_only") is True)

    items = freshness.get("freshness_items") or []
    ok("freshness.count4", len(items) >= 4)
    ok("freshness.all_false", freshness.get("all_can_drive_decision_false") is True)
    states = {i.get("freshness_state") for i in items}
    ok("freshness.simulated", "simulated_only" in states)
    ok("freshness.stale", "stale_risk_possible" in states)
    ok("freshness.task_scope", "task_scope_candidate" in states)
    for field in FRESHNESS_STATUS_FIELDS:
        ok(f"freshness_field.{field[:18]}", all(field in i for i in items))

    for field in PRIORITY_MAP_FIELDS:
        ok(f"priority.{field[:18]}", field in priority)
    ok("priority.survival_high", priority.get("survival_priority_weight", 0) >= 0.9)
    ok("priority.task_med", 0.4 <= priority.get("task_priority_weight", 0) <= 0.8)
    ok("priority.hint", priority.get("output_priority_hint") == "hold_or_observe_more_candidate")

    for field in DECISION_READINESS_FIELDS:
        ok(f"readiness.{field[:18]}", field in readiness)
    ok(
        "readiness.status",
        readiness.get("readiness_status")
        in ("not_ready_for_real_navigation_decision", "candidate_ready_for_decision_review"),
    )
    ok("readiness.sufficient_false", readiness.get("sufficient_for_decision") is False)
    ok("readiness.handoff_false", readiness.get("decision_center_handoff_allowed") is False)
    ok("readiness.candidate", readiness.get("candidate_only") is True)

    for item in VISUAL_OCR_MAP_ROUTE_REVIEW_ITEMS:
        ok(f"visual_review.{item[:18]}", visual_review.get("dryrun_and_review_pass") is True)
    ok("visual_review.scene", visual_review.get("scene_street_crossing") is True)

    for item in DRIVE_PRIORITY_REVIEW_ITEMS:
        ok(f"drive_review.{item[:18]}", drive_review.get("dryrun_and_review_pass") is True)
    ok("drive_review.survival", drive_review.get("survival_elevated") is True)

    for item in RISK_INTEGRATION_REVIEW_ITEMS:
        ok(f"risk_review.{item[:18]}", risk_review.get("dryrun_and_review_pass") is True)

    for item in EVIDENCE_TRACEABILITY_REVIEW_ITEMS:
        ok(f"trace_review.{item[:18]}", trace_review.get("dryrun_and_review_pass") is True)
    ok("trace_review.matrix", trace_review.get("source_chain_matrix_present") is True)

    for item in CONFLICT_GAP_FRESHNESS_REVIEW_ITEMS:
        ok(f"cgf_review.{item[:18]}", cgf_review.get("dryrun_and_review_pass") is True)
    ok("cgf_review.gap", cgf_review.get("gap_generated") is True)

    for item in DC_HANDOFF_REVIEW_ITEMS:
        ok(f"dc_handoff.{item[:18]}", dc_handoff.get("dryrun_and_review_pass") is True)
    ok(
        "dc_handoff.no_decision",
        dc_handoff.get("handoff_package", {}).get("decision_candidate_generated") is False,
    )

    ok("boundary.audit_pass", boundary.get("audit_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count18", blocked.get("blocked_count") == 18)
    for path in BLOCKED_PATHS:
        ok(
            f"blocked.{path[:18]}",
            any(
                b.get("path_id") == path and b.get("status") == "blocked"
                for b in (blocked.get("blocked_paths") or [])
            ),
        )

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("next_route.ready", next_route.get("ready_for_decision_chain_candidate_dryrun") is True)
    ok("next_route.phase", next_route.get("selected_next_phase") == NEXT_PHASE_GO)

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
        "dryrun_and_review_pass": summary.get("dryrun_and_review_pass"),
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
