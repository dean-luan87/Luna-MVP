# tests/v1_4_5a/test_map_record_piece.py
"""
测试 MapRecordPiece 积木的集成

验证：
1. MapRecordPiece 可以正确注册
2. CompositionEngine 可以找到并应用 MapRecordPiece
3. 组合后的流程包含地图记录节点
4. 节点个数增加（从 3 个变为 4 个）
"""
from pieces.registry import TaskPieceRegistry
from composition.composition_engine import CompositionEngine
from patches.flow_patch import FlowPatch

from core.flow_engine.flow_types import FlowDefinition, FlowContext, FlowNode, FlowNodeType


def test_map_record_piece_injected_via_composition():
    """测试通过 CompositionEngine 注入 MapRecordPiece"""
    # 1. 准备一个空骨架流程
    flow_def = FlowDefinition(
        id="test_flow",
        nodes={},
        edges=[],
        entry_node_id="start",
    )
    context = FlowContext(
        task_id="t1",
        user_id="u1",
        scene_type="outdoor",
        intent="go_hospital",
        data={},
    )

    # 2. 组合引擎 + 默认注册中心（已注册 map_record_piece）
    registry = TaskPieceRegistry.create_default_registry()
    engine = CompositionEngine(piece_registry=registry)

    # 3. 调用 compose，手动传入 hook_points=["GO_BEFORE"]
    env = {"hook_points": ["GO_BEFORE"]}
    new_flow_def = engine.compose(flow_def, context, env)

    # 4. 验证：map_record 节点已被注入
    assert "map_record" in new_flow_def.nodes
    node = new_flow_def.nodes["map_record"]
    assert node.node_type == FlowNodeType.CUSTOM
    assert node.params.get("action") == "map_record"


def test_map_record_piece_with_existing_nodes():
    """测试在有现有节点的情况下注入 MapRecordPiece"""
    # 1. 创建一个有节点的流程
    existing_node = FlowNode(
        id="existing",
        node_type=FlowNodeType.QUERY_USER,
        params={},
    )
    flow_def = FlowDefinition(
        id="test_flow",
        nodes={"existing": existing_node},
        edges=[],
        entry_node_id="existing",
    )
    context = FlowContext(
        task_id="t1",
        user_id="u1",
        scene_type="outdoor",
        intent="go_hospital",
        data={},
    )

    # 2. 组合引擎 + 默认注册中心
    registry = TaskPieceRegistry.create_default_registry()
    engine = CompositionEngine(piece_registry=registry)

    # 3. 调用 compose
    env = {"hook_points": ["GO_BEFORE"]}
    new_flow_def = engine.compose(flow_def, context, env)

    # 4. 验证：原有节点保留，新增 map_record 节点
    assert "existing" in new_flow_def.nodes
    assert "map_record" in new_flow_def.nodes
    assert len(new_flow_def.nodes) == 2


def test_composition_without_hook_points():
    """测试不传入 hook_points 时，流程保持不变"""
    # 1. 准备流程
    existing_node = FlowNode(
        id="existing",
        node_type=FlowNodeType.QUERY_USER,
        params={},
    )
    flow_def = FlowDefinition(
        id="test_flow",
        nodes={"existing": existing_node},
        edges=[],
        entry_node_id="existing",
    )
    context = FlowContext(
        task_id="t1",
        user_id="u1",
        scene_type="outdoor",
        intent="go_hospital",
        data={},
    )

    # 2. 组合引擎
    registry = TaskPieceRegistry.create_default_registry()
    engine = CompositionEngine(piece_registry=registry)

    # 3. 调用 compose，不传入 hook_points
    env = {}  # 没有 hook_points
    new_flow_def = engine.compose(flow_def, context, env)

    # 4. 验证：流程保持不变
    assert len(new_flow_def.nodes) == 1
    assert "existing" in new_flow_def.nodes
    assert "map_record" not in new_flow_def.nodes


def test_map_record_piece_registration():
    """测试 MapRecordPiece 可以正确注册"""
    registry = TaskPieceRegistry.create_default_registry()
    
    # 验证注册成功
    retrieved = registry.get("map_record_piece")
    assert retrieved is not None
    assert retrieved.id == "map_record_piece"
    assert retrieved.hook_point == "GO_BEFORE"


def test_map_record_piece_condition():
    """测试 MapRecordPiece 的条件判断"""
    registry = TaskPieceRegistry.create_default_registry()
    piece = registry.get("map_record_piece")
    assert piece is not None
    
    # 模拟 context 和 env
    class MockContext:
        scene_type = "outdoor"
        intent = "go_hospital"
    
    context = MockContext()
    env = {}
    
    # 条件应该始终为 True
    assert piece.condition(context, env) is True
