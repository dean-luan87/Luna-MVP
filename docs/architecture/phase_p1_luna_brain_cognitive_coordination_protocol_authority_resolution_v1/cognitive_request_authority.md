# Cognitive Request Authority

| Responsibility | Producer | Admission/lifecycle owner | Semantic owner | Mutation owner | Decision |
|---|---|---|---|---|---|
| Request intent | Brain responsibility domain | `OWNER_UNRESOLVED` | `OWNER_UNRESOLVED` | `OWNER_UNRESOLVED` | `OWNER_UNRESOLVED` |
| Request admission | Brain-domain producer | `OWNER_UNRESOLVED` | `OWNER_UNRESOLVED` | no mutation | `OWNER_UNRESOLVED` |
| Loop materialization | admitted protocol caller | Cognitive Flow Governance for candidate lifecycle mechanics | `OWNER_UNRESOLVED` for Brain semantic acceptance | Cognitive Flow candidate state only | `RESOLVED_TO_EXISTING_OWNER` for mechanics |
| Lifecycle start transition | admitted Cognitive Flow input | Cognitive Flow Governance | no semantic Brain claim | candidate-only transition | `RESOLVED_TO_EXISTING_OWNER` |

Evidence: `CognitiveFlowInputV1` accepts `scenario_id`, `cycle_snapshot`,
owner references and `candidate_only`/`synthetic_only` flags, while
`CognitiveFlowOutputV1` returns candidate transitions and a candidate final
state (`cognitive_flow_io_types_v1.py:41-82`). The registry names Cognitive
Flow Governance as the canonical owner and explicitly forbids mutation of
Intent, Field, Memory, Learning, and source-owner output
(`cognitive_flow_registry_v1.py:7,36-78`).

This proves lifecycle mechanics, not admission of a Brain Cognitive Request.
No concrete request admission contract was found. Therefore the phase does
not assign request acceptance to Cognitive Flow Governance.
