# Integration Contract

Only a canonical proof with `SUFFICIENT`, a sufficiency ref, a Stop ref,
Current World ref, hypothesis refs, and evidence refs can produce a cognitive
Decision handoff candidate. The adapter then maps those read-only refs into
`DecisionGovernanceInputV1`.

Decision Governance remains the owner of Decision Candidate formation. Its
existing output remains `candidate_only=true`, `decision_output=false`,
`action_output=false`, and `task_output=false`.

