from __future__ import annotations

"""
PreCheckPiece

作用：
- 任务链正式启动前的预检查积木；
- 典型用途：确认用户是否准备出发、是否带好关键物品、当前环境是否允许执行任务等。

Hook：
- START_BEFORE：在整个 Flow 的起点之前执行。

当前版本（v1.4.5C-1）：
- 仅提供骨架与元数据，不实现具体业务逻辑。
"""

from typing import Any, Dict

from pieces.base_piece import TaskPiece, TaskPieceType
from patches.flow_patch import FlowPatch
from core.flow_engine.flow_types import FlowNode, FlowNodeType


HOOK_POINT_START_BEFORE = "START_BEFORE"


def _always_enabled(context: Any, env: Dict[str, Any]) -> bool:
    """条件：当前版本无条件启用。"""
    return True


def _build_pre_check_patch(context: Any, env: Dict[str, Any]) -> FlowPatch:
    """
    为当前流程插入一个"预检查节点"（占位实现）。
    后续在 C-3 中再补充具体实现。
    """
    node_id = "pre_check"
    node = FlowNode(
        id=node_id,
        node_type=FlowNodeType.CUSTOM,
        params={
            "action": "pre_check",
            "description": "任务链启动前的预检查（占位实现）",
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


def create_pre_check_piece() -> TaskPiece:
    """工厂函数：返回一个 PreCheckPiece 实例。"""
    return TaskPiece(
        id="pre_check_piece",
        hook_point=HOOK_POINT_START_BEFORE,
        piece_type=TaskPieceType.NODE,
        condition=_always_enabled,
        builder=_build_pre_check_patch,
        priority=30,
        description="在任务链启动前插入预检查节点的任务积木",
    )

