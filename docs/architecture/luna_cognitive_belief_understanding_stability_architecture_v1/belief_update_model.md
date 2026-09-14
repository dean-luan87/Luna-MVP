# Belief Update Model v1

Belief Update is an interface only:

```text
Current Belief + New Evidence + Reliability + Context Change
                 + Reality Validation Result
                   -> Belief Update Candidate
```

Update types are `Strengthen`, `Weaken`, `Replace`, `Invalidate`, and `Suspend`. The original Belief, Evidence, Field, timestamp, confidence delta, and Unknown remain preserved. No update directly writes Reality, Memory, Schema, Self, Identity, Goal, or Action.

