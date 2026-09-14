# Execution Boundary

Actual invocation is permitted only when `execution_mode=LIVE_RUNTIME`, the
repository-backed Capability/Model/Provider and Runtime Admission references
are valid, the local model asset is present and matches its declared checksum,
and the bounded raw frame is admitted, and the provider admission carries the
canonical FPO `CapabilityRequirementCandidateV1.requirement_id`.

The normalized provider-runtime resolution requirement is not an equivalent
substitute: its `provider-requirement:...` identity is retained for resolution
lineage, while admission uses the source `capability-requirement:...` identity.

The provider may load/invoke the local model and return native detection
candidates. It may not create Fact or World Truth, mutate Field, or invoke
Decision, Task, Action, Runtime Executor, device control, or external
side-effect paths. `provider_invoked` and `model_invoked` are copied from the
actual provider adapter result.
