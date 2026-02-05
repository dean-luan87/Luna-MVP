"""
测试 Arbiter 和 ScoreLogger

验证：
1. Arbiter 正确决策 detect 任务
2. Arbiter 正确决策 ocr/classify 任务
3. ScoreLogger 正确记录日志
4. MultiModelEngine 集成 Arbiter 和 ScoreLogger 后正常工作
"""

import sys
import os
import unittest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.vision.arbiter import Arbiter, ArbiterDecision, ModelScore
from core.vision.score_logger import ScoreLogger, ScoreLogEntry
from core.vision.multi_model_engine import MultiModelEngine, ModelSpec
from core.vision.vision_task_orchestrator import VisionTask, VisionResult


def test_arbiter_decide_detect():
    """测试：Arbiter 正确决策 detect 任务"""
    arbiter = Arbiter()

    def runner_a(task: VisionTask):
        return [{"label": "person", "score": 0.5}]

    def runner_b(task: VisionTask):
        return [{"label": "person", "score": 0.8}]

    spec_a = ModelSpec(name="model_a", runner=runner_a, weight=1.0)
    spec_b = ModelSpec(name="model_b", runner=runner_b, weight=1.0)

    task = VisionTask(task_type="detect", payload={"image": "dummy"})
    results = [
        (spec_a, True, runner_a(task), None),
        (spec_b, True, runner_b(task), None),
    ]

    decision = arbiter.decide_detect(task, results)

    assert decision.winner == "model_b"
    assert len(decision.scores) == 2
    assert decision.error is None

    # 检查评分
    score_a = next(s for s in decision.scores if s.model == "model_a")
    score_b = next(s for s in decision.scores if s.model == "model_b")

    assert score_a.final_score == 0.5
    assert score_b.final_score == 0.8
    assert score_b.reason == "winner"


def test_arbiter_decide_detect_with_weights():
    """测试：Arbiter 考虑权重进行决策"""
    arbiter = Arbiter()

    def runner_a(task: VisionTask):
        return [{"label": "person", "score": 0.9}]

    def runner_b(task: VisionTask):
        return [{"label": "person", "score": 0.7}]

    spec_a = ModelSpec(name="model_a", runner=runner_a, weight=0.3)
    spec_b = ModelSpec(name="model_b", runner=runner_b, weight=1.0)

    task = VisionTask(task_type="detect", payload={"image": "dummy"})
    results = [
        (spec_a, True, runner_a(task), None),
        (spec_b, True, runner_b(task), None),
    ]

    decision = arbiter.decide_detect(task, results)

    # model_b: 0.7 * 1.0 = 0.7 > model_a: 0.9 * 0.3 = 0.27
    assert decision.winner == "model_b"


def test_arbiter_decide_first_success():
    """测试：Arbiter 正确决策 first-success 任务"""
    arbiter = Arbiter()

    def runner_fail(task: VisionTask):
        raise RuntimeError("failed")

    def runner_ok(task: VisionTask):
        return "HELLO"

    spec_fail = ModelSpec(name="bad_model", runner=runner_fail, weight=1.0)
    spec_ok = ModelSpec(name="good_model", runner=runner_ok, weight=1.0)

    task = VisionTask(task_type="ocr", payload={"image": "dummy"})
    results = [
        (spec_fail, False, None, "failed"),
        (spec_ok, True, "HELLO", None),
    ]

    decision = arbiter.decide_first_success(task, results)

    assert decision.winner == "good_model"
    assert decision.winner_output == "HELLO"
    assert len(decision.scores) == 2


def test_score_logger():
    """测试：ScoreLogger 正确记录日志"""
    logger = ScoreLogger()
    arbiter = Arbiter()

    def runner(task: VisionTask):
        return [{"label": "person", "score": 0.8}]

    spec = ModelSpec(name="model_a", runner=runner, weight=1.0)
    task = VisionTask(task_type="detect", payload={"image": "dummy"}, task_id="test_123")
    results = [(spec, True, runner(task), None)]

    decision = arbiter.decide_detect(task, results)
    logger.log(task_id="test_123", task_type="detect", decision=decision)

    entries = logger.get_all()
    assert len(entries) == 1
    assert entries[0].task_id == "test_123"
    assert entries[0].task_type == "detect"
    assert entries[0].winner == "model_a"
    assert len(entries[0].scores) == 1

    # 测试 clear
    logger.clear()
    assert len(logger.get_all()) == 0


def test_multi_model_engine_with_arbiter():
    """测试：MultiModelEngine 集成 Arbiter 后正常工作"""
    engine = MultiModelEngine(max_workers=2)

    def runner_a(task: VisionTask):
        return [{"label": "person", "score": 0.5}]

    def runner_b(task: VisionTask):
        return [{"label": "person", "score": 0.8}]

    engine.register_model("detect", ModelSpec(name="model_a", runner=runner_a, weight=1.0))
    engine.register_model("detect", ModelSpec(name="model_b", runner=runner_b, weight=1.0))

    task = VisionTask(task_type="detect", payload={"image": "dummy"}, task_id="test_456")
    result = engine.run(task)

    assert result.ok
    assert isinstance(result.result, dict)
    assert result.result["model"] == "model_b"
    assert "scores" in result.result
    assert len(result.result["scores"]) == 2

    # 检查日志
    entries = engine._score_logger.get_all()
    assert len(entries) == 1
    assert entries[0].task_id == "test_456"
    assert entries[0].winner == "model_b"


def test_multi_model_engine_result_contains_scores():
    """测试：MultiModelEngine 返回的结果包含详细的评分信息"""
    engine = MultiModelEngine(max_workers=2)

    def runner_a(task: VisionTask):
        return [{"label": "person", "score": 0.6}]

    def runner_b(task: VisionTask):
        return [{"label": "person", "score": 0.9}]

    engine.register_model("detect", ModelSpec(name="model_a", runner=runner_a, weight=1.0))
    engine.register_model("detect", ModelSpec(name="model_b", runner=runner_b, weight=1.0))

    task = VisionTask(task_type="detect", payload={"image": "dummy"})
    result = engine.run(task)

    assert result.ok
    scores = result.result["scores"]
    assert len(scores) == 2

    # 检查评分详情
    score_a = next(s for s in scores if s["model"] == "model_a")
    score_b = next(s for s in scores if s["model"] == "model_b")

    assert score_a["max_conf"] == 0.6
    assert score_b["max_conf"] == 0.9
    assert score_b["reason"] == "winner"
    assert score_a["reason"] in ["score_computed", "loser"]


if __name__ == "__main__":
    unittest.main()












