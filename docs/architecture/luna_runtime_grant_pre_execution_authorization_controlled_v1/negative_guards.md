# Negative guards

The phase has no provider/model invocation or selection, resource or slot
reservation, capability activation, execution instance creation, provider
session start, Gateway submission, runtime observation, evidence ingress,
truth/world mutation, Attention, Decision, Task, Action, ranking, scoring,
winner selection, fallback, semantic string inference, or upstream mutation.

`GRANTED` is explicitly tested as `GRANTED != STARTED`,
`EXECUTION_READY != EXECUTION_AUTHORIZED` in the reverse direction, and
`Capability/Provider admission != Runtime Grant`. Expired, revoked, and stale
inputs fail closed without interrupting any live runtime.
