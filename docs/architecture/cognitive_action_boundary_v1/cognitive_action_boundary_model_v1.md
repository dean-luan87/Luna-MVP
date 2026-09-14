# Cognitive Action Boundary Model v1

## Purpose

Action Boundary separates a Brain Decision from any later execution system. It
defines how a Decision Candidate becomes an Action Intent and an Action Request
without becoming an Action Command or executing anything.

```text
Brain Decision Candidate
        ↓
Action Intent
        ↓
Action Request
        ↓
Action Permission Candidate
        ↓
Execution Boundary
        ↓
Runtime (future, outside this phase)
        ↓
Outcome Evidence
```

Decision is not Execution. “Reach the airport” is a Decision-level intent; it
is not “move the robot.” Action Intent expresses the required capability or
execution support. Action Request asks an authorized execution boundary to
prepare or perform work; it is not a command.

## Authority boundaries

Brain retains Goal, Value, Decision, and authorization judgment. Action
Boundary may validate request shape, constraints, capability requirements,
authorization level, and risk classification. Runtime may eventually execute
an admitted request, but cannot interpret Reality, modify Goal, modify
Decision, or become a cognitive subject.

Action cannot directly modify Reality. The only permitted reality feedback path
is External World Change → Evidence → Reality Update Candidate → Reducer.
Action Failure becomes Outcome Evidence and Cause Attribution Candidate; it does
not prove Decision Failure.

## Permission and safety

Low-risk requests such as a weather query or observation-frequency adjustment
may form an automatic-permission candidate. High-risk requests such as payment,
data deletion, environmental change, or movement require an authorization
candidate and appropriate Brain/User authority. A Safety Action Candidate from
Neural Fast Path is still a candidate; this architecture phase does not execute
it.

No real Action Runtime, hardware control, robot movement, payment, external
operation, automatic execution, Emotion, Role, Social Runtime, or B is enabled.

It cannot modify Goal or modify Decision.
Environment Change, Capability Gap, Execution Gap, Information Gap,
Understanding Gap, Random Event, and Unknown Factor remain explicit candidate
classes for attribution.
