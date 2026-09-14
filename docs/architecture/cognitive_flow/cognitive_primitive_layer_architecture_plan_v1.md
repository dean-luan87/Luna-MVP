# Luna Cognitive Primitive Layer Architecture Plan v1

## Position

The Cognitive Primitive Layer is Luna's internal candidate-expression layer. It receives only abstract Evidence/Context references through the frozen Translation boundary and organizes possible cognitive units for future review, analysis, and governed admission.

```text
External Capability / Provider (outside this phase)
        ↓
Evidence / Context Reference
        ↓
Translation Layer (external reference conversion)
        ↓
Cognitive Primitive Candidate
        ↓
Primitive Review / Validation (future)
        ↓
Field Event Candidate or Cognitive Analysis input (future, separately governed)
```

## Responsibilities

- express possible internal Entity, Relation, State, Event, and Situation units;
- preserve Evidence, Context, provenance, trace, uncertainty, and candidate status;
- support internal composition without provider-schema leakage; and
- provide a stable candidate vocabulary for Field Kernel and future Cognitive Analysis consumers.

## Authority Boundaries

| layer | responsibility |
| --- | --- |
| Translation Layer | converts governed external references into candidate-only Translation output; no world understanding |
| Cognitive Primitive Layer | expresses possible internal cognitive structure; no Fact or State authority |
| Field Kernel / Read Model | organizes and exposes current world representation |
| Field State Reducer | unique Field State mutation authority |
| future Decision Layer | separately governs action/decision judgment |

The Primitive Layer does not perform Fact Admission, Decision, Action, Field State mutation, Snapshot write, Context mutation, or Memory write.

## Future Ecology and Hive Boundary

Future Experience or Hive systems may consume primitive candidates only through separate traceable, review-bound contracts. They cannot use Primitive expressions to bypass Field Event Admission, Reducer authority, or individual Luna boundaries.

