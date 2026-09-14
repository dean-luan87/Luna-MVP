# A/B Concurrency Candidate Boundary

`ABConcurrentStateCandidateV1` represents A ACTIVE + B ACTIVE, or A PAUSED/WAITING + B ACTIVE, without threads or scheduling. Shared references are read-only; A and B local state references remain isolated. B completion does not automatically resume A.
