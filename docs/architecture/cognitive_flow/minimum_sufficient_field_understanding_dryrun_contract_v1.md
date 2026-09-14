# Minimum Sufficient Field Understanding Controlled DryRun Contract v1

## Fixture contract

Each fixture supplies a Field reference, identity status, constraint reference, behavior boundary, explicit information gap, temporal/spatial scope, task reference, provenance, and trace. The only allowed identity statuses are `known`, `partially_known`, and `unknown`.

The public-space fixture may contain a Neighbor Field reference inside candidate context. It is evidence for a constraint candidate only; it cannot produce an Identity Fact. The exploration fixture fixes `exploration_candidate=true` and `permission_granted=false`.

## Output contract

The runner writes canonical `dryrun_result_v1.json`; every candidate remains `candidate_only`, `not_fact`, `not_state`, `not_decision`, and `not_action`. It also records fixture-only/simulation-only flags, six cases, all negative guard identifiers, and the run1/run2 equality result.

## Verifier contract

The verifier reads only `dryrun_result_v1.json`, writes `verification_result_v1.json`, and checks case inventory, identity-status coverage, provenance/trace closure, candidate flags, no forbidden authority fields, exploration non-permission, no external/runtime flags, and determinism.
