from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .ask_schema import AskSchema, AskSlot, AskSlotKind
from .ask_node import AskNodeBase, StandardAskNode
from .retry_policy import RetryPolicy, OnExceedAction


@dataclass
class AskChainPlan:
    """
    AskChainPlan 描述了由 AskSchema 生成的一条"问询链"。

    - entry: 入口节点 ID
    - exit:  末尾节点 ID
    - nodes: 所有节点 ID（按执行顺序）
    - edges: 节点连线 (source_id, target_id)
    - ask_nodes: 节点 ID -> AskNode 实例映射
    - chain_timestamp: 本条问询链的时间戳（秒级）
    - task_id: 关联的任务 ID（用于日志与调试）
    """

    entry: str
    exit: str
    nodes: List[str]
    edges: List[Tuple[str, str]]
    ask_nodes: Dict[str, AskNodeBase]
    chain_timestamp: int
    task_id: str = field(default="")


class AskChainBuilder:
    """
    AskChainBuilder 根据 AskSchema 生成一条线性的问询链。

    1.4.6a 的设计目标：
    - 每个 AskSlot 对应一个 AskNode（1:1 映射）；
    - 节点 ID 统一为：
        {timestamp}_ask_{task_id}_{slot_name}
      其中 timestamp 为秒级整型；
    - 节点按 slot.kind 的优先级排序：
        REQUIRED → CLARIFY → OPTIONAL；
    - 同一 AskChain 内共享同一个 timestamp，便于追踪。

    当前版本仅关注"拓扑结构 + 节点 ID/实例映射"，
    重试/澄清/超限的实际调度由 AskManager / 上层 TaskChain 负责。
    """

    # kind 优先级：数值越小越优先
    _KIND_PRIORITY = {
        AskSlotKind.REQUIRED: 0,
        AskSlotKind.CLARIFY: 1,
        AskSlotKind.OPTIONAL: 2,
    }

    def __init__(self, default_retry_policy: Optional[RetryPolicy] = None) -> None:
        self._default_retry_policy = default_retry_policy or RetryPolicy.default()

    def _sort_slots(self, slots: List[AskSlot]) -> List[AskSlot]:
        """
        按优先级排序 slot，同时保持同一 kind 内的原始顺序（稳定排序）。
        """
        def key_fn(slot: AskSlot) -> int:
            return self._KIND_PRIORITY.get(slot.kind, 99)

        # sorted 默认是稳定排序
        return sorted(slots, key=key_fn)

    def _ensure_retry_policy_for_schema(self, schema: AskSchema) -> RetryPolicy:
        """
        根据 schema 和全局默认策略，确定本 AskChain 的有效 RetryPolicy。

        1.4.6a：沿用 AskSchema.effective_retry_policy 逻辑。
        未来可扩展为按 slot 定制。
        """
        return schema.effective_retry_policy(default_policy=self._default_retry_policy)

    def _build_node_id(self, chain_ts: int, task_id: str, slot_name: str) -> str:
        """
        统一构建 AskNode 节点 ID：
            {timestamp}_ask_{task_id}_{slot_name}
        """
        return f"{chain_ts}_ask_{task_id}_{slot_name}"

    def build_chain(
        self,
        schema: AskSchema,
        *,
        now_ts: Optional[int] = None,
    ) -> AskChainPlan:
        """
        从 AskSchema 构建一条线性的 AskChainPlan。

        now_ts:
            可选的时间戳（秒级）。如果未提供，则使用当前时间 time.time() 取整。
            这样可方便测试中控制 timestamp。
        """
        # 1) 决定本链的时间戳，所有节点共享
        chain_ts = int(now_ts if now_ts is not None else int(time.time()))

        # 2) 按 kind 优先级排序 slots
        slots_sorted = self._sort_slots(schema.slots)

        nodes: List[str] = []
        edges: List[Tuple[str, str]] = []
        ask_nodes: Dict[str, AskNodeBase] = {}

        # 3) 为每个 slot 生成节点 ID 和 StandardAskNode 实例
        prev_node_id: Optional[str] = None

        for slot in slots_sorted:
            node_id = self._build_node_id(chain_ts, schema.task_id, slot.name)
            nodes.append(node_id)
            ask_nodes[node_id] = StandardAskNode(slot=slot)

            if prev_node_id is not None:
                edges.append((prev_node_id, node_id))

            prev_node_id = node_id

        if not nodes:
            raise ValueError(f"AskSchema(task_id={schema.task_id}) has no slots, cannot build AskChain.")

        entry = nodes[0]
        exit_ = nodes[-1]

        return AskChainPlan(
            entry=entry,
            exit=exit_,
            nodes=nodes,
            edges=edges,
            ask_nodes=ask_nodes,
            chain_timestamp=chain_ts,
            task_id=schema.task_id,
        )












