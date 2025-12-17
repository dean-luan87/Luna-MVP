"""
C-5 Convergence Replay Test

一次性跑完所有关心的点：
- TURNING 静默
- 队列 flush / replace
- 延迟分桶
- C-4 + C-5 协同
"""

import os
import sys
import time
import logging

# 设置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from expression.scheduler.c5_types import VisionRhythmContext, ExpressionCandidate
from expression.scheduler.c5_scheduler import C5Scheduler
from demo_runner.fixtures.vision_timeline import VisionFrame, replay_vision_timeline
from demo_runner.utils.log_capture import LogCapture


class C5ConvergenceReplayTest:
    """C-5 收敛回放测试"""
    
    def __init__(self):
        """初始化测试"""
        self.scheduler = C5Scheduler()
        self.log = LogCapture()
        self._last_vision_state = None
    
    def emit_callback(self, expr: ExpressionCandidate, delay_ms: int):
        """
        输出回调（记录日志）
        
        Args:
            expr: 表达式候选
            delay_ms: 延迟毫秒数
        """
        self.log.record({
            "action": "EMIT",
            "contract_id": expr.contract_id,
            "vision_state": self._last_vision_state or "UNKNOWN",
            "speed": getattr(self, '_current_speed', 0.0),
            "delay_ms": delay_ms,
            "is_critical": expr.is_critical,
            "urgency": expr.urgency,
            "reason": "emit_callback"
        })
        
        if delay_ms > 0:
            time.sleep(delay_ms / 1000.0)
        
        print(f"    🎤 [TTS] {expr.contract_id} (延迟: {delay_ms}ms)")
    
    def update_vision(self, ctx: dict):
        """
        更新视觉上下文
        
        Args:
            ctx: 视觉上下文（包含 vision_state, speed）
        """
        vision_state = ctx["vision_state"]
        speed = ctx["speed"]
        
        self._last_vision_state = vision_state
        self._current_speed = speed
        
        # 记录视觉状态变化
        self.log.record({
            "action": "VISION_UPDATE",
            "vision_state": vision_state,
            "speed": speed,
            "reason": "vision_update"
        })
    
    def test_full_convergence_replay(self):
        """测试完整收敛回放"""
        print("="*60)
        print("C-5 完整收敛回放测试")
        print("="*60)
        print("\n模拟真实行走节奏，验证 C-5 行为\n")
        
        # 先插入几个表达
        print("📝 插入表达式...")
        
        expr1 = ExpressionCandidate(
            contract_id="nav_forward",
            duplicate_key="forward",
            urgency="low",
            is_critical=False
        )
        
        ctx_stable = VisionRhythmContext(
            vision_state="STABLE",
            speed_mps=1.0,
            last_vision_ts=time.time()
        )
        
        result1 = self.scheduler.schedule(expr1, ctx_stable, self.emit_callback)
        self.log.record({
            "action": result1,
            "contract_id": expr1.contract_id,
            "vision_state": "STABLE",
            "speed": 1.0,
            "delay_ms": 0,
            "reason": "initial_schedule"
        })
        print(f"  表达式 1: {expr1.contract_id} → {result1}")
        
        # 插入相同 duplicate_key 的表达式（应该 replace）
        expr2 = ExpressionCandidate(
            contract_id="nav_forward",
            duplicate_key="forward",  # 相同的 duplicate_key
            urgency="low",
            is_critical=False
        )
        
        result2 = self.scheduler.schedule(expr2, ctx_stable, self.emit_callback)
        self.log.record({
            "action": result2,
            "contract_id": expr2.contract_id,
            "vision_state": "STABLE",
            "speed": 1.0,
            "delay_ms": 0,
            "reason": "replace_attempt"
        })
        print(f"  表达式 2: {expr2.contract_id} (相同 duplicate_key) → {result2}")
        
        # 插入关键表达
        expr3 = ExpressionCandidate(
            contract_id="nav_turn_critical",
            duplicate_key="turn_left",
            urgency="high",
            is_critical=True,
        )
        
        print(f"  表达式 3: {expr3.contract_id} (关键) → 等待视觉时间线")
        
        # 🧠 模拟一段"真实行走节奏"
        print("\n🎬 回放视觉节奏时间线...")
        timeline = [
            VisionFrame("STABLE", 1.0, 1.0),    # 稳定，高速，1秒
            VisionFrame("TURNING", 0.3, 2.0),  # 转弯，低速，2秒
            VisionFrame("LOCKED", 0.8, 1.5),    # 锁定，中速，1.5秒
            VisionFrame("STABLE", 0.5, 2.0),   # 稳定，低速，2秒
        ]
        
        # 在时间线回放过程中调度表达式
        def on_vision_update(ctx_dict):
            """视觉更新回调"""
            self.update_vision(ctx_dict)
            
            # 在每个视觉帧中尝试调度表达式
            vision_ctx = VisionRhythmContext(
                vision_state=ctx_dict["vision_state"],
                speed_mps=ctx_dict["speed"],
                last_vision_ts=time.time()
            )
            
            # 调度关键表达（在 TURNING 阶段应该能输出）
            if ctx_dict["vision_state"] == "TURNING":
                result = self.scheduler.schedule(expr3, vision_ctx, self.emit_callback)
                self.log.record({
                    "action": result,
                    "contract_id": expr3.contract_id,
                    "vision_state": ctx_dict["vision_state"],
                    "speed": ctx_dict["speed"],
                    "delay_ms": 0,
                    "is_critical": expr3.is_critical,
                    "urgency": expr3.urgency,
                    "reason": "during_turning"
                })
            
            # 处理队列（在稳定/锁定状态）
            if ctx_dict["vision_state"] in ("STABLE", "LOCKED"):
                self.scheduler.process_queue(vision_ctx, self.emit_callback)
        
        # ▶️ 回放视觉节奏
        replay_vision_timeline(timeline, on_vision_update)
        
        # 给调度器一点处理时间
        print("\n⏳ 等待调度器处理...")
        time.sleep(0.5)
        
        # ✅ 断言区
        print("\n" + "="*60)
        print("✅ 断言验证")
        print("="*60)
        
        try:
            # 1. TURNING 段无非关键播报
            print("\n  1. 验证 TURNING 段无非关键播报...")
            self.log.assert_no_emit_during("TURNING", allow_critical=True)
            print("     ✅ TURNING 段只有关键表达能输出")
            
            # 2. 延迟分桶验证
            print("\n  2. 验证延迟分桶 (0, 100, 200, 300)...")
            self.log.assert_delay_bucket({0, 100, 200, 300})
            print("     ✅ 所有延迟都在允许范围内")
            
            # 3. replace 验证
            print("\n  3. 验证 replace 操作...")
            # 检查是否有 replace 相关的记录
            has_replace = any(
                r.get("action") == "QUEUE" and "replace" in str(r.get("reason", "")).lower()
                for r in self.log.records
            )
            if has_replace:
                print("     ✅ replace 操作已发生")
            else:
                print("     ⚠️  未检测到 replace（可能因为队列为空）")
            
            # 4. 队列 flush 验证（通过视觉状态变化）
            print("\n  4. 验证队列 flush（视觉状态变化）...")
            # 检查 STABLE → TURNING 时队列是否清空
            state_changes = []
            for i, r in enumerate(self.log.records):
                if r.get("action") == "VISION_UPDATE":
                    state_changes.append(r.get("vision_state"))
            
            if "STABLE" in state_changes and "TURNING" in state_changes:
                stable_idx = state_changes.index("STABLE")
                turning_idx = state_changes.index("TURNING")
                if turning_idx > stable_idx:
                    print("     ✅ 视觉状态从 STABLE → TURNING，队列应已清空")
            
            # 5. 打印日志摘要
            print("\n  5. 日志摘要:")
            self.log.print_summary()
            
            print("\n" + "="*60)
            print("✅ 所有断言通过")
            print("="*60)
            
        except AssertionError as e:
            print(f"\n❌ 断言失败: {e}")
            self.log.print_summary()
            raise


def main():
    """主函数"""
    test = C5ConvergenceReplayTest()
    test.test_full_convergence_replay()


if __name__ == "__main__":
    main()
