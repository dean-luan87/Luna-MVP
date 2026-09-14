# Negative Guards

The controlled integration rejects `task_handoff_without_valid_decision`
before invoking Task Manager. Positive cases also require:

- no Task handoff before a selected eligible Decision;
- no Decision/Task handoff in Case B cycle 1;
- candidate-only Task state with no runtime dispatch;
- no Action, device control, model, Provider, live Observation, Field,
  Memory, Experience, Learning, or World Truth mutation;
- Task Manager does not own Decision semantics.

