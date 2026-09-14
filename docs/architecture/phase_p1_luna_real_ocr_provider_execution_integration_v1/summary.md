# Summary

This implementation prepares one callable real OCR path using the existing
canonical `ocr_v1` binding and RapidOCR/ONNXRuntime. It reaches the shared
Provider Runtime result, Runtime Observation envelope, Observation Gateway,
A-Route, and Cognitive State Formation boundaries, then stops at sufficiency /
information gap / stop.

OCR output is candidate-only. `truth_declared=false`, evidence remains
candidate evidence, and no Fact, World Truth, Decision, Task, Action, Runtime
Executor, device, or field mutation is allowed.

The user must execute the Runner and then the Verifier in the terminal. Until
that result is supplied, the phase status is:

`WAITING_FOR_USER_TERMINAL_VERIFICATION`

The long-term integration standard is maintained in the [Luna External Model /
Provider Integration SOP v1](../luna_external_model_provider_integration_sop_v1.md).
