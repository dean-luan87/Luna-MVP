from core.logging import get_logger

log = get_logger("main_loop_v1_2_backup")
"""
Main loop for Luna Badge v1.2.0.

整合：
- FrameManager
- VisionDispatcher
- YoloDetector
- DepthEstimator
- FusionEngine
- NavigationEngine
- TTSManager
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径，确保可以导入 core 模块
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import time
from typing import Optional

from core.frame_manager import FrameManager
from core.vision_dispatcher import VisionDispatcher
from core.yolo_detector import YoloDetector
from core.depth_estimator import DepthEstimator
from core.fusion_engine import FusionEngine
from core.scene_output import build_scene_state
from capabilities.navigation_logic import NavigationEngine
from core.tts_manager import TTSManager


def main():
    # 初始化各模块（v1.2 使用简单配置）
    frame_manager = FrameManager(max_cache_size=10, target_fps=5)

    yolo_config = {
        "model_name": "yolov8n",
        "conf_threshold": 0.5,
    }
    detector = YoloDetector(yolo_config)
    detector.load_model()

    depth_config = {
        "enabled": False
    }
    depth_estimator = DepthEstimator(depth_config)
    depth_estimator.load_model()

    dispatcher = VisionDispatcher(detector=detector, depth_estimator=depth_estimator)
    fusion_engine = FusionEngine(window_size=10)
    navigation_engine = NavigationEngine()
    tts = TTSManager()

    log.info("[Main] Luna Badge v1.2.0 main loop started.")

    try:
        while True:
            frame: Optional[dict] = frame_manager.grab_frame()
            if frame is None:
                # 抽帧频率控制
                time.sleep(0.01)
                continue

            vision_result = dispatcher.run_inference(frame)
            fusion_engine.add_result(vision_result)
            fused_result = fusion_engine.get_fused_result()

            scene_state = build_scene_state(
                fused_result=fused_result,
                depth_result=vision_result.get("depth_map"),
                raw_frame=frame,
            )

            navigation_engine.update(scene_state)
            text = navigation_engine.decide()
            if text:
                tts.speak(text)

            # 控制主循环速度，避免 CPU 打满
            time.sleep(0.05)
    except KeyboardInterrupt:
        log.info("\n[Main] Exiting main loop.")


if __name__ == "__main__":
    main()

