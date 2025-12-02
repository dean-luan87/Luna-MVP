#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
读取 perf_logs 最新采样，输出瓶颈分析：

- det/nav/overhead 平均耗时和占比
- total_ms 分布情况
- 自动识别主瓶颈模块并给出优化建议
"""

import os
import csv
import json
from pathlib import Path

PERF_DIR = Path("perf_logs")


def latest_pair():
    """找到最新的一组 *_samples.csv + *_report.json"""
    csv_files = sorted(PERF_DIR.glob("*_samples.csv"))
    if not csv_files:
        raise RuntimeError("perf_logs 下没有 *_samples.csv，可先跑 demo_realtime_navigation.py")
    csv_path = csv_files[-1]
    base = csv_path.stem.replace("_samples", "")
    json_path = PERF_DIR / f"{base}_report.json"
    if not json_path.exists():
        raise RuntimeError(f"未找到对应报告文件: {json_path}")
    return csv_path, json_path, base


def main():
    os.makedirs(PERF_DIR, exist_ok=True)
    csv_path, json_path, base = latest_pair()

    print(f"[INFO] 读取采样文件: {csv_path.name}")
    print(f"[INFO] 读取报告文件: {json_path.name}")
    print()

    dets, navs, totals = [], [], []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dets.append(float(row["det_ms"]))
            navs.append(float(row["nav_ms"]))
            totals.append(float(row["total_ms"]))

    if not totals:
        raise RuntimeError("采样为空")

    avg_det = sum(dets) / len(dets)
    avg_nav = sum(navs) / len(navs)
    avg_total = sum(totals) / len(totals)
    avg_overhead = max(avg_total - avg_det - avg_nav, 0.0)

    def pct(part):
        return (part / avg_total * 100.0) if avg_total > 0 else 0.0

    report = {
        "base": base,
        "avg_total_ms": round(avg_total, 2),
        "avg_det_ms": round(avg_det, 2),
        "avg_nav_ms": round(avg_nav, 2),
        "avg_overhead_ms": round(avg_overhead, 2),
        "share": {
            "det_pct": round(pct(avg_det), 1),
            "nav_pct": round(pct(avg_nav), 1),
            "overhead_pct": round(pct(avg_overhead), 1),
        },
    }

    # 控制台输出
    print("=" * 70)
    print("Luna Badge 瓶颈分析")
    print("=" * 70)
    print(f"样本文件: {csv_path.name}")
    print(f"场景标记: {base}")
    print()
    print(f"平均总延迟: {avg_total:.2f} ms (100%)")
    print(f"  - 检测 det: {avg_det:.2f} ms ({pct(avg_det):.1f}%)")
    print(f"  - 导航 nav: {avg_nav:.2f} ms ({pct(avg_nav):.1f}%)")
    print(f"  - 其他 overhead: {avg_overhead:.2f} ms ({pct(avg_overhead):.1f}%)")
    print()

    # 判断瓶颈
    parts = [("det", avg_det), ("nav", avg_nav), ("overhead", avg_overhead)]
    parts.sort(key=lambda x: x[1], reverse=True)
    top_name, top_val = parts[0]
    second_name, second_val = parts[1] if len(parts) > 1 else (None, 0)

    print(f"当前主瓶颈模块: {top_name} ({top_val:.2f} ms, {pct(top_val):.1f}%)")
    if second_name and second_val > 0:
        print(f"次要瓶颈模块: {second_name} ({second_val:.2f} ms, {pct(second_val):.1f}%)")
    print()

    # 优化建议
    print("优化建议:")
    if top_name == "det":
        print("  ✅ 优先优化检测模型：")
        print("     - 使用更小的模型（如 yolo11-tiny）")
        print("     - 模型量化（INT8）")
        print("     - 降低输入分辨率")
        print("     - 模型剪枝")
    elif top_name == "nav":
        print("  ✅ 优先优化导航算法：")
        print("     - 检查导航算法复杂度")
        print("     - 减少不必要的重复计算")
        print("     - 优化路径规划算法")
        print("     - 缓存中间结果")
    else:
        print("  ✅ 优先优化系统开销：")
        print("     - 检查图像预处理开销")
        print("     - 减少数据拷贝操作")
        print("     - 优化日志输出频率")
        print("     - 检查其他系统调用开销")

    # 写文件
    out_path = PERF_DIR / f"{base}_bottleneck_report.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print()
    print("=" * 70)
    print(f"[INFO] 瓶颈报告已保存：{out_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()


