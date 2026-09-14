# Cognitive Core Integration Whitebox v1

## Ownership questions

| Question | Canonical answer |
|---|---|
| Who creates evidence? | Observation/Provider output through Evidence Gateway |
| Who owns current field state? | Field System |
| Who owns the active cognitive window? | Cognitive Workspace |
| Who owns attention allocation? | Attention System |
| Who owns decision candidate generation? | Brain |
| Who owns commitment review? | Decision Commitment with authority checks |
| Who owns execution gating? | Action Boundary |
| Who owns long-term memory admission? | Memory System |
| Who proposes learning/evolution? | Learning System / Self Evolution |
| Who preserves stability? | Self Regulation, subject to governance |

## Boundary questions

1. Does any Provider directly write Brain, Reality, Memory, Goal, or Identity?
   No; all outputs pass through Evidence and admission boundaries.
2. Does Learning directly rewrite Value or rules? No; it emits candidates only.
3. Does Self Regulation become Capability Governance? No; it proposes and
   evaluates stability, while Capability Governance retains admission.
4. Does Emotion control Decision or Action? No; the interface is placeholder
   only.
5. Is Action Runtime active in this phase? No; only its boundary contract is
   reviewed.

## Review method

The phase verifier checks artifact completeness, JSON contracts, master-flow
continuity, unique ownership, dependency acyclicity, boundary permissions,
future-extension isolation, and planning-only imports. It does not execute
Runtime, Model, Provider, Hardware, Action, Emotion, Social, or Learning code.
