from core.logging import get_logger

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
log = get_logger("benchmark_full_pipeline")
"""
Luna Badge 1.3.0 全链路响应时间 Benchmark
端到端性能测试脚本，自动测试 A-G 七段链路，对标 250ms 标准
"""

import time
import json
import statistics
from datetime import datetime
from pathlib import Path

# 报告目录
REPORT_DIR = Path("test_reports")
REPORT_DIR.mkdir(exist_ok=True, parents=True)

# ---------------------------------------------------------
#  基础工具
# ---------------------------------------------------------
def measure(func, label, results, repeat=3):
    """测量函数执行耗时，取多次的中位数"""
    costs = []
    for _ in range(repeat):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        costs.append((end - start) * 1000)  # 转成 ms
    median_cost = statistics.median(costs)
    results[label] = median_cost
    log.info(f"[{label}] {median_cost:.2f} ms")
    return median_cost


# ---------------------------------------------------------
#  Mock 函数（真实环境中替换为实际模块调用）
# ---------------------------------------------------------

def camera_capture():
    """A1: Camera 捕获"""
    time.sleep(0.015)   # 15ms


def frame_preprocess():
    """A2: 预处理"""
    time.sleep(0.010)   # 10ms


def object_detection():
    """B1: 目标检测 YOLO"""
    time.sleep(0.050)   # 50ms


def env_semantic():
    """B2: 场景语义判断"""
    time.sleep(0.030)   # 30ms


def nav_planner():
    """C1: 路径规划"""
    time.sleep(0.040)   # 40ms


def tts_output():
    """D1: 语音合成"""
    time.sleep(0.020)   # 20ms


# ---------------------------------------------------------
#  A-G 测试任务集
# ---------------------------------------------------------

def run_A(results):
    """A段：图像捕获与预处理"""
    measure(camera_capture, "A1.Camera 捕获", results)
    measure(frame_preprocess, "A2.预处理", results)


def run_B(results):
    """B段：视觉识别与场景理解"""
    measure(object_detection, "B1.目标检测 YOLO", results)
    measure(env_semantic, "B2.场景语义判断", results)


def run_C(results):
    """C段：导航规划"""
    measure(nav_planner, "C1.路径规划", results)


def run_D(results):
    """D段：语音输出"""
    measure(tts_output, "D1.语音合成", results)


def run_E(results):
    """E段：任务缓存与恢复"""
    measure(lambda: time.sleep(0.010), "E1.任务缓存写入", results)
    measure(lambda: time.sleep(0.012), "E2.任务恢复", results)


def run_F(results):
    """F段：FailSafe 监控与自愈"""
    measure(lambda: time.sleep(0.018), "F1.FailSafe 监控", results)
    measure(lambda: time.sleep(0.015), "F2.自愈机制", results)


def run_G(results):
    """G段：异常处理与重启判定"""
    measure(lambda: time.sleep(0.010), "G1.异常捕捉", results)
    measure(lambda: time.sleep(0.015), "G2.NavBrain 重启判定", results)


# ---------------------------------------------------------
#  全链路执行
# ---------------------------------------------------------

def run_full_benchmark():
    log.info("\n=== Luna Badge 1.3.0 全链路响应 Benchmark ===\n")
    results = {}

    start_total = time.perf_counter()

    run_A(results)
    run_B(results)
    run_C(results)
    run_D(results)
    run_E(results)
    run_F(results)
    run_G(results)

    end_total = time.perf_counter()
    total_ms = (end_total - start_total) * 1000

    log.info("\n=== 总结 ===")
    log.info("json.dumps(results, indent=2, ensure_ascii=False)")
    log.info(f"\n全链路耗时: {total_ms:.2f} ms")

    # 判断是否达标
    threshold_ms = 250.0
    if total_ms <= threshold_ms:
        log.info(f"【✅ PASS】满足 {threshold_ms}ms 响应时间标准")
        passed = True
    else:
        log.error(f"【❌ FAIL】超出 {threshold_ms}ms 标准，需要优化")
        passed = False

    # 计算各段占比
    segment_totals = {
        "A段(图像捕获)": results.get("A1.Camera 捕获", 0) + results.get("A2.预处理", 0),
        "B段(视觉识别)": results.get("B1.目标检测 YOLO", 0) + results.get("B2.场景语义判断", 0),
        "C段(导航规划)": results.get("C1.路径规划", 0),
        "D段(语音输出)": results.get("D1.语音合成", 0),
        "E段(任务缓存)": results.get("E1.任务缓存写入", 0) + results.get("E2.任务恢复", 0),
        "F段(FailSafe)": results.get("F1.FailSafe 监控", 0) + results.get("F2.自愈机制", 0),
        "G段(异常处理)": results.get("G1.异常捕捉", 0) + results.get("G2.NavBrain 重启判定", 0),
    }

    log.info("\n=== 各段耗时占比 ===")
    for segment, segment_time in segment_totals.items():
        percentage = (segment_time / total_ms * 100) if total_ms > 0 else 0
        log.info(f"{segment}: {segment_time:.2f} ms ({percentage:.1f}%)")

    # 保存报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "version": "1.3.0",
        "results": results,
        "total_ms": total_ms,
        "threshold_ms": threshold_ms,
        "passed": passed,
        "segment_totals": segment_totals,
    }

    # 写入 JSON 报告
    json_path = REPORT_DIR / "benchmark_full_pipeline_report.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # 追加日志
    log_path = REPORT_DIR / "benchmark_log.json"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(report, ensure_ascii=False) + "\n")

    log.info(f"\n📁 报告已保存: {json_path}")
    log.info(f"📁 日志已追加: {log_path}")

    return report


# ---------------------------------------------------------
#  执行入口
# ---------------------------------------------------------

if __name__ == "__main__":
    run_full_benchmark()







