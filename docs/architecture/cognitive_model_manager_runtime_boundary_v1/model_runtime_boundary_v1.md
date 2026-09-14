# Model Runtime Boundary v1

## Runtime contract

Future Model Runtime may accept a scoped Capability Request and return a Raw
Evidence Candidate. It must not receive Goal, full Self, full Field, Decision,
Authority, or the complete cognitive state.

```text
Situation Requirement
        ↓
Vision / OCR / Spatial / Audio Capability
        ↓
Model Provider
        ↓
Scene / Text / Spatial / Audio Evidence Candidate
        ↓
Evidence Gateway
```

Model local reasoning is bounded by Model Cognitive Scope. “Possible vehicle”
is allowed; “you should go there” is outside scope. Provider output cannot
directly become Situation, Decision, Goal, Action, or Reality.

## Availability boundary

Controlled Available means Registry, Capability Binding, Admission, Permission,
Hardware Compatibility, Resource Profile, Health Baseline, and Evidence Output
Contract have passed as candidates. It does not mean Runtime is executing.

Model Manager does not automatically switch models. A degraded model returns
Model Capability Degradation Candidate and Diagnostics; Selection and any
future activation remain governed candidates.

No real Model Runtime, Provider Runtime, GPT/VLM/OCR/SLAM/ASR call, Hardware
Runtime, or Action Runtime is implemented.

Provider output is a Raw Evidence Candidate. Evidence Output Contract is
mandatory. No Provider Runtime, No GPT, No VLM, No OCR, No SLAM, No ASR, and No
Action Runtime are implemented.

No Action Runtime is implemented in this architecture phase.
