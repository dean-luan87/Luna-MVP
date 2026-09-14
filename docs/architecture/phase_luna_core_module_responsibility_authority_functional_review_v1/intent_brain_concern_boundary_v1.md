# Intent / Brain / Concern Boundary v1

Brain owns Goal identity, Goal admission and global priority/constraint
governance. Intent Governance owns Intent identity and lifecycle. A Goal can
motivate or constrain an Intent proposal, and Brain can request that an Intent
be reconsidered, but Brain does not directly mutate Intent state.

Intent Governance may return a `NewConcernCandidate`-like causal or concern
handoff reference when an Intent implies a separate cognitive work direction.
The handoff is candidate-only. Brain alone admits, rejects, defers, merges or
splits a Concern. An Intent therefore cannot silently create a Concern or
cause Loop materialization.

The repository's current `IntentToCausalHandoffCandidateV1` is evidence of a
bounded downstream handoff, not proof that Causal Governance has replaced
Brain as Concern owner. Its `candidate_only`, `decision_output=False`,
`action_output=False`, and `task_output=False` fields preserve this boundary.
