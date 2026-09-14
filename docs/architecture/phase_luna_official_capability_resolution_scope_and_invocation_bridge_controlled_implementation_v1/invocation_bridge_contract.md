# Invocation Bridge Contract

`build_scoped_invocation_candidate()` accepts only when scope is valid and
resolution is `READY_CANDIDATE`. It carries requirement, Module, Slot, scope
assessment, implementation/model/provider refs, Gateway/FPO refs, execution
boundary, trace refs, and candidate-only guards.

It creates no provider call, model inference, camera activation, or runtime
side effect.
