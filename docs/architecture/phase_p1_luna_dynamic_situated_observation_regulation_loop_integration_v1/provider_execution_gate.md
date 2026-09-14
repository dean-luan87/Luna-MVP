# Provider Execution Gate

The phase does not create a Provider Runtime. It delegates execution to:

`Situated Capability Eligibility → SituatedCapabilityExecutionAdmissionV1`
`→ RealOCRProviderExecutionEngineV1`

The only real Provider/Model path is the existing RapidOCR / ONNXRuntime
implementation with canonical identities:

- capability: `text_recognition`;
- provider: `provider:ocr_v1`;
- model: `model:ocr_v1`;
- native implementation/model asset: `rapidocr_onnxruntime_v0`.

For waiting, not-required, or lost-opportunity states, the gated Engine is not
called. For an executing eligible state, it is called once for that state and
its returned runtime result is reused for all regulation output projections.

`eligible_now=true` is not itself a Provider invocation. Existing Provider
Runtime admission remains authoritative after the situated gate.
