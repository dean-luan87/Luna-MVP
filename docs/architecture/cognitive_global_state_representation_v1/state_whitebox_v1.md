# Global State Whitebox v1

## Authority questions

1. Who owns each component? Its existing Field, Self, Workspace, Attention,
   Memory, Learning, Capability, Hypothesis, Expectation, Goal, or Task
   contract.
2. Who composes Global Cognitive State? A governed read-only State Composer.
3. Who validates freshness? Composition Governance checks source version,
   timestamp, Field context, confidence, and Provenance.
4. Who owns Unknown State? The originating modules; the composer preserves
   their Unknown and Conflict states.
5. Who consumes the package? Brain or an explicitly authorized read-only
   consumer.
6. Who owns final Decision? Brain retains final Decision authority.
7. Who updates modules? Only their existing owner contracts through candidate
   interfaces; Global State cannot write them.
8. Who stores history? Memory stores selected State Transition records, not
   the live state as a database.

## Allowed flow

```text
Field / Self / Workspace / Attention / Hypothesis / Expectation / Memory /
Learning / Capability / Goal / Task / Reality
                              ↓
                 Global Cognitive State Snapshot
                              ↓
                 Global Cognitive State Package
                              ↓
                              Brain
```

## Negative paths

- Global State → Reality write: forbidden.
- Global State → Field mutation: forbidden.
- Global State → Self Identity mutation: forbidden.
- Global State → Goal or Task mutation: forbidden.
- Global State → Attention allocation: forbidden.
- Global State → Hypothesis or Belief resolution: forbidden.
- Global State → Expectation update: forbidden.
- Global State → Decision: forbidden.
- Global State → Action: forbidden.
- Global State → Prediction Runtime: forbidden.
- Global State → World Model: forbidden.
- Global State → B Runtime: forbidden.
- Global State → automatic learning: forbidden.

## Preserved state fields

Every snapshot preserves component references, source versions, timestamp,
Field context, Identity reference, Confidence, Unknown State, Conflict State,
Risk, Constraints, and Provenance. Stale or unavailable modules remain
Unknown; the composer never fabricates a complete state.

