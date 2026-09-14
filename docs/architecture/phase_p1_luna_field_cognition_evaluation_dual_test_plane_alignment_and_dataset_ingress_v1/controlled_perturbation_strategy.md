# Controlled Perturbation Strategy

Future cases may vary one or more dimensions:

- irrelevant objects, clutter, occlusion, false/conflicting/stale/duplicated/
  delayed evidence;
- confidence, lighting, viewpoint, target count, distractor similarity;
- wrong attention target selection;
- capability availability, observation budget, latency/resource;
- Role, Goal, Context, prior Field;
- missing and changing environment information.

Perturbations test Luna's cognitive robustness and ownership boundaries. They
are not merely model robustness tests. Each perturbation must retain a version,
provenance, affected refs, and expected process class.

## Canonical vocabulary

The Level-1 suite's canonical perturbation vocabulary is
`capabilities/evaluation/level1_field_cognition_suite/types_v1.py::PERTURBATION_KINDS`.
The attention-target perturbation is named `wrong_attention` in case
references. The diagnostic category `wrong_attention_trap` uses this
perturbation together with `irrelevant_clutter`; the category ID and the
perturbation kind are distinct identifiers.
