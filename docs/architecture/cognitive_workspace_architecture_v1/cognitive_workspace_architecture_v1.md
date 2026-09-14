# Cognitive Workspace Architecture v1

## Position

Cognitive Workspace is the current cognitive operating window for Luna. It
unifies references to the active Field, Role, Relationship, Task, Self,
Attention, Drive, Value, Memory, and Brain context without becoming any of
those systems.

```text
Field + Role + Relationship + Task + Self + Attention + Drive + Value + Memory
                                  ↓
                         Cognitive Workspace
                                  ↓
                          Brain Input Package
```

Reality remains the source of world facts. Memory remains the source of
historical experience. Field remains the source of field structure. Workspace
stores only the current cognitive focus. Brain retains reasoning,
Goal authority, and final Decision authority.

## Core workspace model

```text
Cognitive Workspace
├── Active Field Context
├── Active Role Context
├── Active Relationship Context
├── Active Task Context
├── Active Goal Context
├── Attention State
├── Current Unknown
├── Current Risk
├── Relevant Memory
├── Drive Influence
└── Value Constraint
```

Workspace references an existing Field; it does not create or mutate a Field.
Workspace references the active Role and Relationship contexts; it does not
own the Role or Relationship definitions. Attention selects what enters the
workspace. Memory contributes retrieval candidates through the workspace and
does not override current Reality.

## Boundary model

| Layer | Owns | Workspace relationship |
|---|---|---|
| Reality | current world facts | read-only fact reference |
| Field | physical/social/virtual/task field structure | active context reference |
| Role / Relationship | social position and relation candidates | active context reference |
| Task / Goal | continuity and purpose | current process reference |
| Self | Identity, Capability, State | current self context reference |
| Attention | resource allocation | admission/filter authority |
| Drive / Value | motivation and constraints | influence/constraint reference |
| Memory | historical experience | relevant retrieval candidates |
| Brain | understanding, reasoning, Decision | receives Workspace Package |

Workspace does not perform No Decision, No Reasoning, No Planning, No Emotion Runtime,
No B Route Runtime, No automatic learning, No Memory modification, No Action Runtime,
No model training, or No hardware calls. Workspace cannot modify Reality, cannot
modify Goal, cannot modify Identity, or cannot modify Decision.
Workspace cannot modify Goal, Identity, or Decision.

## Activation and lifecycle

Workspace lifecycle is `Created → Active → Updated → Background → Closed`.
Activation is admitted from an existing Field/Task/Attention context. Update
is candidate-based and provenance-preserving. Background workspaces remain
isolated from the Primary Workspace. Closing a workspace releases its current
focus but does not delete Memory or alter the originating Field.

## Multi-workspace model

Multiple Cognitive Workspaces are allowed as separate contexts:

- Primary Workspace: user navigation;
- Background Workspace: battery monitoring;
- Background Workspace: family task continuity.

These are not multiple consciousnesses and do not grant any workspace
independent Decision authority. Cross-workspace information requires an
explicit governed candidate and must preserve Field, Task, Unknown, Risk,
Provenance, and Boundary metadata.

## Unknown and conflict

Unknown is first-class workspace information. The workspace contains Known State,
Unknown State, and Conflict State. Unknowns are not silently completed,
and conflicts are surfaced as candidates for Attention or Brain review.
The exact workspace triad is Known State, Unknown State, and Conflict State.

## B Route placeholder

Future B Route may consume a Workspace Snapshot to produce a Simulation
Workspace Candidate. This phase only defines a placeholder. Simulation cannot
write Reality, alter Identity, or make a Decision.
