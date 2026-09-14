# Implementation Overview

The bounded integration package contains:

- reference-only A semantic decision types;
- A grant validation against the existing authority grant candidate types;
- a compatibility wrapper for existing Dynamic Flow output;
- a semantic-decision-to-mechanical-command bridge using the existing Loop
  command validation and state candidates;
- 36 synthetic scenarios with compact Runner/Verifier output.

The wrapper changes authority interpretation at the controlled boundary only:
Dynamic Flow may still compute values internally, but its output is not treated
as the semantic authority owner. The emitted decision candidates carry
`decision_owner_ref = A_REASONING_ROLE`.
