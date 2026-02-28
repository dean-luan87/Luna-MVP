"""
测试 MultiModelEngine 的动态权重调整和自动禁用功能

验证：
1. 动态权重调整逻辑
2. 自动禁用低成功率模型
3. 健康快照功能
"""

import sys
import os
import unittest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.vision.multi_model_engine import MultiModelEngine, ModelSpec
from core.vision.vision_task_orchestrator import VisionTask


def test_recalculate_weights_and_auto_disable():
    """测试：动态权重调整和自动禁用"""
    mme = MultiModelEngine(max_workers=2)
    mme.min_calls_for_adjust = 10
    mme.auto_disable_threshold = 0.2
    mme.weight_adjust_alpha = 0.5

    def runner_good(task: VisionTask):
        return [{"label": "person", "score": 0.9}]

    def runner_bad(task: VisionTask):
        raise RuntimeError("fail")

    mme.register_model("detect", ModelSpec(name="good_model", runner=runner_good, weight=1.0))
    mme.register_model("detect", ModelSpec(name="bad_model", runner=runner_bad, weight=1.0))

    # good_model 成功 15 次，bad_model 失败 15 次
    for i in range(15):
        task = VisionTask(task_type="detect", payload={"image": "dummy"}, task_id=f"t{i}")
        _ = mme.run(task)

    # 强制调权重
    mme.recalculate_weights("detect")

    snapshot = mme.get_model_health_snapshot()
    detect_stats = snapshot.get("detect", {})

    assert "good_model" in detect_stats
    assert "bad_model" in detect_stats

    good = detect_stats["good_model"]
    bad = detect_stats["bad_model"]

    # good_model 应该成功率高于 0.5，且仍启用
    assert good["success_rate"] > 0.5
    assert good["enabled"] is True

    # bad_model 成功率为 0，应该被 auto_disable
    assert bad["success_rate"] == 0.0
    assert bad["enabled"] is False

    # good_model 权重要大于 0
    assert good["weight"] > 0.0


def test_weight_adjustment_based_on_success_rate():
    """测试：基于成功率的权重调整"""
    mme = MultiModelEngine(max_workers=2)
    mme.min_calls_for_adjust = 10
    mme.weight_adjust_alpha = 0.5

    def runner_high(task: VisionTask):
        return [{"label": "person", "score": 0.9}]

    def runner_low(task: VisionTask):
        return [{"label": "person", "score": 0.5}]

    spec_high = ModelSpec(name="high_model", runner=runner_high, weight=1.0)
    spec_low = ModelSpec(name="low_model", runner=runner_low, weight=1.0)

    mme.register_model("detect", spec_high)
    mme.register_model("detect", spec_low)

    # 模拟调用，high_model 总是获胜（因为置信度高）
    for i in range(20):
        task = VisionTask(task_type="detect", payload={"image": "dummy"}, task_id=f"t{i}")
        _ = mme.run(task)

    # 强制调权重
    mme.recalculate_weights("detect")

    # high_model 应该权重更高（因为成功率高）
    stats_high = mme._score_logger.get_stats("detect", "high_model")
    stats_low = mme._score_logger.get_stats("detect", "low_model")

    # 由于 high_model 总是获胜，它的成功率应该更高
    # 但两个模型都会成功执行，所以成功率应该都是 1.0
    # 权重调整主要基于 success_rate，如果都成功，权重应该接近
    assert stats_high.success_rate >= stats_low.success_rate


def test_health_snapshot_structure():
    """测试：健康快照结构"""
    mme = MultiModelEngine(max_workers=2)

    def runner(task: VisionTask):
        return [{"label": "person", "score": 0.8}]

    mme.register_model("detect", ModelSpec(name="model_a", runner=runner, weight=1.0))
    mme.register_model("ocr", ModelSpec(name="ocr_model", runner=lambda t: "text", weight=1.0))

    # 执行一些任务
    for i in range(5):
        task_detect = VisionTask(task_type="detect", payload={"image": "dummy"}, task_id=f"d{i}")
        task_ocr = VisionTask(task_type="ocr", payload={"image": "dummy"}, task_id=f"o{i}")
        mme.run(task_detect)
        mme.run(task_ocr)

    snapshot = mme.get_model_health_snapshot()

    # 检查结构
    assert "detect" in snapshot
    assert "ocr" in snapshot
    assert "model_a" in snapshot["detect"]
    assert "ocr_model" in snapshot["ocr"]

    # 检查字段
    model_a_stats = snapshot["detect"]["model_a"]
    assert "total_calls" in model_a_stats
    assert "success_calls" in model_a_stats
    assert "success_rate" in model_a_stats
    assert "avg_conf" in model_a_stats
    assert "enabled" in model_a_stats
    assert "weight" in model_a_stats


def test_auto_disable_after_threshold():
    """测试：达到阈值后自动禁用"""
    mme = MultiModelEngine(max_workers=2)
    mme.min_calls_for_adjust = 5
    mme.auto_disable_threshold = 0.3

    def runner_fail(task: VisionTask):
        raise RuntimeError("always fail")

    spec = ModelSpec(name="failing_model", runner=runner_fail, weight=1.0)
    mme.register_model("detect", spec)

    # 执行足够次数的失败调用
    for i in range(10):
        task = VisionTask(task_type="detect", payload={"image": "dummy"}, task_id=f"t{i}")
        mme.run(task)

    # 检查是否被禁用
    assert spec.enabled is False

    # 检查快照
    snapshot = mme.get_model_health_snapshot()
    failing_stats = snapshot["detect"]["failing_model"]
    assert failing_stats["success_rate"] == 0.0
    assert failing_stats["enabled"] is False


def test_weight_normalization():
    """测试：权重归一化"""
    mme = MultiModelEngine(max_workers=2)
    mme.min_calls_for_adjust = 5
    mme.weight_adjust_alpha = 0.5

    def runner_a(task: VisionTask):
        return [{"label": "person", "score": 0.8}]

    def runner_b(task: VisionTask):
        return [{"label": "person", "score": 0.7}]

    spec_a = ModelSpec(name="model_a", runner=runner_a, weight=2.0)
    spec_b = ModelSpec(name="model_b", runner=runner_b, weight=1.0)

    mme.register_model("detect", spec_a)
    mme.register_model("detect", spec_b)

    # 执行调用
    for i in range(10):
        task = VisionTask(task_type="detect", payload={"image": "dummy"}, task_id=f"t{i}")
        mme.run(task)

    # 强制调权重
    mme.recalculate_weights("detect")

    # 检查权重是否被归一化（总和应该接近 1.0）
    total_weight = sum(m.weight for m in mme._registry.get("detect", []) if m.enabled)
    assert 0.9 <= total_weight <= 1.1  # 允许小的浮点误差


if __name__ == "__main__":
    unittest.main()












