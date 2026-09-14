# Selected Provider

## Canonical identity

- Capability registry identity: `text_recognition`
- Capability requirement kind: `OCR_TEXT_EVIDENCE` / `TEXT_READ`
- Canonical provider/model registry identity: `ocr_v1`
- Provider request ref: `provider:ocr_v1`
- Model request ref: `model:ocr_v1`
- Native implementation identity: `rapidocr_onnxruntime_v0`
- Native model config identity: `rapidocr_onnxruntime_v0`

The canonical identities are resolved from the existing capability, provider,
and model registries. The native RapidOCR identifiers describe the existing
implementation behind the canonical `ocr_v1` binding; they do not replace the
canonical registry identity.

## Selection rationale

RapidOCR satisfies the phase priorities: existing implementation, local
runtime, no network at invocation, existing model assets in its package,
existing raw text adapter, and the smallest integration gap. PaddleOCR has a
more elaborate pinned-weight adapter but its repository manifest says the
weights are not present. macOS Vision is retained as a system fallback, not a
new provider in this phase.

## Invocation owner

Only `Capability/Provider Runtime` invokes RapidOCR. The OCR adapter owns
native-output normalization; Observation Gateway owns admission; A-Route and
Cognitive State Formation own downstream cognition. No business module calls
the OCR provider directly.
