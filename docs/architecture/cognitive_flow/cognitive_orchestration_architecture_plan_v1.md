# Cognitive Orchestration Architecture Plan v1

- Phase: `Phase-Cognitive-Orchestration-Architecture-Planning-v1-001`
- Stage: Planning Only
- Previous Phase: `Phase-Cognitive-Activation-Architecture-Planning-v1-001`
- Previous Decision: `COGNITIVE_ACTIVATION_ARCHITECTURE_PLANNING_READY_WITH_NOTES`

## Position

`Trigger -> Cognitive Tick Candidate -> Orchestration Candidate -> Cognitive Modules -> Candidate Integration Candidate -> Evaluation Candidate -> Experience Feedback Candidate`.

Cognitive Orchestration coordinates participation, candidate ordering, integration, conflict visibility, and resource-investment suggestions across cognitive subsystems. It is not Decision Authority, Runtime Executor, scheduler, model/device caller, Action, Permission, or State authority.

## Candidate-first flow

`Observation -> Candidate -> Evaluation -> Validation -> Adoption Candidate`.

No Observation-to-Belief-to-Action shortcut is permitted. Orchestration cannot make any candidate a Fact, Decision, Action, or State mutation.
