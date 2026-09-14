# LUNA — PaddleOCR Fairness Review Before Provider Decision v0

## Phase

- **Phase-ModelOCR-006**

## Mandatory caveat

Current benchmark path for PaddleOCR is **not a fair final comparison baseline** for provider decision, because:
- path remains impacted by skeleton/init-biased adapter behavior
- `cls` is `missing_optional`
- rotated/orientation-sensitive capability is `not_claimed`
- current latency/bbox numbers are not equivalent to full real-inference path comparison

## Required status

- `unfair_current_path=true`
- `needs_real_inference_path=true`
- `needs_same_input_same_gt=true`
- `no_default_decision_allowed=true`

## Next suggested phase

- **Phase-ModelOCR-006A**: PaddleOCR Real Inference Raw Text Evaluation v0
