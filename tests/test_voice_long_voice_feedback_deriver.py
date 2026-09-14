# -*- coding: utf-8 -*-
"""长语音反馈推导与 parse 挂载。"""

from __future__ import annotations

from capabilities.voice.bridge.voice_long_voice_feedback_deriver import derive_long_voice_feedback_result
from capabilities.voice.bridge.voice_long_input_task_planner import run_long_input_task_planning_v1
from capabilities.voice.schemas.voice_long_input_feedback_kind import (
    MIXED_INPUT_ACKNOWLEDGED,
    TASK_UNDERSTOOD_AND_READY,
    UNSUPPORTED_OR_REJECTED,
)
from shared.schemas.task_domain_v1 import NON_TASK_DIALOGUE_FUTURE


def test_planner_attaches_voice_feedback() -> None:
    r = run_long_input_task_planning_v1("先去商场，再找便利店买点吃的")
    assert r.voice_feedback is not None
    assert r.voice_feedback.feedback_mode == TASK_UNDERSTOOD_AND_READY
    assert "voice_feedback" in r.to_dict()


def test_non_task_feedback_not_reject_tone() -> None:
    from capabilities.voice.schemas.voice_long_input_feedback_kind import NON_TASK_PRESERVED_FOR_FUTURE

    r = run_long_input_task_planning_v1("我今天真的很烦，感觉什么都不顺。")
    assert r.domain_result.primary_domain == NON_TASK_DIALOGUE_FUTURE
    assert r.voice_feedback is not None
    assert r.voice_feedback.feedback_mode == NON_TASK_PRESERVED_FOR_FUTURE
    assert r.voice_feedback.non_task_acknowledged is True


def test_mixed_feedback_mode() -> None:
    r = run_long_input_task_planning_v1("我今天有点不舒服，你先带我去最近的医院吧")
    assert r.voice_feedback is not None
    assert r.voice_feedback.feedback_mode == MIXED_INPUT_ACKNOWLEDGED


def test_unsupported_feedback() -> None:
    r = run_long_input_task_planning_v1("替我给别人发消息")
    assert r.voice_feedback is not None
    assert r.voice_feedback.feedback_mode == UNSUPPORTED_OR_REJECTED


def test_derive_idempotent_fields() -> None:
    r = run_long_input_task_planning_v1("带我去医院")
    fb = derive_long_voice_feedback_result(r)
    assert fb.related_plan_version == "v1"
    assert fb.feedback_mode == TASK_UNDERSTOOD_AND_READY
