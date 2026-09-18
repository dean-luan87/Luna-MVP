from __future__ import annotations

import inspect

from capabilities.midplatform.core.cognitive_flow.integration.a_owned_semantic_decision_loop_bridge_controlled import (
    a_owned_semantic_decision_engine_v1 as semantic_engine,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_owned_semantic_decision_loop_bridge_controlled import (
    loop_mechanical_bridge_v1 as mechanical_bridge,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_owned_semantic_decision_loop_bridge_controlled import (
    a_owned_semantic_decision_adapter_v1 as adapter,
)


def test_semantic_and_mechanical_functions_have_one_active_boundary() -> None:
    semantic_source = inspect.getsource(semantic_engine)
    mechanical_source = inspect.getsource(mechanical_bridge)

    assert "def form_cognitive_semantic_judgment(" in semantic_source
    assert "def bridge_bundle_to_loop(" not in semantic_source
    assert mechanical_source.count("def bridge_bundle_to_loop(") == 1
    assert "from .loop_mechanical_bridge_v1 import bridge_bundle_to_loop" in inspect.getsource(adapter)


def test_mechanical_bridge_contract_surface_remains_equivalent() -> None:
    payload = adapter.build_a_owned_semantic_decision_run_v1()
    mechanical_cases = [case for case in payload["cases"] if str(case["scenario_id"]).startswith("MC-")]

    assert len(mechanical_cases) == 5
    assert all(case["passed"] is True for case in mechanical_cases)
    assert all(case["rejected_semantic_authority_violation"] == 0 for case in mechanical_cases)
    assert payload["summary"]["key_guards"]["loop_has_no_semantic_authority"] is True
