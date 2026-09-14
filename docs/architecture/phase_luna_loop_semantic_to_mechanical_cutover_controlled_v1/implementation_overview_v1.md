# Implementation overview

The package
`loop_semantic_to_mechanical_cutover_controlled` adds three supplied-input
records:

- `LoopResumeMechanicalInputV1`
- `LoopLocalDispositionRecordV1`
- `LoopClosureMechanicalInputV1`

The adapter validates an A/Brain grant, concern/work scope, source state
version, and Loop grant before reusing the existing mechanical command engine.
The Loop return surface remains mechanical state, refs, closure/freeze refs,
and trace/provenance only.

