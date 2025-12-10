from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

from .ask_chain import AskChainPlan
from .ask_manager import AskManager, AskSessionState
from .ask_node import AskNodeBase, AskNodeResult
from .retry_policy import RetryPolicy, OnExceedAction
from task_engine.tts import tts_manager
from task_engine.tts.router_facade import get_tts_router_facade


@dataclass
class AskChainState:
    """
    表示当前 AskChain 的运行状态。

    current_node_id:
        当前正在处理的节点 ID（None 表示链已结束或未开始）。

    done:
        True 表示整个链已完成（正常问完或策略性终止）。

    aborted:
        True 表示因为策略（如 ABORT）终止。

    restarted:
        True 表示策略要求重启整个链（ASK_RESTART）。

    extra:
        预留扩展字段（如 fallback_target, clarify_info 等）。
    """

    current_node_id: Optional[str]
    done: bool = False
    aborted: bool = False
    restarted: bool = False
    extra: Dict[str, Any] = field(default_factory=dict)


class AskChainRuntime:
    """
    AskChainRuntime 负责在"一个对话轮次"的粒度上驱动 AskChainPlan。

    设计理念：
    - 不直接处理 IO（语音/文本），只处理：
        - 当前节点 ID
        - 当前用户回复（可为空）
        - 当前时间（秒级时间戳）
    - 不关心外部 TaskChain 的细节，只负责：
        - 哪个 slot 该问；
        - 是否可以重试；
        - 是否链条应该结束 / 终止 / 重启。

    调用模式（伪代码）：

        runtime = AskChainRuntime(plan, ask_manager, retry_policy)

        # 第一次调用（没有用户输入，只是要给出第一个 prompt）
        result, state = runtime.step(user_input=None, now_ts=now)

        # 上层把 result.message 输出给用户，等待回答……

        # 用户回答后，再次调用：
        result, state = runtime.step(user_input="虹口医院", now_ts=now2)

        # 根据 state.current_node_id 是否为 None / state.done / state.aborted
        # 决定是否继续 ask 链或切回主任务。

    注意：
    - Runtime 只对"一个 AskChainPlan"负责；
    - 同一条链内所有节点共享一个 RetryPolicy（来自 AskSchema.effective_retry_policy）。
    """

    def __init__(
        self,
        plan: AskChainPlan,
        ask_manager: AskManager,
        retry_policy: Optional[RetryPolicy] = None,
    ) -> None:
        self._plan = plan
        self._ask_manager = ask_manager
        self._retry_policy = retry_policy or RetryPolicy.default()

        # 当前节点 ID，None 表示链还未开始或已结束。
        self._current_node_id: Optional[str] = None

        # 内部维护的 session 状态映射（node_id -> AskSessionState）
        self._sessions: Dict[str, AskSessionState] = {}
        
        # 答案收集
        self._answers: Dict[str, Any] = {}
        
        # 链状态（用于快速检查是否已完成/终止）
        self._state: AskChainState = AskChainState(
            current_node_id=None,
            done=False,
            aborted=False,
            restarted=False,
        )

    @property
    def plan(self) -> AskChainPlan:
        return self._plan

    @property
    def current_node_id(self) -> Optional[str]:
        return self._current_node_id
    
    @property
    def answers(self) -> Dict[str, Any]:
        """获取已收集的答案"""
        return self._answers.copy()

    def _get_ask_node(self, node_id: str) -> AskNodeBase:
        try:
            return self._plan.ask_nodes[node_id]
        except KeyError:
            raise KeyError(f"AskChainRuntime: node_id={node_id!r} not found in ask_nodes.")

    def _next_node_after(self, node_id: str) -> Optional[str]:
        """向后兼容的别名方法"""
        return self._next_node_id(node_id)

    def _next_node_id(self, current_node_id: str) -> Optional[str]:
        """
        根据 plan.nodes 的顺序找到下一个节点 ID。
        如果已经是最后一个，返回 None。
        """
        try:
            idx = self._plan.nodes.index(current_node_id)
        except ValueError:
            return None

        if idx + 1 >= len(self._plan.nodes):
            return None
        return self._plan.nodes[idx + 1]

    def _session_key_for_node(self, node_id: str) -> str:
        """
        用 node_id 作为 session slot_key，一条链内天然唯一。
        """
        return node_id

    def step(
        self,
        *,
        user_input: Optional[str],
        now_ts: int,
        context: Optional[Dict[str, Any]] = None,
    ) -> tuple[AskNodeResult, AskChainState]:
        """
        推进 AskChain 一步（核心状态机）。

        规则：
        - state.done / aborted / restarted 时，直接返回空结果；
        - user_input is None → 只生成当前节点的初始 prompt，不推进节点；
        - user_input 非空：
            - extract_answer.filled_value is None → 进入 retry/超限逻辑，不推进节点；
            - extract_answer.filled_value 有效 → 写入 answers，推进到下一个节点或结束。
        """
        # 0. 终止态保护
        if self._state.done or self._state.aborted or self._state.restarted:
            return AskNodeResult(filled_value=None, action="continue", message=None), self._state

        # 1) 如果当前还没开始，从 entry 起步
        if self._current_node_id is None:
            self._current_node_id = self._plan.entry
            self._state.current_node_id = self._current_node_id

        current_node_id = self._state.current_node_id
        if current_node_id is None:
            # 理论上不该出现，兜底标记为 done
            self._state.done = True
            return AskNodeResult(filled_value=None, action="continue", message=None), self._state

        # 1. 取当前节点 / 槽位
        ask_node = self._get_ask_node(current_node_id)
        slot = ask_node.slot
        slot_key = self._session_key_for_node(current_node_id)

        # 获取或初始化该节点的 retry 状态
        session_state = self._sessions.get(slot_key)
        if session_state is None:
            session_state = self._ask_manager.create_session(
                slot_id=slot_key,
                policy=self._retry_policy,
                now=now_ts,
            )
            self._sessions[slot_key] = session_state

        if context is None:
            context = {}

        # 2. 没有用户输入 → 输出首次 prompt
        if user_input is None:
            prompt = ask_node.build_prompt(context)
            # P5-3: 自动播报首次提问
            # Step 13: 使用统一入口
            if prompt:
                get_tts_router_facade().speak_task(prompt, meta={"stage": "ask_first"})
            state = AskChainState(current_node_id=current_node_id, done=False)
            self._state = state
            return AskNodeResult(filled_value=None, action="retry", message=prompt), state

        # 3. 有输入 → 先尝试解析
        filled_value = ask_node.extract_answer(user_input)

        # 3.1 解析失败 → retry / 超限，不推进节点
        if filled_value is None:
            policy = session_state.policy

            # 3.1.1 时间窗口检查
            if not self._ask_manager.should_retry_now(session_state, now=now_ts):
                retry_prompt = ask_node.build_retry_prompt(
                    retry_count=session_state.retry_count,
                    policy=policy,
                    context=context,
                )
                # P5-3: 自动播报 Retry 提示（时间窗口未到）
                # Step 13: 使用统一入口
                if retry_prompt:
                    get_tts_router_facade().speak_task(retry_prompt, meta={"stage": "ask_retry"})
                state = AskChainState(current_node_id=current_node_id, done=False)
                self._state = state
                return AskNodeResult(filled_value=None, action="retry", message=retry_prompt), state

            # 3.1.2 注册一次重试，内部会累加 retry_count，并根据 limit 标记 exceeded
            self._ask_manager.register_retry(session_state, now=now_ts)

            # 3.1.3 超限处理
            if session_state.exceeded:
                exceed_result = ask_node.decide_on_exceed(policy)
                action = exceed_result.action

                # P5-3: 根据超限策略自动播报
                # Step 13: 使用统一入口
                if action == "abort":
                    get_tts_router_facade().speak_task(
                        "对不起，我无法继续确认这个信息。",
                        meta={"stage": "ask_abort"},
                    )
                    self._state.aborted = True
                    self._state.done = True
                elif action == "fallback":
                    get_tts_router_facade().speak_task(
                        "我无法确认，但我会继续执行后续流程。",
                        meta={"stage": "ask_fallback"},
                    )
                    # 跳过此 slot
                    next_id = self._next_node_id(current_node_id)
                    self._state.current_node_id = next_id
                    self._current_node_id = next_id
                    if next_id is None:
                        self._state.done = True
                    return AskNodeResult(
                        filled_value=None,
                        action="fallback",
                        message=exceed_result.message,
                    ), self._state
                elif action == "clarify":
                    get_tts_router_facade().speak_task(
                        "让我再换一种方式确认你的意思。",
                        meta={"stage": "ask_clarify"},
                    )
                    # Clarify 行为等同于重新问
                    prompt = ask_node.build_prompt(context)
                    if prompt:
                        get_tts_router_facade().speak_task(prompt, meta={"stage": "ask_clarify_prompt"})
                    state = AskChainState(current_node_id=current_node_id, done=False)
                    self._state = state
                    return AskNodeResult(filled_value=None, action="clarify", message=prompt), state
                elif action == "restart":
                    get_tts_router_facade().speak_task(
                        "我们从头再来一次。",
                        meta={"stage": "ask_restart"},
                    )
                    # 重置状态（保持 done=True，restarted=True，由上层决定是否重新开始）
                    self._state.restarted = True
                    self._state.done = True
                    self._state.current_node_id = current_node_id
                    return exceed_result, self._state
                else:
                    # 其他策略暂时也视为终止，由上层决策
                    self._state.aborted = True
                    self._state.done = True

                self._state.current_node_id = current_node_id
                return exceed_result, self._state

            # 3.1.4 未超限 → 正常 retry，停留在当前节点
            retry_prompt = ask_node.build_retry_prompt(
                retry_count=session_state.retry_count,
                policy=policy,
                context=context,
            )
            # P5-3: 自动播报 Retry 提示
            # Step 13: 使用统一入口
            if retry_prompt:
                get_tts_router_facade().speak_task(retry_prompt, meta={"stage": "ask_retry"})
            state = AskChainState(current_node_id=current_node_id, done=False)
            self._state = state
            return AskNodeResult(filled_value=None, action="retry", message=retry_prompt), state

        # 3.2 解析成功 → 清理 retry 状态，写入答案，并推进节点
        self._ask_manager.reset_session(session_state, now=now_ts)
        if slot_key in self._sessions:
            del self._sessions[slot_key]

        # 保存答案
        self._answers[slot.name] = filled_value

        # 推进到下一个节点
        next_node_id = self._next_node_id(current_node_id)
        if next_node_id is None:
            # 已经走到最后一个节点
            # P5-3: AskChain 完成时 TTS
            # Step 13: 使用统一入口
            get_tts_router_facade().speak_task(
                "好的，我已确认所有需要的信息。",
                meta={"stage": "ask_done"},
            )
            self._current_node_id = None
            self._state.current_node_id = None
            self._state.done = True
            state = AskChainState(current_node_id=None, done=True)
            self._state = state
            return AskNodeResult(filled_value=filled_value, action="continue", message=None), state
        else:
            # 还有后续节点，切换到下一个
            self._current_node_id = next_node_id
            self._state.current_node_id = next_node_id
            next_prompt = self._get_ask_node(next_node_id).build_prompt(context)
            # P5-3: 自动播报下一条提问
            # Step 13: 使用统一入口
            if next_prompt:
                get_tts_router_facade().speak_task(next_prompt, meta={"stage": "ask_next"})
            state = AskChainState(current_node_id=next_node_id, done=False)
            self._state = state
            return AskNodeResult(filled_value=filled_value, action="continue", message=next_prompt), state

    def _decide_on_exceed(
        self,
        *,
        node_id: str,
        ask_node: AskNodeBase,
        policy: RetryPolicy,
    ) -> AskNodeResult:
        """
        触发超限策略时，委托 AskNode.decide_on_exceed，外加必要的链级语义。
        """
        base = ask_node.decide_on_exceed(policy)
        # 这里可以在 future 版本加入更多链级补充信息
        return base

