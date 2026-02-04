from core.logging import get_logger

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
log = get_logger("heat_decay_test")
"""
热衰减测试工具

功能：
- 连续运行指定时长的压测
- 每隔 N 秒记录 CPU/内存/GPU 使用率
- 叠加实时性能延迟数据（从 JSONL 读取）
- 输出 JSON 报告 + CSV + JSONL
"""

import argparse
import time
import json
import subprocess
import shutil
from datetime import datetime
from pathlib import Path
from statistics import mean

try:
    import psutil
except ImportError:
    log.error("[ERROR] 需要安装 psutil: pip install psutil")
    exit(1)

LOG_DIR = Path("perf_logs")
LOG_DIR.mkdir(exist_ok=True)


def run_stress_command(cmd: str):
    """
    启动一个持续压测命令，例如：
    python tools/stress_runner.py --duration 600 --fps 10 --ws on
    """
    log.info(f"[heat] 启动压测命令: {cmd}")
    proc = subprocess.Popen(cmd, shell=True)
    return proc


def read_gpu_stats():
    """
    优先读取 nvidia-smi，如果不存在则返回 None。
    """
    if not shutil.which("nvidia-smi"):
        return None
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=utilization.gpu,temperature.gpu", "--format=csv,noheader,nounits"],
            stderr=subprocess.DEVNULL,
        ).decode("utf-8").strip()
        # 只读第一个 GPU
        line = out.splitlines()[0]
        util_str, temp_str = [x.strip() for x in line.split(",")]
        return {
            "gpu_util": float(util_str),
            "gpu_temp": float(temp_str),
        }
    except Exception:
        return None


def collect_system_metrics():
    """收集系统指标"""
    cpu = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory()
    gpu_info = read_gpu_stats()
    m = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "cpu_percent": cpu,
        "mem_percent": mem.percent,
        "mem_used_mb": mem.used / (1024 * 1024),
        "mem_total_mb": mem.total / (1024 * 1024),
    }
    if gpu_info:
        m.update(gpu_info)
    return m


def parse_latest_latency(latest_jsonl: Path):
    """
    简单从 run_*.jsonl 中解析最近窗口的平均延迟（端到端 / infer / nav）
    按你之前 JSONL 格式调整 key 名称。
    """
    if not latest_jsonl.exists():
        return {}

    lat_total = []
    lat_infer = []
    lat_nav = []

    with latest_jsonl.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            # 假设写入格式中有这些字段（可按你的实际情况改名）
            if obj.get("type") == "frame":
                if "end_to_end_ms" in obj:
                    lat_total.append(obj["end_to_end_ms"])
                server = obj.get("server", {})
                if "inference_ms" in server:
                    lat_infer.append(server["inference_ms"])
                if "nav_ms" in obj:
                    lat_nav.append(obj["nav_ms"])

    metrics = {}
    if lat_total:
        metrics["lat_total_avg"] = float(f"{mean(lat_total):.2f}")
    if lat_infer:
        metrics["lat_infer_avg"] = float(f"{mean(lat_infer):.2f}")
    if lat_nav:
        metrics["lat_nav_avg"] = float(f"{mean(lat_nav):.2f}")
    return metrics


def main():
    parser = argparse.ArgumentParser(description="Luna Badge 热衰减测试 (10 分钟 CPU/GPU 监控)")
    parser.add_argument("--duration", type=int, default=600, help="测试时长（秒），默认 600 秒（10 分钟）")
    parser.add_argument("--interval", type=int, default=10, help="采样间隔（秒），默认 10 秒")
    parser.add_argument("--stress-cmd", type=str,
                        default="python3 realtime_server.py --host 0.0.0.0 --port 8899 --model yolo11n.pt",
                        help="压测命令，默认启动服务器")
    parser.add_argument("--jsonl", type=str, default=None,
                        help="实时性能 JSONL（run_*.jsonl），用于叠加平均延迟信息")
    args = parser.parse_args()

    run_id = datetime.now().strftime("heat_%Y%m%d_%H%M%S")
    out_json = LOG_DIR / f"{run_id}.json"
    out_jsonl = LOG_DIR / f"{run_id}.jsonl"
    out_csv = LOG_DIR / f"{run_id}.csv"

    log.info(f"[heat] 运行 ID: {run_id}")
    log.info(f"[heat] 总时长: {args.duration} 秒，采样间隔: {args.interval} 秒")
    log.info(f"[heat] 输出: {out_json}, {out_jsonl}, {out_csv}")

    # 启动压测进程
    stress_proc = None
    if args.stress_cmd:
        stress_proc = run_stress_command(args.stress_cmd)
        log.info(f"[heat] 压测进程 PID: {stress_proc.pid}")
        time.sleep(3)  # 等待进程启动

    start = time.time()
    end = start + args.duration
    samples = []

    try:
        while time.time() < end:
            metrics = collect_system_metrics()
            if args.jsonl:
                latest_lat = parse_latest_latency(Path(args.jsonl))
                metrics.update(latest_lat)

            samples.append(metrics)
            # 写 JSONL 方便后续分析
            with out_jsonl.open("a", encoding="utf-8") as f:
                f.write(json.dumps(metrics, ensure_ascii=False) + "\n")

            gpu_info = ""
            if "gpu_util" in metrics:
                gpu_info = f" GPU={metrics['gpu_util']:.1f}% T={metrics.get('gpu_temp', '-')}°C"
            
            print(f"[heat] {metrics['timestamp']} CPU={metrics['cpu_percent']:.1f}% "
                  f"MEM={metrics['mem_percent']:.1f}%{gpu_info}")

            time.sleep(args.interval)

    except KeyboardInterrupt:
        log.info("\n[heat] 用户中断测试")
    finally:
        # 停压测
        if stress_proc and stress_proc.poll() is None:
            log.info("[heat] 结束压测进程")
            stress_proc.terminate()
            try:
                stress_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                stress_proc.kill()

    # 汇总统计
    if not samples:
        log.info("[heat] 无采样数据，结束。")
        return

    cpu_list = [s["cpu_percent"] for s in samples]
    mem_list = [s["mem_percent"] for s in samples]
    gpu_list = [s.get("gpu_util") for s in samples if "gpu_util" in s]
    gpu_t_list = [s.get("gpu_temp") for s in samples if "gpu_temp" in s]

    summary = {
        "run_id": run_id,
        "duration_sec": args.duration,
        "interval_sec": args.interval,
        "stress_cmd": args.stress_cmd,
        "cpu_avg": float(f"{mean(cpu_list):.2f}"),
        "cpu_max": max(cpu_list),
        "cpu_min": min(cpu_list),
        "mem_avg": float(f"{mean(mem_list):.2f}"),
        "mem_max": max(mem_list),
        "mem_min": min(mem_list),
        "sample_count": len(samples),
    }
    if gpu_list:
        summary["gpu_util_avg"] = float(f"{mean(gpu_list):.2f}")
        summary["gpu_util_max"] = max(gpu_list)
        summary["gpu_util_min"] = min(gpu_list)
    if gpu_t_list:
        summary["gpu_temp_avg"] = float(f"{mean(gpu_t_list):.2f}")
        summary["gpu_temp_max"] = max(gpu_t_list)
        summary["gpu_temp_min"] = min(gpu_t_list)

    # 如果有延迟叠加，也写入 summary（最后一次解析的结果）
    if args.jsonl:
        latest_lat = parse_latest_latency(Path(args.jsonl))
        summary.update(latest_lat)

    # 写 JSON 总结
    with out_json.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    # 写 CSV
    with out_csv.open("w", encoding="utf-8") as f:
        # header
        if samples:
            keys = sorted(samples[0].keys())
            f.write(",".join(keys) + "\n")
            for s in samples:
                row = []
                for k in keys:
                    row.append(str(s.get(k, "")))
                f.write(",".join(row) + "\n")

    log.info("")
    log.info("[heat] 热衰减测试完成。Summary:")
    log.info("json.dumps(summary, ensure_ascii=False, indent=2)")
    log.info("")
    log.info(f"[heat] 输出文件:")
    log.info(f"  - JSON: {out_json}")
    log.info(f"  - JSONL: {out_jsonl}")
    log.info(f"  - CSV: {out_csv}")


if __name__ == "__main__":
    main()

















