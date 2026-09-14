# Cognitive Self Model Architecture v2

## Position

Self Model is Luna's Brain-internal cognitive explanation of the current
subject. It is not a Registry, provider inventory, Memory store, Personality
implementation, Goal source, or Runtime controller.

```text
Self Model
├── Identity Awareness
├── Capability Awareness
├── Resource Awareness
├── Limitation Awareness
├── Experience Awareness
├── Social Identity Awareness
├── Growth Potential Candidate
└── Regulation State Awareness
```

## This phase versus future interfaces

| Element | v1/v2 status | Boundary |
|---|---|---|
| Capability Awareness | defined through existing Self Capability Context | abstract present ability, not Registry data |
| Resource / Limitation Awareness | architecture interface | no raw telemetry or direct resource control |
| Identity / Social Identity | architecture interface | no personality or independent entity identity |
| Experience Awareness | architecture interface | not a substitute for Memory or experience mutation |
| Growth Potential | candidate interface | no automatic learning/self-upgrade |
| Regulation State Awareness | contextual interface | no scheduler, tempo control, or State mutation |

Only admitted candidate flows may update a Self Model; Reducer remains the
sole State mutation authority.
