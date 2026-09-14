# Luna Execution Profile Plan

## Purpose

An Execution Profile is a single evaluation-run record that joins technical
model output with the observed cognitive chain. It is an evaluation artifact,
not runtime state and not World Truth.

## Required groups

- identity: `execution_profile_id`, phase, attempt, test case, task;
- dataset/sample: dataset/version, sample, split, condition, input refs;
- governance: capability requirement, capability/model/provider refs and
  versions, admission/binding refs;
- observation cycles: demand/request IDs, cycle count, ROI/frame refs,
  requested capabilities;
- evidence: count, kinds, quality, uncertainty, conflict, freshness, source
  diversity, normalized evidence refs;
- cognition: hypothesis create/revision refs, sufficiency statuses and
  transitions, information gaps, re-observation candidates/count;
- handoff: Decision Governance target or candidate ref, stop reason;
- performance: latency and invocation duration when observable; resource usage
  as `planned` when unavailable;
- failures: failure/gap taxonomy refs, retries/retry candidates, stale and
  invalidation refs;
- outcome: task outcome candidate and provenance, never authoritative closure;
- trace: trace/provenance/source-version/TestBoard refs.

## State semantics

Every field should distinguish `observed`, `derived_candidate`, `planned`,
`unavailable`, and `not_applicable`. Missing instrumentation is not zero.

## Persistence

The future profile should reference Model Test Result Envelope, Model Test
Trace, Evaluation Report, and protected TestBoard artifacts. It should not
create a competing output hierarchy.
