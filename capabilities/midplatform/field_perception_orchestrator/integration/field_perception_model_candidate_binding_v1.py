from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.model_manager.module.model_manager_module_api_v1 import (
    run_model_manager_module_api_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_to_model_manager_requirement_adapter_v1 import (
    normalize_visual_capabilities_for_model_manager_v1,
)


def _bind_candidate(
    row: Mapping[str, Any], ownership_ok: bool, resource_ok: bool
) -> Dict[str, Any]:
    model_id = str(row.get("model_id") or "")
    admission = str(row.get("admission_status") or "pending")
    capability_match = True
    availability = "available"
    version_status = "compatible"
    ownership_status = "valid" if ownership_ok else "invalid"
    resource_fit = bool(resource_ok)
    admitted = (
        capability_match
        and admission in {"admitted", "active", ""}
        and availability == "available"
        and resource_fit
        and ownership_status == "valid"
        and version_status == "compatible"
    )
    return {
        "model_asset_id": model_id,
        "capability_match": capability_match,
        "admission_status": "admitted" if admitted else (admission or "rejected"),
        "availability_status": availability,
        "resource_fit": resource_fit,
        "ownership_status": ownership_status,
        "version_status": version_status,
        "selection_reason": "qualified_for_binding"
        if admitted
        else "failed_binding_constraints",
    }


def build_model_candidate_binding_v1(
    input_candidate: Mapping[str, Any],
    model_requirement_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    budget = dict(input_candidate.get("resource_budget") or {})
    normalized_required_capabilities = tuple(
        str(x)
        for x in (
            model_requirement_candidate.get("required_capabilities")
            or normalize_visual_capabilities_for_model_manager_v1(
                tuple(
                    str(x)
                    for x in (
                        model_requirement_candidate.get(
                            "source_effective_capability_plan"
                        )
                        or ()
                    )
                )
            )
        )
    )
    requested_capability = str(
        model_requirement_candidate.get("primary_required_capability")
        or (
            normalized_required_capabilities[0]
            if normalized_required_capabilities
            else "unknown_scene_reasoning"
        )
    )
    mm_payload = {
        "request_id": f"model_mgr_req::{model_requirement_candidate.get('requirement_id')}",
        "requested_capability": requested_capability,
        "task_ref": input_candidate.get("task_id"),
        "device_ref": str(
            (model_requirement_candidate.get("device_constraints") or {}).get(
                "device_ref"
            )
            or "device_main"
        ),
        "region_ref": str(
            (model_requirement_candidate.get("device_constraints") or {}).get(
                "region_ref"
            )
            or "region_main"
        ),
        "resource_snapshot": {
            "memory_available": int(
                model_requirement_candidate.get("memory_budget") or 2048
            ),
            "memory_mb": int(model_requirement_candidate.get("memory_budget") or 2048),
            "latency_ms": int(
                budget.get("latency_budget") or budget.get("latency_budget_ms") or 1200
            ),
            "cpu_load_percent": float(budget.get("cpu_load_percent") or 40),
            "gpu_memory_available_gb": float(
                budget.get("gpu_memory_available_gb") or 4
            ),
            "gpu_memory_required_gb": float(budget.get("gpu_memory_required_gb") or 1),
            "concurrent_limit": int(budget.get("concurrent_invocation_limit") or 2),
            "concurrent_slots_used": int(budget.get("concurrent_slots_used") or 0),
            "runtime_status": "available",
            "api_quota_available": True,
        },
        "allowed_model_classes": tuple(
            model_requirement_candidate.get("preferred_model_classes") or ()
        ),
        "forbidden_model_ids": tuple(budget.get("forbidden_model_ids") or ()),
        "latency_requirement": int(
            budget.get("latency_budget") or budget.get("latency_budget_ms") or 1200
        ),
        "memory_budget": int(model_requirement_candidate.get("memory_budget") or 2048),
        "offline_required": bool(budget.get("offline_required", False)),
        "privacy_requirement": str(budget.get("privacy_requirement") or "normal"),
        "ownership_context": dict(budget.get("ownership_context") or {}),
        "version_snapshot": dict(
            model_requirement_candidate.get("version_constraints") or {}
        ),
        "trace_context": dict(input_candidate.get("trace_context") or {}),
    }

    mm_result = run_model_manager_module_api_v1(mm_payload)
    ownership_ok = bool(
        (mm_result.get("ownership_decision") or {}).get("ownership_ok", True)
    )
    resource_ok = bool(
        (mm_result.get("resource_evaluation") or {}).get("resource_ok", True)
    )

    eligible = []
    rejected = []
    for row in tuple(
        mm_result.get("admitted_model_candidates") or ()
    ):  # admitted from manager
        bound = _bind_candidate(row, ownership_ok, resource_ok)
        if (
            bound["capability_match"]
            and bound["admission_status"] == "admitted"
            and bound["availability_status"] == "available"
            and bound["resource_fit"]
            and bound["ownership_status"] == "valid"
            and bound["version_status"] == "compatible"
        ):
            eligible.append(bound)
        else:
            rejected.append(bound)

    for row in tuple(
        mm_result.get("rejected_model_candidates") or ()
    ):  # explicit rejects
        rejected.append(
            {
                "model_asset_id": str(row.get("model_id") or ""),
                "capability_match": True,
                "admission_status": "rejected",
                "availability_status": "available",
                "resource_fit": bool(resource_ok),
                "ownership_status": "valid" if ownership_ok else "invalid",
                "version_status": "compatible",
                "selection_reason": ",".join(
                    tuple(
                        row.get("rejection_reasons") or ("rejected_by_model_manager",)
                    )
                ),
            }
        )

    fallback = []
    for row in tuple(mm_result.get("fallback_candidates") or ()):  # fallback list
        fallback.append(
            {
                "model_asset_id": str(row.get("model_id") or ""),
                "capability_match": True,
                "admission_status": "admitted",
                "availability_status": "available",
                "resource_fit": bool(resource_ok),
                "ownership_status": "valid" if ownership_ok else "invalid",
                "version_status": "compatible",
                "selection_reason": "fallback_candidate",
            }
        )

    return {
        "eligible_model_candidates": tuple(eligible),
        "rejected_model_candidates": tuple(rejected),
        "fallback_model_candidates": tuple(fallback),
        "model_manager_result": {
            "module_status": mm_result.get("module_status"),
            "trace_ref": mm_result.get("trace_ref"),
            "replay_key": mm_result.get("replay_key"),
            "rejection_reasons": tuple(mm_result.get("rejection_reasons") or ()),
            "requested_capability": requested_capability,
            "normalized_required_capabilities": normalized_required_capabilities,
        },
    }
