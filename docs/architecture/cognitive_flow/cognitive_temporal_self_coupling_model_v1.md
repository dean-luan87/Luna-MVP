# Temporal–Self Coupling Model v1

## Purpose

The same temporal change has different current meaning for different subjects.
Temporal–Self Coupling combines dynamic-world candidates with governed Self
Capability, resource, and Goal references to enhance the current Situation.

```text
Temporal Change Candidate
        +
Self Capability Context
        +
Goal Context
        +
Resource Context
        ↓
Temporal Situation Enhancement Candidate
```

## Examples

| Temporal change | Self / goal condition | Candidate interpretation |
|---|---|---|
| battery is steadily decreasing | navigation is active and reserve is limited | task-completion capacity may narrow |
| illumination is decreasing | text understanding is low-light limited | observation uncertainty may increase |
| road density is rising | safety-sensitive navigation goal | route-delay relevance may increase |
| temperature is recovering | noncritical background task | no immediate escalation is implied |

## Boundary

Temporal–Self Coupling does not change Self Model, capability facts, resource
facts, Goal, Attention Runtime, or Regulation State. It cannot infer a
Decision, Action, safety verdict, or future certainty. It supplies only
traceable Situation Enhancement Candidate information.

