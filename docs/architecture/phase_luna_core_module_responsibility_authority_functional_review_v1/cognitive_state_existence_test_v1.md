# Cognitive State Formation Existence Test

| Architecture | Unique responsibility | Authority clarity | Duplication risk | Testability | Decision |
|---|---|---|---|---|---|
| A. Independent State Formation | version-aligned candidate snapshot and provenance | clear if candidate-only | medium, controllable | high | viable |
| B. State inside Working Envelope | refs/constraints and snapshot collapse | ambiguous source vs derived state | high | medium | reject as target |
| C. State as Semantic output | semantic outline plus state collapse | blurs representation and semantics | high | medium | reject as target |
| D. State inside A | local reasoning state plus source assembly | risks A owning external state | high | low boundary clarity | reject as target |

## Decision

An independent but narrowed module remains justified for version alignment, snapshot consistency, candidate Current World/state assembly and provenance. It must not become a semantic reasoner or authoritative state owner.
