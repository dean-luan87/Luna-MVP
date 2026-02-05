# tests/v1_4_5a/test_apply_patch_rewire.py
from core.flow_engine.flow_types import FlowDefinition, FlowNode, FlowNodeType, FlowEdge
from patches.flow_patch import FlowPatch
from composition.patch_utils import apply_patch


def _make_node(node_id: str) -> FlowNode:
    return FlowNode(
        id=node_id,
        node_type=FlowNodeType.CUSTOM,
        params={},
    )


def test_apply_patch_rewire_with_attach_node():
    """测试 apply_patch 的边重接逻辑"""
    # 原始流程：ask_hospital -> navigate -> wait_arrival
    nodes = {
        "ask_hospital": _make_node("ask_hospital"),
        "navigate": _make_node("navigate"),
        "wait_arrival": _make_node("wait_arrival"),
    }
    edges = [
        FlowEdge(source_id="ask_hospital", target_id="navigate", condition="success"),
        FlowEdge(source_id="navigate", target_id="wait_arrival", condition="success"),
    ]

    flow_def = FlowDefinition(
        id="test_flow",
        nodes=nodes,
        edges=edges,
        entry_node_id="ask_hospital",
    )

    # patch：新增 map_record 节点，不显式新增边
    map_record_node = _make_node("map_record")
    patch = FlowPatch(
        new_nodes={"map_record": map_record_node},
        new_edges=[],
        delete_nodes=[],
        rewire_entry=None,
        rewire_exit=None,
    )

    # attach_node = ask_hospital
    updated = apply_patch(flow_def, patch, attach_node="ask_hospital")

    # 验证节点
    assert "map_record" in updated.nodes
    assert "ask_hospital" in updated.nodes
    assert "navigate" in updated.nodes
    assert "wait_arrival" in updated.nodes

    # 收集边
    rel = {(e.source_id, e.target_id, e.condition) for e in updated.edges}

    # 必须：ask_hospital -> map_record，map_record -> navigate，navigate -> wait_arrival
    assert ("ask_hospital", "map_record", None) in rel
    assert ("map_record", "navigate", "success") in rel
    assert ("navigate", "wait_arrival", "success") in rel

    # 不应存在原来的 ask_hospital -> navigate 直连
    assert ("ask_hospital", "navigate", "success") not in rel


def test_apply_patch_without_attach_node():
    """测试不提供 attach_node 时，只添加节点和显式边"""
    nodes = {
        "start": _make_node("start"),
    }
    edges = []

    flow_def = FlowDefinition(
        id="test_flow",
        nodes=nodes,
        edges=edges,
        entry_node_id="start",
    )

    new_node = _make_node("new_node")
    patch = FlowPatch(
        new_nodes={"new_node": new_node},
        new_edges=[
            FlowEdge(source_id="start", target_id="new_node", condition="success"),
        ],
        delete_nodes=[],
    )

    updated = apply_patch(flow_def, patch, attach_node=None)

    # 验证节点
    assert "new_node" in updated.nodes

    # 验证边（只包含显式添加的边）
    rel = {(e.source_id, e.target_id, e.condition) for e in updated.edges}
    assert ("start", "new_node", "success") in rel


def test_apply_patch_attach_node_validation():
    """测试 attach_node 校验"""
    nodes = {
        "start": _make_node("start"),
    }
    edges = []

    flow_def = FlowDefinition(
        id="test_flow",
        nodes=nodes,
        edges=edges,
        entry_node_id="start",
    )

    new_node = _make_node("new_node")
    patch = FlowPatch(
        new_nodes={"new_node": new_node},
        new_edges=[],
    )

    # 应该抛出异常，因为 "invalid_node" 不存在
    try:
        apply_patch(flow_def, patch, attach_node="invalid_node")
        assert False, "应该抛出 ValueError"
    except ValueError as e:
        assert "invalid_node" in str(e)
        assert "not found" in str(e)












