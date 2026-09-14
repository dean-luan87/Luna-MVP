# -*- coding: utf-8 -*-
"""Module-local Model Profile Standardization Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.layered_capability_stack_standard_v1 import STANDARD_ID as UNIVERSAL_STACK_STANDARD_ID
from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    PHASE_GOVERNANCE_STANDARD_REUSE_RULE,
)
from capabilities.governance.model_profile_registry_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as REGISTRY_DR_FINAL_GO,
)
from capabilities.governance.model_profile_registry_planning_v1 import SEED_CANDIDATE_IDS

PHASE_ID = "Phase-Module-Local-Model-Profile-Standardization-Planning-v1-001"
SCOPE = "module_local_model_profile_standardization_planning_only"
SOURCE_CHAIN = "module_local_model_profile_standardization_planning_v1"

FINAL_DECISION_GO = "MODULE_LOCAL_MODEL_PROFILE_STANDARDIZATION_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MODULE_LOCAL_MODEL_PROFILE_STANDARDIZATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Module-Local-Model-Profile-Standardization-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Module-Local-Model-Profile-Issue-Review-v1-001"

REGISTRY_REF = "luna_model_profile_registry_v1"

MODULE_LOCAL_PROFILE_SCHEMA_FIELDS: Tuple[str, ...] = (
    "module_local_profile_id", "module_id", "module_type", "capability_domain",
    "capability_stack_ref", "capability_stack_layer", "layered_governance_mapping_ref",
    "registry_model_profile_ref", "model_role_in_module", "model_source_strategy",
    "model_profile_status", "module_input_contract_refs", "module_output_contract_refs",
    "expected_model_input_types", "expected_model_output_types", "candidate_output_type",
    "confidence_semantics", "ttl_semantics", "source_chain_required", "whitebox_trace_required",
    "quality_acceptance_ref", "validation_requirement_ref", "health_requirement_ref",
    "provider_abstraction_ref", "controlled_runtime_requirement_ref",
    "fallback_model_profile_refs", "replacement_conditions", "version_compatibility_ref",
    "midplatform_governance_binding_ref", "no_registry_override", "no_model_selection_by_module",
    "no_model_invocation_by_profile", "no_direct_fact_action_output",
)

STANDARD_DUTIES: Tuple[str, ...] = (
    "require modules to reference model_profile_id from Registry",
    "describe module-specific model usage role",
    "bind model to capability stack layer",
    "bind model to layered governance mapping",
    "bind model I/O to module contracts",
    "define fallback and replacement conditions",
    "define validation / health / whitebox requirements",
    "define provider/runtime boundary",
    "expose module-local profile refs to midplatform governance binding",
)

STANDARD_NOT: Tuple[str, ...] = (
    "model_selector", "model_invoker", "provider_runtime", "benchmark_runner",
    "license_clearing_authority", "registry_override", "module_owned_governance_authority",
)

DOMAIN_COVERAGE: Tuple[str, ...] = (
    "Vision", "OCR", "TTS", "ASR", "Map/Navigation", "World Continuity",
    "Memory", "Emotion", "Evolution", "Provider/Model Management",
)

REUSED_GOVERNANCE_STANDARDS: Tuple[str, ...] = (
    "Model Profile Registry",
    "Layered Capability Stack Standard",
    "Layered Governance Mapping",
    "Constitution-Bus v1.0",
    "Provider Abstraction Standard",
    "Controlled Runtime Framework",
    "Health Oversight Externality",
    "Whitebox Trace Standard",
    "Candidate/Evidence Contract pattern",
    "Boundary Matrix / Blocked Path / Non-Claims pattern",
)

IO_FORBIDDEN: Tuple[str, ...] = (
    "direct_fact", "direct_action", "direct_user_output", "direct_memory_write",
    "direct_worldmodel_write", "direct_runtime_enable",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Module-local Model Profile Standardization Planning GO ≠ model connected",
    "module-local profile template ≠ module runtime enabled",
    "registry ref planned ≠ model selected",
    "qianwen/yolo/ocr/asr module template ≠ invoked",
    "next DryRunAndReview ≠ benchmark/runtime",
    "Module Internal Self-Check GO ≠ Midplatform Interaction Check GO",
    "Midplatform Interaction Check GO ≠ Runtime Ready",
)

DUAL_VALIDATION_MECHANISM_ID = "dual_validation_mechanism_v1"
DUAL_VALIDATION_MECHANISM_ZH = "双检验机制"

MODULE_INTERNAL_SELF_CHECK_COVERAGE: Tuple[str, ...] = (
    "capability_stack_definition",
    "layered_governance_mapping",
    "module_local_model_profile",
    "input_contracts",
    "output_contracts",
    "candidate_object_set",
    "model_profile_ref",
    "quality_acceptance_ref",
    "fallback_replacement_policy",
    "failure_route_set",
    "boundary_matrix",
    "blocked_paths",
    "non_claims",
)

MIDPLATFORM_INTERACTION_CHECK_COVERAGE: Tuple[str, ...] = (
    "Constitution-Bus binding",
    "Capability Bus contract",
    "Provider Abstraction binding",
    "Information Integration handoff",
    "Decision Center handoff",
    "Validation requirement",
    "Health requirement / Health external oversight",
    "Whitebox trace",
    "Gate Chain binding",
    "Controlled Runtime requirement",
    "Memory / WorldModel Admission requirement if applicable",
    "source_chain / evidence / traceability preservation",
)

DUAL_VALIDATION_NON_CLAIMS: Tuple[str, ...] = (
    "Module Internal Self-Check GO ≠ Midplatform Interaction Check GO",
    "Midplatform Interaction Check GO ≠ Runtime Ready",
    "self-check pass ≠ midplatform interaction pass",
    "interaction-check pass ≠ controlled runtime ready",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("module_local_model_profile_standardization_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "module_local_profile_standard_runtime_enabled_now", "module_local_profile_created_as_runtime_now",
    "model_selected_now", "model_downloaded_now", "model_invoked_now", "provider_invoked_now",
    "model_runtime_enabled_now", "benchmark_executed_now", "license_cleared_now",
    "security_review_completed_now", "training_started_now", "fine_tuning_started_now",
    "code_generation_executed_now", "skill_added_now", "memory_written_now",
    "world_model_written_now", "task_state_committed_now", "user_output_generated_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "module_local_model_profile_standardization_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
        "system_level_simulated_go": True,
        "candidate_only": True,
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


def _module_template(
    template_id: str,
    module_id: str,
    capability_domain: str,
    registry_refs: List[str],
    layers: List[str],
    outputs: List[str],
    confirmations: List[str],
    *,
    module_type: str = "capability_module",
    stack_layer: str = "layer_1_perception",
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    profiles = []
    for ref in registry_refs:
        profiles.append({
            "module_local_profile_id": f"{module_id}__{ref}",
            "module_id": module_id,
            "module_type": module_type,
            "capability_domain": capability_domain,
            "capability_stack_ref": UNIVERSAL_STACK_STANDARD_ID,
            "capability_stack_layer": stack_layer,
            "layered_governance_mapping_ref": ADDENDUM_ID,
            "registry_model_profile_ref": ref,
            "registry_ref": REGISTRY_REF,
            "model_role_in_module": "signal_or_candidate_provider",
            "model_profile_status": "candidate_registered",
            "no_registry_override": True,
            "no_model_selection_by_module": True,
            "no_model_invocation_by_profile": True,
            "no_direct_fact_action_output": True,
            "selected_now": False,
            "invoked_now": False,
        })
    base = {
        "template_id": template_id,
        "module_id": module_id,
        "capability_domain": capability_domain,
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_refs": registry_refs,
        "capability_layers": layers,
        "module_outputs": outputs,
        "module_local_profiles": profiles,
        "confirmations": confirmations,
    }
    if extra:
        base.update(extra)
    return base


def run_module_local_model_profile_standardization_planning_v1(
    *,
    model_profile_registry_dryrun_and_review_root: str,
    model_profile_registry_planning_root: str,
    scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review_root: str,
    layered_capability_stack_standard_dryrun_and_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_controlled_runtime_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    registry_dr_root = Path(model_profile_registry_dryrun_and_review_root).expanduser().resolve()
    registry_plan_root = Path(model_profile_registry_planning_root).expanduser().resolve()
    roadmap_dr_root = Path(
        scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review_root
    ).expanduser().resolve()
    stack_root = Path(layered_capability_stack_standard_dryrun_and_review_root).expanduser().resolve()
    cb_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    provider_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    cr_root = Path(midplatform_controlled_runtime_dryrun_and_review_root).expanduser().resolve()

    registry_dr_vr = _try_read_json(registry_dr_root / "verifier_report.json") or {}
    registry_dr_sm = _try_read_json(registry_dr_root / "summary.json") or {}
    registry_candidate = _try_read_json(registry_dr_root / "model_profile_registry_candidate_v1.json") or {}
    seeds_review = _try_read_json(registry_dr_root / "seed_model_profile_candidates_review_v1.json") or {}
    module_binding_r = _try_read_json(registry_dr_root / "module_local_binding_review_v1.json") or {}
    mid_binding_r = _try_read_json(registry_dr_root / "midplatform_governance_binding_review_v1.json") or {}
    stack_vr = _try_read_json(stack_root / "verifier_report.json") or {}
    cb_vr = _try_read_json(cb_root / "verifier_report.json") or {}
    provider_vr = _try_read_json(provider_root / "verifier_report.json") or {}
    cr_vr = _try_read_json(cr_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "output_root": str(out_root),
        "upstream_registry_dryrun_root": str(registry_dr_root),
        "upstream_registry_planning_root": str(registry_plan_root),
    }

    if registry_dr_vr.get("verifier") != "GO":
        blockers.append("Model Profile Registry DryRunAndReview must be GO")
    if registry_dr_sm.get("final_decision") != REGISTRY_DR_FINAL_GO:
        blockers.append("Registry DryRunAndReview final_decision mismatch")
    if registry_candidate.get("registry_id") != REGISTRY_REF:
        blockers.append("luna_model_profile_registry_v1 candidate missing")
    if not seeds_review.get("review_pass"):
        blockers.append("14 seed candidates must be reviewed")
    if not module_binding_r.get("review_pass"):
        blockers.append("module-local binding rules must be reviewed")
    if not mid_binding_r.get("review_pass"):
        blockers.append("midplatform binding rules must be reviewed")
    for name, vr in (
        ("stack_std", stack_vr), ("constitution_bus", cb_vr),
        ("provider_abs", provider_vr), ("controlled_runtime", cr_vr),
    ):
        if vr.get("verifier") != "GO":
            blockers.append(f"{name} must be GO")

    input_ok = len(blockers) == 0

    registry_input_review = {
        "review_id": "model_profile_registry_input_review_v1",
        "registry_dryrun_verifier": registry_dr_vr.get("verifier"),
        "registry_dryrun_final_decision": registry_dr_sm.get("final_decision"),
        "registry_id": registry_candidate.get("registry_id"),
        "seed_candidate_count": registry_dr_sm.get("seed_candidate_count"),
        "seeds_review_pass": seeds_review.get("review_pass"),
        "module_binding_review_pass": module_binding_r.get("review_pass"),
        "mid_binding_review_pass": mid_binding_r.get("review_pass"),
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
        "module_local_binding_standardization_not_new_framework": True,
        **meta,
    }

    standard_definition = {
        "standard_id": "module_local_model_profile_standard_v1",
        "standard_type": "module_level_model_profile_binding_standard",
        "scope": "Luna capability modules",
        "registry_ref": REGISTRY_REF,
        "module_local_profile_runtime_enabled_now": False,
        "model_selection_allowed_now": False,
        "model_invocation_allowed_now": False,
        "candidate_only": True,
        "standard_duties": list(STANDARD_DUTIES),
        "standard_is_not": list(STANDARD_NOT),
        "core_principle": {
            "registry": "总档案库",
            "module_local_profile": "模块内部实现说明",
            "midplatform_binding": "中台监管合同",
        },
        "dual_validation_mechanism": {
            "mechanism_id": DUAL_VALIDATION_MECHANISM_ID,
            "mechanism_name": "Dual Validation Mechanism",
            "mechanism_name_zh": DUAL_VALIDATION_MECHANISM_ZH,
            "layers": [
                {"layer": 1, "name": "Module Internal Self-Check", "name_zh": "模块内部自检"},
                {"layer": 2, "name": "Midplatform Interaction Check", "name_zh": "中台交互检验"},
            ],
            "progression": [
                "Module-local Model Profile Standardization",
                "Module Internal Self-Check",
                "Midplatform Interaction Check",
                "Controlled Runtime Readiness",
                "Model Candidate Controlled Trial",
            ],
            "summary_zh": "模块先证明自己内部不乱，再证明自己接入中台不越权",
        },
        **meta,
    }

    profile_schema = {
        "schema_id": "module_local_model_profile_schema_v1",
        "required_fields": list(MODULE_LOCAL_PROFILE_SCHEMA_FIELDS),
        "defaults": {
            "source_chain_required": True,
            "whitebox_trace_required": True,
            "no_registry_override": True,
            "no_model_selection_by_module": True,
            "no_model_invocation_by_profile": True,
            "no_direct_fact_action_output": True,
        },
        **meta,
    }

    registry_ref_policy = {
        "policy_id": "module_local_profile_to_registry_reference_policy_v1",
        "rules": [
            "every module-local profile must reference registry_model_profile_ref",
            "registry_model_profile_ref must exist in luna_model_profile_registry_v1",
            "module-local profile cannot create unregistered model profile",
            "module-local profile cannot override registry version/license/source status",
            "module-local profile can only add module-specific usage context",
            "missing registry ref blocks module-local profile admission",
        ],
        "registry_ref": REGISTRY_REF,
        **meta,
    }

    stack_binding_policy = {
        "policy_id": "module_local_profile_capability_stack_binding_policy_v1",
        "rules": [
            "every module-local profile must bind capability_stack_ref",
            "model must map to specific capability_stack_layer",
            "application-layer model cannot claim foundation-layer authority",
            "navigation model remains Layer 3 application",
            "person/identity model remains high-risk later layer",
            "lower-layer dependencies must be declared",
        ],
        "capability_stack_ref": UNIVERSAL_STACK_STANDARD_ID,
        **meta,
    }

    gov_binding_policy = {
        "policy_id": "module_local_profile_layered_governance_binding_policy_v1",
        "rules": [
            "every module-local profile must bind layered_governance_mapping_ref",
            "governance principles consistent across layers",
            "execution intensity varies by layer",
            "L1 models require source_chain / confidence / ttl / candidate-only",
            "L2 models require freshness/conflict/gap/evidence chain",
            "L3 models require safety/task boundary/Decision linkage",
            "L4/L5 models require privacy/identity/memory admission",
            "module cannot apply all governance rules blindly to all layers",
            "module cannot weaken constitution principles by layer",
        ],
        "layered_governance_mapping_ref": ADDENDUM_ID,
        **meta,
    }

    io_binding_policy = {
        "policy_id": "module_local_profile_input_output_binding_policy_v1",
        "allowed_inputs": [
            "module input candidate/context/signal refs",
            "registry-approved model input profile",
            "provider_context_candidate",
            "drive_signal_candidate",
            "integrated_context_candidate",
        ],
        "allowed_outputs": ["candidate", "evidence", "signal", "context", "proposal"],
        "forbidden_outputs": list(IO_FORBIDDEN),
        **meta,
    }

    quality_binding_policy = {
        "policy_id": "module_local_profile_quality_acceptance_binding_policy_v1",
        "rules": [
            "each module-local profile must reference quality_acceptance_ref",
            "module-specific latency/resource budget required",
            "confidence semantics required",
            "failure behavior required",
            "degradation behavior required",
            "candidate contract compliance required",
            "benchmark required later does not mean benchmark executed now",
        ],
        **meta,
    }

    health_binding_policy = {
        "policy_id": "module_local_profile_health_validation_whitebox_binding_policy_v1",
        "rules": [
            "validation_requirement_ref required",
            "health_requirement_ref required",
            "whitebox_trace_required=true",
            "health_status_ref transported, not judged by Bus",
            "issue_trace / failure_route required",
            "module-local profile cannot self-certify health",
            "module-local profile cannot suppress validation failure",
        ],
        **meta,
    }

    provider_boundary_policy = {
        "policy_id": "module_local_profile_provider_runtime_boundary_policy_v1",
        "rules": [
            "provider_abstraction_ref required if provider-backed",
            "controlled_runtime_requirement_ref required if runtime-capable",
            "module-local profile cannot select provider",
            "module-local profile cannot invoke provider",
            "module-local profile cannot enable runtime",
            "provider_candidate ≠ selected ≠ invoked",
            "runtime readiness remains later",
        ],
        **meta,
    }

    fallback_policy = {
        "policy_id": "module_local_profile_fallback_replacement_policy_v1",
        "rules": [
            "fallback_model_profile_refs optional but structured",
            "replacement_conditions required",
            "no auto-switch without governance policy",
            "high-risk replacement requires owner/governance/validation/rollback later",
            "fallback does not imply runtime invocation",
            "hold may be preferred to fallback when safety/privacy/licensing risk exists",
        ],
        **meta,
    }

    midplatform_handoff = {
        "policy_id": "module_local_profile_midplatform_handoff_policy_v1",
        "rules": [
            "module-local profile exposes midplatform_governance_binding_ref",
            "binding includes Constitution-Bus",
            "Provider Abstraction",
            "Validation",
            "Health",
            "Whitebox",
            "Controlled Runtime",
            "Output Gate if output-capable",
            "Memory/WorldModel admission if write-capable later",
            "Information Integration / Decision consumption policy if candidate-consuming",
        ],
        **meta,
    }

    module_internal_self_check_policy = {
        "policy_id": "module_internal_self_check_policy_v1",
        "mechanism_layer": "Module Internal Self-Check",
        "mechanism_layer_zh": "模块内部自检",
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "purpose": "模块自己有没有按标准写好",
        "rules": [
            "每个模块必须能独立完成内部合规自检",
            "自检对象是模块内部规范，不替代中台检验",
            "自检不授权 runtime",
            "自检不选择模型",
            "自检不调用 provider",
            "自检不写 Memory / WorldModel",
            "自检不生成 user output",
        ],
        "self_check_coverage": list(MODULE_INTERNAL_SELF_CHECK_COVERAGE),
        "self_check_focus": [
            "capability_stack_definition 是否完整",
            "layered_governance_mapping 是否完整",
            "module-local model profile 是否引用 registry profile",
            "输入输出合同是否清晰",
            "candidate / evidence / signal / context 是否区分",
            "fallback / replacement / failure route 是否定义",
            "quality / latency / resource / confidence 是否声明",
            "runtime / memory / worldmodel / user_output 边界是否关闭",
        ],
        "does_not_replace": "Midplatform Interaction Check",
        **meta,
    }

    midplatform_interaction_check_policy = {
        "policy_id": "midplatform_interaction_check_policy_v1",
        "mechanism_layer": "Midplatform Interaction Check",
        "mechanism_layer_zh": "中台交互检验",
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "purpose": "模块和中台互动时有没有越权、漏接、绕路",
        "rules": [
            "中台检验对象是模块与中台的交互合规性",
            "中台检验不替代模块内部自检",
            "中台检验不等于 runtime 授权",
            "中台检验不等于模型选择",
            "中台检验不等于 provider invocation",
        ],
        "interaction_check_coverage": list(MIDPLATFORM_INTERACTION_CHECK_COVERAGE),
        "interaction_check_focus": [
            "是否接入 Constitution-Bus",
            "是否绑定 Provider Abstraction",
            "是否把输出交给 Information Integration",
            "是否由 Decision Center 裁决",
            "是否接入 Validation / Health / Whitebox",
            "是否经过 Gate Chain",
            "是否遵守 Controlled Runtime",
            "是否没有绕过 Memory / WorldModel Admission",
            "是否保留 source_chain / evidence / traceability",
            "是否没有直接 select / invoke model",
        ],
        "does_not_replace": "Module Internal Self-Check",
        **meta,
    }

    vision_template = _module_template(
        "vision_module_local_model_profile_template_v1",
        "vision_scene_understanding_module",
        "first_person_vision_scene_understanding",
        [
            "yolo_family_object_detection_candidate",
            "grounded_sam_style_grounding_segmentation_candidate",
            "visual_tracking_candidate",
            "vlm_scene_understanding_candidate",
        ],
        ["Current Scene Understanding", "Spatiotemporal Continuity later"],
        [
            "visual_observation_candidate", "target_recognition_candidate",
            "tracking_candidate", "scene_context_candidate", "risk_context_candidate",
        ],
        ["no camera/runtime now", "no fact/action output", "no model selected/invoked"],
        stack_layer="layer_1_perception",
    )

    ocr_template = _module_template(
        "ocr_module_local_model_profile_template_v1",
        "ocr_text_reading_module",
        "ocr_text_recognition_reading",
        ["rapidocr_candidate", "paddleocr_candidate", "other_ocr_provider_placeholder"],
        ["text region detection", "OCR reading candidate", "text structure later", "reading application later"],
        ["text_region_candidate", "ocr_result_candidate", "signage_context_candidate", "reading_candidate later"],
        ["OCR output candidate only", "no fact", "no OCR runtime"],
    )

    tts_template = _module_template(
        "tts_module_local_model_profile_template_v1",
        "tts_voice_output_module",
        "tts_voice_output",
        ["qianwen_tts_candidate", "moss_tts_style_candidate", "local_tts_placeholder"],
        ["Voice Output / TTS ExecutionRuntime later"],
        ["audio_artifact_candidate later", "speech synthesis candidate later"],
        ["qianwen candidate ≠ selected", "no TTS invocation", "Speech Gate / Voice Output Plane required"],
        stack_layer="layer_6_runtime_later",
    )

    asr_template = _module_template(
        "asr_module_local_model_profile_template_v1",
        "asr_voice_input_module",
        "asr_voice_input",
        ["sensevoice_asr_candidate", "whisper_like_asr_candidate", "qwen_asr_style_candidate"],
        ["audio capture candidate", "ASR transcript candidate", "intent/emotion/speaker later"],
        ["transcript_candidate", "voice_intent_candidate later"],
        ["ASR not_started/planned_only", "no ASR runtime"],
    )

    map_template = _module_template(
        "map_navigation_module_local_model_profile_template_v1",
        "map_navigation_application_module",
        "map_location_navigation_application",
        [
            "map_provider_placeholder", "route_reasoning_candidate",
            "indoor_facility_search_candidate", "transit_context_candidate",
        ],
        ["Stage 3 Navigation Application Layer"],
        [
            "map_location_context_candidate", "route_context_candidate",
            "navigation_task_candidate", "facility_search_candidate later",
        ],
        [
            "navigation depends on Stage 1 + Stage 2",
            "no map provider invocation", "no navigation action",
        ],
        stack_layer="layer_4_application",
    )

    world_template = _module_template(
        "world_continuity_module_local_model_profile_template_v1",
        "world_continuity_understanding_module",
        "spatiotemporal_world_continuity",
        [
            "scene_delta_candidate", "temporal_tracking_candidate",
            "visual_map_alignment_candidate", "stcm_self_developed_profile",
        ],
        ["Stage 2 Spatiotemporal Continuity / World Continuity"],
        [
            "world_continuity_candidate", "scene_delta_candidate",
            "missing_context_hypothesis_candidate",
        ],
        [
            "external models provide signals only", "Luna owns continuity governance",
            "no WorldModel write",
        ],
        stack_layer="layer_2_spatiotemporal",
    )

    mem_emo_evo_template = {
        "template_id": "memory_emotion_evolution_module_local_model_profile_template_v1",
        "modules": [
            {"module_id": "memory_personal_continuity_module", "capability_domain": "memory_personal_continuity"},
            {"module_id": "emotion_engine_module", "capability_domain": "emotion_engine_social_adaptation"},
            {"module_id": "evolutionary_recursion_module", "capability_domain": "evolutionary_recursion_self_improvement"},
        ],
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_refs": [
            "embedding_retrieval_candidate",
            "emotion_signal_model_candidate",
            "relationship_context_model_candidate",
            "market_feedback_analysis_candidate",
            "code_analysis_assistant_candidate",
        ],
        "module_local_profiles": [
            {
                "module_local_profile_id": f"memory_personal_continuity_module__embedding_retrieval_candidate",
                "module_id": "memory_personal_continuity_module",
                "registry_model_profile_ref": "embedding_retrieval_candidate",
                "registry_ref": REGISTRY_REF,
                "no_registry_override": True,
                "no_model_selection_by_module": True,
                "no_model_invocation_by_profile": True,
                "selected_now": False,
                "invoked_now": False,
            },
            {
                "module_local_profile_id": "emotion_engine_module__emotion_signal_model_candidate",
                "module_id": "emotion_engine_module",
                "registry_model_profile_ref": "emotion_signal_model_candidate",
                "registry_ref": REGISTRY_REF,
                "no_registry_override": True,
                "selected_now": False,
                "invoked_now": False,
            },
            {
                "module_local_profile_id": "evolutionary_recursion_module__market_feedback_analysis_candidate",
                "module_id": "evolutionary_recursion_module",
                "registry_model_profile_ref": "market_feedback_analysis_candidate",
                "registry_ref": REGISTRY_REF,
                "proposal_only": True,
                "selected_now": False,
                "invoked_now": False,
            },
        ],
        "confirmations": [
            "Personal Continuity governance self-owned",
            "Emotion governance self-owned",
            "Evolutionary Recursion proposal_only",
            "no memory write", "no code modification", "no skill addition",
        ],
        **meta,
    }

    domain_matrix = {
        "matrix_id": "module_local_profile_domain_coverage_matrix_v1",
        "domains": [
            {"domain": d, "template_ref": f"{d.lower().replace('/', '_').replace(' ', '_')}_template"}
            for d in DOMAIN_COVERAGE
        ],
        "domain_count": len(DOMAIN_COVERAGE),
        "templates_provided": [
            "vision", "ocr", "tts", "asr", "map_navigation", "world_continuity", "memory_emotion_evolution",
        ],
        "provider_later": "Provider/Model Management covered in registry; module template later",
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "module_local_profile_non_runtime_boundary_matrix_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "module_local_profile_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "objectives": [
            "generate module_local_model_profile_standard_candidate",
            "verify module_local_model_profile_schema",
            "verify registry reference / stack / governance / I-O / quality / health / provider / fallback / midplatform",
            "verify Vision/OCR/TTS/ASR/Map/World/Memory-Emotion-Evolution templates",
            "generate module_internal_self_check_review_v1",
            "generate midplatform_interaction_check_review_v1",
            "verify dual validation mechanism: self-check ≠ interaction-check ≠ runtime ready",
            "no model select/download/invoke/benchmark",
        ],
        **meta,
    }

    planning_pass = input_ok
    planning_decision = {
        "decision_id": "module_local_model_profile_standardization_planning_decision_v1",
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "module_local_model_profile_standardization_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "standardization_planning_only": True,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        "dual_validation_non_claims": list(DUAL_VALIDATION_NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_pass": planning_pass,
        "standard_id": "module_local_model_profile_standard_v1",
        "registry_ref": REGISTRY_REF,
        "template_count": 7,
        "domain_coverage_count": len(DOMAIN_COVERAGE),
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "dual_validation_layers": 2,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    for tpl in (vision_template, ocr_template, tts_template, asr_template, map_template, world_template, mem_emo_evo_template):
        tpl.update(meta)

    return {
        "module_local_model_profile_standardization_planning_policy": policy,
        "model_profile_registry_input_review": registry_input_review,
        "governance_standard_reuse_review": governance_reuse,
        "module_local_model_profile_standard_definition": standard_definition,
        "module_local_model_profile_schema": profile_schema,
        "module_local_profile_to_registry_reference_policy": registry_ref_policy,
        "module_local_profile_capability_stack_binding_policy": stack_binding_policy,
        "module_local_profile_layered_governance_binding_policy": gov_binding_policy,
        "module_local_profile_input_output_binding_policy": io_binding_policy,
        "module_local_profile_quality_acceptance_binding_policy": quality_binding_policy,
        "module_local_profile_health_validation_whitebox_binding_policy": health_binding_policy,
        "module_local_profile_provider_runtime_boundary_policy": provider_boundary_policy,
        "module_local_profile_fallback_replacement_policy": fallback_policy,
        "module_local_profile_midplatform_handoff_policy": midplatform_handoff,
        "module_internal_self_check_policy": module_internal_self_check_policy,
        "midplatform_interaction_check_policy": midplatform_interaction_check_policy,
        "vision_module_local_model_profile_template": vision_template,
        "ocr_module_local_model_profile_template": ocr_template,
        "tts_module_local_model_profile_template": tts_template,
        "asr_module_local_model_profile_template": asr_template,
        "map_navigation_module_local_model_profile_template": map_template,
        "world_continuity_module_local_model_profile_template": world_template,
        "memory_emotion_evolution_module_local_model_profile_template": mem_emo_evo_template,
        "module_local_profile_domain_coverage_matrix": domain_matrix,
        "module_local_profile_non_runtime_boundary_matrix": boundary_matrix,
        "module_local_profile_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "module_local_model_profile_standardization_planning_decision": planning_decision,
        "summary": summary,
    }
