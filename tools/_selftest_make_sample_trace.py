#!/usr/bin/env python3
"""
自检脚本：生成示例 trace.jsonl

生成一个 10 行 trace.jsonl（含 2 条 RED、2 条 YELLOW、其余 GREEN）用于演示。
"""

import json
from pathlib import Path

def make_event(engine_version, human_time, frame_id, impact, main_factor=None, 
               range_m=None, decision_level=None, advisory_only=None, 
               writeback_timeline=False, human_interpretation=None):
    """创建事件"""
    event = {
        "engine_version": engine_version,
        "time": {
            "human_time": human_time,
            "t_video_s": frame_id / 30.0,
            "frame_id": frame_id
        },
        "impact": {
            "impact": impact
        },
        "writeback": {
            "timeline": writeback_timeline
        }
    }
    
    if main_factor:
        event["factors"] = {"main_factor": main_factor}
        event["main_factor"] = main_factor
    
    if decision_level:
        event["impact"]["level"] = decision_level
        event["decision"] = {"level": decision_level}
    
    if advisory_only is not None:
        event["impact"]["advisory_only"] = advisory_only
    
    if range_m is not None:
        event["range_m"] = range_m
        event["gate"] = {"details": {"range_m": range_m}}
    
    if human_interpretation:
        event["human_interpretation"] = human_interpretation
        event["trace_explain"] = {"human_interpretation": human_interpretation}
    
    return event

def main():
    events = []
    
    # 2 条 RED
    # RED 1: authority_violation (2m 内 NEED_STOP)
    events.append(make_event(
        "v0.4.3", "00:01.000", 30, "NEED_STOP", 
        main_factor="PATH", range_m=1.5, decision_level="INTERRUPT", 
        advisory_only=True
    ))
    
    # RED 2: env_overreach (ENV 触发 INTERRUPT)
    events.append(make_event(
        "v0.4.3", "00:02.000", 60, "NEED_SLOW_DOWN",
        main_factor="ENV", decision_level="INTERRUPT", advisory_only=True
    ))
    
    # 2 条 YELLOW
    # YELLOW 1: no_op_timeline (NO_OP 写入 timeline)
    events.append(make_event(
        "v0.4.3", "00:03.000", 90, "NO_OP",
        writeback_timeline=True
    ))
    
    # YELLOW 2: over_prediction_language (确认性语言)
    events.append(make_event(
        "v0.4.3", "00:04.000", 120, "NEED_SLOW_DOWN",
        main_factor="PATH", advisory_only=True,
        human_interpretation="前方必然会出现障碍物"
    ))
    
    # 6 条 GREEN
    for i in range(6):
        events.append(make_event(
            "v0.4.3", f"00:{5+i:02d}.000", 150 + i * 30,
            "NEED_SLOW_DOWN" if i % 2 == 0 else "NO_OP",
            main_factor="PATH" if i % 2 == 0 else None,
            advisory_only=True if i % 2 == 0 else None,
            writeback_timeline=(i % 2 == 0)
        ))
    
    # 写入文件
    output_path = Path("trace.jsonl")
    with open(output_path, "w", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    
    print(f"✅ Generated {len(events)} events in {output_path}")
    print(f"  - RED: 2 (authority_violation, env_overreach)")
    print(f"  - YELLOW: 2 (no_op_timeline, over_prediction_language)")
    print(f"  - GREEN: 6")

if __name__ == "__main__":
    main()
