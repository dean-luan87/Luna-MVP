#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v0.5 Patch F: Runtime Fingerprint Generator

跨视频可对齐、可量化、可审判的稳定性 Fingerprint。

目标：证明"同一个系统，在不同视频中，性格一致"。
"""

import json
import sys
import argparse
from pathlib import Path
from collections import Counter
from typing import Dict, Any, List


def clamp(value: float, min_val: float, max_val: float) -> float:
    """将值限制在 [min_val, max_val] 范围内"""
    return max(min_val, min(value, max_val))


def calculate_stability_score(
    gate_switch_rate: float,
    decision_density: float,
    read_only_ratio: float
) -> float:
    """
    v0.5 冻结公式：计算稳定性评分
    
    stability_score = 1
      - clamp(gate_switch_rate / 5.0, 0, 0.4)
      - clamp(decision_density / 10.0, 0, 0.4)
      - clamp(read_only_ratio, 0, 0.2)
    
    解释：
    - 频繁切 Gate → 不稳定
    - 决策太多 → 冲动
    - 长期 READ_ONLY → 感知不足
    """
    penalty1 = clamp(gate_switch_rate / 5.0, 0, 0.4)
    penalty2 = clamp(decision_density / 10.0, 0, 0.4)
    penalty3 = clamp(read_only_ratio, 0, 0.2)
    
    score = 1.0 - penalty1 - penalty2 - penalty3
    return round(max(0.0, score), 4)


def generate_fingerprint(trace_path: str, video_id: str = None, duration_sec: float = None) -> Dict[str, Any]:
    """
    生成 Runtime Fingerprint
    
    :param trace_path: Trace 文件路径（JSONL）
    :param video_id: 视频 ID（可选）
    :param duration_sec: 视频时长（秒，可选）
    :return: Fingerprint 字典
    """
    gate_states = []
    c_states = []
    tick_count = 0
    no_op_count = 0
    
    # 假设 30fps
    FPS = 30.0
    
    with open(trace_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            try:
                e = json.loads(line)
                t = e.get("event_type")
                
                if t == "GATE_RUNTIME_PROFILE":
                    gate_info = e.get("gate_runtime_profile") or e.get("gate", {})
                    mode = gate_info.get("gate_mode") or gate_info.get("mode")
                    if mode:
                        gate_states.append(mode)
                
                elif t == "C_RUNTIME_PROFILE":
                    c_info = e.get("c_runtime_profile") or e.get("c", {})
                    mode = c_info.get("mode")
                    if mode:
                        c_states.append(mode)
                
                elif t == "tick":
                    tick_count += 1
                    impact = e.get("impact") or e.get("impact_evaluation", {}).get("impact")
                    if impact == "NO_OP":
                        no_op_count += 1
            except json.JSONDecodeError:
                continue
    
    total_frames = len(gate_states)
    if total_frames == 0:
        return {
            "engine": "B",
            "engine_version": "v0.5",
            "video_id": video_id or "unknown",
            "duration_sec": duration_sec or 0.0,
            "error": "No gate states found in trace"
        }
    
    # Gate 状态分布
    gate_dist = Counter(gate_states)
    
    def ratio(x: int) -> float:
        return round(x / total_frames, 4)
    
    gate_distribution = {
        k: ratio(v) for k, v in gate_dist.items()
    }
    
    # 计算状态切换次数
    gate_switches = sum(
        1 for i in range(1, total_frames)
        if gate_states[i] != gate_states[i - 1]
    )
    
    c_switches = sum(
        1 for i in range(1, len(c_states))
        if c_states[i] != c_states[i - 1]
    ) if len(c_states) > 1 else 0
    
    # 计算每分钟切换率
    duration_minutes = (total_frames / FPS / 60.0) if total_frames > 0 else 1.0
    if duration_sec:
        duration_minutes = duration_sec / 60.0
    
    gate_switches_per_min = round(gate_switches / duration_minutes, 3) if duration_minutes > 0 else 0.0
    c_switches_per_min = round(c_switches / duration_minutes, 3) if duration_minutes > 0 else 0.0
    
    # 决策密度
    ticks_per_min = round(tick_count / duration_minutes, 3) if duration_minutes > 0 else 0.0
    no_op_ratio = round(no_op_count / tick_count, 4) if tick_count > 0 else 1.0
    
    # 计算稳定性评分
    read_only_ratio = gate_distribution.get("READ_ONLY", 0.0)
    stability_score = calculate_stability_score(
        gate_switch_rate=gate_switches_per_min,
        decision_density=ticks_per_min,
        read_only_ratio=read_only_ratio
    )
    
    fingerprint = {
        "engine": "B",
        "engine_version": "v0.5",
        "video_id": video_id or Path(trace_path).stem,
        "duration_sec": round(duration_sec or (total_frames / FPS), 1),
        "total_frames": total_frames,
        "gate_distribution": gate_distribution,
        "state_switch_rate": {
            "gate_switches_per_min": gate_switches_per_min,
            "c_switches_per_min": c_switches_per_min
        },
        "decision_density": {
            "ticks_per_min": ticks_per_min,
            "no_op_ratio": no_op_ratio
        },
        "stability_score": stability_score
    }
    
    return fingerprint


def main():
    parser = argparse.ArgumentParser(description="v0.5 Patch F: Runtime Fingerprint Generator")
    parser.add_argument("trace", help="Trace 文件路径（JSONL）")
    parser.add_argument("--video-id", help="视频 ID（可选）")
    parser.add_argument("--duration", type=float, help="视频时长（秒，可选）")
    parser.add_argument("--output", help="输出文件路径（JSON，可选）")
    
    args = parser.parse_args()
    
    if not Path(args.trace).exists():
        print(f"错误: trace 文件不存在: {args.trace}", file=sys.stderr)
        sys.exit(1)
    
    fingerprint = generate_fingerprint(
        trace_path=args.trace,
        video_id=args.video_id,
        duration_sec=args.duration
    )
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(fingerprint, f, indent=2, ensure_ascii=False)
        print(f"Fingerprint 已保存到: {args.output}")
    else:
        print(json.dumps(fingerprint, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
