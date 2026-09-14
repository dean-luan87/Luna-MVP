# Observation Lifecycle v1

Conceptual lifecycle: `candidate → admitted → capability-ready → provider-ready
→ acquiring → result-returned → evidence-admitted / failed / stale / cancelled
/ expired`.

Observation owns request/result correlation and acquisition lifecycle. Provider
owns invocation state; Gateway owns Evidence admission; Field/Current World
owners handle downstream state candidates.
