# Verification

The verifier requires exactly Case A and Case B, admitted Task state before
Action handoff, one final Action handoff per case, canonical Action candidate
and trace linkage, and no cycle-1 Action path for Case B.

It recalculates the candidate/readiness, trace, handoff, read-only-reference,
and no-side-effect checks from the serialized runner output. The negative
fixture must report a canonical rejection and `action_boundary_invoked=false`.

Runtime execution remains user-terminal owned.

## Dual acceptance dimensions

This phase's operational checks are one input to the reusable [Luna Cognitive
Logic Conformance Test Contract](../luna_cognitive_logic_conformance_test_contract_v1.md).
Any major E2E or full-regression result that includes this boundary must report
`operational_result` and `cognitive_logic_result` independently. Final `GO`
requires both to be `PASS`; an operationally valid Task-to-Action candidate
does not by itself prove cognitive logic conformance.
