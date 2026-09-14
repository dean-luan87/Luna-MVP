# Luna Architecture Baseline v2.0

## Status

This document is the canonical planning baseline for the Luna architecture after the Self/Social Self boundary review. It consolidates already-validated architecture assets; it does not migrate code, move files, activate runtime behavior, or replace existing governance.

## Canonical layer tree

```text
L0 System Constitution
└── L1 Cognitive Operating System
    ├── L2 Cognitive Core
    ├── L2 Self System
    ├── L2 Social System
    ├── L2 Integration System
    ├── L2 Capability Governance
    ├── L2 Action System
    └── L2 Runtime System
        └── L3 External / Provider / Hardware boundary
```

L0 is the highest constraint. L1 governs lifecycle and interfaces. L2 modules own their declared state and candidates. L3 is an external boundary and never becomes a cognitive authority.

## Canonical ownership

Self Layer owns identity continuity, capability awareness, resources, regulation, and evolution. Social Self owns role, relationship, responsibility, and social norm context. Integration owns the boundary between internal and social context, including the future Emotion Context boundary. Capability Governance owns capability and model admission; it does not create goals or decisions. Action Runtime is the execution gate; it does not create decisions.

## Canonical information loop

```text
External World → Social Self / External Cognition → Evidence → Cognitive Core
→ Brain → Decision → Action → Feedback → Learning → Self / Social Update
```

The internal capability path is:

```text
Self State → Self Regulation → Brain → Capability Request
→ Capability Governance → Capability Runtime → Evidence
```

Evidence, uncertainty, and feedback remain explicit. Provider output is evidence candidate only; it cannot directly write Reality, Brain, Goal, or Action.

## Baseline rules

1. Every canonical module has one identity and one primary owner.
2. Every core state has one writer; readers are explicitly listed.
3. Dependencies flow from Constitution and governance toward cognition, capability, and execution; the control graph is acyclic.
4. Feedback is an event re-entry, not an authority cycle.
5. Future extensions are planning entries behind Constitution, Governance, Core Integration, Capability Admission, and Boundary Verification gates.
6. This phase is mapping-only. No code migration, file move, deletion, rename, runtime activation, model integration, hardware integration, Emotion Runtime, Social Runtime, or capability replacement is authorized.

## Engineering mapping policy

Mappings point to existing architecture directories and manifests. Status values distinguish implemented, planned, conceptual, and missing assets. A mapping does not authorize implementation or alter ownership of an existing file.

## Verification authority

The agent may perform V0 static checks only. The user terminal owns the phase verifier (V2). ChatGPT performs the V3 audit and final decision. The agent stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
