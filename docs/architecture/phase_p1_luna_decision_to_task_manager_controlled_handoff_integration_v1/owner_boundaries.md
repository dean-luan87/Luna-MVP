# Owner Boundaries

| Responsibility | Owner |
|---|---|
| Cognition and readiness for Decision | Cognitive State Formation Governance |
| Decision Candidate and Decision trace | Decision Governance |
| Decision-to-Task candidate handoff | Decision Governance output consumed through this adapter |
| Task admission, Task state, lifecycle, dependencies | Task Manager |
| Action execution | Action Boundary; not invoked |
| Brain / CState Decision or Task execution | Forbidden |

The adapter transports references and does not create a Decision Candidate or
execute a Task.

