#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 v0.5 格式的测试 trace（包含 GateRuntimeProfile）

用于测试 DCS 审计和 Viewer
"""

import json
import time
from pathlib import Path

def generate_v05_test_trace(output_path: str = "traces/b2_v05_test_trace.jsonl", num_frames: int = 100):
    """生成 v0.5 格式的测试 trace"""
    
    base_ts = time.time()
    fps = 30.0
    
    # 模拟不同的 Gate 状态
    gate_scenarios = [
        {"gate_mode": "ACTIVE", "compute_level": "FULL", "tick_interval_ms": 100, "blocked_by": None, "reason": "正常"},
        {"gate_mode": "ACTIVE", "compute_level": "FULL", "tick_interval_ms": 100, "blocked_by": None, "reason": "正常"},
        {"gate_mode": "READ_ONLY", "compute_level": "LIGHT", "tick_interval_ms": 150, "blocked_by": "insufficient_evidence", "reason": "证据不足"},
        {"gate_mode": "SUSPENDED", "compute_level": "NONE", "tick_interval_ms": 250, "blocked_by": "camera_shake", "reason": "镜头晃动"},
        {"gate_mode": "ACTIVE", "compute_level": "FULL", "tick_interval_ms": 100, "blocked_by": None, "reason": "正常"},
    ]
    
    with open(output_path, "w", encoding="utf-8") as f:
        for frame_id in range(num_frames):
            scenario = gate_scenarios[frame_id % len(gate_scenarios)]
            frame_ts = base_ts + (frame_id / fps)
            
            # 构造 v0.5 格式的 trace
            trace = {
                "event_type": "GATE_RUNTIME_PROFILE",
                "time": {
                    "ts": frame_ts,
                    "frame_id": frame_id,
                    "fps": fps,
                    "human_time": f"{int(frame_ts // 60):02d}:{int(frame_ts % 60):02d}.{int((frame_ts % 1) * 1000):03d}"
                },
                "gate_runtime_profile": {
                    "version": "v0.5",
                    "gate_mode": scenario["gate_mode"],
                    "compute_level": scenario["compute_level"],
                    "tick_interval_ms": scenario["tick_interval_ms"],
                    "allow_future_probe": False,
                    "authority_scope": "ADVISORY_ONLY",
                    "blocked_by": scenario["blocked_by"],
                    "human_reason": scenario["reason"],
                    "meta": {
                        "frame_ts": frame_ts,
                        "frame_id": frame_id,
                        "has_view_state": True
                    }
                },
                "dcs_result": {
                    "level": "GREEN" if scenario["gate_mode"] == "ACTIVE" else ("YELLOW" if scenario["gate_mode"] == "READ_ONLY" else "RED"),
                    "violations": [] if scenario["gate_mode"] == "ACTIVE" else [f"gate_{scenario['gate_mode'].lower()}"]
                }
            }
            
            f.write(json.dumps(trace, ensure_ascii=False) + "\n")
    
    print(f"✅ 已生成 v0.5 测试 trace: {output_path}")
    print(f"   总帧数: {num_frames}")

if __name__ == "__main__":
    generate_v05_test_trace()
