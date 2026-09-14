# M06 Cognitive State Formation — Module Review

## Identity and purpose

Canonical name: Cognitive State Formation. Evidence: `capabilities/midplatform/core/cognitive_state_formation/`, `CurrentWorldCandidateV1`, attention/hypothesis types, and B2 current-world flow. If removed, Luna loses a structured candidate representation of attention, hypotheses, observations, context, field state, uncertainty, conflict, and Current World.

## Functions and authority

`CORE`: assemble candidate state representation and source-version lineage. `SUPPORTING`: candidate builders, validation, trace/provenance. `COMPATIBILITY_ONLY`: controlled B1/B2 handoff packaging. It may construct `CANDIDATE_ONLY` Current World/Hypothesis/Attention representations but has no authority to declare World Truth, select Need, judge sufficiency, decide continuation, mutate Field/Context/Intent, or control Loop.

Responsibility is representation validity and provenance, not semantic adoption. A evaluates relevance and meaning; source owners remain responsible for authoritative source updates; Brain adjudicates global consequences.

## Inputs, outputs, state, lifecycle

Inputs: observations/evidence, Field/Context refs, Attention, hypotheses, Intent, uncertainty/conflict, state versions. Outputs: candidate Current World/state/hypothesis refs to A and governance. State is candidate/reference-only; authoritative source duplication is forbidden. Lifecycle: assemble → validate → supersede on source change → hand off/archive.

## Communication and negative boundaries

Allowed: source state/evidence→formation; formation→A/Brain candidate envelopes; Loop stores refs. Forbidden: formation→Need/Capability/Provider/Loop semantic decision, Current World truth claim, direct Intent mutation. Known risk is A and Dynamic Flow both interpreting state-derived values.

## Walkthroughs

1. Normal: combine evidence/context/field refs into a Current World candidate; A assesses.
2. Conflict/stale: emit uncertainty/conflict or stale version; no automatic A decision.
3. Field/context change: build a new candidate lineage; A judges material impact and Brain governs source/grant consequences.

## Overlap, gaps, evolution, disposition

Overlap: `STATE_DUPLICATION` risk with Context/Field/Current World and `SEMANTIC_OVERLAP` if formation starts calculating Need/sufficiency. Gap: explicit representation-vs-decision contract and unified envelope source. It may evolve as a state assembly/lineage service, never an A substitute or World Truth owner. **Disposition: KEEP / NARROW**.

**Ledger summary:** authority = representation validity only; state = candidate representation; receiver = A/Brain; confidence = medium-high.
