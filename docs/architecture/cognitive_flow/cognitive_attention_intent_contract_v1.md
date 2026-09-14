# Attention Intent Contract v1

## Role

Attention Intent is the Brain-provided candidate explanation of why information
is needed. It responds to an existing Brain Goal, Situation, or cognitive
uncertainty; it cannot create a Goal, Survival Drive, Decision, or Action.

```text
Attention Intent Candidate
├── Purpose
├── Cognitive Direction
├── Required Context
├── Time Requirement
├── Confidence Requirement
├── Priority Candidate
└── trace_ref
```

| Field | Meaning | Boundary |
|---|---|---|
| Purpose | why an observation may matter to current cognition | not a new Goal |
| Cognitive Direction | broad information orientation | not a device or movement command |
| Required Context | background needed to interpret evidence | not a Reality claim |
| Time Requirement | bounded relevance window | not a Scheduler or frequency command |
| Confidence Requirement | sufficiency expectation for candidate evidence | not Truth or final certainty |
| Priority Candidate | Brain-provided importance candidate | not actual resource allocation |
| trace_ref | Brain/Situation/Goal provenance | required for review |

## Example

For “find a pharmacy,” the Brain can express a purpose of completing a medicine
purchase task and request evidence about medical-service location, name, and
open status. It does not mandate OCR, a camera, a specific Provider, or a
device command.

