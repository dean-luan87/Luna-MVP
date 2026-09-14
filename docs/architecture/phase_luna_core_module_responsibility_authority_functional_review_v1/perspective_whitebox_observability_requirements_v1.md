# Perspective White-Box Observability Requirements v1

Current White-box scope should expose:

`Base Attribute → Role condition → Role knowledge/responsibility/skill/
capability-relevance source → Derived Augmented Attribute → provenance →
Projection version → Semantic/Cognitive-State handoff → A consumption`

The source-mutation field must remain false.

Required current synthetic/static coverage should include:

- same base entity with different Roles;
- new Role projected over old data;
- Role invalidation;
- Role A isolation from Role B;
- same Role with different Concern producing different relevance;
- Role removal/invalidation removing or invalidating the overlay without
  damaging base information;
- unrelated Role producing no meaningful augmentation;
- no duplicate world object;
- no Role-specific Memory duplication;
- complete projection provenance.

Emotion-related White-box cases are `DEFERRED` and are not part of the current
test definition.

No UI, runtime, cache, or neural implementation is introduced here.

## Implementation-agnostic network language

The architecture may later be implemented as one shared information substrate
plus many Role-conditioned projections. Possible implementations include
multi-head networks, role-conditioned Transformers, dynamic adapters,
LoRA-style adapters, Hypernetworks, Mixture-of-Experts, or graph-based
relation projection. This is semantic architecture language, not a required
neural topology: one physical neural head does not equal one Role.
