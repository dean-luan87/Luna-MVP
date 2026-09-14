# Reality Context Projection Go/No-Go v1

## Required checks

- Reality Context Projection is a bridge, not a Situation Engine.
- Output contains Observable State, State Change, Relevant Constraints, Unknowns, and Provenance.
- Projection does not interpret facts or add risk, danger, emotion, recommendation, plan, prediction, or Decision.
- Reality State and Context Package remain distinct from Situation.
- Unknown Propagation preserves explicit unresolved information.
- Context Provenance preserves source, timestamp, confidence, uncertainty, validity, and transform trace.
- A Route receives a bounded read model and performs Situation Understanding.
- Context Bridge is read-only and cannot modify Reality State or bypass Brain.

## Hard prohibitions

No Situation Engine. No raw model-to-A-Route path. No direct Reality Database dump.
No real model. No OCR. No SLAM. No Hardware, no Action Runtime, no Planning, no
Prediction, no Emotional Engine, no online learning, and no State mutation.

## Verification handoff

The agent performs planning and V0 static checks only. User Terminal runs the
phase verifier and returns all required sections. The agent stops at
`WAITING_FOR_USER_TERMINAL_VERIFICATION`.

Target output: `COGNITIVE_REALITY_CONTEXT_PROJECTION_ARCHITECTURE_READY_WITH_NOTES`.
