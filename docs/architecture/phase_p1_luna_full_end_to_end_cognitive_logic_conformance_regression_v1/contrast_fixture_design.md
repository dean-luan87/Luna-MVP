# Contrast fixture design

The runner uses one controlled office-field evidence baseline and the
canonical CState engine. It compares observed semantic output, not merely
metadata references.

| Category | Pair / case | Controlled change | Expected evidence |
|---|---|---|---|
| `SAME_FIELD_DIFFERENT_ROLE` | `role-owner` / `role-visitor` | Role only | Attention, relation interpretation, or evidence relevance may change; physical field must not be rewritten. |
| `SAME_FIELD_DIFFERENT_TASK` | `task-document` / `task-exit` | Task and task-linked goal only | Information Need, sufficiency threshold, or stop behavior may change. |
| `SAME_FIELD_DIFFERENT_ROLE_AND_TASK` | `role-task-owner` / `role-task-visitor` | Role and Task | Hypothesis, Current World Candidate, or downstream decision may change where justified. |
| `SAME_ROLE_TASK_IRRELEVANT_FIELD_CHANGE` | `task-document` / `irrelevant-clutter` | Irrelevant field detail | Relevant cognitive outputs remain stable. |
| `SAME_EVIDENCE_DIFFERENT_GOAL` | `goal-locate` / `goal-operational-state` | Required information need | Same evidence yields different sufficiency when the operational-state requirement is absent. |
| `SAME_GOAL_MISSING_EVIDENCE` | `missing-evidence` | Required information absent | `INSUFFICIENT`, Information Gap, and no premature Stop. |
| `SAME_GOAL_CONFLICTING_EVIDENCE` | `conflicting-evidence` | Conflicting evidence candidates | Conflict/uncertainty is retained; no World Truth promotion. |

The role/task pairs now enter the controlled replay request and are evaluated
by the same Gateway → A-Route → Cognitive State Formation path. The
missing-evidence and conflict cases continue to exercise the existing
canonical loop behavior. `scenario_id` remains an identity/trace namespace,
not a semantic switch in controlled replay.
