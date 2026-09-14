# -*- coding: utf-8 -*-
"""长语音输入模式 v1.1：任务 / 混合 / 非任务 + non_task_payload。"""

from __future__ import annotations

from shared.schemas.task_domain_v1 import NON_TASK_DIALOGUE_FUTURE

from capabilities.voice.bridge.voice_long_input_task_planner import run_long_input_task_planning_v1


def test_non_task_dialogue_reserved_not_rejected() -> None:
    r = run_long_input_task_planning_v1("我今天真的很烦，感觉什么都不顺。")
    assert r.domain_result.primary_domain == NON_TASK_DIALOGUE_FUTURE
    assert r.task_plan_v1 is None
    assert r.rejection_needed is False
    assert r.input_mode_judgement is not None
    assert r.input_mode_judgement.mode == "non_task_only"
    assert r.non_task_payload is not None
    assert r.non_task_payload.exists is True
    assert r.non_task_payload.handoff_candidate == "emotion_engine_future"


def test_mixed_emotion_and_task_preserves_non_task_segments() -> None:
    r = run_long_input_task_planning_v1("我今天有点不舒服，你先带我去最近的医院吧")
    assert r.input_mode_judgement is not None
    assert r.input_mode_judgement.mode == "mixed_task_and_non_task"
    assert r.mixed_input_flag is True
    assert r.non_task_payload is not None
    assert r.non_task_payload.exists is True
    assert any("不舒服" in s.content for s in r.non_task_payload.segments)
    assert r.task_plan_v1 is not None


def test_task_only_still_generates_plan() -> None:
    r = run_long_input_task_planning_v1("先带我去医院，路上顺便看看有没有便利店")
    assert r.input_mode_judgement is not None
    assert r.input_mode_judgement.mode == "task_only"
    assert r.mixed_input_flag is False
    assert r.task_plan_v1 is not None
