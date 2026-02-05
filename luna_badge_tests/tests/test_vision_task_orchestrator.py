"""
测试 VisionTaskOrchestrator 和 VisionRouter

验证：
1. detect 任务正常执行
2. ocr 任务正常执行
3. classify 任务正常执行
4. 错误处理（缺少图像、未知类型等）
"""

import sys
import os
import unittest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.vision.vision_task_orchestrator import (
    VisionTaskOrchestrator,
    VisionTask,
    VisionResult,
)
from core.vision.vision_router import VisionRouter


class FakeDetector:
    """模拟检测器"""
    def detect(self, img):
        return [{"label": "person", "score": 0.8, "bbox": [10, 20, 30, 40]}]


class FakeOCR:
    """模拟 OCR 读取器"""
    def read(self, img):
        return "HELLO OCR"


class FakeOCRWithExtractText:
    """模拟使用 extract_text 方法的 OCR"""
    def extract_text(self, img):
        return "EXTRACTED TEXT"


class TestVisionTaskOrchestrator(unittest.TestCase):
    """测试 VisionTaskOrchestrator"""

    def setUp(self):
        """设置测试环境"""
        self.detector = FakeDetector()
        self.ocr = FakeOCR()
        self.orch = VisionTaskOrchestrator(detector=self.detector, ocr_reader=self.ocr)

    def test_detect(self):
        """测试检测任务"""
        task = VisionTask(task_type="detect", payload={"image": "dummy"})
        res = self.orch.run(task)
        self.assertTrue(res.ok)
        self.assertEqual(len(res.result), 1)
        self.assertEqual(res.result[0]["label"], "person")

    def test_ocr(self):
        """测试 OCR 任务"""
        task = VisionTask(task_type="ocr", payload={"image": "dummy"})
        res = self.orch.run(task)
        self.assertTrue(res.ok)
        self.assertEqual(res.result, "HELLO OCR")

    def test_ocr_with_extract_text(self):
        """测试使用 extract_text 方法的 OCR"""
        ocr_extract = FakeOCRWithExtractText()
        orch = VisionTaskOrchestrator(ocr_reader=ocr_extract)
        task = VisionTask(task_type="ocr", payload={"image": "dummy"})
        res = orch.run(task)
        self.assertTrue(res.ok)
        self.assertEqual(res.result, "EXTRACTED TEXT")

    def test_classify(self):
        """测试分类任务"""
        task = VisionTask(task_type="classify", payload={"image": "dummy"})
        res = self.orch.run(task)
        self.assertTrue(res.ok)
        self.assertIn("label", res.result)
        self.assertEqual(res.result["label"], "unknown")

    def test_missing_image(self):
        """测试缺少图像的情况"""
        task = VisionTask(task_type="detect", payload={})
        res = self.orch.run(task)
        self.assertFalse(res.ok)
        self.assertIn("Missing image", res.error)

    def test_unknown_type(self):
        """测试未知任务类型"""
        task = VisionTask(task_type="xxx", payload={})
        res = self.orch.run(task)
        self.assertFalse(res.ok)
        self.assertIn("Unknown", res.error)

    def test_detector_not_initialized(self):
        """测试检测器未初始化"""
        orch = VisionTaskOrchestrator(detector=None, ocr_reader=None)
        task = VisionTask(task_type="detect", payload={"image": "dummy"})
        res = orch.run(task)
        self.assertFalse(res.ok)
        self.assertIn("Detector not initialized", res.error)

    def test_ocr_not_initialized(self):
        """测试 OCR 未初始化"""
        orch = VisionTaskOrchestrator(detector=None, ocr_reader=None)
        task = VisionTask(task_type="ocr", payload={"image": "dummy"})
        res = orch.run(task)
        self.assertFalse(res.ok)
        self.assertIn("OCR not initialized", res.error)

    def test_task_id_preserved(self):
        """测试任务 ID 被保留"""
        task_id = "test_task_123"
        task = VisionTask(task_type="detect", payload={"image": "dummy"}, task_id=task_id)
        res = self.orch.run(task)
        self.assertEqual(res.task_id, task_id)


class TestVisionRouter(unittest.TestCase):
    """测试 VisionRouter"""

    def setUp(self):
        """设置测试环境"""
        self.detector = FakeDetector()
        self.ocr = FakeOCR()
        self.router = VisionRouter(detector=self.detector, ocr_reader=self.ocr)

    def test_router_detect(self):
        """测试路由器的 detect 方法"""
        res = self.router.detect("dummy_image")
        self.assertTrue(res.ok)
        self.assertEqual(len(res.result), 1)
        self.assertIsNotNone(res.task_id)

    def test_router_ocr(self):
        """测试路由器的 ocr 方法"""
        res = self.router.ocr("dummy_image")
        self.assertTrue(res.ok)
        self.assertEqual(res.result, "HELLO OCR")
        self.assertIsNotNone(res.task_id)

    def test_router_classify(self):
        """测试路由器的 classify 方法"""
        res = self.router.classify("dummy_image")
        self.assertTrue(res.ok)
        self.assertIn("label", res.result)
        self.assertIsNotNone(res.task_id)

    def test_router_custom_task_id(self):
        """测试自定义任务 ID"""
        custom_id = "custom_task_456"
        res = self.router.detect("dummy_image", task_id=custom_id)
        self.assertEqual(res.task_id, custom_id)


if __name__ == "__main__":
    unittest.main()












