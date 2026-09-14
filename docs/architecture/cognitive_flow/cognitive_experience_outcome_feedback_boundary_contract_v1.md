# Experience Outcome Feedback Boundary Contract v1

## Input boundary

Permitted inputs are governed references to Decision Commitment, Context, Field/View, Survival, Mission, Behavior/Decision candidates, expected outcome, observed outcome evidence, unexpected event candidate, Experience Candidate, Learning Candidate, emotion importance/salience/preference candidate, provenance, and trace.

Raw model output, provider payload, Fact Store, State handle, Reducer command, Decision result asserted as truth, Action command, Permission grant, Memory, model-training output, Learning execution result, or Hive/Library output asserted as authority are forbidden.

## Output boundary

Outcome, Outcome Evaluation, Experience, Learning Candidate Feedback, and Future Cognitive Influence outputs remain `candidate_only=true`, `not_fact=true`, `not_state=true`, `not_decision=true`, `not_action=true`, `not_permission=true`, and `not_memory=true`.

## Negative guards

- Outcome != Truth.
- Experience != Reality Replacement.
- Failure != Negative Learning.
- Success != Correct Reasoning.
- Pattern != Rule.
- Experience != Shortcut.
- Hive != Experience Authority.
- Reducer != Learning Authority.
- Emotion != Experience Rewrite or Truth.
- Learning Candidate != Automatic Cognitive Flow Mutation.
- Reducer remains the only State Mutation Authority.
