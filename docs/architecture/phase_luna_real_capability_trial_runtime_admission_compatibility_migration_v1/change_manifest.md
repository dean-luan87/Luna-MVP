# Change Manifest

## Modified

- Existing Real Capability trial adapter: inserted the candidate seam before
  Provider admission.
- Existing trial result type: added migration diagnostics with defaults.
- Existing trial Runner: exposed migration diagnostics while retaining legacy
  fields.
- Existing trial Verifier: added Runtime Admission and single-invocation checks
  and registered the helper in the exact source set.

## Created

- Trial-local runtime admission compatibility helper.
- This phase documentation directory.

## Not modified

- Provider implementation/selection
- YOLO11n model contract
- Consolidated regression harness
- Brain/A/B/Loop authority
- Canonical enums or owners

## Execution

Python, Runner, Verifier, pytest, py_compile, Provider, model, YOLO, camera and
OCR were not executed or invoked.

