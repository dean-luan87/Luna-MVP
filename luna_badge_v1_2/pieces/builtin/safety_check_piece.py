from __future__ import annotations

"""
SafetyCheckPiece

作用：
- 在关键步骤前插入安全相关的检查逻辑；
- 如：进入车流密集区域前、靠近施工区域前，附加一层安全检查。

Hook：
- SAFETY_BEFORE：安全相关节点前。

当前版本（v1.4.5C-1）：
- 仅提供骨架与元数据，不实现具体业务逻辑。
"""

from typing import Any, Dict

from pieces.base_piece import TaskPiece, TaskPieceType
from patches.flow_patch import FlowPatch
from core.flow_engine.flow_types import FlowNode, FlowNodeType


HOOK_POINT_SAFETY_BEFORE = "SAFETY_BEFORE"


def _always_enabled(context: Any, env: Dict[str, Any]) -> bool:
    """条件：当前版本无条件启用。"""
    return True


def _build_safety_check_patch(context: Any, env: Dict[str, Any]) -> FlowPatch:
    """
    为当前流程插入一个"安全检查节点"（占位实现）。
    后续在 C-3 中再补充具体实现。
    """
    node_id = "safety_check"
    node = FlowNode(
        id=node_id,
        node_type=FlowNodeType.CUSTOM,
        params={
            "action": "safety_check",
            "description": "关键步骤前的安全检查（占位实现）",
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


def create_safety_check_piece() -> TaskPiece:
    """工厂函数：返回一个 SafetyCheckPiece 实例。"""
    return TaskPiece(
        id="safety_check_piece",
        hook_point=HOOK_POINT_SAFETY_BEFORE,
        piece_type=TaskPieceType.NODE,
        condition=_always_enabled,
        builder=_build_safety_check_patch,
        priority=35,
        description="在关键步骤前插入安全检查节点的任务积木",
    )

