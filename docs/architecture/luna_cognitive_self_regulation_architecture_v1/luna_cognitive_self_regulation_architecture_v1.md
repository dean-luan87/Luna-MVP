# Luna Cognitive Self Regulation Architecture v1

## Position

Self Regulation is the second-stage extension of the Cognitive Self Model. It maintains current cognitive stability by observing self state, assessing health, proposing capability/resource adjustments, managing degradation, and preparing recovery candidates.

```text
Self Model
    |
Self Observation
    |
Self Health Assessment
    |
Capability / Resource Regulation Candidates
    |
Degradation or Recovery Candidate
    |
Adaptation Governance
    |
Capability Governance / Admission
    |
Stable Cognitive Operation
```

Self Regulation is not a second Capability Manager. It proposes the need and constraints for regulation; Capability Governance admits an available capability option, and Model Manager/Provider surfaces remain implementation boundaries.

## Scope

In scope:

- observing changes in runtime, hardware, capability, model, memory, and resources;
- representing Healthy, Warning, Degraded, Critical, and Recovery Required states;
- proposing capability homeostasis and resource regulation candidates;
- recording degraded capability profiles and explicit unknowns;
- preparing diagnosis, recovery, validation, apply-candidate, and monitoring contracts;
- governing adaptation with review, admission, rollback, and trace requirements;
- exposing stability context to Brain, Capability Governance, Model Manager, and Learning.

Out of scope:

- automatic code modification, model training, or parameter updates;
- automatic Value, Identity, Goal, Brain-rule, personality, Emotion, or Social Identity changes;
- direct Provider invocation, Action execution, or Reality mutation;
- production scheduler implementation or live device control.

## Core distinction

Learning improves future understanding from external experience. Self Regulation maintains present operating stability. A current OCR failure can produce a degraded capability and recovery candidate; repeated night-time limitations can later become Self Evolution evidence. Neither path automatically changes the model or the subject's identity.

## Regulation authority

```text
Self Regulation: observe, assess, propose, degrade, recover-candidate
Capability Governance: admit and authorize capability options
Model Manager: provide registered model/version/resource options
Calibration: provide performance evidence
Brain: retain judgment and goal/decision authority
```

All adaptation follows:

```text
Observation -> Assessment -> Candidate -> Evidence -> Review -> Admission -> Apply Candidate -> Monitor
```

Unknown and failure provenance remain explicit at every stage.
