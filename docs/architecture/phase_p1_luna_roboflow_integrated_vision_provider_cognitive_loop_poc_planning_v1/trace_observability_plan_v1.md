# Trace and Observability Plan

## Required reversible chain

One trace must link:

`goal/concern/grant → envelope → reasoning cycle → requirement → attention /
observation request → capability/runtime/provider admission → Roboflow
request/invocation → provider result → evidence → gateway → Current World /
Field candidate → hypothesis/sufficiency → next observation or decision`.

## Minimum observable record per edge

Reuse existing edge/vision trace conventions. Capture transition/trace id,
parent transition refs, Concern and reasoning-cycle refs, producer,
consumer, authority/responsibility owner, transition class, input/output
refs and versions, admission/validation status, evidence/constraint refs,
failure/invalidation refs, next target, provenance, candidate-only status,
runtime/provider execution flags and timestamps.

## Provider-specific provenance

Record provider request id, external workflow/model/version, frame/ROI/source
refs, raw output ref, adapter translation ref, and correlation to the
Observation Request. Raw Roboflow schema may be retained behind the adapter;
the cognitive trace exposes references and normalized evidence, not a new
provider-native semantic model.

## Verification questions

The future PoC verifier must answer: can provenance be reversed from a
hypothesis or re-observation request to the original frame and provider
result; are versions preserved independently; did any candidate become Truth;
did a failed/stale provider result return to the responsible boundary; and
did Roboflow cause any unauthorized selection, mutation or closure?

