# Intent State Ownership v1

| State/field | Classification | Owner/handling |
|---|---|---|
| Intent identity | AUTHORITATIVE | Intent Governance |
| Intent version/lifecycle | AUTHORITATIVE | Intent Governance |
| Intent Candidate | CANDIDATE | Intent Governance candidate seam |
| Potential Intent | CANDIDATE | source proposal / Intent Governance |
| active/coexisting/dominant status | AUTHORITATIVE after admission; candidate before | Intent Governance; Brain constrains global priority |
| carryover relation | LOCAL_DERIVED/CANDIDATE until governed | Intent Governance |
| source influence refs | REFERENCE_ONLY | source owners |
| Goal refs | REFERENCE_ONLY | Brain |
| Concern refs | REFERENCE_ONLY | Brain |
| Task refs | REFERENCE_ONLY | Task Manager |
| A reasoning refs | REFERENCE_ONLY | A |
| interaction/competition record | CANDIDATE or Intent-owned relation | Intent Governance |
| Loop persistence record | MECHANICAL | Loop |

Intent Governance must not duplicate Goal, Concern, Task, A reasoning, Field,
Context, Role, Memory or Experience payloads. The candidate types' read-only
refs and provenance fields follow this rule; future admitted state must retain
the same source ownership.
