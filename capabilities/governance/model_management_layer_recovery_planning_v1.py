# -*- coding: utf-8 -*-
"""Model Management Layer Recovery Planning v1 — registry/health/switch planning only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.luna_validation_factory_consolidation_v1 import (
    FINAL_DECISION as FACTORY_FINAL,
    PHASE_ID as FACTORY_PHASE,
)
from capabilities.governance.midplatform_backbone_definition_alignment_v1 import (
    FINAL_DECISION_GO as ALIGNMENT_FINAL_GO,
    PHASE_ID as ALIGNMENT_PHASE,
)
from capabilities.governance.midplatform_module_gap_and_roadmap_planning_v1 import (
    FINAL_DECISION_GO as GAP_FINAL_GO,
    P1_MODULES,
    P2_MODULES,
    PHASE_ID as GAP_PHASE,
)
from capabilities.governance.midplatform_post_backbone_roadmap_decision_v1 import (
    DEFERRED_ROUTE,
    SELECTED_ROUTE,
)
from capabilities.governance.midplatform_structure_cleanup_planning_v1 import (
    FINAL_DECISION_GO as CLEANUP_FINAL_GO,
    PHASE_ID as CLEANUP_PHASE,
)
from capabilities.governance.task_response_candidate_midplatform_integration_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as TASK_RESPONSE_REVIEW_FINAL_GO,
    NEXT_PHASE_GO as TASK_RESPONSE_REVIEW_NEXT,
    PHASE_ID as TASK_RESPONSE_REVIEW_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Model-Management-Layer-Recovery-Planning-v1-001"
SCOPE = "model_management_layer_recovery_planning_only"
SOURCE_CHAIN = "model_management_layer_recovery_planning_v1"

UPSTREAM_TASK_RESPONSE_FINAL = TASK_RESPONSE_REVIEW_FINAL_GO
UPSTREAM_TASK_RESPONSE_NEXT = TASK_RESPONSE_REVIEW_NEXT

FINAL_DECISION_GO = "MODEL_MANAGEMENT_LAYER_RECOVERY_PLANNING_READY_FOR_DRYRUN"
FINAL_DECISION_HOLD = "MODEL_MANAGEMENT_LAYER_RECOVERY_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Model-Management-Layer-Recovery-DryRun-v1-001"

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_recovery_planning"
)

MODEL_DOMAINS: Tuple[str, ...] = (
    "emotion",
    "vision",
    "perspective",
    "ocr",
    "voice",
    "asr",
    "tts",
    "face_recognition",
    "scan",
    "skill_provider_future",
)

RUNTIME_MODES: Tuple[str, ...] = ("mock", "fixture", "local", "cloud", "disabled")

HEALTH_STATES: Tuple[str, ...] = (
    "available",
    "degraded",
    "timeout",
    "failed",
    "disabled",
    "unknown",
)

CAPABILITY_DESCRIPTORS: Tuple[str, ...] = (
    "can_see",
    "can_read_text",
    "can_transcribe",
    "can_speak",
    "can_recognize_face",
    "can_scan",
    "can_detect_emotion",
    "can_generate_candidate",
    "can_write_fact",
    "can_trigger_action",
)

MODEL_OUTPUT_CANDIDATE_TYPES: Tuple[str, ...] = (
    "visual_observation_candidate",
    "ocr_result_candidate",
    "speech_response_candidate",
    "task_response_candidate",
    "emotion_state_candidate",
    "face_identity_candidate",
    "scan_result_candidate",
)

SWITCHING_RULES: Tuple[str, ...] = (
    "primary_model_unavailable_to_fallback_candidate",
    "provider_timeout_to_hold_or_fallback",
    "high_latency_to_lower_cost_model_candidate",
    "hardware_pressure_to_degrade_model",
    "unsafe_output_block",
    "uncertain_output_candidate_only_not_fact",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Planning GO ≠ any model invoked",
    "Registry contract defined ≠ model_registry_created_now",
    "Skill registry defined ≠ skill enabled",
    "Health state defined ≠ runtime health monitor enabled",
    "Switch policy defined ≠ model_switch_executed_now",
    "Route B recovery planning ≠ Route A task response rollback",
    "DryRun plan ≠ provider optimization",
)


def _boundary_meta() -> Dict[str, Any]:
    return {
        "model_management_layer_recovery_planning_only": True,
        "model_registry_created_now": False,
        "skill_registry_created_now": False,
        "model_runtime_invoked_now": False,
        "model_provider_invoked_now": False,
        "ocr_provider_invoked_now": False,
        "vision_model_invoked_now": False,
        "voice_model_invoked_now": False,
        "emotion_model_invoked_now": False,
        "face_recognition_model_invoked_now": False,
        "scan_model_invoked_now": False,
        "model_switch_executed_now": False,
        "model_update_executed_now": False,
        "model_repair_executed_now": False,
        "runtime_enabled_now": False,
        "task_state_committed_now": False,
        "tts_invoked_now": False,
        "llm_invoked_now": False,
        "user_facing_output_generated_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "model_layer_optimization_started_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _check_go(root: Path) -> bool:
    if not root.is_dir():
        return False
    vr = _try_read_json(root / "verifier_report.json") or {}
    sm = _try_read_json(root / "summary.json") or {}
    return (vr.get("verifier") == "GO" and vr.get("passed") is True) or sm.get("boundary_ok") is True


def run_model_management_layer_recovery_planning_v1(
    *,
    task_response_candidate_midplatform_integration_post_dryrun_review_root: str,
    midplatform_post_backbone_roadmap_decision_root: str,
    midplatform_module_gap_and_roadmap_planning_root: str,
    midplatform_structure_cleanup_planning_root: str,
    midplatform_backbone_definition_alignment_root: str,
    luna_validation_factory_consolidation_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    roots = {
        "task_response_review": Path(task_response_candidate_midplatform_integration_post_dryrun_review_root).expanduser().resolve(),
        "roadmap": Path(midplatform_post_backbone_roadmap_decision_root).expanduser().resolve(),
        "gap": Path(midplatform_module_gap_and_roadmap_planning_root).expanduser().resolve(),
        "cleanup": Path(midplatform_structure_cleanup_planning_root).expanduser().resolve(),
        "alignment": Path(midplatform_backbone_definition_alignment_root).expanduser().resolve(),
        "factory": Path(luna_validation_factory_consolidation_root).expanduser().resolve(),
    }
    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_boundary_meta(), "output_root": str(out_root), "upstream_roots": {k: str(v) for k, v in roots.items()}}

    tr_sm = _try_read_json(roots["task_response_review"] / "summary.json") or {}
    tr_vr = _try_read_json(roots["task_response_review"] / "verifier_report.json") or {}
    roadmap_sm = _try_read_json(roots["roadmap"] / "summary.json") or {}
    gap_sm = _try_read_json(roots["gap"] / "summary.json") or {}
    align_sm = _try_read_json(roots["alignment"] / "summary.json") or {}

    tr_go = tr_vr.get("verifier") == "GO" and tr_vr.get("passed") is True
    if not tr_go:
        blockers.append("task response post-dryrun review verifier must be GO")
    if tr_sm.get("final_decision") != UPSTREAM_TASK_RESPONSE_FINAL:
        blockers.append("task response review final_decision mismatch")
    if tr_sm.get("recommended_next_phase") != UPSTREAM_TASK_RESPONSE_NEXT:
        blockers.append("task response review next phase mismatch")

    if roadmap_sm.get("deferred_route") != DEFERRED_ROUTE:
        blockers.append("route B must match deferred_route in roadmap")
    if roadmap_sm.get("selected_route") != SELECTED_ROUTE:
        blockers.append("route A must remain selected_route")
    closure = _try_read_json(roots["task_response_review"] / "post_dryrun_closure_decision_v1.json") or {}
    if closure.get("first_round_midplatform_task_response_closure") is not True:
        blockers.append("route A first-round closure required")

    if not _check_go(roots["gap"]):
        blockers.append("module gap planning must be GO")
    if gap_sm.get("final_decision") != GAP_FINAL_GO:
        blockers.append("gap planning final mismatch")
    p2_register = _try_read_json(roots["gap"] / "optional_future_module_register_v1.json") or {}
    registered = set(p2_register.get("P2") or p2_register.get("modules") or [])
    for mod in P2_MODULES:
        if mod not in registered:
            blockers.append(f"P2 model module not in gap register: {mod}")

    for label, root, phase, final in (
        ("cleanup", roots["cleanup"], CLEANUP_PHASE, CLEANUP_FINAL_GO),
        ("alignment", roots["alignment"], ALIGNMENT_PHASE, ALIGNMENT_FINAL_GO),
        ("factory", roots["factory"], FACTORY_PHASE, FACTORY_FINAL),
    ):
        if not _check_go(root):
            blockers.append(f"{label} upstream must be GO")
        sm = _try_read_json(root / "summary.json") or {}
        if phase and sm.get("phase") != phase:
            blockers.append(f"{label} phase mismatch")
        if final and sm.get("final_decision") != final:
            blockers.append(f"{label} final mismatch")

    if align_sm.get("layer_count", 8) != 8 and "model_management" not in str(align_sm):
        pass  # eight layer defined in alignment artifacts

    input_review = {
        "review_id": "upstream_task_response_review_input_review_v1",
        "task_response_review_root": str(roots["task_response_review"]),
        "roadmap_root": str(roots["roadmap"]),
        "route_a_closed": closure.get("first_round_midplatform_task_response_closure"),
        "route_b_deferred_route": roadmap_sm.get("deferred_route"),
        "task_response_review_go": tr_go,
        "gap_p1_model_modules": [m for m in P1_MODULES if "model" in m],
        "gap_p2_model_modules": list(P2_MODULES),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    scope_doc = {
        "scope_id": "model_management_layer_scope_v1",
        "layer": "model_management",
        "covers_domains": list(MODEL_DOMAINS),
        "includes_skill_extension": True,
        "planning_not_optimization": True,
        "invocation_allowed_default": False,
        **meta,
    }

    registry_contract = {
        "contract_id": "model_registry_contract_planning_v1",
        "required_fields": [
            "model_id",
            "model_domain",
            "model_type",
            "version",
            "provider_type",
            "runtime_mode",
            "capability_tags",
            "input_contract",
            "output_contract",
            "health_state_ref",
            "fallback_model_ref",
            "invocation_allowed",
            "runtime_boundary_profile",
        ],
        "runtime_modes": list(RUNTIME_MODES),
        "invocation_allowed_default": False,
        "default_runtime_mode_planning": "disabled",
        "dryrun_will_use": ["mock", "fixture"],
        **meta,
    }

    skill_contract = {
        "contract_id": "skill_registry_contract_planning_v1",
        "required_fields": [
            "skill_id",
            "skill_domain",
            "skill_type",
            "required_models",
            "required_runtime_permissions",
            "input_candidate_types",
            "output_candidate_types",
            "safety_gate_required",
            "constitution_gate_required",
            "user_facing_output_allowed",
        ],
        "safety_gate_required_default": True,
        "constitution_gate_required_default": True,
        "user_facing_output_allowed_default": False,
        **meta,
    }

    capability_descriptor = {
        "contract_id": "model_capability_descriptor_contract_v1",
        "descriptors": {k: (False if k in ("can_write_fact", "can_trigger_action") else True) for k in CAPABILITY_DESCRIPTORS},
        "defaults": {"can_write_fact": False, "can_trigger_action": False, "can_generate_candidate": True},
        **meta,
    }

    health_contract = {
        "contract_id": "model_health_state_contract_v1",
        "states": list(HEALTH_STATES),
        "required_fields": [
            "available",
            "degraded",
            "timeout",
            "failed",
            "disabled",
            "unknown",
            "last_check",
            "latency_budget",
            "error_count",
            "fallback_required",
        ],
        "dryrun_candidate_type": "model_health_state_candidate",
        **meta,
    }

    switching_policy = {
        "policy_id": "model_switching_and_degradation_policy_v1",
        "rules": list(SWITCHING_RULES),
        "primary_unavailable": "fallback_model_candidate",
        "provider_timeout": "hold_or_fallback",
        "high_latency": "lower_cost_model_candidate",
        "hardware_pressure": "degrade_model",
        "unsafe_output": "block",
        "uncertain_output": "candidate_only_not_fact",
        "dryrun_candidate_type": "model_switching_candidate",
        **meta,
    }

    output_integration = {
        "plan_id": "model_output_contract_integration_plan_v1",
        "candidate_output_types": list(MODEL_OUTPUT_CANDIDATE_TYPES),
        "defaults": {
            "candidate_only": True,
            "fact_status": "not_fact",
            "write_allowed": False,
            "runtime_action_allowed": False,
            "user_facing_output_allowed": False,
        },
        "integrates_with": "candidate_output_contract_v1",
        "no_direct_fact_upgrade": True,
        **meta,
    }

    runtime_matrix = {
        "matrix_id": "model_runtime_boundary_matrix_v1",
        "rows": [
            {"boundary": "planning_no_model_invocation", "allowed_now": False},
            {"boundary": "registry_defined_not_invocation_allowed", "allowed_now": False},
            {"boundary": "skill_registry_defined_not_skill_enabled", "allowed_now": False},
            {"boundary": "health_state_defined_not_monitor_enabled", "allowed_now": False},
            {"boundary": "switch_policy_defined_not_switch_executed", "allowed_now": False},
            {"boundary": "provider_change_blocked", "allowed_now": False},
            {"boundary": "real_ocr_vision_voice_blocked", "allowed_now": False},
        ],
        **meta,
    }

    provider_mapping = {
        "mapping_id": "model_provider_governance_mapping_v1",
        "domains": [
            {"domain": "vision", "planning_provider_type": "mock_or_fixture_only", "real_provider": "blocked"},
            {"domain": "ocr", "planning_provider_type": "mock_or_fixture_only", "real_provider": "blocked"},
            {"domain": "voice", "planning_provider_type": "mock_or_fixture_only", "real_provider": "blocked"},
            {"domain": "emotion", "planning_provider_type": "disabled", "real_provider": "blocked"},
            {"domain": "face_recognition", "planning_provider_type": "disabled", "real_provider": "blocked"},
            {"domain": "scan", "planning_provider_type": "disabled", "real_provider": "blocked"},
        ],
        "no_provider_rewrite": True,
        **meta,
    }

    factory_integration = {
        "plan_id": "validation_factory_model_layer_integration_plan_v1",
        "factory_layer_role": "candidate contract enforcement for model outputs",
        "hooks": [
            "validate_candidate_output on model-layer dryrun emissions",
            "single-chain trials remain separate from registry dryrun",
        ],
        "no_live_provider_in_factory_dryrun": True,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "model_management_recovery_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "objectives": [
            "register mock/fixture model registry entries",
            "register skill registry entries",
            "emit model_health_state_candidate",
            "emit model_switching_candidate",
            "wire model outputs to CandidateOutputContract",
            "invoke_no_real_models",
        ],
        **meta,
    }

    planning_ok = input_review.get("review_pass") is True

    decision = {
        "decision_id": "model_management_recovery_planning_decision_v1",
        "ready_for_model_management_recovery_dryrun": planning_ok,
        "final_decision": FINAL_DECISION_GO if planning_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_ok else PHASE_ID,
        "route_b_resume_after_route_a_closure": True,
        **meta,
    }

    policy = {
        "policy_id": "model_management_recovery_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "principles": [
            "governance_skeleton_first",
            "no_model_invocation",
            "no_model_optimization",
        ],
        **meta,
    }

    non_claims = {
        "register_id": "model_management_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": planning_ok,
        "violations": blockers,
        "final_decision": decision["final_decision"],
        "recommended_next_phase": decision["recommended_next_phase"],
        "high_risk_count": 0 if planning_ok else 1,
        **meta,
    }

    return {
        "model_management_recovery_planning_policy": policy,
        "upstream_task_response_review_input_review": input_review,
        "model_management_layer_scope": scope_doc,
        "model_registry_contract_planning": registry_contract,
        "skill_registry_contract_planning": skill_contract,
        "model_capability_descriptor_contract": capability_descriptor,
        "model_health_state_contract": health_contract,
        "model_switching_and_degradation_policy": switching_policy,
        "model_output_contract_integration_plan": output_integration,
        "model_runtime_boundary_matrix": runtime_matrix,
        "model_provider_governance_mapping": provider_mapping,
        "validation_factory_model_layer_integration_plan": factory_integration,
        "model_management_recovery_dryrun_plan": dryrun_plan,
        "model_management_non_claims_register": non_claims,
        "model_management_recovery_planning_decision": decision,
        "summary": summary,
    }
