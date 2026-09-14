# Cognitive Trigger Orchestration Model v1

## Inputs

External Trigger Candidates: Vision Change, Audio Change, Language Input, Sensor Event.

Internal Trigger Candidates: Task Window, Temporal Change, Risk Increase, Experience Match, Activation Request.

## Output

A Cognitive Tick Candidate records trigger references, context boundary, priority candidate, expected cognitive need, resource-budget reference, provenance, and trace.

Trigger Assessment may defer or coalesce candidates when value is low or resources are constrained. Trigger != Decision, Action, Permission, scheduler invocation, or State transition.
