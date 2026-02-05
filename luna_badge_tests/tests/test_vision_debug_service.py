"""
测试 VisionDebugService

验证：
1. VisionDebugService 正确封装健康快照
2. get_health() 返回正确的结构
3. get_model_block() 正确过滤任务类型
"""

import sys
import os
import unittest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.vision.multi_model_engine import MultiModelEngine, ModelSpec
from core.vision.vision_debug_service import VisionDebugService, VisionHealthSnapshot
from core.vision.vision_task_orchestrator import VisionTask


def test_vision_debug_service_get_health():
    """测试：VisionDebugService.get_health() 返回正确结构"""
    engine = MultiModelEngine(max_workers=2)

    def runner(task: VisionTask):
        return [{"label": "person", "score": 0.8}]

    engine.register_model("detect", ModelSpec(name="model_a", runner=runner, weight=1.0))
    engine.register_model("ocr", ModelSpec(name="ocr_model", runner=lambda t: "text", weight=1.0))

    # 执行一些任务
    for i in range(5):
        task_detect = VisionTask(task_type="detect", payload={"image": "dummy"}, task_id=f"d{i}")
        task_ocr = VisionTask(task_type="ocr", payload={"image": "dummy"}, task_id=f"o{i}")
        engine.run(task_detect)
        engine.run(task_ocr)

    debug_service = VisionDebugService(engine)
    snapshot = debug_service.get_health()

    assert isinstance(snapshot, VisionHealthSnapshot)
    data = snapshot.to_dict()

    # 检查结构
    assert "engine_status" in data
    assert "models" in data
    assert data["engine_status"]["total_task_types"] == 2
    assert "detect" in data["models"]
    assert "ocr" in data["models"]


def test_vision_debug_service_get_model_block():
    """测试：VisionDebugService.get_model_block() 正确过滤"""
    engine = MultiModelEngine(max_workers=2)

    def runner(task: VisionTask):
        return [{"label": "person", "score": 0.8}]

    engine.register_model("detect", ModelSpec(name="model_a", runner=runner, weight=1.0))
    engine.register_model("ocr", ModelSpec(name="ocr_model", runner=lambda t: "text", weight=1.0))

    # 执行一些任务
    for i in range(3):
        task_detect = VisionTask(task_type="detect", payload={"image": "dummy"}, task_id=f"d{i}")
        engine.run(task_detect)

    debug_service = VisionDebugService(engine)

    # 获取 detect 任务类型
    detect_block = debug_service.get_model_block("detect")
    assert detect_block is not None
    assert "model_a" in detect_block

    # 获取不存在的任务类型
    unknown_block = debug_service.get_model_block("unknown")
    assert unknown_block is None


def test_vision_health_snapshot_to_dict():
    """测试：VisionHealthSnapshot.to_dict() 方法"""
    snapshot = VisionHealthSnapshot(data={"test": "data"})
    result = snapshot.to_dict()
    assert result == {"test": "data"}


if __name__ == "__main__":
    unittest.main()












