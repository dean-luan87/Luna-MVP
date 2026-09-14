# Cognitive Continuous Runtime Validation v1

## V1 synthetic scenarios

1. `task_continuity`: conversation -> airport request -> route question -> precaution question -> task closed. Verifies Context, Goal, Workspace, Schema, Attention, Retention, and Activation transition candidates.
2. `environment_change`: mall entry -> store search -> target absent -> alternate plan. Verifies Unknown increase, Hypothesis revision, Attention reallocation, Workspace replanning, and the frozen reasoning-mode interface.
3. `error_recovery`: initial hypothesis -> contradicting evidence. Verifies Hypothesis Revision Candidate without deleting Experience or modifying a long-term asset.

## V1 criteria

- same synthetic stream produces an identical replay signature;
- each record exposes snapshot references, transition reasons/confidence candidates, retention/activation references, candidate trace, and authority checks;
- all state, action, decision, permission, memory, experience, reducer, reality, and B-route execution flags remain false; and
- transitions are evaluated candidates for a future tick, never commands.
