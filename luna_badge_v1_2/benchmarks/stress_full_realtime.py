from core.logging import get_logger

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
log = get_logger("stress_full_realtime")
"""
并发压测 + 热衰减：真实链路版本
基于真实模块，不是 sleep 模拟
"""

import json
import os
import sys
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

# 添加项目路径
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

# 导入真实链路函数（使用绝对导入）
import importlib.util
spec = importlib.util.spec_from_file_location(
    "benchmark_full_realtime",
    os.path.join(os.path.dirname(__file__), "benchmark_full_realtime.py")
)
benchmark_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(benchmark_module)
run_full_pipeline_once = benchmark_module.run_full_pipeline_once
ensure_dir = benchmark_module.ensure_dir

REPORT_PATH = "test_reports/stress_full_realtime_report.json"


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


def stress_test(duration_sec: int = 60, concurrency: int = 4, target_ms: float = 250.0):
    """并发压测真实链路"""
    ensure_dir(REPORT_PATH)

    start = time.time()
    futures = []
    latencies = []
    errors = []

    log.info(f"\n=== 真实链路压测开始：duration={duration_sec}s, concurrency={concurrency} ===")
    log.info(f"目标延迟: {target_ms}ms\n")

    def worker():
        m = run_full_pipeline_once()
        return m

    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        # 在 duration 内不断提交任务
        submitted = 0
        while time.time() - start < duration_sec:
            futures.append(pool.submit(worker))
            submitted += 1
            if submitted % 10 == 0:
                log.info(f"  已提交 {submitted} 个任务...")
            time.sleep(0.1)  # 控制提交频率

        log.info(f"\n  等待 {len(futures)} 个任务完成...")
        completed = 0
        for fut in as_completed(futures):
            m = fut.result()
            if m["success"]:
                latencies.append(m["total_ms"])
            else:
                errors.append(m.get("error", "Unknown error"))
            completed += 1
            if completed % 50 == 0:
                log.info(f"  已完成 {completed}/{len(futures)} 个任务...")

    total = len(latencies) + len(errors)
    error_rate = len(errors) / total if total else 0.0

    summary = {
        "timestamp": datetime.now().isoformat(),
        "duration_sec": duration_sec,
        "concurrency": concurrency,
        "target_ms": target_ms,
        "total_runs": total,
        "success": len(latencies),
        "failures": len(errors),
        "error_rate": error_rate,
        "avg_ms": statistics.mean(latencies) if latencies else None,
        "p50_ms": percentile(latencies, 50),
        "p90_ms": percentile(latencies, 90),
        "p95_ms": percentile(latencies, 95),
        "p99_ms": percentile(latencies, 99),
        "min_ms": min(latencies) if latencies else None,
        "max_ms": max(latencies) if latencies else None,
        "over_target_count": sum(1 for v in latencies if v > target_ms),
        "over_target_ratio": sum(1 for v in latencies if v > target_ms) / len(latencies) if latencies else 0.0,
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    log.info("\n=== 压测完成 ===")
    log.info("json.dumps(summary, indent=2, ensure_ascii=False)")
    log.info(f"\n✅ 报告已保存: {REPORT_PATH}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="真实链路压测")
    parser.add_argument("--duration", type=int, default=60, help="压测持续时间（秒）")
    parser.add_argument("--concurrency", type=int, default=4, help="并发线程数")
    parser.add_argument("--target", type=float, default=250.0, help="目标延迟（ms）")
    args = parser.parse_args()
    
    stress_test(duration_sec=args.duration, concurrency=args.concurrency, target_ms=args.target)

