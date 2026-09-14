# Cognitive Subsystem Interaction Boundary Contract v1

## Required exchange boundary

Subsystems exchange candidate request/response signals with provenance, trace, uncertainty, Context boundaries, and source/target declarations. They do not directly call to command a Decision, Action, Permission, Fact, knowledge mutation, representation mutation, Memory/Hive write, or State mutation.

## Negative guards

- Signal != Fact.
- Signal != Command.
- Candidate Flow != Action Flow.
- Observation != Belief Authority.
- Validation != Fact Authority.
- Adoption Candidate != Adoption.
- Perception != Decision.
- Context != Goal Override.
- Attention != Knowledge Change.
- Reasoning != Fact.
- Evaluation != Action.
- Experience != Rule.
- Governance != Reality Change.
- Emotion != Decision.
- World Model != Reality Authority.
- Hive != Global Rule.
- Language != Cognition Authority.
- Reducer remains the only State Mutation Authority.
