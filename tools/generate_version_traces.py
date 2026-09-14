#!/usr/bin/env python3
"""
生成三个版本的 trace 文件用于对比测试

v0.3: 没有 view_state，没有 Gate，会输出提醒
v0.4.1: 有 Gate，但可能缺少 view_state
v0.4.3: 有 view_state，Gate 正常工作
"""

import json
from pathlib import Path

def make_v03_event(frame_id, impact="NEED_SLOW_DOWN", main_factor="PATH"):
    """v0.3: 没有 view_state，没有 Gate，会输出提醒"""
    return {
        "engine_version": "v0.3",
        "time": {
            "human_time": f"00:{frame_id//30:02d}.{(frame_id%30)*33:03d}",
            "t_video_s": frame_id / 30.0,
            "frame_id": frame_id
        },
        "impact": {
            "impact": impact,
            "level": "CONDITION_CHANGE" if impact != "NO_OP" else "NOTICE",
            "advisory_only": True
        },
        "factors": {
            "main_factor": main_factor
        },
        "main_factor": main_factor,
        "writeback": {
            "timeline": impact != "NO_OP"
        },
        "to_c": {
            "send": impact != "NO_OP"
        },
        # v0.3 特点：没有 view_state，没有 gate
    }

def make_v041_event(frame_id, impact="NEED_SLOW_DOWN", main_factor="PATH", has_view_state=False):
    """v0.4.1: 有 Gate，但可能缺少 view_state"""
    event = {
        "engine_version": "v0.4.1",
        "time": {
            "human_time": f"00:{frame_id//30:02d}.{(frame_id%30)*33:03d}",
            "t_video_s": frame_id / 30.0,
            "frame_id": frame_id
        },
        "gate": {
            "mode": "ACTIVE"  # v0.4.1 可能 fallback 为 ACTIVE
        },
        "impact": {
            "impact": impact,
            "level": "CONDITION_CHANGE" if impact != "NO_OP" else "NOTICE",
            "advisory_only": True
        },
        "factors": {
            "main_factor": main_factor
        },
        "main_factor": main_factor,
        "writeback": {
            "timeline": impact != "NO_OP"
        },
        "to_c": {
            "send": impact != "NO_OP"
        }
    }
    
    # v0.4.1 特点：可能缺少 view_state
    if has_view_state:
        event["view_state"] = {
            "stability_score": 0.7,
            "range_m": 10.0,
            "visibility_score": 0.75
        }
    
    return event

def make_v043_event(frame_id, impact="NEED_SLOW_DOWN", main_factor="PATH", gate_mode="ACTIVE"):
    """v0.4.3: 有 view_state，Gate 正常工作"""
    return {
        "engine_version": "v0.4.3",
        "time": {
            "human_time": f"00:{frame_id//30:02d}.{(frame_id%30)*33:03d}",
            "t_video_s": frame_id / 30.0,
            "frame_id": frame_id
        },
        "gate": {
            "mode": gate_mode
        },
        "view_state": {
            "stability_score": 0.8 if gate_mode == "ACTIVE" else 0.3,
            "range_m": 10.0,
            "visibility_score": 0.75
        },
        "impact": {
            "impact": impact,
            "level": "CONDITION_CHANGE" if impact != "NO_OP" else "NOTICE",
            "advisory_only": True
        },
        "factors": {
            "main_factor": main_factor
        },
        "main_factor": main_factor,
        "writeback": {
            "timeline": impact != "NO_OP" and gate_mode == "ACTIVE"
        },
        "to_c": {
            "send": impact != "NO_OP" and gate_mode == "ACTIVE"
        }
    }

def main():
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)
    
    # 生成 60 秒的 trace（30 fps = 1800 帧，我们生成 60 个事件）
    events_per_version = 60
    
    # v0.3: 没有 view_state，没有 Gate，会输出提醒
    v03_events = []
    for i in range(events_per_version):
        frame_id = i * 30
        # v0.3 会频繁输出提醒（即使没有依据）
        impact = "NEED_SLOW_DOWN" if i % 3 == 0 else "NO_OP"
        main_factor = "PATH" if i % 3 == 0 else None
        v03_events.append(make_v03_event(frame_id, impact, main_factor))
    
    # v0.4.1: 有 Gate，但可能缺少 view_state（50% 缺少）
    v041_events = []
    for i in range(events_per_version):
        frame_id = i * 30
        impact = "NEED_SLOW_DOWN" if i % 3 == 0 else "NO_OP"
        main_factor = "PATH" if i % 3 == 0 else None
        # 50% 的事件缺少 view_state
        has_view_state = (i % 2 == 0)
        v041_events.append(make_v041_event(frame_id, impact, main_factor, has_view_state))
    
    # v0.4.3: 有 view_state，Gate 正常工作
    v043_events = []
    for i in range(events_per_version):
        frame_id = i * 30
        impact = "NEED_SLOW_DOWN" if i % 3 == 0 else "NO_OP"
        main_factor = "PATH" if i % 3 == 0 else None
        # v0.4.3 Gate 正常工作
        gate_mode = "ACTIVE" if i % 5 != 0 else "READ_ONLY"  # 80% ACTIVE
        v043_events.append(make_v043_event(frame_id, impact, main_factor, gate_mode))
    
    # 写入文件
    v03_path = artifacts_dir / "trace_v03.jsonl"
    v041_path = artifacts_dir / "trace_v041.jsonl"
    v043_path = artifacts_dir / "trace_v043.jsonl"
    
    for path, events in [(v03_path, v03_events), (v041_path, v041_events), (v043_path, v043_events)]:
        with open(path, "w", encoding="utf-8") as f:
            for event in events:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
        print(f"✅ Generated {len(events)} events in {path}")
    
    print(f"\n📊 Trace files ready for DCS evaluation")

if __name__ == "__main__":
    main()
