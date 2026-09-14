# Luna Action Runtime Foundation Architecture v1

## Position

Action Runtime Foundation is the future execution substrate below the Action
Boundary. It receives an Approved Action Candidate, creates a bounded context,
tracks lifecycle and resources, collects and verifies outcomes, and feeds
evidence back to cognition. This phase defines contracts only.

```text
Approved Action Candidate
        ↓
Execution Context
        ↓
Action Lifecycle / Resource / Scheduler Boundary
        ↓
Action Executor (future)
        ↓
Monitor → Outcome Collector → Verification
        ↓                         ↓
Recovery Candidate          Outcome Evidence
        ↓                         ↓
Action Trace → L2 Experience / Learning
```

## Boundary principles

- Action Runtime executes only an already-approved candidate; it cannot create
  or revise a Decision, Goal, Value, or Constitution.
- Execution Context fixes target, environment, permission, risk, timeout, and
  trace before any future executor is admitted.
- Scheduler and Adapter are boundaries, not implementations.
- Outcome is richer than success/failure: expected, actual, difference, and
  confidence are preserved, including partial and unexpected outcomes.
- Recovery diagnoses and proposes retry, alternative, or abort; it does not
  silently change goals or values.
- This phase has no hardware, robot, API, device, Provider, or external side
  effect.

