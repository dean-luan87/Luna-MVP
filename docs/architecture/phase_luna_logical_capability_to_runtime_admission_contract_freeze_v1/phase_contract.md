# Phase Contract — Logical Capability to Runtime Admission v1

## Mode

Read / contract freeze / schema design only. No Python, Runner, Verifier,
pytest, py_compile, Provider, model, YOLO, OCR, camera, checksum computation,
dependency probe, runtime health probe, model loading, or runtime mutation.

## Frozen split

```text
Logical Capability Resolution
  → Runtime Admission Assessment Candidate
  → Executable Capability Candidate
  → Provider Admission
  → Provider Invocation
```

This phase introduces no runtime implementation, no new Manager, no Scheduler,
no canonical enum, and no change to Brain, A, B-CR, or Loop authority.

## Existing owners retained

- Capability Registry / Universal Slot Governance: logical capability and slot
  resolution.
- Model Manager / Model Governance: model asset identity, version, governed
  path metadata, contract and integrity metadata.
- System Diagnostics / Runtime Health: dependency and runtime health evidence.
- Capability Admission Governance: coordinates and decides executable
  admission candidate status.
- Provider Governance / FPO: Provider-specific admission and invocation
  boundary.
- Observation Gateway: acquisition/evidence admission and return.
- Loop: mechanical reference persistence only.

