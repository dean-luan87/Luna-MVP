# Communication Path Matrix

| Path | Status | Contract |
|---|---|---|
| Brain → A | DIRECT_ALLOWED | grant + working envelope |
| A → Brain | DIRECT_ALLOWED | outcome/evaluation/grant feedback |
| A → B-CR | DIRECT_ALLOWED | bounded request + derived grant |
| B-CR → A | DIRECT_ALLOWED | non-binding result/handoff |
| A → Loop | VIA_ADAPTER | supplied semantic refs → mechanical command |
| Loop → A | REFERENCE_ONLY | mechanical state/result refs |
| Brain → Loop | VIA_BRAIN | accepted governance/mechanical refs only |
| Task → Loop | REFERENCE_ONLY | task/lifecycle refs, no cognition |
| B-CR → Loop | FORBIDDEN | B must return to A |
| Observation → Loop | REFERENCE_ONLY | evidence/admission refs |
| Capability → Loop | REFERENCE_ONLY | requirement/resolution/admission refs |
| Experience → Loop | FORBIDDEN | prior refs go through envelope/A |
| Role → A | VIA_ENVELOPE | versioned role/perspective refs |
| Field → A | VIA_ENVELOPE | source state refs |
| Emotion → A | VIA_ENVELOPE | modulation refs |
| Task → A | VIA_ENVELOPE | constraint/completion refs |
| Context → A | VIA_ENVELOPE | context refs |
| A → Capability | DIRECT_ALLOWED | Cognitive Requirement/category |
| A → Observation | VIA_CAPABILITY_BRIDGE | requirement/admission request |
| Brain → Provider | FORBIDDEN_DIRECT | Brain governs policy, not implementation selection |
| A → Provider | FORBIDDEN_DIRECT | A requests information category |
| Loop → Capability/Observation | FORBIDDEN_SEMANTIC | Loop records supplied refs only |
| Dynamic Flow → downstream semantic consumer | FORBIDDEN_DIRECT | compatibility output must be interpreted by A |

Bypass findings: legacy Dynamic Flow callers, old Loop continuity helpers, distributed Role/Perspective propagation, and the incomplete A→Observation/Capability return bridge.
