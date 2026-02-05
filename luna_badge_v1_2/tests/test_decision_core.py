# tests/test_decision_core.py
from core.framework.decision.decision_core import DecisionCore, DecisionRequest
from core.flow_templates.templates_registry import FlowTemplateRegistry
from core.flow_templates.hospital_go_template import GoHospitalTemplate
from core.flow_engine.planner import FlowPlanner
from core.flow_engine.runtime import FlowRuntime
from core.query_engine.query_manager import QueryEngine


def build_decision_core_for_test() -> DecisionCore:
    registry = FlowTemplateRegistry()
    registry.register_template(GoHospitalTemplate())
    planner = FlowPlanner(template_registry=registry)
    runtime = FlowRuntime()
    query_engine = QueryEngine()
    return DecisionCore(
        flow_planner=planner,
        flow_runtime=runtime,
        query_engine=query_engine,
    )


def test_decision_core_routes_to_hospital_template():
    core = build_decision_core_for_test()
    req = DecisionRequest(
        user_id="u1",
        utterance="我想去医院挂号",
        extra={"scene_type": "outdoor"},
    )
    reply = core.handle(req)
    # 预期第一句为"你要去哪个医院？"
    assert "你要去哪个医院" in reply
