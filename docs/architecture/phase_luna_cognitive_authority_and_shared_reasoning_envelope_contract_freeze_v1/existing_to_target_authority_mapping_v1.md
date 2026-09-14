# Existing to Target Authority Mapping

This mapping is static. No listed future action is executed in this phase.

| Current file/class/function | Current behavior | Target authority | Future action | Difficulty / risk |
|---|---|---|---|---|
| cognitive_dynamic_loop_engine_v1.py, run_case | advances state, selects Need, evaluates evidence, sufficiency and next step | A for semantics; Loop for mechanics | MOVE_DECISION_OUT | High / high regression |
| cognitive_dynamic_loop_engine_v1.py, _select_next_need | selects next Need from plan refs | A | MOVE_DECISION_OUT | Medium / high |
| cognitive_dynamic_loop_engine_v1.py, _reconsideration | forms reconsideration candidate | A/B; Flow transports | WRAP | Medium / medium |
| cognitive_dynamic_loop_types_v1.py, GoalSufficiencyCandidateV1 | carries sufficiency/stop candidate | A local, Brain global | WRAP | Medium / high |
| LoopLocalStateCandidateV1 | stores Need, hypothesis lineage, transitions, pause/wait and closure | Shared Loop Engine mechanics | KEEP | Low / low |
| LoopIdentityCandidateV1 | stores concern and external owner refs | Brain concern ref plus Loop identity | KEEP | Low / low |
| ContinuityAssessmentCandidateV1 | compares authoritative refs | A/B semantic assessment | MOVE_DECISION_OUT | Medium / medium |
| ResumeAssessmentCandidateV1 | emits KEEP/SUPERSEDE/REPLAN/COMPLETE/WAITING | Brain/A semantic decision | WRAP | High / high |
| CapabilityCandidatePathV1 | records Need to Requirement/Scope/Resolution path | A/B request; Capability resolves | KEEP | Low / low |
| CapabilityGrowthGuardCandidateV1 | records growth gates | shared governance; A/B requests | WRAP | Medium / medium |
| BranchReservationCandidateV1 | stores branch/merge reservation | Brain concern governance | KEEP | Low / low |
| ClosureAssessmentCandidateV1 | suggests closure reason and eligibility | A/B request; Brain/Flow accepts | MOVE_DECISION_OUT | Medium / high |
| LifecycleClosureCandidateV1 | records accepted lifecycle closure mechanics | Shared Loop Engine after command | CONVERT_TO_MECHANICAL | High / high |
| BrainAssimilationCandidateV1 | carries outcome handoff | Brain assimilation | KEEP | Low / low |
| ARouteProductLoopIntegrationEngineV1 | assembles broad route stages | A orchestration plus external owners | NARROW / WRAP | High / medium |
| ARouteOrchestrationEngineV1 | stages lifecycle and handoffs | orchestration only | KEEP | Low / low |
| B2 adapter / run_b2_case | directly calls State Formation and Cognitive Flow | A/B input adapter; Flow mechanics | WRAP | Medium / high |
| B3 adapter | maps B2 refs to Intent, Decision and Task | downstream governed path | KEEP | Medium / medium |
| task_manager_capability_router_v1.py | maps Task capability requirements to request candidates | Task request surface; Capability resolves | NARROW | Medium / medium |
| B4 Outcome Evaluation adapter | emits feedback, reconsideration and observation need candidates | Outcome emits; A consumes | KEEP | Low / low |
| Observation Gateway | normalizes/admit observation candidate | Observation owner | KEEP | Low / low |
| Capability resolution functions | Scope, Resolution, Invocation candidates | Capability/Provider Governance | KEEP | Low / low |
| ExperienceCandidateV1 / MemoryCandidateV1 | candidate-only historical boundary | Experience/Memory Governance | KEEP | Low / low |

## Migration rule

MOVE_DECISION_OUT means future adapters receive semantic decisions from A/B
and preserve existing candidate output shape during transition. It does not
mean immediate deletion or canonical type modification.
