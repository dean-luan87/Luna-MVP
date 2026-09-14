# Cognitive Global State Representation Architecture v1

## Phase boundary

This phase defines a unified representation of Luna's current cognitive
condition. Global Cognitive State is a composed, provenance-preserving
snapshot of module states; it is not a new authority and does not replace the
owning modules.

```text
Module State
    ↓
Global Cognitive State
    ↓
Brain Context
```

Global Cognitive State is not a database, not Memory, not Decision, and not
Reality. It is the current subject's unified state representation for a
bounded cognitive cycle. It can be created, refreshed, compared, and
snapshotted, but it cannot itself reason, decide, execute, or mutate a source
module.

## Global Cognitive State structure

```text
Global Cognitive State
├── Reality State
├── Field State
├── Self State
├── Role State
├── Relationship State
├── Situation State
├── Intent State
├── Goal State
├── Task State
├── Workspace State
├── Attention State
├── Drive State
├── Value State
├── Hypothesis State
├── Belief State
├── Expectation State
├── Memory Context
├── Learning Context
├── Capability State
└── Unknown State
```

Each component is a reference or bounded projection from its owning contract.
The representation retains status, confidence, time context, conflicts,
unknowns, risk, constraints, and provenance. A missing or stale component is
represented as Unknown or Stale Candidate rather than silently completed.

## Composition rules

State composition is deterministic and candidate-based:

1. Read the current state reference from each owner.
2. Validate identity, version, time, Field context, and provenance.
3. Preserve conflicts and Unknown State.
4. Compose a Global Cognitive State Snapshot with a snapshot timestamp and
   source versions.
5. Publish a read-only Global Cognitive State Package to Brain or another
   explicitly authorized consumer.

The composer does not infer a new Reality, resolve a Hypothesis, update a
Belief, change an Expectation, allocate Attention, or create a Decision.

## State ownership and interfaces

| State | Owner | Global representation |
|---|---|---|
| Reality State | Reality Workspace / Reducer | fact reference and Evidence status |
| Field State | Cognitive Field | active Field context and dynamics |
| Self State | Self | Identity, Capability, and dynamic state references |
| Role / Relationship State | Social Field contracts | active role and relationship projections |
| Situation State | Situation Understanding | current context candidate |
| Intent / Goal / Task State | Intent and continuity contracts | purpose and process references |
| Workspace State | Cognitive Workspace | current focus and context package |
| Attention State | Attention Governance | allocation and resource state |
| Drive / Value State | Drive and Value Core | influence and constraint candidates |
| Hypothesis / Belief / Expectation State | uncertainty contracts | current candidates and feedback |
| Memory / Learning Context | Memory and Learning | relevant references and candidates |
| Capability State | Capability and Self Capability | availability and confidence |
| Unknown State | all owners, composed centrally | unresolved and conflicting items |

The Global Cognitive State does not become an owner of these states. Updates
must return to the owning interface as governed candidates.

## Brain Context Package

Brain receives a Global Cognitive State Package rather than unrelated module
messages. The package contains:

- snapshot identity, time, version, and provenance;
- Reality, Field, Self, Role, Relationship, Situation, Intent, Goal, and Task;
- Workspace, Attention, Drive, Value, Hypothesis, Belief, and Expectation;
- Memory Context, Learning Context, Capability State, Unknown State, Risk,
  Conflict, and Confidence.

Brain retains interpretation, goal review, value review, and final Decision
authority. The package is context, not a Decision or an Action command.

## Snapshot, transition, and memory rules

Snapshots are immutable references to a composition point. A new composition
creates a new snapshot or a governed State Transition Candidate; it does not
rewrite a previous snapshot. Memory may retain important State Transition
records, not every snapshot. Learning may inspect transitions and produce a
candidate pattern, but it cannot silently mutate the current state.

Future B Route may copy a Current Cognitive State Snapshot into a Simulation
State placeholder. This phase does not implement Simulation State or a B
Runtime, and a snapshot copy cannot write to live Reality or Self.

## Explicit non-goals

This phase does not implement Decision, Prediction, World Model, B Runtime,
automatic learning, Action, Runtime execution, model invocation, hardware
invocation, Emotion Runtime, or state mutation. Global Cognitive State is a
representation and interface layer only.

Contract keywords: not Reality; Conflicts; Provenance; does not resolve a
Hypothesis; does not update a Belief; does not change an Expectation; does not
allocate Attention; does not create a Decision; final Decision authority;
current Reality; Memory may retain important State Transition records;
Simulation State placeholder; hardware invocation.
Contract keyword: does not resolve a Hypothesis; does not allocate Attention.
