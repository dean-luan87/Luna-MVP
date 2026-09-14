# Attention Refinement Model v1

## Purpose

Attention Refinement makes an Attention Intent cognitively actionable without
collapsing it into a model invocation.

```text
Attention Intent Candidate
        +
Current Situation Candidate
        +
Available Capability Context
        +
Experience Reference
        ↓
Attention Requirement Candidate
        ↓
Capability Observation Candidate
```

Example: “confirm whether the path ahead is safe” may refine into information
needs for obstacle presence, moving-object relation, road boundary, and height
difference. It does not select YOLO, SAM, OCR, or any Provider.

## Authority boundary

- Refinement does not create Goal, Decision, Action, Reality interpretation, or
  actual resource allocation.
- Available Capability Context limits candidate feasibility but does not expose
  provider/model details to Brain intent.
- Capability Observation Candidate is sent to existing governance; it is not a
  direct Provider call.

