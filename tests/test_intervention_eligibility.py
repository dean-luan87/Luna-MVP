# -*- coding: utf-8 -*-
"""主线 A：介入资格门禁（v0）单元测试"""

import pytest

from intervention.eligibility import (
    TaskState,
    infer_task_state,
    compute_intervention_eligibility,
)


def test_infer_task_state():
    assert infer_task_state(has_goal=True) == TaskState.ACTIVE
    assert infer_task_state(has_goal=True, explore_mode=True) == TaskState.ACTIVE
    assert infer_task_state(has_goal=False, explore_mode=True) == TaskState.PASSIVE
    assert infer_task_state(has_goal=False, explore_mode=False) == TaskState.NONE


def test_eligibility_none():
    r = compute_intervention_eligibility(TaskState.NONE, 0.9)
    assert r["allowed"] is False
    assert r["reason"] == "NO_ACTIVE_TASK"


def test_eligibility_passive():
    r = compute_intervention_eligibility(TaskState.PASSIVE, 0.9)
    assert r["allowed"] is False
    assert r["reason"] == "NO_ACTIVE_TASK"


def test_eligibility_active_low_complexity():
    r = compute_intervention_eligibility(TaskState.ACTIVE, 0.3)
    assert r["allowed"] is False
    assert r["reason"] == "LOW_COMPLEXITY"


def test_eligibility_active_threshold():
    r = compute_intervention_eligibility(TaskState.ACTIVE, 0.5)
    assert r["allowed"] is True
    assert r["reason"] == "ACTIVE_TASK_AND_HIGH_COMPLEXITY"


def test_eligibility_active_high_complexity():
    r = compute_intervention_eligibility(TaskState.ACTIVE, 0.8)
    assert r["allowed"] is True
    assert r["reason"] == "ACTIVE_TASK_AND_HIGH_COMPLEXITY"
