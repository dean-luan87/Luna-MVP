from core.logging import get_logger

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
log = get_logger("stress_full_realtime")
"""
真实链路压测

功能：
- 在真实链路基础上做 N 次压测（默认 60 秒内循环）
- 收集 total_ms 分布（avg / p50 / p90 / p95 / p99）
- 写入 perf_logs，后续给 Dashboard 用
"""

import os
import json
import time
import threading
import csv
from pathlib import Path
from typing import List, Dict, Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
import sys

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.yolo_detector import YoloDetector
from tests.benchmark_full_realtime import (
    run_full_pipeline_once,
)  # 复用刚才的真实链路逻辑


def _percentile(data: List[float], p: float) -> float:
    """计算百分位数"""
    if not data:
        return 0.0
    data_sorted = sorted(data)
    k = (len(data_sorted) - 1) * p
    f = int(k)
    c = min(f + 1, len(data_sorted) - 1)
    if f == c:
        return data_sorted[int(k)]
    d0 = data_sorted[f] * (c - k)
    d1 = data_sorted[c] * (k - f)
    return d0 + d1


def worker(detector: YoloDetector, results: List[float], lock: threading.Lock, duration_s: int, stop_flag):
    """工作线程：持续运行压测"""
    end_time = time.time() + duration_s
    while time.time() < end_time and not stop_flag[0]:
        try:
            m = run_full_pipeline_once(detector)
            with lock:
                results.append(m["total_ms"])
        except Exception as e:
            # 出错时记录 -1，后续统计时可过滤
            log.error(f"[STRESS] error: {e}")
            with lock:
                results.append(-1.0)


def main():
    os.makedirs(ROOT / "perf_logs", exist_ok=True)
    report_path = ROOT / "perf_logs" / "full_realtime_stress_report.json"
    samples_path = ROOT / "perf_logs" / "full_realtime_stress_samples.csv"

    # 参数：持续时间 & 线程数
    duration_s = int(os.getenv("LUNA_STRESS_DURATION", "60"))
    num_threads = int(os.getenv("LUNA_STRESS_THREADS", "4"))

    log.info("\n" + "=" * 70)
    log.info("真实链路压测")
    log.info("=" * 70")
    log.info(f"持续时间: {duration_s} 秒")
    log.info(f"并发线程: {num_threads}")
    log.info("=" * 70")
    log.info("")

    try:
        detector = YoloDetector()
        log.info("[INFO] YOLO11-tiny 检测器初始化成功")
    except Exception as e:
        log.error(f"[ERROR] YOLO11-tiny 检测器初始化失败: {e}")
        return

    results: List[float] = []
    lock = threading.Lock()
    stop_flag = [False]

    threads = [
        threading.Thread(target=worker, args=(detector, results, lock, duration_s, stop_flag))
        for _ in range(num_threads)
    ]

    log.info("[INFO] 开始压测...")
    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end = time.perf_counter()

    # 过滤错误样本
    ok_samples = [x for x in results if x >= 0]
    error_count = len(results) - len(ok_samples)

    if ok_samples:
        avg = float(sum(ok_samples) / len(ok_samples))
        p50 = _percentile(ok_samples, 0.5)
        p90 = _percentile(ok_samples, 0.9)
        p95 = _percentile(ok_samples, 0.95)
        p99 = _percentile(ok_samples, 0.99)
        min_v = min(ok_samples)
        max_v = max(ok_samples)
    else:
        avg = p50 = p90 = p95 = p99 = min_v = max_v = 0.0

    report: Dict[str, Any] = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "duration_s": duration_s,
        "threads": num_threads,
        "num_samples": len(results),
        "num_ok_samples": len(ok_samples),
        "num_error_samples": error_count,
        "error_rate": round(error_count / len(results) * 100, 2) if results else 0.0,
        "avg_ms": round(avg, 2),
        "p50_ms": round(p50, 2),
        "p90_ms": round(p90, 2),
        "p95_ms": round(p95, 2),
        "p99_ms": round(p99, 2),
        "min_ms": round(min_v, 2),
        "max_ms": round(max_v, 2),
        "total_runtime_s": round(end - start, 2),
    }

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # 写入 CSV 样本
    with open(samples_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["total_ms"])
        for v in ok_samples:
            writer.writerow([f"{v:.3f}"])

    log.info("\n" + "=" * 70)
    log.info("压测结果")
    log.info("=" * 70")
    log.info(f"总样本数: {len(results)}")
    log.info(f"成功样本: {len(ok_samples)}")
    log.error(f"错误样本: {error_count} (错误率: {report['error_rate']:.2f}%)")
    log.info("")
    log.info("延迟统计:")
    log.info(f"  平均: {avg:.2f}ms")
    log.info(f"  P50:  {p50:.2f}ms")
    log.info(f"  P90:  {p90:.2f}ms")
    log.info(f"  P95:  {p95:.2f}ms")
    log.info(f"  P99:  {p99:.2f}ms")
    log.info(f"  最小: {min_v:.2f}ms")
    log.info(f"  最大: {max_v:.2f}ms")
    log.info("")
    log.info(f"报告: {report_path}")
    log.info(f"样本: {samples_path}")
    log.info("=" * 70")


if __name__ == "__main__":
    main()


