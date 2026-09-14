# Luna Cognitive State Management Architecture v1

## Position

Cognitive State Management is an architecture-only model for representing Luna's current cognitive operating condition. It extends Self Regulation and Self Rhythm without becoming a runtime state machine, scheduler, or controller.

## State vocabulary

The canonical state candidates are `NORMAL`, `IDLE`, `FOCUS`, `PROTECTION`, `DEGRADED`, and `RECOVERY`. A state describes the condition in which cognition should be considered; it does not command a model, hardware device, Runtime, or Action.

## Inputs and outputs

State candidates may be informed by Self Regulation, Resource Awareness, Field Complexity, Task Demand, Capability Health, and Runtime Health. The output is a candidate with a reason, evidence references, confidence, resource implications, and unknowns. Self Regulation proposes stability constraints; Self Rhythm supplies a rhythm hint; Cognitive Kernel consumes the candidate; Brain retains cognitive judgment; Runtime may eventually execute an admitted policy.

## Boundary

There is no automatic transition, scheduler mutation, model switching, hardware control, memory write, identity change, goal change, or emotion runtime in this phase. A candidate must preserve its evidence and remain reviewable.

