# Test Case Taxonomy

## Orthogonal dimensions

Each test case should select values across independent dimensions:

- `task`: object detection, OCR, navigation-like understanding, depth, SLAM,
  multimodal observation, etc.;
- `dataset_ref` and `sample_ref`;
- `environment_condition`: lighting, clutter, motion, occlusion, viewpoint,
  weather, audio noise, or temporal change;
- `data_distribution`: public benchmark, Luna scenario, real observation,
  synthetic/curated, in-distribution or shifted;
- `model_ref` and immutable `model_version`;
- `provider_ref` and provider/binding version;
- `capability_ref` and requirement version;
- `cognitive_difficulty`: direct, ambiguous, conflicting, incomplete,
  temporally changing, multi-cycle;
- `resource_constraint`: latency, memory, compute, network, energy, or unknown;
- `expected_observation_requirement`: one observation, targeted ROI, multiple
  modalities, re-observation, or no additional observation expected;
- `cognitive_strategy`: single-pass, evidence-first, compare, verify, or
  re-observe candidate.

## Case is not sample

A sample is an input/data member. A test case is a governed evaluation
composition. The same sample may be paired with multiple tasks, conditions,
models, versions, providers, and cognitive strategies:

`Sample × Task × Model × Model Version × Condition × Cognitive Strategy`

The case manifest should reference a sample and retain its own case identity,
expected evidence contract, resource profile, and trace policy.

## Expected outcome policy

Expected fields should describe structural requirements and admissible outcome
classes, not hardcode a semantic answer. For example, a case may require an
information-gap trace when evidence coverage is insufficient, while allowing
the actual hypothesis content to remain a candidate produced by Luna.
