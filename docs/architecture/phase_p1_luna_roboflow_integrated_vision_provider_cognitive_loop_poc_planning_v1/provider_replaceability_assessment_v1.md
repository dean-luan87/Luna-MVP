# Provider Replaceability Assessment

## Existing abstraction assessment

The current repository already has a Provider admission candidate, bounded
provider session, Provider Result/evidence split, Observation Gateway handoff,
canonical Capability/Model/Runtime/Provider references, and a real YOLO adapter
that demonstrates the boundary. This is enough abstraction for the first
Roboflow PoC.

`VisionExecutionProvider` should therefore **not** be introduced now. A new
interface would risk duplicating the already frozen Provider Governance seam.

## Roboflow adapter contract gap to close later

The implementation phase may need a narrow adapter contract for external
request authentication reference (without secrets), endpoint/workflow ref,
request correlation, response status/error mapping, rate/cost metadata and
provider-native detection/OCR payload references. These are Provider adapter
details, not new governance domains.

## Replacement test

The same cognitive trace should be able to replace Roboflow with the existing
YOLO visual adapter or a separate OCR/VLM provider by changing only governed
Provider declarations, binding/admission inputs and adapter implementation.
A, Field, Current World, Evidence Gateway, Hypothesis and Decision contracts
must remain unchanged.

