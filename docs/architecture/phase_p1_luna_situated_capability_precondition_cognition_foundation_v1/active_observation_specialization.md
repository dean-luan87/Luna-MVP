# Active Observation specialization

The existing Active Observation Preconditions implementation is the first
specialization of the generic semantics:

| Generic | Active Observation |
|---|---|
| Capability Necessity | `ObservationNecessityCandidateV1` |
| Capability condition declaration | `MinimumObservationConditionsV1` dimensions |
| Minimum condition resolution | `MinimumSituatedConditionRequirementV1` from Information Need |
| Situated State | `SelfPerceptualViewpointStateV1` + `RelativeObservationStateV1` |
| Capability Feasibility | `ObservationFeasibilityCandidateV1` |
| Capability Condition Gap | `ObservationConditionGapV1` |
| Capability Adjustment Need | `RelativeObservationAdjustmentNeedV1` |
| Capability Opportunity | `ObservationWindowCandidateV1` |
| Capability Eligibility | `ObservationCapabilityEligibilityCandidateV1` |

This phase maps the already implemented controlled Active Observation state
through the generic evaluator. It does not run OCR and does not refactor the
existing Active Observation code.
