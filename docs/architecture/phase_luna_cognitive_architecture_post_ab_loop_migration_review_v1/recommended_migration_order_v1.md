# Recommended Migration Order

## P0 — authority cleanup contracts

- Define A-owned semantic input/output envelope for Dynamic Flow decisions.
- Mark Loop continuity semantic fields as supplied decision refs, not Loop decisions.
- Freeze Brain grant issuance/revocation/assimilation API shape without implementing runtime.

## P1 — controlled integration

- Add one A working-envelope adapter composing Current World, Context, Field, Role, Attention, Task, Intent, Emotion and state refs.
- Route A Need to existing Capability Requirement → Scope → Resolution → Observation admission candidates.
- Route admitted evidence/outcomes back to A state assessment.
- Add controlled invalidation tests for state/Field/Role/Task/Emotion changes.

## P2 — consolidation

- narrow A Route stage labels to orchestration;
- preserve Dynamic Flow generic state/evidence computation while deprecating semantic authority output;
- consolidate B-CR terminology and historical Route B references;
- consolidate trace/provenance envelope assembly.

## Defer

Do not implement Brain runtime, Semantic Module, Experience Filter runtime, real multi-provider execution, scheduler, child Loop spawning, Action, Learning, Memory/Experience mutation, or semantic compression.

Stop condition for the next phase: one controlled A working-envelope + Requirement/Observation admission seam with explicit grant invalidation and no new owner.
