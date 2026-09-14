# Cognitive State Transition Model Definition v1

`CognitiveStateTransitionCandidateV1` may retain Current Cognitive State, Monitoring, Field/Context/Role/Goal/Survival/Time/Cognitive Failure evidence references, Transition Type, transition reason, uncertainty, provenance, and trace.

Types are **Maintain**, **Update**, **Switch**, **Suspend**, **Resume**, **Terminate**, and **Restart**. Each is a possible cognitive-state handling label, never a state mutation, Decision, Action, command, or permission.

Output remains `candidate_only=true`, `not_fact=true`, `not_state_mutation=true`, `not_decision=true`, `not_action=true`, `not_permission=true`, and `not_memory=true`.
