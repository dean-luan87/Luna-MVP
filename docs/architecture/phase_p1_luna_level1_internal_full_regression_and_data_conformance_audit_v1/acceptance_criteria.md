# Acceptance Criteria

The final GO candidate requires all three independent conditions:

- Execution health: every P0 current runner/verifier path passes and required
  P1 coverage is either passing or explicitly blocked.
- Runtime data: no BLOCKER or MAJOR ownership, causal, cognition, identity, or
  governance finding.
- Artifact data: no BLOCKER or MAJOR output, archive, White-box, provenance,
  or cross-reference finding.

The consolidated audit verifier must pass, and the user must review the
generated JSON/Markdown report. Agent preparation alone cannot declare GO.

## Mandatory cognitive-logic dimension

In addition to the three audit layers above, the regression must evaluate the
shared [Luna Cognitive Logic Conformance Test Contract](../luna_cognitive_logic_conformance_test_contract_v1.md)
as an independent result:

- `operational_result: PASS` — current P0 execution health and required
  runtime paths operate as contracted;
- `cognitive_logic_result: PASS` — the observed cognitive chain, perspective
  conditioning, ownership, evidence/truth boundaries, sufficiency, stopping,
  and observation economy conform to the shared assertions.

`final_decision: GO` is valid only when both values are `PASS`, with no
BLOCKER/MAJOR runtime or artifact finding. A verifier-only PASS or an
operational PASS cannot substitute for cognitive-logic conformance.
