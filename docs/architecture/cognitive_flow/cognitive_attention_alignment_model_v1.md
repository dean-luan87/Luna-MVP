# Attention Alignment Model v1

## Alignment chain

```text
Original Intent
        ↓
Attention Selection Candidate
        ↓
Evidence Candidate
        ↓
Situation Update Candidate
        ↓
Attention Alignment Evaluation Candidate
```

The evaluation asks whether obtained information improved support for the
Original Intent, rather than whether a Provider returned data. For a pharmacy intent, reading many unrelated advertisements is technical output with low alignment.

Alignment is candidate-only. It does not decide, act, retry a Provider, or
change Attention strategy automatically.
