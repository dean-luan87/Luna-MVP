# src/vision/models/yolo/yolo_detector.py

from typing import Any, Dict, List

import numpy as np

from .yolo_loader import UnifiedYOLOLoader
from core.logging import get_logger

log = get_logger("yolo_detector")


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

        return DetectionResult(boxes)
