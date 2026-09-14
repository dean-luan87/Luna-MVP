"""
测试：TaskPatch 与 Piece.build_patches 统一抽象的行为。

覆盖点：
- 带有 build_task_patches(...) 的 Piece 可以返回多个 TaskPatch，并被依序应用；
- 只有 build_patch(...) 的老 Piece 会自动被包装为单一 TaskPatch；
- attach_node 能正确传递到 apply_task_patch / apply_patch。
"""

from dataclasses import dataclass
from typing import List, Optional, Any

from composition.patch_utils import TaskPatch, apply_task_patch
from core.flow_engine.flow_types import FlowDefinition, FlowNode, FlowEdge, FlowNodeType
from pieces.base_piece import TaskPiece, TaskPieceType
from patches.flow_patch import FlowPatch


def _always_enabled(context: Any, env: dict) -> bool:
    return True


def _dummy_builder(context: Any, env: dict) -> FlowPatch:
    return FlowPatch(
        new_nodes={},
        new_edges=[],
        delete_nodes=[],
        rewire_entry=None,
        rewire_exit=None,
    )


@dataclass
class _MultiPatchPiece(TaskPiece):
    """用于测试的 Piece，实现 build_task_patches 返回多个 TaskPatch。"""

    def build_task_patches(
        self,
        flow_def: FlowDefinition,
        *,
        attach_node: Optional[str] = None,
    ) -> List[TaskPatch]:
        # 模拟产生两个 Patch：分别插入两个节点
        node_a = FlowNode(
            id="a",
            node_type=FlowNodeType.CUSTOM,
            params={"action": "a"},
        )
        node_b = FlowNode(
            id="b",
            node_type=FlowNodeType.CUSTOM,
            params={"action": "b"},
        )
        edge_a = FlowEdge(
            source_id=attach_node or "start",
            target_id="a",
            condition=None,
        )
        edge_b = FlowEdge(
            source_id="a",
            target_id="b",
            condition=None,
        )

        patch1 = TaskPatch(
            new_nodes=[node_a],
            new_edges=[edge_a],
            attach_node=attach_node,
        )
        patch2 = TaskPatch(
            new_nodes=[node_b],
            new_edges=[edge_b],
            attach_node=None,  # 第二个 patch 不再重新重接 attach_node
        )
        return [patch1, patch2]


def test_taskpatch_can_apply_multiple_patches_in_order() -> None:
    # 构造一个最小的 FlowDefinition
    from core.flow_engine.flow_types import FlowNode, FlowNodeType

    start_node = FlowNode(
        id="start",
        node_type=FlowNodeType.CUSTOM,
        params={},
    )

    flow = FlowDefinition(
        id="test",
        nodes={"start": start_node},
        edges=[],
        entry_node_id="start",
        metadata={},
    )

    # 创建测试 Piece
    piece = _MultiPatchPiece(
        id="multi_patch_piece",
        hook_point="GO_BEFORE",
        piece_type=TaskPieceType.NODE,
        condition=_always_enabled,
        builder=_dummy_builder,
        priority=10,
    )

    patches = list(piece.build_patches(flow_def=flow, attach_node="start"))

    # 应该产生两个 patch
    assert len(patches) == 2
    assert patches[0].attach_node == "start"
    # 第二个无 attach_node
    assert patches[1].attach_node is None

    # 顺序应用
    for patch in patches:
        flow = apply_task_patch(flow, patch)

    # 验证节点和边的数量
    # 具体断言可根据 apply_patch 的行为稍作调整，
    # 核心是确认两个 patch 都生效，而不是只应用了第一个。
    node_ids = set(flow.nodes.keys())
    assert "a" in node_ids
    assert "b" in node_ids

    # 验证边的连接
    edge_sources = {e.source_id for e in flow.edges}
    edge_targets = {e.target_id for e in flow.edges}
    assert "start" in edge_sources or "a" in edge_sources
    assert "a" in edge_targets
    assert "b" in edge_targets


def test_legacy_piece_with_builder_is_wrapped_as_taskpatch() -> None:
    """测试：只有 builder 的老 Piece 会被自动包装为 TaskPatch。"""
    from pieces.builtin.map_record_piece import create_map_record_piece

    piece = create_map_record_piece()

    # 构造一个最小的 FlowDefinition
    from core.flow_engine.flow_types import FlowNode, FlowNodeType

    start_node = FlowNode(
        id="ask_hospital",
        node_type=FlowNodeType.QUERY_USER,
        params={},
    )

    flow = FlowDefinition(
        id="test",
        nodes={"ask_hospital": start_node},
        edges=[],
        entry_node_id="ask_hospital",
        metadata={},
    )

    patches = list(piece.build_patches(flow_def=flow, attach_node="ask_hospital"))

    # 应该产生一个 patch（从 builder 转换而来）
    assert len(patches) == 1
    assert patches[0].attach_node == "ask_hospital"
    assert len(patches[0].new_nodes) > 0
    assert any(node.id == "map_record" for node in patches[0].new_nodes)


def test_attach_node_passed_through_taskpatch() -> None:
    """测试：attach_node 能正确传递到 apply_task_patch。"""
    from core.flow_engine.flow_types import FlowNode, FlowNodeType

    start_node = FlowNode(
        id="start",
        node_type=FlowNodeType.CUSTOM,
        params={},
    )
    end_node = FlowNode(
        id="end",
        node_type=FlowNodeType.CUSTOM,
        params={},
    )

    flow = FlowDefinition(
        id="test",
        nodes={"start": start_node, "end": end_node},
        edges=[FlowEdge(source_id="start", target_id="end", condition=None)],
        entry_node_id="start",
        metadata={},
    )

    # 创建一个简单的 patch，插入到 start 和 end 之间
    new_node = FlowNode(
        id="middle",
        node_type=FlowNodeType.CUSTOM,
        params={},
    )

    patch = TaskPatch(
        new_nodes=[new_node],
        new_edges=[],
        attach_node="start",
    )

    result = apply_task_patch(flow, patch)

    # 验证新节点已添加
    assert "middle" in result.nodes

    # 验证边重接：start -> middle -> end
    edge_dict = {(e.source_id, e.target_id): e for e in result.edges}
    assert ("start", "middle") in edge_dict
    assert ("middle", "end") in edge_dict

