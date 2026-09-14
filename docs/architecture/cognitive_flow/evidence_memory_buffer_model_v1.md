# Evidence Memory Buffer Model v1

## Purpose

Evidence Memory Buffer is a short-term cache for fragmented capability output.
It retains raw references and Evidence Candidates until assembly, validation,
expiry, withdrawal, or handoff to a Reality Candidate.

## Required metadata

Each buffered item preserves source, capability reference, timestamp, provenance,
confidence, uncertainty, temporal window, spatial scope, and retention deadline.

## Boundary

The buffer is not a Memory of decisions or experience. It does not reason,
predict, plan, evaluate, create a Goal, or choose an Action. It does not predict.
It does not plan. Buffer expiry removes
stale evidence from the working set; it does not turn missing information into a
fact.
