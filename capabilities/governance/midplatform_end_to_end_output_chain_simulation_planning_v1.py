# -*- coding: utf-8 -*-
"""Midplatform End-to-End Output Chain Simulation Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_candidate_evidence_flow_integration_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CEF_DR_FINAL_GO,
)
from capabilities.governance.midplatform_decision_center_module_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DC_DR_FINAL_GO,
)
from capabilities.governance.midplatform_output_plane_integration_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as OP_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SAFETY_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import (
    FOUR_LAYER_ARCHITECTURE,
    SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT,
)
from capabilities.governance.midplatform_speech_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SPEECH_DR_FINAL_GO,
)
from capabilities.governance.midplatform_task_response_candidate_integration_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as TRC_DR_FINAL_GO,
)
from capabilities.governance.midplatform_tts_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as TTS_DR_FINAL_GO,
    NEXT_PHASE_GO as TTS_DR_NEXT_PHASE,
)
from capabilities.governance.midplatform_tts_runtime_planning_v1 import (
    CURRENT_PREFERRED_PROVIDER_CANDIDATE,
)
from capabilities.governance.midplatform_user_output_constitution_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as UO_CONST_DR_FINAL_GO,
)
from capabilities.governance.midplatform_voice_output_plane_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VOICE_DR_FINAL_GO,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-End-to-End-Output-Chain-Simulation-Planning-v1-001"
SCOPE = "end_to_end_output_chain_simulation_planning_only"
SOURCE_CHAIN = "midplatform_end_to_end_output_chain_simulation_planning_v1"

UPSTREAM_TTS_DR_FINAL = TTS_DR_FINAL_GO
UPSTREAM_TTS_DR_NEXT = TTS_DR_NEXT_PHASE

FINAL_DECISION_GO = (
    "MIDPLATFORM_END_TO_END_OUTPUT_CHAIN_SIMULATION_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_END_TO_END_OUTPUT_CHAIN_SIMULATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-End-to-End-Output-Chain-Simulation-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-End-to-End-Output-Chain-Simulation-Issue-Review-v1-001"

MAIN_CHAIN = (
    "candidate/evidence/validation/health/whitebox → decision_request_candidate → "
    "decision_candidate → task_response_candidate → user_output_candidate → "
    "constraint_bundle → safety_gate_result_candidate / enforcement_result_candidate → "
    "speech_gate_result_candidate → speech_request_candidate → audio_artifact_candidate"
)

OUTPUT_CHAIN_STAGES: Tuple[Dict[str, str], ...] = (
    {"stage_id": 1, "stage_name": "Domain / Factory Candidate", "object_type": "domain_candidate"},
    {"stage_id": 2, "stage_name": "Evidence Pack", "object_type": "evidence_pack"},
    {"stage_id": 3, "stage_name": "Validation Result", "object_type": "validation_result"},
    {"stage_id": 4, "stage_name": "Health Signal", "object_type": "health_signal"},
    {"stage_id": 5, "stage_name": "Whitebox Visibility", "object_type": "whitebox_visibility"},
    {"stage_id": 6, "stage_name": "Candidate/Evidence Flow Integration", "object_type": "decision_request_assembly"},
    {"stage_id": 7, "stage_name": "Decision Request Candidate", "object_type": "decision_request_candidate"},
    {"stage_id": 8, "stage_name": "Decision Center", "object_type": "decision_center"},
    {"stage_id": 9, "stage_name": "Decision Candidate", "object_type": "decision_candidate"},
    {"stage_id": 10, "stage_name": "Task Response Candidate Integration", "object_type": "task_response_integration"},
    {"stage_id": 11, "stage_name": "Task Response Candidate", "object_type": "task_response_candidate"},
    {"stage_id": 12, "stage_name": "Output Plane", "object_type": "output_plane"},
    {"stage_id": 13, "stage_name": "User Output Candidate", "object_type": "user_output_candidate"},
    {"stage_id": 14, "stage_name": "Constitution Resolver", "object_type": "constitution_resolver"},
    {"stage_id": 15, "stage_name": "Constraint Bundle", "object_type": "constraint_bundle"},
    {"stage_id": 16, "stage_name": "Safety Gate", "object_type": "safety_gate"},
    {"stage_id": 17, "stage_name": "Enforcement Result Candidate", "object_type": "enforcement_result_candidate"},
    {"stage_id": 18, "stage_name": "Speech Gate", "object_type": "speech_gate"},
    {"stage_id": 19, "stage_name": "Speech Gate Result Candidate", "object_type": "speech_gate_result_candidate"},
    {"stage_id": 20, "stage_name": "Voice Output Plane", "object_type": "voice_output_plane"},
    {"stage_id": 21, "stage_name": "Speech Request Candidate", "object_type": "speech_request_candidate"},
    {"stage_id": 22, "stage_name": "TTS Runtime", "object_type": "tts_runtime"},
    {"stage_id": 23, "stage_name": "Audio Artifact Candidate", "object_type": "audio_artifact_candidate"},
)

SIMULATION_SCOPE_INCLUDED: Tuple[str, ...] = (
    "candidate intake",
    "evidence binding",
    "validation result binding",
    "health signal binding",
    "whitebox visibility binding",
    "decision_request_candidate assembly",
    "decision_candidate generation simulated",
    "task_response_candidate assembly simulated",
    "user_output_candidate assembly simulated",
    "Constitution Resolver / constraint_bundle simulated",
    "Safety Gate result simulated",
    "Speech Gate result simulated",
    "Voice Output Plane speech_request_candidate simulated",
    "TTS Runtime audio_artifact_candidate simulated",
)

SIMULATION_SCOPE_EXCLUDED: Tuple[str, ...] = (
    "real runtime",
    "real provider",
    "real TTS",
    "real audio",
    "real display",
    "real notification",
    "Memory write",
    "WorldModel write",
    "task_state commit",
    "real user-facing output",
)

SIMULATION_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "case_1_normal_low_risk_output",
        "case_name": "normal_low_risk_output",
        "plan_file": "case_1_normal_low_risk_output_plan_v1.json",
        "objective": "verify normal low-risk chain reaches audio_artifact_candidate in simulation",
        "expected": [
            "validation_pass",
            "decision_action=allow_candidate_forward",
            "task_response_candidate generated in simulation",
            "user_output_candidate generated in simulation",
            "constraint_bundle allows speech path",
            "safety_action=safety_allow_candidate_forward",
            "speech_gate_action=speech_allow_candidate_forward",
            "speech_request_candidate generated in simulation",
            "audio_artifact_candidate generated in simulation",
            "real TTS/audio remains false",
        ],
    },
    {
        "case_id": "case_2_missing_evidence_hold",
        "case_name": "missing_evidence_hold",
        "plan_file": "case_2_missing_evidence_hold_plan_v1.json",
        "objective": "verify missing evidence triggers correct hold",
        "expected": [
            "missing_evidence detected",
            "decision_action=request_more_evidence or hold_candidate",
            "task_response_candidate=hold/evidence_request candidate",
            "user_output_candidate either hold_notice candidate or no_output candidate",
            "no speech_request_candidate",
            "no audio_artifact_candidate",
        ],
    },
    {
        "case_id": "case_3_validation_fail_block",
        "case_name": "validation_fail_block",
        "plan_file": "case_3_validation_fail_block_plan_v1.json",
        "objective": "verify validation_fail blocks output chain",
        "expected": [
            "validation_fail ref preserved",
            "decision_action=block_candidate or hold_candidate",
            "task_response_candidate=block/validation_failure candidate",
            "safety gate does not allow user-facing path",
            "no speech path",
        ],
    },
    {
        "case_id": "case_4_high_uncertainty_disclosure",
        "case_name": "high_uncertainty_disclosure",
        "plan_file": "case_4_high_uncertainty_disclosure_plan_v1.json",
        "objective": "verify high uncertainty preserved through speech constraints",
        "expected": [
            "uncertainty_level=high preserved",
            "constraint_bundle requires uncertainty disclosure",
            "Safety Gate requires disclosure / uncertainty surface",
            "Speech Gate requires uncertainty surface",
            "speech_request_candidate includes uncertainty_surface_required=true",
            "TTS audio_artifact_candidate preserves uncertainty_surface_preserved=true",
        ],
    },
    {
        "case_id": "case_5_privacy_risk_no_output",
        "case_name": "privacy_risk_no_output",
        "plan_file": "case_5_privacy_risk_no_output_plan_v1.json",
        "objective": "verify privacy risk triggers no_output / hold",
        "expected": [
            "privacy_policy blocks or holds",
            "safety_action=safety_block_candidate or safety_no_output_candidate",
            "user_output_candidate=no_output_candidate",
            "no Speech Gate forward",
            "no speech_request_candidate",
        ],
    },
    {
        "case_id": "case_6_urgent_safety_degrade_disclosure",
        "case_name": "urgent_safety_degrade_disclosure",
        "plan_file": "case_6_urgent_safety_degrade_disclosure_plan_v1.json",
        "objective": "verify urgent safety reminder can degrade output with disclosure preserved",
        "expected": [
            "urgent_safety_context preserved",
            "decision_action=degrade_mode_candidate or allow with safety disclosure",
            "constraint_bundle requires disclosure",
            "Safety Gate action=safety_degrade_candidate or safety_require_disclosure",
            "Speech Gate attaches short-form / priority / calm tone constraints",
            "speech_request_candidate generated in simulation",
            "real TTS/audio remains false",
        ],
    },
    {
        "case_id": "case_7_speech_forbidden_block",
        "case_name": "speech_forbidden_block",
        "plan_file": "case_7_speech_forbidden_block_plan_v1.json",
        "objective": "verify Safety allows user output but forbids speech_output; Speech Gate blocks voice",
        "expected": [
            "user_output_candidate may exist",
            "constraint_bundle forbids speech_output",
            "Safety Gate result includes forbidden_actions=speech_output",
            "Speech Gate action=speech_block_candidate",
            "no speech_request_candidate",
            "display/other channel may remain later candidate only",
        ],
    },
    {
        "case_id": "case_8_execution_layer_bypass_attempt",
        "case_name": "execution_layer_bypass_attempt",
        "plan_file": "case_8_execution_layer_bypass_attempt_block_plan_v1.json",
        "objective": "verify execution layer bypass attempts are blocked",
        "simulated_attempts": [
            "Voice Output Plane reads raw constitution",
            "Voice Output Plane accepts user_output_candidate directly",
            "TTS Runtime invokes Qianwen directly",
            "TTS Runtime generates audio without speech_request_candidate",
        ],
        "expected": [
            "all bypass attempts blocked",
            "raw constitution read blocked",
            "speech_gate_bypassed_now=false",
            "qianwen_tts_invoked_now=false",
            "audio_synthesis_invoked_now=false",
            "violation/issue trace candidate generated in simulation",
        ],
    },
)

STAGE_HANDOFF_CONTRACTS: Tuple[Dict[str, str], ...] = (
    {"from": "candidate", "to": "evidence_pack", "ref": "candidate → evidence_pack refs preserved"},
    {"from": "evidence_pack", "to": "decision_request", "ref": "evidence_pack → decision_request refs preserved"},
    {"from": "decision_request", "to": "decision_candidate", "ref": "decision_request → decision_candidate refs preserved"},
    {"from": "decision_candidate", "to": "task_response", "ref": "decision_candidate → task_response refs preserved"},
    {"from": "task_response", "to": "user_output", "ref": "task_response → user_output refs preserved"},
    {"from": "user_output", "to": "constraint_bundle", "ref": "user_output → constraint_bundle refs preserved"},
    {"from": "constraint_bundle", "to": "safety_gate_result", "ref": "constraint_bundle → safety_gate_result refs preserved"},
    {"from": "safety_gate_result", "to": "speech_gate_result", "ref": "safety_gate_result → speech_gate_result refs preserved"},
    {"from": "speech_gate_result", "to": "speech_request_candidate", "ref": "speech_gate_result → speech_request_candidate refs preserved"},
    {"from": "speech_request_candidate", "to": "audio_artifact_candidate", "ref": "speech_request_candidate → audio_artifact_candidate refs preserved"},
)

RULE_RESOLUTION_RULES: Tuple[str, ...] = (
    "raw constitution not consumed by gates/execution layers",
    "Constraint Bundle consumed by enforcement layers",
    "Safety Gate is Enforcement Layer",
    "Speech Gate is Enforcement Layer",
    "Voice Output Plane is Execution Layer",
    "TTS Runtime is ExecutionRuntime",
    "Execution layers consume enforcement-derived results",
    "Execution layers cannot override enforcement results",
)

TRACEABILITY_FIELDS: Tuple[str, ...] = (
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
)

BOUNDARY_SIMULATION_FALSE: Tuple[str, ...] = (
    "runtime_enabled_now",
    "real_decision_executed_now",
    "real_gate_invoked_now",
    "real_provider_invoked_now",
    "qianwen_tts_invoked_now",
    "network_tts_call_executed_now",
    "audio_synthesis_invoked_now",
    "audio_output_generated_now",
    "audio_playback_started_now",
    "display_output_invoked_now",
    "notification_sent_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

EXPECTED_SIMULATION_OUTPUTS: Tuple[str, ...] = (
    "simulation_case_results_v1.json",
    "chain_stage_result_matrix_v1.json",
    "boundary_violation_matrix_v1.json",
    "traceability_matrix_v1.json",
    "expected_vs_actual_decision_matrix_v1.json",
    "blocked_path_matrix_v1.json",
    "summary.json",
    "verifier_report.json",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Simulation Planning GO ≠ simulation executed",
    "simulation case plan ≠ runtime enabled",
    "expected audio_artifact_candidate ≠ audio generated",
    "Qianwen candidate in simulation ≠ Qianwen invoked",
    "next DryRunAndReview ≠ real output allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("end_to_end_output_chain_simulation_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "simulation_executed_now",
    "runtime_enabled_now",
    "decision_runtime_enabled_now",
    "decision_executed_now",
    "validation_runtime_enabled_now",
    "safety_gate_invoked_now",
    "speech_gate_invoked_now",
    "voice_output_plane_invoked_now",
    "tts_runtime_invoked_now",
    "qianwen_tts_invoked_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "audio_synthesis_invoked_now",
    "audio_artifact_generated_now",
    "audio_output_generated_now",
    "audio_playback_started_now",
    "display_output_invoked_now",
    "notification_sent_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

UPSTREAM_REQUIREMENTS: Tuple[Dict[str, str], ...] = (
    {"key": "tts_runtime_dryrun", "final": TTS_DR_FINAL_GO, "verifier_required": "GO"},
    {"key": "voice_output_plane_dryrun", "final": VOICE_DR_FINAL_GO, "verifier_required": "GO"},
    {"key": "speech_gate_dryrun", "final": SPEECH_DR_FINAL_GO, "verifier_required": "GO"},
    {"key": "safety_gate_dryrun", "final": SAFETY_DR_FINAL_GO, "verifier_required": "GO"},
    {"key": "user_output_constitution_dryrun", "final": UO_CONST_DR_FINAL_GO, "verifier_required": "GO"},
    {"key": "output_plane_integration_dryrun", "final": OP_DR_FINAL_GO, "verifier_required": "GO"},
    {"key": "task_response_integration_dryrun", "final": TRC_DR_FINAL_GO, "verifier_required": "GO"},
    {"key": "candidate_evidence_flow_dryrun", "final": CEF_DR_FINAL_GO, "verifier_required": "GO"},
    {"key": "decision_center_dryrun", "final": DC_DR_FINAL_GO, "verifier_required": "GO"},
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_end_to_end_output_chain_simulation_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "current_preferred_provider_candidate": CURRENT_PREFERRED_PROVIDER_CANDIDATE,
        "main_chain": MAIN_CHAIN,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "display_gate_deferred_not_skipped": True,
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


def _case_plan(case: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "plan_id": case["plan_file"].replace(".json", ""),
        "case_id": case["case_id"],
        "case_name": case["case_name"],
        "objective": case["objective"],
        "expected_outcomes": list(case["expected"]),
        "simulated_attempts": list(case.get("simulated_attempts") or []),
        "simulation_only": True,
        "real_runtime": False,
        "real_tts": False,
        "real_audio": False,
        **meta,
    }


def run_midplatform_end_to_end_output_chain_simulation_planning_v1(
    *,
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

    roots = {
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

    upstream_data: Dict[str, Dict[str, Any]] = {}
    for key, root in roots.items():
        upstream_data[key] = {
            "summary": _try_read_json(root / "summary.json") or {},
            "verifier": _try_read_json(root / "verifier_report.json") or {},
            "root": str(root),
        }

    tts_model = _try_read_json(
        roots["tts_runtime_dryrun"] / "tts_runtime_model_candidate_v1.json"
    ) or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        **{f"upstream_{k}_root": v["root"] for k, v in upstream_data.items()},
        "output_root": str(out_root),
    }

    for req in UPSTREAM_REQUIREMENTS:
        key = req["key"]
        data = upstream_data[key]
        if data["verifier"].get("verifier") != req["verifier_required"]:
            blockers.append(f"{key} verifier must be GO")
        if data["summary"].get("final_decision") != req["final"]:
            blockers.append(f"{key} final_decision mismatch")

    if upstream_data["tts_runtime_dryrun"]["summary"].get("recommended_next_phase") != UPSTREAM_TTS_DR_NEXT:
        blockers.append("TTS Runtime DryRun recommended_next_phase mismatch")

    if tts_model.get("runtime_abstraction") is not True:
        blockers.append("TTS Runtime must remain abstract runtime")
    if tts_model.get("current_preferred_provider_candidate") != CURRENT_PREFERRED_PROVIDER_CANDIDATE:
        blockers.append("qianwen_tts_candidate must be current preferred provider candidate")
    if tts_model.get("provider_selected_for_execution_now") is not False:
        blockers.append("provider must not be selected for execution")
    if tts_model.get("invokes_tts") is not False:
        blockers.append("TTS Runtime must not invoke TTS in dryrun state")
    if upstream_data["tts_runtime_dryrun"]["summary"].get("qianwen_tts_invoked_now") is not False:
        blockers.append("qianwen_tts_invoked_now must be false")

    input_ok = len(blockers) == 0

    upstream_review = {
        "review_id": "upstream_output_chain_input_review_v1",
        "upstream_checks": [
            {
                "upstream": req["key"],
                "verifier": upstream_data[req["key"]]["verifier"].get("verifier"),
                "final_decision": upstream_data[req["key"]]["summary"].get("final_decision"),
                "pass": (
                    upstream_data[req["key"]]["verifier"].get("verifier") == req["verifier_required"]
                    and upstream_data[req["key"]]["summary"].get("final_decision") == req["final"]
                ),
            }
            for req in UPSTREAM_REQUIREMENTS
        ],
        "tts_runtime_abstraction": tts_model.get("runtime_abstraction") is True,
        "qianwen_registered_not_invoked": (
            tts_model.get("current_preferred_provider_candidate") == CURRENT_PREFERRED_PROVIDER_CANDIDATE
            and upstream_data["tts_runtime_dryrun"]["summary"].get("qianwen_tts_invoked_now") is False
        ),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    scope_definition = {
        "definition_id": "simulation_scope_definition_v1",
        "included": list(SIMULATION_SCOPE_INCLUDED),
        "excluded": list(SIMULATION_SCOPE_EXCLUDED),
        "included_count": len(SIMULATION_SCOPE_INCLUDED),
        "excluded_count": len(SIMULATION_SCOPE_EXCLUDED),
        "simulation_executed_now": False,
        **meta,
    }

    stage_inventory = {
        "inventory_id": "output_chain_stage_inventory_v1",
        "stages": list(OUTPUT_CHAIN_STAGES),
        "stage_count": len(OUTPUT_CHAIN_STAGES),
        **meta,
    }

    case_matrix = {
        "matrix_id": "simulation_case_matrix_v1",
        "cases": [
            {
                "case_id": c["case_id"],
                "case_name": c["case_name"],
                "plan_file": c["plan_file"],
                "objective": c["objective"],
            }
            for c in SIMULATION_CASES
        ],
        "case_count": len(SIMULATION_CASES),
        **meta,
    }

    case_plans = {
        c["plan_file"].replace("_v1.json", ""): _case_plan(c, meta) for c in SIMULATION_CASES
    }

    handoff_review = {
        "plan_id": "stage_handoff_contract_review_plan_v1",
        "handoffs": list(STAGE_HANDOFF_CONTRACTS),
        "handoff_count": len(STAGE_HANDOFF_CONTRACTS),
        "review_pass": True,
        **meta,
    }

    rule_resolution_review = {
        "plan_id": "rule_resolution_enforcement_execution_review_plan_v1",
        "rules": list(RULE_RESOLUTION_RULES),
        "rule_count": len(RULE_RESOLUTION_RULES),
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "enforcement_execution_split": list(SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT),
        "review_pass": True,
        **meta,
    }

    traceability_review = {
        "plan_id": "traceability_preservation_review_plan_v1",
        "fields": list(TRACEABILITY_FIELDS),
        "field_count": len(TRACEABILITY_FIELDS),
        "review_pass": True,
        **meta,
    }

    boundary_review = {
        "plan_id": "boundary_and_non_claims_review_plan_v1",
        "simulation_boundary_false": {f: False for f in BOUNDARY_SIMULATION_FALSE},
        "all_simulation_boundaries_false": True,
        "non_claims": list(NON_CLAIMS),
        "review_pass": True,
        **meta,
    }

    expected_outputs = {
        "contract_id": "expected_simulation_outputs_contract_v1",
        "next_phase_outputs": list(EXPECTED_SIMULATION_OUTPUTS),
        "output_count": len(EXPECTED_SIMULATION_OUTPUTS),
        **meta,
    }

    dryrun_plan = {
        "plan_id": "simulation_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "execute 8 simulated cases",
            "generate case result matrix",
            "verify allow / hold / block / degrade / no_output / bypass blocked",
            "verify full-chain traceability",
            "verify Rule Source → Resolver → Enforcement → Execution layering",
            "no real runtime / TTS / audio / display / memory / worldmodel",
            "output system-level GO / HOLD decision",
        ],
        **meta,
    }

    planning_pass = input_ok

    planning_decision = {
        "decision_id": "end_to_end_output_chain_simulation_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "main_chain": MAIN_CHAIN,
        "stage_count": len(OUTPUT_CHAIN_STAGES),
        "case_count": len(SIMULATION_CASES),
        **meta,
    }

    policy = {
        "policy_id": "end_to_end_output_chain_simulation_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "system_level_acceptance_planning": True,
        "simulation_planning_not_execution": True,
        "tts_runtime_abstract_not_qianwen": True,
        "main_chain": MAIN_CHAIN,
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
        "boundary_ok": planning_pass,
        "violations": list(blockers),
        "planning_pass": planning_pass,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    result: Dict[str, Any] = {
        "end_to_end_output_chain_simulation_planning_policy": policy,
        "upstream_output_chain_input_review": upstream_review,
        "simulation_scope_definition": scope_definition,
        "output_chain_stage_inventory": stage_inventory,
        "simulation_case_matrix": case_matrix,
        "stage_handoff_contract_review_plan": handoff_review,
        "rule_resolution_enforcement_execution_review_plan": rule_resolution_review,
        "traceability_preservation_review_plan": traceability_review,
        "boundary_and_non_claims_review_plan": boundary_review,
        "expected_simulation_outputs_contract": expected_outputs,
        "simulation_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "end_to_end_output_chain_simulation_planning_decision": planning_decision,
        "summary": summary,
    }

    for key, plan in case_plans.items():
        result[key] = plan

    return result
