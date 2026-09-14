# Evaluation World / Observation Corpus

Dataset is primarily a source of worlds and observations for Luna cognition,
not a training or model-ranking system.

It should represent variation in information density, missingness, conflict,
long-tail conditions, temporal change, role, context, and distractors. Public
benchmarks, Luna scenarios, and future real observations remain distinct
dataset classes.

`World Sample × Cognitive Task × Goal × Role × Environment Condition ×
Cognitive Difficulty × Controlled Perturbation × Available Capability Set`
`→ Cognitive Test Case`.

No sample is automatically a test case. No `_tmp_eval_inputs`, `_tmp_eval_out`,
`_eval_out`, RF-DETR smoke result, or TestBoard artifact is automatically
registered.
