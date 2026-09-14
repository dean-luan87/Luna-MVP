# Roboflow Provider Boundary

## Allowed provider responsibility

Roboflow may execute an external visual workflow and return provider-native
object detections, OCR text/regions, confidence, timing and provider metadata.
It may choose internal inference details within its declared Provider
contract. That internal choice is not Luna model/capability authority.

The Luna adapter owns translation correctness for the returned payload. The
adapter must output candidate evidence, preserve provenance, and fail closed
on malformed or uncorrelated results.

## Forbidden responsibility

Roboflow must not own Goal, Intent, Attention, Capability Resolution,
Capability↔Model lifecycle, Model Governance, Runtime Admission, Evidence
admission semantics, Current World, Field, Hypothesis, Sufficiency, Decision,
Task, Action, Memory, Experience or Brain outcome authority. It must not write
Field/Current World or declare World Truth.

## Raw schema rule

Roboflow JSON/native schema is allowed only inside the Provider adapter and
trace/provenance storage boundary. Outside that adapter, use existing Luna
candidate evidence contracts. Do not expose a parallel Roboflow-native
canonical type hierarchy.

## Provider admission

The existing `VisionProviderAdmissionCandidateV1` is the intended boundary.
The planned adapter consumes Observation/Runtime/Provider admission refs and
returns a Provider Result. Provider admission does not imply health, model
loading, or invocation success.

## Replaceability

Roboflow should be one Provider implementation behind the existing contract;
local YOLO, OCR Tool, or a later VLM can use the same admission/result/evidence
shape. A new `VisionExecutionProvider` interface is therefore not required
for the first PoC. Add one only after a concrete missing field in the
existing Provider contract is demonstrated and reviewed.

