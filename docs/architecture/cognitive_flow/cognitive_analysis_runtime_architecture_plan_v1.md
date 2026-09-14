# A3 Cognitive Analysis Runtime Architecture Plan v1

## Planning Status

`planning_only: true`  
`runtime_authorization_status: NOT_AUTHORIZED`

This document plans a future A3 Cognitive Analysis Runtime without implementing it, changing the frozen A3 Controlled DryRun baseline, or granting runtime permission.

## Runtime Position

The future A3 Runtime is an analysis-capability layer. It may organize and evaluate already governed Context, Evidence, Hypothesis, and Analysis Question references into an Analysis Result Candidate. It is not a state-management layer, a Field Kernel, a Reducer, a Fact Store, a Decision engine, or an Action executor.

```text
CurrentCognitiveContextV1 (A2, reference only)
        + Evidence / Hypothesis / Question references
                              |
                              v
                 A3 Cognitive Analysis Runtime
                              |
                              v
             Analysis Result Candidate + trace/warnings
                              |
                              v
          Future Decision Candidate boundary (separate domain)
```

The last arrow is a future read-only handoff boundary. An A3 result is never itself a Decision Candidate, Fact, Event, or State update.

## Future Runtime Lifecycle

1. **Input binding** — accept only declared Context, Evidence, Hypothesis, and Analysis Question references.
2. **Reference admissibility check** — require traceability, lifecycle visibility, and explicit missing/stale/revoked/unknown signals; absence blocks or warns rather than being completed.
3. **Evidence-reference organization** — select and relate supplied references without fetching raw observations or altering evidence.
4. **Hypothesis evaluation** — assess existing Hypothesis Candidates and competing sets; do not promote, force dominance, or generate Fact.
5. **Semantic analysis** — derive candidate-only interpretation, sufficiency, uncertainty, information-gap, and warning signals.
6. **Candidate result generation** — produce references to existing A3 result structures, with provenance and trace retained.
7. **Independent verifier handoff** — submit output to a separate verifier boundary; no verifier result may be trusted merely because Runtime emitted it.
8. **Stop without side effect** — no State, Snapshot, Context, Event, Fact Store, Decision, or Action writeback is permitted.

## Input Sources

| Source | Future A3 use | Explicit exclusion |
| --- | --- | --- |
| `CurrentCognitiveContextV1` from A2 | direct input by reference only; preserves Context and Snapshot trace references | no Context construction or mutation |
| Evidence Reference | supplied, traceable evidence identity and lifecycle signals | no raw observation retrieval or evidence mutation |
| Hypothesis Reference | existing candidate or competing-set reference | no Fact promotion or forced dominance |
| Analysis Question | declared analytical scope and task/goal context | no Decision or Action instruction |

## Output Types

The future Runtime must use versioned, governance-approved A3 candidate structures. At minimum its outputs remain within the existing conceptual categories: `CognitiveAnalysisResult`, `AnalysisEvidenceAssessment`, `CognitiveAnalysisSufficiencyResult`, `InformationGapRefinement`, `ObservationRequestCandidate`, warnings, uncertainty, provenance, and trace references.

Outputs are candidates only. Confidence remains a candidate attribute, not an admission rule or Fact claim.

## Relationship to A2, Reducer, and Field State

- **A2 Context Construction** owns Current Context construction and provides A3 input by reference. A3 does not rebuild, update, or write Context or Snapshot.
- **Field State Reducer** remains the sole Field State mutation authority. A3 may neither invoke nor wrap it.
- **Field State** is visible only through governed A2 Context references. A3 cannot directly query, create, modify, or write Field State.

## Future Model Adapter Relationship

No LLM, Vision Model, OCR, SLAM, database, network, camera, sensor, or external capability is introduced by this plan. A future Model Adapter, if separately approved, is an external-capability boundary and cannot be the A3 Runtime core. It must supply governed Evidence Candidate/Reference inputs through its own admission and provenance controls; it may not write A3 results, Fact, Context, Snapshot, Event, or Field State directly.

## Preserved Non-Goals

- No Runtime implementation, invocation, or authorization.
- No new capability, protocol, Contract, Fixture, Runner, Verifier, or serializer.
- No model connection, persistence, network, device, or database integration.
- No Decision Candidate construction, Decision execution, or Action execution.
