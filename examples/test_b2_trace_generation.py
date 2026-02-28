#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B2 Runtime Trace 生成测试脚本
目标：生成 10-20 秒的真实 trace，用于"人类视角 vs B 的认知复盘"

三条铁律验证：
1. 任何一次行为判断，必须可视
2. 任何一次判断，必须可追溯到"哪一秒、哪一帧、哪条规则"
3. 任何一次"不作为"，也必须有理由
"""

import sys
import os
import time
import json
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 直接导入，避免触发其他模块的导入
import importlib.util
spec = importlib.util.spec_from_file_location(
    "b2_v03",
    project_root / "vision_pipeline" / "b2" / "v03" / "b2_v03.py"
)
b2_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b2_module)
B2v03 = b2_module.B2v03


def generate_simulated_perception(ts: float, scenario: str = "normal") -> dict:
    """
    生成模拟的 perception 数据
    
    scenario 选项：
    - "normal": 正常行走
    - "path_change": 路面变化（触发 PATH factor）
    - "event": 突发事件（触发 EVENT factor）
    - "people": 人群密集（触发 PEOPLE factor）
    - "no_evidence": 无证据
    """
    base_perception = {
        "timestamp": ts,
        "objects": [],
        "path": {},
        "scene": "outdoor",
        "structure": "open"
    }
    
    if scenario == "normal":
        # 正常情况，可能有轻微的 ENV 信息
        base_perception["path"] = {
            "surface": "smooth",
            "obstacle": False
        }
        base_perception["scene"] = "outdoor"
        
    elif scenario == "path_change":
        # 路面变化：从平滑到粗糙
        if int(ts) % 3 == 0:  # 每 3 秒变化一次
            base_perception["path"] = {
                "surface": "rough",
                "texture_change": True,
                "obstacle": False
            }
        else:
            base_perception["path"] = {
                "surface": "smooth",
                "texture_change": False,
                "obstacle": False
            }
            
    elif scenario == "event":
        # 突发事件：障碍物出现
        if 5.0 <= ts <= 7.0:  # 5-7 秒之间有事件
            base_perception["path"] = {
                "surface": "smooth",
                "obstacle": True,
                "obstacle_type": "blocking"
            }
            base_perception["objects"] = [
                {"type": "obstacle", "confidence": 0.9, "distance": 2.0}
            ]
        else:
            base_perception["path"] = {
                "surface": "smooth",
                "obstacle": False
            }
            
    elif scenario == "people":
        # 人群密集
        if 3.0 <= ts <= 8.0:  # 3-8 秒之间人群密集
            base_perception["people"] = {
                "count": 5,
                "density": "high",
                "distance": 3.0
            }
        else:
            base_perception["people"] = {
                "count": 0,
                "density": "low",
                "distance": 10.0
            }
            
    elif scenario == "no_evidence":
        # 无证据情况
        base_perception["path"] = {}
        base_perception["objects"] = []
        
    return base_perception


def run_trace_test(duration_seconds: int = 15, scenario: str = "path_change", fps: float = 30.0):
    """
    运行 trace 生成测试
    
    :param duration_seconds: 测试时长（秒）
    :param scenario: 测试场景
    :param fps: 帧率
    """
    print(f"\n{'='*70}")
    print(f"B2 Runtime Trace 生成测试")
    print(f"{'='*70}")
    print(f"场景: {scenario}")
    print(f"时长: {duration_seconds} 秒")
    print(f"帧率: {fps} fps")
    print(f"{'='*70}\n")
    
    # 清理旧的 trace 文件
    trace_file = "traces/b2_runtime_trace_v04.jsonl"
    if os.path.exists(trace_file):
        os.remove(trace_file)
        print(f"已清理旧 trace 文件: {trace_file}")
    
    # 初始化 B2
    base_ts = time.time()
    b2 = B2v03(
        future_window_start=1.0,
        future_window_end=8.0,
        debug=False,
        log_mode="video",
        log_base_ts=base_ts,
        enable_trace=True,
        trace_file=trace_file,
        fps=fps
    )
    
    # 模拟运行
    frame_interval = 1.0 / fps
    current_ts = 0.0
    frame_id = 0
    
    print(f"开始生成 trace...")
    print(f"时间范围: 0.0s - {duration_seconds}s\n")
    
    while current_ts < duration_seconds:
        # 生成 perception
        perception = generate_simulated_perception(current_ts, scenario)
        
        # 调用 tick
        result = b2.tick(
            frame_ts=base_ts + current_ts,
            perception=perception,
            frame_id=frame_id
        )
        
        # 打印关键信息
        if result:
            impact = result.get("impact", "NO_OP")
            main_factor = result.get("main_factor", "unknown")
            print(f"[{current_ts:6.2f}s] Impact: {impact:15s} | Factor: {main_factor:10s} | Confidence: {result.get('confidence', 0.0):.2f}")
        
        # 更新时间和帧 ID
        current_ts += frame_interval
        frame_id += 1
        
        # 控制输出频率（每 0.5 秒输出一次）
        if int(current_ts * 2) != int((current_ts - frame_interval) * 2):
            pass  # 可以在这里添加进度输出
    
    print(f"\n{'='*70}")
    print(f"Trace 生成完成！")
    print(f"{'='*70}")
    print(f"Trace 文件: {trace_file}")
    
    # 统计 trace 内容
    if os.path.exists(trace_file):
        with open(trace_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        print(f"总 trace 记录数: {len(lines)}")
        
        # 统计 impact 分布
        impact_counts = {}
        trigger_counts = {"triggered": 0, "not_triggered": 0}
        timeline_written = 0
        
        for line in lines:
            try:
                trace = json.loads(line.strip())
                impact = trace.get("impact_evaluation", {}).get("impact", "NO_OP")
                impact_counts[impact] = impact_counts.get(impact, 0) + 1
                
                trigger = trace.get("trigger", {})
                if trigger.get("triggered", False):
                    trigger_counts["triggered"] += 1
                else:
                    trigger_counts["not_triggered"] += 1
                
                if trace.get("writeback", {}).get("timeline_written", False):
                    timeline_written += 1
            except:
                pass
        
        print(f"\nImpact 分布:")
        for impact, count in sorted(impact_counts.items()):
            print(f"  {impact:20s}: {count:4d} 次")
        
        print(f"\n触发统计:")
        print(f"  已触发: {trigger_counts['triggered']:4d} 次")
        print(f"  未触发: {trigger_counts['not_triggered']:4d} 次")
        
        print(f"\nTimeline 写入: {timeline_written} 次")
        
        print(f"\n{'='*70}")
        print(f"查看 trace 文件:")
        print(f"  cat {trace_file} | jq 'select(.time.ts >= 5.0 and .time.ts <= 10.0)'")
        print(f"  cat {trace_file} | jq 'select(.to_c_message.sent == true)'")
        print(f"{'='*70}\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="B2 Runtime Trace 生成测试")
    parser.add_argument("--duration", type=int, default=15, help="测试时长（秒）")
    parser.add_argument("--scenario", type=str, default="path_change",
                       choices=["normal", "path_change", "event", "people", "no_evidence"],
                       help="测试场景")
    parser.add_argument("--fps", type=float, default=30.0, help="帧率")
    
    args = parser.parse_args()
    
    run_trace_test(
        duration_seconds=args.duration,
        scenario=args.scenario,
        fps=args.fps
    )
