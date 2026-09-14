# Phase-P1 Luna Real OCR Provider Execution Integration v1

This phase adds one real OCR provider execution path to the already verified
shared Provider Runtime. The selected canonical provider is `ocr_v1`, whose
existing local implementation is RapidOCR/ONNXRuntime.

The bounded path is:

`Observation Demand → OCR Capability Requirement → Universal Capability Slot
Resolution → OCR Provider Resolution → ProviderRuntimeRequestV1 → LIVE_RUNTIME
RapidOCR invocation → ProviderRuntimeResultV1 → RuntimeObservationEnvelopeV1
→ Observation Gateway → OCR/Text Evidence Candidate → A-Route → Cognitive
State Formation → Sufficiency / Information Gap / Stop`.

The phase stops before Decision, Task, Action, Runtime Executor, device control,
field mutation, and World Truth declaration. The Agent performed only static
inspection and code/document changes. Real OCR execution remains pending until
the user runs the Runner in the terminal.

## Static audit conclusion

Static audit count: 5 callable real OCR implementation families (with RapidOCR
represented by multiple aliases/variants), plus stub/disabled adapters:

- RapidOCR/ONNXRuntime;
- PaddleOCR;
- macOS Vision OCR;
- EasyOCR;
- Tesseract.

The concrete adapter/alias inventory is:

- RapidOCR/ONNXRuntime (`capabilities/model_ocr/rapidocr_adapter_v0.py`, plus
  the older `capabilities/ocr_runtime` wrapper and v4/v5 variant adapters);
- PaddleOCR (`capabilities/model_ocr/paddleocr_adapter_v0.py`), but its current
  manifest is fail-closed until local det/rec weights exist;
- macOS Vision OCR (`capabilities/model_ocr/macos_vision_ocr_adapter_v0.py`),
  a system fallback requiring Darwin and Swift;
- EasyOCR and Tesseract, plus historical/stub adapters, which are not the
  selected canonical runtime path.

RapidOCR is the smallest existing local integration: it has a real image
entrypoint, text/score/polygon output, and models bundled by the
`rapidocr-onnxruntime` package. No network download is requested by this
phase.
