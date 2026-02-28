# tests/v1_4_5a/test_hospital_flow_with_map_record.py
from core.flow_templates.hospital_go_template import GoHospitalTemplate, HOOK_POINT_GO_BEFORE
from core.flow_engine.flow_types import FlowDefinition, FlowContext, FlowNode, FlowNodeType, FlowEdge
from core.flow_engine.planner import PlanningInput
from composition.composition_engine import CompositionEngine
from pieces.registry import TaskPieceRegistry


def test_hospital_flow_injected_with_map_record_piece():
    """测试医院流程通过 CompositionEngine 注入 MapRecordPiece 后的完整结构"""
    # 1. 构建模板
    template = GoHospitalTemplate()

    planning_input = PlanningInput(
        user_id="u1",
        intent="go_hospital",
        scene_type="outdoor",
        raw_utterance="我想去医院看病",
        extra={},
    )

    flow_def = template.instantiate(planning_input)

    # 保底检查：模板结构符合预期
    assert "ask_hospital" in flow_def.nodes
    assert "navigate" in flow_def.nodes
    assert "wait_arrival" in flow_def.nodes
    assert any(
        e.source_id == "ask_hospital" and e.target_id == "navigate"
        for e in flow_def.edges
    )

    # 2. 组合引擎（含 map_record_piece）
    registry = TaskPieceRegistry.create_default_registry()
    engine = CompositionEngine(piece_registry=registry)

    # 创建上下文
    from core.flow_engine.flow_types import FlowContext
    context = FlowContext(
        task_id="t1",
        user_id="u1",
        scene_type="outdoor",
        intent="go_hospital",
        data={},
    )

    # 3. 调用 compose（模板已经在 metadata 中声明 hook_points / hook_points_detail）
    composed = engine.compose(flow_def, context, env={})

    # 4. 验证：map_record 节点被注入
    assert "map_record" in composed.nodes

    # 5. 验证：ask_hospital -> map_record -> navigate 路径存在
    edges = {(e.source_id, e.target_id, e.condition) for e in composed.edges}
    assert ("ask_hospital", "map_record", None) in edges
    assert ("map_record", "navigate", "success") in edges
    
    # 6. 验证：navigate -> staff_assist -> wait_arrival 路径存在（因为现在有两个 piece）
    assert ("navigate", "staff_assist", None) in edges
    assert ("staff_assist", "wait_arrival", "success") in edges

    # 7. 验证：原始 ask_hospital -> navigate 直连不存在
    assert ("ask_hospital", "navigate", "success") not in edges
    # 原始 navigate -> wait_arrival 直连也不存在（被 staff_assist 插入）
    assert ("navigate", "wait_arrival", "success") not in edges

    # 7. 验证：所有原始节点都保留
    assert "ask_hospital" in composed.nodes
    assert "navigate" in composed.nodes
    assert "wait_arrival" in composed.nodes


def test_hospital_flow_structure_before_after():
    """对比组合前后的流程结构变化"""
    template = GoHospitalTemplate()
    planning_input = PlanningInput(
        user_id="u1",
        intent="go_hospital",
        scene_type="outdoor",
        raw_utterance="我想去医院看病",
        extra={},
    )

    # 组合前
    flow_def_before = template.instantiate(planning_input)
    
    # 组合后
    registry = TaskPieceRegistry.create_default_registry()
    engine = CompositionEngine(piece_registry=registry)
    context = FlowContext(
        task_id="t1",
        user_id="u1",
        scene_type="outdoor",
        intent="go_hospital",
        data={},
    )
    flow_def_after = engine.compose(flow_def_before, context, env={})

    # 验证节点数量变化
    assert len(flow_def_before.nodes) == 3
    assert len(flow_def_after.nodes) == 5  # 增加了 map_record 和 staff_assist

    # 验证边数量变化
    # 组合前：2 条边（ask_hospital->navigate, navigate->wait_arrival）
    # 组合后：4 条边（ask_hospital->map_record, map_record->navigate, navigate->staff_assist, staff_assist->wait_arrival）
    assert len(flow_def_before.edges) == 2
    assert len(flow_def_after.edges) == 4

