# core/navigation/navigation_runtime.py
from __future__ import annotations

import time
import logging
from typing import Dict, Any, List, Optional, Callable

from .scene_context import FrameContext
from .environment_scanner import EnvironmentScanner
from .direction_evaluator import DirectionEvaluator
from .scene_node_layer import SceneNodeLayer

logger = logging.getLogger(__name__)


class NavigationRuntime:
    """
    Navigation Runtime（导航运行时）
    用于真实对接 JS / YOLO / OCR / IMU 数据，
    并把 DirectionEvaluator + EnvironmentScanner 串联起来。

    JS/硬件只需要调用 runtime.feed(data) 即可。
    """

    def __init__(
        self,
        ideal_heading_deg: Optional[float] = None,
        on_result: Optional[Callable[[Dict[str, Any]], None]] = None
    ):
        """
        ideal_heading_deg：当前导航任务的理想方向（可由路径规划传入）
        on_result：回调函数，把最终结果丢回 JS 或播报系统
        """
        self.frame_id = 0
        self.scanner = EnvironmentScanner(SceneNodeLayer())
        self.direction = DirectionEvaluator(ideal_heading_deg=ideal_heading_deg)
        self.on_result = on_result
        self._last_direction: Optional[str] = None
        self._last_direction_confidence: float = 0.0

    # -------------------------------------------------------
    # JS / 设备数据统一入口
    # -------------------------------------------------------
    def feed(self, data: Dict[str, Any]):
        """
        data 格式（JS/硬件端直接发来）：
        {
            "heading_deg": 92.5,
            "speed_mps": 0.72,
            "turn_rate_deg_s": -4.1,
            "yolo": [ { label, bbox, confidence, distance_m }, ... ],
            "ocr": [ { text, bbox, confidence }, ... ]
        }
        """

        self.frame_id += 1
        ts = time.time()

        # IMU + 姿态
        ctx = FrameContext.from_raw(
            frame_id=self.frame_id,
            camera_heading_deg=data.get("heading_deg", 0.0),
            camera_pitch_deg=data.get("pitch_deg", 0.0),
            camera_roll_deg=data.get("roll_deg", 0.0),
            speed_mps=data.get("speed_mps", 0.0),
            turn_rate_deg_s=data.get("turn_rate_deg_s", 0.0),
            previous_direction=self._last_direction,
            previous_direction_confidence=self._last_direction_confidence,
            extras={"timestamp": ts},
        )

        # 环境理解（SceneNodeLayer 多帧滤波）
        stable_nodes = self.scanner.process(
            ctx,
            data.get("yolo", []),
            data.get("ocr", []),
        )

        # 同步环境，给方向分析器做准备
        self.direction.sync_env(stable_nodes)

        # 方向分析
        dr = self.direction.evaluate(ctx, self.scanner.layer)

        # 更新历史方向（用于下一帧）
        self._last_direction = dr.primary_direction
        self._last_direction_confidence = dr.confidence

        result = {
            "frame_id": self.frame_id,
            "timestamp": ts,
            "primary_direction": dr.primary_direction,
            "confidence": dr.confidence,
            "deviation_deg": dr.deviation_deg,
            "is_deviation": dr.is_deviation,
            "recommended_action": dr.recommended_action,
            "environment_hint": dr.environment_hint,
            "raw_reasons": dr.reasons,
            # 场景节点（提供给任务链、播报链、路径推理等）
            "scene_nodes": [n.to_dict() for n in stable_nodes],
        }

        logger.info(f"[NavigationRuntime] Result: {result}")

        # 推回前端/JS（若有）
        if self.on_result:
            try:
                self.on_result(result)
            except Exception as e:
                logger.error(f"[NavigationRuntime] on_result callback error: {e}")

        return result

    def set_ideal_heading(self, ideal_heading_deg: Optional[float]) -> None:
        """动态更新理想方向（例如路径规划更新时）"""
        self.direction.ideal_heading_deg = ideal_heading_deg
        logger.info(f"[NavigationRuntime] ideal_heading updated to {ideal_heading_deg}")

    def reset(self) -> None:
        """重置运行时状态（例如切换导航任务时）"""
        self.frame_id = 0
        self.scanner.layer.nodes.clear()
        self._last_direction = None
        self._last_direction_confidence = 0.0
        logger.info("[NavigationRuntime] runtime reset")

