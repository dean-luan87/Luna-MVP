# Change Manifest

Added under the shared Provider Runtime package:

- `real_ocr_provider_adapter_v1.py`
- `real_ocr_provider_execution_engine_v1.py`
- `real_ocr_provider_execution_runner_v1.py`
- `real_ocr_provider_execution_verifier_v1.py`

Modified shared contracts/adapters:

- `ProviderRuntimeResultV1` now carries optional normalized OCR candidate
  payload and error category;
- `RuntimeObservationEnvelopeV1` now carries optional OCR output candidate and
  explicit empty-result state;
- Gateway evidence can retain a candidate payload and distinguishes
  `ocr_empty_success` from text evidence;
- existing RapidOCR adapter reports derived invocation flags and distinct
  unavailable, invalid-image, invocation-exception, and malformed-output
  categories;
- package exports include the OCR execution engine;
- architecture README includes this phase.

The existing YOLO runtime path was not rewritten and no second Provider Runtime
was created. No registry identity was fabricated or replaced.
