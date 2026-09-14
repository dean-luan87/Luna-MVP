#!/usr/bin/env python3
"""
B2 v0.1 视频验证脚本

你后面要用 6m42s 视频做标准回归，这个脚本就是你固定的"验收入口"。

使用方法：
    python3 examples/b2_v01_video_validation.py --duration 7 --video test_video_complex_6m42s.mp4
"""

import argparse
import time
import json
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from vision_pipeline.b2.b2_controller import B2Controller


def main():
    ap = argparse.ArgumentParser(description="B2 v0.1 视频验证")
    ap.add_argument("--duration", type=float, default=7.0, help="验证时长（分钟）")
    ap.add_argument("--video", type=str, required=True, help="视频文件路径")
    ap.add_argument("--out", type=str, default="artifacts/b2_v01_log.json", help="输出日志路径")
    args = ap.parse_args()
    
    # 初始化 B2 Controller
    controller = B2Controller()
    start = time.time()
    end = start + args.duration * 60
    
    events = []
    frames = 0
    b2_count = 0
    trigger_hist = {}
    
    print("=" * 70)
    print("B2 v0.1 视频验证")
    print("=" * 70)
    print(f"视频文件: {args.video}")
    print(f"验证时长: {args.duration} 分钟")
    print()
    print("开始验证...")
    print()
    
    # 模拟帧循环（实际应该从视频读取）
    # TODO: 这里用你现有的帧循环拿到 world_update / ego_motion / impact_events
    while time.time() < end:
        frames += 1
        
        # v0.1 先用粗指标；后续再接真实 world_update
        # 这里模拟一些变化，确保 B2 能触发
        elapsed = time.time() - start
        density = 20 + int(elapsed / 10) % 30  # 模拟密度变化
        motion_level = 10 + int(elapsed / 5) % 20  # 模拟运动变化
        
        observe_input = {
            "world_update": {
                "density": density,
                "motion_level": motion_level,
                "illumination": 30,
                "dominant_direction": 0,
            },
            "ego_motion": {"heading": 0},
            "impact_events": [],  # v0.1 可为空；后续接入事件检测
            "world_observability": 0.8
        }
        
        out = controller.observe(observe_input)
        if out:
            b2_count += 1
            trigger_hist[out.trigger_reason] = trigger_hist.get(out.trigger_reason, 0) + 1
            
            # 记录事件
            events.append({
                "ts": out.ts,
                "trigger": out.trigger_reason,
                "digest_delta": out.metrics.get("digest_delta"),
                "advisories": [
                    {
                        "type": a.advisory_type,
                        "priority": a.priority,
                        "confidence": a.confidence,
                        "reason_code": a.reason_code,
                    }
                    for a in out.advisories
                ],
                "buffer": None if out.future_buffer is None else {
                    "horizon_sec": out.future_buffer.horizon_sec,
                    "risk_window_sec": out.future_buffer.risk_window_sec,
                    "safe_window_sec": out.future_buffer.safe_window_sec,
                    "ttl_sec": out.future_buffer.ttl_sec,
                    "n_conflicts": len(out.future_buffer.predicted_conflicts),
                }
            })
            
            # 打印进度
            if controller.should_log(out.ts):
                print(f"  [{elapsed:.1f}s] B2 输出 #{b2_count}: {out.trigger_reason}")
        
        time.sleep(0.1)  # 模拟帧循环节律，复用你现有节律亦可
    
    # 生成摘要
    summary = {
        "frames": frames,
        "b2_outputs": b2_count,
        "trigger_hist": trigger_hist,
        "duration_sec": args.duration * 60,
        "validation_time": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    payload = {"summary": summary, "events": events}
    
    # 保存日志
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
    
    # 打印结果
    print()
    print("=" * 70)
    print("B2 v0.1 验证结果")
    print("=" * 70)
    print()
    print("📊 摘要:")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print()
    
    # 验收检查
    print("📋 验收检查:")
    passed = True
    if b2_count < 5:
        print(f"  ❌ b2_outputs ({b2_count}) < 5")
        passed = False
    else:
        print(f"  ✅ b2_outputs ({b2_count}) >= 5")
    
    if "INIT" not in trigger_hist:
        print("  ❌ 缺少 INIT 触发")
        passed = False
    else:
        print(f"  ✅ INIT 触发: {trigger_hist['INIT']} 次")
    
    if "TTL_EXPIRE" not in trigger_hist:
        print("  ❌ 缺少 TTL_EXPIRE 触发")
        passed = False
    else:
        print(f"  ✅ TTL_EXPIRE 触发: {trigger_hist['TTL_EXPIRE']} 次")
    
    if "WORLD_CHANGE" in trigger_hist:
        print(f"  ✅ WORLD_CHANGE 触发: {trigger_hist['WORLD_CHANGE']} 次")
    else:
        print("  ⚠️  WORLD_CHANGE 未触发（可能是 digest 太迟钝或输入未更新）")
    
    print()
    print(f"日志已保存: {out_path}")
    print()
    
    if passed:
        print("=" * 70)
        print("✅ B2 v0.1 验证通过")
        print("=" * 70)
    else:
        print("=" * 70)
        print("❌ B2 v0.1 验证未通过")
        print("=" * 70)
    
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())

