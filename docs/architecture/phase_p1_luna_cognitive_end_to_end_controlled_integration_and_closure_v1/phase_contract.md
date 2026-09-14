# Phase Contract

Implement one controlled end-to-end baseline over existing canonical assets.
The Runner covers exactly two cases and the Verifier proves the complete
causal chain. Brain authority fields remain `BRAIN` and
`OWNER_UNRESOLVED` where the existing contract leaves them unresolved.

No new Brain owner, governance system, runtime capability, model/provider path,
live observation, or downstream mutation is permitted.

Acceptance is dual-dimensional under the shared [Luna Cognitive Logic
Conformance Test Contract](../luna_cognitive_logic_conformance_test_contract_v1.md):
operational correctness and cognitive logic conformance must each be `PASS`
before `final_decision=GO`. Neither a successful runner nor a single
undifferentiated verifier PASS is sufficient.
