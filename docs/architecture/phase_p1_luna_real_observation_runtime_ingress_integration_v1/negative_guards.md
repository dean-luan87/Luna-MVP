# Negative Guards

The runner contains two ingress negatives:

1. `MALFORMED_RUNTIME_OBSERVATION`: Gateway rejects an envelope missing its
   canonical capability identity and produces no Evidence.
2. `PROVIDER_UNAVAILABLE`: Gateway rejects an unavailable provider/capability
   result and produces no Evidence.

The missing-information case is admitted as candidate Evidence, then the
existing Cognitive State Formation logic produces sufficiency status
`INSUFFICIENT` and an Information Gap. `INSUFFICIENT_EVIDENCE` remains a
hypothesis-state label, not the sufficiency status. The case does not
fabricate evidence or stop early.

All phase outputs require false for provider/model invocation by this adapter,
live observation execution by the fixture runner, Decision/Task/Action
execution, Runtime Executor invocation, Field mutation, and World Truth
declaration.
