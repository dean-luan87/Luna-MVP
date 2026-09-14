#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Tuple


def _is_workspace_root(candidate: Path) -> bool:
    markers = (
        candidate / "AGENTS.md",
        candidate / "capabilities",
        candidate / "tools" / "evaluation" / "midplatform",
    )
    return all(marker.exists() for marker in markers)


def _find_ws_root() -> Path:
    cwd = Path.cwd().absolute()
    if _is_workspace_root(cwd):
        return cwd

    script_path = Path(__file__).absolute()
    for candidate in (script_path.parent, *script_path.parents):
        if _is_workspace_root(candidate):
            return candidate

    raise RuntimeError("Unable to locate Luna workspace root")


REPO_ROOT = _find_ws_root()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.task_manager.module import run_task_manager_module_v1
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_module_api_v1 import (
    run_field_perception_orchestrator_module_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_visual_handoff_api_v1 import (
    run_field_perception_visual_handoff_integration_v1,
)
from capabilities.midplatform.vision_manager.module import (
    run_vision_manager_module_api_v1,
)
from capabilities.midplatform.model_manager.module import (
    run_model_manager_module_api_v1,
)
from capabilities.midplatform.observation_manager.module.observation_manager_module_api_v1 import (
    run_observation_manager_module_v1,
)
from capabilities.midplatform.core.field_state_reducer.module import (
    FieldStateReducerModuleRequestV1,
    FieldStateReducerModuleV1,
    module_result_to_dict,
)


def _task_request(case_id: str, task_id: str) -> Dict[str, Any]:
    return {
        "task_request_id": task_id,
        "task_type": "sequential",
        "task_goal": "system_chain_validation",
        "requester_ref": "system_integration_runner",
        "priority": "normal",
        "context_snapshot": {
            "request_direct_action_execution": False,
            "request_direct_model_call": False,
            "request_direct_field_state_write": False,
            "request_bypass_capability_module_api": False,
        },
        "dependency_refs": ("dep_a",),
        "dependency_snapshot": {"dep_a": "completed"},
        "dependency_graph": {"dep_a": []},
        "resource_constraints": {"budget": "candidate_only"},
        "permission_snapshot": {"governance_ref": "gov_tm_v1", "allowed": True},
        "capability_requirements": (
            "luna.field_perception_orchestrator",
            "luna.vision_manager",
            "luna.model_manager",
            "luna.observation_manager",
            "luna.field_state_reducer",
        ),
        "deadline_or_timeout": "t+5m",
        "interruption_policy": {"required_revalidation": True},
        "recovery_policy": {
            "preferred_recovery": ("retry_candidate", "replan_candidate")
        },
        "version_snapshots": {
            "task_manager": "v1",
            "field_perception_orchestrator": "v1",
            "vision_manager": "v1",
            "model_manager": "v1",
            "observation_manager": "v1",
            "field_state_reducer": "v1",
        },
        "health_signal_refs": ("health_ok",),
        "decision_refs": (f"decision_{case_id}",),
        "context_refs": (f"ctx_{case_id}",),
        "observation_refs": (f"obs_{case_id}",),
        "module_adapter_refs": ("adapter_tm",),
        "output_gate_refs": ("gate_tm",),
        "worldmodel_memory_bridge_refs": ("wmb_tm",),
        "decision_center_refs": ("dc_tm",),
        "health_watchdog_refs": ("hw_tm",),
        "readiness_hint": "ready",
        "recovery_point": "rp_0",
        "failure_reason": "",
        "cancel_reason": "",
        "terminate_reason": "",
        "requested_control": "",
        "completion_status": "",
        "interruption_reason": "",
        "recovery_decision": "",
    }


def _fpo_payload(case_id: str, task_id: str, low_budget: bool) -> Dict[str, Any]:
    payload = {
        "task_context": {"task_id": task_id, "goal": "navigate safely"},
        "current_field_state": {
            "field_snapshot_ref": f"field_snapshot_{case_id}",
            "known_entities": ["road", "pedestrian"],
            "known_regions": ["front_corridor", "left_side"],
            "temporary_overlays": [],
            "active_risks": [],
            "navigation_relevance": {"front_corridor": 0.9},
            "uncertainties": [],
            "conflicts": [],
            "stale_evidence": ["front_obstacle"],
            "missing_information": ["front_passability"],
        },
        "recent_observation_summary": {
            "sufficient_for_decision": False,
            "expired": False,
        },
        "available_visual_capabilities": [
            "detection",
            "segmentation",
            "depth",
            "ocr",
            "tracking",
        ],
        "available_model_assets": [
            {
                "model_id": "detection_v1",
                "supports": ["detection", "tracking"],
                "preferred": True,
            },
            {
                "model_id": "slam_v1",
                "supports": ["segmentation", "depth", "spatial_mapping"],
                "preferred": True,
            },
            {
                "model_id": "ocr_v1",
                "supports": ["ocr", "layout_analysis"],
                "preferred": False,
            },
        ],
        "resource_budget": {
            "cpu_budget": 1 if low_budget else 4,
            "memory_budget_mb": 800 if low_budget else 4096,
            "latency_budget_ms": 700 if low_budget else 2500,
        },
        "temporal_context": {
            "is_night": False,
            "low_light": False,
            "fast_changing_scene": False,
        },
        "uncertainty_state": {},
        "conflict_state": {},
        "previous_invocation_history": [],
    }
    return payload


def _handoff_payload(
    case_id: str,
    fpo_result: Mapping[str, Any],
    *,
    no_eligible_model: bool,
) -> Dict[str, Any]:
    plan = dict(fpo_result.get("field_perception_plan") or {})
    requested_capabilities = tuple(plan.get("requested_visual_capabilities") or ())
    resource_budget = {
        "latency_budget_ms": 1500,
        "memory_budget_mb": 2048,
        "compute_budget_units": 2,
        "power_budget": 2,
        "concurrent_invocation_limit": 2,
        "preferred_model_classes": ("teacher", "tool"),
        "fallback_model_classes": ("tool",),
    }
    if no_eligible_model:
        resource_budget["preferred_model_classes"] = ("non_existing_class",)

    return {
        "field_perception_visual_handoff_request": {
            "handoff_request_id": f"handoff_req_{case_id}",
            "field_perception_plan": plan,
            "task_context": {"task_id": fpo_result.get("task_id") or ""},
            "field_snapshot_ref": plan.get("field_snapshot_ref") or "",
            "information_gap_ref": f"gap_ref_{case_id}",
            "observation_goal": plan.get("observation_goal") or "",
            "target_region": plan.get("target_region") or "front_corridor",
            "target_entity_types": tuple(plan.get("target_entity_types") or ()),
            "requested_visual_capabilities": requested_capabilities,
            "preferred_model_candidates": tuple(
                plan.get("preferred_model_candidates") or ()
            ),
            "fallback_model_candidates": tuple(
                plan.get("fallback_model_candidates") or ()
            ),
            "resolution_level": plan.get("resolution_level") or "standard",
            "temporal_window": plan.get("temporal_window") or "normal",
            "observation_priority": plan.get("observation_priority") or "normal",
            "confidence_requirement": float(plan.get("confidence_requirement") or 0.8),
            "expected_evidence_types": tuple(
                plan.get("expected_evidence_types") or ("detection_box",)
            ),
            "stop_condition": dict(plan.get("stop_condition") or {}),
            "reobserve_condition": dict(plan.get("reobserve_condition") or {}),
            "available_visual_capabilities": (
                "detection",
                "segmentation",
                "depth",
                "ocr",
                "tracking",
            ),
            "available_model_assets": (
                {"model_id": "detection_v1", "supports": ("detection",)},
                {
                    "model_id": "slam_v1",
                    "supports": ("segmentation", "depth", "spatial_mapping"),
                },
                {"model_id": "ocr_v1", "supports": ("ocr",)},
            ),
            "model_manager_snapshot": {"source": "model_manager_module_v1"},
            "resource_budget": resource_budget,
            "invocation_history": tuple(),
            "permission_context": {"request_rejected": False, "conflicted": False},
            "version_snapshot": {"capability": "v1", "module_api": "v1"},
            "trace_context": {"phase": "system_integration_validation_v1"},
            "vision_required": True,
        }
    }


def _vision_payload(
    case_id: str,
    handoff_result: Mapping[str, Any],
) -> Dict[str, Any]:
    request = dict(handoff_result.get("vision_request_candidate") or {})
    attention = str(request.get("target_region") or "front_corridor")
    return {
        "request_id": str(request.get("vision_request_id") or f"vision_req_{case_id}"),
        "capability": "luna.vision_manager",
        "observation_request": "observe_task_target_area",
        "attention_target": attention,
        "frame_quality": "good",
        "model_test_lens": "default",
        "ownership_ok": True,
        "version_snapshot": {
            "capability_registry": "v1",
            "module_api": "v1",
        },
        "trace_context": {"case_id": case_id},
    }


def _model_payload(
    case_id: str,
    task_ref: str,
    handoff_result: Mapping[str, Any],
    *,
    force_no_eligible_model: bool,
) -> Dict[str, Any]:
    requirement = dict(handoff_result.get("model_requirement_candidate") or {})
    requested_capability = str(
        requirement.get("primary_required_capability") or "object_detection"
    )
    if force_no_eligible_model:
        requested_capability = "non_existing_capability"

    return {
        "request_id": f"model_req_{case_id}",
        "requested_capability": requested_capability,
        "task_ref": task_ref,
        "device_ref": "device_a",
        "region_ref": "region_001",
        "resource_snapshot": {
            "latency_ms": 900,
            "memory_available": 8192,
            "gpu_memory_required_gb": 2,
            "gpu_memory_available_gb": 8,
            "cpu_load_percent": 35,
            "concurrent_limit": 2,
            "concurrent_slots_used": 0,
            "api_quota_available": True,
            "runtime_status": "available",
            "network_available": True,
            "qwen_available": True,
            "gemini_available": True,
            "local_runtime_available": True,
            "cuda_available": True,
            "temperature_celsius": 62,
            "historical_performance": {"qwen_vl": 0.92, "internvl2_5": 0.86},
            "scoring_mode": "balanced",
        },
        "allowed_model_classes": ["teacher", "local_vlm", "tool"],
        "forbidden_model_ids": [],
        "latency_requirement": 3000,
        "memory_budget": 4096,
        "offline_required": False,
        "privacy_requirement": "normal",
        "ownership_context": {
            "profile_key": "stacked_documents",
            "allowed_regions": ["region_001", "region_002"],
            "allowed_devices": ["device_a", "device_b"],
            "blocked_regions": [],
        },
        "version_snapshot": {
            "capability_registry": "v1",
            "model_registry": "v1",
            "module_api": "v1",
        },
        "trace_context": {"case_id": case_id},
    }


def _observation_payload(
    case_id: str,
    task_ref: str,
    handoff_result: Mapping[str, Any],
    vision_result: Mapping[str, Any],
    *,
    blocked: bool,
) -> Dict[str, Any]:
    observation_candidate = dict(
        handoff_result.get("observation_request_candidate") or {}
    )
    expected_evidence_types = tuple(
        observation_candidate.get("expected_evidence_types") or ()
    )
    return {
        "observation_request_id": str(
            observation_candidate.get("observation_request_id") or f"obs_req_{case_id}"
        ),
        "request_type": "task_driven",
        "task_id": task_ref,
        "task_context": {
            "task_context_ref": f"task_ctx_{task_ref or case_id}",
            "subject_ref": "system_validation",
            "subject_refs": ["system_validation"],
        },
        "scene_context": {
            "scene_context_ref": str(handoff_result.get("field_snapshot_ref") or ""),
            "scene_id": str(handoff_result.get("field_snapshot_ref") or ""),
        },
        "attention_targets": [
            str(handoff_result.get("observation_goal") or "observe_forward_path")
        ],
        "region_hints": [
            str((observation_candidate.get("target_region") or "front_corridor"))
        ],
        "temporal_snapshot": {
            "temporal_snapshot_ref": f"ts_{case_id}",
            "frame_time": "2026-07-17T00:00:00Z",
        },
        "source_constraints": {
            "evidence_sufficient": not blocked,
            "conflicting_evidence": False,
            "request_rejected": blocked,
        },
        "vision_requested": True,
        "ocr_requested": "ocr_text" in expected_evidence_types,
        "human_correction_refs": [],
        "permission_context": {
            "owner_ref": "observation_manager",
            "consent_ref": {"status": "granted"},
            "policy_snapshot": {},
            "risk_context": {},
        },
        "version_snapshot": {"observation_manager": "v1"},
        "trace_context": {"case_id": case_id},
        "vision_evidence_refs": [
            f"vision_ev::{vision_result.get('trace_ref') or case_id}"
        ],
        "ocr_evidence_refs": [],
    }


def _field_state_payload(
    case_id: str,
    observation_result: Mapping[str, Any],
) -> Dict[str, Any]:
    task_context_ref = str(
        observation_result.get("task_context_ref") or "task_ctx_unknown"
    )
    event_time = "2026-07-17T00:00:00+00:00"
    return {
        "reducer_request_id": f"reducer_req_{case_id}",
        "reducer_run_id": f"reducer_run_{case_id}",
        "field_id": "field_001",
        "requested_state_type": "presence_state",
        "admitted_events": (
            {
                "event_id": f"evt_{case_id}_1",
                "source_id": "observation_manager",
                "event_time": event_time,
                "admission_id": f"admission_{case_id}_1",
            },
            {
                "event_id": f"evt_{case_id}_2",
                "source_id": "observation_manager",
                "event_time": event_time,
                "admission_id": f"admission_{case_id}_2",
            },
        ),
        "existing_state_snapshot": {
            "state_id": f"state_{case_id}",
            "status": "candidate",
            "value": {"source": "existing", "task_context_ref": task_context_ref},
        },
        "temporal_snapshot": {
            "status": "active",
            "refresh_evidence_available": True,
            "new_event_available": True,
            "sufficient_evidence": True,
        },
        "policy_registry_snapshot": {"version": "v1"},
        "evaluation_contract_snapshot": {"version": "v1"},
        "selection_contract_snapshot": {"version": "v1"},
        "reduction_contract_snapshot": {"version": "v1"},
        "conflict_snapshot": {
            "conflict_type": "none",
            "unresolved": False,
            "preserve_conflict": False,
            "provisional_candidate_allowed": True,
            "conflicting_event_refs": [],
            "resolution_available": True,
        },
        "overlay_snapshot": {
            "overlay_refs": [],
            "overlay_active": False,
            "overlay_expired": False,
            "substrate_mutation_requested": False,
        },
        "owner_correction_snapshot": {"owner_correction_refs": []},
        "provenance_snapshot": {
            "source_id": "observation_manager",
            "event_id": f"evt_{case_id}_1",
            "event_time": event_time,
            "admission_id": f"admission_{case_id}_1",
            "available_keys": ["source_id", "event_id", "event_time", "admission_id"],
            "source_ids": ["observation_manager"],
            "confidence_policy_snapshot": {"measured_confidence": 0.9},
            "governance_snapshot": {
                "owner_correction_review": True,
                "fact_admission_dependency": True,
                "permission_admission_dependency": True,
                "human_review_dependency": True,
                "protocol_version_dependency": True,
                "provenance_dependency": True,
                "change_control_dependency": True,
                "runtime_boundary_dependency": True,
            },
            "evaluation_requested_at": event_time,
        },
        "version_snapshots": {
            "policy_registry_version": "v1",
            "eligibility_matrix_version": "v1",
            "precedence_matrix_version": "v1",
            "composition_contract_version": "v1",
            "replay_contract_version": "v1",
            "evaluation_contract_version": "v1",
            "reduction_contract_version": "v1",
        },
        "direct_mutation_requested": False,
        "runtime_request": False,
        "provider_request": False,
        "model_request": False,
        "external_lookup_request": False,
    }


def _is_false(mapping: Mapping[str, Any], key: str) -> bool:
    return mapping.get(key) is False


def _boundary_ok(
    task_result: Mapping[str, Any],
    fpo_result: Mapping[str, Any],
    handoff_result: Mapping[str, Any],
    vision_result: Mapping[str, Any],
    model_result: Mapping[str, Any],
    observation_result: Mapping[str, Any],
    field_state_result: Mapping[str, Any],
) -> bool:
    checks = [
        _is_false(task_result, "action_execution_executed"),
        _is_false(task_result, "model_call_executed"),
        _is_false(task_result, "state_mutation_executed"),
        _is_false(task_result, "fact_promotion_executed"),
        _is_false(task_result, "runtime_dispatch_executed"),
        _is_false(fpo_result, "model_invocation_executed"),
        _is_false(fpo_result, "camera_capture_executed"),
        _is_false(fpo_result, "state_mutation_executed"),
        _is_false(fpo_result, "fact_admission_executed"),
        _is_false(fpo_result, "action_execution_executed"),
        _is_false(fpo_result, "runtime_loop_executed"),
        _is_false(handoff_result, "vision_model_executed"),
        _is_false(handoff_result, "camera_capture_executed"),
        _is_false(handoff_result, "provider_runtime_executed"),
        _is_false(handoff_result, "vision_evidence_created"),
        _is_false(handoff_result, "field_state_write_executed"),
        _is_false(handoff_result, "runtime_loop_executed"),
        _is_false(handoff_result, "production_runtime_executed"),
        _is_false(vision_result, "camera_invoked"),
        _is_false(vision_result, "visual_model_invoked"),
        _is_false(vision_result, "production_runtime_executed"),
        _is_false(model_result, "model_inference_executed"),
        _is_false(model_result, "provider_call_executed"),
        _is_false(model_result, "production_runtime_executed"),
        _is_false(observation_result, "provider_runtime_executed"),
        _is_false(observation_result, "field_state_write_executed"),
        _is_false(observation_result, "production_runtime_executed"),
        _is_false(field_state_result, "fact_admitted"),
        _is_false(field_state_result, "state_store_write_executed"),
        _is_false(field_state_result, "action_trigger_executed"),
        _is_false(field_state_result, "runtime_execution"),
    ]
    return all(checks)


def _non_empty_trace_replay(*rows: Mapping[str, Any]) -> bool:
    return all(bool(r.get("trace_ref")) and bool(r.get("replay_key")) for r in rows)


def _run_chain(
    *,
    case_id: str,
    task_id: str,
    low_budget: bool,
    no_eligible_model: bool,
    observation_blocked: bool,
    invalid_task: bool,
) -> Dict[str, Any]:
    issues: List[str] = []
    unhandled_exceptions = 0

    task_request_id = "" if invalid_task else task_id
    task_result = run_task_manager_module_v1(_task_request(case_id, task_request_id))
    task_ref = str(
        task_result.get("task_id")
        or task_result.get("task_plan", {}).get("task_id")
        or ""
    )

    fpo_result = run_field_perception_orchestrator_module_v1(
        _fpo_payload(case_id, task_ref or task_id, low_budget)
    )
    if bool(fpo_result.get("unhandled_exception", False)):
        unhandled_exceptions += 1

    handoff_result = run_field_perception_visual_handoff_integration_v1(
        _handoff_payload(
            case_id,
            fpo_result,
            no_eligible_model=no_eligible_model,
        )
    )
    if bool(handoff_result.get("unhandled_exception", False)):
        unhandled_exceptions += 1

    vision_result = run_vision_manager_module_api_v1(
        _vision_payload(case_id, handoff_result)
    )

    model_result = run_model_manager_module_api_v1(
        _model_payload(
            case_id,
            task_ref=task_ref or task_id,
            handoff_result=handoff_result,
            force_no_eligible_model=no_eligible_model,
        )
    )

    observation_result = run_observation_manager_module_v1(
        _observation_payload(
            case_id,
            task_ref=task_ref or task_id,
            handoff_result=handoff_result,
            vision_result=vision_result,
            blocked=observation_blocked,
        )
    )
    if bool(observation_result.get("unhandled_exception", False)):
        unhandled_exceptions += 1

    field_state_request = FieldStateReducerModuleRequestV1(
        **_field_state_payload(case_id, observation_result)
    )
    field_state_result = module_result_to_dict(
        FieldStateReducerModuleV1.reduce(field_state_request)
    )

    task_ref_preserved = (
        bool(task_ref)
        and str(fpo_result.get("task_id") or "") == task_ref
        and str(handoff_result.get("task_id") or "") == task_ref
    )
    if not task_ref_preserved:
        issues.append("task_ref_not_preserved")

    handoff_field_snapshot_ref = str(handoff_result.get("field_snapshot_ref") or "")
    handoff_information_gap_ref = str(handoff_result.get("information_gap_ref") or "")
    observation_refs_preserved = bool(handoff_field_snapshot_ref) and bool(
        handoff_information_gap_ref
    )
    if not observation_refs_preserved:
        issues.append("observation_refs_not_preserved")

    model_requirement_ref = str(
        (handoff_result.get("model_requirement_candidate") or {}).get("requirement_id")
        or ""
    )
    model_provider_refs_preserved = bool(model_requirement_ref) and bool(
        model_result.get("requested_capability")
    )
    if (
        no_eligible_model
        and str(model_result.get("module_status") or "") != "no_eligible_model"
    ):
        model_provider_refs_preserved = False
        issues.append("model_expected_no_eligible_mismatch")
    if not model_provider_refs_preserved:
        issues.append("model_provider_refs_not_preserved")

    trace_replay_ok = _non_empty_trace_replay(
        task_result,
        fpo_result,
        handoff_result,
        vision_result,
        model_result,
        observation_result,
        field_state_result,
    )
    if not trace_replay_ok:
        issues.append("trace_replay_missing")

    boundary_ok = _boundary_ok(
        task_result,
        fpo_result,
        handoff_result,
        vision_result,
        model_result,
        observation_result,
        field_state_result,
    )
    if not boundary_ok:
        issues.append("boundary_violation")

    if (
        low_budget
        and str(fpo_result.get("module_status") or "") != "degraded_resource_plan"
    ):
        issues.append("expected_budget_degraded")

    if (
        observation_blocked
        and str(observation_result.get("module_status") or "") != "request_rejected"
    ):
        issues.append("expected_observation_blocked")

    if (
        no_eligible_model
        and handoff_result.get("observation_request_candidate") is not None
    ):
        issues.append("observation_fabricated_on_no_eligible_model")

    if invalid_task:
        status = str(task_result.get("task_status") or "")
        if status not in {"blocked", "failed"}:
            issues.append("invalid_task_not_contained")

    passed = len(issues) == 0
    return {
        "case_id": case_id,
        "passed": passed,
        "issues": issues,
        "task_status": task_result.get("task_status"),
        "field_perception_status": fpo_result.get("module_status"),
        "handoff_status": handoff_result.get("integration_status"),
        "vision_status": vision_result.get("module_status"),
        "model_status": model_result.get("module_status"),
        "observation_status": observation_result.get("module_status"),
        "field_state_status": field_state_result.get("module_status"),
        "refs": {
            "task_ref": task_ref,
            "field_snapshot_ref": handoff_field_snapshot_ref,
            "information_gap_ref": handoff_information_gap_ref,
            "model_requirement_ref": model_requirement_ref,
            "trace_ref": {
                "task_manager": task_result.get("trace_ref"),
                "field_perception_orchestrator": fpo_result.get("trace_ref"),
                "visual_handoff": handoff_result.get("trace_ref"),
                "vision_manager": vision_result.get("trace_ref"),
                "model_manager": model_result.get("trace_ref"),
                "observation_manager": observation_result.get("trace_ref"),
                "field_state_reducer": field_state_result.get("trace_ref"),
            },
            "replay_key": {
                "task_manager": task_result.get("replay_key"),
                "field_perception_orchestrator": fpo_result.get("replay_key"),
                "visual_handoff": handoff_result.get("replay_key"),
                "vision_manager": vision_result.get("replay_key"),
                "model_manager": model_result.get("replay_key"),
                "observation_manager": observation_result.get("replay_key"),
                "field_state_reducer": field_state_result.get("replay_key"),
            },
        },
        "boundary_preserved": boundary_ok,
        "trace_replay_preserved": trace_replay_ok,
        "unhandled_exceptions": unhandled_exceptions,
    }


def run() -> Dict[str, Any]:
    scenarios = [
        {
            "case_id": "normal_handoff",
            "task_id": "task_sys_normal",
            "low_budget": False,
            "no_eligible_model": False,
            "observation_blocked": False,
            "invalid_task": False,
        },
        {
            "case_id": "degraded_budget",
            "task_id": "task_sys_degraded",
            "low_budget": True,
            "no_eligible_model": False,
            "observation_blocked": False,
            "invalid_task": False,
        },
        {
            "case_id": "no_eligible_model",
            "task_id": "task_sys_no_model",
            "low_budget": False,
            "no_eligible_model": True,
            "observation_blocked": False,
            "invalid_task": False,
        },
        {
            "case_id": "observation_blocked",
            "task_id": "task_sys_obs_blocked",
            "low_budget": False,
            "no_eligible_model": False,
            "observation_blocked": True,
            "invalid_task": False,
        },
        {
            "case_id": "invalid_task",
            "task_id": "task_sys_invalid",
            "low_budget": False,
            "no_eligible_model": False,
            "observation_blocked": False,
            "invalid_task": True,
        },
    ]

    rows: List[Dict[str, Any]] = []
    failed_cases: List[str] = []
    total_unhandled_exceptions = 0

    for scenario in scenarios:
        row = _run_chain(**scenario)
        rows.append(row)
        total_unhandled_exceptions += int(row.get("unhandled_exceptions") or 0)
        if not bool(row.get("passed", False)):
            failed_cases.append(str(row.get("case_id") or "unknown_case"))

    deterministic_a = _run_chain(
        case_id="deterministic_replay",
        task_id="task_sys_deterministic",
        low_budget=False,
        no_eligible_model=False,
        observation_blocked=False,
        invalid_task=False,
    )
    deterministic_b = _run_chain(
        case_id="deterministic_replay",
        task_id="task_sys_deterministic",
        low_budget=False,
        no_eligible_model=False,
        observation_blocked=False,
        invalid_task=False,
    )

    deterministic_ok = deterministic_a.get("refs", {}).get(
        "replay_key"
    ) == deterministic_b.get("refs", {}).get("replay_key")
    deterministic_case = dict(deterministic_a)
    deterministic_case["case_id"] = "deterministic_replay"
    deterministic_case["deterministic_replay_match"] = deterministic_ok
    if not deterministic_ok:
        deterministic_case["passed"] = False
        deterministic_case.setdefault("issues", []).append(
            "deterministic_replay_mismatch"
        )
        failed_cases.append("deterministic_replay")
    rows.append(deterministic_case)
    total_unhandled_exceptions += int(
        deterministic_case.get("unhandled_exceptions") or 0
    )

    scenario_count = len(rows)
    boundary_preserved = all(bool(r.get("boundary_preserved", False)) for r in rows)
    trace_replay_preserved = all(
        bool(r.get("trace_replay_preserved", False)) for r in rows
    )
    deterministic_replay = deterministic_ok
    integration_pass = (
        scenario_count <= 6
        and len(failed_cases) == 0
        and boundary_preserved
        and trace_replay_preserved
        and deterministic_replay
        and total_unhandled_exceptions == 0
    )

    return {
        "module": "luna.system_integration_validation",
        "runner": "run_system_integration_validation_v1",
        "scenario_count": scenario_count,
        "integration_pass": integration_pass,
        "failed_cases": sorted(set(failed_cases)),
        "boundary_preserved": boundary_preserved,
        "deterministic_replay": deterministic_replay,
        "trace_replay_refs_preserved": trace_replay_preserved,
        "unhandled_exceptions": total_unhandled_exceptions,
        "cases": rows,
    }


def main() -> int:
    report = run()
    output_root = (
        REPO_ROOT / "_tmp_eval_out" / "system_integration_validation_v1_smoke_v0"
    )
    output_root.mkdir(parents=True, exist_ok=True)
    output_file = output_root / "system_integration_validation_v1.json"
    output_file.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "integration_pass": report["integration_pass"],
                "scenario_count": report["scenario_count"],
                "failed_cases": report["failed_cases"],
                "boundary_preserved": report["boundary_preserved"],
                "deterministic_replay": report["deterministic_replay"],
                "unhandled_exceptions": report["unhandled_exceptions"],
                "output": str(output_file),
            },
            ensure_ascii=False,
        )
    )
    return 0 if report["integration_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
