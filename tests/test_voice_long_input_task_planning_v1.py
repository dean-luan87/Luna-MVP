# -*- coding: utf-8 -*-
"""语音长输入拆解 v1：分类 → 映射 → task_plan_v1。"""

from __future__ import annotations

from shared.schemas.task_domain_v1 import NAVIGATION, OBSERVATION, UNSUPPORTED_OR_REJECT

from capabilities.voice.bridge.voice_long_input_task_planner import run_long_input_task_planning_v1


def test_scenario1_single_navigation() -> None:
    r = run_long_input_task_planning_v1("带我去医院")
    assert r.rejection_needed is False
    assert r.domain_result.primary_domain == NAVIGATION
    assert r.task_plan_v1 is not None
    assert r.task_plan_v1.plan_version == "v1"
    assert len(r.task_plan_v1.tasks) == 1
    assert r.task_plan_v1.tasks[0].system_mapping_candidate.startswith("navigation.start")
    assert r.task_plan_v1.knowledge_collaboration_pending is True
    assert r.task_plan_v1.next_stage == "knowledge_collaboration_and_optimization"


def test_scenario2_find_phone() -> None:
    r = run_long_input_task_planning_v1("帮我找手机")
    assert r.domain_result.primary_domain == OBSERVATION
    assert r.task_plan_v1 is not None
    assert "find_object" in r.task_plan_v1.tasks[0].system_mapping_candidate


def test_scenario3_sequential_two_tasks() -> None:
    r = run_long_input_task_planning_v1("先去商场，再找便利店买点吃的")
    assert r.task_plan_v1 is not None
    assert len(r.task_plan_v1.execution_order) == 2
    assert r.task_plan_v1.execution_order[0] == "task_001"
    assert r.task_plan_v1.execution_order[1] == "task_002"


def test_scenario4_conditional() -> None:
    r = run_long_input_task_planning_v1("先去便利店，如果太远就算了")
    assert r.task_plan_v1 is not None
    assert len(r.task_plan_v1.tasks) == 1
    assert "conditional_clauses" in (r.task_plan_v1.tasks[0].target or {})


def test_scenario5_accompanying_observation() -> None:
    r = run_long_input_task_planning_v1("去医院，路上顺便看看有没有便利店")
    assert r.task_plan_v1 is not None
    assert len(r.task_plan_v1.tasks) >= 2
    kinds = [t.system_mapping_candidate for t in r.task_plan_v1.tasks]
    assert any(k.startswith("navigation.") for k in kinds)
    assert any(k.startswith("observation.") for k in kinds)


def test_scenario6_unsupported() -> None:
    r = run_long_input_task_planning_v1("帮我自动挂号")
    assert r.domain_result.primary_domain == UNSUPPORTED_OR_REJECT
    assert r.rejection_needed is True
    assert r.task_plan_v1 is None


def test_scenario7_too_many_segments() -> None:
    r = run_long_input_task_planning_v1("去东，去南，去西，去北，去中")
    assert r.clarification_needed is True
    assert r.task_plan_v1 is None
    assert "too_many" in (r.notes or "")
