# Evaluation Run Contract

Implementation: `capabilities/evaluation/level1_cognitive_evaluation_run/types_v1.py`.

`EvaluationRunCandidateV1` records:

- stable run/protocol identity, plane, and Level-1 level;
- Dataset, Sample, and Cognitive Test Case refs plus versions;
- Luna code/config version refs with explicit availability state;
- conditions, perturbations, capabilities, and observation budget;
- start/completion availability semantics;
- existing trace/profile/gap refs;
- result and failure-attribution refs;
- provenance, source versions, invalidation refs;
- A-Route bridge and White-box attachment status;
- comparison eligibility and runtime-metric availability;
- negative execution/mutation/promotion flags.

`EvaluationRunRecordV1` wraps the candidate as immutable historical evaluation evidence. It is not Field state, World Truth, runtime cognition, Memory, Experience, or Knowledge.

Unavailable values use `unavailable`, `not_observed`, `planned`, or `not_applicable`; they are never replaced by measured-looking zeroes.

