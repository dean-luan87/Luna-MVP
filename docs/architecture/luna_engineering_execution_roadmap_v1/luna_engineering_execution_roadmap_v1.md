# Luna Engineering Execution Roadmap v1.0

## Phase position

This phase maps Architecture Baseline v2.0 to the existing engineering tree and defines a safe future construction order. It is a read-only Planning Only phase. It does not migrate code, move files, rename assets, activate runtime, integrate models/providers/hardware, or implement Emotion/Social Runtime.

## Current engineering truth

The repository contains a large capability/tool asset population and many validated architecture directories. The inventory distinguishes architecture-only contracts from code assets and does not infer executable readiness from a document alone. Existing code is mapped to its canonical owner without changing that code.

## Architecture-to-engineering policy

Every entry has one canonical architecture module, engineering location, implementation status, owner, dependency, and next action. Status values are `Implemented`, `Skeleton`, `Architecture Only`, `Partial`, `Deprecated Candidate`, or `Migration Required`.

`Model Manager` manages model assets and versions; it does not define capabilities. `Capability Governance` owns capability contracts and admission. `Self Regulation` observes and proposes stability adjustments; it does not own external capability implementations.

## Execution priority baseline

### P0 — Core Runtime Foundation

Establish the state, event, trace, lifecycle, recovery, and persistence contracts needed to carry the already-frozen cognitive loop. This is a planning priority; implementation requires a separate authorized phase.

### P1 — Capability Activation

After P0 validation, connect Capability Runtime, Model Manager, Provider Adapter, and Calibration through the existing admission/evidence boundaries.

### P2 — Cognitive Enhancement

Only after runtime traces are stable, consider Memory Runtime, Learning Runtime, and Self Evolution Runtime under candidate-only governance.

### P3 — Social / Emotion Future

Social Self Runtime, Role Manager, and Emotion Engine remain future work behind a new boundary review.

## Runtime activation gates

```text
Constitution Ready
  → Architecture Baseline Ready
  → State Ownership Ready
  → Runtime Foundation Ready
  → Capability Governance Ready
  → Capability Runtime Authorization
  → External Model Admission
```

No external model or provider may bypass these gates.

## Migration strategy

Use `Architecture → Mapping → Adapter → Gradual Migration`. Mapping comes first; no mass refactor, deletion, or rename is authorized by this phase. Each migration candidate records target owner, priority, risk, compatibility strategy, and a validation gate.

## Future development workflow

1. Classify the new module into Self, Social Self, Cognitive, Capability, Action, or Governance.
2. Assign one owner and state writer.
3. Define the contract and lifecycle.
4. Define allowed and forbidden dependencies.
5. Add the mapping and status entry.
6. Implement only under an explicit phase.
7. Run V0, user V2, and ChatGPT V3 review.

## Verification authority

The agent runs read-only V0 checks only. The user terminal runs the final phase verifier. ChatGPT performs the final audit. The agent stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
