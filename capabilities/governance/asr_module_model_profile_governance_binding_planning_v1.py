# -*- coding: utf-8 -*-
"""ASR Module Model Profile + Governance Binding Planning v1 — qualification only."""

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
    DECISION_CENTER_REF,
    INFORMATION_INTEGRATION_REF,
    MODULE_LOCAL_PROFILE_STANDARD_REF,
    PROVIDER_ABS_STANDARD_ID,
    REGISTRY_REF,
    STANDARD_ID as MIDPLATFORM_BINDING_STANDARD_ID,
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
from capabilities.governance.tts_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as TTS_DR_FINAL_GO,
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

PHASE_ID = "Phase-ASR-Module-Model-Profile-Governance-Binding-Planning-v1-001"
SCOPE = "asr_module_model_profile_governance_binding_planning_only"
SOURCE_CHAIN = "asr_module_model_profile_governance_binding_planning_v1"

FINAL_DECISION_GO = (
    "ASR_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "ASR_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-ASR-Module-Model-Profile-Governance-Binding-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-ASR-Module-Model-Profile-Governance-Binding-Issue-Review-v1-001"

MODULE_ID = "asr_voice_input_module"
MODULE_LOCAL_PROFILE_ID = "asr_voice_input_module_local_profile_v1"
MIDPLATFORM_BINDING_ID = "asr_voice_input_midplatform_binding_v1"
CAPABILITY_STACK_DEF_ID = "asr_capability_stack_definition_v1"
LAYERED_GOV_MAPPING_ID = "asr_layered_governance_mapping_v1"
CAPABILITY_BUS_CONTRACT_REF = "asr_voice_input_capability_bus_contract_v1"

ASR_REGISTRY_REFS: Tuple[str, ...] = (
    "sensevoice_asr_candidate",
    "whisper_like_asr_candidate",
    "qwen_asr_style_candidate",
)

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
    "Information Integration / Decision Center handoff",
    "Privacy / Identity boundary",
    "Health Oversight Externality",
    "Whitebox Trace Standard",
    "Boundary Matrix / Blocked Path / Non-Claims pattern",
)

ASR_MIDPLATFORM_INTERACTION_CHECK_COVERAGE: Tuple[str, ...] = (
    "Constitution-Bus binding",
    "Capability Bus contract",
    "Provider Abstraction binding",
    "Information Integration handoff",
    "Decision Center handoff",
    "Validation requirement",
    "Health requirement / external oversight",
    "Whitebox trace",
    "Controlled Runtime requirement",
    "Privacy / Identity boundary",
    "Memory / WorldModel non-write boundary",
    "source_chain / evidence / traceability preservation",
)

IO_FORBIDDEN: Tuple[str, ...] = (
    "direct_action",
    "direct_task_state_commit",
    "direct_navigation_action",
    "direct_user_output",
    "direct_memory_write",
    "direct_worldmodel_write",
    "direct_runtime_enable",
    "direct_identity_fact",
)

NON_CLAIMS: Tuple[str, ...] = (
    "ASR Module Planning GO ≠ SenseVoice/Whisper/Qwen-ASR selected",
    "ASR candidate ref ≠ ASR runtime",
    "ASR output contract planned ≠ transcript generation",
    "ASR binding feasible ≠ Constitution/Oversight fully integrated",
    "Health/Oversight refs attached ≠ health/supervision metrics finalized",
    "privacy/identity boundary declared ≠ speaker identity enabled",
    "next DryRunAndReview ≠ model benchmark/runtime/audio capture",
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
    "ASR module can reference Registry",
    "ASR module can bind Module-local Profile Standard",
    "ASR module can bind Midplatform Governance Standard",
    "ASR module can preserve candidate-only transcript outputs",
    "ASR module can attach Health/Oversight refs later",
    "ASR module can declare microphone / privacy / identity boundaries",
)

CLOSURE_CANNOT_SAY: Tuple[str, ...] = (
    "ASR runtime is ready",
    "SenseVoice/Whisper/Qwen-ASR selected or invoked",
    "microphone capture is available",
    "transcript generation is available",
    "ASR quality is benchmarked",
    "ASR is fully integrated with Constitution",
    "ASR is fully integrated with Health/Oversight",
    "health/supervision metrics finalized",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "asr_module_model_profile_governance_binding_planning_only",
    "qualification_check_only",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "asr_module_runtime_enabled_now",
    "microphone_invoked_now",
    "audio_capture_executed_now",
    "asr_provider_invoked_now",
    "transcript_generated_now",
    "model_selected_now",
    "model_downloaded_now",
    "model_invoked_now",
    "provider_invoked_now",
    "benchmark_executed_now",
    "license_cleared_now",
    "security_review_completed_now",
    "voice_intent_generated_now",
    "speaker_identity_generated_now",
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
    "asr_module_model_profile_governance_binding_planning"
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
        "microphone_invoked_now": False,
        "transcript_generated_now": False,
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


def run_asr_module_model_profile_governance_binding_planning_v1(
    *,
    tts_module_model_profile_governance_binding_dryrun_and_review_root: str,
    ocr_module_model_profile_governance_binding_dryrun_and_review_root: str,
    vision_module_model_profile_governance_binding_dryrun_and_review_root: str,
    midplatform_model_governance_binding_standardization_dryrun_and_review_root: str,
    module_local_model_profile_standardization_dryrun_and_review_root: str,
    model_profile_registry_dryrun_and_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_controlled_runtime_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    tts_dr_root = Path(
        tts_module_model_profile_governance_binding_dryrun_and_review_root
    ).expanduser().resolve()
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
    cb_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    provider_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    cr_root = Path(midplatform_controlled_runtime_dryrun_and_review_root).expanduser().resolve()

    tts_dr_vr = _try_read_json(tts_dr_root / "verifier_report.json") or {}
    tts_dr_sm = _try_read_json(tts_dr_root / "summary.json") or {}
    ocr_dr_vr = _try_read_json(ocr_dr_root / "verifier_report.json") or {}
    ocr_dr_sm = _try_read_json(ocr_dr_root / "summary.json") or {}
    vision_dr_vr = _try_read_json(vision_dr_root / "verifier_report.json") or {}
    vision_dr_sm = _try_read_json(vision_dr_root / "summary.json") or {}
    binding_dr_vr = _try_read_json(binding_dr_root / "verifier_report.json") or {}
    ml_dr_vr = _try_read_json(ml_dr_root / "verifier_report.json") or {}
    registry_dr_vr = _try_read_json(registry_dr_root / "verifier_report.json") or {}
    registry_dr_sm = _try_read_json(registry_dr_root / "summary.json") or {}
    cb_vr = _try_read_json(cb_root / "verifier_report.json") or {}
    provider_vr = _try_read_json(provider_root / "verifier_report.json") or {}
    cr_vr = _try_read_json(cr_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_planning_meta(), "output_root": str(out_root)}

    if tts_dr_vr.get("verifier") != "GO":
        blockers.append("TTS Module DryRunAndReview must be GO")
    if tts_dr_sm.get("final_decision") != TTS_DR_FINAL_GO:
        blockers.append("TTS DryRun final_decision mismatch")
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
    if cb_vr.get("verifier") != "GO":
        blockers.append("Constitution-Bus v1.0 must be GO")
    if provider_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction Standard must be GO")
    if cr_vr.get("verifier") != "GO":
        blockers.append("Controlled Runtime Framework must be GO")

    for ref in ASR_REGISTRY_REFS:
        if ref not in SEED_CANDIDATE_IDS:
            blockers.append(f"{ref} must exist in registry seed list")

    input_ok = len(blockers) == 0

    upstream_review = {
        "review_id": "upstream_tts_module_input_review_v1",
        "tts_dryrun_verifier": tts_dr_vr.get("verifier"),
        "tts_dryrun_final_decision": tts_dr_sm.get("final_decision"),
        "ocr_dryrun_verifier": ocr_dr_vr.get("verifier"),
        "ocr_dryrun_final_decision": ocr_dr_sm.get("final_decision"),
        "vision_dryrun_verifier": vision_dr_vr.get("verifier"),
        "vision_dryrun_final_decision": vision_dr_sm.get("final_decision"),
        "binding_dryrun_verifier": binding_dr_vr.get("verifier"),
        "module_local_dryrun_verifier": ml_dr_vr.get("verifier"),
        "registry_dryrun_verifier": registry_dr_vr.get("verifier"),
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
        "asr_module_qualification_planning_not_new_framework": True,
        **meta,
    }

    module_definition = {
        "definition_id": "asr_module_definition_v1",
        "module_id": MODULE_ID,
        "module_type": "pluggable_capability_module",
        "capability_domain": "ASR / Voice Input / Speech Recognition",
        "primary_goal": "transcript_candidate_generation_later",
        "related_goal": "voice_intent_candidate_generation_later",
        "later_goal": "speaker_context / emotion_hint / dialect adaptation later",
        "registry_ref": REGISTRY_REF,
        "runtime_enabled_now": False,
        "microphone_invoked_now": False,
        "provider_invoked_now": False,
        "transcript_generated_now": False,
        "candidate_only": True,
        "confirmations": [
            "ASR module does not directly generate command action",
            "ASR module does not directly trigger task_state_commit",
            "ASR module does not write Memory/WorldModel",
            "ASR module does not generate user output",
            "transcript is candidate only, not fact",
        ],
        **meta,
    }

    capability_stack = {
        "definition_id": CAPABILITY_STACK_DEF_ID,
        "module_id": MODULE_ID,
        "universal_stack_ref": UNIVERSAL_STACK_STANDARD_ID,
        "layers": {
            "layer_1_audio_intake_candidate": {
                "outputs": [
                    "audio_capture_candidate_later",
                    "speech_presence_candidate_later",
                    "noise_context_candidate_later",
                ],
                "status": "later",
            },
            "layer_2_asr_transcript_candidate": {
                "outputs": [
                    "transcript_candidate_later",
                    "language_hint_candidate_later",
                    "confidence_candidate_later",
                ],
                "status": "later",
            },
            "layer_3_voice_intent_dialogue_context_later": {
                "outputs": [
                    "voice_intent_candidate_later",
                    "interruption_signal_candidate_later",
                    "command_candidate_later",
                ],
                "status": "later",
            },
            "layer_4_speaker_emotion_dialect_later": {
                "outputs": [
                    "speaker_context_candidate_later",
                    "emotion_hint_candidate_later",
                    "dialect_or_phrase_habit_candidate_later",
                ],
                "status": "later",
            },
        },
        "forbidden": [
            "no direct command action",
            "no direct task_state_commit",
            "no user output",
            "no Memory/WorldModel write",
            "transcript is candidate not fact",
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
                    "audio_source_ref_later", "source_chain", "candidate_only",
                    "privacy_sensitive_by_default",
                ],
            },
            "L2": {
                "requirements": [
                    "transcript_confidence", "language_uncertainty", "noise_context",
                    "evidence trace",
                ],
            },
            "L3": {
                "requirements": [
                    "intent ambiguity", "Decision Center handoff",
                    "task_state_commit blocked now", "interruption handling later",
                ],
            },
            "L4": {
                "requirements": [
                    "speaker identity later", "emotion hint later",
                    "dialect/personal language learning later",
                    "Privacy / Identity / Memory Admission required later",
                ],
            },
        },
        "confirmations": [
            "governance principles consistent",
            "execution intensity layered",
            "no raw microphone runtime without Controlled Runtime",
            "no speaker identity without Privacy/Identity gates",
            "no weakened constitution by layer",
        ],
        **meta,
    }

    module_local_profile = {
        "module_local_profile_id": MODULE_LOCAL_PROFILE_ID,
        "module_id": MODULE_ID,
        "module_type": "pluggable_capability_module",
        "capability_domain": "ASR / Voice Input / Speech Recognition",
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_refs": list(ASR_REGISTRY_REFS),
        "capability_stack_ref": CAPABILITY_STACK_DEF_ID,
        "layered_governance_mapping_ref": LAYERED_GOV_MAPPING_ID,
        "model_role_in_module": [
            "speech_recognition_candidate_later",
            "language_detection_candidate_later",
            "voice_activity_candidate_later",
            "speaker_context_candidate_later",
            "emotion_hint_candidate_later",
        ],
        "model_source_strategy": "A_direct_open_source_or_external_provider",
        "candidate_output_type": "asr_candidate/transcript_candidate/voice_context_candidate",
        "midplatform_governance_binding_ref": MIDPLATFORM_BINDING_ID,
        "validation_requirement_ref": "required_later",
        "health_requirement_ref": "required_later",
        "supervision_metric_ref": "required_later",
        "whitebox_trace_requirement_ref": "asr_whitebox_trace_requirement_v1",
        "quality_acceptance_ref": "asr_quality_acceptance_plan_v1",
        "no_registry_override": True,
        "no_model_selection_by_module": True,
        "no_model_invocation_by_profile": True,
        "no_direct_action_output": True,
        "model_selected_now": False,
        "model_invoked_now": False,
        **meta,
    }

    registry_refs_review = {
        "review_id": "asr_model_profile_registry_refs_review_v1",
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_refs": list(ASR_REGISTRY_REFS),
        "seed_candidates_in_registry": [
            {"ref": ref, "in_seed_list": ref in SEED_CANDIDATE_IDS,
             "candidate_only": True, "selected_now": False, "invoked_now": False}
            for ref in ASR_REGISTRY_REFS
        ],
        "confirmations": [
            "sensevoice_asr_candidate exists or is referenced from Registry seed/profile candidates",
            "whisper_like_asr_candidate exists or is referenced from Registry seed/profile candidates",
            "qwen_asr_style_candidate exists or is referenced from Registry seed/profile candidates",
            "all refs are candidate only",
            "none selected_now",
            "none invoked_now",
            "license/version/profile completeness later",
            "ASR provider readiness later required",
        ],
        "review_pass": all(ref in SEED_CANDIDATE_IDS for ref in ASR_REGISTRY_REFS),
        **meta,
    }

    role_assignment = {
        "plan_id": "asr_model_role_assignment_plan_v1",
        "assignments": [
            {"registry_ref": "sensevoice_asr_candidate",
             "role": "ASR transcript / language / emotion-hint candidate role", "status": "deferred_later"},
            {"registry_ref": "whisper_like_asr_candidate", "role": "transcript candidate role",
             "status": "deferred_later"},
            {"registry_ref": "qwen_asr_style_candidate",
             "role": "multilingual / speech recognition candidate role", "status": "planned_later"},
        ],
        "confirmations": [
            "SenseVoice maps to ASR transcript / language / emotion-hint candidate role",
            "Whisper-like ASR maps to transcript candidate role",
            "Qwen-ASR style maps to multilingual / speech recognition candidate role",
            "no single ASR model owns voice interaction",
            "ASR transcript ≠ user intent final decision",
            "ASR candidate ≠ task command",
        ],
        **meta,
    }

    input_contract = {
        "contract_id": "asr_input_contract_v1",
        "module_id": MODULE_ID,
        "allowed_inputs": [
            "audio_capture_candidate_later",
            "microphone_stream_candidate_later",
            "speech_presence_candidate_later",
            "user_interrupt_candidate_later",
            "task_context_candidate_later",
            "provider_context_candidate_later",
        ],
        "confirmations": [
            "microphone input not allowed now",
            "audio capture not executed now",
            "microphone_stream_candidate_later requires Controlled Runtime later",
        ],
        **meta,
    }

    output_contract = {
        "contract_id": "asr_output_contract_v1",
        "module_id": MODULE_ID,
        "allowed_outputs": [
            "transcript_candidate_later",
            "language_hint_candidate_later",
            "confidence_candidate_later",
            "voice_intent_candidate_later",
            "interruption_signal_candidate_later",
            "speaker_context_candidate_later",
            "emotion_hint_candidate_later",
            "dialect_or_phrase_habit_candidate_later",
        ],
        "forbidden_outputs": list(IO_FORBIDDEN),
        "handoff_target": INFORMATION_INTEGRATION_REF,
        **meta,
    }

    quality_plan = {
        "plan_id": "asr_quality_acceptance_plan_v1",
        "requirements": [
            "word_error_rate_target_later",
            "latency_budget_later",
            "noise_robustness_target_later",
            "multilingual_accuracy_target_later",
            "interruption_detection_latency_target_later",
            "confidence_calibration_required",
        ],
        "candidate_contract_compliance_required": True,
        "traceability_completeness_required": True,
        "degradation_behavior_required": True,
        "benchmark_required_later": True,
        "benchmark_executed_now": False,
        **meta,
    }

    health_validation_whitebox = {
        "plan_id": "asr_health_validation_whitebox_plan_v1",
        "validation_requirement_ref": "required_later",
        "health_requirement_ref": "required_later",
        "supervision_metric_ref": "required_later",
        "whitebox_trace_requirement_ref": "asr_whitebox_trace_requirement_v1",
        "source_chain_required": True,
        "issue_trace_required": True,
        "health_status_ref_transport_only": True,
        "module_cannot_self_certify_health": True,
        "scope_note": "ref slots only; metric detail deferred",
        **meta,
    }

    provider_runtime_boundary = {
        "plan_id": "asr_provider_runtime_boundary_plan_v1",
        "provider_abstraction_required": True,
        "controlled_runtime_required": True,
        "confirmations": [
            "provider_candidate ≠ selected ≠ invoked",
            "no provider auto-switch",
            "audio capture requires Controlled Runtime later",
            "microphone runtime requires Controlled Runtime later",
            "ASR runtime remains disabled now",
        ],
        **meta,
    }

    fallback_plan = {
        "plan_id": "asr_fallback_replacement_plan_v1",
        "fallback_model_profile_refs": list(ASR_REGISTRY_REFS),
        "replacement_conditions": [
            "quality_regression", "provider_unavailable", "license_risk", "latency_budget_failure",
            "hardware_incompatibility", "high_noise_failure", "high_false_command_risk",
            "privacy_sensitive_audio_risk",
        ],
        "hold_instead_of_fallback_when": "safety/privacy/licensing risk exists",
        "no_auto_switch_without_governance_policy": True,
        "replacement_does_not_imply_invocation": True,
        **meta,
    }

    self_check_plan = {
        "plan_id": "asr_module_internal_self_check_plan_v1",
        "mechanism_layer": "Module Internal Self-Check",
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "purpose": "ASR 模块内部是否按标准写好 profile / contract / binding refs",
        "self_check_coverage": list(MODULE_INTERNAL_SELF_CHECK_COVERAGE),
        "rules": [
            "自检不授权 ASR runtime",
            "自检不选择 SenseVoice/Whisper/Qwen-ASR",
            "自检不调用 ASR provider",
            "自检不启 microphone / audio capture",
            "自检不生成 transcript",
            "自检不写 Memory / WorldModel",
            "自检不生成 task command / user output",
        ],
        "does_not_replace": "Midplatform Interaction Check",
        **meta,
    }

    interaction_check_plan = {
        "plan_id": "asr_midplatform_interaction_check_plan_v1",
        "mechanism_layer": "Midplatform Interaction Check",
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "purpose": "ASR 模块与中台交互是否合规、无绕路",
        "interaction_check_coverage": list(ASR_MIDPLATFORM_INTERACTION_CHECK_COVERAGE),
        "rules": [
            "中台检验不等于 ASR runtime 授权",
            "中台检验不等于模型选择",
            "中台检验不等于 ASR provider invocation",
            "中台检验不等于 microphone / transcript generation",
        ],
        "does_not_replace": "Module Internal Self-Check",
        **meta,
    }

    midplatform_binding = {
        "midplatform_governance_binding_id": MIDPLATFORM_BINDING_ID,
        "module_local_profile_ref": MODULE_LOCAL_PROFILE_ID,
        "module_id": MODULE_ID,
        "registry_model_profile_refs": list(ASR_REGISTRY_REFS),
        "registry_ref": REGISTRY_REF,
        "midplatform_binding_standard_ref": MIDPLATFORM_BINDING_STANDARD_ID,
        "constitution_bus_ref": CONSTITUTION_BUS_REF,
        "capability_bus_contract_ref": CAPABILITY_BUS_CONTRACT_REF,
        "provider_abstraction_ref": PROVIDER_ABS_STANDARD_ID,
        "validation_requirement_ref": "required_later",
        "health_requirement_ref": "required_later",
        "supervision_metric_ref": "required_later",
        "whitebox_trace_requirement_ref": "asr_whitebox_trace_requirement_v1",
        "information_integration_consumption_policy_ref": "asr_information_integration_handoff_plan_v1",
        "decision_center_consumption_policy_ref": "asr_decision_center_handoff_plan_v1",
        "controlled_runtime_requirement_ref": CONTROLLED_RUNTIME_FRAMEWORK_REF,
        "privacy_identity_requirement_ref_later": "asr_privacy_identity_boundary_plan_v1",
        "memory_admission_requirement_ref_later": "memory_admission_gate_later",
        "worldmodel_admission_requirement_ref_later": "worldmodel_admission_gate_later",
        "source_chain_requirement_ref": "asr_source_chain_requirement_v1",
        "issue_trace_requirement_ref": "asr_issue_trace_requirement_v1",
        "non_compliance_handling_policy_ref_later": DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID,
        "model_selected_now": False,
        "model_invoked_now": False,
        "runtime_enabled_now": False,
        **meta,
    }

    ii_handoff = {
        "plan_id": "asr_information_integration_handoff_plan_v1",
        "information_integration_ref": INFORMATION_INTEGRATION_REF,
        "consumes": [
            "transcript_candidate", "language_hint", "voice_intent",
            "interruption_signal", "emotion_hint",
        ],
        "confirmations": [
            "ASR outputs go to Information Integration as candidate/context/evidence",
            "Information Integration consumes transcript / language_hint / voice_intent / "
            "interruption_signal / emotion_hint later",
            "ASR module cannot bypass Information Integration to Decision Center unless explicit policy later",
            "no integrated_context generated now",
        ],
        **meta,
    }

    decision_handoff = {
        "plan_id": "asr_decision_center_handoff_plan_v1",
        "decision_center_ref": DECISION_CENTER_REF,
        "handoff_via": ["integrated_context", "decision_request"],
        "confirmations": [
            "decision-relevant ASR outputs reach Decision Center only through "
            "integrated_context / decision_request",
            "ASR module cannot emit final task command",
            "transcript cannot directly trigger navigation/action/task commit",
            "no decision generated now",
        ],
        **meta,
    }

    privacy_identity = {
        "plan_id": "asr_privacy_identity_boundary_plan_v1",
        "confirmations": [
            "microphone / voice input is privacy-sensitive by default",
            "speaker identity is later and requires Privacy / Identity gates",
            "emotion hint later requires privacy/emotion governance",
            "dialect/personal phrase learning later requires Memory Admission",
            "no speaker identity fact generated now",
        ],
        **meta,
    }

    memory_wm_boundary = {
        "plan_id": "asr_memory_worldmodel_admission_boundary_plan_v1",
        "confirmations": [
            "ASR module cannot write Memory",
            "ASR module cannot write WorldModel",
            "transcript evidence may be admission candidate later",
            "user phrase/dialect learning later requires Memory Admission",
            "no memory/worldmodel write now",
        ],
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "asr_non_runtime_boundary_matrix_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        **meta,
    }

    qualification_check = {
        "check_id": "asr_module_qualification_check_v1",
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
        "plan_id": "asr_module_model_profile_governance_binding_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "qualification_mode": QUALIFICATION_MODE,
        "objectives": [
            "qualification check only: verify ASR module sample is compliant",
            "generate asr_module_model_profile_governance_binding_candidate",
            "verify ASR module definition / capability stack / layered governance mapping",
            "verify module-local model profile registry refs",
            "verify SenseVoice / Whisper-like / Qwen-ASR role assignment",
            "verify input/output contracts",
            "verify quality / health / validation / whitebox / provider-runtime / fallback",
            "verify privacy-identity boundary",
            "execute ASR module internal self-check + midplatform interaction check",
            "no health/supervision metric detail expansion",
            "no model select/download/invoke/benchmark",
            "no microphone/ASR runtime / transcript generation",
        ],
        **meta,
    }

    planning_pass = qualification_check.get("qualification_pass")
    planning_decision = {
        "decision_id": "asr_module_model_profile_governance_binding_planning_decision_v1",
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
        "policy_id": "asr_module_model_profile_governance_binding_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "asr_module_model_profile_governance_binding_planning_only": True,
        "qualification_check_only": True,
        "phase_goal": (
            "ASR module model profile + governance binding qualification planning confirmation only. "
            "No health/supervision metric expansion. No SenseVoice/Whisper/Qwen-ASR selection, "
            "no microphone, no ASR runtime, no transcript generation."
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
        "registry_model_profile_ref_count": len(ASR_REGISTRY_REFS),
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
        "asr_module_model_profile_governance_binding_planning_policy": policy,
        "upstream_tts_module_input_review": upstream_review,
        "governance_standard_reuse_review": governance_reuse,
        "asr_module_definition": module_definition,
        "asr_capability_stack_definition": capability_stack,
        "asr_layered_governance_mapping": layered_governance,
        "asr_module_local_model_profile": module_local_profile,
        "asr_model_profile_registry_refs_review": registry_refs_review,
        "asr_model_role_assignment_plan": role_assignment,
        "asr_input_contract": input_contract,
        "asr_output_contract": output_contract,
        "asr_quality_acceptance_plan": quality_plan,
        "asr_health_validation_whitebox_plan": health_validation_whitebox,
        "asr_provider_runtime_boundary_plan": provider_runtime_boundary,
        "asr_fallback_replacement_plan": fallback_plan,
        "asr_module_internal_self_check_plan": self_check_plan,
        "asr_midplatform_interaction_check_plan": interaction_check_plan,
        "asr_midplatform_governance_binding": midplatform_binding,
        "asr_information_integration_handoff_plan": ii_handoff,
        "asr_decision_center_handoff_plan": decision_handoff,
        "asr_privacy_identity_boundary_plan": privacy_identity,
        "asr_memory_worldmodel_admission_boundary_plan": memory_wm_boundary,
        "asr_module_qualification_check": qualification_check,
        "asr_non_runtime_boundary_matrix": boundary_matrix,
        "asr_module_model_profile_governance_binding_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "asr_module_model_profile_governance_binding_planning_decision": planning_decision,
        "summary": summary,
    }
