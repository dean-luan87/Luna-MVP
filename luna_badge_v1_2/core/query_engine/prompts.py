# core/query_engine/prompts.py
"""
问询文案模板（多场景）
"""

from typing import Dict, Any
from ..flow_engine.flow_types import FlowContext


class QueryPrompts:
    """问询文案模板集合."""

    @staticmethod
    def goal_disambiguation(ctx: FlowContext) -> str:
        """目标澄清问句."""
        intent = ctx.intent
        if "hospital" in intent.lower():
            return "请问你要去哪个医院？"
        elif "toilet" in intent.lower():
            return "请问你要去哪个洗手间？"
        else:
            return "请问你的具体目标是什么？"

    @staticmethod
    def confirm_destination(ctx: FlowContext) -> str:
        """确认目的地."""
        destination = ctx.data.get("destination", "那里")
        return f"确认要去 {destination} 吗？"

    @staticmethod
    def need_help(ctx: FlowContext) -> str:
        """是否需要帮助."""
        return "需要我帮你导航吗？"

    @staticmethod
    def custom_prompt(template: str, variables: Dict[str, Any]) -> str:
        """自定义模板."""
        return template.format(**variables)

