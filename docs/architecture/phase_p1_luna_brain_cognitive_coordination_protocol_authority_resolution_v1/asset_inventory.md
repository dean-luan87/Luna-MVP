# Existing Owner Audit

## Canonical assets inspected

| Asset | Evidence | Classification | Authority relevant to this phase |
|---|---|---|---|
| Cognitive Flow registry | `capabilities/midplatform/core/cognitive_flow/cognitive_flow_registry_v1.py:7-24` | canonical independent owner | `Cognitive Flow Governance`; lifecycle state vocabulary |
| Cognitive Flow input/output | `capabilities/midplatform/core/cognitive_flow/cognitive_flow_io_types_v1.py:41-82` | canonical candidate protocol | candidate flow envelope and output transitions; not request admission |
| Cognitive Flow state/transition types | `cognitive_cycle_state_types_v1.py`, `cognitive_cycle_transition_types_v1.py` | canonical lifecycle candidates | mechanical state/transition references; no semantic override |
| Lifecycle closure adapter | `.../cognitive_loop_lifecycle_closure_adapter_v1.py:12-23` | canonical controlled adapter | identifies Cognitive Flow Governance and candidate closure surface |
| Cognitive State Formation registry | `capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_registry_v1.py:7-25` | canonical independent owner | state formation owner and boundary owner |
| Cognitive loop contracts | `capabilities/midplatform/core/cognitive_state_formation/cognitive_loop_types_v1.py:17-75` | canonical cognitive candidates | Sufficiency, Gap, Revision, Stop contracts |
| Cognitive loop validator | `cognitive_loop_types_v1.py:77-135` | canonical guard | verifies owner and causal links; not a Brain authority |
| Cognitive State Formation engine | `cognitive_state_formation_engine_v1.py:549-630` | canonical producer | produces Sufficiency/Gap/Re-observation/Revision/Stop |
| Cognitive Need bridge | `capabilities/midplatform/model_manager/registries/universal_capability_slot/cognitive_need_capability_requirement_bridge_types_v1.py:12-101` | canonical candidate bridge | carries Need into capability requirement formation; does not register Brain Need |
| Dynamic Cognitive Regulation | `capabilities/midplatform/core/dynamic_cognitive_regulation/dynamic_cognitive_regulation_registry_v1.py:8` and its ownership guards | canonical independent owner | regulates candidate flow/resource signals; not request or closure authority |
| Field Perception Orchestrator | `capabilities/midplatform/field_perception_orchestrator/integration/field_perception_active_observation_control_engine_v1.py:22-24,398-415` | canonical independent owner | observation/re-observation control boundary |
| Intent Governance | `capabilities/midplatform/core/intent_governance/intent_registry_v1.py` | canonical independent owner | Intent authority; outside Brain mutation |
| Context Foundation | context foundation registry/integration | canonical independent owner | Context authority; outside Brain mutation |
| Decision Governance | `capabilities/midplatform/core/decision_governance/decision_registry_v1.py:8-15` | canonical independent owner | Decision authority; Action and Task remain downstream |
| Task Manager | `capabilities/midplatform/core/task_manager/module/` | canonical downstream service/owner | Task lifecycle and execution boundary; outside Brain cognition |
| Memory/Experience Governance | `cognitive_memory_experience_registry_v1.py:7,26-39` | canonical independent owner | admission/mutation authority for Memory/Experience |
| Cognitive Learning Governance | `cognitive_learning_registry_v1.py:7,42-56` | canonical independent owner | learning admission/mutation authority |
| Self Governance | `capabilities/midplatform/core/self_governance/self_governance_registry_v1.py:7` | canonical independent owner | Self/identity references; outside Brain mutation |
| Capability/System protocol contracts | Cognitive Flow, Observation Gateway, capability and runtime-admission contracts | canonical boundary contracts | constrain admission and handoff; none establishes Brain owner |
| Brain Golden Baseline / Integrated Closure | `capabilities/midplatform/core/brain_golden_baseline/`; architecture review `module_brain_review_v1.md:5,11,31` | metadata/candidate governance; runtime gap | architectural Brain responsibility evidence, not a unified runtime owner |
| Brain closure integration | `.../brain_cognitive_loop_closure_assimilation_controlled/` | controlled boundary adapter | uses Brain responsibility domain with `OWNER_UNRESOLVED`; no new owner |

## Audit conclusion

The repository contains strong owner registries for existing modules, but no
concrete Brain runtime registry, request-admission API, Need registry,
closure-acceptance owner, or generic assimilation dispatcher. Architectural
references to Brain remain responsibility-domain references unless backed by
one of those executable contracts.

The inspected assets therefore classify as follows: existing registries and
engines are canonical independent owners or services; Cognitive Flow and the
controlled closure package are candidate protocol/mechanics surfaces; Brain
request, Need admission, semantic closure acceptance, and generic assimilation
routing are unresolved; no overlapping asset was selected as a replacement
Brain owner.
