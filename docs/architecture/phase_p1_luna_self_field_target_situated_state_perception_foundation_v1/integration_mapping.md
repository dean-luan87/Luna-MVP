# Integration Mapping

The new layer is additive inside the existing Situated Capability
Preconditions owner:

1. Existing Minimum Situated Condition Resolution supplies the required
   condition refs for the current Information Need.
2. Situated State Perception derives condition candidates from Self/Field/
   Target/Relation inputs.
3. The derived `SituatedCapabilityStateV1` is passed to the existing generic
   precondition evaluator.
4. Existing Feasibility consumes the resolved minimum and the derived
   condition statuses.
5. Existing Condition Gap, Adjustment Need, Opportunity, and Eligibility
   semantics remain the downstream owners.

The previous direct state field remains a compatibility field, but this phase
never supplies it from a fixture.  The new path fills it only from the
derived candidate set and also carries the full candidate records.

No Provider Runtime, Observation Gateway, A-Route, OCR, or model path was
modified.
