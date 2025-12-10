# patches/flow_patch.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

try:
    # 避免在还没实现这些类型时报错，只作为类型提示使用
    from core.flow_engine.flow_types import FlowNode, FlowEdge
except Exception:  # pragma: no cover
    FlowNode = object  # type: ignore
    FlowEdge = object  # type: ignore


@dataclass
class FlowPatch:
    """
    FlowPatch 表示针对一个 FlowDefinition 的"局部修改集"。

    典型用途：
    - 注入新的节点/边（扩展任务链）
    - 删除部分节点（剪裁任务链）
    - 重接入口/出口（替换或绕过某些子流程）
    """
    new_nodes: Dict[str, FlowNode] = field(default_factory=dict)
    new_edges: List[FlowEdge] = field(default_factory=list)

    # 需要删除的节点 ID 列表（剪枝用）
    delete_nodes: List[str] = field(default_factory=list)

    # 如果需要替换某段子流程，可以指定新的入口/出口节点
    rewire_entry: Optional[str] = None
    rewire_exit: Optional[str] = None
