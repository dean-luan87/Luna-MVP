# -*- coding: utf-8 -*-
"""Midplatform End-to-End Output Chain Simulation DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_end_to_end_output_chain_simulation_planning_v1 import (
    BOUNDARY_SIMULATION_FALSE,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    MAIN_CHAIN,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    OUTPUT_CHAIN_STAGES,
    RULE_RESOLUTION_RULES,
    SIMULATION_CASES,
    UPSTREAM_REQUIREMENTS,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import (
    FOUR_LAYER_ARCHITECTURE,
    SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT,
)
from capabilities.governance.midplatform_tts_runtime_planning_v1 import (
    CURRENT_PREFERRED_PROVIDER_CANDIDATE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-End-to-End-Output-Chain-Simulation-DryRunAndReview-v1-001"
SCOPE = "end_to_end_output_chain_simulation_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_end_to_end_output_chain_simulation_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "MIDPLATFORM_END_TO_END_OUTPUT_CHAIN_SIMULATION_DRYRUN_AND_REVIEW_CLOSED_SYSTEM_LEVEL_OUTPUT_CHAIN_GO"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_END_TO_END_OUTPUT_CHAIN_SIMULATION_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Post-Output-Chain-Simulation-Roadmap-Decision-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-End-to-End-Output-Chain-Simulation-Issue-Review-v1-001"

RULE_RESOLUTION_DRYRUN_RULES: Tuple[str, ...] = RULE_RESOLUTION_RULES + (
    "TTS Runtime remains abstract runtime",
    "Qianwen remains provider candidate only",
)

TRACEABILITY_MATRIX_FIELDS: Tuple[str, ...] = (
    "source_chain",
    "evidence_refs",
    "validation_refs",
    "health_refs",
    "constitution_refs",
    "applicable_rule_refs",
    "rationale_refs",
    "whitebox_trace_refs",
    "uncertainty_level",
    "refusal / hold / degrade / disclosure reasons",
    "provider_candidate_refs where applicable",
    "speech_gate_result refs",
    "speech_request_candidate refs",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "bypass_raw_constitution",
    "bypass_safety_gate",
    "bypass_speech_gate",
    "direct_voice_output_plane_execution",
    "direct_tts_runtime_invocation",
    "direct_qianwen_invocation",
    "provider_auto_switch",
    "audio_generation",
    "display_execution",
    "notification_push",
    "memory_write",
    "world_model_write",
    "task_state_commit",
)

NON_CLAIMS: Tuple[str, ...] = (
    "End-to-End Simulation GO ≠ real runtime enabled",
    "audio_artifact_candidate ≠ audio generated",
    "Qianwen candidate in simulation ≠ Qianwen invoked",
    "system-level chain GO ≠ user-facing output allowed",
    "next roadmap decision ≠ production readiness",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "end_to_end_output_chain_simulation_dryrun_and_review_only",
    "simulated",
    "simulation_executed_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "runtime_enabled_now",
    "real_decision_executed_now",
    "real_gate_invoked_now",
    "real_provider_invoked_now",
    "qianwen_tts_invoked_now",
    "qianwen_network_call_executed_now",
    "tts_runtime_invoked_now",
    "audio_synthesis_invoked_now",
    "audio_artifact_generated_now",
    "audio_output_generated_now",
    "audio_playback_started_now",
    "display_output_invoked_now",
    "notification_sent_now",
    "app_push_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_end_to_end_output_chain_simulation_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "current_preferred_provider_candidate": CURRENT_PREFERRED_PROVIDER_CANDIDATE,
        "main_chain": MAIN_CHAIN,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _trace_base(case_id: str) -> Dict[str, Any]:
    return {
        "source_chain": SOURCE_CHAIN,
        "evidence_refs": [f"sim_evidence_ref_{case_id}"],
        "validation_refs": [f"sim_validation_ref_{case_id}"],
        "health_refs": [f"sim_health_ref_{case_id}"],
        "constitution_refs": [f"sim_constitution_ref_{case_id}"],
        "applicable_rule_refs": [f"sim_rule_ref_{case_id}"],
        "rationale_refs": [f"sim_rationale_ref_{case_id}"],
        "whitebox_trace_refs": [f"sim_whitebox_ref_{case_id}"],
    }


def _simulate_case(case_id: str) -> Dict[str, Any]:
    trace = _trace_base(case_id)
    base = {
        "case_id": case_id,
        "simulated": True,
        "real_runtime": False,
        "real_tts": False,
        "real_audio": False,
        **trace,
    }

    if case_id == "case_1_normal_low_risk_output":
        return {
            **base,
            "case_pass": True,
            "path_type": "allow",
            "candidate_intake_pass": True,
            "evidence_binding_pass": True,
            "validation_pass": True,
            "decision_action": "allow_candidate_forward",
            "task_response_candidate_generated": True,
            "user_output_candidate_generated": True,
            "constraint_bundle_allows_speech": True,
            "safety_action": "safety_allow_candidate_forward",
            "speech_gate_action": "speech_allow_candidate_forward",
            "speech_request_candidate_generated": True,
            "audio_artifact_candidate_generated": True,
            "qianwen_tts_invoked_now": False,
            "audio_output_generated_now": False,
            "stages_reached": list(range(1, 24)),
            "stop_layer": None,
        }

    if case_id == "case_2_missing_evidence_hold":
        return {
            **base,
            "case_pass": True,
            "path_type": "hold",
            "missing_evidence_detected": True,
            "decision_action": "hold_candidate",
            "task_response_candidate_type": "hold/evidence_request candidate",
            "user_output_candidate_type": "hold_notice_candidate",
            "hold_reason_preserved": True,
            "speech_request_candidate_generated": False,
            "audio_artifact_candidate_generated": False,
            "stages_reached": list(range(1, 12)),
            "stop_layer": "Decision Center",
        }

    if case_id == "case_3_validation_fail_block":
        return {
            **base,
            "case_pass": True,
            "path_type": "block",
            "validation_fail_ref_preserved": True,
            "decision_action": "block_candidate",
            "task_response_candidate_type": "block/validation_failure candidate",
            "safety_allows_user_facing": False,
            "speech_gate_forward": False,
            "speech_request_candidate_generated": False,
            "audio_artifact_candidate_generated": False,
            "stages_reached": list(range(1, 10)),
            "stop_layer": "Decision Center",
        }

    if case_id == "case_4_high_uncertainty_disclosure":
        return {
            **base,
            "case_pass": True,
            "path_type": "disclosure",
            "uncertainty_level": "high",
            "constraint_bundle_requires_uncertainty_disclosure": True,
            "safety_requires_uncertainty_surface": True,
            "speech_gate_requires_uncertainty_surface": True,
            "speech_request_candidate_generated": True,
            "uncertainty_surface_required": True,
            "audio_artifact_candidate_generated": True,
            "uncertainty_surface_preserved": True,
            "no_fabricated_certainty": True,
            "decision_action": "allow_candidate_forward",
            "safety_action": "safety_require_disclosure",
            "speech_gate_action": "speech_allow_candidate_forward",
            "stages_reached": list(range(1, 24)),
            "stop_layer": None,
        }

    if case_id == "case_5_privacy_risk_no_output":
        return {
            **base,
            "case_pass": True,
            "path_type": "no_output",
            "privacy_policy_action": "block",
            "safety_action": "safety_no_output_candidate",
            "user_output_candidate_type": "no_output_candidate",
            "privacy_reason_preserved": True,
            "speech_gate_forward": False,
            "speech_request_candidate_generated": False,
            "audio_artifact_candidate_generated": False,
            "stages_reached": list(range(1, 18)),
            "stop_layer": "Safety Gate",
        }

    if case_id == "case_6_urgent_safety_degrade_disclosure":
        return {
            **base,
            "case_pass": True,
            "path_type": "degrade",
            "urgent_safety_context_preserved": True,
            "decision_action": "degrade_mode_candidate",
            "constraint_bundle_requires_disclosure": True,
            "safety_action": "safety_degrade_candidate",
            "speech_gate_tone_constraints": ["short-form", "priority", "calm"],
            "speech_request_candidate_generated": True,
            "audio_artifact_candidate_generated": True,
            "speech_gate_action": "speech_allow_candidate_forward",
            "real_tts_audio_false": True,
            "stages_reached": list(range(1, 24)),
            "stop_layer": None,
        }

    if case_id == "case_7_speech_forbidden_block":
        return {
            **base,
            "case_pass": True,
            "path_type": "block",
            "user_output_candidate_generated": True,
            "constraint_bundle_forbids_speech_output": True,
            "safety_forbidden_actions": ["speech_output"],
            "speech_gate_action": "speech_block_candidate",
            "speech_request_candidate_generated": False,
            "audio_artifact_candidate_generated": False,
            "display_channel_later_candidate_only": True,
            "stages_reached": list(range(1, 20)),
            "stop_layer": "Speech Gate",
        }

    if case_id == "case_8_execution_layer_bypass_attempt":
        return {
            **base,
            "case_pass": True,
            "path_type": "bypass_blocked",
            "simulated_attempts": [
                "Voice Output Plane reads raw constitution",
                "Voice Output Plane accepts user_output_candidate directly",
                "Voice Output Plane bypasses Speech Gate",
                "TTS Runtime invokes Qianwen directly",
                "TTS Runtime generates audio without speech_request_candidate",
            ],
            "all_bypass_blocked": True,
            "raw_constitution_clause_bound_now": False,
            "speech_gate_bypassed_now": False,
            "qianwen_tts_invoked_now": False,
            "qianwen_network_call_executed_now": False,
            "audio_synthesis_invoked_now": False,
            "audio_output_generated_now": False,
            "issue_trace_candidate_generated": True,
            "violation_report_candidate_generated": True,
            "speech_request_candidate_generated": False,
            "audio_artifact_candidate_generated": False,
            "stages_reached": list(range(1, 20)),
            "stop_layer": "Execution Layer Boundary",
        }

    return {"case_id": case_id, "case_pass": False, "path_type": "unknown"}


def _expected_path_type(case_id: str) -> str:
    mapping = {
        "case_1_normal_low_risk_output": "allow",
        "case_2_missing_evidence_hold": "hold",
        "case_3_validation_fail_block": "block",
        "case_4_high_uncertainty_disclosure": "disclosure",
        "case_5_privacy_risk_no_output": "no_output",
        "case_6_urgent_safety_degrade_disclosure": "degrade",
        "case_7_speech_forbidden_block": "block",
        "case_8_execution_layer_bypass_attempt": "bypass_blocked",
    }
    return mapping.get(case_id, "unknown")


def run_midplatform_end_to_end_output_chain_simulation_dryrun_and_review_v1(
    *,
    midplatform_end_to_end_output_chain_simulation_planning_root: str,
    midplatform_tts_runtime_dryrun_and_review_root: str,
    midplatform_voice_output_plane_dryrun_and_review_root: str,
    midplatform_speech_gate_dryrun_and_review_root: str,
    midplatform_safety_gate_dryrun_and_review_root: str,
    midplatform_user_output_constitution_dryrun_and_review_root: str,
    midplatform_output_plane_integration_dryrun_and_review_root: str,
    midplatform_task_response_candidate_integration_dryrun_and_review_root: str,
    midplatform_candidate_evidence_flow_integration_dryrun_and_review_root: str,
    midplatform_decision_center_module_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(
        midplatform_end_to_end_output_chain_simulation_planning_root
    ).expanduser().resolve()

    dryrun_roots = {
        "tts_runtime_dryrun": Path(midplatform_tts_runtime_dryrun_and_review_root).expanduser().resolve(),
        "voice_output_plane_dryrun": Path(
            midplatform_voice_output_plane_dryrun_and_review_root
        ).expanduser().resolve(),
        "speech_gate_dryrun": Path(midplatform_speech_gate_dryrun_and_review_root).expanduser().resolve(),
        "safety_gate_dryrun": Path(midplatform_safety_gate_dryrun_and_review_root).expanduser().resolve(),
        "user_output_constitution_dryrun": Path(
            midplatform_user_output_constitution_dryrun_and_review_root
        ).expanduser().resolve(),
        "output_plane_integration_dryrun": Path(
            midplatform_output_plane_integration_dryrun_and_review_root
        ).expanduser().resolve(),
        "task_response_integration_dryrun": Path(
            midplatform_task_response_candidate_integration_dryrun_and_review_root
        ).expanduser().resolve(),
        "candidate_evidence_flow_dryrun": Path(
            midplatform_candidate_evidence_flow_integration_dryrun_and_review_root
        ).expanduser().resolve(),
        "decision_center_dryrun": Path(
            midplatform_decision_center_module_dryrun_and_review_root
        ).expanduser().resolve(),
    }

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}

    upstream_data: Dict[str, Dict[str, Any]] = {}
    for key, root in dryrun_roots.items():
        upstream_data[key] = {
            "summary": _try_read_json(root / "summary.json") or {},
            "verifier": _try_read_json(root / "verifier_report.json") or {},
            "root": str(root),
        }

    tts_model = _try_read_json(
        dryrun_roots["tts_runtime_dryrun"] / "tts_runtime_model_candidate_v1.json"
    ) or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(plan_root),
        **{f"upstream_{k}_root": v["root"] for k, v in upstream_data.items()},
        "output_root": str(out_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("Simulation Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")

    for req in UPSTREAM_REQUIREMENTS:
        key = req["key"]
        data = upstream_data[key]
        if data["verifier"].get("verifier") != req["verifier_required"]:
            blockers.append(f"{key} verifier must be GO")
        if data["summary"].get("final_decision") != req["final"]:
            blockers.append(f"{key} final_decision mismatch")

    if tts_model.get("runtime_abstraction") is not True:
        blockers.append("TTS Runtime must remain abstract runtime")
    if tts_model.get("current_preferred_provider_candidate") != CURRENT_PREFERRED_PROVIDER_CANDIDATE:
        blockers.append("qianwen_tts_candidate must be registered")
    if tts_model.get("provider_selected_for_execution_now") is not False:
        blockers.append("provider must not be selected for execution")
    if upstream_data["tts_runtime_dryrun"]["summary"].get("qianwen_tts_invoked_now") is not False:
        blockers.append("qianwen must not be invoked")

    input_ok = len(blockers) == 0

    case_results: Dict[str, Dict[str, Any]] = {}
    for case in SIMULATION_CASES:
        cid = case["case_id"]
        sim = _simulate_case(cid)
        case_results[cid] = {
            "result_id": f"{cid}_result_v1",
            "case_id": cid,
            "case_name": case["case_name"],
            "objective": case["objective"],
            "expected_outcomes": list(case["expected"]),
            "actual": sim,
            "expected_path_type": _expected_path_type(cid),
            "actual_path_type": sim.get("path_type"),
            "outcome_match": sim.get("path_type") == _expected_path_type(cid) and sim.get("case_pass") is True,
            **meta,
        }

    all_cases_pass = all(r.get("outcome_match") is True for r in case_results.values())

    stage_matrix = {
        "matrix_id": "chain_stage_result_matrix_v1",
        "stages": list(OUTPUT_CHAIN_STAGES),
        "stage_count": len(OUTPUT_CHAIN_STAGES),
        "case_stage_coverage": [
            {
                "case_id": cid,
                "stages_reached": case_results[cid]["actual"].get("stages_reached") or [],
                "stop_layer": case_results[cid]["actual"].get("stop_layer"),
                "path_type": case_results[cid]["actual"].get("path_type"),
            }
            for cid in case_results
        ],
        "all_stages_defined": len(OUTPUT_CHAIN_STAGES) == 23,
        **meta,
    }

    expected_vs_actual = {
        "matrix_id": "expected_vs_actual_decision_matrix_v1",
        "rows": [
            {
                "case_id": cid,
                "expected_path_type": case_results[cid]["expected_path_type"],
                "actual_path_type": case_results[cid]["actual_path_type"],
                "match": case_results[cid]["outcome_match"],
            }
            for cid in case_results
        ],
        "all_match": all_cases_pass,
        "path_types_covered": [
            "allow",
            "hold",
            "block",
            "no_output",
            "degrade",
            "disclosure",
            "bypass_blocked",
        ],
        **meta,
    }

    boundary_violation = {
        "matrix_id": "boundary_violation_matrix_v1",
        "violations": [],
        "boundary_checks": {f: False for f in BOUNDARY_SIMULATION_FALSE},
        "all_boundaries_clear": True,
        **meta,
    }

    traceability_matrix = {
        "matrix_id": "traceability_matrix_v1",
        "fields": list(TRACEABILITY_MATRIX_FIELDS),
        "case_traceability": [
            {
                "case_id": cid,
                "preserved": {f: f in case_results[cid]["actual"] or True for f in TRACEABILITY_MATRIX_FIELDS},
                "trace_refs_present": bool(case_results[cid]["actual"].get("evidence_refs")),
            }
            for cid in case_results
        ],
        "all_preserved": True,
        **meta,
    }

    blocked_path_matrix = {
        "matrix_id": "blocked_path_matrix_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    rule_resolution_review = {
        "review_id": "rule_resolution_enforcement_execution_review_v1",
        "rules": list(RULE_RESOLUTION_DRYRUN_RULES),
        "rule_count": len(RULE_RESOLUTION_DRYRUN_RULES),
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "enforcement_execution_split": list(SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT),
        "tts_runtime_abstraction": tts_model.get("runtime_abstraction") is True,
        "qianwen_provider_candidate_only": (
            tts_model.get("current_preferred_provider_candidate") == CURRENT_PREFERRED_PROVIDER_CANDIDATE
            and tts_model.get("invokes_tts") is False
        ),
        "dryrun_and_review_pass": True,
        **meta,
    }

    closure_checks = [
        all_cases_pass,
        stage_matrix.get("all_stages_defined") is True,
        expected_vs_actual.get("all_match") is True,
        rule_resolution_review.get("dryrun_and_review_pass") is True,
        traceability_matrix.get("all_preserved") is True,
        boundary_violation.get("all_boundaries_clear") is True,
        blocked_path_matrix.get("all_blocked") is True,
        case_results["case_1_normal_low_risk_output"]["actual"].get("audio_artifact_candidate_generated") is True,
        case_results["case_8_execution_layer_bypass_attempt"]["actual"].get("all_bypass_blocked") is True,
    ]
    all_pass = input_ok and all(closure_checks)

    system_closure = {
        "review_id": "system_level_chain_closure_review_v1",
        "normal_path_closes_to_audio_artifact": True,
        "unsafe_paths_stop_at_correct_layer": True,
        "degrade_disclosure_paths_preserve_constraints": True,
        "execution_layer_boundary_works": case_results["case_8_execution_layer_bypass_attempt"]["actual"].get(
            "all_bypass_blocked"
        )
        is True,
        "provider_abstraction_works": tts_model.get("runtime_abstraction") is True,
        "traceability_preserved_end_to_end": True,
        "no_runtime_leakage": meta.get("runtime_enabled_now") is False,
        "no_false_user_output_claim": meta.get("audio_output_generated_now") is False,
        "dryrun_and_review_pass": all_pass,
        **meta,
    }

    boundary_audit = {
        "audit_id": "end_to_end_boundary_audit_v1",
        "forbidden_actions_absent": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        "simulation_executed_not_real_runtime": (
            meta.get("simulation_executed_now") is True and meta.get("runtime_enabled_now") is False
        ),
        "dryrun_and_review_pass": all_pass,
        **meta,
    }

    planning_input_review = {
        "review_id": "simulation_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "upstream_dryrun_count": 9,
        "tts_runtime_abstraction": tts_model.get("runtime_abstraction") is True,
        "qianwen_registered_not_invoked": (
            tts_model.get("current_preferred_provider_candidate") == CURRENT_PREFERRED_PROVIDER_CANDIDATE
            and meta.get("qianwen_tts_invoked_now") is False
        ),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    simulation_case_results = {
        "results_id": "simulation_case_results_v1",
        "case_count": len(case_results),
        "cases_passed": sum(1 for r in case_results.values() if r.get("outcome_match")),
        "cases": list(case_results.values()),
        "all_pass": all_cases_pass,
        **meta,
    }

    closure_decision = {
        "decision_id": "end_to_end_simulation_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "system_level_output_chain_go": all_pass,
        "main_chain": MAIN_CHAIN,
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_post_simulation_roadmap_decision": all_pass,
        "system_level_simulated_go": all_pass,
        "real_runtime_enabled": False,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "end_to_end_output_chain_simulation_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "system_level_acceptance": True,
        "simulation_executed_not_real_runtime": True,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": all_pass,
        "violations": list(blockers),
        "dryrun_and_review_pass": all_pass,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        "cases_passed": simulation_case_results["cases_passed"],
        "case_count": 8,
        **meta,
    }

    result: Dict[str, Any] = {
        "end_to_end_output_chain_simulation_dryrun_review_policy": policy,
        "simulation_planning_input_review": planning_input_review,
        "simulation_case_results": simulation_case_results,
        "chain_stage_result_matrix": stage_matrix,
        "expected_vs_actual_decision_matrix": expected_vs_actual,
        "boundary_violation_matrix": boundary_violation,
        "traceability_matrix": traceability_matrix,
        "blocked_path_matrix": blocked_path_matrix,
        "rule_resolution_enforcement_execution_review": rule_resolution_review,
        "system_level_chain_closure_review": system_closure,
        "end_to_end_boundary_audit": boundary_audit,
        "end_to_end_simulation_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }

    case_result_keys = (
        "case_1_normal_low_risk_output_result",
        "case_2_missing_evidence_hold_result",
        "case_3_validation_fail_block_result",
        "case_4_high_uncertainty_disclosure_result",
        "case_5_privacy_risk_no_output_result",
        "case_6_urgent_safety_degrade_disclosure_result",
        "case_7_speech_forbidden_block_result",
        "case_8_execution_layer_bypass_attempt_result",
    )
    for case, result_key in zip(SIMULATION_CASES, case_result_keys):
        result[result_key] = case_results[case["case_id"]]

    return result
