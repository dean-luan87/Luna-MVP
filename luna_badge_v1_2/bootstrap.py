# bootstrap.py
from core.flow_templates.templates_registry import FlowTemplateRegistry
from core.flow_templates.hospital_go_template import GoHospitalTemplate
from core.flow_engine.planner import FlowPlanner
from core.flow_engine.runtime import FlowRuntime
from core.query_engine.query_manager import QueryEngine
from decision_core.decision_core import DecisionCore, DecisionRequest


def build_decision_core() -> DecisionCore:
    registry = FlowTemplateRegistry()
    registry.register_template(GoHospitalTemplate())

    planner = FlowPlanner(template_registry=registry)
    runtime = FlowRuntime()
    query_engine = QueryEngine()

    core = DecisionCore(
        flow_planner=planner,
        flow_runtime=runtime,
        query_engine=query_engine,
    )
    return core


if __name__ == "__main__":
    core = build_decision_core()
    req = DecisionRequest(
        user_id="u1",
        utterance="我想去医院看病",
        extra={"scene_type": "outdoor"},
    )
    reply = core.handle(req)
    print("Assistant:", reply)

