# Luna Self / Social Self Architecture Refactoring and Engineering Migration Planning v1

## Position

This phase combines two explicitly separated parts:

1. Architecture refactoring: Self Layer, Social Self Layer, and Integration
   Layer define conceptual ownership.
2. Engineering migration planning: existing assets, code impact, Runtime
   impact, risk, and future development workflow are registered without moving
   or rewriting code.

## Target model

```text
Luna
├── Self Layer
│   ├── Identity / Capability / Boundary
│   ├── Resource / Regulation / Evolution
├── Social Self Layer
│   ├── Social Identity / Role / Relationship
│   ├── Norm / Responsibility / Adaptation
└── Cognitive Integration Layer
    ├── Internal + External Cognition
    ├── Feedback Classification
    └── Emotion Context Boundary
```

## Engineering rule

`No Move First → Mapping First → Owner First → Migration Later`.

The current repository contains existing Self, Role, Relationship, Emotion,
Capability, and Runtime assets. They are recorded in an impact inventory and
ownership map. No file is moved, deleted, renamed, or refactored by this phase.

## Future module process

Every new module must pass:

1. Subject ownership classification;
2. Cognitive object definition;
3. Permission definition;
4. Interface definition;
5. Engineering implementation planning.

Architecture changes use:

`Proposal → Impact Analysis → Ownership Review → Migration Plan →
Implementation → Validation`.

## Runtime impact

Future Runtime may read Self State, Social State, and Integration Context, but
must preserve their owners and provenance. This phase does not modify or
activate Runtime.

## Phase boundary

This is a Planning Only phase. It does not implement Emotion, Role, Social,
Memory migration, Runtime, or automatic owner/registry changes.
