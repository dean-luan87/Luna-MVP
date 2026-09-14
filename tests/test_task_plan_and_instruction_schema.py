# -*- coding: utf-8 -*-
"""内部指令与 task_plan 骨架 smoke test。"""

from __future__ import annotations

from shared.schemas.instruction_mapping import InstructionMappingRecord
from shared.schemas.internal_task_instructions_v1 import Navigation, Task as TaskInstr
from shared.schemas.domain_classification import DomainClassificationResult
from shared.schemas.knowledge_collaboration import KnowledgeCollaborationContext, KnowledgeCollaborationResult
from shared.schemas.task_domain_v1 import NAVIGATION, PRIMARY_DOMAIN_V1
from shared.schemas.task_optimization import TaskOptimizationRecord
from shared.schemas.task_plan import PlanChange, PlanDelta, TaskPlan, TaskPlanItem, wrap_plan_delta_nested


def test_instruction_constants() -> None:
    assert Navigation.START == "navigation.start"
    assert TaskInstr.PAUSE == "task.pause"


def test_instruction_mapping_record() -> None:
    r = InstructionMappingRecord(
        human_intent_domain="navigation",
        human_intent_action="go_to_place",
        system_mapping_candidate=Navigation.START,
        required_params=("destination",),
        optional_params=("waypoints", "constraints"),
        requires_confirmation_default=False,
        task_chain_impact_level="high",
        supports_temporary_insertion=True,
        allowed_in_no_task_mode=True,
        allowed_in_task_mode=True,
    )
    d = r.to_dict()
    assert d["system_mapping_candidate"] == "navigation.start"
    assert "destination" in d["required_params"]
    assert d["allowed_in_task_mode"] is True


def test_task_plan_roundtrip_dict() -> None:
    t = TaskPlanItem(
        task_id="task_001",
        task_domain="navigation",
        task_action="start_navigation",
        system_mapping_candidate=Navigation.START,
        target={"destination": "hospital"},
        confidence=0.91,
    )
    p = TaskPlan(
        plan_id="task_plan_v1_xxx",
        plan_version="v1",
        source="raw_user_intent",
        primary_domain=NAVIGATION,
        secondary_domains=["observation"],
        tasks=[t],
        execution_order=["task_001"],
        generated_at="2026-03-30T12:00:00Z",
    )
    out = p.to_dict()
    assert out["plan_version"] == "v1"
    assert out["primary_domain"] == "navigation"
    assert out["tasks"][0]["system_mapping_candidate"] == "navigation.start"
    assert len(PRIMARY_DOMAIN_V1) == 9


def test_plan_delta_wrap() -> None:
    delta = PlanDelta(
        delta_id="pd_1",
        from_plan_id="plan_v1_001",
        to_plan_id="plan_v2_001",
        changes=[
            PlanChange(change_type="reorder", task_id="task_002", details="moved before task_001"),
            PlanChange(change_type="field_autofill", task_id="task_001", details="destination from history"),
        ],
    )
    w = wrap_plan_delta_nested(delta)
    assert w["plan_delta"]["from_plan_id"] == "plan_v1_001"
    assert w["plan_delta"]["changes"][0]["task_id"] == "task_002"
    assert w["plan_delta"]["changes"][1]["change_type"] == "field_autofill"


def test_domain_classification_result() -> None:
    d = DomainClassificationResult(
        primary_domain="navigation",
        secondary_domains=["observation"],
        intent_complexity="multi_step",
        can_map_to_system_tasks=True,
        confidence=0.89,
    )
    js = d.to_dict()
    assert js["primary_domain"] == "navigation"
    assert js["intent_complexity"] == "multi_step"
    assert js["should_reject"] is False


def test_knowledge_collaboration_and_optimization_placeholders() -> None:
    ctx = KnowledgeCollaborationContext(base_plan_id="plan_v1_001", user_literal_constraints=["先去商场"])
    assert ctx.base_plan_id == "plan_v1_001"
    res = KnowledgeCollaborationResult(
        result_id="kcr_1",
        base_plan_id="plan_v1_001",
        knowledge_sources=["library.v1"],
    )
    assert res.to_dict()["constraints_respected"] is True
    opt = TaskOptimizationRecord(
        optimization_id="opt_1",
        source_plan_id="plan_v1_001",
        target_plan_id="plan_v2_001",
        optimization_reason="store_is_on_route",
        changes_summary=["reorder task_002 before task_001"],
    )
    assert opt.to_dict()["requires_confirmation"] is True
