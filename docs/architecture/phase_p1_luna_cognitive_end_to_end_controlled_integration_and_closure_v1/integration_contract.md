# Integration Contract

The new Runner is a thin composition layer over
`brain_cognitive_loop_closure_assimilation_controlled.build_brain_closure_run_v1`.
It does not construct Current World, Hypothesis, Sufficiency, Gap,
Re-observation, Revision, or Stop objects.

The canonical path remains:

`Brain-domain request → Information Need Candidate → Observation Gateway →
A-Route → Cognitive State Formation → closure candidate → assimilation
candidate`.

The raw canonical case payload is retained in the transient summary so the
Verifier can validate source linkage rather than trusting projected fields.
