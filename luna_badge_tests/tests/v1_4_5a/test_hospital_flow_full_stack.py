"""
综合测试：验证医院模板 + 多 Hook + 多 Piece + 多 Patch 的组合行为。

目标：
- 模板声明 GO_BEFORE + REGISTER_BEFORE
- Piece:
    MapRecordPiece (GO_BEFORE)
    StaffAssistPiece (REGISTER_BEFORE)
    PreCheckPiece (START_BEFORE) —— 不应被触发
- 插入点 attach_node:
    GO_BEFORE → ask_hospital 之前
    REGISTER_BEFORE → navigate 之后

期望拓扑结构：
    ask_hospital -> map_record -> navigate -> staff_assist -> wait_arrival
"""

import pytest

from core.flow_templates.hospital_go_template import GoHospitalTemplate
from core.flow_engine.planner import PlanningInput
from composition.composition_engine import CompositionEngine
from pieces.registry import TaskPieceRegistry
from core.flow_engine.flow_types import FlowDefinition, FlowContext


def _edge_pairs(flow: FlowDefinition):
    """提取所有边的 (source, target) 对，便于断言。"""
    return {(e.source_id, e.target_id) for e in flow.edges}


def test_hospital_full_stack_flow():
    # 1. 构建模板
    template = GoHospitalTemplate()
    
    # 创建 PlanningInput（模板的 instantiate 需要这个参数）
    planning_input = PlanningInput(
        user_id="test_user",
        intent="go_hospital",
        scene_type="outdoor",
        raw_utterance="我想去医院",
        extra={},
    )
    
    flow_def = template.instantiate(planning_input)

    original_nodes = set(flow_def.nodes.keys())
    assert "ask_hospital" in original_nodes
    assert "navigate" in original_nodes
    assert "wait_arrival" in original_nodes

    # 2. 使用默认 Registry
    registry = TaskPieceRegistry.create_default_registry()

    # 3. CompositionEngine 执行 Hook → Piece → Patch 拼装
    context = FlowContext(
        task_id="test_task",
        user_id="test_user",
        scene_type="outdoor",
        intent="go_hospital",
    )
    
    engine = CompositionEngine(registry)
    composed = engine.compose(flow_def, context, env={})

    # 4. 检查 Piece 是否正确插入节点
    all_nodes = set(composed.nodes.keys())
    assert "map_record" in all_nodes, "MapRecordPiece 应插入 map_record"
    assert "staff_assist" in all_nodes, "StaffAssistPiece 应插入 staff_assist"
    assert "pre_check" not in all_nodes, "PreCheckPiece 不应被触发"

    # 5. 检查拓扑结构（边）
    edges = _edge_pairs(composed)

    # GO_BEFORE：ask_hospital -> map_record -> navigate
    assert ("ask_hospital", "map_record") in edges
    assert ("map_record", "navigate") in edges
    assert ("ask_hospital", "navigate") not in edges  # 原直连必须被替换

    # REGISTER_BEFORE：navigate -> staff_assist -> wait_arrival
    assert ("navigate", "staff_assist") in edges
    assert ("staff_assist", "wait_arrival") in edges
    assert ("navigate", "wait_arrival") not in edges

    # 最终关键路径
    expected_path = [
        ("ask_hospital", "map_record"),
        ("map_record", "navigate"),
        ("navigate", "staff_assist"),
        ("staff_assist", "wait_arrival"),
    ]
    for p in expected_path:
        assert p in edges, f"缺少关键路径边：{p}"

    # 验证终点不会作为 source 出现
    sources = {e.source_id for e in composed.edges}
    assert "wait_arrival" not in sources

