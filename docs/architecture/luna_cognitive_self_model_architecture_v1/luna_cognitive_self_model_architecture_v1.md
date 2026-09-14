# Luna Cognitive Self Model Architecture v1

## Position

The Cognitive Self Model is Luna's task-and-cognition-level representation of its current state, capabilities, limitations, resources, context, history references, and boundaries. It is not personality, emotional identity, or social identity.

```text
Self Evolution Evidence
          |
          v
  Cognitive Self Model
  ├── Self State
  ├── Capability Awareness
  ├── Limitation Awareness
  ├── Resource Awareness
  ├── Context Awareness
  ├── Boundary Awareness
  └── Relevant Self History
          |
          v
  Brain Context / Action Boundary Review
```

## Scope

In scope:

- representing current Self State separately from Identity;
- binding capability awareness to field, condition, evidence, and confidence;
- keeping limitations, unknowns, and permission boundaries explicit;
- representing resource availability and constraints;
- composing current Field, Workspace, Intent, Goal, and Task context;
- retrieving only task-relevant self history;
- exposing a read-oriented context package to Brain and an eligibility check to Action Boundary;
- accepting reviewed update candidates from Self Evolution.

Out of scope:

- personality or emotional state;
- social identity or relationship generation;
- automatic value, goal, constitution, or identity changes;
- Runtime Learning, model training, parameter updates, or provider control;
- Action execution or direct Reality mutation.

## Core distinctions

Identity is the stable subject boundary. Self State is dynamic. Capability Awareness describes what Luna can currently do under a condition. Limitation Awareness describes where confidence is insufficient. Resource Awareness describes available body and compute resources. Context Awareness describes the current task situation. None of these changes Identity.

```text
Self Evolution Growth Candidate
        -> Evidence -> Review -> Self Model Update Candidate
```

The Self Model does not directly write itself from a provider, Memory record, or unreviewed learning signal.

## Dual-drive future interface

The project may record a future distinction between Cognitive Drive and Emotional Drive, but this phase exposes only a neutral future-interface placeholder. Emotional Drive, Social Self Model, and Emotion Runtime are not part of the current self model.

## Authority and safety

The model supplies context and eligibility information. Brain retains judgment and decision authority. Action Boundary retains execution-gate authority. Constitution, Value, Identity, and Goal ownership remain outside this phase. Unknown is never silently converted into capability or permission.
