# Self Capability Awareness Whitebox v1

## Governed trace

```text
Capability Registry / Provider Diagnostics
                  ↓
          Capability Failure or Health Evidence
                  ↓
             Diagnostics Candidate
                  ↓
       Capability State Update Candidate
                  ↓
       Capability Confidence Candidate
                  ↓
          Self Capability Context
          ├── capability identity
          ├── current state
          ├── limitations
          ├── uncertainty
          └── provenance
                  ↓
       Attention Reallocation Candidate
                  ↓
          A Route Confidence Input
                  ↓
          Brain Awareness Candidate
```

## Provider replacement trace

Provider A → Provider Replacement Candidate → Provider B may alter evidence
quality, latency, or resource cost. It must not alter Capability Identity,
Self Identity, Goal, Decision, or Reality. Evidence Gateway remains mandatory.

## Boundary trace

```text
Capability State ≠ Reality State
Capability Confidence ≠ Fact
Failure Feedback ≠ Self Identity Rewrite
Self Capability Awareness ≠ Brain Decision
```

The Reducer remains the sole State mutation authority. Baseline assets are
used only for governance calibration and diagnostics, not as ordinary Runtime
input. This whitebox contains no real model, OCR, SLAM, Camera, Hardware
Runtime, Action, Emotion, Role, Social Runtime, or B Runtime. Hardware Runtime
is prohibited.
