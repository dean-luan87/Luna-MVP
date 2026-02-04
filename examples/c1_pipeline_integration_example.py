"""
C1 集成到 PipelineController 示例

展示如何在 PipelineController.process_frame() 之前调用 C1Controller。
"""

import sys
import os
import time
import numpy as np

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from c1_controller import C1Controller, C1Input
from vision_pipeline.pipeline_controller import PipelineController


def build_c1_input_from_frame(frame, motion_score=0.0, frame_diff_score=0.5):
    """
    从 frame 构建 C1Input（示例实现）
    
    实际实现中，需要：
    - 从 IMU 获取 motion_score
    - 从帧间差异计算 frame_diff_score
    - 从地图/记忆系统获取 next_scene_hint
    - 从风险系统获取 risk_hint
    - 从场景识别/用户设置获取 privacy_zone
    
    Args:
        frame: 图像帧
        motion_score: 镜头晃动强度（mock）
        frame_diff_score: 帧变化幅度（mock）
    
    Returns:
        C1Input
    """
    return C1Input(
        timestamp=time.time(),
        motion_score=motion_score,
        frame_diff_score=frame_diff_score,
        next_scene_hint=None,  # 从地图/记忆系统获取
        risk_hint=None,        # 从风险系统获取
        privacy_zone=None,     # 从场景识别/用户设置获取
        user_camera_override=False,
    )


def example_pipeline_with_c1():
    """
    示例：在 PipelineController 中集成 C1
    
    关键点：
    1. 在 process_frame() 之前调用 C1Controller.decide()
    2. 如果 C1 禁止抽帧，直接返回
    3. 根据 C1Decision.target_fps 实现帧率控制（需要额外逻辑）
    """
    print("=" * 70)
    print("C1 集成到 PipelineController 示例")
    print("=" * 70)
    
    # 初始化
    c1_controller = C1Controller()
    pipeline_controller = PipelineController()
    
    # 模拟处理几帧
    print("\n[示例 1] 正常帧（允许抽帧）")
    frame_1 = np.zeros((480, 640, 3), dtype=np.uint8)
    c1_input_1 = build_c1_input_from_frame(frame_1, motion_score=0.1, frame_diff_score=0.3)
    c1_decision_1 = c1_controller.decide(c1_input_1)
    
    print(f"  C1 Decision: allow_frame={c1_decision_1.allow_frame}, target_fps={c1_decision_1.target_fps}")
    print(f"  Reason: {c1_decision_1.reason}")
    
    if c1_decision_1.allow_frame:
        # 继续处理（这里只是示例，实际需要实现帧率控制）
        print("  ✅ 允许处理这一帧")
        # pipeline_result = pipeline_controller.process_frame(frame_1, ...)
    else:
        print("  ❌ 禁止处理这一帧（视觉已暂停）")
    
    print("\n[示例 2] 严重晃动（禁止抽帧）")
    frame_2 = np.zeros((480, 640, 3), dtype=np.uint8)
    c1_input_2 = build_c1_input_from_frame(frame_2, motion_score=0.9, frame_diff_score=0.8)
    c1_decision_2 = c1_controller.decide(c1_input_2)
    
    print(f"  C1 Decision: allow_frame={c1_decision_2.allow_frame}, target_fps={c1_decision_2.target_fps}")
    print(f"  Reason: {c1_decision_2.reason}")
    
    if c1_decision_2.allow_frame:
        print("  ✅ 允许处理这一帧")
    else:
        print("  ❌ 禁止处理这一帧（视觉已暂停）")
        # 直接返回，不调用 pipeline_controller.process_frame()
    
    print("\n[示例 3] 隐私区域 Class C（禁止抽帧）")
    c1_input_3 = C1Input(
        timestamp=time.time(),
        motion_score=0.1,
        frame_diff_score=0.3,
        privacy_zone="C",  # Class C
    )
    c1_decision_3 = c1_controller.decide(c1_input_3)
    
    print(f"  C1 Decision: allow_frame={c1_decision_3.allow_frame}, target_fps={c1_decision_3.target_fps}")
    print(f"  Reason: {c1_decision_3.reason}")
    
    if c1_decision_3.allow_frame:
        print("  ✅ 允许处理这一帧")
    else:
        print("  ❌ 禁止处理这一帧（隐私区域）")
    
    print("\n" + "=" * 70)
    print("✅ 集成示例完成")
    print("=" * 70)
    print("\n📋 关键点：")
    print("  1. 在 PipelineController.process_frame() 之前调用 C1Controller.decide()")
    print("  2. 如果 C1Decision.allow_frame == False，直接返回，不处理这一帧")
    print("  3. 根据 C1Decision.target_fps 实现帧率控制（需要额外逻辑）")
    print("  4. 记录 C1Decision.reason 用于调试")


if __name__ == "__main__":
    example_pipeline_with_c1()


