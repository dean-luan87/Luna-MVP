"""
测试 MultiModelEngine

验证：
1. detect 任务的竞争选择正确 winner
2. 权重对结果有影响
3. OCR first-success 行为正常
4. 无模型注册时的错误处理
"""

import sys
import os
import unittest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.vision.multi_model_engine import MultiModelEngine, ModelSpec
from core.vision.vision_task_orchestrator import VisionTask, VisionResult


def test_detect_competitive_selects_best_model():
    """测试：detect 任务竞争选择最佳模型"""
    engine = MultiModelEngine(max_workers=4)

    def runner_a(task: VisionTask):
        # 模拟弱模型：score = 0.5
        return [{"label": "person", "score": 0.5}]

    def runner_b(task: VisionTask):
        # 模拟强模型：score = 0.8
        return [{"label": "person", "score": 0.8}]

    engine.register_model("detect", ModelSpec(name="model_a", runner=runner_a, weight=1.0))
    engine.register_model("detect", ModelSpec(name="model_b", runner=runner_b, weight=1.0))

    task = VisionTask(task_type="detect", payload={"image": "dummy"})
    res: VisionResult = engine.run(task)

    assert res.ok
    assert isinstance(res.result, dict)
    assert res.result["model"] == "model_b"
    # Patch-2: 结果结构包含 output、detections（向后兼容）和 scores
    assert "output" in res.result
    assert "detections" in res.result  # 向后兼容字段
    assert len(res.result["detections"]) == 1
    assert res.result["detections"][0]["score"] == 0.8
    assert "scores" in res.result


def test_detect_respects_weights():
    """测试：detect 任务尊重权重"""
    engine = MultiModelEngine(max_workers=4)

    def runner_a(task: VisionTask):
        # 高置信度但低权重
        return [{"label": "person", "score": 0.9}]

    def runner_b(task: VisionTask):
        # 低置信度但高权重
        return [{"label": "person", "score": 0.7}]

    engine.register_model("detect", ModelSpec(name="model_a", runner=runner_a, weight=0.3))
    engine.register_model("detect", ModelSpec(name="model_b", runner=runner_b, weight=1.0))

    task = VisionTask(task_type="detect", payload={"image": "dummy"})
    res: VisionResult = engine.run(task)

    assert res.ok
    # model_b: 0.7 * 1.0 = 0.7  >  model_a: 0.9 * 0.3 = 0.27
    assert res.result["model"] == "model_b"


def test_ocr_first_success():
    """测试：OCR 任务返回第一个成功的模型"""
    engine = MultiModelEngine(max_workers=4)

    def runner_fail(task: VisionTask):
        raise RuntimeError("ocr failed")

    def runner_ok(task: VisionTask):
        return "HELLO"

    engine.register_model("ocr", ModelSpec(name="bad_ocr", runner=runner_fail, weight=1.0))
    engine.register_model("ocr", ModelSpec(name="good_ocr", runner=runner_ok, weight=1.0))

    task = VisionTask(task_type="ocr", payload={"image": "dummy"})
    res: VisionResult = engine.run(task)

    assert res.ok
    assert res.result["model"] == "good_ocr"
    assert res.result["output"] == "HELLO"


def test_no_models_registered():
    """测试：无模型注册时的错误处理"""
    engine = MultiModelEngine(max_workers=2)
    task = VisionTask(task_type="detect", payload={"image": "dummy"})
    res = engine.run(task)
    assert not res.ok
    assert "No models registered" in (res.error or "")


def test_all_models_fail():
    """测试：所有模型都失败时的处理"""
    engine = MultiModelEngine(max_workers=2)

    def runner_fail(task: VisionTask):
        raise RuntimeError("model failed")

    engine.register_model("detect", ModelSpec(name="model_a", runner=runner_fail, weight=1.0))
    engine.register_model("detect", ModelSpec(name="model_b", runner=runner_fail, weight=1.0))

    task = VisionTask(task_type="detect", payload={"image": "dummy"})
    res = engine.run(task)

    assert not res.ok
    assert "All models failed" in (res.error or "") or "failed" in (res.error or "").lower()


def test_detect_empty_detections():
    """测试：检测结果为空时的处理"""
    engine = MultiModelEngine(max_workers=2)

    def runner_empty(task: VisionTask):
        return []

    def runner_ok(task: VisionTask):
        return [{"label": "person", "score": 0.8}]

    engine.register_model("detect", ModelSpec(name="empty_model", runner=runner_empty, weight=1.0))
    engine.register_model("detect", ModelSpec(name="ok_model", runner=runner_ok, weight=1.0))

    task = VisionTask(task_type="detect", payload={"image": "dummy"})
    res = engine.run(task)

    assert res.ok
    assert res.result["model"] == "ok_model"


if __name__ == "__main__":
    unittest.main()

