# Real Input / Dynamic Cognitive Loop Integrated Controlled Implementation

The integration layer is additive and candidate-only under the existing Cognitive Flow owner.

## Contract

B1 supplies an already-produced real visual evidence reference shaped as a `CurrentWorldCandidateV1`. B2 consumes that candidate read-only and returns the existing Cognitive State Formation and Cognitive Flow outputs. The Dynamic Cognitive Flow engine then selects one current minimum Need from a provisional, non-binding plan. Only that Need is passed through the existing Need-to-Capability Requirement bridge.

Capability scope is evaluated before readiness resolution and invocation-candidate formation. A controlled Capability Experience fixture can report execution outcome, requirement satisfaction, and task contribution independently. None of these fields is promoted to Goal sufficiency. The resulting evidence is fed to the existing Dynamic Flow engine, which creates a new candidate state version and can continue, replan, request more evidence, defer, or stop with `STOP_SUFFICIENT`.

## State and stale requirements

Every dynamic evidence update names its source state version. A new accepted update advances the state version. The existing bridge reassessment marks a requirement from an older state `SUPERSEDED` when new evidence exists; the Dynamic Flow output excludes stale requirements from eligible invocation candidates.

## Reconsideration

Unavailable, degraded, and out-of-scope capability candidates remain governed candidates. They produce reconsideration/request-more-evidence or a capability gap plus alternative Need. No fallback hallucination, scope bypass, acquisition, or runtime call is created. B4 references are carried back to Cognitive Flow and FPO reobserve remains a candidate handoff.

## Verification

The runner covers 28 cross-module scenarios and prints JSON when run directly. The verifier checks the runner result, negative guards, exact source set, and documentation set, then prints JSON and exits non-zero on failure. The files are intentionally left for user-terminal verification.
