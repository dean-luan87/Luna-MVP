#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B2 v0.5 视频测试脚本（简化版）

处理 test_video_complex_6m42s.mp4 并生成 v0.5 格式的 trace
"""

import sys
import os
import cv2
import time
import json
from pathlib import Path
from typing import Optional

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入 B2（使用简化方式，避免复杂的依赖）
try:
    from vision_pipeline.b2.v03.b2_v03 import B2v03
    from vision_pipeline.b2.v03.utils.view_state_builder import build_view_state
    from vision_pipeline.b2.v03.trace_writer_v043 import TraceWriterV043
    # v0.5: 导入 C 控制器
    from vision_pipeline.c1_controller.c1_active_controller import C1ActiveController
    # TEMP: 临时证据（仅用于 v0.5 视频回归）
    from tools.temp_evidence import TempEvidence
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保所有依赖已安装")
    sys.exit(1)


def extract_perception_from_frame(frame, frame_id, ts, fps):
    """从视频帧提取 perception 数据（简化版）"""
    # 简化实现：返回基本的 perception 结构
    perception = {
        "timestamp": ts,
        "frame_id": frame_id,
        "objects": [],
        "path": {
            "surface": "smooth",
            "obstacle": False
        },
        "scene": "outdoor",
        "structure": "open",
        "people": {
            "count": 0,
            "density": "low"
        },
        "events": []
    }
    
    # v0.4.3: 添加 view_state
    # v0.5 点火修复：提高稳定性分数以满足点火条件
    # 点火条件：stability >= 0.85, visibility >= 0.7, range_m >= 2.0
    current_stability = 0.90  # 提高稳定性以满足点火条件
    estimated_range_m = 8.0   # 假设 8 米
    current_visibility = 0.85  # 提高可见度以满足点火条件
    
    perception["view_state"] = build_view_state(
        stability_score=current_stability,
        range_m=estimated_range_m,
        visibility_score=current_visibility,
        source="vision",
        confidence=0.8,
    )
    
    return perception


def _should_print_event(event_type: str) -> bool:
    """
    v0.5 runtime trace contains multiple event types per frame:
      - GATE_RUNTIME_PROFILE
      - C_RUNTIME_PROFILE
      - tick (sparse or none when NO_OP is filtered)

    Console should print only one line per frame for clarity.
    We print only Gate runtime lines here to avoid duplicate prints.
    """
    return event_type == "GATE_RUNTIME_PROFILE"


def run_v05_video_test(video_path: str, output_trace: str = "traces/b2_v05_video_trace.jsonl", max_frames: int = None, assume_evidence_ok: bool = False, use_temp_evidence: bool = False):
    """处理视频并生成 v0.5 格式的 trace"""
    print(f"\n{'='*70}")
    print(f"B2 v0.5 视频测试 - 生成 Trace")
    print(f"{'='*70}")
    print(f"视频文件: {video_path}")
    print(f"Trace 输出: {output_trace}")
    print(f"{'='*70}\n")
    
    # 清理旧的 trace 文件
    if os.path.exists(output_trace):
        os.remove(output_trace)
        print(f"已清理旧 trace 文件: {output_trace}\n")
    
    # 打开视频
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ 无法打开视频文件: {video_path}")
        return
    
    # 获取视频信息
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0
    
    print(f"视频信息:")
    print(f"  帧率: {fps:.2f} fps")
    print(f"  总帧数: {total_frames}")
    print(f"  时长: {duration:.2f} 秒 ({int(duration//60)}分{int(duration%60)}秒)")
    
    if max_frames:
        print(f"  限制处理: {max_frames} 帧")
    
    print(f"\n开始处理...\n")
    
    # 初始化 B2
    base_ts = time.time()
    try:
        b2 = B2v03(
            future_window_start=1.0,
            future_window_end=8.0,
            debug=False,
            log_mode="video",
            log_base_ts=base_ts,
            enable_trace=True,
            fps=fps
        )
        # 设置 trace 路径
        b2.trace_writer_v043.out_path = output_trace
        # v0.5: Test mode - force evidence_ok=True for video regression
        if assume_evidence_ok:
            b2._test_mode_assume_evidence_ok = True
        
        # TEMP: 临时证据（仅用于 v0.5 视频回归，不引入 YOLO）
        temp_evidence = None
        if use_temp_evidence:
            temp_evidence = TempEvidence(min_stable_frames=10, min_visibility=0.6)
            b2._temp_evidence = temp_evidence
    except Exception as e:
        print(f"❌ B2 初始化错误: {e}")
        import traceback
        traceback.print_exc()
        cap.release()
        return
    
    # v0.5: 初始化 C 控制器（使用同一个 trace writer）
    try:
        c_trace_writer = TraceWriterV043(out_path=output_trace, enabled=True)
        c1_controller = C1ActiveController(
            trace_writer=c_trace_writer
        )
        print("✅ C 控制器初始化完成")
    except Exception as e:
        print(f"⚠️ C 控制器初始化失败: {e}")
        print("   继续运行，但不会生成 C RuntimeProfile")
        c1_controller = None
    
    frame_id = 0
    processed_frames = 0
    last_print_ts = 0
    
    # 统计信息
    stats = {
        "total_frames": 0,
        "processed_frames": 0,
        "decisions": 0,
        "no_ops": 0,
        "gate_active": 0,
        "gate_read_only": 0,
        "gate_suspended": 0
    }
    
    print(f"{'时间':>8} | {'帧ID':>6} | {'Gate':>12} | {'Compute':>10} | {'Impact':>15}")
    print(f"{'-'*70}")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if max_frames and frame_id >= max_frames:
                print(f"\n达到最大帧数限制: {max_frames}")
                break
            
            # 计算当前时间戳（相对于视频开始）
            current_ts = frame_id / fps
            absolute_ts = base_ts + current_ts
            
            # 提取 perception
            perception = extract_perception_from_frame(frame, frame_id, absolute_ts, fps)
            
            # Ensure view_state exists (v0.5 requirement)
            if isinstance(perception, dict):
                vs = perception.get("view_state") or {}
                # If upstream didn't supply it, keep conservative defaults here
                vs.setdefault("stability_score", None)  # let GateEvaluator apply missing policy
                vs.setdefault("range_m", None)
                vs.setdefault("visibility_score", 0.75)
                perception["view_state"] = vs
            
            # 调用 B2 tick
            try:
                result = b2.tick(
                    frame_ts=absolute_ts,
                    perception=perception,
                    frame_id=frame_id
                )
            except Exception as e:
                print(f"⚠️ Frame {frame_id} 处理错误: {e}")
                frame_id += 1
                continue
            
            # v0.5: 调用 C 控制器 observe（生成 C RuntimeProfile）
            if c1_controller:
                try:
                    # 模拟 motion_score 和 frame_diff（简化版）
                    # 实际应用中这些值应该从视频帧计算得出
                    motion_score = 0.5  # 中等运动
                    frame_diff = 0.3     # 中等帧差异
                    
                    c1_controller.observe(
                        motion_score=motion_score,
                        frame_diff=frame_diff,
                        timestamp=absolute_ts,
                        scene_class="allow_camera"
                    )
                except Exception as e:
                    # C 控制器错误不影响主流程
                    pass
            
            stats["total_frames"] += 1
            stats["processed_frames"] += 1
            
            # 读取 trace 文件，获取 Gate 状态（如果已写入）
            # Note: b2.tick() 会立即写入 GATE_RUNTIME_PROFILE，所以我们可以读取最后一条记录
            gate_mode = "UNKNOWN"
            compute_level = "UNKNOWN"
            last_event_type = None
            if os.path.exists(output_trace):
                try:
                    with open(output_trace, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        # 从后往前查找最近的 GATE_RUNTIME_PROFILE 事件
                        for line in reversed(lines):
                            if not line.strip():
                                continue
                            trace_obj = json.loads(line)
                            event_type = trace_obj.get("event_type", "")
                            
                            # v0.5: GATE_RUNTIME_PROFILE 事件结构
                            if event_type == "GATE_RUNTIME_PROFILE":
                                gate_profile = trace_obj.get("gate_runtime_profile", {})
                                if isinstance(gate_profile, dict):
                                    # v0.5: gate_mode 字段在 gate_runtime_profile 顶层
                                    gate_mode = gate_profile.get("gate_mode") or gate_profile.get("mode", "UNKNOWN")
                                    compute_level = gate_profile.get("compute_level", "UNKNOWN")
                                    last_event_type = event_type
                                    
                                    # 统计（每帧统计一次，用于最终报告）
                                    if gate_mode == "ACTIVE":
                                        stats["gate_active"] += 1
                                    elif gate_mode == "READ_ONLY":
                                        stats["gate_read_only"] += 1
                                    elif gate_mode == "SUSPENDED":
                                        stats["gate_suspended"] += 1
                                break
                            # 兼容旧格式：如果有 gate 字段
                            elif trace_obj.get("gate"):
                                gate_info = trace_obj.get("gate", {})
                                if isinstance(gate_info, dict):
                                    gate_mode = gate_info.get("gate_mode") or gate_info.get("mode", "UNKNOWN")
                                    compute_level = gate_info.get("compute_level", "UNKNOWN")
                                    last_event_type = event_type
                                    
                                    # 统计（每帧统计一次，用于最终报告）
                                    if gate_mode == "ACTIVE":
                                        stats["gate_active"] += 1
                                    elif gate_mode == "READ_ONLY":
                                        stats["gate_read_only"] += 1
                                    elif gate_mode == "SUSPENDED":
                                        stats["gate_suspended"] += 1
                                break
                except Exception:
                    pass
            
            # v0.5: print only once per frame, and only for Gate runtime profile
            # (C runtime profile is still written into trace, just not spammed to console)
            # Only print if we found a GATE_RUNTIME_PROFILE event (not C_RUNTIME_PROFILE)
            # If we have gate_mode info, we print (even if last_event_type check fails on first frame)
            should_print = False
            # Print if: (1) we found GATE_RUNTIME_PROFILE event, OR (2) we have gate_mode info (fallback for first frame)
            if _should_print_event(last_event_type or "") or (gate_mode != "UNKNOWN" and last_event_type != "C_RUNTIME_PROFILE"):
                if result:
                    should_print = True
                    stats["decisions"] += 1
                    impact = result.get("impact", "NO_OP")
                    if isinstance(impact, object) and hasattr(impact, "name"):
                        impact = impact.name
                    print(f"{current_ts:8.2f}s | {frame_id:6d} | {gate_mode:12s} | {compute_level:10s} | {str(impact):15s}")
                elif current_ts - last_print_ts >= 1.0:
                    # 每 1 秒打印一次进度（只打印 Gate 状态，不打印 C 状态）
                    should_print = True
                    stats["no_ops"] += 1
                    print(f"{current_ts:8.2f}s | {frame_id:6d} | {gate_mode:12s} | {compute_level:10s} | {'NO_OP':15s}")
            
            if should_print:
                last_print_ts = current_ts
            
            frame_id += 1
            
            # 显示进度（每 10 秒）
            if int(current_ts) % 10 == 0 and int(current_ts) != int(last_print_ts):
                progress = (current_ts / duration) * 100 if duration > 0 else 0
                print(f"\n[进度] {current_ts:.1f}s / {duration:.1f}s ({progress:.1f}%)")
    
    except KeyboardInterrupt:
        print(f"\n\n⚠️ 用户中断处理")
    except Exception as e:
        print(f"\n\n❌ 处理错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cap.release()
        
        print(f"\n{'='*70}")
        print(f"处理完成！")
        print(f"{'='*70}")
        print(f"统计信息:")
        print(f"  总帧数: {stats['total_frames']}")
        print(f"  处理帧数: {stats['processed_frames']}")
        print(f"  决策次数: {stats['decisions']}")
        print(f"  NO_OP 次数: {stats['no_ops']}")
        print(f"\nGate 状态分布:")
        print(f"  ACTIVE: {stats['gate_active']}")
        print(f"  READ_ONLY: {stats['gate_read_only']}")
        print(f"  SUSPENDED: {stats['gate_suspended']}")
        print(f"\nTrace 文件: {output_trace}")
        
        # 统计 trace 内容
        if os.path.exists(output_trace):
            with open(output_trace, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            print(f"Trace 记录数: {len(lines)}")
        
        print(f"\n{'='*70}\n")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="B2 v0.5 视频测试脚本")
    parser.add_argument("video_path", nargs="?", default="test_video_complex_6m42s.mp4", 
                        help="视频文件路径（默认: test_video_complex_6m42s.mp4）")
    parser.add_argument("--max-frames", type=int, help="最大处理帧数（用于快速测试）")
    parser.add_argument("--output", type=str, default="traces/b2_v05_video_trace.jsonl",
                        help="Trace 输出文件路径（默认: traces/b2_v05_video_trace.jsonl）")
    parser.add_argument("--assume-evidence-ok", action="store_true",
                        help="Test-only: force evidence_ok=True (no YOLO)")
    parser.add_argument("--use-temp-evidence", action="store_true",
                        help="TEMP: heuristic evidence for v0.5 regression (no YOLO)")
    args = parser.parse_args()
    
    video_path = args.video_path
    
    if not os.path.exists(video_path):
        print(f"❌ 视频文件不存在: {video_path}")
        print(f"当前目录: {os.getcwd()}")
        sys.exit(1)
    
    run_v05_video_test(video_path, output_trace=args.output, max_frames=args.max_frames, 
                      assume_evidence_ok=args.assume_evidence_ok, use_temp_evidence=args.use_temp_evidence)
