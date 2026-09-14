# Attention / Role-Perspective / Semantic Boundary v1

Role/Perspective may change semantic relevance. Semantic Module may expose
relations, unresolved slots and relevance features. Both are inputs to
Attention, not Attention owners.

Target path:

`Role/Perspective refs → Semantic/A relevance impact → Attention priority
candidate → Observation/FPO`.

Attention may consume Perspective relevance features directly when they are
already governed refs, but it must not create Role, select Perspective,
perform projection, expand/fold semantics or judge the cognitive consequence.

Example: a parent Role may make a child-related region more relevant. A judges
whether that changes Need; Attention ranks an eligible focus candidate.
