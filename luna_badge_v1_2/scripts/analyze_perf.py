#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能分析脚本

功能：
- 读取 JSONL 日志文件
- 生成统计报告
- 输出 CSV 文件供 Dashboard 使用
- 自动瓶颈分析
"""

import json
import sys
import statistics
import csv
from pathlib import Path
from typing import List, Dict, Any

# 导入协议验证库
try:
    from protocol.perflogspec import PerfLogSpec
    PROTOCOL_AVAILABLE = True
except ImportError:
    PROTOCOL_AVAILABLE = False
    print("[WARN] 协议库未找到，跳过规范验证")


def load_frames(path: Path) -> List[Dict[str, Any]]:
    """从 JSONL 文件加载所有 frame 记录（使用协议验证）"""
    frames = []
    invalid_count = 0
    
    with path.open(encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
                
                # 使用协议库验证
                if PROTOCOL_AVAILABLE:
                    is_valid, error = PerfLogSpec.validate(rec)
                    if not is_valid:
                        print(f"[WARN] 第 {line_num} 行不符合 PerfLogSpec: {error}")
                        invalid_count += 1
                        continue
                
                # 只处理 infer_result 事件
                if rec.get("event") == "infer_result":
                    frames.append(rec)
            except json.JSONDecodeError as e:
                print(f"[WARN] 第 {line_num} 行 JSON 解析失败: {e}")
                invalid_count += 1
                continue
    
    if invalid_count > 0:
        print(f"[INFO] 跳过 {invalid_count} 条无效记录")
    
    return frames


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


def summarize(frames: List[Dict[str, Any]], path: Path):
    """生成统计报告"""
    if not frames:
        print(f"[ERROR] 未找到 frame 记录")
        return
    
    # 确保输出可以被脚本捕获
    import sys
    sys.stdout.flush()
    
    # 端到端延迟
    lat = [f.get("end_to_end_ms", 0) for f in frames if "end_to_end_ms" in f]
    
    if not lat:
        print(f"[ERROR] 未找到端到端延迟数据")
        return
    
    print("=" * 70)
    print("Luna Badge 性能分析报告")
    print("=" * 70)
    print(f"日志文件: {path.name}")
    print(f"总帧数: {len(frames)}")
    print()
    
    # 端到端延迟统计
    print("端到端延迟统计:")
    print(f"  平均: {statistics.mean(lat):.1f}ms")
    print(f"  中位数 (P50): {statistics.median(lat):.1f}ms")
    print(f"  P90: {percentile(lat, 90):.1f}ms")
    print(f"  P95: {percentile(lat, 95):.1f}ms")
    print(f"  P99: {percentile(lat, 99):.1f}ms")
    print(f"  最小: {min(lat):.1f}ms")
    print(f"  最大: {max(lat):.1f}ms")
    print()
    
    # 分段统计
    segs = {}
    total_avg = statistics.mean(lat)
    
    # 客户端阶段
    if any("client" in f for f in frames):
        segs["client_capture"] = [f.get("client", {}).get("capture_ms", 0) for f in frames]
        segs["client_encode"] = [f.get("client", {}).get("encode_ms", 0) for f in frames]
        segs["client_pack"] = [f.get("client", {}).get("pack_ms", 0) for f in frames]
    
    # 网络阶段
    if any("network" in f for f in frames):
        segs["net_upload"] = [f.get("network", {}).get("upload_ms", 0) for f in frames]
        segs["net_download"] = [f.get("network", {}).get("download_ms", 0) for f in frames]
        segs["net_rtt"] = [f.get("network", {}).get("rtt_ms", 0) for f in frames]
    
    # 服务端阶段
    if any("server" in f for f in frames):
        segs["server_decode"] = [f.get("server", {}).get("decode_ms", 0) for f in frames]
        segs["server_preprocess"] = [f.get("server", {}).get("preprocess_ms", 0) for f in frames]
        segs["server_infer"] = [f.get("server", {}).get("inference_ms", 0) for f in frames]
        segs["server_postprocess"] = [f.get("server", {}).get("postprocess_ms", 0) for f in frames]
        segs["server_pack"] = [f.get("server", {}).get("pack_ms", 0) for f in frames]
    
    # 显示分段占比
    print("分段耗时统计:")
    seg_list = []
    for name, vals in segs.items():
        if vals and any(v > 0 for v in vals):
            avg = statistics.mean(vals)
            pct = (avg / total_avg * 100) if total_avg > 0 else 0
            seg_list.append((name, avg, pct))
    
    # 按平均耗时排序
    seg_list.sort(key=lambda x: x[1], reverse=True)
    
    for name, avg, pct in seg_list:
        print(f"  {name:20} {avg:6.1f}ms  ({pct:5.1f}%)")
    print()
    
    # 瓶颈分析
    if seg_list:
        print("⚠️  瓶颈分析（按平均耗时排序）:")
        for i, (name, avg, pct) in enumerate(seg_list[:3], 1):
            print(f"  {i}. {name:20} {avg:6.1f}ms  ({pct:5.1f}%)")
        print(f"\n建议优先优化: {seg_list[0][0]}")
        print()
    
    # 输出 CSV
    csv_path = path.with_suffix(".csv")
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        
        # 构建表头
        headers = ["frame_id", "seq", "end_to_end_ms"]
        if any("client" in fr for fr in frames):
            headers.extend(["client_capture_ms", "client_encode_ms", "client_pack_ms"])
        if any("network" in fr for fr in frames):
            headers.extend(["net_upload_ms", "net_download_ms", "net_rtt_ms"])
        if any("server" in fr for fr in frames):
            headers.extend(["server_decode_ms", "server_preprocess_ms", 
                          "server_infer_ms", "server_postprocess_ms", "server_pack_ms"])
        headers.extend(["det_count", "image_bytes"])
        
        w.writerow(headers)
        
        # 写入数据
        for fz in frames:
            row = [
                fz.get("frame_id", ""),
                fz.get("seq", 0),
                fz.get("end_to_end_ms", 0),
            ]
            
            client = fz.get("client", {})
            if client:
                row.extend([
                    client.get("capture_ms", 0),
                    client.get("encode_ms", 0),
                    client.get("pack_ms", 0),
                ])
            
            network = fz.get("network", {})
            if network:
                row.extend([
                    network.get("upload_ms", 0),
                    network.get("download_ms", 0),
                    network.get("rtt_ms", 0),
                ])
            
            server = fz.get("server", {})
            if server:
                row.extend([
                    server.get("decode_ms", 0),
                    server.get("preprocess_ms", 0),
                    server.get("inference_ms", 0),
                    server.get("postprocess_ms", 0),
                    server.get("pack_ms", 0),
                ])
            
            row.extend([
                fz.get("det_count", len(fz.get("detections", []))),
                fz.get("image_bytes", 0),
            ])
            
            w.writerow(row)
    
    print(f"✅ CSV 输出: {csv_path}")
    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 analyze_perf.py <jsonl_file>")
        sys.exit(1)
    
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"[ERROR] 文件不存在: {path}")
        sys.exit(1)
    
    frames = load_frames(path)
    summarize(frames, path)

