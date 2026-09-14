"""
测试 AskResultBinder 的绑定逻辑
"""

import pytest
from task_engine.ask.ask_binder import AskResultBinder


def test_bind_no_bindings_only_writes_raw_answers():
    """测试：没有 bindings 配置时，只写入原始 answers 到 ask_result"""
    answers = {"hospital_name": "瑞金医院"}
    task_meta = {}   # 没有 ask_bindings
    ctx = {}

    AskResultBinder.bind(answers, task_meta, ctx)

    assert ctx["ask_result"]["hospital_name"] == "瑞金医院"
    assert "params" not in ctx  # 不应创建 params


def test_bind_simple_params_mapping():
    """测试：简单的 params 映射"""
    answers = {"hospital_name": "瑞金医院"}
    task_meta = {
        "ask_bindings": {
            "hospital_name": {"target": "params", "name": "hospital"},
        }
    }
    ctx = {}

    AskResultBinder.bind(answers, task_meta, ctx)

    assert ctx["ask_result"]["hospital_name"] == "瑞金医院"
    assert ctx["params"]["hospital"] == "瑞金医院"


def test_bind_multiple_slots():
    """测试：多个 slot 的映射"""
    answers = {
        "hospital_name": "瑞金医院",
        "time_slot": "下午三点",
    }
    task_meta = {
        "ask_bindings": {
            "hospital_name": {"target": "params", "name": "hospital"},
            "time_slot": {"target": "params", "name": "time"},
        }
    }
    ctx = {}

    AskResultBinder.bind(answers, task_meta, ctx)

    assert ctx["params"]["hospital"] == "瑞金医院"
    assert ctx["params"]["time"] == "下午三点"


def test_bind_slot_not_answered_should_skip():
    """测试：slot 未回答时应该跳过，不写入 params"""
    answers = {"hospital_name": "瑞金医院"}
    task_meta = {
        "ask_bindings": {
            "hospital_name": {"target": "params", "name": "hospital"},
            "doctor_name": {"target": "params", "name": "doctor"},
        }
    }
    ctx = {}

    AskResultBinder.bind(answers, task_meta, ctx)

    assert ctx["params"]["hospital"] == "瑞金医院"
    assert "doctor" not in ctx["params"]












