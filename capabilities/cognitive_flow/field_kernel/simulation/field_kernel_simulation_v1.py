"""Pure, fixture-only Field Kernel scenario assembly v1.

Fixtures include an Admitted Event and a separately declared Reducer output
representation. No event reduction is implemented or invoked here.
"""

from __future__ import annotations

from typing import Any, Dict

from capabilities.cognitive_flow.field_kernel.core.field_identity_v1 import FieldIdentityV1
from capabilities.cognitive_flow.field_kernel.core.field_relation_v1 import FieldRelationV1
from capabilities.cognitive_flow.field_kernel.core.field_state_v1 import field_state_from_reducer_output_v1
from capabilities.cognitive_flow.field_kernel.core.field_unit_v1 import FieldUnitV1
from capabilities.cognitive_flow.field_kernel.reducer_adapter_v1 import FieldKernelReducerAdapterV1
from capabilities.cognitive_flow.field_kernel.snapshot_api_v1 import get_field_snapshot


_SCENARIO_FIXTURES_V1: Dict[str, Dict[str, Any]] = {
    "shopping_mall": {"field_type": "shopping_mall", "unit_type": "entrance", "state_type": "accessibility_state", "state_value": {"access": "closed_candidate"}},
    "airport": {"field_type": "airport", "unit_type": "gate", "state_type": "accessibility_state", "state_value": {"access": "restricted_candidate"}},
    "street": {"field_type": "street", "unit_type": "crossing", "state_type": "path_state", "state_value": {"path": "obstructed_candidate"}}
}


def simulate_field_kernel_scenario(scenario_name: str):
    """Assemble a Snapshot using fixture-only admitted/reducer-produced inputs.

    This function is not a runner. It calls no external capability, model,
    database, network, Admission logic, or Reducer implementation.
    """

    fixture = _SCENARIO_FIXTURES_V1.get(scenario_name)
    if fixture is None:
        raise ValueError("unsupported Field Kernel simulation scenario")

    field_id = f"field:{scenario_name}:v1"
    unit_id = f"unit:{scenario_name}:primary:v1"
    trace_ref = f"trace:simulation:{scenario_name}:v1"
    admitted_event = {
        "admission_status": "admitted_event",
        "event_ref": f"event:{scenario_name}:v1",
        "field_ref": field_id,
        "reducer_eligible": True,
        "reducer_input_candidate": {"event_id": f"event:{scenario_name}:v1", "field_ref": field_id, "trace_ref": trace_ref, "admission_status": "admitted_event", "reducer_eligible": True},
        "temporal_assessment": {"status": "assessed", "timezone_aware": True},
        "evidence_refs": [f"evidence:simulation:{scenario_name}:v1"],
        "source_chain": ["simulation"],
        "trace_ref": trace_ref
    }
    adapter_input = FieldKernelReducerAdapterV1.adapt_admitted_event(admitted_event)
    identity = FieldIdentityV1(field_id=field_id, field_type=str(fixture["field_type"]), parent_field_ref=None, physical_context={"simulation": True}, social_context={}, task_context={}, provenance={"trace_ref": trace_ref, "source": "simulation"})
    unit = FieldUnitV1(unit_id=unit_id, unit_type=str(fixture["unit_type"]), parent_field=field_id, attributes={}, provenance={"trace_ref": trace_ref})
    relation = FieldRelationV1(relation_id=f"relation:{scenario_name}:contains:v1", subject_ref=field_id, predicate="contains", object_ref=unit_id, provenance={"trace_ref": trace_ref})
    reducer_produced_state = {
        "produced_by": "field_state_reducer",
        "reducer_output_ref": f"reducer-output:simulation:{scenario_name}:v1",
        "state_id": f"state:{scenario_name}:v1",
        "target_ref": unit_id,
        "state_type": fixture["state_type"],
        "value": fixture["state_value"],
        "valid_time": {"effective_from": "2026-01-01T00:00:00Z"},
        "evidence_refs": adapter_input.evidence_refs,
        "source_chain": adapter_input.source_chain,
        "trace_ref": trace_ref,
        "provenance": {"admitted_event_ref": adapter_input.event_ref}
    }
    state = field_state_from_reducer_output_v1(reducer_produced_state)
    return get_field_snapshot(field_id, identity, (unit,), (relation,), (state,), "2026-01-01T00:00:00Z", {"simulation": True, "admitted_event_ref": adapter_input.event_ref})
