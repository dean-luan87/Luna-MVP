# Dataset as World / Observation Corpus Relationship

## Correct role

The Dataset Registry is **Evaluation World / Observation Corpus
Infrastructure**, not a Model Benchmark Dataset Registry.

It supplies varied worlds and observations:

- information density;
- missingness and conflict;
- visual/environment conditions;
- long-tail and distribution shifts;
- temporal change;
- role/task context.

## Relationship

`World Sample`
× `Cognitive Task`
× `Goal/Concern`
× `Role`
× `Condition`
× `Available Capability`
→ `Cognitive Test Case`

Dataset Registry remains under `capabilities/evaluation/dataset_registry/`.
It does not own Field, Current World, Evidence semantics, or Truth.

The prior four declarations remain: Dataset entry, sample manifest,
annotation/GT ref, and benchmark spec. They serve Cognitive Evaluation and
must gain task/condition/observation references in a later implementation.
