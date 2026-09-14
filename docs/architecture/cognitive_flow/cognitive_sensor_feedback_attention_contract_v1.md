# Cognitive Sensor Feedback Attention Contract v1

Perception/Adapter layers may receive a Perception Request Candidate only as a bounded information-need reference. Any future adapter must independently validate capability availability, source scope, resource constraints, and permission boundary.

```text
Controller -> Perception Request Candidate -> Future Perception Adapter
  -> Evidence Candidate -> Evidence Field
```

Sensor Request != Action Command. Sensor Feedback != Evidence Truth, Sensor Invocation, Device Control, Model Invocation, Reality modification, Memory mutation, or State mutation.
