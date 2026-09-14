# -*- coding: utf-8 -*-
"""
从域分类 + 指令候选生成 task_plan_v1（不做 V2/环境/图书馆）。
"""

from __future__ import annotations

import uuid
from typing import List

from shared.schemas.domain_classification import DomainClassificationResult
from shared.schemas.task_plan import TaskPlan, TaskPlanItem
from shared.schemas.task_domain_v1 import (
    DEVICE_CONTROL,
    NAVIGATION,
    OBSERVATION,
    TASK_CONTROL,
    TASK_QUERY,
)

from capabilities.voice.schemas.voice_long_input_instruction_candidate import VoiceLongInputInstructionCandidate


def _action_label(sid: str) -> str:
    return sid.split(".")[-1].replace("_", " ")


def _task_domain_for_candidate(sid: str) -> str:
    if sid.startswith("navigation."):
        return NAVIGATION
    if sid.startswith("observation."):
        return OBSERVATION
    if sid.startswith("device."):
        return DEVICE_CONTROL
    if sid.startswith("task.query"):
        return TASK_QUERY
    if sid.startswith("task."):
        return TASK_CONTROL
    return NAVIGATION


def build_task_plan_v1_from_candidates(
    *,
    plan_id: str,
    domain: DomainClassificationResult,
    candidates: List[VoiceLongInputInstructionCandidate],
    clarification_needed: bool,
    rejection_needed: bool,
    generated_at: str,
) -> TaskPlan:
    """组装 TaskPlan（plan_version 固定 v1）。"""
    tasks: List[TaskPlanItem] = []
    order: List[str] = []

    for i, cand in enumerate(candidates):
        tid = f"task_{i+1:03d}"
        order.append(tid)
        dep = None
        if cand.relation_hint == "accompanying" and i > 0:
            dep = order[0] if order else None
        tasks.append(
            TaskPlanItem(
                task_id=tid,
                task_domain=_task_domain_for_candidate(cand.system_mapping_candidate),
                task_action=_action_label(cand.system_mapping_candidate),
                system_mapping_candidate=cand.system_mapping_candidate,
                target=dict(cand.param_candidates),
                constraints=[],
                priority="primary" if i == 0 else "secondary",
                dependency=dep,
                is_temporary=False,
                requires_confirmation=cand.requires_confirmation_candidate,
                confidence=cand.confidence,
                metadata={
                    "segment_text": cand.segment_text,
                    "relation_hint": cand.relation_hint,
                },
            )
        )

    return TaskPlan(
        plan_id=plan_id,
        plan_version="v1",
        source="raw_user_intent",
        primary_domain=domain.primary_domain,
        secondary_domains=list(domain.secondary_domains),
        tasks=tasks,
        execution_order=order,
        clarification_needed=clarification_needed,
        confirmation_needed=domain.needs_confirmation,
        optimization_applied=False,
        optimization_reason=None,
        generated_at=generated_at,
        knowledge_collaboration_pending=True,
        task_optimization_pending=True,
        next_stage="knowledge_collaboration_and_optimization",
        metadata={},
    )


def new_plan_id() -> str:
    return f"plan_v1_{uuid.uuid4().hex[:12]}"
