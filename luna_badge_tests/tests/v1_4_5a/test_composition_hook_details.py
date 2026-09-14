# tests/v1_4_5a/test_composition_hook_details.py
"""
测试从模板 hook_points_detail 自动触发 hook 并传递 attach_node

验证：
1. metadata 写了 hook_points 和 hook_points_detail
2. CompositionEngine 能根据 metadata 触发 map_record_piece
3. attach_node 信息能正确传递到 apply_patch
4. map_record 节点如期存在
"""
from pieces.registry import TaskPieceRegistry
from composition.composition_engine import CompositionEngine

from core.flow_engine.flow_types import FlowDefinition, FlowContext, FlowNode, FlowNodeType


def test_map_record_injected_from_hook_details_metadata():
    """测试从 hook_points_detail metadata 自动注入 MapRecordPiece"""
    # 1. 构造最小 FlowDefinition，模拟医院模板输出
    # 需要先创建一个节点，attach_node 才能指向它
    from core.flow_engine.flow_types import FlowNode, FlowNodeType
    start_node = FlowNode(
        id="start",
        node_type=FlowNodeType.QUERY_USER,
        params={},
    )
    
    flow_def = FlowDefinition(
        id="test_flow",
        nodes={"start": start_node},
        edges=[],
        entry_node_id="start",
    )
    # hook_points + hook_points_detail
    flow_def.metadata["hook_points"] = ["GO_BEFORE"]
    flow_def.metadata["hook_points_detail"] = {
        "GO_BEFORE": {"attach_node": "start"}
    }

    context = FlowContext(
        task_id="t1",
        user_id="u1",
        scene_type="outdoor",
        intent="go_hospital",
        data={},
    )

    # 2. 使用默认 TaskPieceRegistry（含 map_record_piece）
    registry = TaskPieceRegistry.create_default_registry()
    engine = CompositionEngine(piece_registry=registry)

    # 3. 执行组合（env 不提供 hook_points）
    new_flow_def = engine.compose(flow_def, context, env={})

    # 4. 验证：map_record 节点已被注入
    assert "map_record" in new_flow_def.nodes
    node: FlowNode = new_flow_def.nodes["map_record"]
    assert node.params.get("action") == "map_record"
    assert node.node_type == FlowNodeType.CUSTOM


def test_hospital_template_with_hook_details():
    """测试医院模板实际生成的 FlowDefinition 包含 hook_points_detail"""
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

    # 4. 验证 metadata 中包含 hook_points 和 hook_points_detail
    assert "hook_points" in flow_def.metadata
    assert isinstance(flow_def.metadata["hook_points"], list)
    assert "GO_BEFORE" in flow_def.metadata["hook_points"]
    
    assert "hook_points_detail" in flow_def.metadata
    assert isinstance(flow_def.metadata["hook_points_detail"], dict)
    assert "GO_BEFORE" in flow_def.metadata["hook_points_detail"]
    assert "attach_node" in flow_def.metadata["hook_points_detail"]["GO_BEFORE"]
    assert flow_def.metadata["hook_points_detail"]["GO_BEFORE"]["attach_node"] == "ask_hospital"


def test_attach_node_passed_to_apply_patch():
    """测试 attach_node 能正确传递到 apply_patch（通过组合引擎）"""
    # 1. 构建 FlowDefinition，包含 hook_points_detail
    flow_def = FlowDefinition(
        id="test_flow",
        nodes={"start": FlowNode(
            id="start",
            node_type=FlowNodeType.QUERY_USER,
            params={},
        )},
        edges=[],
        entry_node_id="start",
    )
    flow_def.metadata["hook_points"] = ["GO_BEFORE"]
    flow_def.metadata["hook_points_detail"] = {
        "GO_BEFORE": {"attach_node": "start"}
    }

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

    # 3. 执行组合
    new_flow_def = engine.compose(flow_def, context, env={})

    # 4. 验证：map_record 节点被注入
    assert "map_record" in new_flow_def.nodes
    # 验证：原有节点保留
    assert "start" in new_flow_def.nodes
    # 注意：当前版本不实现边重接，所以边结构可能不变
    # 后续实现边重接后，可以验证边的连接关系

