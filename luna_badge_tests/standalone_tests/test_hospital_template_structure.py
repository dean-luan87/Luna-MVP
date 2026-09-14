# test_hospital_template_structure.py
from core.flow_templates.hospital_go_template import GoHospitalTemplate
from core.flow_engine.flow_types import PlanningInput

if __name__ == "__main__":
    # 创建 PlanningInput（正确的参数）
    planner_input = PlanningInput(
        user_id="u1",
        intent="go_hospital",
        scene_type="outdoor",
        raw_utterance="去医院",
        extra={},
    )
    
    # 实例化模板
    template = GoHospitalTemplate()
    flow_def = template.instantiate(planner_input)

    print("=== Hospital Template Nodes ===")
    for node_id, node in flow_def.nodes.items():
        print(f"- {node_id} (type: {node.node_type.value})")

    print("\n=== Hospital Template Edges ===")
    for edge in flow_def.edges:
        print(f"{edge.source_id} -> {edge.target_id} (cond={edge.condition})")
    
    print(f"\n=== Entry Node ===")
    print(f"entry_node_id: {flow_def.entry_node_id}")
    
    print(f"\n=== Metadata ===")
    print(f"hook_points: {flow_def.metadata.get('hook_points', [])}")
    print(f"hook_points_detail: {flow_def.metadata.get('hook_points_detail', {})}")

