# Registry–Self Model Coupling v1

## Three-layer mapping

```text
Registry Asset
      ↓
Capability / Health State
      ↓
Self Capability Context
      ↓
Brain / Neural Usage
```

Registry Asset says what exists. Capability or Health State says its current
condition. Self Capability Context says what Luna currently believes it can do,
with boundary, confidence, limitations, and unknowns. Raw provider parameters and
hardware internals do not enter Brain directly.

## Continuity

Hardware damage or Model replacement may change Capability, Resource, Health, and
Limitation. It must not silently change Identity. A failure produces a candidate
such as "visual capability degraded by hardware failure", not "Luna cannot see"
and not an independent Goal.

## Boundary

Self Model consumes an abstract context. Registry, Hardware Manager, Model
Manager, and Diagnostics remain infrastructure sources; they do not become a second cognitive subject
or bypass Reality Workspace and Brain.
The registry system does not become a second cognitive subject.
