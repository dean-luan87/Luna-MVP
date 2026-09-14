# -*- coding: utf-8 -*-
"""Midplatform Backbone Definition Alignment v1 — 8-layer architecture definition only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_current_state_inventory_v1 import (
    FINAL_DECISION_GO as INVENTORY_FINAL_GO,
    PHASE_ID as INVENTORY_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.navigation_guidance_candidate_single_chain_trial_via_validation_factory_v1 import (
    FINAL_DECISION_GO as NAV_TRIAL_FINAL,
)
from capabilities.governance.ocr_mock_result_single_chain_trial_via_validation_factory_v1 import (
    FINAL_DECISION_GO as OCR_TRIAL_FINAL,
)
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_post_execution_review_v1 import (
    FINAL_DECISION_GO as VISION_TRIAL_FINAL,
)

PHASE_ID = "Phase-Midplatform-Backbone-Definition-Alignment-v1-001"
SCOPE = "midplatform_backbone_definition_alignment_only"
SOURCE_CHAIN = "midplatform_backbone_definition_alignment_v1"

UPSTREAM_FACTORY_PHASE = "Phase-Luna-Validation-Factory-Consolidation-v1-001"

FINAL_DECISION_GO = "MIDPLATFORM_8_LAYER_BACKBONE_DEFINITION_ALIGNED_READY_FOR_STRUCTURE_CLEANUP_PLANNING"
FINAL_DECISION_HOLD = "MIDPLATFORM_BACKBONE_DEFINITION_ALIGNMENT_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Structure-Cleanup-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Backbone-Definition-Alignment-Issue-Review-v1-001"

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_backbone_definition_alignment"
)

PRIMARY_LAYER = "capabilities/midplatform"
BRIDGE_LAYER = "capabilities/mid_platform"

CLOSED_CANDIDATES = (
    "visual_observation_candidate",
    "ocr_result_candidate",
    "navigation_guidance_candidate",
)

EIGHT_LAYERS: Tuple[Dict[str, Any], ...] = (
    {
        "layer_id": 1,
        "layer_key": "input_output",
        "name_en": "Input / Output Layer",
        "name_zh": "输入 / 输出层",
        "layer_type": "sequential_flow",
        "constitution_overlay": True,
    },
    {
        "layer_id": 2,
        "layer_key": "model_management",
        "name_en": "Model Management Layer",
        "name_zh": "模型管理层",
        "layer_type": "sequential_flow",
        "constitution_overlay": True,
    },
    {
        "layer_id": 3,
        "layer_key": "health_management",
        "name_en": "Health Management Layer",
        "name_zh": "健康管理层",
        "layer_type": "sequential_flow",
        "constitution_overlay": True,
        "drive_linkage": True,
    },
    {
        "layer_id": 4,
        "layer_key": "constitution",
        "name_en": "Constitution Layer",
        "name_zh": "宪法层",
        "layer_type": "global_horizontal_constraint",
        "not_sequential_only": True,
        "overlays_all_layers": True,
    },
    {
        "layer_id": 5,
        "layer_key": "task",
        "name_en": "Task Layer",
        "name_zh": "任务层",
        "layer_type": "sequential_flow",
        "constitution_overlay": True,
    },
    {
        "layer_id": 6,
        "layer_key": "drive",
        "name_en": "Drive Layer",
        "name_zh": "驱动层",
        "layer_type": "sequential_flow",
        "constitution_overlay": True,
        "health_linkage": True,
    },
    {
        "layer_id": 7,
        "layer_key": "local_memory",
        "name_en": "Local Memory Layer",
        "name_zh": "本地记忆层",
        "layer_type": "sequential_flow",
        "constitution_overlay": True,
    },
    {
        "layer_id": 8,
        "layer_key": "support",
        "name_en": "Support Layer",
        "name_zh": "支持层",
        "layer_type": "sequential_flow",
        "constitution_overlay": True,
        "local_memory_gate_required": True,
    },
)

NON_CLAIMS: Tuple[str, ...] = (
    "Backbone alignment GO ≠ directory merge executed",
    "Backbone alignment GO ≠ midplatform refactor executed",
    "8-layer definition ≠ runtime enabled",
    "Constitution overlay defined ≠ all modules migrated",
    "Drive linkage defined ≠ active drive execution enabled",
    "Support external_experience_candidate ≠ library write to local memory",
    "Model management contract ≠ model runtime invoked",
    "Input/output unified candidate protocol ≠ user-facing output allowed",
    "Prior 9-layer cleanup planning superseded for mapping purposes only",
    "Structure cleanup planning next ≠ cleanup execution",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "midplatform_backbone_definition_alignment_only": True,
        "file_move_executed_now": False,
        "file_rename_executed_now": False,
        "module_merge_executed_now": False,
        "module_delete_executed_now": False,
        "directory_merge_executed_now": False,
        "midplatform_refactor_executed_now": False,
        "midplatform_cleanup_executed_now": False,
        "runtime_enabled_now": False,
        "active_drive_execution_enabled_now": False,
        "task_state_committed_now": False,
        "task_manager_committed_now": False,
        "model_runtime_invoked_now": False,
        "live_camera_enabled_now": False,
        "ocr_provider_invoked_now": False,
        "navigation_action_triggered_now": False,
        "tts_invoked_now": False,
        "llm_invoked_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "library_write_executed_now": False,
        "hive_sync_executed_now": False,
        "scene_delta_generated_now": False,
        "user_facing_output_generated_now": False,
        "protected_asset_modified_now": False,
        "eval_out_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "task_response_candidate_chain_deferred_now": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _check_go(root: Path) -> bool:
    sm = _try_read_json(root / "summary.json") or {}
    vr = _try_read_json(root / "verifier_report.json") or {}
    return (vr.get("verifier") == "GO" and vr.get("passed") is True) or sm.get("boundary_ok") is True


def _validate_upstream(
    inventory_root: Path,
    factory_root: Path,
    vision_root: Path,
    ocr_root: Path,
    nav_root: Path,
) -> Tuple[List[str], Dict[str, Any]]:
    blockers: List[str] = []
    ctx: Dict[str, Any] = {}

    inv_sm = _try_read_json(inventory_root / "summary.json") or {}
    ctx["inventory"] = inv_sm
    if not _check_go(inventory_root):
        blockers.append("inventory verifier must be GO")
    if inv_sm.get("final_decision") != INVENTORY_FINAL_GO:
        blockers.append("inventory final_decision mismatch")
    if inv_sm.get("dual_directory_risk_previously_registered") != "medium":
        blockers.append("dual directory risk must be medium")

    for label, root, final in [
        ("factory", factory_root, None),
        ("vision", vision_root, VISION_TRIAL_FINAL),
        ("ocr", ocr_root, OCR_TRIAL_FINAL),
        ("nav", nav_root, NAV_TRIAL_FINAL),
    ]:
        if not _check_go(root):
            blockers.append(f"{label} verifier must be GO")
        sm = _try_read_json(root / "summary.json") or {}
        ctx[label] = sm
        if final and sm.get("final_decision") != final:
            blockers.append(f"{label} final_decision mismatch")

    return blockers, ctx


def run_midplatform_backbone_definition_alignment_v1(
    *,
    midplatform_current_state_inventory_root: str,
    luna_validation_factory_consolidation_root: str,
    vision_sample_frame_single_chain_controlled_trial_post_execution_review_root: str,
    ocr_mock_result_single_chain_trial_via_validation_factory_root: str,
    navigation_guidance_candidate_single_chain_trial_via_validation_factory_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    inventory_root = Path(midplatform_current_state_inventory_root).expanduser().resolve()
    factory_root = Path(luna_validation_factory_consolidation_root).expanduser().resolve()
    vision_root = Path(vision_sample_frame_single_chain_controlled_trial_post_execution_review_root).expanduser().resolve()
    ocr_root = Path(ocr_mock_result_single_chain_trial_via_validation_factory_root).expanduser().resolve()
    nav_root = Path(navigation_guidance_candidate_single_chain_trial_via_validation_factory_root).expanduser().resolve()

    blockers, ctx = _validate_upstream(inventory_root, factory_root, vision_root, ocr_root, nav_root)
    aligned = len(blockers) == 0
    meta = _boundary_meta()
    meta["upstream_inventory_root"] = str(inventory_root)
    meta["prior_planning_phase_superseded_for_mapping"] = (
        "Phase-Midplatform-Structure-Cleanup-Planning-v1-001-nine-layer-draft"
    )
    meta["alignment_output_root"] = str(output_root or DEFAULT_OUTPUT_ROOT)

    midplatform_definition = (
        "Luna Midplatform 是 Luna 个体系统的大脑干 / 中枢调度层，负责连接前端输入、模型能力、"
        "任务系统、健康监控、宪法约束、本地记忆、图书馆/蜂巢支持系统，并对信息流、模型流、"
        "任务流、驱动力、资源流、输出流进行统一调度、治理和裁决。"
    )

    architecture = {
        "architecture_id": "luna_midplatform_8_layer_architecture_v1",
        "version": "v1",
        "layer_count": 8,
        "constitution_layer_model": "global_horizontal_overlay",
        "constitution_not_sequential_only": True,
        "primary_code_layer": PRIMARY_LAYER,
        "runtime_bridge_layer": BRIDGE_LAYER,
        "midplatform_total_definition": midplatform_definition,
        "layers": list(EIGHT_LAYERS),
        "five_alignment_points": [
            {
                "point_id": 1,
                "title": "宪法层横向覆盖",
                "rule": "Constitution Layer overlays all layers; not only layer-4 sequential hop",
            },
            {
                "point_id": 2,
                "title": "健康管理层与驱动层联动",
                "rule": "health_warning / provider_failure / hardware_degradation → survival_drive_candidate",
            },
            {
                "point_id": 3,
                "title": "支持层不得直写本地记忆",
                "rule": "Library/Hive → external_experience_candidate → constitution + local_memory gate",
            },
            {
                "point_id": 4,
                "title": "模型管理层扩展职责",
                "rule": "Skill registry, capability spec, model status, switch policy, output standard",
            },
            {
                "point_id": 5,
                "title": "输入输出统一候选协议",
                "rule": "All I/O via candidate; no direct fact/action/speech",
            },
        ],
        **meta,
    }

    responsibility_matrix = {
        "matrix_id": "midplatform_layer_responsibility_matrix_v1",
        "rows": [
            {
                "layer": "input_output",
                "responsibilities": [
                    "frontend_input_normalization",
                    "information_integration",
                    "candidate_intake",
                    "source_chain_evidence_chain",
                    "output_arbitration",
                    "speech_task_navigation_guidance_output_candidates",
                ],
            },
            {
                "layer": "model_management",
                "responsibilities": [
                    "model_registry_versions",
                    "model_invocation_repair_switch",
                    "model_capability_spec",
                    "model_health_status",
                    "invocation_policy_degradation",
                    "skill_extension_entry",
                    "model_output_standard_to_candidate",
                ],
                "not_only": "model_invoker",
            },
            {
                "layer": "health_management",
                "responsibilities": [
                    "software_health",
                    "hardware_health_reserved",
                    "system_monitor_robustness",
                    "resource_allocation",
                    "failure_handling_candidates",
                    "drive_layer_signal_emission",
                ],
                "subdomains": ["software", "hardware", "system_monitor"],
            },
            {
                "layer": "constitution",
                "responsibilities": [
                    "spacetime_governance",
                    "information_constraints",
                    "gate_management",
                    "safety_survival_constitution",
                    "fact_action_output_memory_model_boundaries",
                ],
                "overlay": "all_layers",
            },
            {
                "layer": "task",
                "responsibilities": [
                    "passive_task_orchestration",
                    "task_state_lifecycle",
                    "clarification_pause_resume_cancel",
                    "task_perception_judgment",
                    "drive_candidate_to_task_candidate",
                ],
            },
            {
                "layer": "drive",
                "responsibilities": [
                    "luna_initiative_source",
                    "survival_drive",
                    "task_completion_drive",
                    "learning_drive",
                    "emotion_relationship_drive",
                    "exploration_drive_defined_not_enabled",
                ],
            },
            {
                "layer": "local_memory",
                "responsibilities": [
                    "local_memory_user_profile",
                    "communication_records",
                    "local_world_model_experience",
                    "routes_family_preferences",
                ],
            },
            {
                "layer": "support",
                "responsibilities": [
                    "library_connection",
                    "hive_connection",
                    "external_experience_sync",
                    "safety_tech_rule_candidates",
                ],
            },
        ],
        **meta,
    }

    authority_matrix = {
        "matrix_id": "midplatform_layer_authority_matrix_v1",
        "precedence": [
            "constitution_layer_global",
            "safety_survival_over_task_completion",
            "safety_survival_over_model_output",
            "safety_survival_over_user_instruction",
            "safety_survival_over_emotion_expression",
        ],
        "constitution_overlays": [l["layer_key"] for l in EIGHT_LAYERS if l.get("constitution_overlay") or l.get("overlays_all_layers")],
        "write_authority": {
            "fact_write": "constitution_gate_only",
            "memory_write": "constitution_gate + local_memory_gate + source_validation",
            "library_hive_to_local": "forbidden_direct; external_experience_candidate_only",
            "user_facing_output": "input_output_arbitration_after_constitution",
            "runtime_action": "constitution + health + model_management_boundary",
        },
        **meta,
    }

    old_new_mapping = {
        "mapping_id": "midplatform_old_new_layer_mapping_v1",
        "prior_nine_layer_cleanup_planning": "Phase-Midplatform-Structure-Cleanup-Planning-v1-001-nine-layer-draft",
        "superseded_for_engineering_mapping": True,
        "mappings": [
            {"old": "Candidate Intake", "new_layers": ["input_output"]},
            {"old": "Evidence Governance", "new_layers": ["input_output", "constitution"]},
            {"old": "Task State", "new_layers": ["task"]},
            {"old": "Perception Orchestration", "new_layers": ["task", "model_management"]},
            {"old": "Guidance Candidate Queue", "new_layers": ["input_output", "task"]},
            {"old": "Safety / Survival Gate", "new_layers": ["constitution", "health_management", "drive"]},
            {"old": "Runtime Boundary", "new_layers": ["constitution", "health_management", "model_management"]},
            {"old": "Output Arbitration", "new_layers": ["input_output"]},
            {"old": "Memory / World / Library Access", "new_layers": ["local_memory", "support"]},
        ],
        "directory_roles_unchanged": {
            "primary": PRIMARY_LAYER,
            "bridge": BRIDGE_LAYER,
            "safe_to_merge": False,
        },
        **meta,
    }

    io_contract = {
        "contract_id": "input_output_layer_contract_v1",
        "unified_candidate_protocol": True,
        "rules": [
            "all_inputs_standardized_to_candidate_first",
            "all_outputs_generated_as_candidate_first",
            "no_direct_fact_write",
            "no_direct_runtime_action",
            "no_direct_user_facing_output",
            "no_direct_tts",
        ],
        "supported_output_candidates": [
            "speech_response_candidate",
            "task_response_candidate",
            "navigation_guidance_candidate",
            "routing_decision_candidate",
            "blocked_or_allowed_decision",
        ],
        "closed_validation_factory_inputs": list(CLOSED_CANDIDATES),
        **meta,
    }

    model_contract = {
        "contract_id": "model_management_layer_contract_v1",
        "beyond_invoker": True,
        "responsibilities": {
            "registry": ["model_id", "version", "provider_type"],
            "skill_registry": "skill_id, skill_capability_spec, skill_boundary",
            "capability_spec": "per-model capability document",
            "health_status": "healthy, degraded, unavailable",
            "switch_policy": "degradation, fallback_model, constitution_required",
            "output_standard": "all_model_outputs → candidate contract",
        },
        "model_families": [
            "emotion",
            "perspective",
            "ocr",
            "voice",
            "face_recognition",
            "scan",
            "future_skill_provider",
        ],
        "constraints": [
            "must_not_bypass_constitution",
            "runtime_boundary_required",
            "no_direct_fact_write",
        ],
        **meta,
    }

    health_contract = {
        "contract_id": "health_management_layer_contract_v1",
        "domains": {
            "software": ["module_health", "provider_health", "gate_health", "runtime_chain_health"],
            "hardware": ["camera", "microphone", "speaker", "battery", "compute", "temperature", "storage", "network", "sensors"],
            "system_monitor": ["resource_allocation", "robustness", "fault_recovery_candidates"],
        },
        "drive_linkage": {
            "enabled_in_definition_only": True,
            "triggers": [
                {"signal": "health_warning", "candidate": "survival_drive_candidate"},
                {"signal": "provider_failure", "candidate": "fallback_drive_candidate"},
                {"signal": "hardware_degradation", "candidate": "model_degradation_task_candidate"},
                {"signal": "system_anomaly", "candidate": "survival_drive_candidate"},
                {"signal": "model_failure", "candidate": "fallback_drive_candidate"},
            ],
        },
        **meta,
    }

    constitution_contract = {
        "contract_id": "constitution_layer_contract_v1",
        "layer_model": "global_horizontal_constraint",
        "overlays_all_layers": True,
        "not_ordered_as_normal_layer_only": True,
        "hard_constraints": [
            "candidate ≠ fact",
            "map_hint ≠ map_fact",
            "navigation_guidance_candidate ≠ navigation_action",
            "speech_response_candidate ≠ TTS",
            "memory_candidate ≠ memory_write",
            "library_experience ≠ local_fact",
            "user_instruction_cannot_override_safety_gate",
        ],
        "gate_domains": [
            "fact_write",
            "action",
            "output",
            "memory_write",
            "model_invocation",
            "library_hive_ingest",
        ],
        **meta,
    }

    task_contract = {
        "contract_id": "task_layer_contract_v1",
        "passive_tasks": ["user_initiated", "external_input", "explicit_request"],
        "active_tasks": ["from_drive_layer_drive_candidate"],
        "lifecycle": [
            "idle",
            "task_candidate_created",
            "waiting_for_clarification",
            "active_candidate",
            "paused_candidate",
            "cancelled_candidate",
            "completed_candidate",
            "failed_candidate",
            "fallback_required",
        ],
        "constraints": [
            "task_state_candidate ≠ task_commit",
            "task_response_candidate ≠ user_output",
            "task_manager_runtime_default_off",
        ],
        **meta,
    }

    drive_contract = {
        "contract_id": "drive_layer_contract_v1",
        "drive_classes": {
            "survival": ["safety", "avoidance", "degradation", "help_seeking", "offline_minimum", "failure_alternate_path"],
            "task_completion": ["continue_task", "request_observation", "request_clarification", "task_observation_requirement_candidate"],
            "learning": ["pattern_candidate", "experience_candidate", "memory_write_candidate_no_direct_write"],
            "emotion_relationship": ["care_candidate", "emotion_response_candidate", "relationship_maintenance_candidate"],
            "exploration": ["defined_not_enabled"],
        },
        "constraints": [
            "active_drive_execution_enabled=false",
            "drive_candidate cannot execute action",
            "drive_candidate cannot user_output",
            "drive_candidate cannot direct_memory_write",
            "must_enter_task_layer_orchestration",
            "must_obey_constitution",
            "must_read_health_management_state",
        ],
        **meta,
    }

    local_memory_contract = {
        "contract_id": "local_memory_layer_contract_v1",
        "domains": [
            "local_memory",
            "user_profile",
            "communication_records",
            "local_world_model",
            "local_experience",
            "common_routes",
            "family_members",
            "preferences",
        ],
        "readonly_first": True,
        "write_blocked_by_default": True,
        "write_path": ["constitution_gate", "memory_gate", "source_validation", "policy_or_user_confirm"],
        **meta,
    }

    support_contract = {
        "contract_id": "support_layer_contract_v1",
        "external_sources": ["library", "hive"],
        "output_type": "external_experience_candidate",
        "forbidden": [
            "direct_local_memory_overwrite",
            "direct_worldmodel_write",
            "bypass_privacy",
            "bypass_constitution",
        ],
        "required_gates": ["constitution_layer", "local_memory_layer"],
        **meta,
    }

    active_passive = {
        "relation_id": "active_passive_task_relation_v1",
        "passive_entry": "input_output → task_layer",
        "active_entry": "health_management → drive_layer → task_layer",
        "drive_to_task": "drive_candidate → task_candidate (no direct commit)",
        **meta,
    }

    survival_drive = {
        "contract_id": "survival_drive_candidate_contract_v1",
        "triggers_from_health": [
            "health_warning",
            "provider_failure",
            "hardware_degradation",
            "system_anomaly",
            "model_failure",
        ],
        "candidate_type": "survival_drive_candidate",
        "downstream": "task_layer_task_candidate",
        "execution_blocked": True,
        **meta,
    }

    flow_examples = {
        "examples_id": "midplatform_cross_layer_flow_examples_v1",
        "flows": [
            {
                "flow_id": "passive_task",
                "steps": [
                    "User input",
                    "Input Layer",
                    "Task Layer",
                    "Model Management Layer",
                    "Candidate Output",
                    "Constitution Gate (overlay)",
                    "Output Arbitration",
                ],
            },
            {
                "flow_id": "survival_drive",
                "steps": [
                    "Health warning / safety uncertainty",
                    "Health Management Layer",
                    "Drive Layer survival_drive_candidate",
                    "Task Layer task_candidate",
                    "Constitution Gate",
                    "Output Arbitration candidate / fallback",
                ],
            },
            {
                "flow_id": "perception_candidate",
                "steps": [
                    "Vision / OCR / Navigation candidate (Validation Factory closed)",
                    "Input Layer",
                    "Evidence Governance",
                    "Task Layer / Drive Layer",
                    "Safety Gate (constitution + health)",
                    "Output Arbitration",
                ],
            },
            {
                "flow_id": "memory_readonly",
                "steps": [
                    "Task need context",
                    "Local Memory readonly lookup candidate",
                    "Evidence Governance",
                    "Task Layer",
                    "Output candidate",
                ],
            },
            {
                "flow_id": "library_hive_support",
                "steps": [
                    "Support Layer external_experience_candidate",
                    "Constitution Gate",
                    "Local Memory candidate (not direct write)",
                    "Task / Model Management reference",
                ],
            },
        ],
        **meta,
    }

    missing_concerns = {
        "register_id": "midplatform_missing_concern_register_v1",
        "concerns": [
            {"id": "ttl_staleness", "owner": "input_output + constitution"},
            {"id": "candidate_priority", "owner": "task + input_output"},
            {"id": "interrupt_user_interruption", "owner": "task + constitution"},
            {"id": "fallback_policy", "owner": "constitution + drive"},
            {"id": "candidate_conflict_resolution", "owner": "input_output + task"},
            {"id": "audit_trace", "owner": "constitution + input_output"},
            {"id": "resource_budget", "owner": "health_management"},
            {"id": "privacy_local_sovereignty", "owner": "constitution + local_memory"},
            {"id": "model_capability_registry", "owner": "model_management"},
            {"id": "skill_extension_boundary", "owner": "model_management + constitution"},
            {"id": "memory_write_gate", "owner": "local_memory + constitution"},
            {"id": "library_hive_sync_gate", "owner": "support + constitution"},
            {"id": "survival_minimum_operating_mode", "owner": "drive + health_management"},
        ],
        **meta,
    }

    input_review = {
        "review_id": "midplatform_inventory_input_review_v1",
        "inventory_root": str(inventory_root),
        "review_pass": aligned,
        "blockers": blockers,
        "confirmed": {
            "inventory_go": aligned,
            "factory_go": _check_go(factory_root),
            "three_candidate_chains_closed": True,
            "task_response_deferred": True,
            "dual_directory_medium": True,
        },
        **meta,
    }

    decision = {
        "decision_id": "midplatform_backbone_definition_alignment_decision_v1",
        "boundary_ok": aligned,
        "final_decision": FINAL_DECISION_GO if aligned else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if aligned else NEXT_PHASE_HOLD,
        "architecture_model": "8_layer_with_constitution_horizontal_overlay",
        "blockers": blockers,
        **meta,
    }

    policy = {
        "policy_id": "midplatform_backbone_definition_policy_v1",
        "scope": SCOPE,
        "approach": "architecture_definition_alignment_only",
        **decision,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": aligned,
        "violations": blockers,
        "final_decision": decision["final_decision"],
        "recommended_next_phase": decision["recommended_next_phase"],
        "layer_count": 8,
        "constitution_overlay_model": "global_horizontal",
        **meta,
    }

    return {
        "midplatform_backbone_definition_policy": policy,
        "midplatform_inventory_input_review": input_review,
        "luna_midplatform_8_layer_architecture": architecture,
        "midplatform_layer_responsibility_matrix": responsibility_matrix,
        "midplatform_layer_authority_matrix": authority_matrix,
        "midplatform_old_new_layer_mapping": old_new_mapping,
        "input_output_layer_contract": io_contract,
        "model_management_layer_contract": model_contract,
        "health_management_layer_contract": health_contract,
        "constitution_layer_contract": constitution_contract,
        "task_layer_contract": task_contract,
        "drive_layer_contract": drive_contract,
        "local_memory_layer_contract": local_memory_contract,
        "support_layer_contract": support_contract,
        "active_passive_task_relation": active_passive,
        "survival_drive_candidate_contract": survival_drive,
        "midplatform_cross_layer_flow_examples": flow_examples,
        "midplatform_missing_concern_register": missing_concerns,
        "midplatform_backbone_definition_non_claims_register": {
            "register_id": "midplatform_backbone_definition_non_claims_register_v1",
            "non_claims": list(NON_CLAIMS),
            **meta,
        },
        "midplatform_backbone_definition_alignment_decision": decision,
        "summary": summary,
    }
