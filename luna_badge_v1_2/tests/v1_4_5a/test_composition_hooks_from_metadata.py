# tests/v1_4_5a/test_composition_hooks_from_metadata.py
"""
测试从模板 metadata 自动触发 hook

验证：
1. FlowDefinition.metadata 中的 hook_points 可以自动触发 TaskPiece
2. 不需要手动传入 env["hook_points"]
3. metadata 和 env 的 hook_points 可以合并
"""
from pieces.registry import TaskPieceRegistry
from composition.composition_engine import CompositionEngine

from core.flow_engine.flow_types import FlowDefinition, FlowContext, FlowNode, FlowNodeType


def test_map_record_injected_from_template_metadata():
    """测试从模板 metadata 自动注入 MapRecordPiece"""
    # 1. 构建一个最小 FlowDefinition，模拟医院模板输出
    flow_def = FlowDefinition(
        id="test_flow",
        nodes={},
        edges=[],
        entry_node_id="start",
    )
    flow_def.metadata["hook_points"] = ["GO_BEFORE"]

    context = FlowContext(
        task_id="t1",
        user_id="u1",
        scene_type="outdoor",
        intent="go_hospital",
        data={},
    )

    # 2. 使用默认注册中心（已注册 map_record_piece）
    registry = TaskPieceRegistry.create_default_registry()
    engine = CompositionEngine(piece_registry=registry)

    # 3. 不传 env 中的 hook_points，仅依赖 metadata
    new_flow_def = engine.compose(flow_def, context, env={})

    # 4. 验证 map_record 节点被注入
    assert "map_record" in new_flow_def.nodes
    node: FlowNode = new_flow_def.nodes["map_record"]
    assert node.node_type == FlowNodeType.CUSTOM
    assert node.params.get("action") == "map_record"


def test_metadata_and_env_hooks_merged():
    """测试 metadata 和 env 的 hook_points 可以合并"""
    # 1. 构建 FlowDefinition，metadata 中有 GO_BEFORE
    flow_def = FlowDefinition(
        id="test_flow",
        nodes={},
        edges=[],
        entry_node_id="start",
    )
    flow_def.metadata["hook_points"] = ["GO_BEFORE"]

    context = FlowContext(
        task_id="t1",
        user_id="u1",
        scene_type="outdoor",
        intent="go_hospital",
        data={},
    )

    # 2. env 中也有 hook_points（虽然当前没有其他 piece，但测试合并逻辑）
    registry = TaskPieceRegistry.create_default_registry()
    engine = CompositionEngine(piece_registry=registry)

    # 3. env 中传入相同的 hook（应该去重）
    env = {"hook_points": ["GO_BEFORE"]}
    new_flow_def = engine.compose(flow_def, context, env=env)

    # 4. 验证 map_record 节点被注入（只注入一次，因为去重）
    assert "map_record" in new_flow_def.nodes
    # 验证只有一个 map_record 节点（去重成功）
    map_record_nodes = [nid for nid in new_flow_def.nodes.keys() if nid == "map_record"]
    assert len(map_record_nodes) == 1


def test_no_hooks_no_injection():
    """测试没有 hook_points 时，不注入任何节点"""
    # 1. 构建 FlowDefinition，没有 hook_points
    flow_def = FlowDefinition(
        id="test_flow",
        nodes={"existing": FlowNode(
            id="existing",
            node_type=FlowNodeType.QUERY_USER,
            params={},
        )},
        edges=[],
        entry_node_id="existing",
    )
    # 不设置 metadata["hook_points"]

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

    # 3. 不传 env 中的 hook_points
    new_flow_def = engine.compose(flow_def, context, env={})

    # 4. 验证：原有节点保留，没有注入 map_record
    assert "existing" in new_flow_def.nodes
    assert "map_record" not in new_flow_def.nodes
    assert len(new_flow_def.nodes) == 1


def test_hospital_template_with_metadata():
    """测试医院模板实际生成的 FlowDefinition 包含 metadata hook_points"""
    from core.flow_templates.templates_registry import FlowTemplateRegistry
    from core.flow_templates.hospital_go_template import GoHospitalTemplate
    from core.flow_engine.planner import PlanningInput

    # 1. 创建模板注册表并注册医院模板
    registry = FlowTemplateRegistry()
    registry.register_template(GoHospitalTemplate())

    # 2. 创建 PlanningInput
    planning_input = PlanningInput(
        user_id="u1",
        intent="go_hospital",
        scene_type="outdoor",
        raw_utterance="我想去医院看病",
        extra={},
    )

    # 3. 从模板生成 FlowDefinition
    template = registry.select_template("go_hospital", "outdoor")
    assert template is not None
    flow_def = template.instantiate(planning_input)

    # 4. 验证 metadata 中包含 hook_points
    assert "hook_points" in flow_def.metadata
    assert isinstance(flow_def.metadata["hook_points"], list)
    assert "GO_BEFORE" in flow_def.metadata["hook_points"]












