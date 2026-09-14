# M10 Field / Context / Current World — Module Review

## Identity and purpose

This module is three distinct boundaries: Field State Reducer/read model, Context Foundation, and Cognitive State Formation's Current World candidate. Evidence: `core/field_state_reducer/`, `core/field_state_read_model/`, `core/context_foundation/`, `current_world_types_v1.py`, and B1/B2 integrations. If removed, Luna loses authoritative environment state reduction, contextual validity/carryover, and a candidate integrated current-world representation.

## Functions and authority

Field Reducer `CORE`: reduce/update Field State under its policy; read model is projection/reference. Context Foundation `CORE`: assemble context/carryover/projection refs and validity. Current World `CORE`: candidate representation of observations, hypotheses, field/context refs and uncertainty; it does not declare World Truth. None decides Need, sufficiency, continuation, or Concern.

Responsibility: Field owner owns field transitions; Context owner owns context assembly/validity; Current World formation owns candidate structural validity; A judges semantic significance; Brain governs global safety/resource implications.

## Inputs, outputs, state, lifecycle

Inputs: field events/state, context sources/carryover, observations/evidence, hypotheses, attention, intent. Outputs: authoritative Field/Context refs and candidate Current World refs to A/Brain. Field/Context are authoritative source state; Current World is candidate/reference-only. Lifecycle: update/reduce → version → assemble candidate → supersede on change → A reassesses → archive.

## Communication and negative boundaries

Allowed: source events→Field/Context; Field/Context→Working Envelope/State Formation/A; Current World→A/Brain; Loop stores refs. Forbidden: Current World→World Truth, Field/Context→Need/Loop semantic control, direct Provider selection. B receives bounded refs only.

## Walkthroughs

1. Normal: event reduces Field, Context packages validity, Current World candidate is assembled; A assesses.
2. Conflict/stale: reducer/read model exposes conflict or version change; A decides semantic consequence; no Loop inference.
3. Role/task/emotion change: source versions update envelope/invalidation; A judges impact and Brain handles grant policy.

## Overlap, gaps, evolution, disposition

Overlap: `STATE_DUPLICATION` risk among Field, Context, Current World; `TERMINOLOGY_OVERLAP` current world vs truth. Gap: explicit inter-module version/invalidation contract and authoritative envelope generator. They may evolve as clean source-state/representation boundaries, never A/Brain semantic substitutes. **Disposition: KEEP / CLARIFY**.

**Ledger summary:** authority = Field/Context source-specific updates; Current World candidate only; state = authoritative source + candidate representation; receiver = A/Brain/envelope; confidence = medium-high.
