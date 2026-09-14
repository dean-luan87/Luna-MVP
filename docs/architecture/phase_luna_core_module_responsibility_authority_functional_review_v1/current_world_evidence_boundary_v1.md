# Current World Evidence Boundary v1

## Evidence path

Observation/FPO and Provider governance produce evidence refs. A Current World
adapter may assemble an observation-local or fused candidate from those refs.
Where evidence is field-relevant, a separate Field Event candidate may be
created and sent through Field Event Admission; Current World formation does
not bypass that path.

`Observation → evidence/handoff → Current World candidate` is therefore a
candidate representation path. `Observation → field event candidate → Field
Event Admission → Field Reducer` is the governed source-state path. A Field
transition may subsequently be represented in a new Current World candidate.

## Evidence classification

- Provider/Observation evidence: evidence, not Truth.
- Field-admitted state: best-known operational source state, not metaphysical
  Truth.
- Current World attribute/relation: derived candidate, with provenance.
- uncertainty/conflict/missing refs: preserved, not silently resolved.

## Forbidden promotion

Current World must not promote a candidate entity to Field, promote an
inference to a fact, create a World Truth record, mutate Current World in place,
or convert A hypothesis refs into active hypotheses. A determines cognitive
meaning after receiving the candidate.
