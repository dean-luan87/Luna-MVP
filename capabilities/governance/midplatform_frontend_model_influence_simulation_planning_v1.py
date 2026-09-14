# -*- coding: utf-8 -*-
"""Midplatform Frontend Model Influence Simulation Planning v1.

Planning-only phase to verify that Constitution / Standard / Rule Resolution /
Enforcement / Health / Whitebox / Provider Abstraction can influence front-model
input/output contracts and behavior boundaries — without invoking real models or providers.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_end_to_end_output_chain_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as E2E_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_speech_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SPEECH_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SAFETY_DR_FINAL_GO,
)
from capabilities.governance.midplatform_tts_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as TTS_DR_FINAL_GO,
)
from capabilities.governance.midplatform_user_output_constitution_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as UO_CONST_DR_FINAL_GO,
)
from capabilities.governance.midplatform_validation_engineering_separation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VALIDATION_DR_FINAL_GO,
)
from capabilities.governance.midplatform_voice_output_plane_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VOICE_DR_FINAL_GO,
)
from capabilities.governance.midplatform_whitebox_inspection_integration_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as WHITEBOX_DR_FINAL_GO,
)
from capabilities.governance.provider_abstraction_standard_alignment_planning_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_PLANNING_FINAL_GO,
    STANDARD_ID as PROVIDER_ABSTRACTION_STANDARD_ID,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Frontend-Model-Influence-Simulation-Planning-v1-001"
SCOPE = "frontend_model_influence_simulation_planning_only"
SOURCE_CHAIN = "midplatform_frontend_model_influence_simulation_planning_v1"

FINAL_DECISION_GO = "MIDPLATFORM_FRONTEND_MODEL_INFLUENCE_SIMULATION_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_FRONTEND_MODEL_INFLUENCE_SIMULATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Frontend-Model-Influence-Simulation-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Frontend-Model-Influence-Simulation-Issue-Review-v1-001"

CORE_SIMULATION_CHAIN = (
    "Rule Source → Constitution Resolver → constraint_bundle → Enforcement Layer → "
    "enforcement_result_candidate → Frontend Model Input Contract → "
    "Frontend Model Output Contract → Whitebox / Health / Decision Center review"
)

INFLUENCE_DIMENSIONS: Tuple[str, ...] = (
    "constitution affects front model input",
    "constitution affects front model output",
    "enforcement layer affects front model actions",
    "health management affects front model runtime mode",
    "whitebox/monitoring explains influence source",
)

FRONT_MODEL_TYPES: Tuple[Dict[str, str], ...] = (
    {"type_id": 1, "model_type": "Vision front model", "domain": "Vision"},
    {"type_id": 2, "model_type": "OCR front model", "domain": "OCR"},
    {"type_id": 3, "model_type": "ASR front model", "domain": "Voice ASR"},
    {"type_id": 4, "model_type": "TTS front model", "domain": "Voice TTS"},
    {"type_id": 5, "model_type": "Map / Navigation front model", "domain": "Map"},
    {"type_id": 6, "model_type": "Generic response model", "domain": "Generic"},
    {"type_id": 7, "model_type": "Memory / Retrieval model candidate", "domain": "Memory"},
    {"type_id": 8, "model_type": "Tool / provider adapter model candidate", "domain": "Tool"},
)

INFLUENCE_SIGNALS: Tuple[str, ...] = (
    "front_model_input_contract",
    "front_model_output_contract",
    "constraint_bundle",
    "enforcement_result_candidate",
    "health_signal",
    "whitebox_trace",
    "provider_abstraction_status",
)

VERIFICATION_REQUIREMENTS: Tuple[str, ...] = (
    "front model does not read raw constitution directly",
    "front model consumes constraint_bundle / enforcement_result / model_io_contract only",
    "front model input clipped/masked/held/degraded/forbidden by rules",
    "front model output constrained/labeled/uncertainty-preserved/privacy-filtered",
    "provider unhealthy does not auto-switch",
    "health pressure can trigger degrade / hold / fallback candidate",
    "whitebox trace explains each influence source",
    "front model cannot bypass Decision Center / Safety Gate / Speech Gate / Provider Readiness",
)

SIMULATION_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "case_1_normal_allowed_model_input",
        "case_name": "normal_allowed_model_input",
        "objective": "rules allow standardized input_contract delivery",
        "expected": [
            "validation_pass",
            "constraint_bundle allows input",
            "front_model_input_contract delivered standardized",
            "no raw constitution in input",
        ],
    },
    {
        "case_id": "case_2_privacy_masked_input",
        "case_name": "privacy_masked_input",
        "objective": "privacy risk masks sensitive input fields",
        "expected": [
            "privacy_policy masks sensitive fields",
            "raw sensitive content not in model input",
            "mask_reason preserved in trace",
        ],
    },
    {
        "case_id": "case_3_uncertainty_required_output",
        "case_name": "uncertainty_required_output",
        "objective": "high uncertainty requires uncertainty_surface in output",
        "expected": [
            "uncertainty_level=high preserved",
            "output_contract requires uncertainty_surface",
            "no fabricated certainty",
        ],
    },
    {
        "case_id": "case_4_safety_blocked_generation",
        "case_name": "safety_blocked_generation",
        "objective": "safety block prevents speech_request/action/output generation",
        "expected": [
            "safety_action=block or no_output",
            "speech_request generation forbidden",
            "audio/display/action generation forbidden",
        ],
    },
    {
        "case_id": "case_5_health_degraded_mode",
        "case_name": "health_degraded_mode",
        "objective": "health pressure triggers degrade_mode instructions",
        "expected": [
            "health_pressure=high",
            "degrade_mode instruction in input_contract",
            "output shorter and more conservative",
        ],
    },
    {
        "case_id": "case_6_provider_not_ready",
        "case_name": "provider_not_ready",
        "objective": "provider readiness fail/unknown blocks provider invocation",
        "expected": [
            "provider_readiness=fail or unknown",
            "provider invocation forbidden",
            "hold/fallback candidate only",
        ],
    },
    {
        "case_id": "case_7_bypass_attempt",
        "case_name": "bypass_attempt",
        "objective": "direct raw constitution / provider / user output attempts blocked",
        "expected": [
            "raw constitution read blocked",
            "direct provider invocation blocked",
            "direct user output blocked",
            "violation/issue trace generated",
        ],
    },
    {
        "case_id": "case_8_rule_change_propagation",
        "case_name": "rule_change_propagation",
        "objective": "rule changes propagate via constraint_bundle version to model_io_contract",
        "expected": [
            "constraint_bundle version updated",
            "model_io_contract updated",
            "front model core not rewritten",
            "rule_refs preserved",
        ],
    },
)

BOUNDARY_MATRIX_FALSE: Tuple[str, ...] = (
    "simulation_executed_now",
    "front_model_runtime_enabled_now",
    "front_model_invoked_now",
    "real_model_invoked_now",
    "provider_invoked_now",
    "provider_selected_now",
    "provider_auto_switch_executed_now",
    "tts_runtime_invoked_now",
    "ocr_runtime_invoked_now",
    "vision_runtime_invoked_now",
    "asr_runtime_invoked_now",
    "map_runtime_invoked_now",
    "audio_synthesis_invoked_now",
    "audio_output_generated_now",
    "display_output_invoked_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "raw_constitution_read_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Frontend Model Influence Simulation Planning GO ≠ real model invoked",
    "influence mapping planned ≠ rules automatically enforced in runtime",
    "provider abstraction boundary planned ≠ provider selected",
    "Display Gate deferred remains not skipped",
    "next DryRunAndReview ≠ user-facing output allowed",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_frontend_model_influence_simulation_planning"
)


def _meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "provider_abstraction_standard_ref": PROVIDER_ABSTRACTION_STANDARD_ID,
        "frontend_model_influence_simulation_planning_only": True,
        "display_gate_deferred_not_skipped": True,
        "simulation_category": "Front Model Influence Simulation",
    }
    for f in BOUNDARY_MATRIX_FALSE:
        meta[f] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_midplatform_frontend_model_influence_simulation_planning_v1(
    *,
    provider_abstraction_standard_alignment_planning_root: str,
    midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root: str,
    midplatform_user_output_constitution_dryrun_and_review_root: str,
    midplatform_safety_gate_dryrun_and_review_root: str,
    midplatform_speech_gate_dryrun_and_review_root: str,
    midplatform_voice_output_plane_dryrun_and_review_root: str,
    midplatform_tts_runtime_dryrun_and_review_root: str,
    midplatform_validation_engineering_separation_dryrun_and_review_root: str,
    midplatform_whitebox_inspection_integration_dryrun_and_review_root: str,
    health_management_layer_integration_post_dryrun_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    roots = {
        "provider_abs_planning": Path(provider_abstraction_standard_alignment_planning_root).expanduser().resolve(),
        "e2e_dr": Path(midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root).expanduser().resolve(),
        "uo_const_dr": Path(midplatform_user_output_constitution_dryrun_and_review_root).expanduser().resolve(),
        "safety_dr": Path(midplatform_safety_gate_dryrun_and_review_root).expanduser().resolve(),
        "speech_dr": Path(midplatform_speech_gate_dryrun_and_review_root).expanduser().resolve(),
        "voice_dr": Path(midplatform_voice_output_plane_dryrun_and_review_root).expanduser().resolve(),
        "tts_dr": Path(midplatform_tts_runtime_dryrun_and_review_root).expanduser().resolve(),
        "validation_dr": Path(midplatform_validation_engineering_separation_dryrun_and_review_root).expanduser().resolve(),
        "whitebox_dr": Path(midplatform_whitebox_inspection_integration_dryrun_and_review_root).expanduser().resolve(),
        "health_dr": Path(health_management_layer_integration_post_dryrun_review_root).expanduser().resolve(),
    }

    upstream: Dict[str, Dict[str, Any]] = {}
    for key, root in roots.items():
        upstream[key] = {
            "summary": _try_read_json(root / "summary.json") or {},
            "verifier": _try_read_json(root / "verifier_report.json") or {},
            "root": str(root),
        }

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_meta(),
        **{f"upstream_{k}_root": v["root"] for k, v in upstream.items()},
        "output_root": str(out_root),
    }

    checks_expected = {
        "provider_abs_planning": (PROVIDER_ABS_PLANNING_FINAL_GO, "verifier"),
        "e2e_dr": (E2E_DR_FINAL_GO, "verifier"),
        "uo_const_dr": (UO_CONST_DR_FINAL_GO, "verifier"),
        "safety_dr": (SAFETY_DR_FINAL_GO, "verifier"),
        "speech_dr": (SPEECH_DR_FINAL_GO, "verifier"),
        "voice_dr": (VOICE_DR_FINAL_GO, "verifier"),
        "tts_dr": (TTS_DR_FINAL_GO, "verifier"),
        "validation_dr": (VALIDATION_DR_FINAL_GO, "verifier"),
        "whitebox_dr": (WHITEBOX_DR_FINAL_GO, "verifier"),
        "health_dr": (None, "verifier"),
    }

    for key, (final_expected, mode) in checks_expected.items():
        data = upstream[key]
        if data["verifier"].get("verifier") != "GO":
            blockers.append(f"{key} verifier must be GO")
        if mode == "verifier" and final_expected and data["summary"].get("final_decision") != final_expected:
            if key == "health_dr":
                if "CLOSED" not in str(data["summary"].get("final_decision", "")):
                    blockers.append("health management post dryrun must be closed GO")
            else:
                blockers.append(f"{key} final_decision mismatch")

    if upstream["provider_abs_planning"]["summary"].get("planning_pass") is not True:
        blockers.append("provider abstraction standard alignment planning must pass")

    input_ok = len(blockers) == 0

    influence_plan = {
        "plan_id": "frontend_model_influence_simulation_plan_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "simulation_category": "Front Model Influence Simulation",
        "core_simulation_chain": CORE_SIMULATION_CHAIN,
        "influence_dimensions": list(INFLUENCE_DIMENSIONS),
        "influence_signals": list(INFLUENCE_SIGNALS),
        "verification_requirements": list(VERIFICATION_REQUIREMENTS),
        "planning_only": True,
        "answers": [
            "rules do influence models via contracts and enforcement-derived permissions",
            "influence passes through constraint_bundle / enforcement_result / model_io_contract",
            "influenced results are controllable, explainable, and traceable",
        ],
        **meta,
    }

    type_inventory = {
        "inventory_id": "front_model_type_inventory_v1",
        "model_types": list(FRONT_MODEL_TYPES),
        "type_count": len(FRONT_MODEL_TYPES),
        **meta,
    }

    io_influence_matrix = {
        "matrix_id": "model_io_contract_influence_matrix_v1",
        "signals": list(INFLUENCE_SIGNALS),
        "applies_to_all_front_model_types": True,
        "influence_paths": [
            "constraint_bundle → front_model_input_contract",
            "enforcement_result_candidate → front_model_output_contract permissions",
            "health_signal → degrade/hold/fallback mode",
            "whitebox_trace → explainability refs",
            "provider_abstraction_status → provider invocation boundary",
        ],
        **meta,
    }

    rule_input_mapping = {
        "mapping_id": "rule_to_model_input_mapping_v1",
        "mappings": [
            {"rule_source": "constitution", "effect": "clip/mask/hold/forbid prompt/request/speech_text/OCR/vision input"},
            {"rule_source": "constraint_bundle", "effect": "standardize input_contract fields and versions"},
            {"rule_source": "enforcement_result", "effect": "block or degrade input permissions"},
            {"rule_source": "health_signal", "effect": "degrade_mode / hold instructions in input"},
            {"rule_source": "provider_abstraction_status", "effect": "forbid provider-direct input paths"},
        ],
        "no_raw_constitution_in_input": True,
        **meta,
    }

    rule_output_mapping = {
        "mapping_id": "rule_to_model_output_mapping_v1",
        "mappings": [
            {"rule_source": "constitution", "effect": "require uncertainty/disclosure; forbid assertion/privacy leak"},
            {"rule_source": "constraint_bundle", "effect": "constrain output_contract shape and labels"},
            {"rule_source": "enforcement_result", "effect": "forbid speech_request/audio/display/action output"},
            {"rule_source": "validation_result", "effect": "annotate confidence/uncertainty; no fact claim"},
            {"rule_source": "provider_abstraction", "effect": "output remains candidate/evidence not user_output"},
        ],
        **meta,
    }

    health_behavior_mapping = {
        "mapping_id": "health_to_model_behavior_mapping_v1",
        "mappings": [
            {"health_state": "normal", "behavior": "standard input/output contracts"},
            {"health_state": "elevated_pressure", "behavior": "degrade_mode candidate"},
            {"health_state": "high_pressure", "behavior": "hold or conservative output"},
            {"health_state": "provider_unhealthy", "behavior": "fallback candidate; no auto-switch"},
            {"health_state": "low_confidence", "behavior": "request_more_evidence / hold"},
        ],
        "provider_auto_switch_forbidden": True,
        **meta,
    }

    enforcement_permission_mapping = {
        "mapping_id": "enforcement_to_model_permission_mapping_v1",
        "mappings": [
            {"enforcement": "Safety Gate allow", "permission": "limited output generation allowed"},
            {"enforcement": "Safety Gate block/no_output", "permission": "speech_request/action/output forbidden"},
            {"enforcement": "Speech Gate allow", "permission": "speech_request_candidate path allowed"},
            {"enforcement": "Speech Gate block", "permission": "speech/audio forbidden"},
            {"enforcement": "Provider Readiness fail", "permission": "provider invocation forbidden"},
        ],
        "bypass_forbidden": [
            "Decision Center",
            "Safety Gate",
            "Speech Gate",
            "Provider Readiness",
        ],
        **meta,
    }

    whitebox_mapping = {
        "mapping_id": "whitebox_explainability_mapping_v1",
        "trace_refs": [
            "applicable_rule_refs",
            "evidence_refs",
            "health_refs",
            "rationale_refs",
            "whitebox_trace_refs",
            "constraint_bundle_version_ref",
            "enforcement_result_ref",
        ],
        "explainability_required_for": [
            "why blocked",
            "why degraded",
            "why uncertainty disclosure required",
            "why provider not invoked",
        ],
        **meta,
    }

    provider_boundary = {
        "boundary_id": "provider_abstraction_to_front_model_boundary_v1",
        "rules": [
            "front model is not provider",
            "front model consumes provider_abstraction_status not provider core",
            "provider candidate registered ≠ selected ≠ invoked",
            "provider unhealthy does not auto-switch front model provider binding",
            "adapter handles provider-specific logic outside front model core",
        ],
        "provider_abstraction_standard_ref": PROVIDER_ABSTRACTION_STANDARD_ID,
        **meta,
    }

    case_matrix = {
        "matrix_id": "simulation_case_matrix_v1",
        "cases": [
            {"case_id": c["case_id"], "case_name": c["case_name"], "objective": c["objective"]}
            for c in SIMULATION_CASES
        ],
        "case_count": len(SIMULATION_CASES),
        **meta,
    }

    expected_matrix = {
        "matrix_id": "expected_result_matrix_v1",
        "cases": [
            {"case_id": c["case_id"], "expected_outcomes": list(c["expected"])} for c in SIMULATION_CASES
        ],
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "boundary_matrix_v1",
        "all_false": True,
        "matrix": {k: False for k in BOUNDARY_MATRIX_FALSE},
        **meta,
    }

    dryrun_plan = {
        "plan_id": "dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "execute 8 front model influence simulated cases",
            "verify input/output/permission/health/whitebox influence paths",
            "verify no raw constitution read, no provider invocation, no real model runtime",
            "verify provider abstraction boundary on front models",
            "output system-level influence simulation GO/HOLD",
        ],
        **meta,
    }

    planning_pass = input_ok
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": planning_pass,
        "violations": list(blockers),
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "case_count": len(SIMULATION_CASES),
        "front_model_type_count": len(FRONT_MODEL_TYPES),
        **meta,
    }

    return {
        "frontend_model_influence_simulation_plan": influence_plan,
        "front_model_type_inventory": type_inventory,
        "model_io_contract_influence_matrix": io_influence_matrix,
        "rule_to_model_input_mapping": rule_input_mapping,
        "rule_to_model_output_mapping": rule_output_mapping,
        "health_to_model_behavior_mapping": health_behavior_mapping,
        "enforcement_to_model_permission_mapping": enforcement_permission_mapping,
        "whitebox_explainability_mapping": whitebox_mapping,
        "provider_abstraction_to_front_model_boundary": provider_boundary,
        "simulation_case_matrix": case_matrix,
        "expected_result_matrix": expected_matrix,
        "boundary_matrix": boundary_matrix,
        "dryrun_plan": dryrun_plan,
        "summary": summary,
    }
