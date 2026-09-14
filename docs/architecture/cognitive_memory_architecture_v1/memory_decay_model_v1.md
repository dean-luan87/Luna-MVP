# Memory Decay Model v1

## Decay inputs

Memory decay considers Time, Confidence, Importance, Reuse, and Contradiction.
The resulting Decay Candidate affects retrieval priority, not Reality truth.

```text
Time + Confidence + Importance + Reuse + Contradiction
                      ↓
                 Decay Candidate
                      ↓
          Retrieval Priority / Archive Candidate
```

Decay is not simple deletion. A low-reuse but high-importance historical event
may remain Archived and retrievable with lower confidence. A contradicted item
is marked Conflict and cannot silently influence Situation.

## Lifecycle

Candidate → Working → Retained → Decaying → Archived → Released Candidate.

Transitions require provenance, scope, current-Reality reconciliation, and
retention policy. No automatic purge, automatic learning, or Memory Runtime is
implemented.

No automatic learning. No Memory Runtime.
