from __future__ import annotations

"""
HumanAssistPiece

作用：
- 在系统认为"机器能力可能不足"或"人工协助更高效"的位置，
  主动插入引导用户寻求工作人员/旁人帮助的步骤；
- 典型场景：医院复杂挂号、政府大厅窗口分流、异常导航环境等。

Hook：
- HELP_BEFORE：在特定关键节点前触发人工协助建议。

当前版本（v1.4.5C-1）：
- 仅提供骨架与元数据，不实现具体业务逻辑。
"""

from typing import Any, Dict

from pieces.base_piece import TaskPiece, TaskPieceType
from patches.flow_patch import FlowPatch
from core.flow_engine.flow_types import FlowNode, FlowNodeType


HOOK_POINT_HELP_BEFORE = "HELP_BEFORE"


def _always_enabled(context: Any, env: Dict[str, Any]) -> bool:
    """条件：当前版本无条件启用。"""
    return True


def _build_human_assist_patch(context: Any, env: Dict[str, Any]) -> FlowPatch:
    """
    为当前流程插入一个"人工协助引导节点"（占位实现）。
    后续在 C-3 中再补充具体实现。
    """
    node_id = "human_assist"
    node = FlowNode(
        id=node_id,
        node_type=FlowNodeType.CUSTOM,
        params={
            "action": "human_assist",
            "description": "人工协助引导（占位实现）",
        },
    )
    patch = FlowPatch(
        new_nodes={node_id: node},
        new_edges=[],
        delete_nodes=[],
        rewire_entry=None,
        rewire_exit=None,
    )
    return patch


def create_human_assist_piece() -> TaskPiece:
    """工厂函数：返回一个 HumanAssistPiece 实例。"""
    return TaskPiece(
        id="human_assist_piece",
        hook_point=HOOK_POINT_HELP_BEFORE,
        piece_type=TaskPieceType.NODE,
        condition=_always_enabled,
        builder=_build_human_assist_patch,
        priority=25,
        description="在关键节点前插入人工协助引导节点的任务积木",
    )

