# core/query_engine/query_manager.py
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional, Dict
from core.flow_engine.flow_types import FlowContext


class QueryType:
    GOAL = "goal_disambiguation"
    CONTINUE = "continue_task"
    CANCEL = "cancel_confirm"
    SWITCH = "switch_task"
    NEXT = "next_task"


@dataclass
class PendingQuery:
    query_id: str
    user_id: str
    task_id: Optional[str]
    query_type: str
    message: str
    slot: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    retries: int = 0
    max_retries: int = 2
    answered: bool = False


@dataclass
class QueryConfig:
    max_retries: int = 2
    timeout_seconds: int = 20
    confirm_on_finish: bool = True


class QueryEngine:
    def __init__(self, config: Optional[QueryConfig] = None) -> None:
        self._config = config or QueryConfig()
        self._pending: Dict[str, PendingQuery] = {}
        self._user_active_query: Dict[str, str] = {}

    # --------------------------
    # 获取用户未完成问询
    # --------------------------
    def get_active_query(self, user_id: str) -> Optional[PendingQuery]:
        qid = self._user_active_query.get(user_id)
        if not qid:
            return None
        return self._pending.get(qid)

    # --------------------------
    # 创建问询
    # --------------------------
    def _create_query(self, user_id: str, task_id: Optional[str], query_type: str, message: str, slot: Optional[str] = None) -> PendingQuery:
        qid = uuid.uuid4().hex[:8]
        q = PendingQuery(
            query_id=qid,
            user_id=user_id,
            task_id=task_id,
            query_type=query_type,
            message=message,
            slot=slot
        )
        self._pending[qid] = q
        self._user_active_query[user_id] = qid
        return q

    # ---- 五类问询 -----
    def create_goal_query(self, user_id: str, raw_text: str) -> PendingQuery:
        return self._create_query(
            user_id, None, QueryType.GOAL,
            f"你刚才说的是\"{raw_text}\"，请再具体一点，你这次想做什么？",
            slot="goal_detail"
        )

    def create_continue_query(self, user_id: str, task_id: str, task_name: str = "刚才的任务") -> PendingQuery:
        return self._create_query(
            user_id, task_id, QueryType.CONTINUE,
            f"我们刚才还在进行{task_name}，你要继续吗？"
        )

    def create_cancel_query(self, user_id: str, task_id: str, task_name: str = "当前任务") -> PendingQuery:
        return self._create_query(
            user_id, task_id, QueryType.CANCEL,
            f"你是想停止{task_name}吗？"
        )

    def create_switch_query(self, user_id: str, task_id: str) -> PendingQuery:
        return self._create_query(
            user_id, task_id, QueryType.SWITCH,
            "你是要切换到一个新的目标吗？"
        )

    def create_next_query(self, user_id: str, task_name: str = "这个任务") -> PendingQuery:
        return self._create_query(
            user_id, None, QueryType.NEXT,
            f"{task_name}已经完成，你还需要我继续做些什么吗？"
        )

    # --------------------------
    # 关闭问询
    # --------------------------
    def close_query(self, query: PendingQuery) -> None:
        query.answered = True
        self._pending.pop(query.query_id, None)
        self._user_active_query.pop(query.user_id, None)

    # --------------------------
    # 保存回答到上下文
    # --------------------------
    def save_answer(self, ctx: FlowContext, slot: str, value: Any) -> None:
        ctx.data[slot] = value

    # --------------------------
    # 兼容 v1.4.5 的旧方法
    # --------------------------
    def should_ask_for_goal_disambiguation(self, ctx: FlowContext) -> bool:
        # 极简策略：如果 context 里没有 "goal_detail"，就认为需要澄清
        return "goal_detail" not in ctx.data

    def build_goal_question(self, ctx: FlowContext) -> str:
        raw = ctx.data.get("raw_utterance", "")
        return f"你刚才说的是：\"{raw}\"。请再具体一点，你这次的主要目标是什么？"

    def build_finish_confirmation(self, ctx: FlowContext) -> Optional[str]:
        if not self._config.confirm_on_finish:
            return None
        return "当前任务已经完成，你还需要我帮你做别的吗？"

    # --------------------------
    # v1.4.4 扩展问询协议
    # --------------------------
    def ask_continue(self, task_id: str) -> PendingQuery:
        """询问是否继续任务"""
        return self.create_continue_query(
            user_id="",  # 需要从上下文获取
            task_id=task_id,
            task_name=f"任务 {task_id}"
        )

    def ask_cancel(self, task_id: str) -> PendingQuery:
        """询问是否取消任务"""
        return self.create_cancel_query(
            user_id="",  # 需要从上下文获取
            task_id=task_id,
            task_name=f"任务 {task_id}"
        )

    def ask_switch(self, from_task_id: str, to_goal: str) -> PendingQuery:
        """询问是否切换任务"""
        return self.create_switch_query(
            user_id="",  # 需要从上下文获取
            task_id=from_task_id
        )

    def ask_next(self, next_goal: str) -> PendingQuery:
        """询问是否进入下一个目标"""
        return self.create_next_query(
            user_id="",  # 需要从上下文获取
            task_name=next_goal
        )
