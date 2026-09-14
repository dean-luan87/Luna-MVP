# Experience / Memory Boundary Review

## Current clean boundary

`ExperienceCandidateV1` and `MemoryCandidateV1` are candidate-only and non-persistent by default. Brain Golden Baseline guards memory write, experience learning, online learning and semantic compression.

Experience can be a read-only prior or filter input. It cannot override Current World, directly control Loop, declare World Truth, automatically drive A decisions, or mutate Memory.

Loop closure already reserves:

`Runtime Trace → Loop Closure Record → Loop Package reference → Experience Candidate reference → Experience Governance`.

## Deferred work

- semantic compression;
- Experience mutation/admission runtime;
- Memory mutation/persistence runtime;
- future cognitive prior generation;
- Experience/Short-Path Filter runtime.

Finding: boundary `KEEP`; direct Experience→Loop/Memory mutation paths `FORBIDDEN`; Filter-to-A integration is a P1 contract gap.
