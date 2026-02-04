"""
Rule Engine

规则引擎（表驱动）
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from .vision_rhythm_context import VisionRhythmContext
from ..calibration.expression_params import ExpressionParams
import json
import os


@dataclass
class SchedulerDecision:
    """
    调度决策
    
    - allow_output: 是否允许输出
    - enqueue: 是否入队
    - delay_ms: 延迟毫秒数（如果指定）
    - delay_strategy: 延迟策略名称（如果指定）
    - reason: 原因
    """
    allow_output: bool
    enqueue: bool = False
    delay_ms: Optional[int] = None
    delay_strategy: Optional[str] = None
    reason: str = ""


class RuleEngine:
    """
    规则引擎
    
    基于 JSON 配置文件的表驱动规则引擎
    """
    
    def __init__(self, rules_file: Optional[str] = None):
        """
        初始化规则引擎
        
        Args:
            rules_file: 规则文件路径（可选）
        """
        if rules_file is None:
            # 默认路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            rules_file = os.path.join(current_dir, "config", "vision_scheduler_rules.json")
        
        self.rules_file = rules_file
        self.rules: List[Dict[str, Any]] = []
        self._load_rules()
    
    def _load_rules(self):
        """加载规则"""
        try:
            with open(self.rules_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.rules = data.get("rules", [])
        except FileNotFoundError:
            # 如果没有文件，使用默认规则
            self.rules = self._default_rules()
        except Exception as e:
            print(f"Warning: Failed to load rules from {self.rules_file}: {e}")
            self.rules = self._default_rules()
    
    def _default_rules(self) -> List[Dict[str, Any]]:
        """
        默认规则（硬编码）
        
        Returns:
            List[Dict[str, Any]]: 默认规则列表
        """
        return [
            {
                "id": "vision_turning_block_all",
                "when": {
                    "vision_state": "TURNING"
                },
                "then": {
                    "allow_output": False,
                    "reason": "vision_turning"
                }
            },
            {
                "id": "vision_locked_high_priority",
                "when": {
                    "vision_state": "LOCKED",
                    "urgency": "high"
                },
                "then": {
                    "allow_output": True,
                    "delay_ms": 0,
                    "enqueue": False
                }
            },
            {
                "id": "vision_stable_low_priority",
                "when": {
                    "vision_state": "STABLE",
                    "urgency": "low"
                },
                "then": {
                    "allow_output": True,
                    "enqueue": True,
                    "delay_strategy": "vision_adaptive"
                }
            },
            {
                "id": "vision_unstable_block",
                "when": {
                    "vision_state": "UNSTABLE"
                },
                "then": {
                    "allow_output": False,
                    "reason": "vision_unstable"
                }
            }
        ]
    
    def match(
        self,
        expression: ExpressionParams,
        ctx: VisionRhythmContext
    ) -> SchedulerDecision:
        """
        匹配规则
        
        Args:
            expression: 表达参数
            ctx: 视角节奏上下文
            
        Returns:
            SchedulerDecision: 调度决策
        """
        # 按顺序匹配规则，返回第一个匹配的
        for rule in self.rules:
            if self._match_condition(rule.get("when", {}), expression, ctx):
                return self._build_decision(rule.get("then", {}))
        
        # 默认决策：允许输出，使用自适应延迟
        return SchedulerDecision(
            allow_output=True,
            enqueue=False,
            delay_strategy="vision_adaptive",
            reason="default"
        )
    
    def _match_condition(
        self,
        condition: Dict[str, Any],
        expression: ExpressionParams,
        ctx: VisionRhythmContext
    ) -> bool:
        """
        匹配条件
        
        Args:
            condition: 条件字典
            expression: 表达参数
            ctx: 视角节奏上下文
            
        Returns:
            bool: True 表示匹配
        """
        # 匹配 vision_state
        if "vision_state" in condition:
            if ctx.vision_state != condition["vision_state"]:
                return False
        
        # 匹配 urgency
        if "urgency" in condition:
            urgency = getattr(expression, 'urgency', 'normal')
            if urgency != condition["urgency"]:
                return False
        
        # 匹配 visual_confidence
        if "visual_confidence_min" in condition:
            if ctx.visual_confidence < condition["visual_confidence_min"]:
                return False
        
        # 匹配 speed
        if "speed_max" in condition:
            if ctx.speed_mps > condition["speed_max"]:
                return False
        
        return True
    
    def _build_decision(self, then_clause: Dict[str, Any]) -> SchedulerDecision:
        """
        构建决策
        
        Args:
            then_clause: then 子句
            
        Returns:
            SchedulerDecision: 调度决策
        """
        return SchedulerDecision(
            allow_output=then_clause.get("allow_output", True),
            enqueue=then_clause.get("enqueue", False),
            delay_ms=then_clause.get("delay_ms"),
            delay_strategy=then_clause.get("delay_strategy"),
            reason=then_clause.get("reason", "matched_rule")
        )
