# Real Provider Execution Integration v1

This phase connects one existing local provider implementation to the
canonical provider-runtime and observation-ingress path. It selects the
repository-declared YOLO11n local vision provider and stops after A-Route /
Cognitive State Formation. Decision, Task, Action, and Runtime Executor
execution remain disabled.

The phase is separate from the recorded provider-result bridge. Its
`provider_real_execution_verified` value is derived from the actual provider
adapter result and is not asserted by the Agent before terminal execution.
