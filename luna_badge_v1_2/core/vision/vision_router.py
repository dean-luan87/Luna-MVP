"""
VisionRouter: 视觉任务路由层

提供统一的视觉能力接口，内部使用 VisionTaskOrchestrator 进行调度。
"""

from typing import Optional, Dict, Any
import uuid

from .vision_task_orchestrator import (
    VisionTaskOrchestrator,
    VisionTask,
    VisionResult,
)


class VisionRouter:
    """
    视觉任务路由层

    提供统一的视觉能力接口：
    - detect(image) -> VisionResult
    - ocr(image) -> VisionResult
    - classify(image) -> VisionResult
    """

    def __init__(self, detector=None, ocr_reader=None):
        """
        Args:
            detector: 检测器实例，需要有 detect(image) 方法
            ocr_reader: OCR 读取器实例，需要有 read(image) 或 extract_text(image) 方法
        """
        self.orchestrator = VisionTaskOrchestrator(detector=detector, ocr_reader=ocr_reader)

    def detect(self, image, task_id: Optional[str] = None) -> VisionResult:
        """
        执行物体检测

        Args:
            image: 输入图像
            task_id: 可选的任务 ID，用于日志追踪

        Returns:
            VisionResult: 检测结果
        """
        task = VisionTask(
            task_type="detect",
            payload={"image": image},
            task_id=task_id or str(uuid.uuid4())
        )
        return self.orchestrator.run(task)

    def ocr(self, image, task_id: Optional[str] = None) -> VisionResult:
        """
        执行 OCR 识别

        Args:
            image: 输入图像
            task_id: 可选的任务 ID，用于日志追踪

        Returns:
            VisionResult: OCR 结果
        """
        task = VisionTask(
            task_type="ocr",
            payload={"image": image},
            task_id=task_id or str(uuid.uuid4())
        )
        return self.orchestrator.run(task)

    def classify(self, image, task_id: Optional[str] = None) -> VisionResult:
        """
        执行图像分类

        Args:
            image: 输入图像
            task_id: 可选的任务 ID，用于日志追踪

        Returns:
            VisionResult: 分类结果
        """
        task = VisionTask(
            task_type="classify",
            payload={"image": image},
            task_id=task_id or str(uuid.uuid4())
        )
        return self.orchestrator.run(task)












