# Asset reuse matrix

| Need | Existing asset | Use |
|---|---|---|
| Replay ingress | `ObservationGatewayEngineV1`, `ControlledReplayInputV1` | Reused directly |
| A-Route cognition | `ARouteOrchestrationEngineV1` | Reused directly |
| Sufficiency, Gap, Re-observation, Revision, Stop | `cognitive_loop_types_v1.py` and CState engine | Reused as canonical producers |
| Loop lifecycle | `Cognitive Flow Governance` contracts | Referenced; no new semantic owner |
| Closure candidate/acceptance | `ClosureAssessmentCandidateV1`, `ClosureDecisionCandidateV1`, `LifecycleClosureCandidateV1` | Reused; `decision_ref` is exposed as closure acceptance ref |
| Assimilation | `BrainAssimilationCandidateV1` | Reused; candidate-only handoff |
| Outcome/closure record | Existing `CognitiveOutcomeCandidateV1`, `LoopClosureRecordCandidateV1` | Reused as bounded references |
| Brain request/need binding | Missing integration surface | Added narrowly as a candidate-only Brain-domain binding with `OWNER_UNRESOLVED` canonical owner status |

Existing candidate-only lifecycle closure code remains synthetic-only and is
not used as proof of A-Route cognition.
