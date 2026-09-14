# Task / A Route and Product Loop Overlap v1

Historical A Route/Product Loop stages combine lifecycle coordination,
observation requests, capability routing, task handoffs, decision/action
references, and recovery. The current architecture treats that structure as
orchestration, not a new Task owner.

| Historical responsibility | Canonical target |
|---|---|
| Task identity/readiness/completion | Task Manager |
| Need, evidence relevance, reconsideration | A |
| Decision choice/adjudication | Decision Governance |
| Capability scope/resolution/admission | Capability Governance / Runtime Admission |
| Action admission/execution | Action Governance/runtime |
| cognitive persistence | Loop |
| global stop/priority/permission | Brain |
| broad stage sequencing | legacy orchestration adapter |

The route should eventually become a handoff coordinator. It must not remain a
monolithic source of Task, Capability, cognition, or Loop authority.
