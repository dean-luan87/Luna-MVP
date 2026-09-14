# Implementation Mapping

Implementation is additive under:

`capabilities/midplatform/model_manager/registries/universal_capability_slot/`

New feedback governance and fixture modules reuse the existing Slot/Module,
Gap, Self, Scope, Resolution, and Invocation contracts. The only canonical
type extension is optional feedback reference visibility on
`CapabilitySelfViewV1` plus the new feedback candidate records in the existing
types module. No Registry, Resolver, Model Manager, Provider, Gateway, FPO, or
Brain owner is duplicated.
