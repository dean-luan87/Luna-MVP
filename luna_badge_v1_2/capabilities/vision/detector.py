"""
Vision Detector (v1.3.0)

视觉检测器

负责执行 YOLO 推理，返回统一的视觉理解结果
"""

import logging
import time
from typing import List

from .model_loader import YOLOLoader
from .types import SceneObj, SceneFrameResult

logger = logging.getLogger(__name__)


class VisionDetector:
    """
    视觉检测器

    封装 YOLO 模型推理，输出统一的 SceneFrameResult
    """

    def __init__(self, model_path: str, conf_threshold: float = 0.5):
        """
        初始化视觉检测器

        Args:
            model_path: YOLO 模型路径，例如 "yolov8n.pt"
            conf_threshold: 置信度阈值，默认 0.5
        """
        self.model = YOLOLoader.load(model_path)
        self.conf_threshold = conf_threshold
        self.frame_id = 0

        logger.info(f"视觉检测器初始化完成 (conf_threshold={conf_threshold})")

    def detect(self, frame) -> SceneFrameResult:
        """
        执行视觉检测

        Args:
            frame: OpenCV 图像帧（numpy array，BGR 格式）

        Returns:
            SceneFrameResult: 检测结果
        """
        # 自增 frame_id
        self.frame_id += 1

        # 记录当前时间的毫秒时间戳
        timestamp = int(time.time() * 1000)

        # 调用 YOLO 模型进行推理
        try:
            results = self.model(frame)[0]  # 获取第一个结果
        except Exception as e:
            logger.error(f"YOLO 推理失败: {e}")
            # 返回空结果
            return SceneFrameResult(
                frame_id=self.frame_id,
                objects=[],
                risk_level="low",
                timestamp=timestamp,
            )

        # 解析检测结果
        objects: List[SceneObj] = []

        if results.boxes is not None:
            for box in results.boxes:
                # 获取置信度
                conf = float(box.conf[0])
                
                # 如果置信度低于阈值，跳过
                if conf < self.conf_threshold:
                    continue

                # 获取类别
                cls_id = int(box.cls[0])
                cls_name = results.names[cls_id]

                # 获取边界框坐标
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # 创建 SceneObj
                obj = SceneObj(
                    cls=cls_name,
                    conf=conf,
                    bbox=[x1, y1, x2, y2],
                )

                objects.append(obj)

        # 评估风险等级
        risk_level = self._eval_risk(objects)

        # 创建并返回结果
        result = SceneFrameResult(
            frame_id=self.frame_id,
            objects=objects,
            risk_level=risk_level,
            timestamp=timestamp,
        )

        return result

    def _eval_risk(self, objects: List[SceneObj]) -> str:
        """
        评估风险等级（简化版）

        Args:
            objects: 检测到的对象列表

        Returns:
            str: 风险等级（"low" / "medium" / "high"）
        """
        # 如果没有对象，返回 low
        if not objects:
            return "low"

        # 检查是否有对象占画面太大面积
        # 简单阈值：80000 像素（大约 282x282 的区域）
        area_threshold = 80000

        for obj in objects:
            area = obj.area()
            if area > area_threshold:
                # 有物体占画面太大面积，判为 medium
                logger.debug(f"检测到大面积物体: {obj.cls}, 面积: {area}")
                return "medium"

        # 否则返回 low
        return "low"

    def reset_frame_id(self):
        """重置 frame_id（用于测试）"""
        self.frame_id = 0





















