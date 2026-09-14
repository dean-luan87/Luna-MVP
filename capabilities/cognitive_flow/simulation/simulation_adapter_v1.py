"""Deterministic simulation input adapter for Cognitive Primitive Layer v1."""

from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.cognitive_flow.cognitive_primitives.api_v1 import create_observation
from capabilities.cognitive_flow.cognitive_primitives.types_v1 import ObservationEventV1


SIMULATION_SCENARIOS_V1: Dict[str, Dict[str, Any]] = {
    "shopping_mall": {
        "observation_type": "simulated_scene_observation",
        "payload": {"scenario": "shopping_mall", "scene_label_candidate": "indoor_commercial"},
    },
    "airport": {
        "observation_type": "simulated_scene_observation",
        "payload": {"scenario": "airport", "scene_label_candidate": "transport_terminal"},
    },
    "street": {
        "observation_type": "simulated_scene_observation",
        "payload": {"scenario": "street", "scene_label_candidate": "public_road"},
    },
}


def simulation_input_to_observation(value: Mapping[str, Any]) -> ObservationEventV1:
    scenario = value.get("scenario")
    if scenario not in SIMULATION_SCENARIOS_V1:
        raise ValueError("unsupported simulation scenario")
    trace_ref = value.get("trace_ref")
    source_ref = value.get("source_ref") or f"simulation:{scenario}"
    occurred_at = value.get("occurred_at") or "2026-01-01T00:00:00Z"
    observed_at = value.get("observed_at") or occurred_at
    template = SIMULATION_SCENARIOS_V1[scenario]
    return create_observation(
        {
            "observation_id": f"simulation_observation:{scenario}",
            "source_ref": source_ref,
            "observation_type": template["observation_type"],
            "occurred_at": occurred_at,
            "observed_at": observed_at,
            "payload": dict(template["payload"]),
            "evidence_refs": [f"simulation_evidence:{scenario}"],
            "trace_ref": trace_ref,
            "provenance_refs": [f"simulation_case:{scenario}"],
        }
    )

