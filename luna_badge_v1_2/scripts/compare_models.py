from core.logging import get_logger

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
log = get_logger("compare_models")
"""
模型对比脚本

功能：
- 对比多个运行日志的性能
- 生成模型对比报告
"""

import json
import sys
import statistics
from pathlib import Path
from typing import Dict, Any, List


def percentile(values: List[float], p: float) -> float:
    """计算百分位数"""
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    k = (len(sorted_vals) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(sorted_vals) - 1)
    if f == c:
        return sorted_vals[int(k)]
    d0 = sorted_vals[f] * (c - k)
    d1 = sorted_vals[c] * (k - f)
    return d0 + d1


def load(path: Path) -> Dict[str, Any]:
    """加载日志文件并计算统计值"""
    frames = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
                if rec.get("type") == "frame":
                    frames.append(rec)
            except json.JSONDecodeError:
                continue
    
    if not frames:
        return None
    
    lat = [f.get("end_to_end_ms", 0) for f in frames if "end_to_end_ms" in f]
    infer = [f.get("server", {}).get("inference_ms", 0) for f in frames 
             if "server" in f and "inference_ms" in f.get("server", {})]
    
    if not lat:
        return None
    
    return {
        "name": path.stem.replace("run_", ""),
        "count": len(frames),
        "lat_avg": statistics.mean(lat),
        "lat_p50": statistics.median(lat),
        "lat_p90": percentile(lat, 90),
        "lat_p95": percentile(lat, 95),
        "lat_p99": percentile(lat, 99),
        "lat_min": min(lat),
        "lat_max": max(lat),
        "infer_avg": statistics.mean(infer) if infer else 0.0,
        "infer_p95": percentile(infer, 95) if infer else 0.0,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        log.info("用法: python3 compare_models.py <jsonl_file1> [jsonl_file2] ...")
        sys.exit(1)
    
    paths = [Path(p) for p in sys.argv[1:]]
    rows = []
    
    for path in paths:
        if not path.exists():
            log.warning(f"[WARN] 文件不存在，跳过: {path}")
            continue
        result = load(path)
        if result:
            rows.append(result)
    
    if not rows:
        log.error("[ERROR] 没有有效的日志文件")
        sys.exit(1)
    
    log.info("=" * 100")
    log.info("模型对比结果")
    log.info("=" * 100")
    log.info("")
    log.info(f"{'Run ID':<30} {'Frames':>8} {'Lat Avg':>10} {'Lat P95':>10} {'Lat P99':>10} {'Inf Avg':>10} {'Inf P95':>10}")
    log.info("-" * 100")
    
    for r in rows:
        print(f"{r['name']:<30} {r['count']:>8} {r['lat_avg']:>10.1f} {r['lat_p95']:>10.1f} "
              f"{r['lat_p99']:>10.1f} {r['infer_avg']:>10.1f} {r['infer_p95']:>10.1f}")
    
    log.info("")
    log.info("=" * 100")
    
    # 找出最佳模型
    if len(rows) > 1:
        best_lat = min(rows, key=lambda x: x['lat_avg'])
        best_infer = min(rows, key=lambda x: x['infer_avg'])
        log.info(f"\n🏆 最佳端到端延迟: {best_lat['name']} ({best_lat['lat_avg']:.1f}ms)")
        log.info(f"🏆 最佳推理速度: {best_infer['name']} ({best_infer['infer_avg']:.1f}ms)")
        log.info("")

















