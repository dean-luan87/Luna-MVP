# tests/test_flow_engine.py
from core.flow_templates.templates_registry import FlowTemplateRegistry
from core.flow_templates.hospital_go_template import GoHospitalTemplate
from core.flow_engine.planner import FlowPlanner, PlanningInput
from core.flow_engine.runtime import FlowRuntime


def test_hospital_flow_plans_and_runs():
    # 准备模板注册表和 Planner / Runtime
    registry = FlowTemplateRegistry()
    registry.register_template(GoHospitalTemplate())

    planner = FlowPlanner(template_registry=registry)
    runtime = FlowRuntime()

    planning_input = PlanningInput(
        user_id="u1",
        intent="go_hospital",
        scene_type="outdoor",
        raw_utterance="我想去医院看病",
        extra={},
    )

    instance = planner.plan(planning_input)
    assert instance is not None
    assert instance.definition.entry_node_id == "ask_hospital"

    runtime.start(instance)

    ctx = instance.context
    assert instance.finished is True
    prompts = ctx.data.get("prompts")
    assert isinstance(prompts, list)
    # 预期流程：问医院 → 导航提示 → 到达等待提示
    assert len(prompts) >= 3

    # 第一条需要是问医院的问题
    assert "你要去哪个医院" in prompts[0]












