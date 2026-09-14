# Self Situated Position Model v1

## Purpose

Self Situated Position is the current subject-relative reference used by
Situation Assessment. It answers neither “who Luna is” nor “what Luna should
do”; it states how Luna is presently placed relative to the represented world
and ongoing cognition.

```text
Physical + Capability + Resource + Cognitive Position
                         ↓
          Situated Self Position Candidate
```

| Dimension | Candidate content | Excluded content |
|---|---|---|
| Physical | coordinate, orientation, pose, localization uncertainty | movement command |
| Capability | usable level and current boundary | Registry internals/model parameters |
| Resource | abstract available envelope and constraints | raw device telemetry in Brain context |
| Cognitive | active goal/context, attention focus, active uncertainty | decision/permanent memory |

The candidate may state that location is approximate, night visual
understanding is limited, power is constrained, and navigation is in focus. It
cannot claim Identity, modify Self Model, create a task, or actuate a body.
