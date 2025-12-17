"""
C-5 Expression Scheduler (一期收敛版 / Vision-Driven)

C-5 表达调度（一期收敛版）

NON-NEGOTIABLE RULES:

1. Vision is the only rhythm authority.
2. Expression must follow vision, never lead it.
3. GPS never affects expression timing.
4. No expression is emitted during visual TURNING unless critical.
5. This is a frozen v1.4.8 implementation. Do NOT extend features.

版本信息：
- 版本：C-5.v1.4.8.freeze
- 状态：一期封板（禁止功能扩展）
- 核心原则：视角主导一切
"""

# ======================================================================
# [1.4.X frozen] TURNING 状态下的 TTS 白名单（表达调度层）
#
# 在 1.4.X 生命周期内，TURNING（视觉转向/注意力占用）期间：
# - 非关键表达：必须 DROP（永不播报）
# - 关键表达（is_critical=True）：允许以 0ms 覆盖输出
#
# 该白名单语义由 schedule() 内 TURNING 兜底检查 + 规则表 critical_override 共同保证。
# 任何绕过/扩展该白名单的行为，属于 1.5+ 讨论范围。
# ======================================================================

import json
import os
import logging
from dataclasses import dataclass
from typing import Optional, Callable, Dict, Any, List
from .c5_types import VisionRhythmContext, ExpressionCandidate, VisionState
from .c5_queue import C5ExpressionQueue

logger = logging.getLogger(__name__)


@dataclass
class SchedulerRule:
    """调度规则"""
    rule_id: str
    allow: bool
    enqueue: bool = False
    delay_strategy: Optional[str] = None


class C5Scheduler:
    """
    C-5 表达调度器（一期收敛版）
    
    职责：
    1. 决定一句话是否允许输出
    2. 如果允许，决定"什么时候"输出
    3. 如果不合适，决定"丢弃 / 延迟 / 替换"
    
    禁止：
    - 不生成内容
    - 不修改语义
    - 不改导航 FSM
    - 不使用 GPS 作为节奏源
    - 不主动触发播报
    """
    
    def __init__(self, rules_file: Optional[str] = None):
        """
        初始化调度器
        
        Args:
            rules_file: 规则文件路径（可选）
        """
        if rules_file is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            rules_file = os.path.join(current_dir, "config", "c5_rules.json")
        
        self.rules_file = rules_file
        self.rules: List[Dict[str, Any]] = []
        self.queue = C5ExpressionQueue()
        self._last_vision_state: Optional[VisionState] = None
        self._load_rules()

    # ------------------------------------------------------------------
    # [v1.4.9 P0-2-B] Replay determinism support (state reset)
    # ------------------------------------------------------------------
    def reset(self) -> None:
        """
        重置调度器内部可变状态（仅用于 Replay / 测试）。

        约束：
        - 不改变任何调度语义/阈值/规则
        - 仅清空历史状态，避免“沿用上次运行的历史”
        """
        self.queue.flush(reason="replay_reset")
        self._last_vision_state = None
    
    def _load_rules(self):
        """加载规则"""
        try:
            with open(self.rules_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.rules = data.get("rules", [])
        except Exception as e:
            logger.error(f"Failed to load rules from {self.rules_file}: {e}")
            self.rules = []
    
    def _match_rule(
        self,
        expr: ExpressionCandidate,
        ctx: VisionRhythmContext
    ) -> Optional[SchedulerRule]:
        """
        匹配规则
        
        Args:
            expr: 表达式候选
            ctx: 视角节奏上下文
            
        Returns:
            Optional[SchedulerRule]: 匹配的规则，如果没有匹配则返回 None
        """
        for rule in self.rules:
            when = rule.get("when", {})
            then = rule.get("then", {})
            
            # 匹配 vision_state
            vision_state_match = False
            if "vision_state" in when:
                expected_states = when["vision_state"]
                if isinstance(expected_states, list):
                    vision_state_match = ctx.vision_state in expected_states
                else:
                    vision_state_match = ctx.vision_state == expected_states
            else:
                vision_state_match = True
            
            if not vision_state_match:
                continue
            
            # 匹配 urgency
            urgency_match = True
            if "urgency" in when:
                expected_urgency = when["urgency"]
                if isinstance(expected_urgency, list):
                    urgency_match = expr.urgency in expected_urgency
                else:
                    urgency_match = expr.urgency == expected_urgency
            
            if not urgency_match:
                continue
            
            # 匹配 is_critical
            critical_match = True
            if "is_critical" in when:
                expected_critical = when["is_critical"]
                if isinstance(expected_critical, bool):
                    critical_match = expr.is_critical == expected_critical
                else:
                    critical_match = True  # 如果规则中没有明确要求，则匹配
            
            if not critical_match:
                continue
            
            # 匹配成功，返回规则
            return SchedulerRule(
                rule_id=rule.get("id", "unknown"),
                allow=then.get("allow", True),
                enqueue=then.get("enqueue", False),
                delay_strategy=then.get("delay_strategy")
            )
        
        # 默认规则：允许输出，使用 vision_speed 延迟
        return SchedulerRule(
            rule_id="default",
            allow=True,
            enqueue=False,
            delay_strategy="vision_speed"
        )
    
    def compute_delay_ms(self, ctx: VisionRhythmContext) -> int:
        """
        计算延迟毫秒数（仅允许视角驱动）
        
        🚫 禁止出现任何固定大延迟（如 800ms）
        
        Args:
            ctx: 视角节奏上下文
            
        Returns:
            int: 延迟毫秒数
        """
        if ctx.vision_state in ("TURNING", "SEARCHING"):
            return 0
        
        speed = ctx.speed_mps
        
        if speed > 1.2:
            return 100
        elif speed > 0.5:
            return 200
        else:
            return 300
    
    def schedule(
        self,
        expr: ExpressionCandidate,
        ctx: VisionRhythmContext,
        emit_callback: Callable[[ExpressionCandidate, int], None]
    ) -> str:
        """
        调度表达式
        
        流程：
        1. 检查视觉状态变化，触发队列 flush
        2. 匹配规则
        3. 如果不允许输出，丢弃
        4. 如果视觉转弯且非关键，丢弃
        5. 计算延迟
        6. 如果入队，入队；否则立即输出
        
        Args:
            expr: 表达式候选
            ctx: 视角节奏上下文
            emit_callback: 输出回调函数 (expr, delay_ms)
            
        Returns:
            str: 调度结果（"EMIT" | "QUEUE" | "DROP"）
        """
        # 检查视觉状态变化，触发队列 flush
        if self._last_vision_state and self._last_vision_state != ctx.vision_state:
            self.queue.flush(reason="vision_state_change")
        
        self._last_vision_state = ctx.vision_state
        
        # 尝试替换（如果存在相同 contract_id 或 duplicate_key）
        if self.queue.replace(expr):
            self._log("QUEUE", ctx, 0, reason="replaced")
            return "QUEUE"
        
        # 匹配规则
        rule = self._match_rule(expr, ctx)
        
        if not rule or not rule.allow:
            self._log("DROP", ctx, 0, reason="rule_block")
            return "DROP"
        
        # --------------------------------------------------------------
        # [1.4.X frozen] TURNING 白名单兜底（不改逻辑，不改语义）
        #
        # TURNING 期间：仅允许 is_critical=True 的表达输出；
        # 其余一律 DROP（永不播报）。
        # --------------------------------------------------------------
        # 视觉转弯且非关键 → 丢弃（但关键表达可以覆盖，已在规则中处理）
        # 这里只做兜底检查，如果规则已经允许（如 critical_override），则跳过此检查
        if ctx.vision_state == "TURNING" and not expr.is_critical and rule.rule_id != "critical_override":
            self._log("DROP", ctx, 0, reason="vision_turning")
            return "DROP"
        
        # 计算延迟
        if rule.delay_strategy == "zero":
            delay_ms = 0
        elif rule.delay_strategy == "vision_speed":
            delay_ms = self.compute_delay_ms(ctx)
        else:
            delay_ms = self.compute_delay_ms(ctx)
        
        # 如果需要入队
        if rule.enqueue:
            # 尝试替换
            if not self.queue.replace(expr):
                self.queue.enqueue(expr)
            self._log("QUEUE", ctx, delay_ms, reason="enqueued")
            return "QUEUE"
        
        # 立即输出
        emit_callback(expr, delay_ms)
        self._log("EMIT", ctx, delay_ms, reason="vision_speed")
        return "EMIT"
    
    def _log(
        self,
        action: str,
        ctx: VisionRhythmContext,
        delay: int,
        reason: str
    ):
        """
        记录日志
        
        Args:
            action: 动作（EMIT | QUEUE | DROP）
            ctx: 视角节奏上下文
            delay: 延迟毫秒数
            reason: 原因
        """
        logger.info(
            f"[C5] action={action} "
            f"vision_state={ctx.vision_state} "
            f"speed={ctx.speed_mps:.2f} "
            f"delay={delay} "
            f"reason={reason}"
        )
    
    def process_queue(
        self,
        ctx: VisionRhythmContext,
        emit_callback: Callable[[ExpressionCandidate, int], None]
    ):
        """
        处理队列（当视觉状态允许时）
        
        Args:
            ctx: 视角节奏上下文
            emit_callback: 输出回调函数
        """
        # 只有在视觉稳定或锁定时才处理队列
        if ctx.vision_state not in ("STABLE", "LOCKED"):
            return
        
        expr = self.queue.peek()
        if expr:
            # 重新匹配规则
            rule = self._match_rule(expr, ctx)
            if rule and rule.allow:
                # 可以输出，出队
                # 注意：即使原本应该 enqueue，在当前稳定/锁定状态下也可以输出
                self.queue.dequeue()
                delay_ms = self.compute_delay_ms(ctx)
                emit_callback(expr, delay_ms)
                self._log("EMIT", ctx, delay_ms, reason="queue_processed")
