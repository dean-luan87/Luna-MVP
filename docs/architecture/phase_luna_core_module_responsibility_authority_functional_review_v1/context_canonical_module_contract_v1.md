# Context Canonical Module Contract v1

## Adjudication

**Disposition: NARROW.** Context remains an independent assembly boundary, not
an owner of every state it references.

## Canonical purpose

Context is Luna's versioned situation-framing and source-reference assembly
boundary: it describes the conditions under which admitted reality and
cognitive work are being used, preserves temporal validity and provenance, and
returns a coherent reference-only context candidate without rewriting the
underlying Field, Current World, Role, Intent, Task, Memory or policy state.

## Precise answer

Context describes **the situation under which reality is used**, not reality
itself. It can bind time, location, social setting, source projections,
applicability and governance constraints. It does not become an alternate
Field or Current World store.

## Repository evidence

`core/context_foundation/context_foundation_types_v1.py` defines
`ContextAssemblyInputV1`, `ContextEnvelopeCandidateV1` and temporal scope
references. The protocol says Context assembly owns no source object. The
skeleton validates projections, preserves unknowns/source ownership, assembles
an immutable reference candidate and explicitly disables source mutation,
runtime generation, intent/causal/decision outputs and external lookup.

The context/world integration creates observation, Field and Current World
handoff candidates while retaining `context_mutation=False`,
`reference_only=True`, `candidate_only=True` and `truth_declared=False`.

## Authority and responsibility

Context may authoritatively own the identity/version/validity of its assembled
context envelope, subject to the existing contract. It may select which valid
source refs are included for that envelope. It may not authoritatively mutate a
source projection or decide the semantic consequence of its contents.

Context is responsible for incorrect source binding, version/temporal validity,
provenance loss, stale acceptance and cross-source assembly contamination. It
is not responsible for Field transitions, Current World truth, A reasoning,
Intent lifecycle, Task lifecycle or Brain governance.

## Inputs and outputs

Inputs may include time/temporal scope, location, Field projection,
Observation/Evidence projection, Current World ref, Role/Perspective ref,
Intent ref, Task ref, device/runtime/social/user refs, and
permission/resource/safety refs. These are source-owned references unless a
separate Context contract explicitly owns assembly metadata.

Outputs are a context envelope candidate, source-version/validity markers,
missing/unknown/conflict indicators, trace and provenance refs. Primary
receivers are Working Envelope/Cognitive State Formation and A; Brain may
consume the ref for governance but does not become Context owner.

## Negative boundary

No Field mutation, Current World fusion authority, World Truth declaration,
Semantic expansion/folding, Need/Hypothesis/Sufficiency judgment, Attention
scheduling, Capability/Provider selection, Task/Intent mutation, Memory write,
or Action execution.

## Status

`NO_GAP` for the narrow assembly contract; `RUNTIME_GAP` remains because the
inspected implementation is explicitly a controlled skeleton with no real
context generation or mutation.
