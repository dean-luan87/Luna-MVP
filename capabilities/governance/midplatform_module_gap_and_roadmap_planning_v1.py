# -*- coding: utf-8 -*-
"""Midplatform Module Gap and Roadmap Planning v1 — gap/roadmap only, no implementation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_backbone_definition_alignment_v1 import (
    FINAL_DECISION_GO as ALIGNMENT_FINAL_GO,
    PHASE_ID as ALIGNMENT_PHASE,
)
from capabilities.governance.midplatform_current_state_inventory_v1 import (
    FINAL_DECISION_GO as INVENTORY_FINAL_GO,
    PHASE_ID as INVENTORY_PHASE,
)
from capabilities.governance.midplatform_structure_cleanup_planning_v1 import (
    FINAL_DECISION_GO as CLEANUP_PLANNING_FINAL,
    PHASE_ID as CLEANUP_PLANNING_PHASE,
    EIGHT_LAYER_KEYS,
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

PHASE_ID = "Phase-Midplatform-Module-Gap-and-Roadmap-Planning-v1-001"
SCOPE = "midplatform_module_gap_and_roadmap_planning_only"
SOURCE_CHAIN = "midplatform_module_gap_and_roadmap_planning_v1"

UPSTREAM_FACTORY_PHASE = "Phase-Luna-Validation-Factory-Consolidation-v1-001"

FINAL_DECISION_GO = "MIDPLATFORM_MODULE_GAP_AND_ROADMAP_PLANNING_READY_FOR_STRUCTURE_CLEANUP_PLANNING"
FINAL_DECISION_HOLD = "MIDPLATFORM_MODULE_GAP_AND_ROADMAP_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Structure-Cleanup-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Module-Gap-and-Roadmap-Issue-Review-v1-001"

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_module_gap_and_roadmap_planning"
)

CLOSED_CANDIDATES = (
    "visual_observation_candidate",
    "ocr_result_candidate",
    "navigation_guidance_candidate",
)

P0_MODULES: Tuple[str, ...] = (
    "unified_candidate_intake_contract",
    "candidate_flow_contract",
    "guidance_candidate_queue_contract",
    "output_arbitration_contract",
    "constitution_overlay_registry",
    "runtime_boundary_matrix",
    "task_state_candidate_contract",
    "midplatform_minimal_backbone_dryrun_runner_verifier",
)

P1_MODULES: Tuple[str, ...] = (
    "task_lifecycle_state_machine_contract",
    "pause_resume_cancel_contract",
    "health_signal_contract",
    "survival_drive_candidate_contract",
    "health_to_drive_signal_contract",
    "model_registry_contract",
    "model_health_and_switching_policy",
)

P2_MODULES: Tuple[str, ...] = (
    "skill_registry_contract",
    "model_output_standard_contract",
    "model_provider_fallback_policy",
    "model_version_management_contract",
)

P3_MODULES: Tuple[str, ...] = (
    "memory_readonly_lookup_contract",
    "world_model_readonly_candidate_contract",
    "map_readonly_context_contract",
    "external_experience_candidate_contract",
    "library_hive_sync_gate",
)

P4_MODULES: Tuple[str, ...] = (
    "emotion_drive_candidate_contract",
    "relationship_drive_candidate_contract",
    "exploration_drive_candidate_contract",
    "emotional_output_arbitration_policy",
)

LAYER_CHECKS: Dict[str, Dict[str, Any]] = {
    "input_output": {
        "existing_capabilities": [
            "ocr_evidence_readonly_ingest_candidate_v0",
            "vision_recognition_evidence_readonly_ingest_candidate_v0",
            "navigation_guidance_to_speech_candidate_adapter_v1",
            "voice_output_plane_adapter_for_guidance_v1",
            "safety_task_arbitration_policy_v1",
            "cross_modal_* ingest paths",
        ],
        "gaps": [
            "unified_candidate_intake_contract",
            "guidance_candidate_queue_contract",
            "output_arbitration_contract",
        ],
    },
    "model_management": {
        "existing_capabilities": [
            "ocr_activation_governance_policy_v1",
            "hardware_profile_capability_registry_v1",
            "ocr_source_validation_dryrun_v1",
        ],
        "gaps": [
            "model_registry_contract",
            "skill_registry_contract",
            "model_health_and_switching_policy",
        ],
        "note": "model optimization deferred until midplatform stable",
    },
    "health_management": {
        "existing_capabilities": [
            "hardware_camera_runtime_adapter_stub_v1",
            "hardware_camera_control_contract_v1",
            "minimal_runtime_integration_*",
        ],
        "gaps": [
            "health_signal_contract",
            "system_monitor_to_drive_candidate_contract",
            "hardware_capability_registry integration",
        ],
    },
    "constitution": {
        "existing_capabilities": [
            "safety_task_arbitration_policy_v1",
            "ocr_ttl_gate_v1",
            "source_validation_v2_after_ep_v3",
            "migration_governance_development_constraints_v1",
        ],
        "gaps": [
            "constitution_overlay_registry",
            "unified_gate_manager_contract",
            "ttl_staleness_policy",
            "memory_library_hive_gate_contract",
        ],
    },
    "task": {
        "existing_capabilities": [
            "task_manager_contract_v1",
            "midplatform_task_state_runtime_dryrun_v1",
            "task_manager_runtime_dryrun_v1",
            "user_clarification_*",
            "task_observation_request_contract_v1",
        ],
        "gaps": [
            "task_state_candidate_contract",
            "task_lifecycle_state_machine_contract",
            "pause_resume_cancel_contract",
            "task_response_candidate_chain",
        ],
    },
    "drive": {
        "existing_capabilities": [],
        "gaps": [
            "drive_candidate_contract",
            "survival_drive_candidate_contract",
            "health_to_drive_signal_contract",
            "drive_to_task_candidate_contract",
        ],
        "note": "contracts only; active_drive_execution_enabled=false",
    },
    "local_memory": {
        "existing_capabilities": [
            "worldmodel_lookup_for_reading_framework_v1",
            "confirmed_text_evidence_memory_governance_contract_v1",
        ],
        "gaps": [
            "memory_readonly_lookup_contract",
            "memory_write_gate_contract",
            "candidate_to_memory_pollution_guard",
        ],
    },
    "support": {
        "existing_capabilities": [],
        "gaps": [
            "external_experience_candidate_contract",
            "library_hive_sync_gate",
            "local_experience_extraction_contract",
        ],
        "status": "deferred_all",
    },
}

NON_CLAIMS: Tuple[str, ...] = (
    "Gap Planning GO ≠ modules implemented",
    "Roadmap GO ≠ runtime enabled",
    "P0 module listed ≠ module created",
    "Model layer handoff defined ≠ model optimization started",
    "Memory / Library / Map deferred ≠ abandoned",
    "Task response deferred ≠ task layer abandoned",
    "Candidate contract planned ≠ candidate flow executed",
    "Backbone roadmap defined ≠ backbone dryrun executed",
    "Midplatform stable-first ≠ model-layer-first",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "midplatform_module_gap_and_roadmap_planning_only": True,
        "midplatform_stable_before_model_optimization": True,
        "module_implementation_started_now": False,
        "new_module_created_now": False,
        "file_move_executed_now": False,
        "file_rename_executed_now": False,
        "module_merge_executed_now": False,
        "module_delete_executed_now": False,
        "directory_merge_executed_now": False,
        "import_rewrite_executed_now": False,
        "runtime_enabled_now": False,
        "active_drive_execution_enabled_now": False,
        "task_state_committed_now": False,
        "task_manager_committed_now": False,
        "model_runtime_invoked_now": False,
        "model_layer_optimization_started_now": False,
        "live_camera_enabled_now": False,
        "ocr_provider_invoked_now": False,
        "navigation_action_triggered_now": False,
        "tts_invoked_now": False,
        "llm_invoked_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "library_write_executed_now": False,
        "hive_sync_executed_now": False,
        "user_facing_output_generated_now": False,
        "protected_asset_modified_now": False,
        "eval_out_modified_now": False,
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
    if not root.is_dir():
        return False
    sm = _try_read_json(root / "summary.json") or {}
    vr = _try_read_json(root / "verifier_report.json") or {}
    return (vr.get("verifier") == "GO" and vr.get("passed") is True) or sm.get("boundary_ok") is True


def _validate_upstream(
    inventory_root: Path,
    alignment_root: Path,
    factory_root: Path,
    vision_root: Path,
    ocr_root: Path,
    nav_root: Path,
    cleanup_root: Optional[Path],
) -> Tuple[List[str], Dict[str, Any]]:
    blockers: List[str] = []
    ctx: Dict[str, Any] = {}

    for label, root, phase, final in [
        ("inventory", inventory_root, INVENTORY_PHASE, INVENTORY_FINAL_GO),
        ("alignment", alignment_root, ALIGNMENT_PHASE, ALIGNMENT_FINAL_GO),
        ("factory", factory_root, UPSTREAM_FACTORY_PHASE, None),
        ("vision", vision_root, None, VISION_TRIAL_FINAL),
        ("ocr", ocr_root, None, OCR_TRIAL_FINAL),
        ("nav", nav_root, None, NAV_TRIAL_FINAL),
    ]:
        if not _check_go(root):
            blockers.append(f"{label} verifier must be GO")
        sm = _try_read_json(root / "summary.json") or {}
        ctx[f"{label}_summary"] = sm
        if phase and sm.get("phase") != phase:
            blockers.append(f"{label} phase mismatch")
        if final and sm.get("final_decision") != final:
            blockers.append(f"{label} final_decision mismatch")

    if cleanup_root and cleanup_root.is_dir():
        ctx["cleanup_planning_present"] = _check_go(cleanup_root)
        ctx["cleanup_summary"] = _try_read_json(cleanup_root / "summary.json") or {}
    else:
        ctx["cleanup_planning_present"] = False

    return blockers, ctx


def _build_completeness_matrix(
    mapping_counts: Dict[str, int],
    layer_plans: Dict[str, Any],
) -> Dict[str, Any]:
    rows = []
    for layer_key in EIGHT_LAYER_KEYS:
        check = LAYER_CHECKS.get(layer_key, {})
        module_count = mapping_counts.get(layer_key, 0)
        gaps = check.get("gaps", [])
        if layer_key == "support" or check.get("status") == "deferred_all":
            status = "deferred"
        elif module_count >= 5 and len(gaps) <= 2:
            status = "partially_sufficient_needs_contract"
        elif module_count >= 1:
            status = "reuse_with_contract_gaps"
        else:
            status = "needs_new_module_or_contract"
        rows.append(
            {
                "layer_key": layer_key,
                "assigned_module_count": module_count,
                "completeness_status": status,
                "existing_capabilities": check.get("existing_capabilities", []),
                "must_fill_gaps": gaps,
                "layer_plan_gaps": (layer_plans.get(layer_key) or {}).get("identified_gaps", []),
            }
        )
    return {
        "matrix_id": "eight_layer_module_completeness_matrix_v1",
        "rows": rows,
        "summary": {
            "sufficient_with_contract": sum(1 for r in rows if "sufficient" in r["completeness_status"]),
            "needs_contract": sum(1 for r in rows if "contract" in r["completeness_status"]),
            "deferred": sum(1 for r in rows if r["completeness_status"] == "deferred"),
        },
    }


def _reuse_matrix(modules: List[Dict[str, Any]]) -> Dict[str, Any]:
    reuse = []
    for m in modules:
        stem = m.get("module_stem", "")
        if m.get("has_runner") and m.get("has_verifier"):
            verdict = "reuse_as_is"
        elif m.get("has_runner") or m.get("status") in ("implemented", "dryrun_only"):
            verdict = "reuse_with_contract_wrap"
        elif m.get("status") == "governance_only":
            verdict = "reuse_policy_only"
        elif m.get("status") == "stub_placeholder":
            verdict = "stub_keep_deferred"
        else:
            verdict = "review_before_reuse"
        reuse.append(
            {
                "path": m.get("path"),
                "module_stem": stem,
                "status": m.get("status"),
                "reuse_verdict": verdict,
                "primary_layer": m.get("primary_eight_layer"),
            }
        )
    counts = {}
    for r in reuse:
        counts[r["reuse_verdict"]] = counts.get(r["reuse_verdict"], 0) + 1
    return {
        "matrix_id": "existing_module_reuse_matrix_v1",
        "modules_total": len(reuse),
        "reuse_verdict_counts": counts,
        "principle": "prefer_reuse_over_new_module",
        "rows_sample": reuse[:40],
        "rows": reuse,
    }


def run_midplatform_module_gap_and_roadmap_planning_v1(
    *,
    midplatform_current_state_inventory_root: str,
    midplatform_backbone_definition_alignment_root: str,
    luna_validation_factory_consolidation_root: str,
    vision_sample_frame_single_chain_controlled_trial_post_execution_review_root: str,
    ocr_mock_result_single_chain_trial_via_validation_factory_root: str,
    navigation_guidance_candidate_single_chain_trial_via_validation_factory_root: str,
    midplatform_structure_cleanup_planning_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    inventory_root = Path(midplatform_current_state_inventory_root).expanduser().resolve()
    alignment_root = Path(midplatform_backbone_definition_alignment_root).expanduser().resolve()
    factory_root = Path(luna_validation_factory_consolidation_root).expanduser().resolve()
    vision_root = Path(vision_sample_frame_single_chain_controlled_trial_post_execution_review_root).expanduser().resolve()
    ocr_root = Path(ocr_mock_result_single_chain_trial_via_validation_factory_root).expanduser().resolve()
    nav_root = Path(navigation_guidance_candidate_single_chain_trial_via_validation_factory_root).expanduser().resolve()
    cleanup_root = (
        Path(midplatform_structure_cleanup_planning_root).expanduser().resolve()
        if midplatform_structure_cleanup_planning_root
        else None
    )

    blockers, ctx = _validate_upstream(
        inventory_root, alignment_root, factory_root, vision_root, ocr_root, nav_root, cleanup_root
    )
    planning_ok = len(blockers) == 0
    meta = _boundary_meta()

    inv_modules = (_try_read_json(inventory_root / "midplatform_module_inventory_v1.json") or {}).get("modules") or []
    mapping_data = {}
    layer_plans: Dict[str, Any] = {}
    if cleanup_root and cleanup_root.is_dir():
        mapping_data = _try_read_json(cleanup_root / "midplatform_8_layer_module_mapping_v1.json") or {}
        for lk in EIGHT_LAYER_KEYS:
            layer_plans[lk] = _try_read_json(cleanup_root / f"midplatform_{lk}_layer_cleanup_plan_v1.json") or {}

    mapping_counts = mapping_data.get("layer_assignment_counts") or {}
    if cleanup_root and _check_go(cleanup_root):
        meta["structure_cleanup_planning_consumed"] = True
        meta["structure_cleanup_planning_final"] = ctx.get("cleanup_summary", {}).get("final_decision")
    else:
        meta["structure_cleanup_planning_consumed"] = False

    completeness = _build_completeness_matrix(mapping_counts, layer_plans)
    completeness.update(meta)

    reuse = _reuse_matrix(
        [
            {
                **m,
                "primary_eight_layer": next(
                    (
                        x.get("primary_eight_layer")
                        for x in (mapping_data.get("modules") or [])
                        if x.get("path") == m.get("path")
                    ),
                    None,
                ),
            }
            for m in inv_modules
        ]
    )
    reuse.update(meta)

    must_fill = {
        "register_id": "must_fill_module_gap_register_v1",
        "priority": "P0",
        "modules": list(P0_MODULES),
        "rationale": "Required before midplatform minimal backbone can consume VOC/OCR/Nav candidates",
        **meta,
    }

    optional_future = {
        "register_id": "optional_future_module_register_v1",
        "P1": list(P1_MODULES),
        "P2": list(P2_MODULES),
        "P3": list(P3_MODULES),
        "P4": list(P4_MODULES),
        "implementation_policy": "P1/P2 register only; P3/P4 deferred",
        **meta,
    }

    priority_matrix = {
        "matrix_id": "module_addition_priority_matrix_v1",
        "priorities": {
            "P0": {"modules": list(P0_MODULES), "implement_now": False, "plan_now": True},
            "P1": {"modules": list(P1_MODULES), "implement_now": False, "plan_now": True},
            "P2": {"modules": list(P2_MODULES), "implement_now": False, "plan_now": True, "note": "before model optimization"},
            "P3": {"modules": list(P3_MODULES), "implement_now": False, "deferred": True},
            "P4": {"modules": list(P4_MODULES), "implement_now": False, "deferred": True},
        },
        **meta,
    }

    stabilization_roadmap = {
        "roadmap_id": "midplatform_minimal_stabilization_roadmap_v1",
        "sequence": [
            {"step": 1, "phase": PHASE_ID, "status": "current"},
            {"step": 2, "phase": CLEANUP_PLANNING_PHASE, "status": "completed_or_rerun_with_gap_context"},
            {"step": 3, "phase": "Phase-Midplatform-Minimal-Backbone-DryRun-v1-001", "status": "next_after_cleanup"},
            {"step": 4, "phase": "Phase-Midplatform-Minimal-Backbone-Post-DryRun-Review-v1-001", "status": "planned"},
            {"step": 5, "phase": "Phase-Task-Response-Candidate-Single-Chain-Trial-Via-Midplatform-v1-001", "status": "deferred"},
            {"step": 6, "phase": "Phase-Model-Management-Layer-Recovery-Planning-v1-001", "status": "after_backbone"},
            {"step": 7, "phase": "Phase-Model-Registry-Health-Switching-DryRun-v1-001", "status": "after_recovery_planning"},
            {"step": 8, "phase": "Vision/OCR/Voice model optimization", "status": "last"},
        ],
        "principle": "stabilize_midplatform_before_model_optimization",
        **meta,
    }

    model_handoff = {
        "plan_id": "model_layer_optimization_handoff_plan_v1",
        "model_optimization_is_next_step": False,
        "entry_conditions": [
            "Midplatform Minimal Backbone DryRun verifier=GO",
            "candidate_intake consumable",
            "evidence_governance consumable",
            "guidance_queue consumable",
            "output_arbitration consumable",
            "runtime_boundary_matrix GO",
            "constitution_overlay_mapping GO",
            "NoRuntimeBoundaryAudit reusable",
            "model_output_contract attaches to candidate protocol",
        ],
        "midplatform_must_provide": [
            "model_registry",
            "invocation_policy",
            "degradation",
            "health_state",
            "output_contract",
            "skill_extension_boundary",
        ],
        "blocked_until": "backbone_dryrun_GO",
        **meta,
    }

    task_decision = {
        "decision_id": "task_response_candidate_defer_or_resume_decision_v1",
        "task_response_candidate_now": False,
        "task_response_candidate_deferred_until": "after_midplatform_minimal_backbone_dryrun",
        "reason": (
            "Task response belongs to output/task layer; attach after "
            "candidate intake / queue / arbitration are defined and dryrun-validated"
        ),
        **meta,
    }

    memory_policy = {
        "policy_id": "memory_library_map_defer_policy_v1",
        "memory_layer_implementation_now": False,
        "library_support_implementation_now": False,
        "map_write_or_strong_anchor_now": False,
        "only_readonly_contract_planning_allowed_later": True,
        "support_layer_status": "deferred_all",
        **meta,
    }

    input_review = {
        "review_id": "midplatform_input_review_v1",
        "roots": {
            "inventory": str(inventory_root),
            "alignment": str(alignment_root),
            "cleanup_planning": str(cleanup_root) if cleanup_root else None,
        },
        "review_pass": planning_ok,
        "blockers": blockers,
        "three_questions": {
            "what_is_sufficient": "reuse_as_is + reuse_with_contract_wrap modules per reuse matrix",
            "what_must_fill": "P0 must_fill_module_gap_register",
            "addition_rhythm": "module_addition_priority_matrix P0→P4",
        },
        **meta,
    }

    decision = {
        "decision_id": "midplatform_module_gap_roadmap_decision_v1",
        "boundary_ok": planning_ok,
        "final_decision": FINAL_DECISION_GO if planning_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_ok else NEXT_PHASE_HOLD,
        "blockers": blockers,
        **meta,
    }

    policy = {
        "policy_id": "midplatform_module_gap_roadmap_policy_v1",
        "scope": SCOPE,
        "planning_principles": [
            "stabilize_midplatform_skeleton_first",
            "reuse_existing_modules",
            "P0_contracts_only_for_now",
            "P1_P2_register_not_implement",
            "runtime_task_output_memory_write_off",
            "model_optimization_after_backbone_dryrun",
        ],
        **decision,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": planning_ok,
        "violations": blockers,
        "final_decision": decision["final_decision"],
        "recommended_next_phase": decision["recommended_next_phase"],
        "p0_gap_count": len(P0_MODULES),
        "modules_in_inventory": len(inv_modules),
        **meta,
    }

    return {
        "midplatform_module_gap_roadmap_policy": policy,
        "midplatform_input_review": input_review,
        "eight_layer_module_completeness_matrix": completeness,
        "existing_module_reuse_matrix": reuse,
        "must_fill_module_gap_register": must_fill,
        "optional_future_module_register": optional_future,
        "module_addition_priority_matrix": priority_matrix,
        "midplatform_minimal_stabilization_roadmap": stabilization_roadmap,
        "model_layer_optimization_handoff_plan": model_handoff,
        "task_response_candidate_defer_or_resume_decision": task_decision,
        "memory_library_map_defer_policy": memory_policy,
        "midplatform_module_gap_non_claims_register": {
            "register_id": "midplatform_module_gap_non_claims_register_v1",
            "non_claims": list(NON_CLAIMS),
            **meta,
        },
        "midplatform_module_gap_roadmap_decision": decision,
        "summary": summary,
    }
