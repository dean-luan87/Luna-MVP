# Cognitive State Ordering Review

## Candidate flows

- Envelope → Cognitive State → Semantic Outline → A: risks State Formation owning semantic input organization.
- Envelope → Semantic Outline → Cognitive State → A: makes the snapshot structurally informed by the semantic representation.
- Envelope → Semantic Outline → A, with Cognitive State as parallel snapshot: preserves separation but needs explicit synchronization.
- Envelope → Cognitive State → A, with Semantic Module optional: risks semantic transformation being hidden inside A.

## Target ordering

**Working Envelope → Semantic Working Outline and source snapshot formation (parallel, version-linked) → A.**

The Outline and snapshot are sibling derived products from the same admitted Envelope. Neither owns the other’s responsibility. State Formation may consume the Outline ref for alignment metadata, but must not perform semantic transformation. A is the primary receiver and joins both representations under one source-version lineage.

Historical B2 `Current World → Cognitive State` remains a data handoff, not a semantic authority rule.
