# core/yolo_detector.py
# 向后兼容层：保持旧导入路径可用，实际使用新路径的模块

from typing import Any, Dict, List

import numpy as np

# 优先使用新路径，如果不存在则使用旧路径
try:
    from src.vision.models.yolo.yolo_loader import UnifiedYOLOLoader
except ImportError:
    from .yolo_loader import UnifiedYOLOLoader

# 1.4.1-core: 接入新日志系统和 Metrics
try:
    from core.logging.log_manager import LogManager
    from core.health.metrics_collector import MetricsCollector
    log = LogManager.get_logger("yolo_detector")
except (ImportError, RuntimeError):
    # 兼容旧系统
    from core.logging import get_logger
    log = get_logger("yolo_detector")
    MetricsCollector = None


class DetectionResult:
    def __init__(self, boxes: List[Dict[str, Any]]):
        self.boxes = boxes

    def to_dict(self) -> Dict[str, Any]:
        return {"boxes": self.boxes}


class YoloDetector:
    """
    对外统一接口：detect(image) → DetectionResult

    image: H x W x 3 ndarray, RGB
    """

    def __init__(self, config_path: str = "configs/model_registry.yaml") -> None:
        self.loader = UnifiedYOLOLoader(config_path=config_path)
        self.model = self.loader.load_model()

    def detect(self, image: np.ndarray) -> DetectionResult:
        # 1.4.1-core: 使用 Metrics 记录推理耗时
        if MetricsCollector:
            with MetricsCollector.timeit("yolo.inference"):
                return self._detect_internal(image)
        else:
            return self._detect_internal(image)
    
    def _detect_internal(self, image: np.ndarray) -> DetectionResult:
        """内部检测逻辑（分离出来以便 Metrics 包装）"""
        # 确保是 numpy
        if not isinstance(image, np.ndarray):
            image = np.asarray(image)

        # YOLO 内部会做 resize 等处理
        results_list = self.loader.infer(image)

        boxes: List[Dict[str, Any]] = []
        for r in results_list:
            if not hasattr(r, "boxes") or r.boxes is None:
                continue

            xyxy = r.boxes.xyxy.cpu().numpy()
            conf = r.boxes.conf.cpu().numpy()
            cls = r.boxes.cls.cpu().numpy()
            
            # 获取类别名称
            names = r.names if hasattr(r, 'names') else {}

            for i in range(len(xyxy)):
                x1, y1, x2, y2 = xyxy[i].tolist()
                cls_id = int(cls[i])
                cls_name = names.get(cls_id, f"class_{cls_id}")

                boxes.append(
                    {
                        "x1": float(x1),
                        "y1": float(y1),
                        "x2": float(x2),
                        "y2": float(y2),
                        "conf": float(conf[i]),
                        "cls": cls_name,
                        "cls_id": cls_id,
                    }
                )

        # 1.4.1-core: 记录检测结果
        if MetricsCollector:
            MetricsCollector.incr("yolo.detections", len(boxes))
        
        if len(boxes) == 0:
            log.debug("YOLO 检测结果为空")
        else:
            log.debug(f"YOLO 检测到 {len(boxes)} 个目标")

        return DetectionResult(boxes)
