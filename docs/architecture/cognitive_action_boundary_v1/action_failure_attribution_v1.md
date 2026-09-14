# Action Failure Attribution v1

## Failure feedback

```text
Action Failure
      ↓
Outcome Evidence
      ↓
Difference Analysis
      ↓
Cause Attribution Candidate
      ↓
Adaptation Candidate
```

Failure does not automatically mean Decision Failure. Cause Attribution may
retain Environment Change, Capability Gap, Execution Gap, Information Gap,
Understanding Gap, Random Event, Decision Factor, or Unknown Factor. Multiple
factors may coexist and confidence must remain explicit.

Examples: a reasonable walking Decision followed by a road closure may be an
Environment Change; a correct navigation Decision with a failed turn may be an
Execution Gap; a failed distant-text request may be a Capability Gap. None
directly rewrites Goal, Self Model, Decision Policy, Reality, or Action Policy.

Cause Attribution is explanation, not blame or responsibility assignment. The
Reducer remains the sole State mutation authority.

multiple factors may coexist in one outcome trace, and no single cause is
assumed without evidence.
