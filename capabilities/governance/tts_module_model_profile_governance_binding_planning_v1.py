# -*- coding: utf-8 -*-
"""TTS Module Model Profile + Governance Binding Planning v1 — qualification only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONSTITUTION_BUS_DR_FINAL_GO,
)
from capabilities.governance.midplatform_controlled_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONTROLLED_RUNTIME_DR_FINAL_GO,
)
from capabilities.governance.midplatform_model_governance_binding_standardization_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as BINDING_DR_FINAL_GO,
)
from capabilities.governance.midplatform_model_governance_binding_standardization_planning_v1 import (
    CONSTITUTION_BUS_REF,
    CONTROLLED_RUNTIME_FRAMEWORK_REF,
    MODULE_LOCAL_PROFILE_STANDARD_REF,
    PROVIDER_ABS_STANDARD_ID,
    REGISTRY_REF,
    STANDARD_ID as MIDPLATFORM_BINDING_STANDARD_ID,
)
from capabilities.governance.midplatform_speech_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SPEECH_GATE_DR_FINAL_GO,
)
from capabilities.governance.midplatform_speech_gate_planning_v1 import (
    SPEECH_GATE_LAYER_POSITIONING,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    PHASE_GOVERNANCE_STANDARD_REUSE_RULE,
)
from capabilities.governance.model_profile_registry_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as REGISTRY_DR_FINAL_GO,
)
from capabilities.governance.model_profile_registry_planning_v1 import SEED_CANDIDATE_IDS
from capabilities.governance.module_local_model_profile_standardization_dryrun_and_review_v1 import (
    DEFERRED_NON_COMPLIANCE_HANDLING_PHASE,
    DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID,
)
from capabilities.governance.module_local_model_profile_standardization_planning_v1 import (
    DUAL_VALIDATION_MECHANISM_ID,
    DUAL_VALIDATION_NON_CLAIMS,
    MODULE_INTERNAL_SELF_CHECK_COVERAGE,
)
from capabilities.governance.ocr_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as OCR_DR_FINAL_GO,
)
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL_GO,
)
from capabilities.governance.vision_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VISION_DR_FINAL_GO,
)
from capabilities.governance.vision_module_model_profile_governance_binding_planning_v1 import (
    QUALIFICATION_CHECK_CRITERIA,
    QUALIFICATION_MODE,
)
from capabilities.governance.layered_capability_stack_standard_v1 import STANDARD_ID as UNIVERSAL_STACK_STANDARD_ID
from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID

PHASE_ID = "Phase-TTS-Module-Model-Profile-Governance-Binding-Planning-v1-001"
SCOPE = "tts_module_model_profile_governance_binding_planning_only"
SOURCE_CHAIN = "tts_module_model_profile_governance_binding_planning_v1"

FINAL_DECISION_GO = (
    "TTS_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "TTS_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-TTS-Module-Model-Profile-Governance-Binding-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-TTS-Module-Model-Profile-Governance-Binding-Issue-Review-v1-001"

MODULE_ID = "tts_voice_output_module"
MODULE_LOCAL_PROFILE_ID = "tts_voice_output_module_local_profile_v1"
MIDPLATFORM_BINDING_ID = "tts_voice_output_midplatform_binding_v1"
CAPABILITY_STACK_DEF_ID = "tts_capability_stack_definition_v1"
LAYERED_GOV_MAPPING_ID = "tts_layered_governance_mapping_v1"
CAPABILITY_BUS_CONTRACT_REF = "tts_voice_output_capability_bus_contract_v1"
SPEECH_GATE_REF = "midplatform_speech_gate_v1"
VOICE_OUTPUT_PLANE_REF = "midplatform_voice_output_plane_v1"

TTS_REGISTRY_REFS: Tuple[str, ...] = (
    "qianwen_tts_candidate",
    "moss_tts_style_candidate",
    "local_tts_placeholder_candidate",
)
TTS_REGISTRY_PLACEHOLDER_REGISTRY_ID = "local_tts_placeholder"

REUSED_GOVERNANCE_STANDARDS: Tuple[str, ...] = (
    "Model Profile Registry",
    "Module-Local Model Profile Standard",
    "Midplatform Model Governance Binding Standard",
    "Dual Validation Mechanism",
    "Layered Capability Stack Standard",
    "Layered Governance Mapping",
    "Constitution-Bus v1.0",
    "Provider Abstraction Standard",
    "Controlled Runtime Framework",
    "Midplatform Speech Gate",
    "Voice Output Plane boundary",
    "Health Oversight Externality",
    "Whitebox Trace Standard",
    "Candidate/Evidence Contract pattern",
    "Boundary Matrix / Blocked Path / Non-Claims pattern",
)

TTS_MIDPLATFORM_INTERACTION_CHECK_COVERAGE: Tuple[str, ...] = (
    "Constitution-Bus binding",
    "Capability Bus contract",
    "Provider Abstraction binding",
    "Speech Gate binding",
    "Voice Output Plane boundary",
    "Validation requirement",
    "Health requirement / external oversight",
    "Whitebox trace",
    "Controlled Runtime requirement",
    "source_chain / evidence / traceability preservation",
    "Memory / WorldModel non-write boundary",
)

IO_FORBIDDEN: Tuple[str, ...] = (
    "direct_user_output",
    "direct_audio_playback",
    "direct_speech_request_now",
    "direct_fact",
    "direct_action",
    "direct_memory_write",
    "direct_worldmodel_write",
    "direct_runtime_enable",
)

NON_CLAIMS: Tuple[str, ...] = (
    "TTS Module Planning GO ≠ Qianwen/MOSS/local TTS selected",
    "TTS candidate ref ≠ TTS runtime",
    "TTS output contract planned ≠ audio generation",
    "TTS binding feasible ≠ Constitution/Oversight fully integrated",
    "Health/Oversight refs attached ≠ health/supervision metrics finalized",
    "next DryRunAndReview ≠ model benchmark/runtime/audio output",
    "Module Governance Binding GO ≠ module fully integrated with Constitution",
    "Module Governance Binding GO ≠ module fully integrated with Health/Oversight",
    "Constitution binding feasible ≠ constitution effectiveness quantified",
    "Module Internal Self-Check GO ≠ Midplatform Interaction Check GO",
    "Midplatform Interaction Check GO ≠ Runtime Ready",
)

QUALIFICATION_FIELDS: Dict[str, bool] = {
    "qualification_check_only": True,
    "full_integration_certification_now": False,
    "constitution_binding_feasible": True,
    "oversight_binding_feasible": True,
    "constitution_effectiveness_quantified_now": False,
    "health_metrics_finalized_now": False,
    "supervision_metrics_finalized_now": False,
    "module_constitution_fully_integrated_now": False,
    "module_oversight_fully_integrated_now": False,
    "health_metric_detail_defined_now": False,
    "supervision_metric_detail_defined_now": False,
}

CLOSURE_CAN_SAY: Tuple[str, ...] = (
    "TTS module can reference Registry",
    "TTS module can bind Module-local Profile Standard",
    "TTS module can bind Midplatform Governance Standard",
    "TTS module can preserve candidate-only TTS outputs",
    "TTS module can attach Health/Oversight refs later",
    "TTS module can declare Speech Gate / Voice Output Plane boundaries",
)

CLOSURE_CANNOT_SAY: Tuple[str, ...] = (
    "TTS runtime is ready",
    "Qianwen/MOSS/local TTS selected or invoked",
    "audio generation is available",
    "Voice Output Plane is active",
    "TTS quality is benchmarked",
    "TTS is fully integrated with Constitution",
    "TTS is fully integrated with Health/Oversight",
    "health/supervision metrics finalized",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "tts_module_model_profile_governance_binding_planning_only",
    "qualification_check_only",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "tts_module_runtime_enabled_now",
    "tts_provider_invoked_now",
    "audio_generated_now",
    "voice_output_plane_invoked_now",
    "speech_request_generated_now",
    "model_selected_now",
    "model_downloaded_now",
    "model_invoked_now",
    "provider_invoked_now",
    "benchmark_executed_now",
    "license_cleared_now",
    "security_review_completed_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "user_output_generated_now",
    "controlled_runtime_enabled_now",
    "constitution_effectiveness_quantified_now",
    "health_metrics_finalized_now",
    "supervision_metrics_finalized_now",
    "module_constitution_fully_integrated_now",
    "module_oversight_fully_integrated_now",
    "health_metric_detail_defined_now",
    "supervision_metric_detail_defined_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "tts_module_model_profile_governance_binding_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
        "system_level_simulated_go": True,
        "candidate_only": True,
        "runtime_enabled_now": False,
        "provider_invoked_now": False,
        "audio_generated_now": False,
        "voice_output_plane_invoked_now": False,
        "qualification_mode": QUALIFICATION_MODE,
        **QUALIFICATION_FIELDS,
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


def _tts_registry_ids_from_seeds(tts_seeds: Dict[str, Any]) -> List[str]:
    return [c.get("model_profile_id") for c in (tts_seeds.get("candidates") or []) if c.get("model_profile_id")]


def run_tts_module_model_profile_governance_binding_planning_v1(
    *,
    ocr_module_model_profile_governance_binding_dryrun_and_review_root: str,
    vision_module_model_profile_governance_binding_dryrun_and_review_root: str,
    midplatform_model_governance_binding_standardization_dryrun_and_review_root: str,
    module_local_model_profile_standardization_dryrun_and_review_root: str,
    model_profile_registry_dryrun_and_review_root: str,
    midplatform_speech_gate_dryrun_and_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_controlled_runtime_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    ocr_dr_root = Path(
        ocr_module_model_profile_governance_binding_dryrun_and_review_root
    ).expanduser().resolve()
    vision_dr_root = Path(
        vision_module_model_profile_governance_binding_dryrun_and_review_root
    ).expanduser().resolve()
    binding_dr_root = Path(
        midplatform_model_governance_binding_standardization_dryrun_and_review_root
    ).expanduser().resolve()
    ml_dr_root = Path(
        module_local_model_profile_standardization_dryrun_and_review_root
    ).expanduser().resolve()
    registry_dr_root = Path(model_profile_registry_dryrun_and_review_root).expanduser().resolve()
    registry_plan_root = registry_dr_root.parent / "model_profile_registry_planning"
    speech_gate_root = Path(midplatform_speech_gate_dryrun_and_review_root).expanduser().resolve()
    cb_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    provider_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    cr_root = Path(midplatform_controlled_runtime_dryrun_and_review_root).expanduser().resolve()

    ocr_dr_vr = _try_read_json(ocr_dr_root / "verifier_report.json") or {}
    ocr_dr_sm = _try_read_json(ocr_dr_root / "summary.json") or {}
    vision_dr_vr = _try_read_json(vision_dr_root / "verifier_report.json") or {}
    vision_dr_sm = _try_read_json(vision_dr_root / "summary.json") or {}
    binding_dr_vr = _try_read_json(binding_dr_root / "verifier_report.json") or {}
    ml_dr_vr = _try_read_json(ml_dr_root / "verifier_report.json") or {}
    registry_dr_vr = _try_read_json(registry_dr_root / "verifier_report.json") or {}
    registry_dr_sm = _try_read_json(registry_dr_root / "summary.json") or {}
    speech_gate_vr = _try_read_json(speech_gate_root / "verifier_report.json") or {}
    speech_gate_sm = _try_read_json(speech_gate_root / "summary.json") or {}
    cb_vr = _try_read_json(cb_root / "verifier_report.json") or {}
    provider_vr = _try_read_json(provider_root / "verifier_report.json") or {}
    cr_vr = _try_read_json(cr_root / "verifier_report.json") or {}

    tts_seeds = _try_read_json(registry_plan_root / "tts_model_profile_seed_candidates_v1.json") or {}
    tts_seeds_review = _try_read_json(registry_dr_root / "tts_model_profile_seed_candidates_review_v1.json") or {}
    tts_registry_ids = _tts_registry_ids_from_seeds(tts_seeds)

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_planning_meta(), "output_root": str(out_root)}

    if ocr_dr_vr.get("verifier") != "GO":
        blockers.append("OCR Module DryRunAndReview must be GO")
    if ocr_dr_sm.get("final_decision") != OCR_DR_FINAL_GO:
        blockers.append("OCR DryRun final_decision mismatch")
    if vision_dr_vr.get("verifier") != "GO":
        blockers.append("Vision Module DryRunAndReview must be GO")
    if vision_dr_sm.get("final_decision") != VISION_DR_FINAL_GO:
        blockers.append("Vision DryRun final_decision mismatch")
    if binding_dr_vr.get("verifier") != "GO":
        blockers.append("Midplatform Binding DryRunAndReview must be GO")
    if ml_dr_vr.get("verifier") != "GO":
        blockers.append("Module-Local DryRunAndReview must be GO")
    if registry_dr_vr.get("verifier") != "GO":
        blockers.append("Model Profile Registry DryRunAndReview must be GO")
    if registry_dr_sm.get("final_decision") != REGISTRY_DR_FINAL_GO:
        blockers.append("Registry DryRun final_decision mismatch")
    if speech_gate_vr.get("verifier") != "GO":
        blockers.append("Speech Gate DryRunAndReview must be GO")
    if speech_gate_sm.get("final_decision") != SPEECH_GATE_DR_FINAL_GO:
        blockers.append("Speech Gate DryRun final_decision mismatch")
    if cb_vr.get("verifier") != "GO":
        blockers.append("Constitution-Bus v1.0 must be GO")
    if provider_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction Standard must be GO")
    if cr_vr.get("verifier") != "GO":
        blockers.append("Controlled Runtime Framework must be GO")

    if "qianwen_tts_candidate" not in SEED_CANDIDATE_IDS:
        blockers.append("qianwen_tts_candidate must exist in registry seed list")
    if "moss_tts_style_candidate" not in SEED_CANDIDATE_IDS:
        blockers.append("moss_tts_style_candidate must exist in registry seed list")
    if TTS_REGISTRY_PLACEHOLDER_REGISTRY_ID not in tts_registry_ids:
        if not tts_seeds_review.get("review_pass"):
            blockers.append("local TTS placeholder must be explicitly registered in registry TTS seeds")
        else:
            placeholder_ok = any(
                c.get("check_id") == "local" and c.get("pass")
                for c in (tts_seeds_review.get("checks") or [])
            )
            if not placeholder_ok:
                blockers.append("local TTS placeholder review must pass")

    input_ok = len(blockers) == 0

    upstream_review = {
        "review_id": "upstream_ocr_module_input_review_v1",
        "ocr_dryrun_verifier": ocr_dr_vr.get("verifier"),
        "ocr_dryrun_final_decision": ocr_dr_sm.get("final_decision"),
        "vision_dryrun_verifier": vision_dr_vr.get("verifier"),
        "vision_dryrun_final_decision": vision_dr_sm.get("final_decision"),
        "binding_dryrun_verifier": binding_dr_vr.get("verifier"),
        "module_local_dryrun_verifier": ml_dr_vr.get("verifier"),
        "registry_dryrun_verifier": registry_dr_vr.get("verifier"),
        "speech_gate_dryrun_verifier": speech_gate_vr.get("verifier"),
        "speech_gate_dryrun_final_decision": speech_gate_sm.get("final_decision"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    governance_reuse = {
        "review_id": "governance_standard_reuse_review_v1",
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "reuse_rule_text": PHASE_GOVERNANCE_STANDARD_REUSE_RULE,
        "reused_standards": list(REUSED_GOVERNANCE_STANDARDS),
        "new_governance_need_proven": False,
        "no_parallel_duplicate_governance_standard": True,
        "tts_module_qualification_planning_not_new_framework": True,
        **meta,
    }

    module_definition = {
        "definition_id": "tts_module_definition_v1",
        "module_id": MODULE_ID,
        "module_type": "pluggable_capability_module",
        "capability_domain": "TTS / Voice Output / Speech Synthesis",
        "primary_goal": "speech_synthesis_candidate_generation_later",
        "related_goal": "user_output_execution_layer_later",
        "registry_ref": REGISTRY_REF,
        "runtime_enabled_now": False,
        "provider_invoked_now": False,
        "audio_generated_now": False,
        "voice_output_plane_invoked_now": False,
        "candidate_only": True,
        "confirmations": [
            "TTS module does not decide whether to output to user",
            "TTS module does not bypass Speech Gate",
            "TTS module does not directly play audio",
            "TTS module does not generate final user output",
            "TTS module does not write Memory/WorldModel",
        ],
        **meta,
    }

    capability_stack = {
        "definition_id": CAPABILITY_STACK_DEF_ID,
        "module_id": MODULE_ID,
        "universal_stack_ref": UNIVERSAL_STACK_STANDARD_ID,
        "layers": {
            "layer_1_output_content_acceptance": {
                "outputs": [
                    "user_output_candidate_ref_later",
                    "speech_text_candidate_later",
                    "pronunciation_hint_candidate_later",
                ],
                "status": "later",
            },
            "layer_2_speech_synthesis_candidate": {
                "outputs": [
                    "tts_request_candidate_later",
                    "voice_style_candidate_later",
                    "audio_artifact_candidate_later",
                ],
                "status": "later",
            },
            "layer_3_voice_output_application": {
                "outputs": [
                    "voice_output_plane_request_later",
                    "playback_candidate_later",
                    "interruption_support_later",
                ],
                "status": "later",
            },
            "layer_4_personalization_later": {
                "outputs": [
                    "voice_persona_candidate_later",
                    "emotional_tone_candidate_later",
                    "user_preference_voice_candidate_later",
                ],
                "status": "later",
            },
        },
        "forbidden": [
            "no direct user output decision",
            "no Speech Gate bypass",
            "no direct audio playback",
            "no final user output",
            "no Memory/WorldModel write",
        ],
        **meta,
    }

    layered_governance = {
        "mapping_id": LAYERED_GOV_MAPPING_ID,
        "module_id": MODULE_ID,
        "universal_mapping_ref": ADDENDUM_ID,
        "layers": {
            "L1": {
                "requirements": [
                    "output_candidate_ref", "source_chain", "speech_gate_required",
                    "candidate_only",
                ],
            },
            "L2": {
                "requirements": [
                    "synthesis_quality_later", "pronunciation_uncertainty_later",
                    "voice_style_control_later", "evidence trace",
                ],
            },
            "L3": {
                "requirements": [
                    "Voice Output Plane required", "interruption/abort support later",
                    "playback authorization later",
                ],
            },
            "L4": {
                "requirements": [
                    "emotional tone / personalization later",
                    "privacy / preference / identity checks later",
                ],
            },
        },
        "confirmations": [
            "governance principles consistent",
            "execution intensity layered",
            "no audio output without Speech Gate + Voice Output Plane",
            "no weakened constitution by layer",
        ],
        **meta,
    }

    module_local_profile = {
        "module_local_profile_id": MODULE_LOCAL_PROFILE_ID,
        "module_id": MODULE_ID,
        "module_type": "pluggable_capability_module",
        "capability_domain": "TTS / Voice Output / Speech Synthesis",
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_refs": list(TTS_REGISTRY_REFS),
        "registry_placeholder_alias": {
            "local_tts_placeholder_candidate": TTS_REGISTRY_PLACEHOLDER_REGISTRY_ID,
        },
        "capability_stack_ref": CAPABILITY_STACK_DEF_ID,
        "layered_governance_mapping_ref": LAYERED_GOV_MAPPING_ID,
        "model_role_in_module": [
            "speech_synthesis_candidate_later",
            "voice_style_candidate_later",
            "pronunciation_handling_candidate_later",
            "edge_tts_candidate_later",
        ],
        "model_source_strategy": "A_direct_open_source_or_external_provider",
        "candidate_output_type": "tts_candidate/audio_artifact_candidate_later",
        "midplatform_governance_binding_ref": MIDPLATFORM_BINDING_ID,
        "validation_requirement_ref": "required_later",
        "health_requirement_ref": "required_later",
        "supervision_metric_ref": "required_later",
        "whitebox_trace_requirement_ref": "tts_whitebox_trace_requirement_v1",
        "quality_acceptance_ref": "tts_quality_acceptance_plan_v1",
        "no_registry_override": True,
        "no_model_selection_by_module": True,
        "no_model_invocation_by_profile": True,
        "no_direct_user_output": True,
        "model_selected_now": False,
        "model_invoked_now": False,
        **meta,
    }

    registry_refs_review = {
        "review_id": "tts_model_profile_registry_refs_review_v1",
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_refs": list(TTS_REGISTRY_REFS),
        "registry_placeholder_registry_id": TTS_REGISTRY_PLACEHOLDER_REGISTRY_ID,
        "seed_candidates_in_registry": [
            {"ref": "qianwen_tts_candidate", "in_seed_list": "qianwen_tts_candidate" in SEED_CANDIDATE_IDS,
             "candidate_only": True, "selected_now": False, "invoked_now": False},
            {"ref": "moss_tts_style_candidate", "in_seed_list": "moss_tts_style_candidate" in SEED_CANDIDATE_IDS,
             "candidate_only": True, "selected_now": False, "invoked_now": False},
            {"ref": "local_tts_placeholder_candidate", "registry_id": TTS_REGISTRY_PLACEHOLDER_REGISTRY_ID,
             "explicitly_registered": TTS_REGISTRY_PLACEHOLDER_REGISTRY_ID in tts_registry_ids,
             "candidate_only": True, "selected_now": False, "invoked_now": False},
        ],
        "confirmations": [
            "qianwen_tts_candidate exists or is referenced from Registry seed/profile candidates",
            "moss_tts_style_candidate exists or is referenced from Registry seed/profile candidates",
            "local_tts_placeholder_candidate exists or placeholder ref explicitly registered",
            "all refs are candidate only",
            "none selected_now",
            "none invoked_now",
            "license/version/profile completeness later",
            "TTS provider readiness later required",
        ],
        "review_pass": (
            "qianwen_tts_candidate" in SEED_CANDIDATE_IDS
            and "moss_tts_style_candidate" in SEED_CANDIDATE_IDS
            and (
                TTS_REGISTRY_PLACEHOLDER_REGISTRY_ID in tts_registry_ids
                or tts_seeds_review.get("review_pass") is True
            )
        ),
        **meta,
    }

    role_assignment = {
        "plan_id": "tts_model_role_assignment_plan_v1",
        "assignments": [
            {"registry_ref": "qianwen_tts_candidate", "role": "speech synthesis candidate role",
             "status": "primary_candidate_later"},
            {"registry_ref": "moss_tts_style_candidate",
             "role": "reference/voice style/long-text TTS candidate role", "status": "deferred_later"},
            {"registry_ref": "local_tts_placeholder_candidate", "role": "offline/edge TTS future role",
             "status": "placeholder_later"},
        ],
        "confirmations": [
            "Qianwen TTS maps to speech synthesis candidate role",
            "MOSS TTS style maps to reference/voice style/long-text TTS candidate role",
            "local TTS placeholder maps to offline/edge TTS future role",
            "no single TTS model owns Voice Output Plane",
            "TTS synthesis ≠ permission to speak",
            "TTS candidate ≠ audio playback",
        ],
        **meta,
    }

    input_contract = {
        "contract_id": "tts_input_contract_v1",
        "module_id": MODULE_ID,
        "allowed_inputs": [
            "speech_gate_result_candidate_later",
            "user_output_candidate_later",
            "speech_text_candidate_later",
            "pronunciation_hint_candidate_later",
            "tone_constraint_candidate_later",
            "voice_style_candidate_later",
            "provider_context_candidate_later",
        ],
        "confirmations": [
            "raw user text cannot directly trigger TTS",
            "Speech Gate result required later",
            "Voice Output Plane required for playback",
            "no TTS request generated now",
        ],
        **meta,
    }

    output_contract = {
        "contract_id": "tts_output_contract_v1",
        "module_id": MODULE_ID,
        "allowed_outputs": [
            "tts_request_candidate_later",
            "audio_artifact_candidate_later",
            "speech_synthesis_candidate_later",
            "pronunciation_uncertainty_candidate_later",
            "voice_style_candidate_later",
            "playback_candidate_later",
        ],
        "forbidden_outputs": list(IO_FORBIDDEN),
        **meta,
    }

    quality_plan = {
        "plan_id": "tts_quality_acceptance_plan_v1",
        "requirements": [
            "speech_naturalness_target_later",
            "pronunciation_accuracy_target_later",
            "latency_budget_later",
            "resource_budget_later",
            "interruption_latency_target_later",
            "audio_artifact_integrity_required_later",
        ],
        "candidate_contract_compliance_required": True,
        "traceability_completeness_required": True,
        "degradation_behavior_required": True,
        "benchmark_required_later": True,
        "benchmark_executed_now": False,
        **meta,
    }

    health_validation_whitebox = {
        "plan_id": "tts_health_validation_whitebox_plan_v1",
        "validation_requirement_ref": "required_later",
        "health_requirement_ref": "required_later",
        "supervision_metric_ref": "required_later",
        "whitebox_trace_requirement_ref": "tts_whitebox_trace_requirement_v1",
        "source_chain_required": True,
        "issue_trace_required": True,
        "health_status_ref_transport_only": True,
        "module_cannot_self_certify_health": True,
        "scope_note": "ref slots only; metric detail deferred",
        **meta,
    }

    provider_runtime_boundary = {
        "plan_id": "tts_provider_runtime_boundary_plan_v1",
        "provider_abstraction_required": True,
        "controlled_runtime_required": True,
        "confirmations": [
            "provider_candidate ≠ selected ≠ invoked",
            "no provider auto-switch",
            "audio generation requires Controlled Runtime later",
            "Voice Output Plane required for playback later",
            "TTS runtime remains disabled now",
        ],
        **meta,
    }

    fallback_plan = {
        "plan_id": "tts_fallback_replacement_plan_v1",
        "fallback_model_profile_refs": list(TTS_REGISTRY_REFS),
        "replacement_conditions": [
            "quality_regression", "provider_unavailable", "license_risk", "latency_budget_failure",
            "hardware_incompatibility", "pronunciation_failure", "interruption_latency_failure",
        ],
        "hold_instead_of_fallback_when": "safety/privacy/licensing risk exists",
        "no_auto_switch_without_governance_policy": True,
        "replacement_does_not_imply_invocation": True,
        **meta,
    }

    self_check_plan = {
        "plan_id": "tts_module_internal_self_check_plan_v1",
        "mechanism_layer": "Module Internal Self-Check",
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "purpose": "TTS 模块内部是否按标准写好 profile / contract / binding refs",
        "self_check_coverage": list(MODULE_INTERNAL_SELF_CHECK_COVERAGE),
        "rules": [
            "自检不授权 TTS runtime",
            "自检不选择 Qianwen/MOSS/local TTS",
            "自检不调用 TTS provider",
            "自检不生成音频",
            "自检不写 Memory / WorldModel",
            "自检不生成 user output / speech request",
        ],
        "does_not_replace": "Midplatform Interaction Check",
        **meta,
    }

    interaction_check_plan = {
        "plan_id": "tts_midplatform_interaction_check_plan_v1",
        "mechanism_layer": "Midplatform Interaction Check",
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "purpose": "TTS 模块与中台交互是否合规、无绕路",
        "interaction_check_coverage": list(TTS_MIDPLATFORM_INTERACTION_CHECK_COVERAGE),
        "rules": [
            "中台检验不等于 TTS runtime 授权",
            "中台检验不等于模型选择",
            "中台检验不等于 TTS provider invocation",
            "中台检验不等于音频生成",
            "中台检验不等于 Voice Output Plane 激活",
        ],
        "does_not_replace": "Module Internal Self-Check",
        **meta,
    }

    midplatform_binding = {
        "midplatform_governance_binding_id": MIDPLATFORM_BINDING_ID,
        "module_local_profile_ref": MODULE_LOCAL_PROFILE_ID,
        "module_id": MODULE_ID,
        "registry_model_profile_refs": list(TTS_REGISTRY_REFS),
        "registry_ref": REGISTRY_REF,
        "midplatform_binding_standard_ref": MIDPLATFORM_BINDING_STANDARD_ID,
        "constitution_bus_ref": CONSTITUTION_BUS_REF,
        "capability_bus_contract_ref": CAPABILITY_BUS_CONTRACT_REF,
        "provider_abstraction_ref": PROVIDER_ABS_STANDARD_ID,
        "validation_requirement_ref": "required_later",
        "health_requirement_ref": "required_later",
        "supervision_metric_ref": "required_later",
        "whitebox_trace_requirement_ref": "tts_whitebox_trace_requirement_v1",
        "speech_gate_requirement_ref": SPEECH_GATE_REF,
        "voice_output_plane_requirement_ref_later": VOICE_OUTPUT_PLANE_REF,
        "controlled_runtime_requirement_ref": CONTROLLED_RUNTIME_FRAMEWORK_REF,
        "source_chain_requirement_ref": "tts_source_chain_requirement_v1",
        "issue_trace_requirement_ref": "tts_issue_trace_requirement_v1",
        "non_compliance_handling_policy_ref_later": DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID,
        "model_selected_now": False,
        "model_invoked_now": False,
        "runtime_enabled_now": False,
        **meta,
    }

    speech_gate_handoff = {
        "plan_id": "tts_speech_gate_handoff_plan_v1",
        "speech_gate_ref": SPEECH_GATE_REF,
        "speech_gate_layer_positioning": list(SPEECH_GATE_LAYER_POSITIONING),
        "confirmations": [
            "TTS can only consume Speech Gate-approved candidate later",
            "Speech Gate pass ≠ TTS execution",
            "TTS does not run before Speech Gate",
            "TTS does not modify safety/refusal decision",
            "no speech_gate_result consumed now",
        ],
        **meta,
    }

    voice_output_plane_boundary = {
        "plan_id": "tts_voice_output_plane_boundary_plan_v1",
        "voice_output_plane_ref": VOICE_OUTPUT_PLANE_REF,
        "confirmations": [
            "TTS synthesis candidate ≠ playback",
            "Voice Output Plane required later for audio emission",
            "interruption / abort support later",
            "playback authorization later",
            "no Voice Output Plane invoked now",
            "no audio played now",
        ],
        **meta,
    }

    memory_wm_boundary = {
        "plan_id": "tts_memory_worldmodel_admission_boundary_plan_v1",
        "confirmations": [
            "TTS module cannot write Memory",
            "TTS module cannot write WorldModel",
            "voice preference personalization later may require Memory Admission",
            "emotional tone later requires Emotion/Privacy governance",
            "no memory/worldmodel write now",
        ],
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "tts_non_runtime_boundary_matrix_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        **meta,
    }

    qualification_check = {
        "check_id": "tts_module_qualification_check_v1",
        "qualification_mode": QUALIFICATION_MODE,
        "criteria": list(QUALIFICATION_CHECK_CRITERIA),
        "criteria_count": len(QUALIFICATION_CHECK_CRITERIA),
        "qualification_fields": dict(QUALIFICATION_FIELDS),
        "can_say": list(CLOSURE_CAN_SAY),
        "cannot_say": list(CLOSURE_CANNOT_SAY),
        "qualification_pass": input_ok and registry_refs_review.get("review_pass"),
        **meta,
    }

    dryrun_plan = {
        "plan_id": "tts_module_model_profile_governance_binding_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "qualification_mode": QUALIFICATION_MODE,
        "objectives": [
            "qualification check only: verify TTS module sample is compliant",
            "generate tts_module_model_profile_governance_binding_candidate",
            "verify TTS module definition / capability stack / layered governance mapping",
            "verify module-local model profile registry refs",
            "verify Qianwen / MOSS / local TTS role assignment",
            "verify input/output contracts",
            "verify quality / health / validation / whitebox / provider-runtime / fallback",
            "verify Speech Gate / Voice Output Plane boundary",
            "execute TTS module internal self-check + midplatform interaction check",
            "no health/supervision metric detail expansion",
            "no model select/download/invoke/benchmark",
            "no audio generation / TTS runtime enable",
        ],
        **meta,
    }

    planning_pass = qualification_check.get("qualification_pass")
    planning_decision = {
        "decision_id": "tts_module_model_profile_governance_binding_planning_decision_v1",
        "planning_pass": planning_pass,
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_check_only": True,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "closure_can_say": list(CLOSURE_CAN_SAY),
        "closure_cannot_say": list(CLOSURE_CANNOT_SAY),
        **meta,
    }

    policy = {
        "policy_id": "tts_module_model_profile_governance_binding_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "tts_module_model_profile_governance_binding_planning_only": True,
        "qualification_check_only": True,
        "phase_goal": (
            "TTS module model profile + governance binding qualification planning confirmation only. "
            "No health/supervision metric expansion. No Qianwen/MOSS/local TTS selection, "
            "no audio generation, no Voice Output Plane runtime."
        ),
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        "dual_validation_non_claims": list(DUAL_VALIDATION_NON_CLAIMS),
        "non_compliant_module_model_handling_policy_deferred": True,
        "recommended_future_phase": DEFERRED_NON_COMPLIANCE_HANDLING_PHASE,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_pass": planning_pass,
        "module_id": MODULE_ID,
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_ref_count": len(TTS_REGISTRY_REFS),
        "midplatform_binding_standard_ref": MIDPLATFORM_BINDING_STANDARD_ID,
        "module_local_profile_standard_ref": MODULE_LOCAL_PROFILE_STANDARD_REF,
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_check_only": True,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "tts_module_model_profile_governance_binding_planning_policy": policy,
        "upstream_ocr_module_input_review": upstream_review,
        "governance_standard_reuse_review": governance_reuse,
        "tts_module_definition": module_definition,
        "tts_capability_stack_definition": capability_stack,
        "tts_layered_governance_mapping": layered_governance,
        "tts_module_local_model_profile": module_local_profile,
        "tts_model_profile_registry_refs_review": registry_refs_review,
        "tts_model_role_assignment_plan": role_assignment,
        "tts_input_contract": input_contract,
        "tts_output_contract": output_contract,
        "tts_quality_acceptance_plan": quality_plan,
        "tts_health_validation_whitebox_plan": health_validation_whitebox,
        "tts_provider_runtime_boundary_plan": provider_runtime_boundary,
        "tts_fallback_replacement_plan": fallback_plan,
        "tts_module_internal_self_check_plan": self_check_plan,
        "tts_midplatform_interaction_check_plan": interaction_check_plan,
        "tts_midplatform_governance_binding": midplatform_binding,
        "tts_speech_gate_handoff_plan": speech_gate_handoff,
        "tts_voice_output_plane_boundary_plan": voice_output_plane_boundary,
        "tts_memory_worldmodel_admission_boundary_plan": memory_wm_boundary,
        "tts_module_qualification_check": qualification_check,
        "tts_non_runtime_boundary_matrix": boundary_matrix,
        "tts_module_model_profile_governance_binding_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "tts_module_model_profile_governance_binding_planning_decision": planning_decision,
        "summary": summary,
    }
