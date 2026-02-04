# pieces/builtin/staff_assist_piece.py
from __future__ import annotations

from typing import Any, Dict

from pieces.base_piece import TaskPiece, TaskPieceType
from patches.flow_patch import FlowPatch

from core.flow_engine.flow_types import FlowNode, FlowNodeType


HOOK_POINT_REGISTER_BEFORE = "REGISTER_BEFORE"
STAFF_ASSIST_NODE_ID = "staff_assist"


def _always_enabled(context: Any, env: Dict[str, Any]) -> bool:
    """
    当前阶段：无条件启用，后面可以根据场景/用户特征加条件。
    """
    return True


def _build_staff_assist_patch(context: Any, env: Dict[str, Any]) -> FlowPatch:
    """
    在挂号前插入一个"寻求工作人员协助"的节点。

    逻辑行为先占位，真正语音/策略由 runtime 决定。
    """
    node = FlowNode(
        id=STAFF_ASSIST_NODE_ID,
        node_type=FlowNodeType.CUSTOM,
        params={
            "action": "staff_assist",
            "description": "提示用户可以寻求医院工作人员协助挂号（占位实现）",
        },
    )

    patch = FlowPatch(
        new_nodes={STAFF_ASSIST_NODE_ID: node},
        new_edges=[],
        delete_nodes=[],
        rewire_entry=None,
        rewire_exit=None,
    )
    return patch


def create_staff_assist_piece() -> TaskPiece:
    """
    工厂函数：创建 StaffAssistPiece 积木。
    """
    return TaskPiece(
        id="staff_assist_piece",
        hook_point=HOOK_POINT_REGISTER_BEFORE,
        piece_type=TaskPieceType.NODE,
        condition=_always_enabled,
        builder=_build_staff_assist_patch,
        priority=30,  # 比 map_record（假设 40-50）略高或略低都可以，这里取 30
        description="在挂号前插入'寻求工作人员协助'节点",
    )
