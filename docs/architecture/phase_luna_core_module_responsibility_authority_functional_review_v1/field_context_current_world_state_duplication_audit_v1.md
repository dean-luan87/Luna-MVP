# Field / Context / Current World State Duplication Audit v1

| Data | Canonical treatment | Risk |
|---|---|---|
| Entity identity/object record | Field or external source ref; Current World candidate ref/derived view | duplicate mutable entity in Current World |
| Base attributes | source/Field-owned or evidence refs | perspective overlay rewriting base |
| Relations | Field/evidence source plus candidate relation refs | semantic relation silently becoming Field |
| Location/spatial state | Field/map/SLAM source refs as applicable | Context copying geometry as authority |
| Temporal validity | Field/evidence/Context validity refs | stale payload accepted as current |
| Role/Perspective refs | source/derived projection refs | Context or snapshot mutating Role |
| Intent refs | Intent Governance ref/version | Context/Task duplicate Intent lifecycle |
| Task refs | Task ref/version | Current World or Context completing Task |
| Field payload | Field source/read projection | second mutable owner in Current World |
| Context payload | Context envelope ref/derived assembly | snapshot storing a second context store |
| Current World payload | candidate-only, versioned, provenance-preserving | accidental truth promotion |

## Rule

References, versions and derived summaries are not duplication. A second
mutable copy of source payload is duplication risk. Current assets mostly use
read-only/reference-only/candidate-only flags; future runtime must preserve
that strategy.
