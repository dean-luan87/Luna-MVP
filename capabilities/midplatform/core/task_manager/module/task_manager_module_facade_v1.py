from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Mapping

from capabilities.midplatform.task_manager_core_orchestration_builders_v1 import (
    build_candidate_route_candidate,
    build_module_handoff_candidate,
    build_orchestration_plan_candidate,
)
from capabilities.midplatform.task_manager_core_orchestration_types_v1 import (
    OrchestrationInputCandidate,
)

from .task_manager_capability_router_v1 import build_capability_routes_v1
from .task_manager_dependency_resolver_v1 import (
    enforce_waiting_dependency_rule_v1,
    resolve_dependencies_v1,
)
from .task_manager_interruption_recovery_v1 import (
    build_interruption_state_v1,
    build_recovery_candidates_v1,
)
from .task_manager_module_diagnostics_v1 import build_task_manager_diagnostics_v1
from .task_manager_module_input_adapter_v1 import adapt_task_manager_input_v1
from .task_manager_module_status_resolver_v1 import resolve_task_manager_module_status
from .task_manager_result_aggregator_v1 import aggregate_task_result_v1
from .task_manager_task_decomposition_v1 import decompose_task_v1
from .task_manager_task_lifecycle_v1 import (
    build_state_manager_snapshot_v1,
    next_status_v1,
)


class TaskManagerModuleV1:
    def handle(self, request: Mapping[str, Any]) -> Dict[str, Any]:
        step_results = []

        # 1) input adaptation and static checks
        adapted = adapt_task_manager_input_v1(request)
        step_results.append(
            {"step": "input_adaptation", "ok": bool(adapted["adapted_input_ok"])}
        )

        task_id = adapted["task_request_id"] or "tm_missing_id"
        trace_ref = f"tm_module_trace_{task_id}"
        replay_key = f"tm_module_replay_{task_id}"

        blocking_reasons = list(adapted["rejection_reasons"])
        current_status = "received"

        # 2) admission
        admitted = adapted["adapted_input_ok"]
        if not admitted:
            blocking_reasons.append("input_not_admitted")
        current_status = "admitted" if admitted else "blocked"
        step_results.append({"step": "admission", "ok": admitted})

        # 3) dependency resolution
        dep = resolve_dependencies_v1(
            dependency_refs=adapted["dependency_refs"],
            dependency_snapshot=request.get("dependency_snapshot") or {},
        )
        step_results.append(
            {"step": "dependency_resolution", "ok": not dep["dependency_waiting"]}
        )

        # 4) decomposition
        decomp = decompose_task_v1(
            task_id=task_id,
            task_type=adapted["task_type"],
            task_goal=adapted["task_goal"],
            capability_requirements=adapted["capability_requirements"],
            dependency_refs=adapted["dependency_refs"],
            decomposition_mode=str(request.get("decomposition_mode", "atomic")),
        )
        step_results.append({"step": "task_decomposition", "ok": True})

        # 5) capability routing
        routes = build_capability_routes_v1(
            capability_requirements=adapted["capability_requirements"],
            request_payload_seed={"task_id": task_id, "trace_ref": trace_ref},
        )
        if routes["blocked_capabilities"]:
            blocking_reasons.append("capability_unavailable")
        step_results.append(
            {
                "step": "capability_routing",
                "ok": len(routes["blocked_capabilities"]) == 0,
            }
        )

        # 6) lifecycle transition
        waiting_rule = enforce_waiting_dependency_rule_v1(
            current_status="planned" if admitted else "blocked",
            waiting_dependency_refs=dep["waiting_dependency_refs"],
        )
        lifecycle = next_status_v1(
            current_status="planned" if admitted else "blocked",
            dependency_unresolved=dep["dependency_waiting"],
            interruption_reason=str(request.get("interruption_reason", "")),
            recovery_decision=str(request.get("recovery_decision", "")),
            completion_status=str(request.get("completion_status", "")),
            requested_control=str(request.get("requested_control", "")),
            has_blocking_reason=len(blocking_reasons) > 0,
        )
        current_status = lifecycle["task_status"]
        step_results.append(
            {"step": "lifecycle", "ok": lifecycle["transition_allowed"]}
        )

        # 7) interruption
        interruption_state = build_interruption_state_v1(
            interruption_policy=adapted["interruption_policy"],
            requested_control=str(request.get("requested_control", "")),
            interruption_reason=str(request.get("interruption_reason", "")),
            current_status=current_status,
        )
        step_results.append({"step": "interruption", "ok": True})

        # 8) recovery planning
        failure_type = ""
        if "permission_denied" in blocking_reasons:
            failure_type = "permission_denied"
        elif dep["dependency_waiting"]:
            failure_type = "dependency_unavailable"
        elif "capability_unavailable" in blocking_reasons:
            failure_type = "capability_unavailable"
        recovery_candidates = build_recovery_candidates_v1(
            failure_type=failure_type,
            recovery_policy=adapted["recovery_policy"],
        )
        step_results.append({"step": "recovery_planning", "ok": True})

        # 9) bridge to existing orchestration builder contracts
        orchestr_in = OrchestrationInputCandidate(
            candidate_id=f"tm_orch_{task_id}",
            source_module_ref="task_manager_module_facade_v1",
            boundary_registry_ref="luna_boundary_registry_v1",
            lifecycle_state_ref=current_status,
            alignment_rule_ref="task_manager_alignment_rule_v1",
            governance_constraint_ref=str(
                adapted["permission_snapshot"].get(
                    "governance_ref", "governance_missing"
                )
            ),
            protocol_trace_ref=trace_ref,
            traceability_refs=tuple(request.get("context_refs") or ())
            + tuple(request.get("decision_refs") or ()),
            governance_refs=(
                str(
                    adapted["permission_snapshot"].get(
                        "governance_ref", "governance_missing"
                    )
                ),
            ),
        )
        plan_candidate = build_orchestration_plan_candidate(orchestr_in)
        route_candidate = build_candidate_route_candidate(
            plan_candidate,
            route_target_module_ref=str(
                adapted["capability_requirements"][0]
                if adapted["capability_requirements"]
                else "luna.task_manager"
            ),
        )
        handoff_candidate = build_module_handoff_candidate(route_candidate)
        step_results.append({"step": "orchestration_bridge", "ok": True})

        # 10) snapshot
        state_snapshot = build_state_manager_snapshot_v1(
            task_id=task_id,
            task_status=current_status,
            subtasks=decomp["subtasks"],
            blocking_reasons=blocking_reasons,
            waiting_dependencies=dep["waiting_dependency_refs"],
            recovery_point=str(request.get("recovery_point", "")),
            failure_reason=str(request.get("failure_reason", "")),
            cancel_reason=str(request.get("cancel_reason", "")),
            terminate_reason=str(request.get("terminate_reason", "")),
        )
        step_results.append({"step": "state_snapshot", "ok": True})

        historical_blocking_reasons = tuple(blocking_reasons) + tuple(
            lifecycle["blocking_reasons"]
        )
        failed_subtasks = sum(
            1 for s in decomp["subtasks"] if str(s.get("status", "")) == "failed"
        )
        unresolved_subtasks = sum(
            1
            for s in decomp["subtasks"]
            if str(s.get("status", "")) not in {"completed", "cancelled", "terminated"}
        )
        status_resolution = resolve_task_manager_module_status(
            lifecycle_status=lifecycle["task_status"],
            task_status=current_status,
            dependency_status=dep,
            result_completion_status=str(request.get("completion_status", "")),
            interruption_status=interruption_state,
            recovery_status={
                "failure_type": failure_type,
                "candidate_count": len(recovery_candidates),
            },
            blocking_reasons=historical_blocking_reasons,
            failed_subtasks=failed_subtasks,
            unresolved_subtasks=unresolved_subtasks,
            cancelled_reason=str(request.get("cancel_reason", "")),
            termination_reason=str(request.get("terminate_reason", "")),
            requested_control=str(request.get("requested_control", "")),
        )
        current_status = status_resolution["module_status"]

        # 11) aggregate
        merged_exec_candidates = tuple(routes["execution_request_candidates"]) + (
            {
                "requested_capability_id": route_candidate.route_target_module_ref,
                "capability_status": "orchestration_candidate",
                "module_api_ref": None,
                "request_payload_candidate": {
                    "orchestration_input": asdict(orchestr_in),
                    "orchestration_plan": asdict(plan_candidate),
                    "router_candidate": asdict(route_candidate),
                    "handoff_candidate": asdict(handoff_candidate),
                    "waiting_rule": waiting_rule,
                },
                "dependency_order": 0,
                "fallback_candidate": "fallback_candidate",
                "routing_status": "integration_candidate",
            },
        )
        result = aggregate_task_result_v1(
            task_id=task_id,
            task_status=current_status,
            subtasks=decomp["subtasks"],
            execution_request_candidates=merged_exec_candidates,
            dependency_status=dep,
            interruption_state=interruption_state,
            recovery_candidates=recovery_candidates,
            current_blocking_reasons=status_resolution["current_blocking_reasons"],
            historical_blocking_reasons=status_resolution[
                "historical_blocking_reasons"
            ],
            status_resolution=status_resolution,
        )
        step_results.append({"step": "result_aggregation", "ok": True})

        # 12) diagnostics finalization
        diagnostics = build_task_manager_diagnostics_v1(
            step_results=step_results,
            rejection_reasons=adapted["rejection_reasons"],
            current_blocking_reasons=status_resolution["current_blocking_reasons"],
            historical_blocking_reasons=status_resolution[
                "historical_blocking_reasons"
            ],
            trace_ref=trace_ref,
            replay_key=replay_key,
        )

        result["diagnostics"] = diagnostics
        result["trace_ref"] = trace_ref
        result["replay_key"] = replay_key
        result["version_snapshots"] = adapted["version_snapshots"]
        result["action_execution_executed"] = False
        result["model_call_executed"] = False
        result["state_mutation_executed"] = False
        result["fact_promotion_executed"] = False
        result["runtime_dispatch_executed"] = False
        result["state_snapshot"] = state_snapshot
        return result
