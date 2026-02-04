# tests/conftest.py
import pytest

from core.flow_templates.templates_registry import FlowTemplateRegistry
from core.flow_templates.hospital_go_template import GoHospitalTemplate
from core.flow_engine.planner import FlowPlanner
from core.flow_engine.runtime import FlowRuntime
from core.query_engine.query_manager import QueryEngine
from decision_core.decision_core import DecisionCore


@pytest.fixture
def flow_template_registry() -> FlowTemplateRegistry:
    registry = FlowTemplateRegistry()
    registry.register_template(GoHospitalTemplate())
    return registry


@pytest.fixture
def flow_planner(flow_template_registry: FlowTemplateRegistry) -> FlowPlanner:
    return FlowPlanner(template_registry=flow_template_registry)


@pytest.fixture
def flow_runtime() -> FlowRuntime:
    return FlowRuntime()


@pytest.fixture
def query_engine() -> QueryEngine:
    return QueryEngine()


@pytest.fixture
def decision_core(flow_planner: FlowPlanner, flow_runtime: FlowRuntime, query_engine: QueryEngine) -> DecisionCore:
    return DecisionCore(
        flow_planner=flow_planner,
        flow_runtime=flow_runtime,
        query_engine=query_engine,
    )

