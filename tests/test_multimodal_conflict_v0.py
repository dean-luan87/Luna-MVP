# -*- coding: utf-8 -*-
"""K) 多模态输入冲突仲裁 v0 单元测试"""

import pytest

from intervention.multimodal_conflict_v0 import (
    InterventionCandidate,
    SOURCE_TASK,
    SOURCE_VISION,
    SOURCE_VOICE,
    resolve_multimodal_conflict,
    decisions_to_candidates,
)


def test_resolve_single_source():
    """单来源时直接返回"""
    cand = InterventionCandidate(
        source=SOURCE_TASK,
        task_id="t1",
        task_type="TASK_STATE",
        pal=0.5,
        complexity=0.5,
        engagement_level="L2",
        decision={"type": "SPEAK", "text": "test"},
    )
    selected, trace = resolve_multimodal_conflict({SOURCE_TASK: [cand]})
    assert len(selected) == 1
    assert selected[0].task_id == "t1"
    assert trace["selected_source"] == SOURCE_TASK
    assert trace["sources"] == [SOURCE_TASK]


def test_resolve_safety_first():
    """SAFETY 任何来源直接放行"""
    task_cand = InterventionCandidate(
        source=SOURCE_TASK,
        task_id="t1",
        task_type="TASK_STATE",
        pal=0.5,
        complexity=0.5,
        engagement_level="L2",
        decision={},
    )
    vision_cand = InterventionCandidate(
        source=SOURCE_VISION,
        task_id="s1",
        task_type="SAFETY",
        pal=0.5,
        complexity=0.5,
        engagement_level="L2",
        decision={},
    )
    selected, trace = resolve_multimodal_conflict({
        SOURCE_TASK: [task_cand],
        SOURCE_VISION: [vision_cand],
    })
    assert len(selected) == 1
    assert selected[0].task_type == "SAFETY"
    assert trace["reason"] == "SAFETY_FIRST"


def test_resolve_voice_over_vision():
    """VOICE 覆盖 VISION / TASK"""
    task_cand = InterventionCandidate(
        source=SOURCE_TASK,
        task_id="t1",
        task_type="TASK_STATE",
        pal=0.5,
        complexity=0.5,
        engagement_level="L2",
        decision={},
    )
    voice_cand = InterventionCandidate(
        source=SOURCE_VOICE,
        task_id="v1",
        task_type="ENV_AWARENESS",
        pal=0.5,
        complexity=0.5,
        engagement_level="L2",
        decision={},
    )
    selected, trace = resolve_multimodal_conflict({
        SOURCE_TASK: [task_cand],
        SOURCE_VOICE: [voice_cand],
    })
    assert len(selected) == 1
    assert selected[0].source == SOURCE_VOICE
    assert trace["selected_source"] == SOURCE_VOICE
    assert trace["reason"] == "USER_INITIATED"


def test_decisions_to_candidates():
    """decisions_to_candidates 正确转换"""
    decisions = [
        {"type": "SPEAK", "text": "test", "advice_id": "a1", "advice_category": "TASK_STATE", "is_safety": False},
    ]
    cands = decisions_to_candidates(decisions, SOURCE_TASK, "L2", 0.5, 0.5)
    assert len(cands) == 1
    assert cands[0].source == SOURCE_TASK
    assert cands[0].task_id == "a1"
    assert cands[0].task_type == "TASK_STATE"
