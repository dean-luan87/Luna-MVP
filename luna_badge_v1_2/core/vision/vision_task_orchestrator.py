"""
VisionTaskOrchestrator: 通用视觉任务调度器

职责：
- 接收 detect / ocr / classify 等任务
- 按优先级执行
- 保留统一 API：run(task: VisionTask)

Pro-2 更新：
- 若 MultiModelEngine 对该 task_type 有注册模型 → 优先走 MME
- 否则回退到单模型逻辑（detector / ocr_reader）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

# 新增引入（避免循环导入）
try:
    from .multi_model_engine import MultiModelEngine
except ImportError:
    MultiModelEngine = None  # type: ignore


@dataclass
class VisionTask:
    """单一视觉任务的结构定义"""
    task_type: str                 # detect / ocr / classify / segment …
    payload: Dict[str, Any]        # 输入参数（图像、ROI、附加属性）
    priority: int = 5              # 默认优先级
    task_id: Optional[str] = None  # 可用于日志追踪


@dataclass
class VisionResult:
    """视觉任务执行结果"""
    ok: bool
    result: Any = None
    error: Optional[str] = None
    task_id: Optional[str] = None


class VisionTaskOrchestrator:
    """
    通用视觉任务调度器：

    - 接收 detect / ocr / classify 等任务
    - 按优先级执行
    - 保留统一 API：run(task: VisionTask)

    Pro-2 后的 Orchestrator：

    - 若 MultiModelEngine 对该 task_type 有注册模型 → 优先走 MME
    - 否则回退到单模型逻辑（detector / ocr_reader）
    """

    def __init__(
        self,
        detector=None,
        ocr_reader=None,
        multi_model_engine: Optional[MultiModelEngine] = None,
    ):
        """
        Args:
            detector: 检测器实例，需要有 detect(image) 方法
            ocr_reader: OCR 读取器实例，需要有 read(image) 方法
            multi_model_engine: 可选的 MultiModelEngine 实例
        """
        self.detector = detector
        self.ocr_reader = ocr_reader
        # MultiModelEngine 可注入，也可外部统一管理
        self._mme: Optional[MultiModelEngine] = multi_model_engine

    # ======= 主入口 =======
    def run(self, task: VisionTask) -> VisionResult:
        """
        执行视觉任务

        Pro-2 逻辑：
        1. 若存在 MME 且该任务有模型注册 → 优先走多模型
        2. 否则 fallback 到旧逻辑

        Args:
            task: VisionTask 实例

        Returns:
            VisionResult: 执行结果
        """
        try:
            # Step 1: 若存在 MME 且该任务有模型注册 → 优先走多模型
            if self._mme is not None and self._mme.has_models(task.task_type):
                return self._mme.run(task)

            # Step 2: fallback 到旧逻辑
            if task.task_type == "detect":
                return self._run_detect(task)

            elif task.task_type == "ocr":
                return self._run_ocr(task)

            elif task.task_type == "classify":
                return self._run_classify(task)

            else:
                return VisionResult(
                    ok=False,
                    error=f"Unknown vision task_type={task.task_type}",
                    task_id=task.task_id,
                )

        except Exception as e:
            return VisionResult(
                ok=False,
                error=str(e),
                task_id=task.task_id,
            )

    # ======= 旧逻辑保留为 fallback =======
    def _run_detect(self, task: VisionTask) -> VisionResult:
        """执行物体检测任务（fallback）"""
        if self.detector is None:
            return VisionResult(
                ok=False,
                error="Detector not initialized",
                task_id=task.task_id,
            )

        image = task.payload.get("image")
        if image is None:
            return VisionResult(
                ok=False,
                error="Missing image",
                task_id=task.task_id,
            )

        # 调用检测器的 detect 方法
        # 支持不同的检测器接口
        if hasattr(self.detector, "detect"):
            detections = self.detector.detect(image)
            # 如果返回的是对象，尝试转换为列表
            if hasattr(detections, "boxes"):
                # 处理 DetectionResult 类型
                detections = detections.boxes if hasattr(detections, "boxes") else detections
            elif hasattr(detections, "to_dict"):
                detections = detections.to_dict()
            return VisionResult(ok=True, result=detections, task_id=task.task_id)
        else:
            return VisionResult(
                ok=False,
                error="Detector does not have detect() method",
                task_id=task.task_id,
            )

    def _run_ocr(self, task: VisionTask) -> VisionResult:
        """执行 OCR 识别任务（fallback）"""
        if self.ocr_reader is None:
            return VisionResult(
                ok=False,
                error="OCR not initialized",
                task_id=task.task_id,
            )

        image = task.payload.get("image")
        if image is None:
            return VisionResult(
                ok=False,
                error="Missing image",
                task_id=task.task_id,
            )

        # 支持不同的 OCR 接口
        if hasattr(self.ocr_reader, "read"):
            text = self.ocr_reader.read(image)
        elif hasattr(self.ocr_reader, "extract_text"):
            text = self.ocr_reader.extract_text(image)
        elif hasattr(self.ocr_reader, "ocr"):
            # PaddleOCR 风格
            result = self.ocr_reader.ocr(image, cls=True)
            text = result if result else ""
        else:
            return VisionResult(
                ok=False,
                error="OCR reader does not have supported method",
                task_id=task.task_id,
            )

        return VisionResult(ok=True, result=text, task_id=task.task_id)

    def _run_classify(self, task: VisionTask) -> VisionResult:
        """
        执行分类任务（fallback，可做扩展，未来可插模型）

        Args:
            task: VisionTask 实例

        Returns:
            VisionResult: 分类结果
        """
        # 目前 classify 没有默认实现，留作未来扩展
        return VisionResult(
            ok=True,
            result={"label": "unknown", "score": 0.0},
            task_id=task.task_id,
        )

