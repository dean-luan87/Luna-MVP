# Cognitive Test Case Taxonomy

## Orthogonal dimensions

- world/sample reference;
- cognitive task and Goal/Concern;
- Role and Context;
- environment condition and field state;
- information density and distribution shift;
- available capabilities and external implementation refs;
- cognitive difficulty;
- resource constraint;
- expected observation requirement;
- evidence quality, conflict, missingness, uncertainty, and staleness;
- expected admissible process class: stop, re-observe, or Decision handoff.

## Sample is not case

`World Sample × Cognitive Task × Goal × Role × Condition × Available Capability`
produces a Cognitive Test Case. One image or video may therefore support
multiple tasks without duplicating the world sample.

## Assertion policy

Cases assert structural and governance invariants, such as “a missing expected
evidence kind must remain insufficient” or “a targeted gap must produce a
targeted re-observation candidate.” They must not hardcode the correct door,
label, hypothesis answer, or model output.
