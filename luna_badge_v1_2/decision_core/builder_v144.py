# decision_core/builder_v144.py
from core.flow_templates.templates_registry import FlowTemplateRegistry
from core.flow_templates.hospital_go_template import GoHospitalTemplate
from core.flow_engine.planner import FlowPlanner
from core.flow_engine.runtime import FlowRuntime
from core.query_engine.query_manager import QueryEngine
from task_chain.task_chain_manager import TaskChainManager
from decision_core.decision_core import DecisionCore


def build_decision_core_v144() -> DecisionCore:
    # 模板注册
    registry = FlowTemplateRegistry()
    registry.register_template(GoHospitalTemplate())

    planner = FlowPlanner(template_registry=registry)
    runtime = FlowRuntime()
    query_engine = QueryEngine()
    task_manager = TaskChainManager(runtime=runtime)

    core = DecisionCore(
        flow_planner=planner,
        flow_runtime=runtime,
        query_engine=query_engine,
        task_manager=task_manager,
    )
    return core

