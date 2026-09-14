# Integration Contract

The adapter composes:

```text
verified Task-to-Action result
  → ActionGovernanceInputV1
  → ActionGovernanceEngineV1.run_case
  → ActionCandidateV1
  → ExecutionReadinessCandidateV1
  → ActionToRuntimeExecutorHandoffCandidateV1
```

The adapter preserves the existing Action Governance request and output. The
Action Governance `runtime_handoff.handoff_id` is carried as the
`execution_eligibility.ref` because the canonical readiness candidate has no
separate identifier. It is not a newly fabricated readiness object.

The allowed terminal state is candidate-only:

- readiness: `candidate_ready`;
- Action state: `READY_CANDIDATE`;
- Runtime Executor handoff: candidate-only;
- `action_executed=false`;
- `device_control_executed=false`;
- `runtime_executor_invoked=false`.

`READY_CANDIDATE` and `candidate_ready` never imply execution.

The canonical input does not expose a distinct risk-ref contract. Risk is not
silently treated as validated: the output reports that signal as unavailable,
while the existing safety, precondition/dependency, resource, confirmation,
and reversibility gates remain authoritative.
