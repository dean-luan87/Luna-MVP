#!/usr/bin/env python3
"""
C1 Shadow Mode 测试脚本（完全独立版）

测试 C1 Shadow Controller 的观察能力，不控制系统。

运行方式：
    python examples/c1_shadow_mode_test_standalone.py
"""

import time

# 直接复制 C1ShadowController 的核心逻辑（避免导入问题）
MIN_FPS = 1
MAX_FPS = 5
MOTION_SCORE_THRESHOLD = 0.7
CLASS_C_PRIVATE = "force_camera_off"
LOG_INTERVAL_SEC = 0.5


class C1ShadowControllerStandalone:
    """C1 Shadow Controller（独立版）"""
    
    def __init__(self):
        self.last_log_time = 0.0
        self.last_fps_decision = None
        self.current_state = "STABLE"
        self.state_start_time = time.time()
    
    def observe(self, motion_score, frame_diff, scene_class="allow_camera", timestamp=None):
        if timestamp is None:
            timestamp = time.time()
        
        decisions = {}
        
        # Stability 判断
        if motion_score >= MOTION_SCORE_THRESHOLD:
            decisions["state"] = "SUSPEND"
        else:
            decisions["state"] = "STABLE"
        
        # 更新状态持续时间
        if decisions["state"] != self.current_state:
            self.current_state = decisions["state"]
            self.state_start_time = timestamp
        
        # 隐私判断
        if scene_class == CLASS_C_PRIVATE:
            decisions["camera_policy"] = "FORCE_OFF"
        else:
            decisions["camera_policy"] = "ALLOW"
        
        # 抽帧建议（不执行）
        suggested_fps = MIN_FPS
        if decisions["state"] == "STABLE" and decisions["camera_policy"] == "ALLOW":
            suggested_fps = min(MAX_FPS, 3)
        elif decisions["state"] == "SUSPEND":
            suggested_fps = 0
        
        decisions["suggested_fps"] = suggested_fps
        
        # 优先级建议（不执行）
        if decisions["state"] == "SUSPEND":
            decisions["suggested_priority"] = "safety"
        elif motion_score > 0.5:
            decisions["suggested_priority"] = "navigation"
        else:
            decisions["suggested_priority"] = "environment"
        
        # 日志节流
        if timestamp - self.last_log_time >= LOG_INTERVAL_SEC:
            self._log(decisions, timestamp, motion_score, frame_diff)
            self.last_log_time = timestamp
        
        self.last_fps_decision = suggested_fps
        return decisions
    
    def _log(self, decisions, timestamp, motion_score, frame_diff):
        state_duration = timestamp - self.state_start_time
        print(
            f"[C1-SHADOW][{timestamp:.2f}] "
            f"state={decisions['state']} "
            f"fps={decisions['suggested_fps']} "
            f"priority={decisions['suggested_priority']} "
            f"camera={decisions['camera_policy']} "
            f"motion={motion_score:.2f} "
            f"diff={frame_diff:.2f} "
            f"duration={state_duration:.1f}s"
        )


def simulate_motion_scenarios():
    """模拟不同的运动场景"""
    scenarios = [
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
    print("C1 Shadow Mode 测试（独立版）")
    print("=" * 70)
    print()
    print("⚠️  Shadow Mode 特点:")
    print("   - 只观察，不控制")
    print("   - 不影响 pipeline")
    print("   - 不执行任何决策")
    print()
    print("开始模拟场景...")
    print()
    
    shadow_controller = C1ShadowControllerStandalone()
    
    for i, (motion_score, frame_diff, scene_class) in enumerate(simulate_motion_scenarios()):
        timestamp = time.time()
        decisions = shadow_controller.observe(
            motion_score=motion_score,
            frame_diff=frame_diff,
            scene_class=scene_class,
            timestamp=timestamp,
        )
    
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


if __name__ == "__main__":
    main()


