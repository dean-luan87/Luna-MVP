# Ownership and boundaries

| Boundary | Canonical owner | May do | May not do |
| --- | --- | --- | --- |
| Evidence | Observation Gateway evidence boundary | supply admitted, source-linked evidence | become an Event or mutate Field directly |
| Evidence → Event bridge | Field/Event integration adapter | explicit shape mapping and lineage preservation | interpret opaque payload or choose a winner |
| Event Admission | Field Event Admission | validate structure and temporal eligibility | mutate Field State |
| Field State reduction | Field State Reducer | reduce admitted events into a controlled candidate | accept raw evidence, call providers, write Memory |
| Context | Context Foundation | provide scoped, read-only projections | create facts or mutate Field |
| Current World | Cognitive State Formation | assemble a candidate representation | become a writable Field shadow or Truth owner |

Field State Reducer remains the only Field State mutation authority. In this
controlled skeleton the mutation/persistence effect is deliberately not
implemented, so every emitted state representation has
`candidate_only=true` and `state_mutation_executed=false`.

Context provenance means interpretive/reference basis only. It is never
substituted for Evidence provenance or World Truth.
