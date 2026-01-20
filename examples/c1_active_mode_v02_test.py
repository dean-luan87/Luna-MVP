#!/usr/bin/env python3
"""
C1 Active Mode v0.2 测试脚本（完全独立版）

测试 C1 Active Mode v0.2 的状态机和 Protection Mode。

运行方式：
    python examples/c1_active_mode_v02_test.py
"""

import time
from collections import Counter

# 直接复制配置（避免导入问题）
MOTION_SCORE_THRESHOLD = 0.7
RECOVERY_MOTION_THRESHOLD = 0.3
RECOVERY_STABLE_TIME_SEC = 1.0
FRAME_DIFF_LOW_THRESHOLD = 0.05
FRAME_DIFF_HIGH_FREQ_COUNT = 5
PROTECTION_MODE_DURATION_SEC = 3.0


class C1StateMachineStandalone:
    """C1 状态机（独立版）"""
    
    def __init__(self):
        from enum import Enum
        
        class C1State(Enum):
            STABLE = "STABLE"
            SUSPENDED = "SUSPENDED"
            RECOVERING = "RECOVERING"
        
        self.C1State = C1State
        self.current_state = C1State.STABLE
        self.state_start_time = time.time()
        self.recovery_start_time = None
        self.recovery_stable_start_time = None
        
        # Protection Mode
        self.protection_mode_active = False
        self.protection_mode_start_time = None
        self.protection_trigger_reason = None
        self.low_diff_count = 0
        self.frame_diff_history = []
        self.high_freq_jump_count = 0
    
    def update(self, motion_score, frame_diff, timestamp):
        prev_state = self.current_state
        
        # Protection Mode
        protection_result = self._update_protection_mode(frame_diff, timestamp)
        if self.protection_mode_active:
            return {
                "state": self.C1State.SUSPENDED,
                "skip_modeling": True,
                "state_transition": None,
                "protection_trigger_reason": self.protection_trigger_reason,
                "protection_remaining_sec": max(0, PROTECTION_MODE_DURATION_SEC - (timestamp - self.protection_mode_start_time)),
            }
        
        # 状态转换
        if self.current_state == self.C1State.STABLE:
            if motion_score >= MOTION_SCORE_THRESHOLD:
                self.current_state = self.C1State.SUSPENDED
                self.state_start_time = timestamp
                return {
                    "state": self.C1State.SUSPENDED,
                    "skip_modeling": True,
                    "state_transition": "STABLE→SUSPENDED",
                    "protection_trigger_reason": None,
                    "protection_remaining_sec": None,
                }
        
        elif self.current_state == self.C1State.SUSPENDED:
            if motion_score < RECOVERY_MOTION_THRESHOLD:
                self.current_state = self.C1State.RECOVERING
                self.recovery_start_time = timestamp
                self.recovery_stable_start_time = timestamp
                self.state_start_time = timestamp
                return {
                    "state": self.C1State.RECOVERING,
                    "skip_modeling": True,
                    "state_transition": "SUSPENDED→RECOVERING",
                    "protection_trigger_reason": None,
                    "protection_remaining_sec": None,
                }
            else:
                return {
                    "state": self.C1State.SUSPENDED,
                    "skip_modeling": True,
                    "state_transition": None,
                    "protection_trigger_reason": None,
                    "protection_remaining_sec": None,
                }
        
        elif self.current_state == self.C1State.RECOVERING:
            if motion_score >= RECOVERY_MOTION_THRESHOLD:
                self.current_state = self.C1State.SUSPENDED
                self.recovery_start_time = None
                self.recovery_stable_start_time = None
                self.state_start_time = timestamp
                return {
                    "state": self.C1State.SUSPENDED,
                    "skip_modeling": True,
                    "state_transition": "RECOVERING→SUSPENDED",
                    "protection_trigger_reason": None,
                    "protection_remaining_sec": None,
                }
            else:
                if self.recovery_stable_start_time is None:
                    self.recovery_stable_start_time = timestamp
                
                stable_duration = timestamp - self.recovery_stable_start_time
                if stable_duration >= RECOVERY_STABLE_TIME_SEC:
                    self.current_state = self.C1State.STABLE
                    self.recovery_start_time = None
                    self.recovery_stable_start_time = None
                    self.state_start_time = timestamp
                    return {
                        "state": self.C1State.STABLE,
                        "skip_modeling": False,
                        "state_transition": "RECOVERING→STABLE",
                        "protection_trigger_reason": None,
                        "protection_remaining_sec": None,
                    }
                else:
                    return {
                        "state": self.C1State.RECOVERING,
                        "skip_modeling": True,
                        "state_transition": None,
                        "protection_trigger_reason": None,
                        "protection_remaining_sec": None,
                    }
        
        return {
            "state": self.C1State.STABLE,
            "skip_modeling": False,
            "state_transition": None,
            "protection_trigger_reason": None,
            "protection_remaining_sec": None,
        }
    
    def _update_protection_mode(self, frame_diff, timestamp):
        if self.protection_mode_active:
            if self.protection_mode_start_time is not None:
                elapsed = timestamp - self.protection_mode_start_time
                if elapsed >= PROTECTION_MODE_DURATION_SEC:
                    self.protection_mode_active = False
                    self.protection_mode_start_time = None
                    self.protection_trigger_reason = None
        
        # 静态遮挡检测
        if frame_diff < FRAME_DIFF_LOW_THRESHOLD:
            self.low_diff_count += 1
            if self.low_diff_count >= 10:
                if not self.protection_mode_active:
                    self.protection_mode_active = True
                    self.protection_mode_start_time = timestamp
                    self.protection_trigger_reason = "static_occlusion"
                    return {"triggered": True, "reason": "static_occlusion"}
        else:
            self.low_diff_count = 0
        
        # 频闪检测
        self.frame_diff_history.append(frame_diff)
        if len(self.frame_diff_history) > 10:
            self.frame_diff_history.pop(0)
        
        if len(self.frame_diff_history) >= 2:
            if abs(self.frame_diff_history[-1] - self.frame_diff_history[-2]) > 0.5:
                self.high_freq_jump_count += 1
            else:
                self.high_freq_jump_count = max(0, self.high_freq_jump_count - 1)
            
            if self.high_freq_jump_count >= FRAME_DIFF_HIGH_FREQ_COUNT:
                if not self.protection_mode_active:
                    self.protection_mode_active = True
                    self.protection_mode_start_time = timestamp
                    self.protection_trigger_reason = "flicker"
                    return {"triggered": True, "reason": "flicker"}
        
        return {"triggered": False, "reason": None}


def simulate_scenarios():
    """模拟不同的运动场景（包含阈值抖动、频闪、静态遮挡）"""
    scenarios = [
        # (场景名, motion_score, frame_diff, 持续时间)
        ("正常行走", 0.1, 0.05, 3),
        ("阈值附近抖动（0.65）", 0.65, 0.3, 3),
        ("阈值附近抖动（0.75）", 0.75, 0.4, 3),
        ("严重晃动", 0.9, 0.8, 2),
        ("恢复中（低运动）", 0.2, 0.1, 2),
        ("恢复完成", 0.1, 0.05, 2),
        ("高频闪烁（大幅 diff）", 0.1, 0.9, 3),  # 大幅跳变
        ("静态遮挡（持续低 diff）", 0.1, 0.01, 3),  # 持续低 diff
        ("正常恢复", 0.1, 0.05, 2),
    ]
    
    for scenario_name, motion_score, frame_diff, duration in scenarios:
        print(f"\n📋 场景: {scenario_name}")
        print(f"   motion_score={motion_score:.2f}, frame_diff={frame_diff:.2f}")
        
        for _ in range(duration * 2):  # 每 0.5 秒一次
            yield (motion_score, frame_diff)
            time.sleep(0.5)


def main():
    """主函数"""
    print("=" * 70)
    print("C1 Active Mode v0.2 测试（状态机 + Protection Mode）")
    print("=" * 70)
    print()
    print("⚠️  Active Mode v0.2 特点:")
    print("   - 状态机：STABLE / SUSPENDED / RECOVERING")
    print("   - Protection Mode：静态遮挡、频闪检测")
    print("   - 增强日志：state_transition, protection_trigger_reason")
    print()
    print("开始模拟场景...")
    print()
    
    state_machine = C1StateMachineStandalone()
    
    # 统计
    skip_count = 0
    total_count = 0
    state_transitions = []
    protection_triggers = []
    
    # 模拟场景
    for i, (motion_score, frame_diff) in enumerate(simulate_scenarios()):
        timestamp = time.time()
        total_count += 1
        
        # 状态机更新
        result = state_machine.update(motion_score, frame_diff, timestamp)
        
        # 统计
        if result["skip_modeling"]:
            skip_count += 1
        
        if result.get("state_transition"):
            state_transitions.append(result["state_transition"])
        
        if result.get("protection_trigger_reason"):
            protection_triggers.append(result["protection_trigger_reason"])
        
        # 日志
        log_parts = [
            f"[C1-ACTIVE][{timestamp:.2f}]",
            f"C1决策={'SKIP_MODELING' if result['skip_modeling'] else 'ALLOW_MODELING'}",
            f"实际执行={'NO' if result['skip_modeling'] else 'YES'}",
            f"状态={result['state'].value}",
        ]
        
        if result.get("state_transition"):
            log_parts.append(f"state_transition={result['state_transition']}")
        if result.get("protection_trigger_reason"):
            log_parts.append(f"protection_trigger_reason={result['protection_trigger_reason']}")
        if result.get("protection_remaining_sec") is not None:
            log_parts.append(f"protection_remaining_sec={result['protection_remaining_sec']:.1f}")
        
        print(" ".join(log_parts))
    
    print()
    print("=" * 70)
    print("✅ Active Mode v0.2 测试完成")
    print("=" * 70)
    print()
    print("📊 统计结果:")
    print(f"   SKIP 比例: {skip_count}/{total_count} ({skip_count/total_count*100:.1f}%)")
    print(f"   State 切换次数: {len(state_transitions)}")
    if state_transitions:
        transition_counter = Counter(state_transitions)
        print("   State 切换详情:")
        for transition, count in transition_counter.items():
            print(f"     - {transition}: {count} 次")
    print(f"   Protection 触发次数: {len(protection_triggers)}")
    if protection_triggers:
        protection_counter = Counter(protection_triggers)
        print("   Protection 触发详情:")
        for reason, count in protection_counter.items():
            print(f"     - {reason}: {count} 次")
    print()


if __name__ == "__main__":
    main()


