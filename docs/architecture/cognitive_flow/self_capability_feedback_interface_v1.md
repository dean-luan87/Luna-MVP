# Self Capability Feedback Interface v1

## Direction

```text
Capability State Changed
        ↓
Self Capability Context Candidate
        ↓
Brain Awareness
```

Capability availability or quality is an external state observation. It can
provide a candidate limitation, confidence change, or improvement candidate to
Self Model and Brain. It cannot directly redefine Identity, Goal, Reality, or
State.

## Controlled example

OCR degradation may yield:

```text
capability: text_evidence_extraction
state: degraded
constraint: low_light
confidence_effect: decrease_candidate
```

The result is not “Luna cannot read”. Self Capability remains an abstract,
validated candidate and must preserve uncertainty and provenance. Adoption, if
ever needed, follows Candidate → Validation → Adoption and the Reducer remains
the sole State mutation authority.

## Boundary

Provider failure does not become an automatic Self update. Brain receives
Capability Awareness through the governed context interface; it does not receive
provider internals or raw model parameters.
