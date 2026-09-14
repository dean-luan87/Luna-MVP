# Task State Ownership v1

| State/field | Classification | Owner |
|---|---|---|
| Task identity/version | AUTHORITATIVE | Task Manager |
| Task lifecycle | AUTHORITATIVE | Task Manager |
| dependency graph | AUTHORITATIVE | Task Manager; source statuses external |
| readiness aggregate | LOCAL_DERIVED / candidate until governed | Task Manager |
| completion conditions | AUTHORITATIVE | Task Manager |
| completion status | AUTHORITATIVE within Task contract | Task Manager |
| behavior constraints | AUTHORITATIVE Task-owned constraint record or ref | Task/Behavior owner |
| Capability refs | REFERENCE_ONLY | Capability Governance |
| Action refs | REFERENCE_ONLY | Action Governance |
| Intent refs | REFERENCE_ONLY | Intent Governance |
| Decision refs | REFERENCE_ONLY | Decision Governance |
| Loop refs | REFERENCE_ONLY | Loop |
| source-state refs | REFERENCE_ONLY | source owners |
| execution/progress evidence | CANDIDATE/REFERENCE_ONLY | downstream execution/evidence owners |

Task must not copy authoritative Intent, A, Brain, Field, Context, Capability,
Action, or Loop payloads.
