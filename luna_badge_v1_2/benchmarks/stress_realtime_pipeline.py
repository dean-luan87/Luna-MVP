from core.logging import get_logger

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
log = get_logger("stress_realtime_pipeline")
"""
链路压测脚本（并发 + 热衰减）
持续压测真实链路，观察性能衰减和错误率
"""

import os
import sys
import json
import time
import statistics
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入真实链路函数
try:
    from benchmark_realtime_pipeline import run_full_benchmark
    PIPELINE_AVAILABLE = True
except ImportError:
    PIPELINE_AVAILABLE = False
    log.info("⚠️ 真实链路模块不可用，将使用 Mock")


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


def run_full_pipeline_once():
    """执行一次完整链路（适配真实模块）"""
    if PIPELINE_AVAILABLE:
        try:
            # 运行 benchmark 并捕获结果
            import io
            import contextlib
            f = io.StringIO()
            with contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
                report = run_full_benchmark()
            return report.get("total_ms", 0) if isinstance(report, dict) else 0
        except Exception as e:
            log.info(f"⚠️ 链路执行失败: {e}")
            return None
    else:
        # Mock 版本（快速执行）
        time.sleep(0.01)  # 减少 Mock 时间，加快压测
        return 200.0


def stress_test(duration_sec=60, concurrency=4):
    """并发压测，持续 duration_sec 秒，观察热衰减"""
    ensure_perf_dir()
    
    latencies = []
    errors = 0
    start_time = time.time()
    
    log.info(f"\n=== 压测开始：{duration_sec}s, 并发={concurrency} ===")
    
    def worker():
        nonlocal errors
        try:
            total_ms = run_full_pipeline_once()
            return total_ms
        except Exception as e:
            errors += 1
            log.info(f"  ⚠️ 任务失败: {e}")
            return None
    
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = []
        while time.time() - start_time < duration_sec:
            futures.append(executor.submit(worker))
            time.sleep(0.1)  # 控制提交频率
        
        completed = 0
        for fut in as_completed(futures):
            ms = fut.result()
            if ms is not None:
                latencies.append(ms)
            completed += 1
            if completed % 10 == 0:
                log.info(f"  已完成: {completed} 个任务...")
    
    end_time = time.time()
    
    success = len(latencies)
    total = success + errors
    error_rate = (errors / total) * 100 if total > 0 else 0
    
    log.info(f"\n=== 压测结束 ===")
    log.info(f"总请求数: {total}")
    log.info(f"成功: {success}")
    log.error(f"失败: {errors} (错误率 {error_rate:.2f}%)")
    
    if latencies:
        avg = statistics.mean(latencies)
        p50 = percentile(latencies, 50)
        p90 = percentile(latencies, 90)
        p95 = percentile(latencies, 95)
        p99 = percentile(latencies, 99)
        print(
            f"平均延迟: {avg:.2f}ms | "
            f"P50={p50:.2f}ms P90={p90:.2f}ms P95={p95:.2f}ms P99={p99:.2f}ms"
        )
    else:
        avg = p50 = p90 = p95 = p99 = None
        log.info("无成功请求，无法统计延迟")
    
    # 写日志
    result = {
        "timestamp": datetime.now().isoformat(),
        "duration_sec": duration_sec,
        "concurrency": concurrency,
        "total": total,
        "success": success,
        "errors": errors,
        "error_rate": error_rate,
        "latencies": latencies,
        "avg": avg,
        "p50": p50,
        "p90": p90,
        "p95": p95,
        "p99": p99,
    }
    
    out_path = os.path.join("perf_logs", "stress_realtime_result.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # CSV，便于可视化
    csv_path = os.path.join("perf_logs", "stress_realtime_samples.csv")
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("index,latency_ms\n")
        for idx, v in enumerate(latencies):
            f.write(f"{idx},{v:.2f}\n")
    
    log.info(f"\n✅ 压测结果已写入: {out_path}")
    log.info(f"✅ 样本数据已写入: {csv_path}")


if __name__ == "__main__":
    # 示例：60 秒，并发 4
    import argparse
    parser = argparse.ArgumentParser(description="链路压测脚本")
    parser.add_argument("--duration", type=int, default=60, help="压测持续时间（秒）")
    parser.add_argument("--concurrency", type=int, default=4, help="并发线程数")
    args = parser.parse_args()
    
    stress_test(duration_sec=args.duration, concurrency=args.concurrency)

