# scripts/debug_print_hospital_flow.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.flow_templates.hospital_go_template import GoHospitalTemplate
from core.flow_engine.planner import PlanningInput


def main():
    template = GoHospitalTemplate()
    planning_input = PlanningInput(
        user_id="debug-user",
        intent="go_hospital",
        scene_type="outdoor",
        raw_utterance="我想去医院看病",
        extra={},
    )

    flow_def = template.instantiate(planning_input)

    print("=== Hospital Flow: Nodes ===")
    for node_id, node in flow_def.nodes.items():
        node_type = getattr(node, 'node_type', 'unknown')
        if hasattr(node_type, 'value'):
            node_type = node_type.value
        print(f"- {node_id} ({node_type})")

    print("\n=== Hospital Flow: Edges ===")
    for edge in flow_def.edges:
        cond = edge.condition or "None"
        print(f"- {edge.source_id} -> {edge.target_id} (cond={cond})")

    print(f"\n=== Entry Node ===")
    print(f"entry_node_id: {flow_def.entry_node_id}")

    print("\n=== Metadata ===")
    for k, v in flow_def.metadata.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()

