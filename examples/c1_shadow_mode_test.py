#!/usr/bin/env python3
"""
C1 Shadow Mode 测试脚本

测试 C1 Shadow Controller 的观察能力，不控制系统。

运行方式：
    python examples/c1_shadow_mode_test.py
"""

import sys
import os
import time
import random

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vision_pipeline.c1_controller.c1_shadow_controller import C1ShadowController
from vision_pipeline.c1_controller.c1_config import C1_MODE_SHADOW_ONLY


def simulate_motion_scenarios():
    """
    模拟不同的运动场景
    
    返回：
        (motion_score, frame_diff, scene_class) 的生成器
    """
    scenarios = [
        # (场景名, motion_score, frame_diff, scene_class, 持续时间)
        ("正常行走", 0.1, 0.05, "allow_camera", 5),
        ("检测到风险", 0.3, 0.2, "allow_camera", 3),
        ("严重晃动", 0.9, 0.8, "allow_camera", 2),
        ("静止", 0.05, 0.02, "allow_camera", 3),
        ("隐私区域", 0.1, 0.05, "force_camera_off", 2),
        ("恢复稳定", 0.1, 0.05, "allow_camera", 3),
    ]
    
    for scenario_name, motion_score, frame_diff, scene_class, duration in scenarios:
        print(f"\n📋 场景: {scenario_name}")
        print(f"   motion_score={motion_score:.2f}, frame_diff={frame_diff:.2f}, scene_class={scene_class}")
        
        for _ in range(duration * 2):  # 每 0.5 秒一次
            yield (motion_score, frame_diff, scene_class)
            time.sleep(0.5)


def main():
    """主函数"""
    print("=" * 70)
    print("C1 Shadow Mode 测试")
    print("=" * 70)
    print()
    print(f"📋 C1_MODE_SHADOW_ONLY: {C1_MODE_SHADOW_ONLY}")
    print()
    print("⚠️  Shadow Mode 特点:")
    print("   - 只观察，不控制")
    print("   - 不影响 pipeline")
    print("   - 不执行任何决策")
    print()
    print("开始模拟场景...")
    print()
    
    # 创建 Shadow Controller
    shadow_controller = C1ShadowController()
    
    # 模拟场景
    for i, (motion_score, frame_diff, scene_class) in enumerate(simulate_motion_scenarios()):
        timestamp = time.time()
        
        # 观察（但不执行）
        decisions = shadow_controller.observe(
            motion_score=motion_score,
            frame_diff=frame_diff,
            scene_class=scene_class,
            timestamp=timestamp,
        )
        
        # 验证：Shadow Mode 不应该影响系统
        # 这里我们只是打印，不做任何控制
    
    print()
    print("=" * 70)
    print("✅ Shadow Mode 测试完成")
    print("=" * 70)
    print()
    print("📋 观察要点:")
    print("   1. 日志频率是否稳定（LOG_INTERVAL_SEC=0.5）")
    print("   2. 是否出现抖动 / spam")
    print("   3. 是否能覆盖\"晃动 / 静止 / 切换\"场景")
    print()
    print("📋 下一步:")
    print("   1. 跑 5-10 分钟真实输入")
    print("   2. 看 3 件事：")
    print("      - 日志频率是否稳定")
    print("      - 是否出现抖动 / spam")
    print("      - 是否能覆盖\"晃动 / 静止 / 切换\"")
    print()


if __name__ == "__main__":
    main()


