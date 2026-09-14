from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.field_perception_orchestrator.module.field_perception_capability_planner_v1 import (
    build_field_perception_capability_plan_v1,
)
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_diagnostics_v1 import (
    build_field_perception_diagnostics_v1,
)
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_field_snapshot_adapter_v1 import (
    build_field_perception_snapshot_v1,
)
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_information_gap_detector_v1 import (
    build_field_perception_information_gap_v1,
)
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_invocation_history_v1 import (
    build_field_perception_invocation_history_assessment_v1,
)
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_model_requirement_builder_v1 import (
    build_field_perception_model_requirements_v1,
)
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_module_input_adapter_v1 import (
    adapt_field_perception_input_v1,
)
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_module_types_v1 import (
    BOUNDARY_FALSE_FIELDS,
    CAPABILITY_ID,
    not_fact,
)
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_observation_goal_builder_v1 import (
    build_field_perception_observation_goal_v1,
)
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_plan_builder_v1 import (
    build_field_perception_plan_v1,
)
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_reobservation_policy_v1 import (
    build_field_perception_reobservation_policy_v1,
)
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_region_planner_v1 import (
    build_field_perception_region_plan_v1,
)
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_resource_budget_v1 import (
    build_field_perception_resource_budget_plan_v1,
)
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_stop_condition_v1 import (
    build_field_perception_stop_condition_v1,
)
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_task_goal_resolver_v1 import (
    build_field_perception_task_goal_resolution_v1,
)
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_trace_replay_v1 import (
    build_field_perception_trace_replay_v1,
)
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_vision_handoff_v1 import (
    build_field_perception_vision_handoff_candidate_v1,
)


def _resolve_module_status_v1(
    input_candidate: Mapping[str, Any],
    information_gap: Mapping[str, Any],
    history_assessment: Mapping[str, Any],
    resource_plan: Mapping[str, Any],
) -> str:
    if not bool(input_candidate.get("input_valid", False)):
        return "invalid_input"
    if bool(history_assessment.get("suppress_reinvocation", False)):
        return "no_visual_invocation_required"
    if not bool(information_gap.get("need_visual_invocation", False)):
        return "no_visual_invocation_required"
    if bool(resource_plan.get("resource_degraded", False)):
        return "degraded_resource_plan"
    return "plan_candidate_ready"


def run_field_perception_orchestrator_module_v1(
    payload: Mapping[str, Any],
) -> Dict[str, Any]:
    try:
        input_candidate = adapt_field_perception_input_v1(payload)
        task_goal_resolution = build_field_perception_task_goal_resolution_v1(
            input_candidate
        )
        field_snapshot = build_field_perception_snapshot_v1(input_candidate)
        information_gap = build_field_perception_information_gap_v1(
            task_goal_resolution,
            field_snapshot,
            input_candidate.get("uncertainty_state") or {},
            input_candidate.get("conflict_state") or {},
            input_candidate.get("recent_observation_summary") or {},
        )
        observation_goal = build_field_perception_observation_goal_v1(
            task_goal_resolution,
            information_gap,
        )
        history_assessment = build_field_perception_invocation_history_assessment_v1(
            tuple(input_candidate.get("previous_invocation_history") or ()),
            str(observation_goal.get("observation_goal") or ""),
        )
        region_plan = build_field_perception_region_plan_v1(
            observation_goal, field_snapshot
        )
        capability_plan = build_field_perception_capability_plan_v1(
            observation_goal,
            tuple(input_candidate.get("available_visual_capabilities") or ()),
        )
        model_requirements = build_field_perception_model_requirements_v1(
            capability_plan,
            tuple(input_candidate.get("available_model_assets") or ()),
            input_candidate.get("temporal_context") or {},
        )
        resource_plan = build_field_perception_resource_budget_plan_v1(
            input_candidate.get("resource_budget") or {},
            tuple(capability_plan.get("requested_visual_capabilities") or ()),
        )
        module_status = _resolve_module_status_v1(
            input_candidate,
            information_gap,
            history_assessment,
            resource_plan,
        )
        stop_condition = build_field_perception_stop_condition_v1(
            information_gap,
            observation_goal,
        )
        reobservation_policy = build_field_perception_reobservation_policy_v1(
            information_gap,
            input_candidate.get("temporal_context") or {},
        )
        trace = build_field_perception_trace_replay_v1(
            input_candidate,
            module_status,
            str(observation_goal.get("observation_goal") or ""),
        )
        plan = build_field_perception_plan_v1(
            input_candidate,
            field_snapshot,
            observation_goal,
            information_gap,
            region_plan,
            capability_plan,
            model_requirements,
            resource_plan,
            stop_condition,
            reobservation_policy,
            str(trace.get("trace_ref") or ""),
            str(trace.get("replay_key") or ""),
        )
        need_handoff = module_status in {
            "plan_candidate_ready",
            "degraded_resource_plan",
        }
        handoff = build_field_perception_vision_handoff_candidate_v1(plan, need_handoff)
        diagnostics = build_field_perception_diagnostics_v1(
            input_candidate,
            module_status,
            information_gap,
            capability_plan,
            resource_plan,
        )

        output = {
            "capability_id": CAPABILITY_ID,
            "module_status": module_status,
            "task_id": input_candidate.get("task_id"),
            "field_perception_plan": plan,
            "vision_handoff_candidate": handoff.get("vision_handoff_candidate"),
            "diagnostics": diagnostics,
            "trace_ref": trace.get("trace_ref"),
            "replay_key": trace.get("replay_key"),
            "boundary_flags": {field: False for field in BOUNDARY_FALSE_FIELDS},
            "task_goal_resolution": task_goal_resolution,
            "information_gap": information_gap,
            "observation_goal": observation_goal,
            "region_plan": region_plan,
            "capability_plan": capability_plan,
            "model_requirements": model_requirements,
            "resource_plan": resource_plan,
            "history_assessment": history_assessment,
            "stop_condition": stop_condition,
            "reobservation_policy": reobservation_policy,
            **not_fact(),
            "unhandled_exception": False,
        }
        for field in BOUNDARY_FALSE_FIELDS:
            output[field] = False
        return output
    except Exception:  # noqa: BLE001
        return {
            "capability_id": CAPABILITY_ID,
            "module_status": "internal_error",
            "task_id": "",
            "field_perception_plan": {},
            "vision_handoff_candidate": {},
            "diagnostics": {},
            "trace_ref": "",
            "replay_key": "",
            "boundary_flags": {},
            "unhandled_exception": True,
            **not_fact(),
        }
