"""
Vision Model Loader (v1.3.0)

视觉模型加载器

封装 YOLO 模型加载，统一入口
未来如果更换 YOLO 版本或 RT-DETR，只需要改这个文件
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class YOLOLoader:
    """
    YOLO 模型加载器

    负责加载 YOLO 模型
    """

    @staticmethod
    def load(model_path: str):
        """
        加载 YOLO 模型

        Args:
            model_path: 模型路径，例如 "yolov8n.pt" 或完整路径

        Returns:
            YOLO 模型实例

        Raises:
            ImportError: 如果 ultralytics 未安装
            FileNotFoundError: 如果模型文件不存在
        """
        try:
            from ultralytics import YOLO
        except ImportError:
            raise ImportError(
                "ultralytics 未安装。请运行: pip install ultralytics"
            )

        try:
            logger.info(f"正在加载 YOLO 模型: {model_path}")
            model = YOLO(model_path)
            logger.info(f"✅ YOLO 模型加载成功: {model_path}")
            return model
        except Exception as e:
            logger.error(f"❌ YOLO 模型加载失败: {e}")
            raise













