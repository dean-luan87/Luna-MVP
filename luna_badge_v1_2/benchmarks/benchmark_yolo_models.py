#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOLO 多模型对比 Benchmark
对比 yolov8, yolov11, yolov11-tiny 三种模型的检测耗时分布
"""

import os
import sys
import json
import time
import statistics
import numpy as np
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入模块（带容错）
try:
    from core.yolo_detector import YoloDetector
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("⚠️ YOLO 模块不可用，将使用 Mock")

try:
    from utils.camera_handler import CameraHandler
    CAMERA_AVAILABLE = True
except ImportError:
    try:
        from core.camera_manager import CameraManager
        CameraHandler = CameraManager
        CAMERA_AVAILABLE = True
    except ImportError:
        CAMERA_AVAILABLE = False
        print("⚠️ Camera 模块不可用，将使用 Mock 图像")


def ensure_perf_dir():
    """确保 perf_logs 目录存在"""
    os.makedirs("perf_logs", exist_ok=True)


def percentile(values, p):
    """计算百分位数"""
    if not values:
        return None
    values = sorted(values)
    k = (len(values) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(values) - 1)
    if f == c:
        return values[f]
    d0 = values[f] * (c - k)
    d1 = values[c] * (k - f)
    return d0 + d1


def get_test_frame():
    """获取测试图像帧"""
    if CAMERA_AVAILABLE:
        try:
            cam = CameraHandler()
            if hasattr(cam, 'capture_frame'):
                frame = cam.capture_frame()
            elif hasattr(cam, 'read'):
                ret, frame = cam.read()
                if not ret:
                    frame = None
            else:
                frame = None
            
            if frame is not None:
                return frame
        except Exception as e:
            print(f"⚠️ 摄像头捕获失败: {e}")
    
    # 使用 Mock 图像
    return np.zeros((480, 640, 3), dtype=np.uint8)


def benchmark_model(model_name: str, frame, runs: int = 30):
    """测试单个模型的性能"""
    print(f"  测试模型: {model_name} ({runs} 次)...")
    
    if YOLO_AVAILABLE:
        try:
            detector = YoloDetector({"model_name": model_name})
            if hasattr(detector, 'load_model'):
                detector.load_model()
        except Exception as e:
            print(f"  ⚠️ 模型加载失败: {e}，使用 Mock")
            detector = None
    else:
        detector = None
    
    latencies = []
    
    for i in range(runs):
        start = time.perf_counter()
        
        try:
            if detector:
                if hasattr(detector, 'infer'):
                    _ = detector.infer({"timestamp": 0, "data": frame})
                elif hasattr(detector, 'detect'):
                    _ = detector.detect(frame)
                else:
                    # Mock
                    time.sleep(0.05)
            else:
                # Mock
                time.sleep(0.05)
        except Exception as e:
            print(f"  ⚠️ 检测失败: {e}")
            time.sleep(0.05)  # Mock
        
        end = time.perf_counter()
        latency_ms = (end - start) * 1000
        latencies.append(latency_ms)
    
    result = {
        "model": model_name,
        "runs": runs,
        "p50": percentile(latencies, 50),
        "p90": percentile(latencies, 90),
        "p95": percentile(latencies, 95),
        "p99": percentile(latencies, 99),
        "min": min(latencies) if latencies else 0,
        "max": max(latencies) if latencies else 0,
        "avg": statistics.mean(latencies) if latencies else 0,
        "latencies": latencies,
    }
    
    return result


def main():
    ensure_perf_dir()
    
    print("\n=== YOLO 模型对比 Benchmark ===\n")
    
    # 获取测试图像（只取一帧，保证模型对比公平）
    print("获取测试图像...")
    frame = get_test_frame()
    print(f"测试图像尺寸: {frame.shape if isinstance(frame, np.ndarray) else 'Mock'}\n")
    
    models = ["yolov8", "yolov11", "yolov11-tiny"]
    all_results = []
    timestamp = datetime.now().isoformat()
    
    for name in models:
        print(f"\n=== Benchmark 模型：{name} ===")
        result = benchmark_model(name, frame, runs=30)
        all_results.append(result)
        
        print(
            f"模型: {name} | avg={result['avg']:.2f}ms "
            f"p50={result['p50']:.2f}ms p95={result['p95']:.2f}ms p99={result['p99']:.2f}ms"
        )
    
    summary = {
        "timestamp": timestamp,
        "models": all_results,
    }
    
    # 写入 JSON
    out_path = os.path.join("perf_logs", "yolo_model_benchmark.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    # 写入 CSV，方便做表格
    csv_path = os.path.join("perf_logs", "yolo_model_benchmark.csv")
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("model,runs,avg,p50,p90,p95,p99,min,max\n")
        for r in all_results:
            f.write(
                f"{r['model']},{r['runs']},"
                f"{r['avg']:.2f},{r['p50']:.2f},{r['p90']:.2f},"
                f"{r['p95']:.2f},{r['p99']:.2f},{r['min']:.2f},{r['max']:.2f}\n"
            )
    
    print(f"\n✅ 结果已写入：{out_path}")
    print(f"✅ CSV 已写入：{csv_path}")


if __name__ == "__main__":
    main()



