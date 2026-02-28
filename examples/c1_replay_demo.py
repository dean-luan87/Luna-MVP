"""
C1 回访工具演示脚本

演示如何使用 C1 Replay Tool 进行回放分析。
"""

import sys
import os
import json
import time

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from c1_replay.replay_loader import C1ReplayLoader
from c1_replay.replay_engine import C1ReplayEngine
from c1_replay.replay_report import C1ReplayReport
from c1_replay.replay_models import C1ReplayRecord, C1PipelineRecord, C1SystemMeta


def create_demo_logs():
    """
    创建演示用的日志数据
    
    模拟一个真实场景：
    1. 正常行走（STABLE）
    2. 检测到风险（ALERT）
    3. 严重晃动（SUSPENDED）
    4. 恢复（STABLE）
    """
    base_time = time.time() - 60  # 60 秒前开始
    
    c1_records = [
        # 正常行走（STABLE）
        C1ReplayRecord(
            timestamp=base_time + 0,
            prev_state="stable",
            current_state="stable",
            motion_score=0.1,
            frame_diff_score=0.3,
            allow_frame=True,
            target_fps=2,
            priority="environment",
            observation_mode="forward",
            reason="stable",
        ),
        C1ReplayRecord(
            timestamp=base_time + 1,
            prev_state="stable",
            current_state="stable",
            motion_score=0.1,
            frame_diff_score=0.3,
            allow_frame=True,
            target_fps=2,
            priority="environment",
            observation_mode="forward",
            reason="stable",
        ),
        # 检测到风险（ALERT）
        C1ReplayRecord(
            timestamp=base_time + 2,
            prev_state="stable",
            current_state="alert",
            motion_score=0.2,
            frame_diff_score=0.6,
            risk_hint="检测到水边",
            allow_frame=True,
            target_fps=10,
            priority="safety",
            observation_mode="local",
            reason="alert",
        ),
        C1ReplayRecord(
            timestamp=base_time + 3,
            prev_state="alert",
            current_state="alert",
            motion_score=0.3,
            frame_diff_score=0.7,
            risk_hint="检测到水边",
            allow_frame=True,
            target_fps=10,
            priority="safety",
            observation_mode="local",
            reason="alert",
        ),
        # 严重晃动（SUSPENDED）
        C1ReplayRecord(
            timestamp=base_time + 4,
            prev_state="alert",
            current_state="suspended",
            motion_score=0.9,  # 超过阈值
            frame_diff_score=0.8,
            allow_frame=False,
            target_fps=0,
            priority="none",
            observation_mode="none",
            reason="suspended",
        ),
        C1ReplayRecord(
            timestamp=base_time + 5,
            prev_state="suspended",
            current_state="suspended",
            motion_score=0.85,
            frame_diff_score=0.75,
            allow_frame=False,
            target_fps=0,
            priority="none",
            observation_mode="none",
            reason="suspended",
        ),
        # 恢复（STABLE）
        C1ReplayRecord(
            timestamp=base_time + 6,
            prev_state="suspended",
            current_state="stable",
            motion_score=0.1,
            frame_diff_score=0.3,
            allow_frame=True,
            target_fps=2,
            priority="environment",
            observation_mode="forward",
            reason="stable",
        ),
    ]
    
    pipeline_records = [
        C1PipelineRecord(
            timestamp=base_time + 0,
            navigation_executed=True,
            modeling_executed=True,
            latency_ms=5.2,
        ),
        C1PipelineRecord(
            timestamp=base_time + 1,
            navigation_executed=True,
            modeling_executed=True,
            latency_ms=4.8,
        ),
        C1PipelineRecord(
            timestamp=base_time + 2,
            navigation_executed=True,
            modeling_executed=False,  # priority=safety，禁止 modeling
            latency_ms=3.5,
        ),
        C1PipelineRecord(
            timestamp=base_time + 3,
            navigation_executed=True,
            modeling_executed=False,
            latency_ms=3.2,
        ),
        # suspended 时没有 pipeline 执行
        C1PipelineRecord(
            timestamp=base_time + 6,
            navigation_executed=True,
            modeling_executed=True,
            latency_ms=5.0,
        ),
    ]
    
    system_meta = C1SystemMeta(
        luna_id="luna_demo_001",
        version="v1.8.5",
        hardware="badge_v1",
        c1_policy_version="c1_policy_2024_12_19",
        start_timestamp=base_time,
        end_timestamp=base_time + 6,
    )
    
    return c1_records, pipeline_records, system_meta


def demo_factual_replay():
    """
    演示：事实回放
    """
    print("=" * 80)
    print("演示：事实回放（Factual Replay）")
    print("=" * 80)
    print()
    
    # 创建演示日志
    c1_records, pipeline_records, system_meta = create_demo_logs()
    
    # 回放
    engine = C1ReplayEngine()
    timeline = engine.replay_factual(
        c1_records=c1_records,
        pipeline_records=pipeline_records,
    )
    
    # 生成报告
    report = C1ReplayReport()
    report_text = report.generate_full_report(
        c1_records=c1_records,
        timeline=timeline,
        system_meta=system_meta,
    )
    
    print(report_text)


def demo_what_if_replay():
    """
    演示：假设回放
    """
    print("\n" + "=" * 80)
    print("演示：假设回放（What-if Replay）")
    print("=" * 80)
    print()
    
    # 创建演示日志
    c1_records, _, _ = create_demo_logs()
    
    # 假设：如果 motion_threshold 提高到 0.95（更宽松）
    override_policy = {
        "motion_threshold": 0.95,
    }
    
    engine = C1ReplayEngine()
    timeline = engine.replay_what_if(
        c1_records=c1_records,
        override_policy=override_policy,
    )
    
    print(f"覆盖策略: {override_policy}")
    print()
    
    report = C1ReplayReport()
    report_text = report.generate_timeline_view(timeline)
    print(report_text)


def demo_compare_replay():
    """
    演示：策略对比
    """
    print("\n" + "=" * 80)
    print("演示：策略对比（A/B Compare）")
    print("=" * 80)
    print()
    
    # 创建演示日志
    c1_records, _, _ = create_demo_logs()
    
    # 策略 A：motion_threshold = 0.85（当前策略）
    policy_a = {
        "name": "Policy A (当前)",
        "motion_threshold": 0.85,
    }
    
    # 策略 B：motion_threshold = 0.90（更宽松）
    policy_b = {
        "name": "Policy B (更宽松)",
        "motion_threshold": 0.90,
    }
    
    engine = C1ReplayEngine()
    comparison = engine.replay_compare(
        c1_records=c1_records,
        policy_a=policy_a,
        policy_b=policy_b,
    )
    
    print(f"{comparison['policy_a']['name']}:")
    print(f"  ModelingExecutor 执行占比: {comparison['policy_a']['stats']['modeling_execution_ratio']:.1%}")
    print(f"  视觉暂停占比: {comparison['policy_a']['stats']['suspended_ratio']:.1%}")
    print(f"  平均 fps: {comparison['policy_a']['stats']['avg_fps']:.1f}")
    
    print(f"\n{comparison['policy_b']['name']}:")
    print(f"  ModelingExecutor 执行占比: {comparison['policy_b']['stats']['modeling_execution_ratio']:.1%}")
    print(f"  视觉暂停占比: {comparison['policy_b']['stats']['suspended_ratio']:.1%}")
    print(f"  平均 fps: {comparison['policy_b']['stats']['avg_fps']:.1f}")
    
    print(f"\n对比结果:")
    print(f"  ModelingExecutor 执行占比差异: {comparison['comparison']['modeling_execution_diff']:+.1%}")
    print(f"  视觉暂停占比差异: {comparison['comparison']['suspended_time_diff']:+.1%}")


def main():
    """主函数"""
    print("=" * 80)
    print("C1 回访工具演示")
    print("=" * 80)
    print()
    print("这个演示展示了 C1 Replay Tool 的三种模式：")
    print("  1. 事实回放：完全复现当时发生了什么")
    print("  2. 假设回放：同一批日志，换规则跑")
    print("  3. 策略对比：同一输入，两套策略")
    print()
    
    demo_factual_replay()
    demo_what_if_replay()
    demo_compare_replay()
    
    print("\n" + "=" * 80)
    print("✅ 演示完成")
    print("=" * 80)
    print()
    print("📋 使用 CLI 工具:")
    print("  python c1_replay/replay_cli.py factual --c1-log logs/c1.log")
    print("  python c1_replay/replay_cli.py what-if --c1-log logs/c1.log --motion-threshold 0.90")
    print("  python c1_replay/replay_cli.py compare --c1-log logs/c1.log")
    print()


if __name__ == "__main__":
    main()


