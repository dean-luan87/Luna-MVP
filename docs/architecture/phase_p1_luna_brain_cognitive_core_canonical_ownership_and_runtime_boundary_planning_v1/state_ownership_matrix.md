# State ownership matrix

## Brain-local coordination state

Future Brain coordination state may contain only bounded, traceable local
references and control metadata:

- active `goal_ref`, `concern_ref`, and `intent_ref`;
- active `cognitive_loop_ref` and execution refs;
- active `information_need_ref`;
- pending Gap/Re-observation/next-cycle refs;
- pending Closure Candidate and Assimilation Candidate refs;
- coordination status, lifecycle status, and authorized resource/budget refs;
- provenance and version refs.

This state is not a second source of truth for the referenced objects.

## External canonical state

Brain may reference, request, or consume these externally owned states but must
not duplicate or mutate them:

| State | Source of truth | Brain access |
|---|---|---|
| Intent | Intent Governance | Reference/request |
| Context | Context Foundation | Reference |
| Role/identity | Role or Self owner when established | Reference |
| Field | Field State Reducer | Reference |
| Evidence | Source producer and Observation Gateway | Consume admitted refs |
| Current World / Hypothesis | Cognitive State Formation Governance | Consume candidates |
| Sufficiency / Gap / Stop | Cognitive State Formation Governance | Consume results |
| Re-observation | Field Perception Orchestrator | Request/consume ref |
| Decision | Decision Governance | Reference only |
| Task | Task Manager | Reference only |
| Memory / Experience | Cognitive Memory & Experience Governance | Candidate request only |
| Emotion | Emotion integration boundary | Reference only |
| Learning | Cognitive Learning Governance | Candidate request only |

No Brain-local mirror may be promoted to Field State, Memory, Experience,
Knowledge, or World Truth.
