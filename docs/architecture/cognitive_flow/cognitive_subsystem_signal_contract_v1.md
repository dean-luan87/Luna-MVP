# Cognitive Subsystem Signal Contract v1

## Signal form

Every subsystem signal must contain, where applicable: signal type, source subsystem, target/requested capability, candidate payload/reference, context/temporal/spatial/task/risk boundary, uncertainty/confidence candidate, provenance, and trace.

## Example

Perception may emit:

```text
Object Candidate: Traffic Light
State Candidate: Red
Relationship Candidate: Vehicle Flow Stopped
Constraint Candidate: Traffic Constraint
```

Context may emit Crossing-Road Situation, Goal, and Risk candidates. Attention may request traffic-direction/distance observation candidates. Reasoning may return Cross/Wait/Ask-Human Future candidates. Evaluation may return Safety-over-Time Value candidates.

No signal is a Fact, Command, Decision, Action, Permission, or State mutation.
