# Role / Perspective State Ownership v1

| State | Classification | Target handling |
|---|---|---|
| Role identity/version | AUTHORITATIVE source state | applicable Self/Relationship/External source |
| Role lifecycle/applicability | AUTHORITATIVE source governance | source contract, with Brain constraints |
| Role candidate/inferred Role | CANDIDATE | field/observation/user/external producer |
| Perspective Projection Function | LOCAL_DERIVED FUNCTION | conceptual transformation boundary; no Manager |
| Perspective Projection Result | CANDIDATE / LOCAL_DERIVED | versioned augmented working view |
| Perspective identity | LOCAL_DERIVED / REFERENCE_ONLY | projection ref in envelope/snapshot |
| Perspective version | LOCAL_DERIVED | derived from Role/source/envelope versions |
| adopted Perspective | CANDIDATE or cycle-scoped selected ref | Brain/A governed adoption |
| A/B hypothetical perspective | HYPOTHETICAL | branch-local only |
| source refs | REFERENCE_ONLY | source owners |
| Context/Task/Intent refs | REFERENCE_ONLY | respective owners |
| Memory/Permission refs | REFERENCE_ONLY | respective owners |

Augmented attributes are derived, not authoritative source state. Base
attributes and relations remain with their source owners. An augmentation cache,
if introduced later, is derived, versioned, invalidatable and disposable; cache
loss must not destroy base information.
loss must not destroy base information. Emotion-related state is deferred and
is not part of the current Perspective ownership contract.

No authoritative Role/Perspective payload is duplicated in Semantic, A,
Intent, Task, Working Envelope, Cognitive State, or Loop.
