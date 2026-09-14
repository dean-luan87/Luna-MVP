#!/usr/bin/env python3
"""
C1 Active Mode v0.1 测试脚本（完全独立版）

测试 C1 Active Mode 的控制能力（仅控制 ModelingExecutor）。

运行方式：
    python examples/c1_active_mode_test_standalone.py
"""

import time

# 直接复制配置（避免导入问题）
MOTION_SCORE_THRESHOLD = 0.7
LOG_INTERVAL_SEC = 0.5


def simulate_c1_decision(motion_score: float) -> dict:
    """
    模拟 C1 决策（简化版）
    
    Args:
        motion_score: 运动评分
    
    Returns:
        决策字典
    """
    if motion_score >= MOTION_SCORE_THRESHOLD:
        return {
            "state": "SUSPENDED",
            "skip_modeling": True,
            "reason": "motion_score >= threshold"
        }
    else:
        return {
            "state": "STABLE",
            "skip_modeling": False,
            "reason": "normal"
        }


def simulate_pipeline_behavior(c1_decision: dict) -> dict:
    """
    模拟 Pipeline 行为
    
    Args:
        c1_decision: C1 决策
    
    Returns:
        实际执行结果
    """
    if c1_decision["skip_modeling"]:
        return {
            "modeling_executed": False,
            "reason": "C1 skipped"
        }
    else:
        return {
            "modeling_executed": True,
            "reason": "C1 allowed"
        }


def simulate_scenarios():
    """模拟不同的运动场景"""
    scenarios = [
        # (场景名, motion_score, frame_diff, scene_class, 持续时间)
        ("正常行走", 0.1, 0.05, "allow_camera", 3),
        ("检测到风险", 0.3, 0.2, "allow_camera", 2),
        ("严重晃动", 0.9, 0.8, "allow_camera", 2),
        ("静止", 0.05, 0.02, "allow_camera", 2),
        ("恢复稳定", 0.1, 0.05, "allow_camera", 2),
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
    print("C1 Active Mode v0.1 测试（独立版）")
    print("=" * 70)
    print()
    print("⚠️  Active Mode v0.1 特点:")
    print("   - 仅控制 ModelingExecutor 执行")
    print("   - 不允许控制 fps、抽帧频率、路由")
    print("   - LV2 / LV3 仍然跑")
    print("   - 只是重计算被暂停")
    print()
    print("开始模拟场景...")
    print()
    
    # 模拟场景
    for i, (motion_score, frame_diff, scene_class) in enumerate(simulate_scenarios()):
        timestamp = time.time()
        
        # C1 Active Mode 决策
        c1_decision = simulate_c1_decision(motion_score)
        
        # Pipeline 实际行为
        pipeline_result = simulate_pipeline_behavior(c1_decision)
        
        # 对比日志
        print(
            f"[C1-ACTIVE][{timestamp:.2f}] "
            f"C1决策={'SKIP_MODELING' if c1_decision['skip_modeling'] else 'ALLOW_MODELING'} "
            f"实际执行={'NO' if not pipeline_result['modeling_executed'] else 'YES'} "
            f"状态={c1_decision['state']} "
            f"原因={c1_decision['reason']}"
        )
    
    print()
    print("=" * 70)
    print("✅ Active Mode v0.1 测试完成")
    print("=" * 70)
    print()
    print("📋 观察要点:")
    print("   1. C1 决策是否正确（SUSPEND → SKIP_MODELING）")
    print("   2. 实际执行是否与 C1 决策一致")
    print("   3. 是否有误杀 / 漏杀")
    print()
    print("📋 对比 Shadow Mode vs Active Mode:")
    print("   - Shadow Mode: 只观察，不控制")
    print("   - Active Mode: 控制 ModelingExecutor 执行")
    print()


if __name__ == "__main__":
    main()


