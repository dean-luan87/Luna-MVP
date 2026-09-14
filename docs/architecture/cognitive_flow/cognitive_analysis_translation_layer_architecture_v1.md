# A3 Evidence Context Translation Layer Architecture v1

## Position

The Evidence Context Translation Layer is Luna's controlled boundary before a governed external Evidence reference may become a Cognitive Primitive Candidate. It is neither an external capability, Evidence authority, world-understanding layer, Field Kernel, Cognitive Analysis Runtime, Fact Admission, Decision system, nor Memory system.

```text
External Capability
        ↓
Evidence Envelope (candidate-only)
        ↓
Evidence Context Translation Layer
        ↓
Cognitive Primitive Candidate (candidate-only)
        ↓
Cognitive Analysis Runtime boundary
```

## Responsibilities

- normalize Evidence/Context **references**;
- preserve source identity only as provenance;
- preserve uncertainty and trace;
- emit a candidate envelope with no authority upgrade.

The layer does not understand a world, determine semantic truth, judge a task, plan action, or modify Context/Snapshot/Field State.

## Permissions

All external/model calls, Fact creation, Decision/Action creation, State/Context/Snapshot mutation, Memory update, and Learning Candidate admission remain false. `runtime_authorized=false` is unchanged.
