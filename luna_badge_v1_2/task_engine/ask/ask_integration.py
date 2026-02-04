"""
AskIntegrationService: 封装 AskChainRuntime 的生命周期与上下文管理

TaskChainManager 只需要：
- 在任务启动时调用 maybe_start_for_task
- 在每轮对话时调用 step_if_active
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Dict, Optional, Any

from .ask_schema import AskSchema
from .ask_chain import AskChainBuilder
from .ask_runtime import AskChainRuntime, AskChainState
from .ask_manager import AskManager


@dataclass
class ActiveAskSession:
    """当前活跃的 Ask 会话状态"""
    task_id: str
    schema: AskSchema
    runtime: AskChainRuntime
    # 收集好的答案（但现在主要依赖 runtime.answers）
    answers: Dict[str, Any] = field(default_factory=dict)
    last_state: Optional[AskChainState] = None


@dataclass
class AskIntegrationResult:
    """
    统一给上层（TaskChainManager）看的结果对象。
    """
    consumed: bool              # 是否消费了本轮用户输入
    reply: Optional[str]        # 要回给用户的一句话（prompt / retry / 结束提示）
    done: bool                  # 这次 ask 是否已经完全结束
    aborted: bool               # 是否因策略中止（超限 / restart / abort）
    answers: Dict[str, Any]     # 已收集的 slot 填写结果（通常在 done=True 时有用）
    task_id: Optional[str] = None  # 关联的任务 ID（在 done=True 时有用）


class AskIntegrationService:
    """
    封装 AskChainRuntime 的生命周期与上下文管理。

    TaskChainManager 只需要：
    - 在任务启动时调用 maybe_start_for_task
    - 在每轮对话时调用 step_if_active
    """

    def __init__(self, ask_manager: Optional[AskManager] = None) -> None:
        self._ask_manager = ask_manager or AskManager()
        self._active: Optional[ActiveAskSession] = None

    # ==== 查询状态 ====

    @property
    def has_active(self) -> bool:
        return self._active is not None

    def current_task_id(self) -> Optional[str]:
        return self._active.task_id if self._active else None

    # ==== 生命周期管理 ====

    def clear(self) -> None:
        """清空当前活跃的 Ask 会话"""
        self._active = None

    # ==== 启动 Ask ====

    def maybe_start_for_task(
        self,
        task_id: str,
        task_meta: Dict[str, Any],
        now_ts: Optional[float] = None,
    ) -> Optional[AskIntegrationResult]:
        """
        若 task_meta 中存在 ask_schema，则启动 AskChainRuntime。

        否则返回 None，表示该任务没有 Ask 前置。

        Args:
            task_id: 任务 ID
            task_meta: 任务元数据，可能包含 ask_schema
            now_ts: 当前时间戳（秒级），如果为 None 则使用当前时间

        Returns:
            AskIntegrationResult 如果启动了 Ask，否则返回 None
        """
        if now_ts is None:
            now_ts = time.time()

        schema: Optional[AskSchema] = task_meta.get("ask_schema")
        if schema is None:
            return None

        # 构建 AskChainPlan + Runtime
        builder = AskChainBuilder()
        plan = builder.build_chain(schema)

        runtime = AskChainRuntime(
            plan=plan,
            ask_manager=self._ask_manager,
            retry_policy=schema.effective_retry_policy(),
        )

        session = ActiveAskSession(
            task_id=task_id,
            schema=schema,
            runtime=runtime,
        )
        self._active = session

        # 第一次 step：无用户输入，只出 prompt
        # 注意：实际接口是 user_input，不是 user_message
        result, state = runtime.step(user_input=None, now_ts=int(now_ts), context={})
        session.last_state = state

        # 从 runtime.answers 获取已收集的答案
        answers = getattr(runtime, "answers", {})
        if hasattr(runtime, "_answers"):
            answers = runtime._answers.copy()

        return AskIntegrationResult(
            consumed=True,
            reply=result.message,
            done=state.done,
            aborted=state.aborted or state.restarted,
            answers=answers,
            task_id=task_id,
        )

    # ==== 对话轮次驱动 ====

    def step_if_active(
        self,
        user_message: Optional[str],
        now_ts: Optional[float] = None,
    ) -> Optional[AskIntegrationResult]:
        """
        若当前存在 active ask，则推进其一步。

        若没有 active ask，则返回 None。

        Args:
            user_message: 用户输入文本（可为 None 或空字符串）
            now_ts: 当前时间戳（秒级），如果为 None 则使用当前时间

        Returns:
            AskIntegrationResult 如果存在 active ask，否则返回 None
        """
        if self._active is None:
            return None

        if now_ts is None:
            now_ts = time.time()

        runtime = self._active.runtime

        # 将空字符串视为 None（表示没有用户输入）
        # 但只有在首次调用时（current_node_id 为 None）才这样做
        # 否则保留空字符串，让 runtime.step 处理 retry 逻辑
        if user_message is not None and user_message.strip() == "":
            # 如果是首次调用（current_node_id 为 None），则视为 None
            if runtime.current_node_id is None:
                effective_user_input = None
            else:
                # 否则保留空字符串，触发 retry
                effective_user_input = user_message
        else:
            effective_user_input = user_message

        result, state = runtime.step(user_input=effective_user_input, now_ts=int(now_ts), context={})
        self._active.last_state = state

        # runtime.answers 是累积好的所有 slot 值
        answers = getattr(runtime, "answers", {})
        if hasattr(runtime, "_answers"):
            answers = runtime._answers.copy()

        # 未结束：继续停留在 Ask 模式
        if not state.done:
            return AskIntegrationResult(
                consumed=True,
                reply=result.message,
                done=False,
                aborted=False,
                answers=answers,
                task_id=self._active.task_id,
            )

        # 结束：记录结果后清空会话
        aborted = state.aborted or state.restarted
        final_answers = answers.copy()
        final_task_id = self._active.task_id
        self._active = None

        return AskIntegrationResult(
            consumed=True,
            reply=result.message,
            done=True,
            aborted=aborted,
            answers=final_answers,
            task_id=final_task_id,
        )

