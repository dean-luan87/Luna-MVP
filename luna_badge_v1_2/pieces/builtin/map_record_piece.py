# pieces/builtin/map_record_piece.py
from __future__ import annotations

from typing import Any, Dict

from pieces.base_piece import TaskPiece, TaskPieceType
from patches.flow_patch import FlowPatch

from core.flow_engine.flow_types import FlowNode, FlowEdge, FlowNodeType


HOOK_POINT_GO_BEFORE = "GO_BEFORE"  # 约定：医院"出发前"的 hook 名


def _always_enabled(context: Any, env: Dict[str, Any]) -> bool:
    """
    条件：目前无条件启用，后续可以加限制逻辑（例如只在 outdoor 场景启用）。
    """
    return True


def _build_map_record_patch(context: Any, env: Dict[str, Any]) -> FlowPatch:
    """
    为当前流程插入一个"地图记录节点"。

    这里做的是最小可用实现：
      - 新增一个节点 map_record
      - 不强行改动入口/出口，具体连接策略后续根据 FlowDefinition 的结构再增强
    """
    # 约定一个节点 ID
    node_id = "map_record"

    node = FlowNode(
        id=node_id,
        node_type=FlowNodeType.CUSTOM,  # 使用 CUSTOM 类型
        params={
            "action": "map_record",
            "description": "记录本次出发前的位置信息（占位实现）",
        },
    )

    patch = FlowPatch(
        new_nodes={node_id: node},
        new_edges=[],          # 此处暂不自动连边，后续根据实际结构再完善
        delete_nodes=[],
        rewire_entry=None,
        rewire_exit=None,
    )
    return patch


def create_map_record_piece() -> TaskPiece:
    """
    工厂函数：返回一个 TaskPiece 实例，便于在 registry 中注册。
    """
    return TaskPiece(
        id="map_record_piece",
        hook_point=HOOK_POINT_GO_BEFORE,
        piece_type=TaskPieceType.NODE,
        condition=_always_enabled,
        builder=_build_map_record_patch,
        priority=40,  # 地图记录优先级（默认 50，这里设为 40）
        description="在出发前插入地图记录节点的任务积木",
    )
