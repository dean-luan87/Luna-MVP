# Verification

The Verifier fails closed unless exactly the two named cases are present,
canonical runtime proofs exist, all required traceability fields resolve, and
the Case B causal chain preserves exact Cycle 1 identities.

It separately checks:

- one-cycle sufficient stop for Case A;
- two-cycle Gap/Re-observation/Revision linkage for Case B;
- closure after Stop and assimilation after closure;
- existing owner/status boundaries;
- all forbidden capability and mutation flags;
- empty validation errors.

Remediation record: `e2e_verifier_forbidden_behavior_boolean_semantics_mismatch`
was a verifier/test-infrastructure defect. `forbidden_behaviors` is the
normalized closure view produced by the Runner, so each value must be `true`
for the corresponding raw forbidden behavior to be confirmed closed. Raw
runtime flags remain required to be `false`; no runtime behavior is changed.

## Cognitive logic conformance

The operational verifier evidence must be evaluated separately from the
shared [Luna Cognitive Logic Conformance Test Contract](../luna_cognitive_logic_conformance_test_contract_v1.md).
For this baseline, that includes Brain boundary ownership, Field/evidence
semantics, canonical Hypothesis and Current World Candidate production,
minimum sufficient cognition, Gap/Re-observation/Revision causality, Stop
correctness, and the absence of World Truth promotion or irrelevant
over-observation. Future result output must expose
`operational_result` and `cognitive_logic_result`; `final_decision=GO` requires
both to be `PASS`.

User commands:

```text
python -m capabilities.midplatform.core.cognitive_flow.integration.cognitive_end_to_end_controlled_integration_and_closure.runner_v1
python -m capabilities.midplatform.core.cognitive_flow.integration.cognitive_end_to_end_controlled_integration_and_closure.verifier_v1 _eval_out/cognitive_end_to_end_controlled_integration_and_closure_v1/runner_summary_v1.json
```
