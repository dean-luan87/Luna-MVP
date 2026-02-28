"""
测试 VisionTaskOrchestrator 与 MultiModelEngine 的集成

验证：
1. Orchestrator 优先使用 MME（如果有模型注册）
2. Orchestrator fallback 到单模型逻辑（如果没有 MME 模型）
3. 两种模式都能正常工作
"""

import sys
import os
import unittest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.vision.multi_model_engine import MultiModelEngine, ModelSpec
from core.vision.vision_task_orchestrator import (
    VisionTaskOrchestrator,
    VisionTask,
    VisionResult,
)


class FakeDetector:
    """模拟检测器"""
    def detect(self, image):
        return [{"label": "detector_person", "score": 0.6}]


class FakeOCR:
    """模拟 OCR 读取器"""
    def read(self, image):
        return "detector_ocr_text"


def test_orchestrator_uses_mme_if_models_present():
    """测试：Orchestrator 优先使用 MME（如果有模型注册）"""
    engine = MultiModelEngine(max_workers=2)

    def runner_mme(task: VisionTask):
        return [{"label": "mme_person", "score": 0.9}]

    engine.register_model("detect", ModelSpec(name="mme_model", runner=runner_mme, weight=1.0))

    detector = FakeDetector()
    orch = VisionTaskOrchestrator(
        detector=detector,
        ocr_reader=None,
        multi_model_engine=engine,
    )

    task = VisionTask(task_type="detect", payload={"image": "dummy"})
    res: VisionResult = orch.run(task)

    assert res.ok
    assert isinstance(res.result, dict)
    assert res.result["model"] == "mme_model"
    # Patch-2: 结果结构包含 output、detections（向后兼容）和 scores
    assert "output" in res.result
    assert "detections" in res.result  # 向后兼容字段
    assert res.result["detections"][0]["label"] == "mme_person"
    assert "scores" in res.result


def test_orchestrator_fallback_to_detector_if_no_mme_models():
    """测试：Orchestrator fallback 到单模型逻辑（如果没有 MME 模型）"""
    engine = MultiModelEngine(max_workers=2)
    # 不注册任何模型

    detector = FakeDetector()
    orch = VisionTaskOrchestrator(
        detector=detector,
        ocr_reader=None,
        multi_model_engine=engine,
    )

    task = VisionTask(task_type="detect", payload={"image": "dummy"})
    res: VisionResult = orch.run(task)

    assert res.ok
    assert isinstance(res.result, list)
    assert res.result[0]["label"] == "detector_person"


def test_orchestrator_fallback_to_ocr_if_no_mme_models():
    """测试：Orchestrator OCR fallback 到单模型逻辑"""
    engine = MultiModelEngine(max_workers=2)
    # 不注册任何模型

    ocr_reader = FakeOCR()
    orch = VisionTaskOrchestrator(
        detector=None,
        ocr_reader=ocr_reader,
        multi_model_engine=engine,
    )

    task = VisionTask(task_type="ocr", payload={"image": "dummy"})
    res: VisionResult = orch.run(task)

    assert res.ok
    assert res.result == "detector_ocr_text"


def test_orchestrator_without_mme():
    """测试：Orchestrator 在没有 MME 时正常工作"""
    detector = FakeDetector()
    orch = VisionTaskOrchestrator(
        detector=detector,
        ocr_reader=None,
        multi_model_engine=None,  # 不传入 MME
    )

    task = VisionTask(task_type="detect", payload={"image": "dummy"})
    res: VisionResult = orch.run(task)

    assert res.ok
    assert isinstance(res.result, list)
    assert res.result[0]["label"] == "detector_person"


def test_orchestrator_mme_different_task_type():
    """测试：MME 只对注册的 task_type 生效，其他类型 fallback"""
    engine = MultiModelEngine(max_workers=2)

    def runner_mme(task: VisionTask):
        return [{"label": "mme_person", "score": 0.9}]

    # 只注册 detect 任务
    engine.register_model("detect", ModelSpec(name="mme_model", runner=runner_mme, weight=1.0))

    detector = FakeDetector()
    ocr_reader = FakeOCR()
    orch = VisionTaskOrchestrator(
        detector=detector,
        ocr_reader=ocr_reader,
        multi_model_engine=engine,
    )

    # detect 任务应该走 MME
    task_detect = VisionTask(task_type="detect", payload={"image": "dummy"})
    res_detect = orch.run(task_detect)
    assert res_detect.ok
    assert isinstance(res_detect.result, dict)
    assert res_detect.result["model"] == "mme_model"

    # ocr 任务应该 fallback 到单模型
    task_ocr = VisionTask(task_type="ocr", payload={"image": "dummy"})
    res_ocr = orch.run(task_ocr)
    assert res_ocr.ok
    assert res_ocr.result == "detector_ocr_text"


if __name__ == "__main__":
    unittest.main()

