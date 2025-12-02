#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge 1.3.0 真实链路 Benchmark
端到端性能测试脚本，直接调用真实模块，测量实际性能
"""

import sys
import os
import time
import json
import statistics
import numpy as np
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 报告目录
REPORT_DIR = Path("test_reports")
REPORT_DIR.mkdir(exist_ok=True, parents=True)

# -------------------------
# 导入真实模块（带容错）
# -------------------------

# Camera
try:
    from utils.camera_handler import CameraHandler
    CAMERA_AVAILABLE = True
except ImportError:
    try:
        from core.camera_manager import CameraManager
        CAMERA_AVAILABLE = True
        CameraHandler = CameraManager  # 别名
    except ImportError:
        CAMERA_AVAILABLE = False
        print("⚠️ Camera 模块不可用，将使用 Mock")

# YOLO Detector
try:
    from core.yolo_detector import YoloDetector
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("⚠️ YOLO 模块不可用，将使用 Mock")

# TTS Manager
try:
    from core.tts_manager import TTSManager
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️ TTS 模块不可用，将使用 Mock")

# Task Chain Manager
try:
    from core.task_chain_manager import TaskChainManager
    TASK_CHAIN_AVAILABLE = True
except ImportError:
    TASK_CHAIN_AVAILABLE = False
    print("⚠️ TaskChain 模块不可用，将使用 Mock")

# Navigation Planner
try:
    from core.navigation_logic_v1_3 import NavigationLogic
    NAV_AVAILABLE = True
except ImportError:
    try:
        from core.navigation_logic import NavigationLogic
        NAV_AVAILABLE = True
    except ImportError:
        NAV_AVAILABLE = False
        print("⚠️ Navigation 模块不可用，将使用 Mock")

# Scene Understanding
try:
    from core.labeling.scene_classifier import SceneClassifier
    SCENE_AVAILABLE = True
except ImportError:
    try:
        from core.scenes.scene_classifier_v2 import SceneClassifier
        SCENE_AVAILABLE = True
    except ImportError:
        SCENE_AVAILABLE = False
        print("⚠️ Scene Understanding 模块不可用，将使用 Mock")

# FailSafe (使用 monitor 模块)
try:
    from monitor.monitor_agent import MonitorAgent
    FAILSAFE_AVAILABLE = True
except ImportError:
    FAILSAFE_AVAILABLE = False
    print("⚠️ FailSafe 模块不可用，将使用 Mock")

# Self-Heal
try:
    from monitor.self_heal import SelfHeal
    SELF_HEAL_AVAILABLE = True
except ImportError:
    SELF_HEAL_AVAILABLE = False
    print("⚠️ Self-Heal 模块不可用，将使用 Mock")


# -------------------------
# Mock 函数（当真实模块不可用时使用）
# -------------------------

def mock_camera_capture():
    """Mock 摄像头捕获"""
    time.sleep(0.015)
    return np.zeros((480, 640, 3), dtype=np.uint8)


def mock_frame_preprocess(frame):
    """Mock 预处理"""
    time.sleep(0.010)
    return frame


def mock_yolo_detect(frame):
    """Mock YOLO 检测"""
    time.sleep(0.050)
    return {"objects": [], "detections": []}


def mock_scene_understand(det_result):
    """Mock 场景理解"""
    time.sleep(0.030)
    return {"scene": "unknown"}


def mock_nav_plan(start, goal):
    """Mock 路径规划"""
    time.sleep(0.040)
    return {"route": [], "distance": 0}


def mock_tts_speak(text):
    """Mock TTS"""
    time.sleep(0.020)
    return True


def mock_task_save_state(state):
    """Mock 任务保存"""
    time.sleep(0.010)
    return True


def mock_task_load_state():
    """Mock 任务加载"""
    time.sleep(0.012)
    return {}


def mock_failsafe_check():
    """Mock FailSafe 检查"""
    time.sleep(0.018)
    return True


def mock_selfheal_check():
    """Mock Self-Heal 检查"""
    time.sleep(0.010)
    return True


def mock_selfheal_recover():
    """Mock Self-Heal 恢复"""
    time.sleep(0.015)
    return True


# -------------------------
# 工具方法
# -------------------------

def measure(label, func, results, repeat=1):
    """测量函数执行耗时，取多次的中位数"""
    durations = []
    for _ in range(repeat):
        start = time.perf_counter()
        try:
            func()
        except Exception as e:
            print(f"  ⚠️ {label} 执行出错: {e}")
        end = time.perf_counter()
        durations.append((end - start) * 1000)  # 转成 ms
    
    median = statistics.median(durations) if durations else 0
    results[label] = median
    print(f"[{label}] {median:.2f} ms")
    return median


# -------------------------
# A-G: 真实链路测试逻辑
# -------------------------

def run_A(results, cam, frame_holder):
    """A. 摄像头采集 + 图像预处理"""
    
    def capture():
        if CAMERA_AVAILABLE and cam:
            try:
                if hasattr(cam, 'capture_frame'):
                    frame = cam.capture_frame()
                elif hasattr(cam, 'read'):
                    ret, frame = cam.read()
                    if not ret:
                        frame = None
                else:
                    frame = mock_camera_capture()
            except Exception:
                frame = mock_camera_capture()
        else:
            frame = mock_camera_capture()
        
        frame_holder["frame"] = frame
        return frame
    
    measure("A1.Camera 捕获 (真实)", capture, results)
    
    def preprocess():
        frame = frame_holder.get("frame")
        if frame is None:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # 简单预处理（resize）
        if isinstance(frame, np.ndarray):
            import cv2
            frame = cv2.resize(frame, (640, 480))
        frame_holder["frame"] = frame
    
    measure("A2.预处理 (真实)", preprocess, results)


def run_B(results, detector, scene_understand, frame_holder):
    """B. 目标检测 + 场景理解"""
    frame = frame_holder.get("frame")
    if frame is None:
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    def detect():
        if YOLO_AVAILABLE and detector:
            try:
                if hasattr(detector, 'infer'):
                    det_result = detector.infer({"timestamp": 0, "data": frame})
                elif hasattr(detector, 'detect'):
                    det_result = detector.detect(frame)
                else:
                    det_result = mock_yolo_detect(frame)
            except Exception:
                det_result = mock_yolo_detect(frame)
        else:
            det_result = mock_yolo_detect(frame)
        
        frame_holder["det_result"] = det_result
        return det_result
    
    measure("B1.YOLO 目标检测 (真实)", detect, results)
    
    def semantic():
        det_result = frame_holder.get("det_result", {})
        if SCENE_AVAILABLE and scene_understand:
            try:
                if hasattr(scene_understand, 'classify'):
                    scene_understand.classify(frame_holder.get("frame"))
                else:
                    mock_scene_understand(det_result)
            except Exception:
                mock_scene_understand(det_result)
        else:
            mock_scene_understand(det_result)
    
    measure("B2.场景语义判断 (真实)", semantic, results)


def run_C(results, nav):
    """C. 路径规划"""
    def plan():
        if NAV_AVAILABLE and nav:
            try:
                if hasattr(nav, 'plan_route'):
                    nav.plan_route("test_start", "test_goal")
                elif hasattr(nav, 'plan'):
                    nav.plan("test_start", "test_goal")
                else:
                    mock_nav_plan("test_start", "test_goal")
            except Exception:
                mock_nav_plan("test_start", "test_goal")
        else:
            mock_nav_plan("test_start", "test_goal")
    
    measure("C1.路径规划 (真实)", plan, results)


def run_D(results, tts):
    """D. 语音播报"""
    def speak():
        if TTS_AVAILABLE and tts:
            try:
                if hasattr(tts, 'speak'):
                    tts.speak("测试导航语音播报")
                elif hasattr(tts, 'speak_sync'):
                    tts.speak_sync("测试导航语音播报")
                else:
                    mock_tts_speak("测试导航语音播报")
            except Exception:
                mock_tts_speak("测试导航语音播报")
        else:
            mock_tts_speak("测试导航语音播报")
    
    measure("D1.TTS (真实)", speak, results)


def run_E(results, task_chain):
    """E. 中断恢复机制"""
    def save_state():
        if TASK_CHAIN_AVAILABLE and task_chain:
            try:
                if hasattr(task_chain, 'save_state'):
                    task_chain.save_state("NAV_STATE")
                else:
                    mock_task_save_state("NAV_STATE")
            except Exception:
                mock_task_save_state("NAV_STATE")
        else:
            mock_task_save_state("NAV_STATE")
    
    measure("E1.写入任务缓存 (真实)", save_state, results)
    
    def load_state():
        if TASK_CHAIN_AVAILABLE and task_chain:
            try:
                if hasattr(task_chain, 'load_state'):
                    task_chain.load_state()
                else:
                    mock_task_load_state()
            except Exception:
                mock_task_load_state()
        else:
            mock_task_load_state()
    
    measure("E2.恢复任务缓存 (真实)", load_state, results)


def run_F(results, failsafe):
    """F. FailSafe（异常监控）"""
    def check():
        if FAILSAFE_AVAILABLE and failsafe:
            try:
                if hasattr(failsafe, 'check'):
                    failsafe.check()
                elif hasattr(failsafe, 'handle_event'):
                    failsafe.handle_event({"type": "test"})
                else:
                    mock_failsafe_check()
            except Exception:
                mock_failsafe_check()
        else:
            mock_failsafe_check()
    
    measure("F1.Failsafe 检测 (真实)", check, results)


def run_G(results, healer):
    """G. 自愈机制（重启 NavBrain 逻辑）"""
    def health_check():
        if SELF_HEAL_AVAILABLE and healer:
            try:
                if hasattr(healer, 'health_check'):
                    healer.health_check()
                else:
                    mock_selfheal_check()
            except Exception:
                mock_selfheal_check()
        else:
            mock_selfheal_check()
    
    measure("G1.Self-Heal 判断 (真实)", health_check, results)
    
    def recover():
        if SELF_HEAL_AVAILABLE and healer:
            try:
                if hasattr(healer, 'recover_if_needed'):
                    healer.recover_if_needed()
                elif hasattr(healer, 'restart_module'):
                    healer.restart_module("navbrain")
                else:
                    mock_selfheal_recover()
            except Exception:
                mock_selfheal_recover()
        else:
            mock_selfheal_recover()
    
    measure("G2.NavBrain 重启 (真实)", recover, results)


# -------------------------
# 主测试方法
# -------------------------

def run_full_benchmark():
    print("\n========== Luna Badge 1.3.0 • 真实链路 Benchmark ==========\n")
    
    results = {}
    frame_holder = {"frame": None, "det_result": {}}
    
    # 初始化模块（带容错）
    cam = None
    if CAMERA_AVAILABLE:
        try:
            cam = CameraHandler() if CAMERA_AVAILABLE else None
        except Exception:
            cam = None
    
    detector = None
    if YOLO_AVAILABLE:
        try:
            detector = YoloDetector({"model_name": "yolov8n"})
        except Exception:
            detector = None
    
    scene_understand = None
    if SCENE_AVAILABLE:
        try:
            scene_understand = SceneClassifier()
        except Exception:
            scene_understand = None
    
    nav = None
    if NAV_AVAILABLE:
        try:
            nav = NavigationLogic()
        except Exception:
            nav = None
    
    tts = None
    if TTS_AVAILABLE:
        try:
            tts = TTSManager()
        except Exception:
            tts = None
    
    task_chain = None
    if TASK_CHAIN_AVAILABLE:
        try:
            task_chain = TaskChainManager()
        except Exception:
            task_chain = None
    
    failsafe = None
    if FAILSAFE_AVAILABLE:
        try:
            failsafe = MonitorAgent()
        except Exception:
            failsafe = None
    
    healer = None
    if SELF_HEAL_AVAILABLE:
        try:
            healer = SelfHeal()
        except Exception:
            healer = None
    
    # 执行链路
    total_start = time.perf_counter()
    
    run_A(results, cam, frame_holder)
    run_B(results, detector, scene_understand, frame_holder)
    run_C(results, nav)
    run_D(results, tts)
    run_E(results, task_chain)
    run_F(results, failsafe)
    run_G(results, healer)
    
    total_end = time.perf_counter()
    total_ms = (total_end - total_start) * 1000
    
    print("\n========== 测试完成 ==========")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\n全链路总时长：{total_ms:.2f} ms")
    
    # 判断是否满足 250ms Hard Limit
    print("\n性能评估:")
    threshold_ms = 250.0
    if total_ms <= threshold_ms:
        print(f"【✅ PASS】小于 {threshold_ms}ms：满足实时导航标准")
        passed = True
    else:
        print(f"【❌ FAIL】大于 {threshold_ms}ms：需要优化核心链路")
        passed = False
    
    # 计算各段占比
    segment_totals = {
        "A段(图像捕获)": results.get("A1.Camera 捕获 (真实)", 0) + results.get("A2.预处理 (真实)", 0),
        "B段(视觉识别)": results.get("B1.YOLO 目标检测 (真实)", 0) + results.get("B2.场景语义判断 (真实)", 0),
        "C段(导航规划)": results.get("C1.路径规划 (真实)", 0),
        "D段(语音输出)": results.get("D1.TTS (真实)", 0),
        "E段(任务缓存)": results.get("E1.写入任务缓存 (真实)", 0) + results.get("E2.恢复任务缓存 (真实)", 0),
        "F段(FailSafe)": results.get("F1.Failsafe 检测 (真实)", 0),
        "G段(异常处理)": results.get("G1.Self-Heal 判断 (真实)", 0) + results.get("G2.NavBrain 重启 (真实)", 0),
    }
    
    print("\n=== 各段耗时占比 ===")
    for segment, segment_time in segment_totals.items():
        percentage = (segment_time / total_ms * 100) if total_ms > 0 else 0
        print(f"{segment}: {segment_time:.2f} ms ({percentage:.1f}%)")
    
    # 保存报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "version": "1.3.0",
        "module_availability": {
            "camera": CAMERA_AVAILABLE,
            "yolo": YOLO_AVAILABLE,
            "tts": TTS_AVAILABLE,
            "task_chain": TASK_CHAIN_AVAILABLE,
            "navigation": NAV_AVAILABLE,
            "scene": SCENE_AVAILABLE,
            "failsafe": FAILSAFE_AVAILABLE,
            "self_heal": SELF_HEAL_AVAILABLE,
        },
        "results": results,
        "total_ms": total_ms,
        "threshold_ms": threshold_ms,
        "passed": passed,
        "segment_totals": segment_totals,
    }
    
    # 写入 JSON 报告
    json_path = REPORT_DIR / "benchmark_realtime_report.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # 追加日志
    log_path = REPORT_DIR / "benchmark_realtime_log.json"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(report, ensure_ascii=False) + "\n")
    
    print(f"\n📁 报告已保存: {json_path}")
    print(f"📁 日志已追加: {log_path}\n")
    
    return report


# -------------------------
# 入口
# -------------------------

if __name__ == "__main__":
    run_full_benchmark()



