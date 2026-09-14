# A3 Evidence Context Translation Layer Controlled DryRun Plan v1

## Objective

This DryRun verifies the first controlled path:

```text
External Evidence Fixture → Translation Skeleton → Cognitive Primitive Candidate → Independent Verification
```

It is not Runtime, model integration, real sensing, Fact Admission, Decision, Action, Context writeback, State mutation, Memory update, or Learning Candidate Admission.

## Fixture Scope

Five immutable reference-only fixtures cover OCR, Vision, Spatial/SLAM, Audio, and provenance/trace. Fixture labels document expected candidate vocabulary but Skeleton does not generate semantic conclusions; each output remains `translation_not_executed`.

## Execution Boundary

The Runner calls only `CognitiveTranslationSkeletonV1`. It creates no external call, model invocation, network/database access, or writeback. The Verifier reads serialized output only and imports neither Runner nor Skeleton.
