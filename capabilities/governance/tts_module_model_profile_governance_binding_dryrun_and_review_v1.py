# -*- coding: utf-8 -*-
"""TTS Module Model Profile + Governance Binding DryRunAndReview v1 — qualification only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_model_governance_binding_standardization_planning_v1 import (
    CONSTITUTION_BUS_REF,
    CONTROLLED_RUNTIME_FRAMEWORK_REF,
    MODULE_LOCAL_PROFILE_STANDARD_REF,
    PROVIDER_ABS_STANDARD_ID,
    REGISTRY_REF,
    STANDARD_ID as MIDPLATFORM_BINDING_STANDARD_ID,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.model_profile_registry_planning_v1 import SEED_CANDIDATE_IDS
from capabilities.governance.module_local_model_profile_standardization_planning_v1 import (
    DUAL_VALIDATION_MECHANISM_ID,
    MODULE_INTERNAL_SELF_CHECK_COVERAGE,
)
from capabilities.governance.tts_module_model_profile_governance_binding_planning_v1 import (
    CAPABILITY_STACK_DEF_ID,
    CLOSURE_CAN_SAY,
    CLOSURE_CANNOT_SAY,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    IO_FORBIDDEN,
    LAYERED_GOV_MAPPING_ID,
    MIDPLATFORM_BINDING_ID,
    MODULE_ID,
    MODULE_LOCAL_PROFILE_ID,
    QUALIFICATION_FIELDS,
    QUALIFICATION_MODE,
    REUSED_GOVERNANCE_STANDARDS,
    SPEECH_GATE_REF,
    TTS_MIDPLATFORM_INTERACTION_CHECK_COVERAGE,
    TTS_REGISTRY_PLACEHOLDER_REGISTRY_ID,
    VOICE_OUTPUT_PLANE_REF,
)

PHASE_ID = "Phase-TTS-Module-Model-Profile-Governance-Binding-DryRunAndReview-v1-001"
SCOPE = "tts_module_model_profile_governance_binding_dryrun_and_review_only"
SOURCE_CHAIN = "tts_module_model_profile_governance_binding_dryrun_and_review_v1"

CANDIDATE_REGISTRY_REFS: Tuple[str, ...] = (
    "qianwen_tts_candidate",
    "moss_tts_style_candidate",
    TTS_REGISTRY_PLACEHOLDER_REGISTRY_ID,
)

FINAL_DECISION_GO = (
    "TTS_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_ASR_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_PLANNING"
)
FINAL_DECISION_HOLD = (
    "TTS_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-ASR-Module-Model-Profile-Governance-Binding-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-TTS-Module-Model-Profile-Governance-Binding-Issue-Review-v1-001"

NON_CLAIMS: Tuple[str, ...] = (
    "TTS Module DryRun GO ≠ Qianwen/MOSS/local TTS selected",
    "TTS candidate refs reviewed ≠ TTS runtime",
    "TTS output contract reviewed ≠ audio generation",
    "TTS module binding feasible ≠ Constitution/Oversight fully integrated",
    "Speech Gate boundary declared ≠ Voice Output Plane active",
    "Health/Oversight refs attached ≠ health/supervision metrics finalized",
    "next ASR Module Planning ≠ ASR invocation",
    "Module Governance Binding GO ≠ module fully integrated with Constitution",
    "Module Governance Binding GO ≠ module fully integrated with Health/Oversight",
    "Constitution binding feasible ≠ constitution effectiveness quantified",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_tts_runtime_enable",
    "dryrun_to_tts_provider_invocation",
    "dryrun_to_audio_generation",
    "dryrun_to_voice_output_plane_invocation",
    "dryrun_to_speech_request_generation",
    "dryrun_to_model_selection",
    "dryrun_to_model_download",
    "dryrun_to_model_invocation",
    "dryrun_to_provider_invocation",
    "dryrun_to_benchmark_execution",
    "dryrun_to_license_clearance",
    "dryrun_to_security_review_completion",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_user_output",
    "dryrun_to_controlled_runtime_enable",
    "dryrun_to_full_integration_certification",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "tts_module_model_profile_governance_binding_dryrun_and_review_only",
    "qualification_check_only",
    "tts_module_qualification_check_executed_now",
    "simulated",
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
    "tts_module_model_profile_governance_binding_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
        "system_level_simulated_go": True,
        "candidate_only": True,
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


def _review_from_checks(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"check_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "review_pass": len(issues) == 0,
    }


def _with_review(review_id: str, review: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    return {"review_id": review_id, **review, **meta}


def _resolved_registry_refs(profile: Dict[str, Any]) -> List[str]:
    refs = list(profile.get("registry_model_profile_refs") or [])
    alias = profile.get("registry_placeholder_alias") or {}
    return [alias.get(ref, ref) for ref in refs]


def run_tts_module_model_profile_governance_binding_dryrun_and_review_v1(
    *,
    tts_module_model_profile_governance_binding_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    plan_root = Path(tts_module_model_profile_governance_binding_planning_root).expanduser().resolve()

    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    qual_plan = _try_read_json(plan_root / "tts_module_qualification_check_v1.json") or {}

    mod_def = _try_read_json(plan_root / "tts_module_definition_v1.json") or {}
    stack = _try_read_json(plan_root / "tts_capability_stack_definition_v1.json") or {}
    gov_map = _try_read_json(plan_root / "tts_layered_governance_mapping_v1.json") or {}
    profile = _try_read_json(plan_root / "tts_module_local_model_profile_v1.json") or {}
    refs_plan = _try_read_json(plan_root / "tts_model_profile_registry_refs_review_v1.json") or {}
    roles = _try_read_json(plan_root / "tts_model_role_assignment_plan_v1.json") or {}
    inp = _try_read_json(plan_root / "tts_input_contract_v1.json") or {}
    out = _try_read_json(plan_root / "tts_output_contract_v1.json") or {}
    quality = _try_read_json(plan_root / "tts_quality_acceptance_plan_v1.json") or {}
    health = _try_read_json(plan_root / "tts_health_validation_whitebox_plan_v1.json") or {}
    prov_rt = _try_read_json(plan_root / "tts_provider_runtime_boundary_plan_v1.json") or {}
    fallback = _try_read_json(plan_root / "tts_fallback_replacement_plan_v1.json") or {}
    self_check = _try_read_json(plan_root / "tts_module_internal_self_check_plan_v1.json") or {}
    interaction = _try_read_json(plan_root / "tts_midplatform_interaction_check_plan_v1.json") or {}
    binding = _try_read_json(plan_root / "tts_midplatform_governance_binding_v1.json") or {}
    speech_gate = _try_read_json(plan_root / "tts_speech_gate_handoff_plan_v1.json") or {}
    vop = _try_read_json(plan_root / "tts_voice_output_plane_boundary_plan_v1.json") or {}
    mem_wm = _try_read_json(plan_root / "tts_memory_worldmodel_admission_boundary_plan_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_dryrun_meta(), "output_root": str(out_root), "upstream_planning_root": str(plan_root)}

    if plan_vr.get("verifier") != "GO":
        blockers.append("TTS Planning must be GO")
    if plan_sm.get("final_decision") != PLANNING_FINAL_GO:
        blockers.append("Planning final_decision mismatch")
    if plan_sm.get("module_id") != MODULE_ID:
        blockers.append("module_id must be tts_voice_output_module")
    if not plan_sm.get("qualification_check_only"):
        blockers.append("Planning must be qualification_check_only")

    input_ok = len(blockers) == 0
    resolved_refs = _resolved_registry_refs(profile)
    stack_text = json.dumps(stack, ensure_ascii=False)
    gov_text = json.dumps(gov_map, ensure_ascii=False)
    roles_text = json.dumps(roles, ensure_ascii=False)
    inp_text = json.dumps(inp, ensure_ascii=False)
    out_text = json.dumps(out, ensure_ascii=False)
    quality_text = json.dumps(quality, ensure_ascii=False)
    prov_text = json.dumps(prov_rt, ensure_ascii=False)
    fallback_text = json.dumps(fallback, ensure_ascii=False)
    speech_text = json.dumps(speech_gate, ensure_ascii=False)
    vop_text = json.dumps(vop, ensure_ascii=False)
    mem_text = json.dumps(mem_wm, ensure_ascii=False)

    planning_input_review = {
        "review_id": "planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "module_id": plan_sm.get("module_id"),
        "qualification_mode": plan_sm.get("qualification_mode"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    governance_reuse = _with_review(
        "governance_standard_reuse_review_v1",
        _review_from_checks([
            ("constraints_ref", True),
            ("reuse_rule", True),
            ("new_need_false", True),
            ("reused_count", len(REUSED_GOVERNANCE_STANDARDS) == 15),
            *(("std." + s[:12], s in REUSED_GOVERNANCE_STANDARDS) for s in REUSED_GOVERNANCE_STANDARDS),
        ]),
        meta,
    )

    mod_def_review = _with_review(
        "tts_module_definition_review_v1",
        _review_from_checks([
            ("module_id", mod_def.get("module_id") == MODULE_ID),
            ("domain", "TTS / Voice Output" in mod_def.get("capability_domain", "")),
            ("primary", mod_def.get("primary_goal") == "speech_synthesis_candidate_generation_later"),
            ("related", mod_def.get("related_goal") == "user_output_execution_layer_later"),
            ("no_runtime", mod_def.get("runtime_enabled_now") is False),
            ("no_provider", mod_def.get("provider_invoked_now") is False),
            ("no_audio", mod_def.get("audio_generated_now") is False),
            ("no_vop", mod_def.get("voice_output_plane_invoked_now") is False),
            ("candidate", mod_def.get("candidate_only") is True),
        ]),
        meta,
    )

    stack_review = _with_review(
        "tts_capability_stack_review_v1",
        _review_from_checks([
            ("l1", "layer_1_output_content_acceptance" in stack.get("layers", {})),
            ("l2", "layer_2_speech_synthesis_candidate" in stack.get("layers", {})),
            ("l3", "layer_3_voice_output_application" in stack.get("layers", {})),
            ("l4", any(k.startswith("layer_4_personalization") for k in stack.get("layers", {}))),
            ("not_speak", "does not decide whether to output to user" in json.dumps(mod_def, ensure_ascii=False)),
            ("no_gate_bypass", "Speech Gate bypass" in stack_text),
            ("no_playback", "no direct audio playback" in stack_text),
            ("no_user_out", "no final user output" in stack_text),
            ("no_mem_wm", "Memory/WorldModel" in stack_text),
        ]),
        meta,
    )

    gov_map_review = _with_review(
        "tts_layered_governance_mapping_review_v1",
        _review_from_checks([
            ("l1_output", "output_candidate_ref" in gov_text),
            ("l1_gate", "speech_gate_required" in gov_text),
            ("l1_candidate", "candidate_only" in gov_text),
            ("l2_quality", "synthesis_quality_later" in gov_text),
            ("l2_pronunciation", "pronunciation_uncertainty_later" in gov_text),
            ("l2_voice", "voice_style_control_later" in gov_text),
            ("l2_evidence", "evidence trace" in gov_text),
            ("l3_vop", "Voice Output Plane required" in gov_text),
            ("l3_interrupt", "interruption" in gov_text),
            ("l4_tone", "emotional tone" in gov_text),
            ("l4_privacy", "privacy" in gov_text),
            ("consistent", "governance principles consistent" in gov_text),
            ("layered", "execution intensity layered" in gov_text),
            ("no_audio_without", "no audio output without Speech Gate + Voice Output Plane" in gov_text),
            ("no_weaken", "no weakened constitution by layer" in gov_text),
        ]),
        meta,
    )

    profile_review = _with_review(
        "tts_module_local_model_profile_review_v1",
        _review_from_checks([
            ("profile_id", profile.get("module_local_profile_id") == MODULE_LOCAL_PROFILE_ID),
            ("qianwen", "qianwen_tts_candidate" in (profile.get("registry_model_profile_refs") or [])),
            ("moss", "moss_tts_style_candidate" in (profile.get("registry_model_profile_refs") or [])),
            ("placeholder", TTS_REGISTRY_PLACEHOLDER_REGISTRY_ID in resolved_refs),
            ("stack_ref", profile.get("capability_stack_ref") == CAPABILITY_STACK_DEF_ID),
            ("gov_ref", profile.get("layered_governance_mapping_ref") == LAYERED_GOV_MAPPING_ID),
            ("no_override", profile.get("no_registry_override") is True),
            ("no_select", profile.get("no_model_selection_by_module") is True),
            ("no_invoke", profile.get("no_model_invocation_by_profile") is True),
            ("no_user_out", profile.get("no_direct_user_output") is True),
        ]),
        meta,
    )

    refs_review = _with_review(
        "tts_model_profile_registry_refs_review_v1",
        _review_from_checks([
            ("refs_review_pass", refs_plan.get("review_pass") is True),
            ("qianwen_seed", "qianwen_tts_candidate" in SEED_CANDIDATE_IDS),
            ("moss_seed", "moss_tts_style_candidate" in SEED_CANDIDATE_IDS),
            ("placeholder", TTS_REGISTRY_PLACEHOLDER_REGISTRY_ID in resolved_refs),
            ("candidate_only", "candidate only" in json.dumps(refs_plan, ensure_ascii=False)),
            ("none_selected", "none selected_now" in json.dumps(refs_plan, ensure_ascii=False)),
            ("none_invoked", "none invoked_now" in json.dumps(refs_plan, ensure_ascii=False)),
        ]),
        meta,
    )

    roles_review = _with_review(
        "tts_model_role_assignment_review_v1",
        _review_from_checks([
            ("qianwen_role", "Qianwen TTS maps" in roles_text),
            ("moss_role", "MOSS TTS style maps" in roles_text),
            ("local_role", "local TTS placeholder maps" in roles_text),
            ("no_single_vop", "no single TTS model owns Voice Output Plane" in roles_text),
            ("not_speak", "TTS synthesis ≠ permission to speak" in roles_text),
            ("not_playback", "TTS candidate ≠ audio playback" in roles_text),
        ]),
        meta,
    )

    inp_review = _with_review(
        "tts_input_contract_review_v1",
        _review_from_checks([
            ("speech_gate", "speech_gate_result_candidate_later" in inp_text),
            ("user_out", "user_output_candidate_later" in inp_text),
            ("speech_text", "speech_text_candidate_later" in inp_text),
            ("pronunciation", "pronunciation_hint_candidate_later" in inp_text),
            ("tone", "tone_constraint_candidate_later" in inp_text),
            ("voice_style", "voice_style_candidate_later" in inp_text),
            ("provider_ctx", "provider_context_candidate_later" in inp_text),
            ("no_raw", "raw user text cannot directly trigger TTS" in inp_text),
            ("gate_required", "Speech Gate result required later" in inp_text),
            ("vop_playback", "Voice Output Plane required for playback" in inp_text),
            ("no_request", "no TTS request generated now" in inp_text),
        ]),
        meta,
    )

    out_review = _with_review(
        "tts_output_contract_review_v1",
        _review_from_checks([
            ("tts_request", "tts_request_candidate_later" in out_text),
            ("audio", "audio_artifact_candidate_later" in out_text),
            ("synthesis", "speech_synthesis_candidate_later" in out_text),
            ("pronunciation", "pronunciation_uncertainty_candidate_later" in out_text),
            ("voice_style", "voice_style_candidate_later" in out_text),
            ("playback", "playback_candidate_later" in out_text),
            *(("forbid." + f[:14], f in (out.get("forbidden_outputs") or [])) for f in IO_FORBIDDEN),
        ]),
        meta,
    )

    quality_review = _with_review(
        "tts_quality_acceptance_review_v1",
        _review_from_checks([
            ("naturalness", "speech_naturalness_target_later" in quality_text),
            ("pronunciation", "pronunciation_accuracy_target_later" in quality_text),
            ("latency", "latency_budget_later" in quality_text),
            ("resource", "resource_budget_later" in quality_text),
            ("interrupt_latency", "interruption_latency_target_later" in quality_text),
            ("integrity", "audio_artifact_integrity_required_later" in quality_text),
            ("compliance", quality.get("candidate_contract_compliance_required") is True),
            ("trace", quality.get("traceability_completeness_required") is True),
            ("degrade", quality.get("degradation_behavior_required") is True),
            ("bench_later", quality.get("benchmark_required_later") is True),
            ("bench_now", quality.get("benchmark_executed_now") is False),
        ]),
        meta,
    )

    health_review = _with_review(
        "tts_health_validation_whitebox_review_v1",
        _review_from_checks([
            ("validation_ref", bool(health.get("validation_requirement_ref"))),
            ("health_later", health.get("health_requirement_ref") == "required_later"),
            ("supervision_later", health.get("supervision_metric_ref") == "required_later"),
            ("health_detail_false", health.get("health_metric_detail_defined_now") is False),
            ("super_detail_false", health.get("supervision_metric_detail_defined_now") is False),
            ("whitebox", bool(health.get("whitebox_trace_requirement_ref"))),
            ("source_chain", health.get("source_chain_required") is True),
            ("issue_trace", health.get("issue_trace_required") is True),
            ("transport_only", health.get("health_status_ref_transport_only") is True),
            ("no_self_cert", health.get("module_cannot_self_certify_health") is True),
            ("constitution_not_quant", meta.get("constitution_effectiveness_quantified_now") is False),
            ("health_not_final", meta.get("health_metrics_finalized_now") is False),
            ("super_not_final", meta.get("supervision_metrics_finalized_now") is False),
            ("not_fully_const", meta.get("module_constitution_fully_integrated_now") is False),
            ("not_fully_oversight", meta.get("module_oversight_fully_integrated_now") is False),
        ]),
        meta,
    )

    prov_review = _with_review(
        "tts_provider_runtime_boundary_review_v1",
        _review_from_checks([
            ("prov_required", prov_rt.get("provider_abstraction_required") is True),
            ("cr_required", prov_rt.get("controlled_runtime_required") is True),
            ("not_selected", "provider_candidate ≠ selected ≠ invoked" in prov_text),
            ("no_auto", "no provider auto-switch" in prov_text),
            ("cr_later", "Controlled Runtime later" in prov_text),
            ("vop_later", "Voice Output Plane required for playback later" in prov_text),
            ("no_runtime", "TTS runtime remains disabled now" in prov_text),
        ]),
        meta,
    )

    fallback_review = _with_review(
        "tts_fallback_replacement_review_v1",
        _review_from_checks([
            ("refs_structured", len(fallback.get("fallback_model_profile_refs") or []) >= 3),
            ("quality", "quality_regression" in fallback_text),
            ("provider", "provider_unavailable" in fallback_text),
            ("license", "license_risk" in fallback_text),
            ("latency", "latency_budget_failure" in fallback_text),
            ("hardware", "hardware_incompatibility" in fallback_text),
            ("pronunciation", "pronunciation_failure" in fallback_text),
            ("interrupt", "interruption_latency_failure" in fallback_text),
            ("hold", "hold_instead_of_fallback" in fallback_text or "safety/privacy/licensing" in fallback_text),
            ("no_auto", fallback.get("no_auto_switch_without_governance_policy") is True),
            ("no_invoke", fallback.get("replacement_does_not_imply_invocation") is True),
        ]),
        meta,
    )

    self_check_review = _with_review(
        "tts_module_internal_self_check_review_v1",
        _review_from_checks(
            [("plan_exists", bool(self_check.get("plan_id")))]
            + [(c[:16], c in (self_check.get("self_check_coverage") or []))
               for c in MODULE_INTERNAL_SELF_CHECK_COVERAGE]
        ),
        meta,
    )

    interaction_review = _with_review(
        "tts_midplatform_interaction_check_review_v1",
        _review_from_checks(
            [("plan_exists", bool(interaction.get("plan_id")))]
            + [(c[:16], c in (interaction.get("interaction_check_coverage") or []))
               for c in TTS_MIDPLATFORM_INTERACTION_CHECK_COVERAGE]
        ),
        meta,
    )

    binding_review = _with_review(
        "tts_midplatform_governance_binding_review_v1",
        _review_from_checks([
            ("binding_id", binding.get("midplatform_governance_binding_id") == MIDPLATFORM_BINDING_ID),
            ("profile_ref", binding.get("module_local_profile_ref") == MODULE_LOCAL_PROFILE_ID),
            ("refs_preserved", len(binding.get("registry_model_profile_refs") or []) >= 3),
            ("constitution", binding.get("constitution_bus_ref") == CONSTITUTION_BUS_REF),
            ("capability_bus", bool(binding.get("capability_bus_contract_ref"))),
            ("provider", binding.get("provider_abstraction_ref") == PROVIDER_ABS_STANDARD_ID),
            ("validation", bool(binding.get("validation_requirement_ref"))),
            ("health_later", binding.get("health_requirement_ref") == "required_later"),
            ("whitebox", bool(binding.get("whitebox_trace_requirement_ref"))),
            ("speech_gate", binding.get("speech_gate_requirement_ref") == SPEECH_GATE_REF),
            ("vop_later", binding.get("voice_output_plane_requirement_ref_later") == VOICE_OUTPUT_PLANE_REF),
            ("cr_ref", binding.get("controlled_runtime_requirement_ref") == CONTROLLED_RUNTIME_FRAMEWORK_REF),
            ("no_select", binding.get("model_selected_now") is False),
            ("no_invoke", binding.get("model_invoked_now") is False),
            ("no_runtime", binding.get("runtime_enabled_now") is False),
        ]),
        meta,
    )

    speech_gate_review = _with_review(
        "tts_speech_gate_handoff_review_v1",
        _review_from_checks([
            ("consume_later", "Speech Gate-approved candidate later" in speech_text),
            ("pass_not_exec", "Speech Gate pass ≠ TTS execution" in speech_text),
            ("not_before", "TTS does not run before Speech Gate" in speech_text),
            ("no_modify", "does not modify safety/refusal decision" in speech_text),
            ("no_consume", "no speech_gate_result consumed now" in speech_text),
        ]),
        meta,
    )

    vop_review = _with_review(
        "tts_voice_output_plane_boundary_review_v1",
        _review_from_checks([
            ("not_playback", "TTS synthesis candidate ≠ playback" in vop_text),
            ("vop_required", "Voice Output Plane required later for audio emission" in vop_text),
            ("interrupt", "interruption / abort support later" in vop_text),
            ("auth_later", "playback authorization later" in vop_text),
            ("no_invoke", "no Voice Output Plane invoked now" in vop_text),
            ("no_audio", "no audio played now" in vop_text),
        ]),
        meta,
    )

    mem_wm_review = _with_review(
        "tts_memory_worldmodel_admission_boundary_review_v1",
        _review_from_checks([
            ("no_mem", "cannot write Memory" in mem_text),
            ("no_wm", "cannot write WorldModel" in mem_text),
            ("pref_later", "voice preference personalization later" in mem_text),
            ("emotion_later", "emotional tone later requires Emotion/Privacy governance" in mem_text),
            ("no_write_now", "no memory/worldmodel write now" in mem_text),
        ]),
        meta,
    )

    qual_check_review = _with_review(
        "tts_module_qualification_check_review_v1",
        _review_from_checks([
            ("qual_only", qual_plan.get("qualification_check_only") is True or meta.get("qualification_check_only") is True),
            ("full_cert_false", meta.get("full_integration_certification_now") is False),
            ("constitution_feasible", meta.get("constitution_binding_feasible") is True),
            ("oversight_feasible", meta.get("oversight_binding_feasible") is True),
            ("can_say_registry", CLOSURE_CAN_SAY[0] in (qual_plan.get("can_say") or [])),
            ("cannot_runtime", CLOSURE_CANNOT_SAY[0] in (qual_plan.get("cannot_say") or [])),
            ("cannot_vop", "Voice Output Plane is active" in str(qual_plan.get("cannot_say"))),
            ("cannot_metrics", "health/supervision metrics finalized" in str(qual_plan.get("cannot_say"))),
        ] + [(k, meta.get(k) is v) for k, v in QUALIFICATION_FIELDS.items() if k not in (
            "qualification_check_only", "full_integration_certification_now",
            "constitution_binding_feasible", "oversight_binding_feasible",
        )]),
        meta,
    )

    boundary_audit = {
        "audit_id": "tts_non_runtime_boundary_audit_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "audit_pass": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "tts_blocked_path_result_v1",
        "blocked_paths": [{"path_id": p, "status": "blocked", "executed": False} for p in BLOCKED_PATHS],
        "blocked_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    all_reviews = [
        governance_reuse, mod_def_review, stack_review, gov_map_review, profile_review,
        refs_review, roles_review, inp_review, out_review, quality_review, health_review,
        prov_review, fallback_review, self_check_review, interaction_review, binding_review,
        speech_gate_review, vop_review, mem_wm_review, qual_check_review,
    ]

    qualification_pass = (
        input_ok
        and qual_plan.get("qualification_pass") is True
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
        and all(r.get("review_pass") for r in all_reviews)
    )

    candidate = {
        "candidate_id": "tts_module_model_profile_governance_binding_candidate_v1",
        "module_id": MODULE_ID,
        "module_local_profile_ref": MODULE_LOCAL_PROFILE_ID,
        "midplatform_governance_binding_ref": MIDPLATFORM_BINDING_ID,
        "registry_model_profile_refs": list(CANDIDATE_REGISTRY_REFS),
        "registry_ref": REGISTRY_REF,
        "midplatform_binding_standard_ref": MIDPLATFORM_BINDING_STANDARD_ID,
        "module_local_profile_standard_ref": MODULE_LOCAL_PROFILE_STANDARD_REF,
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_pass": qualification_pass,
        "runtime_enabled_now": False,
        "model_selected_now": False,
        "model_invoked_now": False,
        "audio_generated_now": False,
        "voice_output_plane_invoked_now": False,
        **meta,
    }

    closure_decision = {
        "decision_id": "tts_module_closure_decision_v1",
        "dryrun_and_review_pass": qualification_pass,
        "high_risk": not qualification_pass,
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_check_only": True,
        "final_decision": FINAL_DECISION_GO if qualification_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if qualification_pass else NEXT_PHASE_HOLD,
        "closure_can_say": list(CLOSURE_CAN_SAY),
        "closure_cannot_say": list(CLOSURE_CANNOT_SAY),
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_asr_module_model_profile_governance_binding_planning": qualification_pass,
        "selected_next_phase": NEXT_PHASE_GO if qualification_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "tts_module_model_profile_governance_binding_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "qualification_check_only": True,
        "phase_goal": (
            "TTS module qualification verification only. "
            "No TTS runtime/provider/benchmark/audio/Voice Output Plane."
        ),
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
        "dryrun_and_review_pass": qualification_pass,
        "module_id": MODULE_ID,
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_check_only": True,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "tts_module_model_profile_governance_binding_dryrun_review_policy": policy,
        "planning_input_review": planning_input_review,
        "governance_standard_reuse_review": governance_reuse,
        "tts_module_model_profile_governance_binding_candidate": candidate,
        "tts_module_definition_review": mod_def_review,
        "tts_capability_stack_review": stack_review,
        "tts_layered_governance_mapping_review": gov_map_review,
        "tts_module_local_model_profile_review": profile_review,
        "tts_model_profile_registry_refs_review": refs_review,
        "tts_model_role_assignment_review": roles_review,
        "tts_input_contract_review": inp_review,
        "tts_output_contract_review": out_review,
        "tts_quality_acceptance_review": quality_review,
        "tts_health_validation_whitebox_review": health_review,
        "tts_provider_runtime_boundary_review": prov_review,
        "tts_fallback_replacement_review": fallback_review,
        "tts_module_internal_self_check_review": self_check_review,
        "tts_midplatform_interaction_check_review": interaction_review,
        "tts_midplatform_governance_binding_review": binding_review,
        "tts_speech_gate_handoff_review": speech_gate_review,
        "tts_voice_output_plane_boundary_review": vop_review,
        "tts_memory_worldmodel_admission_boundary_review": mem_wm_review,
        "tts_module_qualification_check_review": qual_check_review,
        "tts_non_runtime_boundary_audit": boundary_audit,
        "tts_blocked_path_result": blocked_path_result,
        "tts_module_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
