# Action / Capability / Provider Boundary v1

Capability answers what Luna can functionally do; Action is the concrete
operation; Provider/Runtime Executor is an implementation that performs it.

`Action Candidate → required Capability → Logical Resolution → Runtime
Admission → Provider Admission → Provider execution → Action Result`.
Action Governance does not own Capability taxonomy, Model/Provider selection,
model files, runtime health or Provider invocation.
