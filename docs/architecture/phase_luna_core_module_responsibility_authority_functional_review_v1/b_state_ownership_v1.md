# B-CR State Ownership

| State | Classification | Owner/boundary |
|---|---|---|
| B request execution context | LOCAL_DERIVED / execution-local | B within A request |
| branch tree | LOCAL_DERIVED | B, bounded and traceable |
| temporary branch hypotheses | LOCAL_DERIVED | B candidates only |
| resource/branch/depth usage | MECHANICAL_LOCAL | B reports usage |
| B result | CANDIDATE | B produces; A evaluates |
| source refs | REFERENCE_ONLY | Brain/A/source owners |
| A active Hypotheses | EXTERNAL | A |
| A Need/Sufficiency/Next-step | EXTERNAL | A |
| Brain state | EXTERNAL | Brain |
| Loop lifecycle | EXTERNAL/MECHANICAL | Loop |

B owns no authoritative persistent semantic state.
