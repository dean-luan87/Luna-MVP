# Cognitive Attention Competition and Arbitration Whitebox v1

```text
Field State + Self State + Goal + Risk + Resource
                    ↓
Attention Source Registry
                    ↓
Attention Competition
                    ↓
Mandatory / Competitive / Opportunistic Arbitration
                    ↓
Attention Allocation Candidate
                    ↓
Observation Requirement
                    ↓
Capability Observation
```

Interrupt path:

```text
New Evidence → Risk Candidate → Attention Interrupt Request
             → Attention Arbitration → Resource Reallocation
```

Lifecycle path:

```text
Created → Allocated → Maintained → Decayed → Released → Archived
```

Feedback goes to Field and Brain as candidates. Attention does not perform
Decision, Action, Value Judgment, Prediction, or Reality mutation. Role,
Emotion, Social Field, B, Camera, OCR, SLAM, Hardware Runtime, and real model
runtime are not present.
