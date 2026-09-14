# Cognitive Process Ecology Whitebox Architecture v1

The future Whitebox is read-only and shows cognitive organization rather than model-call logs:

```text
Brain Intent
  ↓
Active Processes / Background Processes / Reflex Signals
  ↓
Capability Requirements
  ↓
Experience Pattern Candidate
  ↓
Evidence and Feedback Candidates
```

Each trace row should expose source, process type, lifecycle candidate, resource-profile candidate, capability requirement, uncertainty, and boundary flags. It must not provide a control surface for process execution or experience adoption.
