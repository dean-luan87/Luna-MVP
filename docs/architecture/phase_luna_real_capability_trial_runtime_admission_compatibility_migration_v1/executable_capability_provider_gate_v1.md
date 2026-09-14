# Executable Capability Provider Gate

The new gate creates `ExecutableCapabilityCandidateV1` through the verified
candidate adapter. Existing `VisionProviderAdmissionCandidateV1` construction
remains unchanged after the gate, except that `provider_admitted` and
`model_admission_ref` require the executable candidate.

The Provider adapter remains responsible for Provider admission and execution.
The migration does not select a new Provider, load a new model, or alter YOLO
invocation behavior.

