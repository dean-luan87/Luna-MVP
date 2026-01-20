#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import json
import statistics
import subprocess
from pathlib import Path
from core.logging import get_logger


log = get_logger("phase2_latency_test")
ROOT_DIR = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT_DIR / "test_reports"
REPORT_DIR.mkdir(exist_ok=True, parents=True)

# 默认跑 50 次，可通过环境变量覆盖
RUNS = int(os.environ.get("PHASE2_LATENCY_RUNS", "50"))


def run_one():
    """
    执行一次完整场景测试：
    把 test_scenes.py 视为一整条导航链路的集成测试。
    """
    cmd = ["python3", "-m", "pytest", "tests/test_scenes.py", "-q"]
    start = time.perf_counter()
    proc = subprocess.run(
        cmd,
        cwd=ROOT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    end = time.perf_counter()
    duration_ms = (end - start) * 1000.0

    return {
        "success": proc.returncode == 0,
        "returncode": proc.returncode,
        "duration_ms": duration_ms,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def percentile(values, p):
    if not values:
        return None
    values_sorted = sorted(values)
    k = (len(values_sorted) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(values_sorted) - 1)
    if f == c:
        return values_sorted[int(k)]
    d0 = values_sorted[f] * (c - k)
    d1 = values_sorted[c] * (k - f)
    return d0 + d1


def main():
    results = []
    log.info(f"Phase-2 链路延迟测试：共 {RUNS} 次完整链路 (test_scenes.py) ...")

    for i in range(RUNS):
        log.info(f"[{i+1}/{RUNS}] 运行中...", flush=True)
        res = run_one()
        results.append(res)
        status = "OK" if res["success"] else f"FAIL({res['returncode']})"
        log.info(f"  -> {status}, {res['duration_ms']:.2f} ms")

        # 如果有失败，直接打印错误信息，方便排查
        if not res["success"]:
            log.info("  stdout:")
            log.info("res["stdout"]")
            log.info("  stderr:")
            log.info("res["stderr"]")

    durations = [r["duration_ms"] for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    summary = {
        "runs": RUNS,
        "success": len(durations),
        "failed": len(failed),
        "durations_ms": durations,
    }

    if durations:
        summary.update(
            {
                "min_ms": min(durations),
                "max_ms": max(durations),
                "mean_ms": statistics.mean(durations),
                "p50_ms": percentile(durations, 50),
                "p90_ms": percentile(durations, 90),
                "p95_ms": percentile(durations, 95),
                "p99_ms": percentile(durations, 99),
            }
        )
    else:
        summary.update(
            {
                "min_ms": None,
                "max_ms": None,
                "mean_ms": None,
                "p50_ms": None,
                "p90_ms": None,
                "p95_ms": None,
                "p99_ms": None,
            }
        )

    # 写 JSON
    json_path = REPORT_DIR / "phase2_latency_report.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # 写 CSV（便于后续画图）
    csv_path = REPORT_DIR / "phase2_latency_samples.csv"
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("run_index,duration_ms,success,returncode\n")
        for idx, r in enumerate(results):
            f.write(
                f"{idx+1},{r['duration_ms']:.3f},{int(r['success'])},{r['returncode']}\n"
            )

    log.info("\n=== Phase-2 链路延迟测试完成 ===")
    log.error(f"成功次数: {summary['success']}, 失败次数: {summary['failed']}")
    if durations:
        print(
            "耗时统计(ms): "
            f"min={summary['min_ms']:.2f}, "
            f"max={summary['max_ms']:.2f}, "
            f"mean={summary['mean_ms']:.2f}, "
            f"p50={summary['p50_ms']:.2f}, "
            f"p90={summary['p90_ms']:.2f}, "
            f"p95={summary['p95_ms']:.2f}, "
            f"p99={summary['p99_ms']:.2f}"
        )
    else:
        log.info("无成功样本，无法计算耗时统计。")


if __name__ == "__main__":
    main()







