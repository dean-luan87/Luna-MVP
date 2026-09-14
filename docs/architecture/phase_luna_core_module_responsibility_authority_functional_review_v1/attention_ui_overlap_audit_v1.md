# Attention UI Overlap Audit v1

Object capsules, HUD colors, priority panels, focus regions, attention scores,
follow-up model suggestions and human-correction signals are UI/TestBoard or
candidate-layer representations.

The Observation Attention Layer explicitly marks them candidate-only,
not-fact, not-navigation, not-runtime and not-speech output. Human correction
is a priority signal candidate, not ground truth.

UI may render or filter Attention candidates. It must not define canonical
Attention ownership, mutate source envelopes/model output, trigger a follow-up
route, select a Provider or promote labels to facts.

The static-site engine and TestBoard records are therefore classified as
`COMPATIBILITY_ONLY` / presentation-layer evidence, not a separate Attention
authority.
