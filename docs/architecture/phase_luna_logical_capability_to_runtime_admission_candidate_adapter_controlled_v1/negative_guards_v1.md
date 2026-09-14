# Negative Guards

- `candidate_only = true`
- `synthetic_only = true`
- Provider invocation is false
- model loading/inference is false
- checksum computation is false
- dependency probe is false
- runtime/device health probe is false
- logical `READY_CANDIDATE` is not executable readiness
- A and Brain do not select model/provider
- Loop does not judge admission
- no Runtime Admission Manager, Model Manager, or Scheduler is created
- no camera/OCR/YOLO/action/learning/memory/experience execution

