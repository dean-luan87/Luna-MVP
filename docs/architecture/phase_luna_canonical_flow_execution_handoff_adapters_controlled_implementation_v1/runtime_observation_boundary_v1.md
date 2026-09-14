# Runtime Admission → Observation Boundary v1

Only a current `READY_FOR_EXECUTABLE_CANDIDATE` assessment plus an
Executable Capability candidate can form an Observation Request candidate.

Blocked, degraded, stale, mismatched or under-provenanced runtime inputs are
rejected. Observation owns request identity/lifecycle; the adapter does not
perform Provider Admission, invocation or evidence production.

