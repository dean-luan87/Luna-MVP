from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Tuple


def _mk_subtask(
    *,
    subtask_id: str,
    parent_task_id: str,
    capability_id: str,
    objective: str,
    dependencies: Iterable[str],
    expected_output: str,
    completion_condition: str,
    failure_policy: str,
    retry_policy: str,
    optional: bool,
    status: str,
) -> Dict[str, Any]:
    return {
        "subtask_id": subtask_id,
        "parent_task_id": parent_task_id,
        "capability_id": capability_id,
        "objective": objective,
        "dependencies": tuple(str(x) for x in dependencies),
        "expected_output": expected_output,
        "completion_condition": completion_condition,
        "failure_policy": failure_policy,
        "retry_policy": retry_policy,
        "optional": optional,
        "status": status,
    }


def decompose_task_v1(
    *,
    task_id: str,
    task_type: str,
    task_goal: str,
    capability_requirements: Tuple[str, ...],
    dependency_refs: Tuple[str, ...],
    decomposition_mode: str = "atomic",
) -> Dict[str, Any]:
    req_caps = capability_requirements or ("luna.task_manager",)
    subtasks: List[Dict[str, Any]] = []

    if decomposition_mode == "sequential":
        for idx, cap in enumerate(req_caps, start=1):
            deps = () if idx == 1 else (f"{task_id}_subtask_{idx - 1}",)
            subtasks.append(
                _mk_subtask(
                    subtask_id=f"{task_id}_subtask_{idx}",
                    parent_task_id=task_id,
                    capability_id=cap,
                    objective=f"sequential_step_{idx}:{task_goal}",
                    dependencies=deps,
                    expected_output=f"output_step_{idx}",
                    completion_condition="subtask_candidate_ready",
                    failure_policy="stop_on_failure",
                    retry_policy="retry_once",
                    optional=False,
                    status="planned",
                )
            )
    elif decomposition_mode == "parallel":
        for idx, cap in enumerate(req_caps, start=1):
            subtasks.append(
                _mk_subtask(
                    subtask_id=f"{task_id}_parallel_{idx}",
                    parent_task_id=task_id,
                    capability_id=cap,
                    objective=f"parallel_step_{idx}:{task_goal}",
                    dependencies=dependency_refs,
                    expected_output=f"output_parallel_{idx}",
                    completion_condition="subtask_candidate_ready",
                    failure_policy="partial_allowed",
                    retry_policy="retry_once",
                    optional=False,
                    status="planned",
                )
            )
    elif decomposition_mode == "conditional":
        primary = req_caps[0]
        secondary = req_caps[1] if len(req_caps) > 1 else req_caps[0]
        subtasks.extend(
            [
                _mk_subtask(
                    subtask_id=f"{task_id}_condition_eval",
                    parent_task_id=task_id,
                    capability_id="luna.task_manager",
                    objective="evaluate_condition",
                    dependencies=dependency_refs,
                    expected_output="condition_result",
                    completion_condition="condition_evaluated",
                    failure_policy="stop_on_failure",
                    retry_policy="retry_once",
                    optional=False,
                    status="planned",
                ),
                _mk_subtask(
                    subtask_id=f"{task_id}_conditional_true",
                    parent_task_id=task_id,
                    capability_id=primary,
                    objective=f"conditional_true:{task_goal}",
                    dependencies=(f"{task_id}_condition_eval",),
                    expected_output="conditional_true_output",
                    completion_condition="subtask_candidate_ready",
                    failure_policy="fallback_to_false_branch",
                    retry_policy="retry_once",
                    optional=False,
                    status="planned",
                ),
                _mk_subtask(
                    subtask_id=f"{task_id}_conditional_false",
                    parent_task_id=task_id,
                    capability_id=secondary,
                    objective=f"conditional_false:{task_goal}",
                    dependencies=(f"{task_id}_condition_eval",),
                    expected_output="conditional_false_output",
                    completion_condition="subtask_candidate_ready",
                    failure_policy="stop_on_failure",
                    retry_policy="retry_once",
                    optional=True,
                    status="planned",
                ),
            ]
        )
    else:
        subtasks.append(
            _mk_subtask(
                subtask_id=f"{task_id}_atomic_1",
                parent_task_id=task_id,
                capability_id=req_caps[0],
                objective=task_goal,
                dependencies=dependency_refs,
                expected_output="atomic_output",
                completion_condition="subtask_candidate_ready",
                failure_policy="retry_or_replan",
                retry_policy="retry_once",
                optional=False,
                status="planned",
            )
        )

    # Always keep verification and recovery tasks as structural candidates.
    subtasks.append(
        _mk_subtask(
            subtask_id=f"{task_id}_verification",
            parent_task_id=task_id,
            capability_id="luna.task_manager",
            objective="verification_task",
            dependencies=tuple(s["subtask_id"] for s in subtasks if not s["optional"]),
            expected_output="verification_summary",
            completion_condition="all_required_subtasks_decided",
            failure_policy="raise_partial_failure",
            retry_policy="no_retry",
            optional=False,
            status="planned",
        )
    )
    subtasks.append(
        _mk_subtask(
            subtask_id=f"{task_id}_recovery",
            parent_task_id=task_id,
            capability_id="luna.task_manager",
            objective="recovery_task",
            dependencies=(f"{task_id}_verification",),
            expected_output="recovery_candidate",
            completion_condition="failure_or_partial_detected",
            failure_policy="human_review_required",
            retry_policy="no_retry",
            optional=True,
            status="planned",
        )
    )

    return {
        "task_plan": {
            "task_id": task_id,
            "task_goal": task_goal,
            "task_type": task_type,
            "decomposition_mode": decomposition_mode,
            "subtask_count": len(subtasks),
        },
        "subtasks": tuple(subtasks),
    }
