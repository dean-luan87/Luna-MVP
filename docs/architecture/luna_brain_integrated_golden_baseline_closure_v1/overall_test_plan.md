# Overall test plan

User-terminal execution groups are ordered as:

1. S3-Y11 real provider boundary
2. B1, B2, B3, B4 Brain stages
3. B5 Golden Baseline governance
4. C01-C36, O01-O36, Intent, and Decision synthetic regressions

The closure package records results explicitly and never orchestrates these
groups automatically.

## Dual acceptance doctrine

The closure package references the shared [Luna Cognitive Logic Conformance
Test Contract](../luna_cognitive_logic_conformance_test_contract_v1.md).
Future closure reports must expose `operational_result` and
`cognitive_logic_result` independently. `final_decision=GO` requires both to
be `PASS`; an operationally successful regression cannot conceal cognitive
logic non-conformance.
