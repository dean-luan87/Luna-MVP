# Negative Guards

Registry and case composition must reject or preserve:

- automatic directory scanning or promotion from `_tmp_eval_inputs`,
  `_tmp_eval_out`, or `_eval_out`;
- image/base64/provider payloads embedded in registry records;
- missing dataset/sample provenance, source version, or identity;
- runtime-enabled Dataset, sample, annotation, benchmark, or case;
- evaluation GT represented as World Truth;
- semantic answer fields in cognitive assertions;
- Plane A and Plane B result collapse;
- evaluator mutation of Goal, Attention, Evidence, Current World, Field,
  Hypothesis, Sufficiency, Decision, Task, or Action;
- model/provider/observation execution during registration or composition;
- unavailable runtime metrics encoded as zero/false;
- automatic model selection or Model Manager binding mutation.
