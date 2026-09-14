# Luna Roboflow Integrated Vision Provider Cognitive-Loop PoC Plan

## Disposition

`PLANNING_ONLY` / `NO_RUNTIME_EXECUTION` / `NO_ROBOFLOW_EXECUTION`.

This package plans the smallest PoC that tests whether Luna can consume an
external visual result and return the result to governed cognition. It does
not promote Roboflow into a Luna authority and does not add a parallel
provider or governance architecture.

## Evidence-based conclusion

The shortest reusable path is:

`A/Goal requirement → Observation Demand/Request → Capability Requirement → governed Capability/Model + Runtime Admission → Provider Admission → external Vision Provider adapter → Provider Result → Evidence/Gateway → Current World candidate and/or Field Event candidate → Cognitive State Formation/A → Evidence Sufficiency → Decision candidate or Next Observation candidate`.

The repository already contains the main candidate contracts and a tested
real-YOLO governance seam. A Roboflow PoC should implement an adapter behind
that seam. A new `VisionExecutionProvider` abstraction is not required for the
first PoC because `VisionProviderAdmissionCandidateV1`, the existing provider
adapter boundary, Observation contracts, and evidence handoff types already
express the required lifecycle. Reconsider only if an external-request
contract gap is proven.

## Current blockers

- No Roboflow runtime/provider declaration or adapter was found; existing
  Roboflow assets are dataset/test-source dry-run assets.
- The existing generic visual handoff still exposes legacy model-manager
  candidate dictionaries. The new PoC must consume the frozen governed
  records, not silently recreate that selection path.
- The repository has candidate sufficiency and re-observation control, but a
  real external-provider-to-A cognitive loop has not been executed or
  verified in this planning phase.

## Scope boundary

Object detection and OCR are required. VLM is optional and only a later
ambiguity-resolution capability. Face, gesture, pose, SAM, multi-camera,
long-running video, optimization, production deployment, learning, memory
retrieval and semantic compression remain deferred.

