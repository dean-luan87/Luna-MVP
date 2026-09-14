# Cognitive State Formation review

The inspected State Formation assets primarily assemble candidate representation and owner-scoped handoffs:

- `CognitiveStateFormationEngineV1` constructs state output;
- `CurrentWorldCandidateV1`, hypothesis, attention and trace/provenance types preserve source references;
- static validators enforce candidate-only, read-only Field/World and hypothesis boundaries;
- B2 maps Current World input into Cognitive State / Cognitive Flow and carries an observation-need bridge.

Disposition: KEEP_AS_STATE_REPRESENTATION. Do not move State Formation wholesale into A or Loop. A consumes the assembled working context and judges local semantic impact; Loop records versions and refs. Any State Formation behavior that starts selecting Need or Sufficiency should be treated as a later owner audit, not assumed from the presence of fields.

