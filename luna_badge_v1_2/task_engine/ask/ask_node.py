from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

from .ask_schema import AskSlot
from .retry_policy import RetryPolicy, OnExceedAction


@dataclass
class AskNodeResult:
    """
    标准化的 Ask 节点执行结果。

    对上游（TaskChain / DecisionCore）暴露统一结构：

    - filled_value: 用户填入的值（若成功解析）

    - action: 控制行为标记：
        - "continue": 正常进入下一个节点
        - "retry": 需要再次追问
        - "fallback": 交给人工/其他模块
        - "clarify": 进入澄清链
        - "restart": 重新开始整个问询
        - "abort": 终止当前任务链

    - message: 要输出给用户的提示文本（由上层渲染为 TTS / 文本）
    """

    filled_value: Optional[Any]
    action: str
    message: Optional[str] = None


class AskNodeBase(ABC):
    """
    Ask 节点抽象基类。

    设计目标：
    - 统一问询型节点的执行接口；
    - 与 RetryPolicy / AskManager 配合；
    - 保持对 TaskChain/FlowEngine 的解耦。
    """

    def __init__(self, slot: AskSlot) -> None:
        self.slot = slot

    @abstractmethod
    def build_prompt(self, context: Mapping[str, Any]) -> str:
        """
        构建用于"第一次提问"的提示语。

        context:
            上下文信息（通常是 dict），由上层传入。
        """
        raise NotImplementedError

    @abstractmethod
    def extract_answer(self, user_text: str) -> Optional[Any]:
        """
        从用户的自然语言回复中提取有用值。

        返回：
        - 非 None: 视为解析成功，进入 filled_value 流程；
        - None: 视为解析失败，由上层决定是否 retry。
        """
        raise NotImplementedError

    def build_retry_prompt(
        self,
        *,
        retry_count: int,
        policy: RetryPolicy,
        context: Optional[Mapping[str, Any]] = None,
    ) -> str:
        """
        当需要追问时，构建新的提示文案。

        默认策略：
        - 在原 prompt 基础上增加"再确认一次"等提示。
        - 上层可以按需要替换 / 扩展此行为。
        """
        base_prompt = None
        if context is None:
            context = {}
        try:
            base_prompt = self.build_prompt(context)
        except Exception:
            # 如果 build_prompt 有问题，退回到最简单文案
            base_prompt = self.slot.prompt_template or f"请再告诉我一次：{self.slot.name}"

        return f"不好意思，我再确认一次：{base_prompt}"

    def decide_on_exceed(self, policy: RetryPolicy) -> AskNodeResult:
        """
        当超过重试上限时，根据 policy.on_exceed 决定控制行为。
        """
        action_map = {
            OnExceedAction.FALLBACK: "fallback",
            OnExceedAction.CLARIFY: "clarify",
            OnExceedAction.ASK_RESTART: "restart",
            OnExceedAction.ABORT: "abort",
        }
        action = action_map.get(policy.on_exceed, "abort")
        message = None

        if action == "abort":
            message = "多次尝试仍未获取到关键信息，本次任务将结束。"
        elif action == "fallback":
            message = "我这边暂时无法确认信息，将为你切换到人工或其他协助方式。"
        elif action == "clarify":
            message = "当前信息有些模糊，我会尝试通过澄清流程再确认一次。"
        elif action == "restart":
            message = "我们从头再梳理一次关键信息。"

        return AskNodeResult(filled_value=None, action=action, message=message)


class StandardAskNode(AskNodeBase):
    """
    标准问询节点实现，适用于大多数简单槽位。

    特点：
    - 使用 AskSlot.prompt_template 作为主提示；
    - 若 prompt_template 为空，则退回通用提示；
    - extract_answer 默认返回原文（去除首尾空白），空串视为失败。
    """

    def build_prompt(self, context: Mapping[str, Any]) -> str:
        """
        构建一次正常提问的文案。
        """
        template = self.slot.prompt_template

        if not template:
            # 通用兜底
            return f"请告诉我 {self.slot.name}。"

        # 支持简单的 str.format(**context) 占位符替换
        try:
            return template.format(**context)
        except Exception:
            # 格式化失败时，退回原模板，避免中断流程
            return template

    def extract_answer(self, user_text: str) -> Optional[Any]:
        """
        默认实现：只要有非空内容，就视为有效回答。
        具体结构化解析可以在后续版本或特化子类中实现。
        """
        if user_text is None:
            return None
        value = user_text.strip()
        if not value:
            return None
        return value












