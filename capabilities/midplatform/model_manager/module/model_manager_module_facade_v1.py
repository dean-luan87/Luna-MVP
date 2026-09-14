from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.model_manager.module.model_manager_admission_v1 import (
    run_model_admission_v1,
)
from capabilities.midplatform.model_manager.module.model_manager_capability_matcher_v1 import (
    build_capability_match_v1,
)
from capabilities.midplatform.model_manager.module.model_manager_fallback_planner_v1 import (
    build_fallback_candidates_v1,
)
from capabilities.midplatform.model_manager.module.model_manager_health_diagnostics_v1 import (
    build_health_and_diagnostics_v1,
)
from capabilities.midplatform.model_manager.module.model_manager_identity_registry_adapter_v1 import (
    build_identity_registry_view_v1,
)
from capabilities.midplatform.model_manager.module.model_manager_lifecycle_planner_v1 import (
    build_lifecycle_plan_v1,
)
from capabilities.midplatform.model_manager.module.model_manager_module_input_adapter_v1 import (
    adapt_model_manager_input_v1,
)
from capabilities.midplatform.model_manager.module.model_manager_module_output_builder_v1 import (
    build_module_output_v1,
)
from capabilities.midplatform.model_manager.module.model_manager_ownership_resolver_v1 import (
    resolve_ownership_v1,
)
from capabilities.midplatform.model_manager.module.model_manager_resource_evaluator_v1 import (
    evaluate_resources_v1,
)
from capabilities.midplatform.model_manager.module.model_manager_routing_candidate_v1 import (
    build_routing_candidate_v1,
)
from capabilities.midplatform.model_manager.module.model_manager_trace_replay_v1 import (
    build_trace_and_replay_v1,
)


def run_model_manager_module_v1(raw_request: Mapping[str, Any]) -> Dict[str, Any]:
    adapted = adapt_model_manager_input_v1(raw_request)
    request_id = adapted["request_id"]

    if not adapted["input_valid"]:
        trace = build_trace_and_replay_v1(
            request_id=request_id,
            required_capability=adapted["requested_capability"],
            module_status="invalid_input",
            selected_model_candidate={},
            trace_context=adapted["trace_context"],
        )
        health_diag = build_health_and_diagnostics_v1(
            request_id=request_id,
            required_capability=adapted["requested_capability"],
            module_status="invalid_input",
            rejection_reasons=adapted["rejection_reasons"],
            ownership_decision={
                "ownership_ok": False,
                "ownership_reason": "input_invalid",
            },
            resource_evaluation={"resource_ok": False},
            lifecycle_plan={"availability_state": "unavailable"},
        )
        return build_module_output_v1(
            module_status="invalid_input",
            required_capability=adapted["requested_capability"],
            admitted_model_candidates=tuple(),
            rejected_model_candidates=tuple(),
            selected_model_candidate={},
            fallback_candidates=tuple(),
            ownership_decision={
                "ownership_ok": False,
                "ownership_reason": "input_invalid",
            },
            resource_evaluation={"resource_ok": False},
            routing_candidate={},
            lifecycle_plan={"availability_state": "unavailable"},
            health_summary=health_diag["health_summary"],
            rejection_reasons=adapted["rejection_reasons"],
            diagnostics=health_diag["diagnostics"],
            trace_ref=trace["trace_ref"],
            replay_key=trace["replay_key"],
        )

    match = build_capability_match_v1(
        requested_capability=adapted["requested_capability"],
        trace_context=adapted["trace_context"],
        task_ref=adapted["task_ref"],
    )
    required_capability = match["required_capability"]

    identity = build_identity_registry_view_v1(
        requested_capability=required_capability,
        forbidden_model_ids=adapted["forbidden_model_ids"],
    )
    provider_records = identity["eligible_provider_records"]

    if not provider_records:
        trace = build_trace_and_replay_v1(
            request_id=request_id,
            required_capability=required_capability,
            module_status="no_eligible_model",
            selected_model_candidate={},
            trace_context=adapted["trace_context"],
        )
        health_diag = build_health_and_diagnostics_v1(
            request_id=request_id,
            required_capability=required_capability,
            module_status="no_eligible_model",
            rejection_reasons=("no_eligible_model",),
            ownership_decision={
                "ownership_ok": False,
                "ownership_reason": "no_registry_match",
            },
            resource_evaluation={"resource_ok": False},
            lifecycle_plan={"availability_state": "unavailable"},
        )
        return build_module_output_v1(
            module_status="no_eligible_model",
            required_capability=required_capability,
            admitted_model_candidates=tuple(),
            rejected_model_candidates=tuple(),
            selected_model_candidate={},
            fallback_candidates=tuple(),
            ownership_decision={
                "ownership_ok": False,
                "ownership_reason": "no_registry_match",
            },
            resource_evaluation={"resource_ok": False},
            routing_candidate={},
            lifecycle_plan={"availability_state": "unavailable"},
            health_summary=health_diag["health_summary"],
            rejection_reasons=("no_eligible_model",),
            diagnostics=health_diag["diagnostics"],
            trace_ref=trace["trace_ref"],
            replay_key=trace["replay_key"],
        )

    admission = run_model_admission_v1(
        provider_records=provider_records,
        allowed_model_classes=adapted["allowed_model_classes"],
        forbidden_model_ids=adapted["forbidden_model_ids"],
        privacy_requirement=adapted["privacy_requirement"],
    )

    admitted = admission["admitted_model_candidates"]
    rejected = admission["rejected_model_candidates"]

    ownership = resolve_ownership_v1(
        device_ref=adapted["device_ref"],
        region_ref=adapted["region_ref"],
        ownership_context=adapted["ownership_context"],
    )

    resources = evaluate_resources_v1(
        admitted_candidates=admitted,
        resource_snapshot=adapted["resource_snapshot"],
        latency_requirement=adapted["latency_requirement"],
        memory_budget=adapted["memory_budget"],
        offline_required=adapted["offline_required"],
    )

    routing = build_routing_candidate_v1(
        required_capability=required_capability,
        admitted_model_candidates=admitted,
        resource_snapshot=adapted["resource_snapshot"],
    )
    selected = routing["selected_model_candidate"]

    lifecycle = build_lifecycle_plan_v1(
        selected_model_candidate=selected,
        resource_evaluation=resources,
    )

    fallback = build_fallback_candidates_v1(
        admitted_model_candidates=admitted,
        selected_model_candidate=selected,
        rejected_model_candidates=rejected,
    )

    reasons = []
    if admission["admission_rejected"]:
        reasons.append("admission_rejected")
    if ownership["ownership_blocked"]:
        reasons.append("ownership_blocked")
    if resources["resource_insufficient"]:
        reasons.append("resource_insufficient")
    if resources["latency_not_met"]:
        reasons.append("latency_not_met")
    if resources["offline_mismatch"]:
        reasons.append("offline_mismatch")
    if not selected:
        reasons.append("routing_unavailable")

    if admission["admission_rejected"]:
        module_status = "admission_rejected"
    elif ownership["ownership_blocked"]:
        module_status = "ownership_blocked"
    elif resources["resource_insufficient"]:
        module_status = "resource_insufficient"
    elif resources["latency_not_met"]:
        module_status = "degraded"
    elif resources["offline_mismatch"]:
        module_status = "unavailable"
    elif not selected and fallback:
        module_status = "fallback_available"
    elif not selected:
        module_status = "unavailable"
    elif lifecycle.get("plan_status") == "lifecycle_plan_ready":
        module_status = "lifecycle_plan_ready"
    else:
        module_status = "candidate_ready"

    health_diag = build_health_and_diagnostics_v1(
        request_id=request_id,
        required_capability=required_capability,
        module_status=module_status,
        rejection_reasons=tuple(reasons),
        ownership_decision=ownership,
        resource_evaluation=resources,
        lifecycle_plan=lifecycle,
    )

    trace = build_trace_and_replay_v1(
        request_id=request_id,
        required_capability=required_capability,
        module_status=module_status,
        selected_model_candidate=selected,
        trace_context=adapted["trace_context"],
    )

    return build_module_output_v1(
        module_status=module_status,
        required_capability=required_capability,
        admitted_model_candidates=admitted,
        rejected_model_candidates=rejected,
        selected_model_candidate=selected,
        fallback_candidates=fallback,
        ownership_decision=ownership,
        resource_evaluation=resources,
        routing_candidate=routing["routing_candidate"],
        lifecycle_plan=lifecycle,
        health_summary=health_diag["health_summary"],
        rejection_reasons=tuple(reasons),
        diagnostics=health_diag["diagnostics"],
        trace_ref=trace["trace_ref"],
        replay_key=trace["replay_key"],
    )
