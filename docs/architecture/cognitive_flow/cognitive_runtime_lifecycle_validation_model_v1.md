# Cognitive Runtime Lifecycle Validation Model v1

The interrupt fixture validates the temporary lifecycle:

```text
Create Candidate -> Active Candidate -> Interrupted Candidate
  -> Resume Candidate -> Close Candidate
```

It requires `Interrupt Candidate -> Attention Reallocation Candidate -> Process Adjustment Candidate`. The lifecycle is explicitly not State, Memory, Experience, or Action.

