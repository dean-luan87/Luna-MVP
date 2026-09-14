# Dynamic Flow Compatibility Wrapper

The wrapper consumes an existing `DynamicCognitiveLoopOutputV1` candidate and
maps eligible output fields into A-owned decision candidates:

`Dynamic Flow output → A decision candidates → Loop mechanical commands`

The source owner is retained as provenance:
`Cognitive Flow Governance`.

The semantic authority reference is A. The wrapper does not rewrite or delete
`DynamicCognitiveFlowEngineV1`, does not invoke it at runtime, and does not
make Loop a semantic judge.
