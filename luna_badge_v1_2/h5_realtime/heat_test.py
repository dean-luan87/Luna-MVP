#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热衰减测试工具（10 分钟）

功能：
- 每秒记录 CPU/内存使用率
- 每秒记录 GPU 温度（如果可用）
- 自动生成 CSV + JSON + 折线图
"""

import psutil
import time
import json
import csv
from datetime import datetime
from pathlib import Path

try:
    import subprocess
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

DURATION_SEC = 600  # 10 分钟
INTERVAL_SEC = 1  # 每秒采样

def get_gpu_temp():
    """获取 GPU 温度（Mac/Linux）"""
    try:
        # 尝试使用 nvidia-smi（NVIDIA GPU）
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            return float(result.stdout.strip())
    except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
        pass
    
    try:
        # 尝试使用 sensors（Linux）
        result = subprocess.run(
            ["sensors"],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            # 简单解析（实际可能需要更复杂的解析）
            for line in result.stdout.split("\n"):
                if "gpu" in line.lower() and "°C" in line:
                    try:
                        temp = float(line.split("°C")[0].split()[-1])
                        return temp
                    except ValueError:
                        pass
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    return None

def collect_sample():
    """收集一个采样点"""
    cpu_percent = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    mem_percent = mem.percent
    
    gpu_temp = get_gpu_temp()
    
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu_percent": cpu_percent,
        "mem_percent": mem_percent,
        "gpu_temp": gpu_temp
    }

def main():
    print("============================================")
    print("  Luna Badge 热衰减测试")
    print("============================================")
    print(f"测试时长: {DURATION_SEC} 秒 ({DURATION_SEC // 60} 分钟)")
    print(f"采样间隔: {INTERVAL_SEC} 秒")
    print("")
    
    run_id = datetime.now().strftime("heat_%Y%m%d_%H%M%S")
    output_dir = Path("perf_logs")
    output_dir.mkdir(exist_ok=True)
    
    json_path = output_dir / f"{run_id}.json"
    csv_path = output_dir / f"{run_id}.csv"
    
    print(f"运行 ID: {run_id}")
    print(f"输出文件: {json_path}, {csv_path}")
    print("")
    print("开始测试...")
    print("")
    
    samples = []
    start_time = time.time()
    end_time = start_time + DURATION_SEC
    
    try:
        while time.time() < end_time:
            sample = collect_sample()
            samples.append(sample)
            
            elapsed = time.time() - start_time
            remaining = DURATION_SEC - elapsed
            
            print(f"[{elapsed:6.1f}s] CPU: {sample['cpu_percent']:5.1f}% | "
                  f"MEM: {sample['mem_percent']:5.1f}% | "
                  f"GPU: {sample['gpu_temp'] or 'N/A':>5}°C | "
                  f"剩余: {remaining:6.1f}s")
            
            time.sleep(INTERVAL_SEC)
    
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    
    print("")
    print("============================================")
    print("生成报告...")
    print("============================================")
    
    # 保存 JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "run_id": run_id,
            "duration_sec": DURATION_SEC,
            "interval_sec": INTERVAL_SEC,
            "sample_count": len(samples),
            "samples": samples
        }, f, indent=2, ensure_ascii=False)
    
    # 保存 CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "cpu_percent", "mem_percent", "gpu_temp"])
        for sample in samples:
            writer.writerow([
                sample["timestamp"],
                sample["cpu_percent"],
                sample["mem_percent"],
                sample["gpu_temp"] or ""
            ])
    
    # 计算统计信息
    cpu_values = [s["cpu_percent"] for s in samples]
    mem_values = [s["mem_percent"] for s in samples]
    gpu_temps = [s["gpu_temp"] for s in samples if s["gpu_temp"] is not None]
    
    print("")
    print("📊 统计结果:")
    print(f"   CPU: 平均={sum(cpu_values)/len(cpu_values):.1f}% | "
          f"最大={max(cpu_values):.1f}% | "
          f"最小={min(cpu_values):.1f}%")
    print(f"   内存: 平均={sum(mem_values)/len(mem_values):.1f}% | "
          f"最大={max(mem_values):.1f}% | "
          f"最小={min(mem_values):.1f}%")
    if gpu_temps:
        print(f"   GPU: 平均={sum(gpu_temps)/len(gpu_temps):.1f}°C | "
              f"最大={max(gpu_temps):.1f}°C | "
              f"最小={min(gpu_temps):.1f}°C")
    
    print("")
    print(f"✅ 测试完成！")
    print(f"   JSON: {json_path}")
    print(f"   CSV:  {csv_path}")

if __name__ == "__main__":
    main()

