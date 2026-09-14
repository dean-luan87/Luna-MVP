# Cognitive Module Coordination Model v1

## Default coordination order candidate

`Perception -> Situation Understanding -> Context -> Goal / Intent -> Attention -> Sufficiency -> Routing -> Reasoning / Future Space -> Evaluation`.

This is a dependency-aware request order, not a mandatory synchronous call chain. Field change, risk increase, Activation, or conflict can request refresh of an earlier stage. Each subsystem receives signals and returns candidates through the shared signal contract.

No module obtains another module's authority. Perception does not decide; Context does not mutate Field; Attention does not retrieve Memory as truth; Reasoning does not produce Fact; Evaluation does not execute Action.
