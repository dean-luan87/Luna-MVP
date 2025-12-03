#!/usr/bin/env python3
import csv
import io
import json
import os
import random
import subprocess
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

import numpy as np
import requests
from core.logging import get_logger


log = get_logger("heat_decay_test")
try:
    import psutil
except ImportError:
    psutil = None

import cv2

API_URL = os.environ.get("LUNA_HEAT_API", "http://127.0.0.1:5001/api/frame")
DURATION_SEC = int(os.environ.get("LUNA_HEAT_DURATION", "600"))  # 默认 10 分钟
TARGET_FPS = float(os.environ.get("LUNA_HEAT_FPS", "5"))         # 默认 5 FPS

OUT_DIR = "perf_logs"
os.makedirs(OUT_DIR, exist_ok=True)

TS = datetime.now().strftime("%Y%m%d_%H%M%S")
CSV_PATH = os.path.join(OUT_DIR, f"heat_decay_{TS}.csv")
JSON_PATH = os.path.join(OUT_DIR, f"heat_decay_{TS}.json")


def gen_dummy_frame(width: int = 640, height: int = 480) -> bytes:
    """生成一张随机图像（模拟摄像头）。"""
    img = (np.random.rand(height, width, 3) * 255).astype("uint8")
    _, buf = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    return buf.tobytes()


def get_cpu_mem() -> Dict[str, float]:
    if psutil is None:
        return {"cpu": -1.0, "mem": -1.0}
    cpu = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory().percent
    return {"cpu": cpu, "mem": mem}


def get_gpu_temp_mem() -> Dict[str, float]:
    """
    使用 nvidia-smi，如果不存在则返回 -1。
    """
    try:
        out = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=temperature.gpu,memory.used,memory.total",
                "--format=csv,noheader,nounits",
            ],
            stderr=subprocess.DEVNULL,
            timeout=1.0,
        )
        line = out.decode("utf-8").strip().split("\n")[0]
        t_str, used_str, total_str = [x.strip() for x in line.split(",")]
        temp = float(t_str)
        mem_used = float(used_str)
        mem_total = float(total_str)
        return {
            "gpu_temp": temp,
            "gpu_mem_used": mem_used,
            "gpu_mem_total": mem_total,
        }
    except Exception:
        return {
            "gpu_temp": -1.0,
            "gpu_mem_used": -1.0,
            "gpu_mem_total": -1.0,
        }


def main() -> None:
    log.info("===========================================")
    log.info(" Luna Badge v1.3.0 热衰减压测")
    log.info("===========================================")
    log.info(f"API: {API_URL}")
    log.info(f"持续时间: {DURATION_SEC} 秒")
    log.info(f"目标 FPS: {TARGET_FPS}")
    log.info(f"CSV: {CSV_PATH}")
    log.info(f"JSON: {JSON_PATH}")
    log.info("===========================================")

    interval = 1.0 / TARGET_FPS
    end_time = datetime.now() + timedelta(seconds=DURATION_SEC)

    records = []

    with open(CSV_PATH, "w", newline="") as f_csv:
        writer = csv.writer(f_csv)
        writer.writerow(
            [
                "ts",
                "latency_ms",
                "status_code",
                "ok",
                "cpu_percent",
                "mem_percent",
                "gpu_temp",
                "gpu_mem_used",
                "gpu_mem_total",
                "box_count",
            ]
        )

        n_ok = 0
        n_total = 0
        latencies = []

        while datetime.now() < end_time:
            loop_start = time.perf_counter()

            ts = datetime.now().isoformat()
            frame_bytes = gen_dummy_frame()

            files = {"frame": ("frame.jpg", frame_bytes, "image/jpeg")}
            cpu_mem = get_cpu_mem()
            gpu_stats = get_gpu_temp_mem()

            t0 = time.perf_counter()
            try:
                resp = requests.post(API_URL, files=files, timeout=5)
                t1 = time.perf_counter()
                latency_ms = (t1 - t0) * 1000.0
                n_total += 1

                if resp.ok:
                    data = resp.json()
                    box_count = int(data.get("box_count", -1))
                    n_ok += 1
                    latencies.append(latency_ms)
                    ok_flag = 1
                else:
                    box_count = -1
                    ok_flag = 0

                writer.writerow(
                    [
                        ts,
                        f"{latency_ms:.2f}",
                        resp.status_code,
                        ok_flag,
                        f"{cpu_mem['cpu']:.2f}",
                        f"{cpu_mem['mem']:.2f}",
                        f"{gpu_stats['gpu_temp']:.2f}",
                        f"{gpu_stats['gpu_mem_used']:.2f}",
                        f"{gpu_stats['gpu_mem_total']:.2f}",
                        box_count,
                    ]
                )

            except Exception as e:
                t1 = time.perf_counter()
                latency_ms = (t1 - t0) * 1000.0
                n_total += 1
                writer.writerow(
                    [
                        ts,
                        f"{latency_ms:.2f}",
                        -1,
                        0,
                        f"{cpu_mem['cpu']:.2f}",
                        f"{cpu_mem['mem']:.2f}",
                        f"{gpu_stats['gpu_temp']:.2f}",
                        f"{gpu_stats['gpu_mem_used']:.2f}",
                        f"{gpu_stats['gpu_mem_total']:.2f}",
                        -1,
                    ]
                )
                log.error(f"[ERROR] request failed: {e}")

            # 控制 FPS
            loop_end = time.perf_counter()
            dt = loop_end - loop_start
            sleep_time = interval - dt
            if sleep_time > 0:
                time.sleep(sleep_time)

        # 汇总
        summary: Dict[str, Any] = {
            "api_url": API_URL,
            "duration_sec": DURATION_SEC,
            "target_fps": TARGET_FPS,
            "total_requests": n_total,
            "ok_requests": n_ok,
            "error_requests": n_total - n_ok,
        }

        if latencies:
            lat_sorted = sorted(latencies)
            n = len(lat_sorted)

            def pct(p: float) -> float:
                if n == 0:
                    return -1.0
                k = min(n - 1, int(n * p) - 1)
                return lat_sorted[k]

            summary.update(
                {
                    "latency_avg_ms": sum(latencies) / n,
                    "latency_p50_ms": pct(0.50),
                    "latency_p90_ms": pct(0.90),
                    "latency_p95_ms": pct(0.95),
                    "latency_p99_ms": pct(0.99),
                    "latency_min_ms": min(latencies),
                    "latency_max_ms": max(latencies),
                }
            )
        else:
            summary.update(
                {
                    "latency_avg_ms": -1.0,
                    "latency_p50_ms": -1.0,
                    "latency_p90_ms": -1.0,
                    "latency_p95_ms": -1.0,
                    "latency_p99_ms": -1.0,
                    "latency_min_ms": -1.0,
                    "latency_max_ms": -1.0,
                }
            )

    with open(JSON_PATH, "w", encoding="utf-8") as f_json:
        json.dump(summary, f_json, ensure_ascii=False, indent=2)

    log.info("===========================================")
    log.info(" 压测完成")
    log.info("json.dumps(summary, ensure_ascii=False, indent=2)")
    log.info(" CSV:", CSV_PATH")
    log.info(" JSON:", JSON_PATH")
    log.info("===========================================")


if __name__ == "__main__":
    main()

