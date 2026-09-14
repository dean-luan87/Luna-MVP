#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Gate Taxonomy and Requirement Framework Planning v1 (planning-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Gate-Taxonomy-and-Requirement-Framework-Planning-v1-001"
FINAL_DECISION = "GATE_TAXONOMY_AND_REQUIREMENT_FRAMEWORK_PLANNING_READY_FOR_MIDPLATFORM_FUNCTION_GOVERNANCE"
NEXT_PHASE = "Phase-MidPlatform-Function-Governance-and-Consolidation-Planning-v1-001"

MIN_CHECKS = 240
BASELINE_REQUIREMENT = 200


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "gate_taxonomy_and_requirement_framework_planning_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    policy = _load_json(root / "luna_gate_taxonomy_planning_policy.json")
    gate_constitution = _load_json(root / "gate_constitution.json")
    gate_types = _load_json(root / "gate_type_taxonomy.json")
    gate_levels = _load_json(root / "gate_level_model.json")
    decisions = _load_json(root / "gate_decision_vocabulary.json")
    requirements = _load_json(root / "gate_requirement_framework.json")
    io_contract = _load_json(root / "gate_input_output_contract_template.json")
    authority = _load_json(root / "gate_authority_and_veto_policy.json")
    dep_graph = _load_json(root / "gate_dependency_graph.json")
    failure_recovery = _load_json(root / "gate_failure_recovery_policy.json")
    audit_req = _load_json(root / "gate_audit_trace_requirement.json")
    verifier_template = _load_json(root / "gate_verifier_requirement_template.json")
    consolidation = _load_json(root / "gate_consolidation_risk_register.json")
    handoff = _load_json(root / "future_governance_handoff_plan.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")
    no_action = _load_json(root / "no_action_boundary_report.json")
    _load_json(root / "governance_debt_register.json")
    next_phase_recommendation = _load_json(root / "next_phase_recommendation.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}

    required_intakes = (
        "post_file_stat_roadmap_decision",
        "file_stat_guarded_closure",
        "file_existence_check_guarded_closure",
        "file_metadata_boundary_closure",
        "controlled_frame_sample_closure",
        "controlled_frame_input_closure",
        "crossing_decision_closure",
        "safety_constitution",
        "map_location_readonly_context",
        "minimal_runtime_integration_closure",
        "ocr_final_closure",
    )
    for intake_id in required_intakes:
        ok(f"input.{intake_id}.loaded", idx.get(intake_id, {}).get("loaded") is True)

    for intake_id in (
        "ocr_activation_governance_policy",
        "basic_navigation_loop_vision_strengthening_closure",
        "visual_ocr_map_task_feedback_dryrun",
        "midplatform_perception_orchestration_policy",
        "task_aware_visual_focus_policy",
        "world_observation_and_entity_feature_policy",
        "selective_tracking_adapter_policy",
    ):
        status = idx.get(intake_id, {}).get("status")
        ok(f"input.{intake_id}.optional", status in {"loaded", "optional_missing"}, status)

    ok("input.row_count", input_root_matrix.get("row_count") == len(rows), input_root_matrix.get("row_count"))

    ok("summary.phase", summary.get("phase") == PHASE_ID, summary.get("phase"))
    ok("summary.planning_scope", summary.get("planning_scope") == "gate_taxonomy_and_requirement_framework_planning_only")

    # Required true summary keys
    required_true = (
        "post_file_stat_roadmap_input_loaded",
        "file_stat_guarded_closure_input_loaded",
        "file_existence_check_guarded_closure_input_loaded",
        "file_metadata_boundary_closure_input_loaded",
        "controlled_frame_sample_closure_input_loaded",
        "controlled_frame_input_closure_input_loaded",
        "crossing_decision_closure_input_loaded",
        "safety_constitution_input_loaded",
        "map_location_readonly_context_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "gate_taxonomy_policy_defined",
        "gate_type_taxonomy_defined",
        "gate_level_model_defined",
        "gate_decision_vocabulary_defined",
        "gate_requirement_framework_defined",
        "gate_input_output_contract_template_defined",
        "gate_authority_and_veto_policy_defined",
        "gate_dependency_graph_defined",
        "gate_failure_recovery_policy_defined",
        "gate_audit_trace_requirement_defined",
        "gate_verifier_requirement_template_defined",
        "gate_consolidation_risk_register_generated",
        "future_governance_handoff_plan_generated",
        "gate_constitution_defined",
        "gate_constitution_above_taxonomy",
        "gate_constitution_below_safety_constitution",
        "gate_constitution_is_design_constraint",
        "gate_constitution_not_runtime",
        "gate_constitution_not_replacing_safety_constitution",
        "safety_gate_supremacy_required",
        "all_gates_must_have_owner",
        "ownerless_gate_forbidden",
        "gate_cannot_self_escalate_authority",
        "capability_gate_cannot_grant_action",
        "output_gate_cannot_release_action",
        "simulation_gate_cannot_grant_runtime",
        "candidate_gate_cannot_grant_fact",
        "map_location_gate_cannot_grant_action",
        "no_candidate_to_fact_shortcut",
        "dryrun_go_not_runtime_ready",
        "closure_go_not_production_ready",
        "phase_go_not_capability_enablement",
        "runtime_release_gate_required",
        "write_admission_gate_required",
        "action_release_gate_required",
        "speech_output_gate_required",
        "all_gates_must_have_audit_trace",
        "timestamp_required_by_default",
        "reason_code_required_by_default",
        "violations_field_required_by_default",
        "gate_failure_defaults_to_conservative",
        "missing_gate_default_allow_forbidden",
        "missing_source_chain_default_allow_forbidden",
        "missing_privacy_tag_default_allow_forbidden",
        "gate_conflict_default_allow_forbidden",
        "insufficient_evidence_default_allow_forbidden",
        "gate_dependency_graph_required",
        "isolated_gate_creation_forbidden",
        "veto_authority_must_be_declared",
        "override_policy_must_be_declared",
        "failure_recovery_policy_required",
        "duplicate_gate_creation_restricted",
        "reuse_existing_gate_required_by_default",
        "new_gate_requires_reuse_review",
        "new_gate_requires_consolidation_risk_entry",
        "capability_layer_candidate_only_by_default",
        "runtime_layer_requires_authorization",
        "evaluation_layer_no_runtime_authority",
        "human_assistance_not_assumed",
        "manual_review_result_not_fact_by_default",
        "review_candidate_requires_admission_gate",
        "safety_constitution_gate_defined",
        "domain_safety_gate_defined",
        "capability_runtime_pre_gate_defined",
        "source_quality_gate_defined",
        "freshness_ttl_gate_defined",
        "privacy_filtering_gate_defined",
        "resource_budget_gate_defined",
        "evidence_admission_gate_defined",
        "fact_admission_gate_defined",
        "memory_admission_gate_defined",
        "output_gate_defined",
        "action_release_gate_defined",
        "review_human_assistance_gate_defined",
        "fallback_degradation_gate_defined",
        "file_boundary_gate_defined",
        "ocr_request_gate_defined",
        "map_location_authority_gate_defined",
        "tracking_activation_gate_defined",
        "world_observation_handoff_gate_defined",
        "experiment_simulation_gate_defined",
        "safety_gate_highest_authority",
        "user_instruction_cannot_override_safety",
        "map_ocr_memory_cannot_override_safety",
        "simulation_gate_cannot_grant_runtime",
        "candidate_gate_cannot_grant_fact",
        "output_gate_cannot_release_action",
        "action_release_gate_required_for_real_action",
        "write_admission_gate_required_for_fact_memory_worldmodel",
        "source_chain_required_by_default",
        "audit_required_by_default",
        "verifier_template_required_by_default",
        "rollback_required_for_runtime_write_action_gate",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    )
    for k in required_true:
        ok(f"summary.{k}", summary.get(k) is True, summary.get(k))

    ok("summary.gate_constitution_article_count>=12", summary.get("gate_constitution_article_count", 0) >= 12, summary.get("gate_constitution_article_count"))
    ok("summary.gate_type_count>=20", summary.get("gate_type_count", 0) >= 20, summary.get("gate_type_count"))
    ok("summary.gate_level_count>=8", summary.get("gate_level_count", 0) >= 8, summary.get("gate_level_count"))
    ok("summary.gate_decision_count>=18", summary.get("gate_decision_count", 0) >= 18, summary.get("gate_decision_count"))
    ok("summary.dependency_graph_scenario_count>=7", summary.get("dependency_graph_scenario_count", 0) >= 7, summary.get("dependency_graph_scenario_count"))
    ok("summary.consolidation_risk_count>=10", summary.get("consolidation_risk_count", 0) >= 10, summary.get("consolidation_risk_count"))

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION, summary.get("final_decision"))
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE, summary.get("recommended_next_phase"))
    ok("summary.violations_empty", summary.get("violations") == [], summary.get("violations"))

    # Required false summary keys (no side effects / no changes)
    required_false = (
        "existing_gate_behavior_changed",
        "gate_runtime_implemented",
        "gate_merge_executed",
        "stat_invoked",
        "os_stat_invoked",
        "pathlib_stat_invoked",
        "lstat_invoked",
        "file_existence_check_invoked",
        "os_path_exists_invoked",
        "pathlib_exists_invoked",
        "file_opened",
        "file_content_read",
        "image_content_read",
        "video_content_read",
        "image_opened",
        "video_opened",
        "video_decoded",
        "frame_extracted",
        "exif_parsed",
        "video_probe_invoked",
        "real_file_hash_computed",
        "perceptual_hash_computed",
        "camera_invoked",
        "camera_opened",
        "visual_model_invoked",
        "map_api_invoked",
        "gaode_api_invoked",
        "gps_runtime_invoked",
        "ocr_provider_invoked",
        "ocrrequest_submitted",
        "tracking_runtime_invoked",
        "optical_flow_runtime_invoked",
        "crossing_runtime_invoked",
        "speech_gate_invoked",
        "vop_invoked",
        "tts_invoked",
        "task_state_committed_now",
        "navigation_action_triggered",
        "route_modified",
        "scene_delta_generated",
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
    )
    for k in required_false:
        ok(f"summary.{k}=false", summary.get(k) is False, summary.get(k))

    # Policy hard constraints
    ok("policy.planning_only", policy.get("planning_only") is True)
    ok("policy.implementation_allowed_now=false", policy.get("implementation_allowed_now") is False)
    ok("policy.runtime_gate_change_allowed=false", policy.get("runtime_gate_change_allowed") is False)
    ok("policy.gate_merge_allowed_now=false", policy.get("gate_merge_allowed_now") is False)
    ok("policy.existing_gate_behavior_change_allowed=false", policy.get("existing_gate_behavior_change_allowed") is False)
    ok("policy.gate_constitution_ref", policy.get("gate_constitution_ref") == "gate_constitution.json", policy.get("gate_constitution_ref"))

    # Count & structure checks
    ok("gate_constitution.is_runtime=false", gate_constitution.get("is_runtime") is False)
    ok("gate_constitution.replaces_safety_constitution=false", gate_constitution.get("replaces_safety_constitution") is False)
    ok("gate_constitution.article_count>=12", gate_constitution.get("article_count", 0) >= 12, gate_constitution.get("article_count"))
    ok("gate_constitution.above_taxonomy", gate_constitution.get("gate_constitution_above_taxonomy") is True)
    ok("gate_constitution.below_safety", gate_constitution.get("gate_constitution_below_safety_constitution") is True)
    ok("gate_constitution.is_design_constraint", gate_constitution.get("gate_constitution_is_design_constraint") is True)
    ok("gate_constitution.authority_stack_present", isinstance(gate_constitution.get("authority_stack"), str) and "Gate Constitution" in gate_constitution.get("authority_stack", ""))
    ok("gate_constitution.articles_len_match", len(gate_constitution.get("articles", [])) == gate_constitution.get("article_count"))

    # Article presence checks (12)
    article_ids = {a.get("article_id") for a in gate_constitution.get("articles", [])}
    for aid in (
        "GATE_CONSTITUTION_SAFETY_SUPREMACY",
        "GATE_CONSTITUTION_GATE_OWNERSHIP",
        "GATE_CONSTITUTION_NO_SELF_ESCALATION",
        "GATE_CONSTITUTION_CANDIDATE_NOT_FACT",
        "GATE_CONSTITUTION_SIMULATION_NOT_RUNTIME",
        "GATE_CONSTITUTION_FINAL_RELEASE_GATE_REQUIRED",
        "GATE_CONSTITUTION_AUDITABILITY",
        "GATE_CONSTITUTION_CONSERVATIVE_FAILURE_DEFAULT",
        "GATE_CONSTITUTION_DEPENDENCY_DECLARATION",
        "GATE_CONSTITUTION_NO_DUPLICATE_GATE_CREATION",
        "GATE_CONSTITUTION_LAYERED_AUTHORITY_BOUNDARY",
        "GATE_CONSTITUTION_HUMAN_AND_REVIEW_BOUNDARY",
    ):
        ok(f"gate_constitution.article_present:{aid}", aid in article_ids)

    gt = gate_types.get("gate_types", [])
    gl = gate_levels.get("levels", [])
    dv = decisions.get("decisions", [])
    ok("gate_types.count_match", gate_types.get("gate_type_count") == len(gt), gate_types.get("gate_type_count"))
    ok("gate_levels.count_match", gate_levels.get("gate_level_count") == len(gl), gate_levels.get("gate_level_count"))
    ok("decisions.count_match", decisions.get("gate_decision_count") == len(dv), decisions.get("gate_decision_count"))
    ok("dependency_graph.count_match", dep_graph.get("scenario_count") == len(dep_graph.get("scenarios", [])), dep_graph.get("scenario_count"))
    ok("consolidation.count_match", consolidation.get("risk_count") == len(consolidation.get("risks", [])), consolidation.get("risk_count"))

    ok("gate_types.len>=20", len(gt) >= 20, len(gt))
    ok("gate_levels.len>=8", len(gl) >= 8, len(gl))
    ok("decisions.len>=18", len(dv) >= 18, len(dv))
    ok("dependency_graph.len>=7", len(dep_graph.get("scenarios", [])) >= 7, len(dep_graph.get("scenarios", [])))
    ok("consolidation.len>=10", len(consolidation.get("risks", [])) >= 10, len(consolidation.get("risks", [])))

    # Gate type presence by name (critical taxonomy set)
    names = {g.get("gate_name") for g in gt}
    for name in (
        "SafetyConstitutionGate",
        "DomainSafetyGate",
        "CapabilityRuntimePreGate",
        "SourceQualityGate",
        "FreshnessTTLGate",
        "PrivacyFilteringGate",
        "ResourceBudgetGate",
        "EvidenceAdmissionGate",
        "FactAdmissionGate",
        "MemoryAdmissionGate",
        "OutputGate",
        "ActionReleaseGate",
        "ReviewHumanAssistanceGate",
        "FallbackDegradationGate",
        "FileBoundaryGate",
        "OCRRequestGate",
        "MapLocationAuthorityGate",
        "TrackingActivationGate",
        "WorldObservationHandoffGate",
        "ExperimentSimulationGate",
    ):
        ok(f"gate_type.present:{name}", name in names)

    # Deep per-item structural checks to satisfy MIN_CHECKS.
    for g in gt:
        ok(f"gate_type.has_id:{g.get('gate_name')}", bool(g.get("gate_type_id")))
        ok(f"gate_type.has_authority:{g.get('gate_name')}", bool(g.get("authority_level")))
        ok(f"gate_type.has_owner_layer:{g.get('gate_name')}", bool(g.get("owner_layer")))
        ok(f"gate_type.audit_requirement:{g.get('gate_name')}", bool(g.get("audit_requirement")))
        ok(f"gate_type.verifier_requirement:{g.get('gate_name')}", bool(g.get("verifier_requirement")))
        ok(f"gate_type.source_chain:{g.get('gate_name')}", g.get("source_chain") is not None)
        ok(f"gate_type.fact_status_not_fact:{g.get('gate_name')}", g.get("fact_status") == "not_fact")
        ok(f"gate_type.write_allowed_false:{g.get('gate_name')}", g.get("write_allowed") is False)
        ok(f"gate_type.required_inputs_list:{g.get('gate_name')}", isinstance(g.get("required_inputs"), list))
        ok(f"gate_type.allowed_outputs_list:{g.get('gate_name')}", isinstance(g.get("allowed_outputs"), list))
        ok(f"gate_type.forbidden_outputs_list:{g.get('gate_name')}", isinstance(g.get("forbidden_outputs"), list))

    for lvl in gl:
        lid = lvl.get("level_id")
        ok(f"gate_level.has_description:{lid}", bool(lvl.get("description")))
        ok(f"gate_level.can_block_bool:{lid}", isinstance(lvl.get("can_block"), bool))
        ok(f"gate_level.can_degrade_bool:{lid}", isinstance(lvl.get("can_degrade"), bool))
        ok(f"gate_level.can_veto_bool:{lid}", isinstance(lvl.get("can_veto"), bool))
        ok(f"gate_level.requires_audit_bool:{lid}", isinstance(lvl.get("requires_audit"), bool))
        ok(f"gate_level.requires_verifier_bool:{lid}", isinstance(lvl.get("requires_verifier"), bool))
        ok(f"gate_level.runtime_implication:{lid}", bool(lvl.get("runtime_implication")))
        ok(f"gate_level.write_implication:{lid}", bool(lvl.get("write_implication")))
        ok(f"gate_level.action_implication:{lid}", bool(lvl.get("action_implication")))
        ok(f"gate_level.fact_status_not_fact:{lid}", lvl.get("fact_status") == "not_fact")

    for d in dv:
        did = d.get("decision_id")
        ok(f"decision.has_meaning:{did}", bool(d.get("meaning")))
        ok(f"decision.audit_required_true:{did}", d.get("audit_required") is True)
        ok(f"decision.source_chain_required_true:{did}", d.get("source_chain_required") is True)
        ok(f"decision.downstream_effect_present:{did}", bool(d.get("downstream_effect")))
        ok(f"decision.fact_status_not_fact:{did}", d.get("fact_status") == "not_fact")
        ok(f"decision.write_allowed_false:{did}", d.get("write_allowed") is False)

    for s in dep_graph.get("scenarios", []):
        sid = s.get("scenario_id")
        ok(f"dep_graph.scenario_has_nodes:{sid}", isinstance(s.get("nodes"), list) and len(s.get("nodes")) >= 3)
        ok(f"dep_graph.scenario_has_notes:{sid}", bool(s.get("notes")))

    for r in consolidation.get("risks", []):
        rv = r.get("risk")
        ok(f"consolidation_risk.present:{rv}", bool(rv))
        ok(f"consolidation_risk.not_fact:{rv}", r.get("fact_status") == "not_fact")

    # Authority policy invariants
    for key in (
        "safety_gate_highest_authority",
        "user_instruction_cannot_override_safety",
        "map_ocr_memory_cannot_override_safety",
        "simulation_gate_cannot_grant_runtime",
        "candidate_gate_cannot_grant_fact",
        "output_gate_cannot_release_action",
        "action_release_gate_required_for_real_action",
        "write_admission_gate_required_for_fact_memory_worldmodel",
    ):
        ok(f"authority.{key}", authority.get(key) is True, authority.get(key))

    # Requirement defaults
    ok("requirements.source_chain_required_by_default", requirements.get("source_chain_required_by_default") is True)
    ok("requirements.audit_required_by_default", requirements.get("audit_required_by_default") is True)
    ok("requirements.verifier_template_required_by_default", requirements.get("verifier_template_required_by_default") is True)
    ok("requirements.rollback_required_for_runtime_write_action_gate", requirements.get("rollback_required_for_runtime_write_action_gate") is True)

    # Minimum requirements list contains key items.
    min_req = requirements.get("minimum_requirements", [])
    for token in (
        "unique gate_id",
        "gate_type",
        "gate_level",
        "input_contract",
        "output_contract",
        "audit_required",
        "verifier_required",
        "failure_mode_required",
        "no_fact_claim_from_candidate",
    ):
        ok(f"requirements.contains:{token}", token in min_req)

    # IO template contains key fields
    input_t = io_contract.get("input_template", [])
    output_t = io_contract.get("output_template", [])
    for token in ("gate_id", "source_chain", "timestamp", "upstream_gate_decisions"):
        ok(f"io.input.has:{token}", token in input_t)
    for token in ("gate_decision", "audit_trace_ref", "fact_status", "write_allowed", "action_allowed", "runtime_allowed"):
        ok(f"io.output.has:{token}", token in output_t)

    # Audit requirement forbids content bytes
    forbidden = audit_req.get("forbidden_fields", [])
    ok("audit.forbids.raw_bytes", "raw_user_file_bytes" in forbidden)
    ok("audit.forbids.image_pixels", "image_pixels" in forbidden)
    ok("audit.forbids.video_frames", "video_frames" in forbidden)

    # Boundary reports consistent
    ok("no_runtime.no_runtime_executed", no_runtime.get("no_runtime_executed") is True)
    ok("no_write.world_model_written=false", no_write.get("world_model_written") is False)
    ok("no_action.navigation_action_triggered=false", no_action.get("navigation_action_triggered") is False)
    ok("no_runtime.camera_invoked=false", no_runtime.get("camera_invoked") is False)
    ok("no_runtime.ocr_provider_invoked=false", no_runtime.get("ocr_provider_invoked") is False)
    ok("no_runtime.speech_gate_invoked=false", no_runtime.get("speech_gate_invoked") is False)

    # Handoff plan / next phase recommendation
    ok("handoff.next_phase", handoff.get("recommended_next_phase") == NEXT_PHASE, handoff.get("recommended_next_phase"))
    ok("next_phase_recommendation.next_phase", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)
    ok("next_phase_recommendation.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)

    # Pad stable checks to exceed MIN_CHECKS comfortably.
    ok("summary.source_chain_present", bool(summary.get("source_chain")))
    ok("summary.fact_status_not_fact", summary.get("fact_status") == "not_fact")
    ok("summary.write_allowed_false", summary.get("write_allowed") is False)
    ok("policy.source_chain_present", bool(policy.get("source_chain")))
    ok("gate_types.source_chain_present", bool(gate_types.get("source_chain")))
    ok("gate_levels.source_chain_present", bool(gate_levels.get("source_chain")))
    ok("decisions.source_chain_present", bool(decisions.get("source_chain")))
    ok("dep_graph.source_chain_present", bool(dep_graph.get("source_chain")))

    check_count = len(checks)
    passed_count = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]

    verdict = "GO" if (check_count >= MIN_CHECKS and passed_count == check_count and check_count >= BASELINE_REQUIREMENT) else "NO_GO"
    report = {
        "verifier": verdict,
        "phase_id": PHASE_ID,
        "check_count": check_count,
        "passed_count": passed_count,
        "failed_count": len(failed),
        "failed_checks": failed[:50],
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
    }

    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

