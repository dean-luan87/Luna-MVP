#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import json
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.logging import get_logger


log = get_logger("phase2_concurrency_test")
ROOT_DIR = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT_DIR / "test_reports"
REPORT_DIR.mkdir(exist_ok=True, parents=True)

# 并发线程数 & 每线程任务数，可通过环境变量配置
CONCURRENCY = int(os.environ.get("PHASE2_CONCURRENCY", "4"))
TASKS_PER_WORKER = int(os.environ.get("PHASE2_TASKS_PER_WORKER", "5"))


def run_one(job_id: int):
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
        "job_id": job_id,
        "success": proc.returncode == 0,
        "returncode": proc.returncode,
        "duration_ms": duration_ms,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def main():
    total_tasks = CONCURRENCY * TASKS_PER_WORKER
    print(
        f"Phase-2 并发稳定性测试：并发={CONCURRENCY}, "
        f"每线程任务={TASKS_PER_WORKER}, 总任务={total_tasks}"
    )

    results = []
    job_id = 0

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = []
        for _ in range(CONCURRENCY):
            for _ in range(TASKS_PER_WORKER):
                job_id += 1
                futures.append(executor.submit(run_one, job_id))

        for fut in as_completed(futures):
            res = fut.result()
            results.append(res)
            status = "OK" if res["success"] else f"FAIL({res['returncode']})"
            print(
                f"[job {res['job_id']:03d}] -> {status}, "
                f"{res['duration_ms']:.2f} ms"
            )
            if not res["success"]:
                log.info("  stdout:")
                log.info("res["stdout"]")
                log.info("  stderr:")
                log.info("res["stderr"]")

    successes = [r for r in results if r["success"]]
    failures = [r for r in results if not r["success"]]
    durations = [r["duration_ms"] for r in successes]

    summary = {
        "concurrency": CONCURRENCY,
        "tasks_per_worker": TASKS_PER_WORKER,
        "total_tasks": total_tasks,
        "success": len(successes),
        "failed": len(failures),
        "durations_ms": durations,
    }

    if durations:
        import statistics

        def percentile(values, p):
            values_sorted = sorted(values)
            k = (len(values_sorted) - 1) * (p / 100.0)
            f = int(k)
            c = min(f + 1, len(values_sorted) - 1)
            if f == c:
                return values_sorted[int(k)]
            d0 = values_sorted[f] * (c - k)
            d1 = values_sorted[c] * (k - f)
            return d0 + d1

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

    json_path = REPORT_DIR / "phase2_concurrency_report.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    csv_path = REPORT_DIR / "phase2_concurrency_samples.csv"
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("job_id,duration_ms,success,returncode\n")
        for r in results:
            f.write(
                f"{r['job_id']},{r['duration_ms']:.3f},"
                f"{int(r['success'])},{r['returncode']}\n"
            )

    log.info("\n=== Phase-2 并发稳定性测试完成 ===")
    log.error(f"成功任务: {len(successes)}, 失败任务: {len(failures)}")
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


if __name__ == "__main__":
    main()


















