"""
Vision-Driven Expression Scheduler (C-5 v2)

视角主导表达调度器

NON-NEGOTIABLE CORE RULE:

Vision is the primary clock of the system.

- Visual rhythm defines all timing decisions.
- Emotion can modulate, but never override.
- GPS is verification-only.
- Speech follows vision, never leads it.

Emotion Engine has NO authority over:
- delay time
- scheduling order
- interruption
- output triggering

⚠️ 任何实现不得违反以上规则，否则视为错误实现。

Where vision is, the system acts there.
Where vision pauses, the system waits.

职责边界：

C-5 只做三件事：
1. 决定一句话是否允许输出
2. 如果允许，决定"什么时候"输出
3. 如果不合适，决定"丢弃 / 延迟 / 替换"

C-5 明确不做的事：
- ❌ 不生成内容
- ❌ 不修改语义
- ❌ 不改导航 FSM
- ❌ 不使用 GPS 作为节奏源
- ❌ 不主动触发播报
"""

import time
from typing import Optional, Callable
import logging
from .vision_rhythm_context import VisionRhythmContext
from .rule_engine import RuleEngine, SchedulerDecision
from .delay_strategy import DelayStrategy, VisionAdaptiveDelayStrategy
from .expression_queue import ExpressionQueue
from .emotion.emotion_adapter import EmotionModulationAdapter
from .emotion.emotion_models import EmotionModulation
from ..calibration.expression_params import ExpressionParams

logger = logging.getLogger(__name__)


class VisionDrivenScheduler:
    """
    视角主导表达调度器（C-5 v2）
    
    这是 C-5 的核心模块，负责以视角为节奏源调度表达式输出。
    """
    
    def __init__(
        self,
        rule_engine: Optional[RuleEngine] = None,
        delay_strategy: Optional[DelayStrategy] = None,
        emotion_adapter: Optional[EmotionModulationAdapter] = None
    ):
        """
        初始化调度器
        
        Args:
            rule_engine: 规则引擎（可选，默认创建）
            delay_strategy: 延迟策略（可选，默认使用 VisionAdaptiveDelayStrategy）
            emotion_adapter: 情感适配器（可选，默认创建）
        """
        self.rule_engine = rule_engine or RuleEngine()
        self.delay_strategy = delay_strategy or VisionAdaptiveDelayStrategy()
        self.queue = ExpressionQueue()
        self._last_vision_state: Optional[str] = None
        
        # 情感适配器（可选依赖）
        self.emotion_adapter = emotion_adapter or EmotionModulationAdapter()
    
    def schedule_expression(
        self,
        expression: ExpressionParams,
        ctx: VisionRhythmContext,
        output_callback: Callable[[ExpressionParams], None],
        emotion_modulation: Optional[EmotionModulation] = None
    ) -> str:
        """
        调度表达式
        
        流程：
        1. 情感适配（如果提供）
        2. 规则引擎匹配
        3. 如果允许输出且不入队 → 计算延迟并输出（可能受情感调制）
        4. 如果允许输出且入队 → 入队
        5. 如果不允许输出 → 丢弃
        
        Args:
            expression: 表达参数
            ctx: 视角节奏上下文
            output_callback: 输出回调函数
            emotion_modulation: 情感调制（可选）
            
        Returns:
            str: 调度结果（"DROPPED" | "QUEUED" | "IMMEDIATE" | "DELAYED"）
        """
        # 1. 情感适配（失败自动回滚）
        emotion = None
        try:
            emotion = self.emotion_adapter.adapt(ctx, emotion_modulation)
        except Exception as e:
            logger.warning(f"Emotion adapter failed, fallback to vision-only mode: {e}")
            emotion = None
        # 检查视觉状态变化，触发队列 flush
        if self._last_vision_state and self._last_vision_state != ctx.vision_state:
            if ctx.is_vision_turning:
                self.queue.flush(reason="vision_state_change_to_turning")
        
        self._last_vision_state = ctx.vision_state
        
        # 丢弃过期的队列项
        self.queue.drop_if_outdated(ctx)
        
        # 规则引擎匹配
        decision = self.rule_engine.match(expression, ctx)
        
        # 如果不允许输出，丢弃
        if not decision.allow_output:
            return "DROPPED"
        
        # 情感抑制非必要表达（在入队之前检查）
        if emotion and emotion.verbosity_bias == "LESS":
            urgency = getattr(expression, 'urgency', 'normal')
            if urgency == "low":
                # 抑制低优先级表达
                return "DROPPED"
        
        # 如果需要入队
        if decision.enqueue:
            # 尝试替换相同合约的项
            contract_id = getattr(expression, 'contract_id', None)
            if not self.queue.replace_if_same_contract(expression, contract_id):
                self.queue.enqueue(expression)
            return "QUEUED"
        
        # 计算延迟（基于视觉）
        if decision.delay_ms is not None:
            base_delay = decision.delay_ms
        elif decision.delay_strategy:
            base_delay = self.delay_strategy.compute_delay_ms(ctx, expression)
        else:
            base_delay = 0
        
        # 情感调制延迟（只能做比例变化，不能直接决定延迟）
        delay_ms = self._apply_emotion_tempo_modulation(base_delay, emotion)
        
        # 传递语言风格给 C-3（如果需要）
        if emotion:
            setattr(expression, '_language_style', emotion.language_style)
        
        # 输出（延迟或立即）
        if delay_ms > 0:
            self._emit_after(delay_ms, expression, output_callback)
            return "DELAYED"
        else:
            output_callback(expression)
            return "IMMEDIATE"
    
    def _apply_emotion_tempo_modulation(
        self,
        base_delay_ms: int,
        emotion: Optional[EmotionModulation]
    ) -> int:
        """
        应用情感节奏调制
        
        只能做比例变化，不能直接决定延迟
        
        Args:
            base_delay_ms: 基于视觉的基础延迟（毫秒）
            emotion: 情感调制（可选）
            
        Returns:
            int: 调制后的延迟（毫秒）
        """
        if emotion is None:
            return base_delay_ms
        
        # 只允许比例调制
        if emotion.tempo_bias == "SLOWER":
            return int(base_delay_ms * 1.3)
        elif emotion.tempo_bias == "FASTER":
            return int(base_delay_ms * 0.7)
        else:  # NEUTRAL
            return base_delay_ms
    
    def _emit_after(
        self,
        delay_ms: int,
        expression: ExpressionParams,
        output_callback: Callable[[ExpressionParams], None]
    ):
        """
        延迟后输出
        
        Args:
            delay_ms: 延迟毫秒数
            expression: 表达参数
            output_callback: 输出回调函数
        """
        # 简化版：直接 sleep（一期）
        # 二期可以改为异步任务
        time.sleep(delay_ms / 1000.0)
        output_callback(expression)
    
    def process_queue(self, ctx: VisionRhythmContext, output_callback: Callable[[ExpressionParams], None]):
        """
        处理队列（当视觉状态允许时）
        
        Args:
            ctx: 视角节奏上下文
            output_callback: 输出回调函数
        """
        # 只有在视觉稳定或锁定时才处理队列
        if not (ctx.is_vision_stable or ctx.is_vision_locked):
            return
        
        # 处理队列头
        expr = self.queue.peek()
        if expr:
            decision = self.rule_engine.match(expr, ctx)
            if decision.allow_output:
                # 可以输出，出队
                # 注意：即使原本应该 enqueue，在当前稳定/锁定状态下也可以输出
                self.queue.dequeue()
                delay_ms = decision.delay_ms
                if delay_ms is None:
                    # 如果没有指定延迟，使用延迟策略
                    if decision.delay_strategy:
                        delay_ms = self.delay_strategy.compute_delay_ms(ctx, expr)
                    else:
                        delay_ms = 0
                
                if delay_ms > 0:
                    self._emit_after(delay_ms, expr, output_callback)
                else:
                    output_callback(expr)
