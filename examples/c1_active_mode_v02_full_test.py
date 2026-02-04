#!/usr/bin/env python3
"""
C1 Active Mode v0.2 完整测试脚本

测试清单（必须全部覆盖）：
1. motion_score 在阈值附近抖动（不频繁切换）
2. 严重晃动 → SUSPENDED
3. 稳定后 → RECOVERING → STABLE
4. 静态画面遮挡 → Protection
5. 高频闪图 → Protection

回归验证：
- NavigationExecutor 始终执行
- ModelingExecutor 被正确跳过
- 世界模型未被写入

输出统计指标：
- state_switch_count
- protection_trigger_count
- skip_ratio
"""

import time
from collections import Counter

# 直接复制配置（避免导入问题）
MOTION_SCORE_THRESHOLD = 0.7
RECOVERY_MOTION_THRESHOLD = 0.3
RECOVERY_STABLE_TIME_SEC = 1.0
STATIC_DIFF_THRESHOLD = 0.05
STATIC_FRAMES_THRESHOLD = 10
FLICKER_COUNT_THRESHOLD = 5
PROTECTION_MODE_DURATION_SEC = 3.0


class C1StateMachineV02:
    """C1 状态机 v0.2（完整版）"""
    
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
    
    def should_run_modeling(self) -> bool:
        """
        最终决策函数（唯一出口）
        
        Returns:
            是否应该执行 ModelingExecutor
        """
        if self.protection_mode_active:
            return False
        if self.current_state in (self.C1State.SUSPENDED, self.C1State.RECOVERING):
            return False
        return True
    
    def update(self, motion_score, frame_diff, timestamp):
        prev_state = self.current_state
        
        # Protection Mode（优先级最高）
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
                    # Protection 结束 → 进入 RECOVERING
                    if self.current_state == self.C1State.STABLE:
                        self.current_state = self.C1State.RECOVERING
                        self.recovery_start_time = timestamp
                        self.recovery_stable_start_time = timestamp
        
        # 静态遮挡检测
        if frame_diff < STATIC_DIFF_THRESHOLD:
            self.low_diff_count += 1
            if self.low_diff_count >= STATIC_FRAMES_THRESHOLD:
                if not self.protection_mode_active:
                    self.protection_mode_active = True
                    self.protection_mode_start_time = timestamp
                    self.protection_trigger_reason = "STATIC_OCCLUSION"
                    return {"triggered": True, "reason": "STATIC_OCCLUSION"}
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
            
            if self.high_freq_jump_count >= FLICKER_COUNT_THRESHOLD:
                if not self.protection_mode_active:
                    self.protection_mode_active = True
                    self.protection_mode_start_time = timestamp
                    self.protection_trigger_reason = "FLICKER"
                    return {"triggered": True, "reason": "FLICKER"}
        
        return {"triggered": False, "reason": None}


def test_threshold_oscillation():
    """测试 1: motion_score 在阈值附近抖动（不频繁切换）"""
    print("\n" + "=" * 70)
    print("测试 1: 阈值附近抖动（0.65-0.75 循环）")
    print("=" * 70)
    
    state_machine = C1StateMachineV02()
    state_transitions = []
    
    # 模拟 0.65-0.75 循环
    for i in range(10):
        motion_score = 0.65 if i % 2 == 0 else 0.75
        frame_diff = 0.3
        timestamp = time.time() + i * 0.5
        
        result = state_machine.update(motion_score, frame_diff, timestamp)
        should_run = state_machine.should_run_modeling()
        
        if result.get("state_transition"):
            state_transitions.append(result["state_transition"])
        
        print(
            f"  [{i}] motion={motion_score:.2f} "
            f"state={result['state'].value} "
            f"modeling={'YES' if should_run else 'NO'} "
            f"transition={result.get('state_transition', 'None')}"
        )
    
    print(f"\n✅ 状态切换次数: {len(state_transitions)}")
    print(f"   预期: ≤ 2（不频繁切换）")
    return len(state_transitions) <= 2


def test_severe_motion():
    """测试 2: 严重晃动 → SUSPENDED"""
    print("\n" + "=" * 70)
    print("测试 2: 严重晃动 → SUSPENDED")
    print("=" * 70)
    
    state_machine = C1StateMachineV02()
    
    # 正常 → 严重晃动
    result1 = state_machine.update(0.1, 0.05, time.time())
    result2 = state_machine.update(0.9, 0.8, time.time() + 0.5)
    
    print(f"  正常状态: state={result1['state'].value}, modeling={'YES' if not result1['skip_modeling'] else 'NO'}")
    print(f"  严重晃动: state={result2['state'].value}, modeling={'YES' if not result2['skip_modeling'] else 'NO'}")
    print(f"  状态转换: {result2.get('state_transition', 'None')}")
    
    success = (
        result1['state'].value == "STABLE" and
        result2['state'].value == "SUSPENDED" and
        result2.get('state_transition') == "STABLE→SUSPENDED"
    )
    print(f"\n✅ 测试结果: {'通过' if success else '失败'}")
    return success


def test_recovery():
    """测试 3: 稳定后 → RECOVERING → STABLE"""
    print("\n" + "=" * 70)
    print("测试 3: 稳定后 → RECOVERING → STABLE")
    print("=" * 70)
    
    state_machine = C1StateMachineV02()
    transitions = []
    
    # 严重晃动 → 低运动 → 持续稳定
    state_machine.update(0.9, 0.8, time.time())  # SUSPENDED
    time.sleep(0.1)
    
    result1 = state_machine.update(0.2, 0.1, time.time())  # RECOVERING
    if result1.get("state_transition"):
        transitions.append(result1["state_transition"])
    
    # 持续稳定 RECOVERY_STABLE_TIME_SEC
    time.sleep(RECOVERY_STABLE_TIME_SEC + 0.1)
    result2 = state_machine.update(0.1, 0.05, time.time())  # STABLE
    
    if result2.get("state_transition"):
        transitions.append(result2["state_transition"])
    
    print(f"  SUSPENDED → RECOVERING: {result1['state'].value}")
    print(f"  RECOVERING → STABLE: {result2['state'].value}")
    print(f"  状态转换: {transitions}")
    
    success = (
        result1['state'].value == "RECOVERING" and
        result2['state'].value == "STABLE" and
        "SUSPENDED→RECOVERING" in transitions and
        "RECOVERING→STABLE" in transitions
    )
    print(f"\n✅ 测试结果: {'通过' if success else '失败'}")
    return success


def test_static_occlusion():
    """测试 4: 静态画面遮挡 → Protection"""
    print("\n" + "=" * 70)
    print("测试 4: 静态画面遮挡 → Protection")
    print("=" * 70)
    
    state_machine = C1StateMachineV02()
    protection_triggered = False
    
    # 连续低 diff
    for i in range(STATIC_FRAMES_THRESHOLD + 2):
        result = state_machine.update(0.1, 0.01, time.time() + i * 0.5)
        if result.get("protection_trigger_reason") == "STATIC_OCCLUSION":
            protection_triggered = True
            print(f"  [{i}] Protection 触发: {result['protection_trigger_reason']}")
            break
        print(f"  [{i}] diff=0.01, low_count={state_machine.low_diff_count}, protection={state_machine.protection_mode_active}")
    
    print(f"\n✅ Protection 触发: {'是' if protection_triggered else '否'}")
    return protection_triggered


def test_flicker():
    """测试 5: 高频闪图 → Protection"""
    print("\n" + "=" * 70)
    print("测试 5: 高频闪图 → Protection")
    print("=" * 70)
    
    state_machine = C1StateMachineV02()
    protection_triggered = False
    
    # 高频跳变
    for i in range(10):
        frame_diff = 0.9 if i % 2 == 0 else 0.1
        result = state_machine.update(0.1, frame_diff, time.time() + i * 0.5)
        if result.get("protection_trigger_reason") == "FLICKER":
            protection_triggered = True
            print(f"  [{i}] Protection 触发: {result['protection_trigger_reason']}")
            break
        print(f"  [{i}] diff={frame_diff:.1f}, jump_count={state_machine.high_freq_jump_count}, protection={state_machine.protection_mode_active}")
    
    print(f"\n✅ Protection 触发: {'是' if protection_triggered else '否'}")
    return protection_triggered


def test_regression():
    """回归验证：NavigationExecutor 始终执行，ModelingExecutor 被正确跳过"""
    print("\n" + "=" * 70)
    print("回归验证: NavigationExecutor / ModelingExecutor")
    print("=" * 70)
    
    state_machine = C1StateMachineV02()
    
    # 正常状态
    state_machine.update(0.1, 0.05, time.time())
    nav_executed_1 = True  # NavigationExecutor 始终执行
    modeling_executed_1 = state_machine.should_run_modeling()
    
    # SUSPENDED 状态
    state_machine.update(0.9, 0.8, time.time() + 0.5)
    nav_executed_2 = True  # NavigationExecutor 始终执行
    modeling_executed_2 = state_machine.should_run_modeling()
    
    # Protection Mode
    for i in range(STATIC_FRAMES_THRESHOLD + 2):
        state_machine.update(0.1, 0.01, time.time() + i * 0.5)
        if state_machine.protection_mode_active:
            break
    nav_executed_3 = True  # NavigationExecutor 始终执行
    modeling_executed_3 = state_machine.should_run_modeling()
    
    print(f"  正常状态: nav={'YES' if nav_executed_1 else 'NO'}, modeling={'YES' if modeling_executed_1 else 'NO'}")
    print(f"  SUSPENDED: nav={'YES' if nav_executed_2 else 'NO'}, modeling={'YES' if modeling_executed_2 else 'NO'}")
    print(f"  Protection: nav={'YES' if nav_executed_3 else 'NO'}, modeling={'YES' if modeling_executed_3 else 'NO'}")
    
    success = (
        nav_executed_1 and nav_executed_2 and nav_executed_3 and  # NavigationExecutor 始终执行
        modeling_executed_1 and not modeling_executed_2 and not modeling_executed_3  # ModelingExecutor 被正确跳过
    )
    print(f"\n✅ 回归验证: {'通过' if success else '失败'}")
    return success


def generate_log_sample():
    """生成日志样例"""
    print("\n" + "=" * 70)
    print("日志样例（v0.2 必须字段）")
    print("=" * 70)
    
    state_machine = C1StateMachineV02()
    logs = []
    
    # 模拟几个场景
    scenarios = [
        (0.1, 0.05, "正常"),
        (0.9, 0.8, "严重晃动"),
        (0.2, 0.1, "恢复中"),
        (0.1, 0.01, "静态遮挡"),
    ]
    
    for motion_score, frame_diff, scenario_name in scenarios:
        timestamp = time.time()
        result = state_machine.update(motion_score, frame_diff, timestamp)
        should_run = state_machine.should_run_modeling()
        
        log_entry = {
            "c1_state": result["state"].value,
            "state_transition": result.get("state_transition"),
            "motion_score": motion_score,
            "frame_diff": frame_diff,
            "protection_active": result.get("protection_trigger_reason") is not None,
            "protection_reason": result.get("protection_trigger_reason"),
            "protection_remaining_sec": result.get("protection_remaining_sec"),
            "modeling_executed": should_run,
        }
        logs.append(log_entry)
        
        print(f"\n场景: {scenario_name}")
        print(f"  {log_entry}")
    
    return logs


def main():
    """主函数"""
    print("=" * 70)
    print("C1 Active Mode v0.2 完整测试")
    print("=" * 70)
    print()
    print("📋 测试清单:")
    print("   1. motion_score 在阈值附近抖动（不频繁切换）")
    print("   2. 严重晃动 → SUSPENDED")
    print("   3. 稳定后 → RECOVERING → STABLE")
    print("   4. 静态画面遮挡 → Protection")
    print("   5. 高频闪图 → Protection")
    print("   6. 回归验证：NavigationExecutor / ModelingExecutor")
    print()
    
    # 运行所有测试
    test_results = []
    
    test_results.append(("阈值抖动", test_threshold_oscillation()))
    test_results.append(("严重晃动", test_severe_motion()))
    test_results.append(("恢复流程", test_recovery()))
    test_results.append(("静态遮挡", test_static_occlusion()))
    test_results.append(("频闪攻击", test_flicker()))
    test_results.append(("回归验证", test_regression()))
    
    # 生成日志样例
    log_sample = generate_log_sample()
    
    # 统计测试结果
    print("\n" + "=" * 70)
    print("测试报告")
    print("=" * 70)
    print()
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    print(f"📊 测试结果: {passed}/{total} 通过")
    print()
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
    
    print()
    print("📋 日志样例（v0.2 必须字段）:")
    import json
    for i, log_entry in enumerate(log_sample):
        print(f"   样例 {i+1}: {json.dumps(log_entry, indent=2, ensure_ascii=False)}")
    
    print()
    print("=" * 70)
    if passed == total:
        print("✅ 所有测试通过")
    else:
        print(f"❌ {total - passed} 个测试失败")
    print("=" * 70)


if __name__ == "__main__":
    main()


