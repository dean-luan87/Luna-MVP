# Runtime Data Conformance Contract

The audit consumes actual runner summaries and archived bounded metadata. It
checks identity, ownership, cycle, transition, causal, governance, and
negative-guard data.

For replay, required claims are `CONTROLLED_REPLAY_RUNTIME`, canonical Gateway
admission, canonical A-Route execution, canonical Cognitive State Formation
proof, and no model/provider/live-observation/action/Field mutation.

For the two-cycle case, exact prior Gap, Re-observation, and next-cycle ingress
refs must appear in the second-cycle replay and revision proof. Missing stages
remain unavailable; they are not converted to success or zero.

The cognitive behavior portion of this audit follows the shared [Luna
Cognitive Logic Conformance Test Contract](../luna_cognitive_logic_conformance_test_contract_v1.md).
Runtime data conformance must therefore report the operational result and the
cognitive-logic result independently; the latter cannot be inferred from
runner exit status or verifier PASS alone.
