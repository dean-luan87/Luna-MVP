# Luna Cognitive Information Processing Pipeline Architecture v1

## Position

This phase freezes the A-route information-processing chain. It is an architecture contract, not a runtime implementation.

## Canonical pipeline

Reality enters through capability-provided observation evidence. The Cognitive Kernel structures evidence, assembles the active Cognitive Field, allocates attention, activates context, maintains multiple hypotheses, and produces a current-understanding candidate. Brain produces a Decision Candidate only. Any action or interaction remains behind the Action Boundary. Outcomes become governed Experience Candidates, which may later be consolidated into patterns and growth candidates.

```text
Reality
  -> Observation Evidence
  -> Information Structuring
  -> Cognitive Field
  -> Attention Allocation
  -> Context Assembly
  -> Hypothesis Generation
  -> Current Understanding
  -> Decision Candidate
  -> Action / Interaction boundary
  -> Experience Extraction
  -> Memory Consolidation
  -> Pattern Formation
  -> Capability / Role / Social Self growth candidates
```

## Frozen boundaries

- Providers and models stop at Evidence. They may report observations, provenance, confidence, limitations, and unknowns; they do not supply meaning, goals, decisions, or memory facts.
- Structured information is not yet an interpretation. It names entities, events, relations, states, and changes with traceable evidence.
- A Cognitive Field is the current reality slice understood by Luna, not Reality, a database, or a World Model.
- The Field activates relevant Memory; Memory does not autonomously take control of the pipeline.
- Knowledge is contextualized through Field, Role, and Task before use.
- Hypotheses may coexist and must preserve Unknown and conflict.
- Current Understanding remains a candidate with provenance and uncertainty.
- Brain emits Decision Candidates. Execution, Reality change, and durable mutation remain outside this phase.
- Experience is a value-bearing outcome, not an action log. Memory consolidation and growth are governed candidate-producing stages.

## Ownership

The ownership registry is canonical for this phase. Each emitted object has one owner and an explicit writer boundary. Cross-stage consumers receive immutable references or candidates; no stage silently acquires another stage's authority.

## Scope and exclusions

Architecture-only contracts are added here. This phase does not implement a runtime pipeline, call models or providers, execute actions, perform automatic learning or memory consolidation, run B-route simulation, or introduce Emotion/Role/Social runtimes.

## A/B relationship

The A route is the current-field processing path. A future B route may consume a snapshot or candidate package, but no simulation is executed here and no simulated result may directly mutate the A route.

