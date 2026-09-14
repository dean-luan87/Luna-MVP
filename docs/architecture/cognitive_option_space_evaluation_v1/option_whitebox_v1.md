# Option Space Whitebox v1

## Structured candidate trace

```text
Situation Candidate
        ↓
Self Capability + Self State + Goal + Constraint + Unknown
        ↓
Option Candidate Space
   ┌────┼────┬────┬────┐
   ↓    ↓    ↓    ↓    ↓
Benefit Cost Risk Capability Unknown
        ↓
Option Evaluation Candidate
        ↓
Decision Candidate Package
        ↓
Brain Evaluation
```

The trace preserves Option List, Tradeoff, Risk, Unknown, Confidence,
Constraint, Experience Reference, and provenance. Expected Benefit is represented.
It does not expose private chain-of-thought, select an Action, execute a Provider, or mutate State. private chain-of-thought is excluded.

Provider output remains Evidence/Capability input. Provider cannot create an
Option, Decision, or Action. Provider cannot create an Option. Self Capability changes feasibility candidates;
it does not decide for Brain. The Reducer remains the sole State mutation authority.

No Action, No Execution Runtime, No automatic execution, No Provider Decision,
No Emotion Runtime, No Role Runtime, No Social Runtime, No B Runtime, and No
Prediction are included. No Prediction is included.
