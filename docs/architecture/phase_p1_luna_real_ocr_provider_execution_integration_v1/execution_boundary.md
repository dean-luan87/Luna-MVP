# Execution Boundary

Allowed in this phase:

- one bounded local image input;
- one real RapidOCR provider/model invocation under `LIVE_RUNTIME`;
- provider-native result capture and candidate-only normalization;
- Gateway admission and A-Route/Cognitive State Formation handoff.

Forbidden in this phase:

- recorded, synthetic, hardcoded, or fixture-as-provider OCR output;
- OCR text promotion to Fact, World Truth, or current-world mutation;
- Decision, Task, Action, Runtime Executor, device control, or field mutation;
- provider fallback orchestration, OCR enhancement, semantic correction,
  cross-modal fusion, VLM, video, or camera streaming.

The Runner reports `provider_invoked` and `model_invoked` from the native
adapter result. It does not assert those values before the provider call.
