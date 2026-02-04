"""
Vision Dispatcher module (v1.3).

多模型调度器（MoE）：
- detector: 目标检测 (YOLO)
- depth_estimator: 深度估计
- segmentor: 分割模型
- tracker: 目标跟踪
- optical_flow: 光流/相机运动
"""

from typing import Any, Dict, Optional


class VisionDispatcher:
    def __init__(
        self,
        detector: Any,
        depth_estimator: Optional[Any] = None,
        segmentor: Optional[Any] = None,
        tracker: Optional[Any] = None,
        optical_flow: Optional[Any] = None,
    ):
        self.detector = detector
        self.depth_estimator = depth_estimator
        self.segmentor = segmentor
        self.tracker = tracker
        self.optical_flow = optical_flow

    def run_inference(self, frame: Any) -> Dict[str, Any]:
        """
        对单帧进行多模型推理，返回统一结构：
        {
          "detections": [...],
          "tracked_objects": [...],
          "segmentation": {...},
          "depth_map": ...,
          "motion": {...},
          "meta": {...}
        }
        """
        detections = self.detector.infer(frame) if self.detector else []

        tracked_objects = detections
        if self.tracker is not None:
            tracked_objects = self.tracker.update(detections)

        segmentation = {}
        if self.segmentor is not None:
            segmentation = self.segmentor.infer(frame)

        depth_map = None
        if self.depth_estimator is not None:
            depth_map = self.depth_estimator.infer(frame)

        motion = {}
        if self.optical_flow is not None:
            self.optical_flow.update(frame)
            motion = self.optical_flow.get_motion()

        timestamp = frame.get("timestamp") if isinstance(frame, dict) else None

        return {
            "detections": detections,
            "tracked_objects": tracked_objects,
            "segmentation": segmentation,
            "depth_map": depth_map,
            "motion": motion,
            "meta": {"timestamp": timestamp},
        }

