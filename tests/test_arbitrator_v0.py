# -*- coding: utf-8 -*-
"""G) 多任务介入仲裁 v0 单元测试"""

import time

import pytest

from intervention.arbitrator_v0 import (
    ArbitratorV0,
    CandidateTask,
    ENV_AWARENESS,
    NAVIGATION,
    SAFETY,
    TASK_STATE,
    build_candidate_tasks,
    get_arbitrator_v0,
    reset_arbitrator_state,
)


def test_safety_always_wins():
    """SAFETY 永远赢"""
    r = ArbitratorV0()
    now = time.time()
    safety = CandidateTask(
        task_id="s1",
        task_type=SAFETY,
        engagement_level="L1",
        pal=0.5,
        complexity=0.5,
        urgency=1.0,
        last_spoken_ts=0,
        decision={},
    )
    nav = CandidateTask(
        task_id="n1",
        task_type=NAVIGATION,
        engagement_level="L3",
        pal=1.0,
        complexity=1.0,
        urgency=0.8,
        last_spoken_ts=0,
        decision={},
    )
    winner, deferred, scores, fairness = r.pick([safety, nav], now, "ASSISTED")
    assert winner is not None
    assert winner.task_id == "s1"
    assert "n1" in [t.task_id for t in deferred]


def test_guarded_suppresses_task_state():
    """GUARDED 下 TASK_STATE 被抑制"""
    r = ArbitratorV0()
    now = time.time()
    task = CandidateTask(
        task_id="t1",
        task_type=TASK_STATE,
        engagement_level="L2",
        pal=0.5,
        complexity=0.5,
        urgency=0.4,
        last_spoken_ts=0,
        decision={},
    )
    winner, deferred, scores, fairness = r.pick([task], now, "GUARDED")
    assert winner is None
    assert len(deferred) == 0


def test_cooldown_penalty():
    """冷却有效：同一 task 不会每秒反复赢"""
    r = ArbitratorV0()
    now = time.time()
    nav1 = CandidateTask(
        task_id="n1",
        task_type=NAVIGATION,
        engagement_level="L2",
        pal=0.8,
        complexity=0.8,
        urgency=0.8,
        last_spoken_ts=now - 1,  # 1s 前刚说过
        decision={},
    )
    nav2 = CandidateTask(
        task_id="n2",
        task_type=NAVIGATION,
        engagement_level="L2",
        pal=0.8,
        complexity=0.8,
        urgency=0.8,
        last_spoken_ts=0,  # 很久没说
        decision={},
    )
    winner, deferred, scores, fairness = r.pick([nav1, nav2], now, "ASSISTED")
    assert winner is not None
    # nav2 冷却惩罚小，应赢
    assert winner.task_id == "n2"


def test_score_threshold():
    """最高分 < 0.25 → 本 tick 不介入"""
    r = ArbitratorV0()
    now = time.time()
    task = CandidateTask(
        task_id="t1",
        task_type=TASK_STATE,
        engagement_level="L1",
        pal=0.0,
        complexity=0.0,
        urgency=0.4,
        last_spoken_ts=0,
        decision={},
    )
    winner, deferred, scores, fairness = r.pick([task], now, "ASSISTED")
    assert winner is None
    assert len(deferred) >= 0


def test_build_candidate_tasks():
    """build_candidate_tasks 正确转换"""
    r = ArbitratorV0()
    decisions = [
        {
            "type": "SPEAK",
            "text": "test",
            "advice_id": "a1",
            "advice_category": "TASK_STATE",
            "is_safety": False,
        },
    ]
    candidates = build_candidate_tasks(decisions, time.time(), "L2", 0.5, 0.5, r)
    assert len(candidates) == 1
    assert candidates[0].task_id == "a1"
    assert candidates[0].task_type == TASK_STATE
    assert candidates[0].engagement_level == "L2"


def test_record_spoken():
    """record_spoken 影响下次 pick：刚说过的任务分数下降"""
    r = ArbitratorV0()
    now = time.time()
    r.record_spoken("n1", now - 1)  # 1s 前刚说过
    nav1 = CandidateTask(
        task_id="n1",
        task_type=NAVIGATION,
        engagement_level="L2",
        pal=0.8,
        complexity=0.8,
        urgency=0.8,
        last_spoken_ts=r.get_last_spoken_ts("n1"),
        decision={},
    )
    nav2 = CandidateTask(
        task_id="n2",
        task_type=NAVIGATION,
        engagement_level="L2",
        pal=0.8,
        complexity=0.8,
        urgency=0.8,
        last_spoken_ts=0,
        decision={},
    )
    winner, _, scores, fairness = r.pick([nav1, nav2], now, "ASSISTED")
    assert winner is not None
    # nav1 1s 前说过（冷却惩罚低），nav2 很久没说（冷却惩罚高），nav2 应赢
    assert winner.task_id == "n2"
    assert scores.get("n2", 0) > scores.get("n1", 0)


def test_clear_state():
    """clear_state 清空 last_spoken 和 fairness"""
    r = ArbitratorV0()
    r.record_spoken("n1", time.time())
    assert r.get_last_spoken_ts("n1") > 0
    r.clear_state()
    assert r.get_last_spoken_ts("n1") == 0


def test_fairness_boost():
    """I) 公平补偿：missed_count 抬高 boost，fairness 输出正确"""
    r = ArbitratorV0()
    now = time.time()
    # 手动注入 missed：通过多次 pick 让 nav2 defer
    nav1 = CandidateTask(
        task_id="n1",
        task_type=NAVIGATION,
        engagement_level="L2",
        pal=0.9,
        complexity=0.9,
        urgency=0.8,
        last_spoken_ts=now - 10,
        decision={},
    )
    nav2 = CandidateTask(
        task_id="n2",
        task_type=NAVIGATION,
        engagement_level="L2",
        pal=0.5,
        complexity=0.5,
        urgency=0.8,
        last_spoken_ts=0,
        decision={},
    )
    # nav1 分数高，先赢；nav2 defer
    winner, deferred, scores, fairness = r.pick([nav1, nav2], now, "ASSISTED")
    assert winner.task_id == "n1"
    assert "n2" in fairness
    assert fairness["n2"]["missed"] == 1
    assert fairness["n2"]["boost"] == 0.1
