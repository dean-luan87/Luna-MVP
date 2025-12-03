from core.logging import get_logger

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
log = get_logger("benchmark_full_realtime")
"""
真实链路单次 Benchmark

功能：
- 从真实图像源抓一帧（Camera → cv2 摄像头 → sample_frames 目录）
- YOLO11-tiny 真实推理
- 调用 NavBrain（若存在）
- 调用 TTS（若存在）
- 统计各阶段耗时 + 总耗时，写入 perf_logs
"""

import os
import json
import time
from pathlib import Path
from typing import Any, Dict, Optional

import numpy as np

# 确保可以 import core 包
ROOT = Path(__file__).resolve().parents[1]
import sys

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.yolo_detector import YoloDetector  # 真 YOLO11-tiny

# 尝试导入 Camera
Camera = None
try:
    from utils.camera_handler import CameraHandler
    Camera = CameraHandler
except Exception:
    try:
        from core.camera_manager import CameraManager
        Camera = CameraManager
    except Exception:
        Camera = None

# 尝试导入 NavBrain
NavBrainCls = None
try:
    from core.navigation_logic_v1_3 import NavigationLogicV1_3
    NavBrainCls = NavigationLogicV1_3
except Exception:
    try:
        from core.navigation_logic import NavigationLogic
        NavBrainCls = NavigationLogic
    except Exception:
        NavBrainCls = None

# 尝试导入 TTS 引擎
TTSEngineCls = None
try:
    from core.tts_manager import TTSManager
    TTSEngineCls = TTSManager
except Exception:
    TTSEngineCls = None

# 尝试导入 cv2
cv2 = None
try:
    import cv2  # type: ignore
    cv2 = cv2
except Exception:
    cv2 = None


def get_frame() -> np.ndarray:
    """真实图像源优先级：
    1) utils.camera_handler.CameraHandler
    2) OpenCV 摄像头
    3) sample_frames 目录下的 jpg/png
    """
    # 1) CameraHandler
    if Camera is not None:
        try:
            cam = Camera(camera_index=0)
            frame = cam.read_frame()
            if hasattr(cam, 'release'):
                cam.release()
            if frame is not None:
                return frame
        except Exception as e:
            log.warning(f"[WARN] CameraHandler 获取失败: {e}")

    # 2) cv2 摄像头
    if cv2 is not None:
        try:
            cap = cv2.VideoCapture(0)
            ok, frame = cap.read()
            cap.release()
            if ok and frame is not None:
                return frame
        except Exception as e:
            log.warning(f"[WARN] OpenCV 摄像头获取失败: {e}")

    # 3) sample_frames 目录
    sample_dir = ROOT / "sample_frames"
    if sample_dir.exists():
        for ext in ("*.jpg", "*.jpeg", "*.png"):
            imgs = list(sample_dir.glob(ext))
            if imgs:
                img_path = imgs[0]
                if cv2 is None:
                    raise RuntimeError(
                        f"找到样本图片 {img_path}，但未安装 opencv-python，无法读取图像。"
                    )
                img = cv2.imread(str(img_path))
                if img is None:
                    continue
                return img

    # 4) 生成一个测试图像（最后兜底）
    if cv2 is not None:
        log.warning("[WARN] 无法获取真实图像，使用生成的测试图像")
        test_img = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.rectangle(test_img, (100, 100), (200, 200), (0, 255, 0), 2)
        return test_img

    raise RuntimeError(
        "无法获取测试图像：无 Camera、无 cv2 摄像头、也没有 sample_frames/*.jpg。"
    )


class DummyNavBrain:
    """当 core.navigation_logic 不存在时，用轻量 Stub 代替"""

    def __init__(self) -> None:
        pass

    def step(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        # 模拟一些计算负载
        time.sleep(0.02)  # 20ms
        return {
            "instruction": "向前走两步，然后稍微向右偏一点。",
            "debug": {"num_detections": len(perception.get("detections", []))},
        }

    def plan_route(self, vision_result, ground_state, dispatch_result):
        time.sleep(0.02)  # 20ms
        return {
            "message": "前方环境正常，可以继续前进。",
            "route": "forward"
        }


class DummyTTSEngine:
    """当 core.tts_manager 不存在时，用 Stub 模拟接口"""

    def __init__(self) -> None:
        pass

    def speak(self, text: str) -> None:
        # 模拟 TTS 播报耗时
        time.sleep(0.02)  # 20ms
        log.info(f"[TTS] {text}")


def build_nav_brain():
    if NavBrainCls is None:
        return DummyNavBrain()
    try:
        return NavBrainCls()
    except Exception as e:
        log.warning(f"[WARN] NavBrain 初始化失败: {e}，使用 DummyNavBrain")
        return DummyNavBrain()


def build_tts_engine():
    if TTSEngineCls is None:
        return DummyTTSEngine()
    try:
        return TTSEngineCls(mode="normal")
    except Exception as e:
        log.warning(f"[WARN] TTS 初始化失败: {e}，使用 DummyTTSEngine")
        return DummyTTSEngine()


def run_full_pipeline_once(detector: YoloDetector) -> Dict[str, Any]:
    """
    单次完整链路：
    Camera → YOLO → NavBrain → TTS
    """
    nav_brain = build_nav_brain()
    tts_engine = build_tts_engine()

    t0 = time.perf_counter()
    frame = get_frame()
    t1 = time.perf_counter()

    det_result = detector.detect(frame)
    t2 = time.perf_counter()

    # 尝试调用导航逻辑
    if hasattr(nav_brain, 'step'):
        nav_result = nav_brain.step(det_result)
    elif hasattr(nav_brain, 'plan_route'):
        nav_result = nav_brain.plan_route(
            vision_result=det_result,
            ground_state={"state": "safe"},
            dispatch_result={}
        )
    else:
        nav_result = {"instruction": "前方环境正常"}
    t3 = time.perf_counter()

    instruction = nav_result.get("instruction") or nav_result.get("message", "")
    tts_engine.speak(instruction)
    t4 = time.perf_counter()

    camera_ms = (t1 - t0) * 1000.0
    detect_ms = (t2 - t1) * 1000.0
    nav_ms = (t3 - t2) * 1000.0
    tts_ms = (t4 - t3) * 1000.0
    total_ms = (t4 - t0) * 1000.0

    return {
        "camera_ms": round(camera_ms, 2),
        "detect_ms": round(detect_ms, 2),
        "nav_ms": round(nav_ms, 2),
        "tts_ms": round(tts_ms, 2),
        "total_ms": round(total_ms, 2),
        "num_detections": len(det_result.get("detections", [])),
    }


def main():
    os.makedirs(ROOT / "perf_logs", exist_ok=True)
    report_path = ROOT / "perf_logs" / "full_realtime_benchmark.json"

    log.info("\n" + "=" * 70)
    log.info("真实链路单次 Benchmark")
    log.info("=" * 70")
    log.info("")

    # 构建 YOLO11-tiny 检测器
    try:
        detector = YoloDetector()
        log.info("[INFO] YOLO11-tiny 检测器初始化成功")
    except Exception as e:
        log.error(f"[ERROR] YOLO11-tiny 检测器初始化失败: {e}")
        return

    log.info("[INFO] 开始执行单次完整链路...")
    metrics = run_full_pipeline_once(detector)

    # 判定是否满足 250ms 标准
    target_ms = 250.0
    metrics["target_ms"] = target_ms
    metrics["pass"] = metrics["total_ms"] <= target_ms
    metrics["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    log.info("\n" + "=" * 70)
    log.info("测试结果")
    log.info("=" * 70")
    print(
        f"全链路延迟: {metrics['total_ms']:.2f} ms "
        f"(camera={metrics['camera_ms']:.2f}, "
        f"det={metrics['detect_ms']:.2f}, "
        f"nav={metrics['nav_ms']:.2f}, "
        f"tts={metrics['tts_ms']:.2f})"
    )
    log.info(f"检测数量: {metrics['num_detections']}")
    log.info(f"目标延迟: {target_ms} ms")
    log.error(f"结果: {'✅ PASS' if metrics['pass'] else '❌ FAIL'}")
    log.info("")
    log.info(f"详细结果已写入: {report_path}")
    log.info("=" * 70")


if __name__ == "__main__":
    main()


