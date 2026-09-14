#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行 B2 处理视频并生成完整 trace 和日志
处理 6分42秒的视频
"""

import sys
import os
import cv2
import time
import json
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 直接导入 B2，避免触发其他模块的导入问题
import importlib.util

# 导入 B2 相关模块
spec_b2 = importlib.util.spec_from_file_location(
    "b2_v03",
    project_root / "vision_pipeline" / "b2" / "v03" / "b2_v03.py"
)
b2_module = importlib.util.module_from_spec(spec_b2)

# 手动设置依赖
spec_factors = importlib.util.spec_from_file_location(
    "factors",
    project_root / "vision_pipeline" / "b2" / "v03" / "factors.py"
)
factors_module = importlib.util.module_from_spec(spec_factors)
sys.modules['vision_pipeline.b2.v03.factors'] = factors_module
spec_factors.loader.exec_module(factors_module)

spec_log_utils = importlib.util.spec_from_file_location(
    "log_utils",
    project_root / "vision_pipeline" / "b2" / "v03" / "log_utils.py"
)
log_utils_module = importlib.util.module_from_spec(spec_log_utils)
sys.modules['vision_pipeline.b2.v03.log_utils'] = log_utils_module
spec_log_utils.loader.exec_module(log_utils_module)

spec_health = importlib.util.spec_from_file_location(
    "b2_health_logger",
    project_root / "vision_pipeline" / "b2" / "v03" / "b2_health_logger.py"
)
health_module = importlib.util.module_from_spec(spec_health)
sys.modules['vision_pipeline.b2.v03.b2_health_logger'] = health_module
spec_health.loader.exec_module(health_module)

spec_trace = importlib.util.spec_from_file_location(
    "trace_writer",
    project_root / "vision_pipeline" / "b2" / "v03" / "trace" / "trace_writer.py"
)
trace_module = importlib.util.module_from_spec(spec_trace)
sys.modules['vision_pipeline.b2.v03.trace.trace_writer'] = trace_module
spec_trace.loader.exec_module(trace_module)

# 现在可以导入 B2
spec_b2.loader.exec_module(b2_module)
B2v03 = b2_module.B2v03


def extract_perception_from_frame(frame, frame_id, ts):
    """
    从视频帧提取 perception 数据
    这是一个简化版本，实际应该调用视觉检测模块
    
    v0.4.3: 添加 view_state 构造
    """
    # 导入 view_state 构造器
    from vision_pipeline.b2.v03.utils.view_state_builder import build_view_state
    
    # 简化实现：返回基本的 perception 结构
    # 实际应该调用 YOLO、OCR 等模块
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
    
    # v0.4.3: 添加 view_state（最小实现）
    # 这里使用简化的估计值，实际应该从 IMU/相机数据计算
    # 对于视频回放，我们假设：
    # - 稳定性：中等（0.7）
    # - 距离：默认 10 米
    # - 可见度：中等（0.75）
    current_stability = 0.7  # 简化：假设中等稳定性
    estimated_range_m = 10.0  # 简化：假设 10 米
    current_visibility = 0.75  # 简化：假设中等可见度
    
    perception["view_state"] = build_view_state(
        stability_score=current_stability,
        range_m=estimated_range_m,
        visibility_score=current_visibility,
        source="vision",
        confidence=0.8,
    )
    
    # 这里可以添加实际的视觉检测逻辑
    # 例如：YOLO 检测、路径分析等
    
    return perception


def run_video_processing(video_path: str, output_trace: str = "traces/b2_runtime_trace_v04.jsonl"):
    """
    处理视频并生成 trace
    """
    print(f"\n{'='*70}")
    print(f"B2 视频处理 - 生成完整 Trace 和日志")
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
    print(f"\n开始处理...\n")
    
    # 初始化 B2
    base_ts = time.time()
    b2 = B2v03(
        future_window_start=1.0,
        future_window_end=8.0,
        debug=True,  # 启用调试输出
        log_mode="video",
        log_base_ts=base_ts,
        enable_trace=True,
        trace_file=output_trace,
        fps=fps
    )
    
    frame_id = 0
    processed_frames = 0
    last_print_ts = 0
    
    # 统计信息
    stats = {
        "total_frames": 0,
        "processed_frames": 0,
        "decisions": 0,
        "no_ops": 0,
        "timeline_written": 0
    }
    
    print(f"{'时间':>8} | {'帧ID':>6} | {'Impact':>15} | {'Factor':>10} | {'Conf':>5} | {'Timeline':>8}")
    print(f"{'-'*70}")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 计算当前时间戳（相对于视频开始）
            current_ts = frame_id / fps
            absolute_ts = base_ts + current_ts
            
            # 提取 perception
            perception = extract_perception_from_frame(frame, frame_id, absolute_ts)
            
            # 调用 B2 tick
            result = b2.tick(
                frame_ts=absolute_ts,
                perception=perception,
                frame_id=frame_id
            )
            
            stats["total_frames"] += 1
            stats["processed_frames"] += 1
            
            # 打印关键信息（每 0.5 秒或每次有决策时）
            should_print = False
            if result:
                should_print = True
                stats["decisions"] += 1
                impact = result.get("impact", "NO_OP")
                main_factor = result.get("main_factor", "unknown")
                confidence = result.get("confidence", 0.0)
                timeline_written = impact not in ("NO_OP", None)
                
                if timeline_written:
                    stats["timeline_written"] += 1
                
                print(f"{current_ts:8.2f}s | {frame_id:6d} | {impact:15s} | {main_factor:10s} | {confidence:5.2f} | {'✓' if timeline_written else '✗':>8}")
            elif current_ts - last_print_ts >= 0.5:
                # 每 0.5 秒打印一次进度
                should_print = True
                stats["no_ops"] += 1
                print(f"{current_ts:8.2f}s | {frame_id:6d} | {'NO_OP':15s} | {'-':10s} | {'-':5s} | {'-':>8}")
            
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
        print(f"  Timeline 写入: {stats['timeline_written']}")
        print(f"\nTrace 文件: {output_trace}")
        
        # 统计 trace 内容
        if os.path.exists(output_trace):
            with open(output_trace, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            print(f"Trace 记录数: {len(lines)}")
            
            # 统计 impact 分布
            impact_counts = {}
            for line in lines:
                try:
                    trace = json.loads(line.strip())
                    impact = trace.get("impact_evaluation", {}).get("impact", "NO_OP")
                    impact_counts[impact] = impact_counts.get(impact, 0) + 1
                except:
                    pass
            
            print(f"\nImpact 分布:")
            for impact, count in sorted(impact_counts.items()):
                print(f"  {impact:20s}: {count:4d} 次")
        
        print(f"\n{'='*70}\n")


if __name__ == "__main__":
    video_path = "test_video_complex_6m42s.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ 视频文件不存在: {video_path}")
        print(f"当前目录: {os.getcwd()}")
        sys.exit(1)
    
    run_video_processing(video_path)
