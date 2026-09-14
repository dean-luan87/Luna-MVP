# -*- coding: utf-8 -*-
"""Midplatform Structure Cleanup Planning v1 — 8-layer mapping, planning-only."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from capabilities.governance.midplatform_backbone_definition_alignment_v1 import (
    FINAL_DECISION_GO as ALIGNMENT_FINAL_GO,
    PHASE_ID as ALIGNMENT_PHASE,
)
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

PHASE_ID = "Phase-Midplatform-Structure-Cleanup-Planning-v1-001"
SCOPE = "midplatform_structure_cleanup_planning_only"
SOURCE_CHAIN = "midplatform_structure_cleanup_planning_v1"

UPSTREAM_FACTORY_PHASE = "Phase-Luna-Validation-Factory-Consolidation-v1-001"

FINAL_DECISION_GO = "MIDPLATFORM_STRUCTURE_CLEANUP_PLANNING_READY_FOR_MINIMAL_BACKBONE_DRYRUN"
FINAL_DECISION_HOLD = "MIDPLATFORM_STRUCTURE_CLEANUP_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Minimal-Backbone-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Structure-Cleanup-Planning-Issue-Review-v1-001"

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_structure_cleanup_planning"
)

PRIMARY_DIR = "capabilities/midplatform"
BRIDGE_DIR = "capabilities/mid_platform"

EIGHT_LAYER_KEYS: Tuple[str, ...] = (
    "input_output",
    "model_management",
    "health_management",
    "constitution",
    "task",
    "drive",
    "local_memory",
    "support",
)

CLOSED_CANDIDATES = (
    "visual_observation_candidate",
    "ocr_result_candidate",
    "navigation_guidance_candidate",
)
RESERVED_CANDIDATES = (
    "task_response_candidate",
    "speech_response_candidate",
    "memory_lookup_candidate",
    "world_model_readonly_candidate",
    "drive_candidate",
    "external_experience_candidate",
)

CONSTITUTION_GATES = (
    "safety_gate",
    "survival_gate",
    "fact_boundary",
    "action_boundary",
    "output_boundary",
    "memory_write_boundary",
    "model_invocation_boundary",
    "privacy_boundary",
    "source_chain_boundary",
    "ttl_staleness_boundary",
)

LAYER_GAPS: Dict[str, List[str]] = {
    "input_output": [
        "unified_candidate_intake_contract_missing",
        "guidance_queue_not_unified",
        "output_arbitration_dispersed",
    ],
    "model_management": [
        "model_registry_missing",
        "skill_registry_missing",
        "model_health_switching_policy_missing",
        "provider_fallback_dispersed",
    ],
    "health_management": [
        "software_health_manager_incomplete",
        "hardware_manager_mostly_stub",
        "system_monitor_scattered_with_runtime_boundary",
        "health_to_drive_signal_missing",
    ],
    "constitution": [
        "constitution_overlay_registry_missing",
        "gate_manager_not_unified",
        "ttl_staleness_not_centralized",
        "memory_library_hive_gate_missing",
    ],
    "task": [
        "pause_resume_cancel_modules_missing",
        "task_state_vs_commit_boundary_needs_enforcement",
        "task_response_candidate_deferred",
    ],
    "drive": [
        "drive_layer_mostly_definition_missing",
        "health_warning_to_survival_drive_route_missing",
        "drive_to_task_candidate_contract_missing",
    ],
    "local_memory": [
        "memory_readonly_access_contract_missing",
        "memory_write_gate_missing",
        "candidate_memory_pollution_guard_incomplete",
    ],
    "support": [
        "support_layer_mostly_unimplemented",
        "external_experience_candidate_contract_missing",
        "library_hive_sync_gate_missing",
        "direct_local_memory_write_forbidden_not_enforced",
    ],
}

NON_CLAIMS: Tuple[str, ...] = (
    "Structure Cleanup Planning GO ≠ cleanup executed",
    "Eight-layer mapping GO ≠ files moved",
    "Directory role selected ≠ mid_platform deprecated",
    "Runtime bridge role defined ≠ import rewritten",
    "Candidate flow contract defined ≠ runtime enabled",
    "Drive layer mapped ≠ active drive execution enabled",
    "Task layer mapped ≠ task commit allowed",
    "Memory layer mapped ≠ memory write allowed",
    "Support layer mapped ≠ Library / Hive sync enabled",
    "Minimal Backbone DryRun planned ≠ backbone executed",
    "old_nine_layer_mapping_used=false in this phase",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "midplatform_structure_cleanup_planning_only": True,
        "eight_layer_mapping_used": True,
        "old_nine_layer_mapping_used": False,
        "file_move_executed_now": False,
        "file_rename_executed_now": False,
        "module_merge_executed_now": False,
        "module_delete_executed_now": False,
        "directory_merge_executed_now": False,
        "import_rewrite_executed_now": False,
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
    alignment_root: Path,
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

    align_sm = _try_read_json(alignment_root / "summary.json") or {}
    mapping_old = _try_read_json(alignment_root / "midplatform_old_new_layer_mapping_v1.json") or {}
    ctx["alignment"] = align_sm
    if not _check_go(alignment_root):
        blockers.append("backbone alignment verifier must be GO")
    if align_sm.get("final_decision") != ALIGNMENT_FINAL_GO:
        blockers.append("alignment final_decision mismatch")
    if mapping_old.get("superseded_for_engineering_mapping") is not True:
        blockers.append("old nine-layer mapping must be superseded")

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


def _map_module(path: str, stem: str, status: str) -> Dict[str, Any]:
    low = f"{path} {stem}".lower()
    layers: Set[str] = set()
    is_bridge = path.startswith(BRIDGE_DIR)

    if is_bridge:
        layers.add("runtime_bridge")
        if "navigation" in low or "formal_decision" in low or "gate" in low:
            layers.add("constitution")
        if "ocr" in low:
            layers.update({"model_management", "input_output"})
        return {
            "primary_eight_layer": "runtime_bridge",
            "eight_layers": [],
            "runtime_bridge": True,
            "constitution_overlay": "constitution" in layers,
        }

    rules: List[Tuple[str, str]] = [
        ("support", "library"),
        ("support", "hive"),
        ("support", "external_experience"),
        ("local_memory", "memory"),
        ("local_memory", "worldmodel"),
        ("local_memory", "confirmed_text_evidence_memory"),
        ("local_memory", "communication"),
        ("drive", "drive"),
        ("drive", "survival"),
        ("task", "task_manager"),
        ("task", "task_state"),
        ("task", "clarification"),
        ("task", "observation_request"),
        ("task", "static_reading_task"),
        ("constitution", "safety"),
        ("constitution", "gate"),
        ("constitution", "governance"),
        ("constitution", "boundary"),
        ("constitution", "source_validation"),
        ("constitution", "ttl"),
        ("constitution", "arbitration_policy"),
        ("health_management", "health"),
        ("health_management", "hardware"),
        ("health_management", "camera"),
        ("health_management", "watchdog"),
        ("health_management", "monitor"),
        ("health_management", "robustness"),
        ("health_management", "degradation"),
        ("health_management", "failsafe"),
        ("model_management", "ocr"),
        ("model_management", "vision"),
        ("model_management", "voice"),
        ("model_management", "semantic"),
        ("model_management", "poster"),
        ("model_management", "rapidocr"),
        ("model_management", "model"),
        ("model_management", "skill"),
        ("model_management", "text_detector"),
        ("input_output", "ingest"),
        ("input_output", "candidate"),
        ("input_output", "queue"),
        ("input_output", "arbitration"),
        ("input_output", "guidance_to_speech"),
        ("input_output", "output_plane"),
        ("input_output", "evidence_readonly"),
        ("input_output", "cross_modal"),
        ("input_output", "scene_delta"),
        ("input_output", "roi"),
        ("input_output", "navigation_guidance"),
    ]

    for layer, kw in rules:
        if kw in low:
            layers.add(layer)

    if "scene_delta" in low and "write" in low:
        layers.add("constitution")
    if "minimal_runtime" in low:
        layers.update({"health_management", "constitution"})
    if "roadmap" in low or "closure" in low:
        layers.add("constitution")
    if not layers:
        layers.add("input_output" if "dryrun" in low else "constitution")

    eight = [l for l in EIGHT_LAYER_KEYS if l in layers]
    primary = eight[0] if eight else "constitution"
    priority = [
        "constitution",
        "task",
        "health_management",
        "model_management",
        "input_output",
        "local_memory",
        "support",
        "drive",
    ]
    for p in priority:
        if p in eight:
            primary = p
            break

    return {
        "primary_eight_layer": primary,
        "eight_layers": eight,
        "runtime_bridge": False,
        "constitution_overlay": True,
    }


def _layer_cleanup_plan(
    layer_key: str,
    *,
    modules: List[Dict[str, Any]],
    meta: Dict[str, Any],
) -> Dict[str, Any]:
    assigned = [m for m in modules if layer_key in m.get("eight_layers", []) or m.get("primary_eight_layer") == layer_key]
    return {
        "plan_id": f"midplatform_{layer_key}_layer_cleanup_plan_v1",
        "layer_key": layer_key,
        "modules_assigned_count": len(assigned),
        "modules_sample": [m["path"] for m in assigned[:20]],
        "identified_gaps": LAYER_GAPS.get(layer_key, []),
        "planning_actions": ["contract_definition", "gap_register", "no_file_move"],
        **meta,
    }


def run_midplatform_structure_cleanup_planning_v1(
    *,
    midplatform_current_state_inventory_root: str,
    midplatform_backbone_definition_alignment_root: str,
    luna_validation_factory_consolidation_root: str,
    vision_sample_frame_single_chain_controlled_trial_post_execution_review_root: str,
    ocr_mock_result_single_chain_trial_via_validation_factory_root: str,
    navigation_guidance_candidate_single_chain_trial_via_validation_factory_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    inventory_root = Path(midplatform_current_state_inventory_root).expanduser().resolve()
    alignment_root = Path(midplatform_backbone_definition_alignment_root).expanduser().resolve()
    factory_root = Path(luna_validation_factory_consolidation_root).expanduser().resolve()
    vision_root = Path(vision_sample_frame_single_chain_controlled_trial_post_execution_review_root).expanduser().resolve()
    ocr_root = Path(ocr_mock_result_single_chain_trial_via_validation_factory_root).expanduser().resolve()
    nav_root = Path(navigation_guidance_candidate_single_chain_trial_via_validation_factory_root).expanduser().resolve()

    blockers, ctx = _validate_upstream(
        inventory_root, alignment_root, factory_root, vision_root, ocr_root, nav_root
    )
    planning_ok = len(blockers) == 0
    meta = _boundary_meta()
    meta["inventory_root"] = str(inventory_root)
    meta["alignment_root"] = str(alignment_root)

    inv_modules = (_try_read_json(inventory_root / "midplatform_module_inventory_v1.json") or {}).get("modules") or []
    mapped: List[Dict[str, Any]] = []
    for m in inv_modules:
        mp = _map_module(m.get("path", ""), m.get("module_stem", ""), m.get("status", ""))
        mapped.append({**m, **mp})

    bridge_modules = [x for x in mapped if x.get("runtime_bridge")]
    primary_modules = [x for x in mapped if not x.get("runtime_bridge")]

    layer_counts = Counter()
    for m in mapped:
        if m.get("runtime_bridge"):
            layer_counts["runtime_bridge"] += 1
        else:
            layer_counts[m.get("primary_eight_layer", "unknown")] += 1

    module_mapping = {
        "mapping_id": "midplatform_8_layer_module_mapping_v1",
        "modules_total": len(mapped),
        "midplatform_count": sum(1 for m in mapped if m["path"].startswith(PRIMARY_DIR)),
        "mid_platform_count": sum(1 for m in mapped if m["path"].startswith(BRIDGE_DIR)),
        "layer_assignment_counts": dict(layer_counts),
        "modules": mapped,
        **meta,
    }

    overlay_rows = []
    for layer_key in EIGHT_LAYER_KEYS:
        if layer_key == "constitution":
            continue
        overlay_rows.append(
            {
                "layer_key": layer_key,
                "constitution_overlay": True,
                "gates_applied": list(CONSTITUTION_GATES),
            }
        )
    constitution_overlay = {
        "mapping_id": "midplatform_constitution_overlay_mapping_v1",
        "model": "global_horizontal_overlay",
        "overlaid_layers": list(EIGHT_LAYER_KEYS),
        "constitution_layer_not_sequential_only": True,
        "gates": list(CONSTITUTION_GATES),
        "rows": overlay_rows,
        **meta,
    }

    role_decision = {
        "decision_id": "midplatform_directory_role_decision_v1",
        "selected_primary_midplatform_dir": PRIMARY_DIR,
        "selected_runtime_bridge_dir": BRIDGE_DIR,
        "safe_to_merge_now": False,
        "import_rewrite_now": False,
        "directory_merge_now": False,
        "deprecated_marking_now": False,
        **meta,
    }

    runtime_bridge_plan = {
        "plan_id": "midplatform_runtime_bridge_plan_v1",
        "bridge_directory": BRIDGE_DIR,
        "module_count": len(bridge_modules),
        "preserve_voice_runtime_imports": True,
        "import_rewrite_in_this_phase": False,
        "modules": [m["path"] for m in bridge_modules],
        "primary_role": "runtime_adapter_legacy_support",
        **meta,
    }

    candidate_flow = {
        "contract_id": "midplatform_candidate_flow_contract_v1",
        "closed_inputs": list(CLOSED_CANDIDATES),
        "reserved_inputs": list(RESERVED_CANDIDATES),
        "default_constraints": {
            "candidate_only": True,
            "fact_status": "not_fact",
            "write_allowed": False,
            "runtime_action_allowed": False,
            "user_facing_output_allowed": False,
            "source_chain_required": True,
            "provenance_required": True,
            "ttl_required_where_applicable": True,
        },
        "flows": [
            {
                "type": "visual_observation_candidate",
                "path": ["Input/Output", "Evidence", "Perception", "Task", "Constitution overlay"],
            },
            {
                "type": "ocr_result_candidate",
                "path": ["Input/Output", "Evidence", "Model Mgmt ref", "Task", "Queue"],
            },
            {
                "type": "navigation_guidance_candidate",
                "path": ["Input/Output", "Evidence", "Safety Gate", "Queue", "Output Arbitration"],
            },
        ],
        **meta,
    }

    backbone_plan = {
        "plan_id": "midplatform_minimal_backbone_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "consumes": list(CLOSED_CANDIDATES),
        "produces": [
            "candidate_intake_record",
            "evidence_governance_record",
            "constitution_gate_review",
            "task_routing_candidate",
            "guidance_queue_item",
            "output_arbitration_candidate",
            "runtime_boundary_decision",
        ],
        "forbidden": [
            "task_commit",
            "tts",
            "navigation_action",
            "model_invocation",
            "fact_write",
            "memory_write",
            "worldmodel_write",
            "library_sync",
            "hive_sync",
        ],
        **meta,
    }

    route_matrix = {
        "matrix_id": "midplatform_cleanup_route_matrix_v1",
        "routes": [
            {"route_id": "A", "name": "Eight-layer contract-first planning", "selected": True},
            {"route_id": "B", "name": "Immediate directory merge", "blocked": True},
            {"route_id": "C", "name": "Runtime bridge preservation", "selected_supporting": True},
            {"route_id": "D", "name": "Candidate flow unification", "selected_supporting": True},
            {"route_id": "E", "name": "Task response chain now", "deferred": True},
            {"route_id": "F", "name": "Library/Memory/Hive implementation now", "deferred": True},
        ],
        "selected_primary": "A",
        **meta,
    }

    gap_priority = {
        "priority_id": "midplatform_gap_resolution_priority_v1",
        "P0": [
            "eight_layer_module_mapping",
            "candidate_flow_contract",
            "constitution_overlay_mapping",
            "runtime_boundary_matrix",
            "minimal_backbone_dryrun_plan",
        ],
        "P1": [
            "task_state_contract",
            "drive_candidate_contract",
            "output_arbitration_contract",
            "health_to_drive_signal_contract",
        ],
        "P2": [
            "model_registry",
            "skill_registry",
            "local_memory_readonly_access",
            "support_external_experience_contract",
        ],
        "P3": [
            "directory_merge",
            "import_rewrite",
            "runner_verifier_cleanup",
            "stub_implementation",
        ],
        **meta,
    }

    input_review = {
        "review_id": "inventory_and_backbone_input_review_v1",
        "inventory_root": str(inventory_root),
        "alignment_root": str(alignment_root),
        "review_pass": planning_ok,
        "blockers": blockers,
        "confirmed": {
            "inventory_go": planning_ok,
            "alignment_go": _check_go(alignment_root),
            "eight_layer_basis": True,
            "old_nine_layer_superseded": True,
            "safe_to_merge_false": True,
        },
        **meta,
    }

    decision = {
        "decision_id": "midplatform_structure_cleanup_planning_decision_v1",
        "boundary_ok": planning_ok,
        "final_decision": FINAL_DECISION_GO if planning_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_ok else NEXT_PHASE_HOLD,
        "blockers": blockers,
        **meta,
    }

    layer_plans = {
        f"midplatform_{k}_layer_cleanup_plan": _layer_cleanup_plan(k, modules=mapped, meta=meta)
        for k in EIGHT_LAYER_KEYS
    }

    policy = {
        "policy_id": "midplatform_structure_cleanup_planning_policy_v1",
        "scope": SCOPE,
        "approach": "eight_layer_contract_first_no_directory_change",
        **decision,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": planning_ok,
        "violations": blockers,
        "final_decision": decision["final_decision"],
        "recommended_next_phase": decision["recommended_next_phase"],
        "modules_mapped": len(mapped),
        "layer_assignment_counts": dict(layer_counts),
        **meta,
    }

    result = {
        "midplatform_structure_cleanup_planning_policy": policy,
        "inventory_and_backbone_input_review": input_review,
        "midplatform_directory_role_decision": role_decision,
        "midplatform_8_layer_module_mapping": module_mapping,
        "midplatform_constitution_overlay_mapping": constitution_overlay,
        "midplatform_runtime_bridge_plan": runtime_bridge_plan,
        "midplatform_candidate_flow_contract": candidate_flow,
        "midplatform_minimal_backbone_dryrun_plan": backbone_plan,
        "midplatform_cleanup_route_matrix": route_matrix,
        "midplatform_gap_resolution_priority": gap_priority,
        "midplatform_structure_cleanup_non_claims_register": {
            "register_id": "midplatform_structure_cleanup_non_claims_register_v1",
            "non_claims": list(NON_CLAIMS),
            **meta,
        },
        "midplatform_structure_cleanup_planning_decision": decision,
        "summary": summary,
        **layer_plans,
    }
    return result
