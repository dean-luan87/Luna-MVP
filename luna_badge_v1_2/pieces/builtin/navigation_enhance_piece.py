from __future__ import annotations

"""
NavigationEnhancePiece

作用：
- 在"导航节点"前插入，用于增强导航能力；
- 如：入口选取、路线合理性检查、个性化偏好修正等。

Hook：
- NAV_BEFORE：在导航节点之前执行。

当前版本（v1.4.5C-1）：
- 仅提供骨架与元数据，不实现具体业务逻辑。
"""

from typing import Any, Dict

from pieces.base_piece import TaskPiece, TaskPieceType
from patches.flow_patch import FlowPatch
from core.flow_engine.flow_types import FlowNode, FlowNodeType


HOOK_POINT_NAV_BEFORE = "NAV_BEFORE"


def _always_enabled(context: Any, env: Dict[str, Any]) -> bool:
    """条件：当前版本无条件启用。"""
    return True


def _build_navigation_enhance_patch(context: Any, env: Dict[str, Any]) -> FlowPatch:
    """
    为当前流程插入一个"导航增强节点"（占位实现）。
    后续在 C-3 中再补充具体实现。
    """
    node_id = "navigation_enhance"
    node = FlowNode(
        id=node_id,
        node_type=FlowNodeType.CUSTOM,
        params={
            "action": "navigation_enhance",
            "description": "导航能力增强（占位实现）",
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


def create_navigation_enhance_piece() -> TaskPiece:
    """工厂函数：返回一个 NavigationEnhancePiece 实例。"""
    return TaskPiece(
        id="navigation_enhance_piece",
        hook_point=HOOK_POINT_NAV_BEFORE,
        piece_type=TaskPieceType.NODE,
        condition=_always_enabled,
        builder=_build_navigation_enhance_patch,
        priority=45,
        description="在导航节点前插入导航增强节点的任务积木",
    )

